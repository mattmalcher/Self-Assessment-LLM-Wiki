"""Write docs/meta/wiki-status.md - a deterministic, no-model-calls report on
how much of the corpus has been extracted and how fresh each wiki page is -
and the .pages nav files that order the site.

    uv run report            # regenerate the status page and the nav
    uv run report --check    # fail if what is committed is out of date

`extract` and `compose` call `write_all` themselves once they have changed
anything, so a successful run cannot leave the published status or nav behind
its own output. `--check` is the CI half of that promise: it regenerates into
memory and fails on any difference, so committed drift cannot reach the site.

Everything here is derived from committed state - the corpus, the extract
cache, both manifests and the page plan - and nothing from the clock, so two
runs over the same tree produce the same bytes.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from .. import configcheck
from ..pipeline import fetch as pipeline_fetch
from ..pipeline import manifest as manifest_store
from ..pipeline import reconcile
from . import compose, extract, nav, schema, store
from .config import DOCS_DIR, REPO_ROOT

OUTPUT = DOCS_DIR / "meta" / "wiki-status.md"


@dataclass
class PageState:
    """One page of the plan, as the committed artifacts actually leave it."""

    spec: dict
    record: dict | None
    status: str  # up to date / stale / missing / not yet generated

    @property
    def written(self) -> bool:
        return self.status != "not yet generated"


def page_states(extracts: dict[str, dict], manifest: dict,
                specs: list[dict]) -> list[PageState]:
    """Recompute each page's staleness key against the model that wrote it.

    `compose.plan` answers "is this page stale for the model I am about to
    run?"; the status page has to answer the narrower question "does the
    committed page still match the notes it was composed from?", which is a
    property of the repository rather than of anyone's command line. So the
    recorded `generated_by` supplies the model, and the rest of the
    invalidation contract is `compose`'s own.
    """
    states: list[PageState] = []
    for spec in specs:
        record = manifest.get(spec["id"])
        if not record:
            states.append(PageState(spec, None, "not yet generated"))
            continue
        if not (REPO_ROOT / spec["output"]).exists():
            states.append(PageState(spec, record, "missing"))
            continue
        model = str(record.get("generated_by", "")).split(":", 1)[-1]
        ihash = compose.input_hash(spec, compose.select(spec, extracts), model)
        status = "up to date" if ihash == record.get("input_hash") else "stale"
        states.append(PageState(spec, record, status))
    return states


def _last_checked(manifest: dict) -> str:
    dates = [e.get("last_checked") for e in manifest.values() if e.get("last_checked")]
    return max(dates) if dates else "-"


def _last_written(states: list[PageState]) -> str:
    dates = [s.record.get("generated_on") for s in states
             if s.record and s.record.get("generated_on")]
    return max(dates) if dates else "-"


def _completeness(*, outstanding: int, invalid: int, gaps: list[dict],
                  states: list[PageState]) -> list[str]:
    """Say plainly whether the committed tree is the output of a complete run.

    Only the *current* state can be established from the repository, so this
    either dates the complete run that produced it or names what is missing;
    it never claims a completeness the artifacts cannot support.
    """
    problems = []
    if gaps:
        problems.append(f"{len(gaps)} fetched source(s) have no artifact in `corpus/`")
    if invalid:
        problems.append(f"{invalid} cached note(s) fail the extract schema")
    if outstanding - invalid > 0:
        problems.append(f"{outstanding - invalid} chunk(s) have never been extracted")
    behind = [s for s in states if s.status in ("stale", "missing")]
    if behind:
        problems.append(f"{len(behind)} page(s) are stale or missing: "
                        + ", ".join(f"`{s.spec['id']}`" for s in behind))
    ungenerated = [s for s in states if not s.written]
    if ungenerated:
        problems.append(f"{len(ungenerated)} planned page(s) have never been composed: "
                        + ", ".join(f"`{s.spec['id']}`" for s in ungenerated))

    if not problems:
        return [f"**The committed corpus, extracts and pages are the output of a "
                f"complete end-to-end run**, finished {_last_written(states)}."]
    return ["**No complete end-to-end run is represented by the committed "
            "artifacts.** Outstanding:", ""] + [f"- {p}" for p in problems]


def render() -> str:
    plans = extract.plan()
    extracts = store.load_all()
    manifest = compose.load_manifest()
    specs = compose.load_pages()
    states = page_states(extracts, manifest, specs)

    total = sum(len(p.chunks) for p in plans)
    done = sum(len(p.chunks) - len(p.todo) for p in plans)
    outstanding = sum(len(p.todo) for p in plans)
    invalid = sum(len(p.invalid) for p in plans)
    gaps = reconcile.audit(pipeline_fetch.load_sources()).failed
    relevance: dict[str, int] = {}
    for data in extracts.values():
        for entry in data.get("chunks", {}).values():
            # An unusable note is counted as invalid, not as a relevance
            # judgement it never made.
            key = ("invalid" if not schema.entry_is_valid(entry)
                   else (entry.get("note") or {}).get("relevance", "unknown"))
            relevance[key] = relevance.get(key, 0) + 1

    lines = [
        "---",
        "title: Wiki status",
        "---",
        "",
        "# Wiki status",
        "",
        "Generated by `uv run report` - **do not hand-edit**. It "
        "records how much of the mirrored corpus has been read by the "
        "extraction stage, and when each wiki page was last written.",
        "",
        "It is derived entirely from what is committed - the corpus, the "
        "extract cache, both manifests and the page plan - so it is "
        "regenerated after every extract and compose, and CI fails if what "
        "is published here has drifted from what the repository holds.",
        "",
        "## Pipeline state",
        "",
        f"- Corpus last checked upstream: {_last_checked(manifest_store.load())}.",
        f"- Most recent page written: {_last_written(states)}.",
        "",
    ]
    lines += _completeness(outstanding=outstanding, invalid=invalid,
                           gaps=gaps, states=states)
    lines += [
        "",
        "## Extraction coverage",
        "",
        f"{done} of {total} corpus chunks extracted "
        f"({(100 * done / total) if total else 0:.0f}%), across "
        f"{len(plans)} mirrored documents. Only notes that pass the extract "
        f"schema count as extracted"
        + (f"; {invalid} cached note(s) do not, and are queued for "
           f"re-extraction." if invalid else "."),
        "",
        "Chunks by Self Assessment relevance, as judged at extraction:",
        "",
        "| Relevance | Chunks |",
        "|---|---|",
    ]
    for key in ("core", "related", "none", "unknown", "invalid"):
        if relevance.get(key):
            lines.append(f"| {key} | {relevance[key]} |")

    if invalid:
        lines += [
            "",
            "### Notes that fail the extract schema",
            "",
            "These chunks have a cached note that `synth/schema.py` rejects. "
            "They are counted as work outstanding, not as coverage, no page "
            "may cite them, and the next `uv run extract` re-runs them.",
            "",
            "| Document | Invalid notes |",
            "|---|---|",
        ]
        for p in plans:
            if p.invalid:
                lines.append(f"| `corpus/{p.doc}` | {len(p.invalid)} |")

    lines += [
        "",
        "| Document | Chunks | Extracted |",
        "|---|---|---|",
    ]
    for p in plans:
        lines.append(f"| `corpus/{p.doc}` | {len(p.chunks)} | {len(p.chunks) - len(p.todo)} |")

    lines += ["", "## Corpus integrity", ""]
    if gaps:
        lines += [f"{len(gaps)} source(s) are registered as fetched but have no "
                  f"artifact in `corpus/`, so the coverage figures above cover "
                  f"less than the registry claims:", ""]
        lines += [f"- `{g['unit']}`: {g['error']}" for g in gaps]
    else:
        lines.append("Every source registered as fetched has the artifact it "
                     "is configured to write.")

    lines += ["", "## Pages", "",
              "In the order the site navigation lists them.", "",
              "| Page | Notes used | Written | By | State |", "|---|---|---|---|---|"]
    for state in states:
        spec, record = state.spec, state.record
        if record:
            rel = spec["output"].removeprefix("docs/").removesuffix(".md")
            page = f"[{spec['title']}](../{rel}.md)"
            lines.append(f"| {page} | {record.get('note_count', '-')} | "
                         f"{record.get('generated_on', '-')} | "
                         f"`{record.get('generated_by', '-')}` | {state.status} |")
        else:
            lines.append(f"| {spec['title']} | - | - | - | {state.status} |")
    lines.append("")
    return "\n".join(lines)


def files() -> dict[Path, str]:
    """Every generated file this module owns, path -> content it should hold."""
    return {OUTPUT: render(), **nav.render(also_present=[OUTPUT])}


def write_all() -> list[Path]:
    """Regenerate the status page and the nav. Returns the paths written."""
    written = []
    for path, content in files().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        written.append(path)
    return written


def drift() -> list[Path]:
    """Paths whose committed content is not what `write_all` would write."""
    return [path for path, content in files().items()
            if not path.exists() or path.read_text() != content]


def _rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="report", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true",
                        help="write nothing; exit non-zero if the committed "
                             "status page or nav is out of date")
    args = parser.parse_args(argv)

    # The report and the nav are published claims about the registry and the
    # page plan; if either does not validate, say so rather than publish a
    # reading of it.
    try:
        pipeline_fetch.load_sources()
        compose.load_pages()
    except configcheck.ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.check:
        stale = drift()
        if not stale:
            print("status and nav are up to date")
            return 0
        print(f"error: {len(stale)} generated file(s) are out of date - "
              f"run `uv run report` and commit the result:", file=sys.stderr)
        for path in stale:
            print(f"  ! {_rel(path)}", file=sys.stderr)
        return 1

    for path in write_all():
        print(f"wrote {_rel(path)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
