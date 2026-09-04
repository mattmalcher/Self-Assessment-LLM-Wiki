"""Stage 2: corpus chunk -> structured JSON note, cached by chunk hash."""
from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

from . import store
from .chunk import Chunk, chunk_file
from .config import CORPUS_DIR, PROMPTS_DIR
from .llm import Backend, extract_json

SYSTEM = (PROMPTS_DIR / "extract.md").read_text()


@dataclass
class Plan:
    doc: str
    meta: dict
    chunks: list[Chunk]
    todo: list[Chunk]
    orphans: int


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
        orphans = len([h for h in data["chunks"] if h not in live])
        todo = [c for c in chunks if c.hash not in data["chunks"]]
        plans.append(Plan(doc=doc_rel, meta=meta, chunks=chunks, todo=todo, orphans=orphans))
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


def run(backend: Backend, *, only: list[str] | None = None, limit: int | None = None,
        concurrency: int = 4, verbose: bool = True) -> tuple[int, int]:
    """Extract every uncached chunk. Returns (extracted, failed)."""
    plans = plan(only)
    budget = limit
    extracted = failed = 0

    for p in plans:
        data = store.load(p.doc)
        pruned = store.prune_orphans(p.doc, data, {c.hash for c in p.chunks})
        todo = p.todo if budget is None else p.todo[:max(budget, 0)]
        if not todo and not pruned:
            continue
        if verbose:
            print(f"{p.doc}: {len(todo)} to extract, {len(p.chunks) - len(p.todo)} cached, {pruned} pruned",
                  flush=True)

        if todo:
            with ThreadPoolExecutor(max_workers=concurrency) as pool:
                futures = {pool.submit(backend.call, SYSTEM, _prompt(c, p.meta)): c for c in todo}
                for future in as_completed(futures):
                    chunk = futures[future]
                    try:
                        note = extract_json(future.result())
                    except Exception as exc:  # one bad chunk shouldn't sink the doc
                        failed += 1
                        print(f"  ! {p.doc} chunk {chunk.index}: {exc}", file=sys.stderr)
                        continue
                    data["chunks"][chunk.hash] = {
                        "index": chunk.index,
                        "heading": chunk.heading,
                        "chars": len(chunk.text),
                        "note": note,
                    }
                    extracted += 1
                    if verbose:
                        rel = note.get("relevance", "?")
                        print(f"  + [{rel}] {chunk.heading[:80]}", flush=True)

        data["doc"] = p.doc
        for key in ("source_id", "source_url", "category"):
            if p.meta.get(key):
                data[key] = p.meta[key]
        store.save(p.doc, data)

        if budget is not None:
            budget -= len(todo)
            if budget <= 0:
                print(f"\nreached --limit; stopping (more chunks remain)", flush=True)
                break

    return extracted, failed
