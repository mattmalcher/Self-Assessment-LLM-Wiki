"""Stage 2: corpus chunk -> structured JSON note, cached by chunk hash."""
from __future__ import annotations

import hashlib
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

from .. import runlog
from . import schema, store
from .chunk import Chunk, chunk_file
from .config import CORPUS_DIR, PROMPTS_DIR
from .llm import Backend, LLMError, extract_json

SYSTEM = (PROMPTS_DIR / "extract.md").read_text()

# How many times a chunk is re-asked when the model returns something that
# isn't a valid note. Each attempt is a fresh `backend.call` (which has its own
# backoff for transport failures) with the validator's complaints appended, so
# this is a schema-repair budget, not a flake budget.
VALIDATION_ATTEMPTS = 3

# Recorded on every cached note. The chunk hash alone cannot tell a note
# written under an older prompt (or a weaker model) from a current one, so
# tuning extract.md mid-run would otherwise leave the corpus silently mixed.
PROMPT_HASH = hashlib.sha256(SYSTEM.encode()).hexdigest()[:16]


@dataclass
class Plan:
    doc: str
    meta: dict
    chunks: list[Chunk]
    todo: list[Chunk]
    orphans: int
    stale_prompt: list[Chunk] = field(default_factory=list)
    # Cached chunks whose note fails `schema.validate_note`. They are a subset
    # of `todo`: a malformed note is work outstanding, not coverage.
    invalid: list[Chunk] = field(default_factory=list)


def corpus_docs(only: list[str] | None) -> list[Path]:
    paths = sorted(p for p in CORPUS_DIR.rglob("*.md"))
    if only:
        wanted = {Path(o).as_posix().removeprefix("corpus/") for o in only}
        paths = [p for p in paths
                 if p.relative_to(CORPUS_DIR).as_posix() in wanted
                 or any(p.relative_to(CORPUS_DIR).as_posix().startswith(w.rstrip("/") + "/") for w in wanted)]
    return paths


def plan(only: list[str] | None = None) -> list[Plan]:
    """Work out, without calling any model, which chunks need extracting."""
    plans: list[Plan] = []
    for path in corpus_docs(only):
        meta, chunks = chunk_file(path, CORPUS_DIR)
        doc_rel = path.relative_to(CORPUS_DIR).as_posix()
        data = store.load(doc_rel)
        live = {c.hash for c in chunks}
        cached = data["chunks"]
        orphans = len([h for h in cached if h not in live])
        invalid = [c for c in chunks
                   if c.hash in cached and not schema.entry_is_valid(cached[c.hash])]
        invalid_hashes = {c.hash for c in invalid}
        todo = [c for c in chunks if c.hash not in cached or c.hash in invalid_hashes]
        stale_prompt = [c for c in chunks
                        if c.hash in cached and c.hash not in invalid_hashes
                        and cached[c.hash].get("prompt_hash") != PROMPT_HASH]
        plans.append(Plan(doc=doc_rel, meta=meta, chunks=chunks, todo=todo, orphans=orphans,
                          stale_prompt=stale_prompt, invalid=invalid))
    return plans


def _prompt(chunk: Chunk, meta: dict) -> str:
    return (
        f"Document: {meta.get('source_id', chunk.doc)}\n"
        f"Source URL: {meta.get('source_url', 'unknown')}\n"
        f"Document type: {meta.get('legislation_type') or meta.get('document_type') or 'unknown'}\n"
        f"Section path: {chunk.heading}\n"
        f"Chunk {chunk.index + 1} of this document.\n\n"
        "--- BEGIN SOURCE CHUNK ---\n"
        f"{chunk.text}\n"
        "--- END SOURCE CHUNK ---\n\n"
        "Return the JSON object now."
    )


def _repair_prompt(base: str, errors: list[str]) -> str:
    """Re-ask for the same chunk, quoting what was wrong with the last answer."""
    complaints = "\n".join(f"- {e}" for e in errors[:10])
    return (
        f"{base}\n\n"
        "Your previous answer for this chunk did not match the required "
        f"schema:\n{complaints}\n\n"
        "Return the complete JSON object again, with every documented key "
        "present, every value a string, no extra keys, and a non-empty `ref` "
        "on every obligation, deadline, amount, penalty and definition."
    )


def extract_note(backend: Backend, chunk: Chunk, meta: dict) -> dict:
    """One chunk -> one *valid* note, or an LLMError.

    A response that isn't JSON, or is JSON of the wrong shape, is a model
    failure the model can fix, so it goes back with the validator's complaints
    rather than being cached as-is. Nothing invalid ever reaches the caller.
    """
    base = _prompt(chunk, meta)
    prompt = base
    errors: list[str] = []
    for attempt in range(VALIDATION_ATTEMPTS):
        raw = backend.call(SYSTEM, prompt)
        try:
            note = extract_json(raw)
        except LLMError as exc:
            errors = [f"note: {exc}"]
        else:
            errors = schema.validate_note(note)
            if not errors:
                return note
        if attempt < VALIDATION_ATTEMPTS - 1:
            prompt = _repair_prompt(base, errors)
    raise LLMError(f"invalid note after {VALIDATION_ATTEMPTS} attempts: "
                   f"{'; '.join(errors[:5])}")


def _unit(doc: str, chunk: Chunk) -> str:
    return f"{doc}#{chunk.index}"


def run(backend: Backend, *, only: list[str] | None = None, limit: int | None = None,
        concurrency: int = 4, stale_prompt: bool = False,
        verbose: bool = True) -> runlog.StageReport:
    """Extract every uncached chunk. Returns a report of what happened.

    A chunk the model never produced a valid note for is a failure, and the
    caller turns that into a non-zero exit. Chunks left untouched by `--limit`
    are `remaining`, not failures: stopping early is what was asked for.

    The extract file is written after every completed chunk, not once per
    document: ITEPA is 238 chunks and a run can take hours, so a Ctrl-C or a
    rate limit an hour in must not discard the work already paid for.
    """
    plans = plan(only)
    budget = limit
    report = runlog.StageReport(stage="extract", unit="chunk")
    pruned_total = 0

    for position, p in enumerate(plans):
        data = store.load(p.doc)
        pruned = store.prune_orphans(p.doc, data, {c.hash for c in p.chunks})
        work = p.todo + (p.stale_prompt if stale_prompt else [])
        todo = work if budget is None else work[:max(budget, 0)]
        pruned_total += pruned
        report.remaining += [_unit(p.doc, c) for c in work[len(todo):]]
        if not todo and not pruned:
            continue
        if verbose:
            invalid_hashes = {c.hash for c in p.invalid}
            broken = len([c for c in todo if c.hash in invalid_hashes])
            restale = len([c for c in todo if c.hash in data["chunks"]]) - broken
            extra = ", ".join(part for part in (
                f"{broken} re-run for a malformed cached note" if broken else "",
                f"{restale} re-run for a stale prompt" if restale else "",
            ) if part)
            print(f"{p.doc}: {len(todo)} to extract"
                  f"{f' ({extra})' if extra else ''}, "
                  f"{len(p.chunks) - len(p.todo)} cached, {pruned} pruned", flush=True)

        data["doc"] = p.doc
        for key in ("source_id", "source_url", "category"):
            if p.meta.get(key):
                data[key] = p.meta[key]
        if pruned:
            store.save(p.doc, data)

        if todo:
            with ThreadPoolExecutor(max_workers=concurrency) as pool:
                futures = {pool.submit(extract_note, backend, c, p.meta): c for c in todo}
                try:
                    for future in as_completed(futures):
                        chunk = futures[future]
                        try:
                            note = future.result()
                        except Exception as exc:  # carry on; the run still fails at the end
                            report.fail(_unit(p.doc, chunk), exc)
                            print(f"  ! {p.doc} chunk {chunk.index}: {exc}", file=sys.stderr)
                            continue
                        data["chunks"][chunk.hash] = {
                            "index": chunk.index,
                            "heading": chunk.heading,
                            "chars": len(chunk.text),
                            "prompt_hash": PROMPT_HASH,
                            "model": f"{backend.name}:{backend.model}",
                            "note": note,
                        }
                        report.succeed(_unit(p.doc, chunk))
                        store.save(p.doc, data)  # checkpoint: never lose a paid-for chunk
                        if verbose:
                            rel = note.get("relevance", "?")
                            print(f"  + [{rel}] {chunk.heading[:80]}", flush=True)
                except KeyboardInterrupt:
                    for future in futures:
                        future.cancel()
                    if data["chunks"]:
                        store.save(p.doc, data)
                    print(f"\ninterrupted; {len(report.succeeded)} chunk(s) saved",
                          file=sys.stderr, flush=True)
                    raise

        if budget is not None:
            budget -= len(todo)
            if budget <= 0:
                print("\nreached --limit; stopping (more chunks remain)", flush=True)
                report.remaining += [_unit(later.doc, c)
                                     for later in plans[position + 1:]
                                     for c in later.todo +
                                     (later.stale_prompt if stale_prompt else [])]
                break

    report.extra["pruned"] = pruned_total
    return report
