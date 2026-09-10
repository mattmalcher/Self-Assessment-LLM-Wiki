#!/usr/bin/env python3
"""Entrypoint: read pipeline/sources.yml, fetch every `status: fetch` source,
write changed markdown into corpus/, and update pipeline/manifest.json.

This is stage 1 of three: it mirrors sources deterministically. Stages 2 and
3 (synth/) read corpus/ and write the wiki in docs/.

Usage:
    uv run fetch                 # fetch everything due
    uv run fetch --only itepa-2003 tma-1970
    uv run fetch --dry-run   # resolve URLs, fetch nothing
    uv run fetch --keep-going  # best effort: report failures, still exit 0

Any source that fails makes the command exit non-zero, so a scheduled run
cannot pass off a partial refresh as a complete one. `last_run.json` records
what was attempted, what succeeded and what failed.
"""
from __future__ import annotations

import argparse
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

import yaml

from .. import runlog
from . import manifest as manifest_store
from . import render_sources_index
from .fetchers import caselaw, govuk_content, legislation, web_page

PIPELINE_DIR = Path(__file__).parent
SOURCES_PATH = PIPELINE_DIR / "sources.yml"

_DISPATCH = {
    "legislation": legislation.fetch,
    "govuk_content": govuk_content.fetch,
    "govuk_content_collection": govuk_content.fetch,
    "govuk_content_manual": govuk_content.fetch,
    "caselaw_feed": caselaw.fetch,
    "web_page": web_page.fetch,
}


def load_sources() -> list[dict]:
    return yaml.safe_load(SOURCES_PATH.read_text())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="*", help="only fetch these source ids")
    parser.add_argument("--dry-run", action="store_true", help="resolve config, fetch nothing")
    parser.add_argument("--keep-going", action="store_true",
                        help="exit 0 even if some sources failed (never the CI default)")
    args = parser.parse_args()

    sources = load_sources()
    ids = {s["id"] for s in sources}
    dupes = [i for i in ids if [s["id"] for s in sources].count(i) > 1]
    if dupes:
        print(f"ERROR: duplicate source ids in sources.yml: {dupes}", file=sys.stderr)
        return 1

    manifest = manifest_store.load()
    report = runlog.StageReport(stage="fetch", unit="source")
    changed: list[str] = []
    due = [s for s in sources
           if s.get("status") == "fetch" and not (args.only and s["id"] not in args.only)]
    if args.dry_run:
        report.remaining = [s["id"] for s in due]

    for source in due:
        fetcher = _DISPATCH.get(source["type"])
        if fetcher is None:
            report.fail(source["id"], f"no fetcher for type={source['type']}")
            continue

        print(f"fetching {source['id']} ({source['type']}) ...", flush=True)
        if args.dry_run:
            continue

        m_entry = manifest_store.entry(manifest, source["id"])
        try:
            if fetcher(source, m_entry):
                changed.append(source["id"])
                print(f"  -> changed: {source['output']}")
            else:
                print("  -> unchanged")
            m_entry["last_checked"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            report.succeed(source["id"])
        except Exception as exc:  # carry on - the run still fails at the end
            report.fail(source["id"], exc)
            print(f"  -> FAILED: {exc}", file=sys.stderr)
            traceback.print_exc()

    if not args.dry_run:
        manifest_store.save(manifest)
        render_sources_index.main()

    report.extra["changed"] = changed
    runlog.write(PIPELINE_DIR / "last_run.json", [report])

    print(f"\n{len(changed)} source(s) changed, {len(report.failed)} failed.")
    if changed:
        print("Changed:", ", ".join(changed))
    if report.failed:
        print("Failed:")
        for failure in report.failed:
            print(f"  - {failure['unit']}: {failure['error']}")
    print(report.verdict(keep_going=args.keep_going))

    # Emit a summary file for the GitHub Actions workflow to use as a PR body.
    # A partial refresh says so in its first line: the PR is the only place
    # most readers will ever look.
    summary_path = PIPELINE_DIR / "last_run_summary.md"
    lines = []
    if report.failed:
        lines += ["> [!WARNING]", f"> **Partial refresh: {len(report.failed)} of "
                  f"{report.attempted} source(s) failed.** The corpus below is "
                  f"incomplete; the failed sources are left as previously fetched.", ""]
    lines += [f"Refreshed {len(sources)} registered sources; {len(changed)} changed.", ""]
    if changed:
        lines.append("### Changed")
        lines += [f"- `{c}`" for c in changed]
        lines.append("")
    if report.failed:
        lines.append("### Failed (left as previously fetched)")
        lines += runlog.failure_lines([report])
    summary_path.write_text("\n".join(lines) + "\n")

    return report.exit_code(keep_going=args.keep_going)


if __name__ == "__main__":
    sys.exit(main())
