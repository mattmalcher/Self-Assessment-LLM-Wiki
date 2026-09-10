"""Stage 3: page spec + selected extract notes -> a wiki page in docs/.

Selection is deterministic (path prefixes, relevance tier, regexes over the
heading/summary/topics of each note), so a page's staleness can be decided
without a model call: hash the brief, the prompt, the compose model and a
fingerprint of every selected note, and skip the page when that hash is
unchanged. See `input_hash` for the invalidation contract.
"""
from __future__ import annotations

import hashlib
import json
import re
import textwrap
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

from .. import configcheck, runlog
from ..pipeline import fetch as pipeline_fetch
from . import schema, store
from .config import DOCS_DIR, MANIFEST_PATH, PAGES_PATH, PROMPTS_DIR, REPO_ROOT
from .llm import Backend

SYSTEM = (PROMPTS_DIR / "compose.md").read_text()
RELEVANCE_ORDER = {"core": 0, "related": 1, "none": 2}


@dataclass
class Selected:
    doc: str
    chunk_hash: str
    heading: str
    note: dict
    source_id: str = ""
    source_url: str = ""
    score: int = 0
    # How the note was produced: the hash of prompts/extract.md (which defines
    # the note schema) and the backend:model that answered it. Both are
    # recorded per chunk by the extract stage.
    prompt_hash: str = ""
    model: str = ""


@dataclass
class PageWork:
    spec: dict
    notes: list[Selected] = field(default_factory=list)
    input_hash: str = ""
    stale: bool = True
    reason: str = ""
    excluded_notes: int = 0
    coverage: "AuthorityCoverage" | None = None


@dataclass(frozen=True)
class AuthorityCoverage:
    """Whether the selected evidence includes every authority a page requires."""

    required: tuple[str, ...]
    covered: tuple[str, ...]
    missing: tuple[str, ...]

    @property
    def complete(self) -> bool:
        return not self.missing


@dataclass
class SelectionResult:
    """Selected notes plus the relevant matches hidden by the cost cap."""

    notes: list[Selected]
    excluded: list[Selected]


def load_pages() -> list[dict]:
    """The validated page plan. Raises `configcheck.ConfigError` rather than
    letting, say, a misspelled relevance tier select nothing and compose a
    page out of no notes."""
    pages = configcheck.load_pages(PAGES_PATH)
    errors = configcheck.validate_authority_references(
        pages, pipeline_fetch.load_sources())
    if errors:
        raise configcheck.ConfigError("pages.yml (authority matrix)", errors)
    return pages


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        return {}
    return json.loads(MANIFEST_PATH.read_text())


def save_manifest(manifest: dict) -> None:
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def _matches(patterns: list[re.Pattern], selected: Selected) -> int:
    """How many of the page's patterns this note hits (0 = not selected)."""
    note = selected.note
    haystack = " ".join([
        selected.heading,
        selected.doc,
        note.get("summary", "") or "",
        " ".join(note.get("topics", []) or []),
        " ".join(o.get("ref", "") for o in note.get("obligations", []) or []),
        " ".join(d.get("ref", "") for d in note.get("deadlines", []) or []),
        " ".join(p.get("ref", "") for p in note.get("penalties", []) or []),
    ])
    return sum(1 for p in patterns if p.search(haystack))


def _source_satisfies(required_id: str, source_id: str) -> bool:
    return source_id == required_id or source_id.startswith(required_id + ":")


def selection(spec: dict, extracts: dict[str, dict]) -> SelectionResult:
    prefixes = spec.get("select", {}).get("docs") or []
    tiers = set(spec.get("select", {}).get("relevance") or ["core"])
    patterns = [re.compile(p, re.IGNORECASE) for p in spec.get("select", {}).get("match") or []]
    max_notes = int(spec.get("select", {}).get("max_notes", 90))

    out: list[Selected] = []
    for doc, data in extracts.items():
        if prefixes and not any(doc == p or doc.startswith(p.rstrip("/") + "/") for p in prefixes):
            continue
        for chunk_hash, entry in data.get("chunks", {}).items():
            note = entry.get("note") or {}
            # A note that fails the schema is not evidence: the extract stage
            # already treats it as work outstanding, so a page must not quietly
            # compose around a half-written one. See `synth/schema.py`.
            if not schema.is_valid(note):
                continue
            if note.get("relevance", "none") not in tiers:
                continue
            sel = Selected(doc=doc, chunk_hash=chunk_hash, heading=entry.get("heading", ""),
                           note=note, source_id=data.get("source_id", ""),
                           source_url=data.get("source_url", ""),
                           prompt_hash=entry.get("prompt_hash", "") or "",
                           model=entry.get("model", "") or "")
            sel.score = _matches(patterns, sel) if patterns else 1
            if patterns and sel.score == 0:
                continue
            out.append(sel)

    out.sort(key=lambda s: (-s.score, RELEVANCE_ORDER.get(s.note.get("relevance", "none"), 9), s.doc, s.heading))
    chosen: list[Selected] = []
    chosen_keys: set[tuple[str, str]] = set()
    for required_id in spec.get("authorities") or []:
        match = next((note for note in out
                      if _source_satisfies(required_id, note.source_id)), None)
        if match and len(chosen) < max_notes:
            chosen.append(match)
            chosen_keys.add((match.doc, match.chunk_hash))
    for note in out:
        key = (note.doc, note.chunk_hash)
        if len(chosen) >= max_notes:
            break
        if key not in chosen_keys:
            chosen.append(note)
            chosen_keys.add(key)
    excluded = [note for note in out if (note.doc, note.chunk_hash) not in chosen_keys]
    return SelectionResult(notes=chosen, excluded=excluded)


def select(spec: dict, extracts: dict[str, dict]) -> list[Selected]:
    """Compatibility wrapper returning the notes handed to the composer."""
    return selection(spec, extracts).notes


def authority_coverage(spec: dict, notes: list[Selected]) -> AuthorityCoverage:
    """Compare a page's minimum authority set with its selected evidence.

    Expanded GOV.UK collection members use ``parent-id:<content-id>`` as
    their source ID, so requiring the parent source covers both its index and
    any substantive member documents selected for the page.
    """
    required = tuple(spec.get("authorities") or ())
    selected_ids = {note.source_id for note in notes if note.source_id}

    def present(required_id: str) -> bool:
        return any(_source_satisfies(required_id, source_id)
                   for source_id in selected_ids)

    covered = tuple(source_id for source_id in required if present(source_id))
    missing = tuple(source_id for source_id in required if source_id not in covered)
    return AuthorityCoverage(required=required, covered=covered, missing=missing)


# Spec keys that affect navigation only, not the page's content - changing
# one shouldn't cost a recompose.
NAV_ONLY_KEYS = ("section",)


# Bumped when the fingerprint layout below changes shape, so an old manifest
# entry can never collide with a new one. Bumping it restages every page.
NOTE_FINGERPRINT_VERSION = 1


def note_fingerprint(sel: Selected) -> str:
    """Canonical serialization of one selected note, as the page sees it.

    Everything that reaches the compose prompt (`_render_notes`) or the page's
    provenance block is in here, plus the provenance of the note itself: the
    chunk it came from, the extraction prompt/schema version that shaped it,
    and the model that wrote it. Sorted keys and compact separators keep the
    encoding stable across Python versions and dict insertion order.
    """
    payload = {
        "v": NOTE_FINGERPRINT_VERSION,
        "doc": sel.doc,
        "chunk_hash": sel.chunk_hash,
        "heading": sel.heading,
        "source_id": sel.source_id,
        "source_url": sel.source_url,
        "prompt_hash": sel.prompt_hash,
        "model": sel.model,
        "note": sel.note,
    }
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def input_hash(spec: dict, notes: list[Selected], model: str) -> str:
    """The staleness key for a page. Changes iff its output should change.

    Invalidation contract - a page is stale when any of these move:

    - `prompts/compose.md`, or the page's spec in `pages.yml` (bar the
      nav-only keys, which don't reach the prompt);
    - the compose model;
    - the *set* of notes the selector picks, or the content of any picked
      note - including a re-extraction that rewrote it under a new
      `prompts/extract.md` or a different extraction model.

    A note the selector does not pick has no effect, whatever happens to it.
    """
    h = hashlib.sha256()
    h.update(SYSTEM.encode())
    h.update(json.dumps({k: v for k, v in spec.items() if k not in NAV_ONLY_KEYS},
                        sort_keys=True).encode())
    h.update(model.encode())
    for note in sorted(notes, key=lambda s: (s.doc, s.chunk_hash)):
        h.update(note_fingerprint(note).encode())
    return h.hexdigest()[:16]


def _render_notes(notes: list[Selected]) -> str:
    blocks = []
    for i, sel in enumerate(notes, 1):
        payload = {k: v for k, v in sel.note.items() if v not in (None, "", [], {})}
        payload.pop("relevance", None)
        blocks.append(
            f"### Note {i}\n"
            f"- source: {sel.source_id or sel.doc}\n"
            f"- source_url: {sel.source_url or 'unknown'}\n"
            f"- section: {sel.heading}\n"
            f"{json.dumps(payload, indent=1, ensure_ascii=False)}"
        )
    return "\n\n".join(blocks)


def build_prompt(spec: dict, notes: list[Selected]) -> str:
    coverage = authority_coverage(spec, notes)
    coverage_instruction = (
        "All declared minimum authorities are represented in the selected notes."
        if coverage.complete else
        "The selected notes do not represent these declared minimum authorities: "
        + ", ".join(coverage.missing)
        + ". Do not fill those gaps from general knowledge or imply complete coverage."
    )
    return (
        f"# Page to write\n\n"
        f"Title: {spec['title']}\n\n"
        f"Brief:\n{textwrap.dedent(spec.get('brief', '')).strip()}\n\n"
        f"Authority coverage:\n{coverage_instruction}\n\n"
        f"# Source notes ({len(notes)})\n\n"
        f"{_render_notes(notes)}\n\n"
        f"Write the page now, in Markdown, starting with `# {spec['title']}`."
    )


def _front_matter(spec: dict, notes: list[Selected], model: str, backend: str, ihash: str) -> str:
    sources = sorted({(s.source_id or s.doc) for s in notes})
    coverage = authority_coverage(spec, notes)
    fm = {
        "title": spec["title"],
        "generated": True,
        "generated_on": date.today().isoformat(),
        "generated_by": f"{backend}:{model}",
        "input_hash": ihash,
        "note_count": len(notes),
        "sources": sources,
        "authority_coverage": "complete" if coverage.complete else "incomplete",
        "missing_authorities": list(coverage.missing),
    }
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, default_flow_style=False).strip() + "\n---\n\n"


# Rendered into the top of every generated page, immediately under the H1.
# The site banner (overrides/main.html) says the same thing, but a page can
# also be read as raw markdown in the repository, printed, or pasted
# elsewhere - so the disclaimer travels inside the page too.
DISCLAIMER = """
!!! danger "Unofficial - not HMRC, not advice, written by an LLM"

    This page is **not** an HMRC publication and has no connection to HMRC or
    any government body. It was **written by a language model** from mirrored
    source material, and can be wrong, incomplete or out of date. It is not
    tax advice. Check every figure, date and rule against the cited source
    before relying on it, and see
    [GOV.UK](https://www.gov.uk/self-assessment-tax-returns) for official
    guidance.
"""


def _with_disclaimer(body: str) -> str:
    """Insert the disclaimer directly below the page's H1."""
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            return "\n".join(lines[: i + 1]) + "\n" + DISCLAIMER + "\n".join(lines[i + 1:])
    return DISCLAIMER + body


def _coverage_notice(coverage: AuthorityCoverage) -> str:
    if coverage.complete:
        detail = ("The selected source notes include every minimum authority "
                  "declared for this page in `pages.yml`.")
        title = "Minimum authority coverage satisfied"
        kind = "success"
    else:
        missing = ", ".join(f"`{source_id}`" for source_id in coverage.missing)
        detail = ("This page is missing, or did not select, required source "
                  f"material: {missing}. Treat it as incomplete until the source "
                  "is mirrored, extracted and selected.")
        title = "Minimum authority coverage incomplete"
        kind = "warning"
    return f'\n!!! {kind} "{title}"\n\n    {detail}\n'


def _provenance(notes: list[Selected]) -> str:
    """A closing block linking every corpus document the page drew on."""
    by_doc: dict[str, Selected] = {}
    for sel in notes:
        by_doc.setdefault(sel.doc, sel)
    lines = ["", "---", "", "## Sources used on this page", "",
             "This page was written by an LLM from structured notes extracted from "
             "the mirrored sources below. Always check the upstream source before "
             "relying on any figure or deadline.", ""]
    for doc, sel in sorted(by_doc.items()):
        count = sum(1 for s in notes if s.doc == doc)
        url = sel.source_url or ""
        label = sel.source_id or doc
        link = f"[{label}]({url})" if url else label
        lines.append(f"- {link} - {count} note(s) - mirrored at `corpus/{doc}`")
    return "\n".join(lines) + "\n"


def plan(model: str, *, only: list[str] | None = None, force: bool = False) -> list[PageWork]:
    extracts = store.load_all()
    manifest = load_manifest()
    works: list[PageWork] = []
    for spec in load_pages():
        if only and spec["id"] not in only:
            continue
        picked = selection(spec, extracts)
        notes = picked.notes
        coverage = authority_coverage(spec, notes)
        ihash = input_hash(spec, notes, model)
        recorded = manifest.get(spec["id"], {})
        exists = (REPO_ROOT / spec["output"]).exists()
        if force:
            stale, reason = True, "forced"
        elif not exists:
            stale, reason = True, "page missing"
        elif recorded.get("input_hash") != ihash:
            stale, reason = True, "inputs changed"
        elif not notes:
            stale, reason = False, "no notes selected"
        else:
            stale, reason = False, "up to date"
        works.append(PageWork(spec=spec, notes=notes, input_hash=ihash, stale=stale,
                              reason=reason, excluded_notes=len(picked.excluded),
                              coverage=coverage))
    return works


def run(backend: Backend, model: str, *, only: list[str] | None = None, force: bool = False,
        verbose: bool = True) -> runlog.StageReport:
    """Write every stale page. Returns a report of what happened.

    A page whose selector matches nothing, or whose model call failed, is a
    failure: the site would otherwise keep serving the last version of a page
    nobody was told had stopped being regenerated.
    """
    manifest = load_manifest()
    report = runlog.StageReport(stage="compose", unit="page")
    skipped: list[str] = []
    for work in plan(model, only=only, force=force):
        spec = work.spec
        if not work.stale:
            if verbose:
                print(f"= {spec['id']}: {work.reason}")
            skipped.append(spec["id"])
            continue
        if not work.notes:
            print(f"! {spec['id']}: no extract notes match its selector - "
                  f"run `uv run extract` first, or widen `select:`")
            report.fail(spec["id"], "no extract notes match its selector")
            continue
        if verbose:
            print(f"* {spec['id']}: composing from {len(work.notes)} notes ({work.reason}) ...", flush=True)
        try:
            body = backend.call(SYSTEM, build_prompt(spec, work.notes)).strip()
        except Exception as exc:  # noqa: BLE001
            print(f"! {spec['id']}: {exc}")
            report.fail(spec["id"], exc)
            continue
        if body.startswith("```"):
            body = body.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        coverage = work.coverage or authority_coverage(spec, work.notes)
        page = (_front_matter(spec, work.notes, model, backend.name, work.input_hash)
                + _with_disclaimer(body) + _coverage_notice(coverage)
                + "\n" + _provenance(work.notes))
        out = REPO_ROOT / spec["output"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page)
        manifest[spec["id"]] = {
            "input_hash": work.input_hash,
            "output": spec["output"],
            "generated_on": date.today().isoformat(),
            "generated_by": f"{backend.name}:{model}",
            "note_count": len(work.notes),
        }
        save_manifest(manifest)
        report.succeed(spec["id"])
        if verbose:
            print(f"  -> {spec['output']}")
    report.extra["up_to_date"] = skipped
    return report
