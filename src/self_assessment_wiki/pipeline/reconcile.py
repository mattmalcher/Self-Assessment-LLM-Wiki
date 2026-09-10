#!/usr/bin/env python3
"""Check that cached fetch state still matches the artifacts on disk.

The manifest records what a source *was* fetched to. It says nothing about
whether that file is still there: delete `corpus/external-explainers.md` and
the next run sees a matching content hash, reports "unchanged", and leaves
the corpus permanently short of a source the registry claims to mirror. That
is how `taxaid-self-assessment` came to be listed as fetched with no file
behind it.

Two halves fix that:

- the fetchers ask `artifact_missing()` before trusting a cache hit, so a
  missing file forces a full re-fetch and a rewrite;
- `uv run reconcile` audits every `status: fetch` source - its output file,
  and for shared outputs its own `<!-- section:ID -->` block - so a gap is
  caught by CI rather than by a reader.

Usage:
    uv run reconcile              # audit every fetchable source
    uv run reconcile --only taxaid-self-assessment
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .. import runlog

PIPELINE_DIR = Path(__file__).parent
REPORT_PATH = PIPELINE_DIR / "last_reconcile.json"

# web_page sources that share one output file each own one of these blocks;
# see fetchers/web_page.py.
SECTION_OPEN = "<!-- section:{sid} -->"
SECTION_CLOSE = "<!-- /section:{sid} -->"


def section_id(source: dict) -> str | None:
    """The section a shared-output source owns, or None if it owns the file."""
    if source.get("type") != "web_page":
        return None
    return source.get("section", source["id"])


def problem(source: dict, root: Path = Path()) -> str | None:
    """Why `source` does not reconcile to an artifact, or None if it does."""
    output = source.get("output")
    if not output:
        return "status: fetch but no output path configured"

    path = root / output
    if not path.exists():
        return f"missing output file: {output}"
    if path.stat().st_size == 0:
        return f"empty output file: {output}"

    sid = section_id(source)
    if sid is None:
        return None

    text = path.read_text()
    if SECTION_OPEN.format(sid=sid) not in text:
        return f"missing section `{sid}` in shared output {output}"
    if SECTION_CLOSE.format(sid=sid) not in text:
        return f"unterminated section `{sid}` in shared output {output}"
    return None


def artifact_missing(source: dict, root: Path = Path()) -> bool:
    """True when a fetcher must ignore its cache and rewrite this artifact.

    Fetchers call this instead of trusting a 304 or a matching content hash:
    an unchanged upstream is only good news if the file it produced is still
    on disk with this source's content in it.
    """
    return problem(source, root) is not None


def fetchable(sources: list[dict], only: list[str] | None = None) -> list[dict]:
    return [s for s in sources
            if s.get("status") == "fetch" and not (only and s["id"] not in only)]


def audit(sources: list[dict], only: list[str] | None = None,
          root: Path = Path()) -> runlog.StageReport:
    report = runlog.StageReport(stage="reconcile", unit="source")
    for source in fetchable(sources, only):
        issue = problem(source, root)
        if issue:
            report.fail(source["id"], issue)
        else:
            report.succeed(source["id"])
    return report


def main() -> int:
    from .fetch import load_sources  # local: fetch imports this module

    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--only", nargs="*", help="only audit these source ids")
    args = parser.parse_args()

    report = audit(load_sources(), args.only)
    runlog.write(REPORT_PATH, [report])

    for failure in report.failed:
        print(f"  ! {failure['unit']}: {failure['error']}", file=sys.stderr)
    print(report.verdict())
    if report.failed:
        print("Re-run `uv run fetch --only " + " ".join(f["unit"] for f in report.failed)
              + "` to rebuild the missing artifact(s).")
    return report.exit_code()


if __name__ == "__main__":
    sys.exit(main())
