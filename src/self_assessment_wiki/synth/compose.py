"""Stage 3: page spec + selected extract notes -> a wiki page in docs/.

Selection is deterministic (path prefixes, relevance tier, regexes over the
heading/summary/topics of each note), so a page's staleness can be decided
without a model call: hash the brief, the prompt, the model and the set of
chunk hashes that feed it, and skip the page when that hash is unchanged.
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

from . import store
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


@dataclass
class PageWork:
    spec: dict
    notes: list[Selected] = field(default_factory=list)
    input_hash: str = ""
    stale: bool = True
    reason: str = ""


def load_pages() -> list[dict]:
    return yaml.safe_load(PAGES_PATH.read_text())


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


def select(spec: dict, extracts: dict[str, dict]) -> list[Selected]:
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
            if note.get("relevance", "none") not in tiers:
                continue
            sel = Selected(doc=doc, chunk_hash=chunk_hash, heading=entry.get("heading", ""),
                           note=note, source_id=data.get("source_id", ""),
                           source_url=data.get("source_url", ""))
            sel.score = _matches(patterns, sel) if patterns else 1
            if patterns and sel.score == 0:
                continue
            out.append(sel)

    out.sort(key=lambda s: (-s.score, RELEVANCE_ORDER.get(s.note.get("relevance", "none"), 9), s.doc, s.heading))
    return out[:max_notes]


# Spec keys that affect navigation only, not the page's content - changing
# one shouldn't cost a recompose.
NAV_ONLY_KEYS = ("section",)


def input_hash(spec: dict, notes: list[Selected], model: str) -> str:
    h = hashlib.sha256()
    h.update(SYSTEM.encode())
    h.update(json.dumps({k: v for k, v in spec.items() if k not in NAV_ONLY_KEYS},
                        sort_keys=True).encode())
    h.update(model.encode())
    for note in sorted(notes, key=lambda s: (s.doc, s.chunk_hash)):
        h.update(f"{note.doc}:{note.chunk_hash}".encode())
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
    return (
        f"# Page to write\n\n"
        f"Title: {spec['title']}\n\n"
        f"Brief:\n{textwrap.dedent(spec.get('brief', '')).strip()}\n\n"
        f"# Source notes ({len(notes)})\n\n"
        f"{_render_notes(notes)}\n\n"
        f"Write the page now, in Markdown, starting with `# {spec['title']}`."
    )


def _front_matter(spec: dict, notes: list[Selected], model: str, backend: str, ihash: str) -> str:
    sources = sorted({(s.source_id or s.doc) for s in notes})
    fm = {
        "title": spec["title"],
        "generated": True,
        "generated_on": date.today().isoformat(),
        "generated_by": f"{backend}:{model}",
        "input_hash": ihash,
        "note_count": len(notes),
        "sources": sources,
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
        notes = select(spec, extracts)
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
        works.append(PageWork(spec=spec, notes=notes, input_hash=ihash, stale=stale, reason=reason))
    return works


def run(backend: Backend, model: str, *, only: list[str] | None = None, force: bool = False,
        verbose: bool = True) -> tuple[int, int]:
    manifest = load_manifest()
    written = failed = 0
    for work in plan(model, only=only, force=force):
        spec = work.spec
        if not work.stale:
            if verbose:
                print(f"= {spec['id']}: {work.reason}")
            continue
        if not work.notes:
            print(f"! {spec['id']}: no extract notes match its selector - "
                  f"run `uv run extract` first, or widen `select:`")
            failed += 1
            continue
        if verbose:
            print(f"* {spec['id']}: composing from {len(work.notes)} notes ({work.reason}) ...", flush=True)
        try:
            body = backend.call(SYSTEM, build_prompt(spec, work.notes)).strip()
        except Exception as exc:  # noqa: BLE001
            print(f"! {spec['id']}: {exc}")
            failed += 1
            continue
        if body.startswith("```"):
            body = body.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        page = (_front_matter(spec, work.notes, model, backend.name, work.input_hash)
                + _with_disclaimer(body) + "\n" + _provenance(work.notes))
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
        written += 1
        if verbose:
            print(f"  -> {spec['output']}")
    return written, failed
