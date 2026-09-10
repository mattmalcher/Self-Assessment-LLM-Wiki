#!/usr/bin/env python3
"""Offline integrity audit of everything the repository publishes.

    uv run audit                  # every check; exits non-zero on an error
    uv run audit --only pages citations
    uv run audit --strict         # warnings count as errors too
    uv run audit --list           # what the checks are

The other gates each guard one seam: `configcheck` guards the registry,
`reconcile` guards corpus artifacts, `report --check` guards the status page
and the nav. None of them looks at the published pages themselves, which are
the part a reader actually sees and the part written by a language model. So
this walks the whole chain the site rests on - config, corpus, extracts, both
manifests, the status page, the pages, and the citations on them - and reports
every problem at once.

It is deterministic and entirely offline: no network, no model calls, no
clock. Everything it reads is committed, so a failure here is reproducible on
any checkout and CI can run it on every deploy.

Severity is the one judgement call. An **error** is a broken artifact: a
configured source with no file, a cached note that fails the schema, a page
with no disclaimer, a manifest pointing at a file that is not there. A
**warning** is a claim the artifacts cannot substantiate but that no
structural rule forbids - today, a citation on a page that appears in none of
the notes that page selected. Warnings are always printed and always land in
the JSON report; `--strict` makes them fail the run as well.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import citations, configcheck, runlog
from .pipeline import fetch as pipeline_fetch
from .pipeline import manifest as pipeline_manifest
from .pipeline import reconcile
from .synth import compose, extract, report, schema, store
from .synth.chunk import split_front_matter
from .synth.config import CORPUS_DIR, EXTRACTS_DIR, REPO_ROOT

REPORT_PATH = Path(__file__).parent / "last_audit.json"

# The footer `compose._provenance` writes, and the callout `_with_disclaimer`
# inserts. Both are structural promises of a generated page, so the audit
# checks for the real strings rather than a paraphrase of them.
PROVENANCE_HEADING = "## Sources used on this page"
DISCLAIMER_MARKER = '!!! danger "Unofficial'


@dataclass
class Findings:
    """What one check found, split by whether it fails the run."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


# --- configuration ---------------------------------------------------------

def check_config(findings: Findings) -> None:
    """Both config files parse and validate. Everything else assumes this."""
    for label, load in (("sources.yml", pipeline_fetch.load_sources),
                        ("pages.yml", compose.load_pages)):
        try:
            load()
        except configcheck.ConfigError as exc:
            findings.error(f"{label}: {'; '.join(exc.errors)}")
        except (OSError, yaml.YAMLError) as exc:
            findings.error(f"{label}: could not be read ({exc})")


# --- corpus ----------------------------------------------------------------

def check_sources(findings: Findings) -> None:
    """Every fetched source reconciles to the artifact it claims to write."""
    try:
        sources = pipeline_fetch.load_sources()
    except configcheck.ConfigError:
        return  # already reported by check_config
    for failure in reconcile.audit(sources, root=REPO_ROOT).failed:
        findings.error(f"{failure['unit']}: {failure['error']}")


def check_corpus(findings: Findings) -> None:
    """Mirrored documents carry the provenance the later stages read.

    `chunk_file` hands the extract stage a document's front matter, and that
    is where a note's `source_id` and `source_url` come from - so a mirrored
    file without them produces notes that cannot be attributed, and pages
    whose provenance footer has nothing to link to.

    Only the files a fetcher writes are in scope. `corpus/` also holds a few
    hand-written index pages, and the shared `web_page` output is structured
    as `<!-- section:ID -->` blocks rather than one document's front matter -
    `check_sources` covers that one.
    """
    try:
        sources = pipeline_fetch.load_sources()
    except configcheck.ConfigError:
        return
    for source in sources:
        if source.get("status") != "fetch" or source.get("type") == "web_page":
            continue
        path = REPO_ROOT / source["output"]
        if not path.exists():
            continue  # `check_sources` reports the gap itself
        meta, _ = split_front_matter(path.read_text())
        missing = [k for k in ("source_id", "source_url") if not meta.get(k)]
        if missing:
            findings.error(f"{source['output']}: front matter is missing "
                           f"{', '.join(missing)}")


# --- extracts --------------------------------------------------------------

def check_extracts(findings: Findings) -> None:
    """Every committed note validates, and every extract file has a document.

    An extract file with no corpus document behind it is an error: nothing
    will ever refresh those notes, and the selector can still reach them.

    A malformed *note* is a warning rather than an error. It is the failure
    `synth/schema.py` exists for, but the design answer to it is already in
    place - such a record is never counted as cached, never selected, and is
    queued for re-extraction - so it is outstanding model work, not a broken
    artifact, and it must not block a deploy of the pages that correctly
    exclude it. `uv run status` lists them, and `--strict` fails on them.
    """
    for path in sorted(EXTRACTS_DIR.rglob("*.json")):
        rel = path.relative_to(EXTRACTS_DIR).as_posix()
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            findings.error(f"extracts/{rel}: not valid JSON ({exc})")
            continue
        doc = data.get("doc")
        if not doc:
            findings.error(f"extracts/{rel}: no `doc` recorded")
        elif not (CORPUS_DIR / doc).exists():
            findings.error(f"extracts/{rel}: no corpus document at corpus/{doc}")
        for chunk_hash, entry in sorted((data.get("chunks") or {}).items()):
            problems = schema.validate_note((entry or {}).get("note"))
            if problems:
                findings.warn(f"extracts/{rel} chunk {chunk_hash}: "
                              f"{'; '.join(problems[:5])}")


def check_chunk_cache(findings: Findings) -> None:
    """The extract cache still describes the corpus as it is chunked today.

    Re-chunks every document and compares. A cached chunk whose hash is no
    longer produced is an orphan the next `uv run extract` would prune; a
    chunk with no cached note is uncovered text. Neither breaks the build,
    but both mean the published coverage figures describe a tree that is not
    quite this one, so they are reported.
    """
    try:
        plans = extract.plan()
    except (OSError, ValueError) as exc:
        findings.error(f"could not chunk the corpus: {exc}")
        return
    orphans = sum(p.orphans for p in plans)
    if orphans:
        findings.warn(f"{orphans} cached chunk(s) no longer appear in the corpus "
                      f"and will be pruned by the next `uv run extract`")
    uncovered = sum(len(p.todo) for p in plans)
    if uncovered:
        findings.warn(f"{uncovered} corpus chunk(s) have no valid cached note")


# --- manifests -------------------------------------------------------------

def check_manifests(findings: Findings) -> None:
    """Both manifests describe things that exist and are what they say.

    The fetch manifest is the cache key for stage 1 and the synth manifest is
    the staleness key for stage 3, so an entry for a source or page that no
    longer exists is a cache that can never be invalidated.
    """
    try:
        sources = pipeline_fetch.load_sources()
        specs = compose.load_pages()
    except configcheck.ConfigError:
        return

    source_ids = {s["id"] for s in sources}
    for source_id in sorted(pipeline_manifest.load()):
        if source_id not in source_ids:
            findings.warn(f"pipeline/manifest.json: `{source_id}` is not in sources.yml")

    by_id = {spec["id"]: spec for spec in specs}
    synth_manifest = compose.load_manifest()
    for page_id, record in sorted(synth_manifest.items()):
        spec = by_id.get(page_id)
        if spec is None:
            findings.error(f"synth/manifest.json: `{page_id}` is not in pages.yml")
            continue
        if record.get("output") != spec["output"]:
            findings.error(f"synth/manifest.json: `{page_id}` records output "
                           f"{record.get('output')!r}, pages.yml says "
                           f"{spec['output']!r}")
        if not (REPO_ROOT / spec["output"]).exists():
            findings.error(f"synth/manifest.json: `{page_id}` is recorded as "
                           f"generated but {spec['output']} does not exist")


def check_status(findings: Findings) -> None:
    """The published status page and the nav match what the tree implies."""
    try:
        drifted = report.drift()
    except configcheck.ConfigError:
        return
    for path in drifted:
        findings.error(f"{path.relative_to(REPO_ROOT).as_posix()} is out of date - "
                       f"run `uv run report` and commit the result")


# --- the pages themselves --------------------------------------------------

def _composed(spec: dict) -> Path | None:
    path = REPO_ROOT / spec["output"]
    return path if path.exists() else None


def check_pages(findings: Findings) -> None:
    """Structural promises every generated page makes to a reader.

    A published page must carry its own H1, the unofficial/not-advice
    disclaimer (the site banner does not travel with the raw markdown), and
    the provenance footer naming the mirrored documents behind it - and every
    document that footer names must actually be in `corpus/`, or the page
    cites a source the repository does not hold.
    """
    try:
        specs = compose.load_pages()
    except configcheck.ConfigError:
        return
    manifest = compose.load_manifest()
    for spec in specs:
        path = _composed(spec)
        if path is None:
            continue  # never composed; `check_status` reports the plan gap
        where = spec["output"]
        meta, body = split_front_matter(path.read_text())

        if not meta.get("generated"):
            findings.error(f"{where}: front matter does not mark the page as generated")
        if meta.get("title") != spec["title"]:
            findings.error(f"{where}: front matter title {meta.get('title')!r} "
                           f"is not the page plan's {spec['title']!r}")

        h1s = [line for line in _prose_lines(body) if line.startswith("# ")]
        if len(h1s) != 1:
            findings.error(f"{where}: expected exactly one H1, found {len(h1s)}")
        elif h1s[0][2:].strip() != spec["title"]:
            findings.error(f"{where}: H1 {h1s[0][2:].strip()!r} is not the page "
                           f"plan's {spec['title']!r}")

        if DISCLAIMER_MARKER not in body:
            findings.error(f"{where}: the unofficial/not-advice disclaimer is missing")

        docs = _provenance_docs(body)
        if docs is None:
            findings.error(f"{where}: no `{PROVENANCE_HEADING}` footer")
        elif not docs:
            findings.error(f"{where}: the provenance footer names no source")
        else:
            for doc in docs:
                if not (CORPUS_DIR / doc).exists():
                    findings.error(f"{where}: cites `corpus/{doc}`, which is not "
                                   f"in the mirrored corpus")

        if manifest.get(spec["id"], {}).get("note_count") == 0:
            findings.error(f"{where}: composed from no notes - a page with no "
                           f"evidence must not be published")


def _prose_lines(body: str) -> list[str]:
    """`body` without its fenced code blocks.

    Pages state machine-implementable rules as pseudo-code, and a `#` comment
    inside a fence is not a heading - reading one as an H1 would fail exactly
    the pages that followed the brief most closely.
    """
    lines, fenced = [], False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            lines.append(line)
    return lines


def _provenance_docs(body: str) -> list[str] | None:
    """The corpus documents a page's footer claims, or None if it has no footer."""
    if PROVENANCE_HEADING not in body:
        return None
    footer = body.split(PROVENANCE_HEADING, 1)[1]
    return [line.split("`corpus/", 1)[1].split("`", 1)[0]
            for line in footer.splitlines()
            if line.startswith("- ") and "`corpus/" in line]


def check_citations(findings: Findings) -> None:
    """Every citation on a page appears in the notes that page selected.

    The compose prompt forbids using anything outside the supplied notes, and
    a citation is the one part of a page whose provenance can be checked
    mechanically: `citations.py` reads both sides as tokens and reports what
    the page cites that its own notes never mentioned.

    A page whose recorded `input_hash` no longer matches is still checked,
    with the caveat said out loud. Its committed text was written from a
    selection this tree may no longer reproduce, so an unsupported citation
    there could be drift rather than invention - but staying silent about
    every page until the next full recompose would leave the check inert
    exactly when the corpus has been moving.

    These are warnings: an unsupported citation is a content defect for a
    human to judge, not a broken artifact, and one must not block the deploy
    of the other seventeen pages. `--strict` makes them fail.
    """
    try:
        specs = compose.load_pages()
    except configcheck.ConfigError:
        return
    extracts = store.load_all()
    manifest = compose.load_manifest()

    for spec in specs:
        path = _composed(spec)
        record = manifest.get(spec["id"])
        if path is None or not record:
            continue
        notes = compose.select(spec, extracts)
        model = str(record.get("generated_by", "")).split(":", 1)[-1]
        stale = compose.input_hash(spec, notes, model) != record.get("input_hash")
        _, body = split_front_matter(path.read_text())
        # The footer is generated from the notes, not written by the model.
        prose = body.split(PROVENANCE_HEADING, 1)[0]
        note_text = json.dumps([{"doc": n.doc, "heading": n.heading,
                                 "source_id": n.source_id, "note": n.note}
                                for n in notes], ensure_ascii=False)
        missing = citations.unsupported(prose, note_text)
        if missing:
            findings.warn(f"{spec['output']}: {len(missing)} citation(s) appear in "
                          f"none of the {len(notes)} notes it selects"
                          + (" (page is stale, so the selection may have moved "
                             "since it was written)" if stale else "")
                          + f": {', '.join(missing)}")


CHECKS = {
    "config": check_config,
    "sources": check_sources,
    "corpus": check_corpus,
    "extracts": check_extracts,
    "chunk-cache": check_chunk_cache,
    "manifests": check_manifests,
    "status": check_status,
    "pages": check_pages,
    "citations": check_citations,
}


def run(only: list[str] | None = None) -> dict[str, Findings]:
    """Run the named checks (all of them by default), in declaration order."""
    wanted = [name for name in CHECKS if not only or name in only]
    results: dict[str, Findings] = {}
    for name in wanted:
        findings = Findings()
        CHECKS[name](findings)
        results[name] = findings
    return results


def as_report(results: dict[str, Findings], *, strict: bool) -> runlog.StageReport:
    """The same machine-readable shape the pipeline stages write."""
    stage = runlog.StageReport(stage="audit", unit="check")
    warnings: list[dict] = []
    for name, findings in results.items():
        for message in findings.warnings:
            warnings.append({"unit": name, "error": message})
        if findings.errors or (strict and findings.warnings):
            for message in findings.errors + (findings.warnings if strict else []):
                stage.fail(name, message)
        else:
            stage.succeed(name)
    stage.extra["warnings"] = warnings
    stage.extra["strict"] = strict
    return stage


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="audit", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", nargs="*", choices=sorted(CHECKS),
                        help="run only these checks")
    parser.add_argument("--strict", action="store_true",
                        help="fail on warnings as well as errors")
    parser.add_argument("--list", action="store_true",
                        help="list the checks and what each one covers")
    args = parser.parse_args(argv)

    if args.list:
        for name, check in CHECKS.items():
            print(f"{name:12} {(check.__doc__ or '').strip().splitlines()[0]}")
        return 0

    results = run(args.only)
    errors = sum(len(f.errors) for f in results.values())
    warnings = sum(len(f.warnings) for f in results.values())

    for name, findings in results.items():
        for message in findings.errors:
            print(f"  ! {name}: {message}", file=sys.stderr)
        for message in findings.warnings:
            print(f"  ~ {name}: {message}")

    stage = as_report(results, strict=args.strict)
    runlog.write(REPORT_PATH, [stage])

    print(f"audit: {len(results)} check(s), {errors} error(s), "
          f"{warnings} warning(s)"
          + (" - warnings are errors (--strict)" if args.strict and warnings else ""))
    return stage.exit_code()


if __name__ == "__main__":
    sys.exit(main())
