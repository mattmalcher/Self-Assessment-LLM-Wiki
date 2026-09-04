#!/usr/bin/env python3
"""Entrypoint: read pipeline/sources.yml, fetch every `status: fetch` source,
write changed markdown into corpus/, and update pipeline/manifest.json.

This is stage 1 of three: it mirrors sources deterministically. Stages 2 and
3 (synth/) read corpus/ and write the wiki in docs/.

Usage:
    uv run fetch                 # fetch everything due
    uv run fetch --only itepa-2003 tma-1970
    uv run fetch --dry-run   # resolve URLs, fetch nothing
"""
from __future__ import annotations

import argparse
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

import yaml

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
    args = parser.parse_args()

    sources = load_sources()
    ids = {s["id"] for s in sources}
    dupes = [i for i in ids if [s["id"] for s in sources].count(i) > 1]
    if dupes:
        print(f"ERROR: duplicate source ids in sources.yml: {dupes}", file=sys.stderr)
        return 1

    manifest = manifest_store.load()
    changed: list[str] = []
    failed: list[tuple[str, str]] = []

    for source in sources:
        if source.get("status") != "fetch":
            continue
        if args.only and source["id"] not in args.only:
            continue

        fetcher = _DISPATCH.get(source["type"])
        if fetcher is None:
            failed.append((source["id"], f"no fetcher for type={source['type']}"))
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
        except Exception as exc:  # keep going - one bad source shouldn't sink the run
            failed.append((source["id"], str(exc)))
            print(f"  -> FAILED: {exc}", file=sys.stderr)
            traceback.print_exc()

    if not args.dry_run:
        manifest_store.save(manifest)
        render_sources_index.main()

    print(f"\n{len(changed)} source(s) changed, {len(failed)} failed.")
    if changed:
        print("Changed:", ", ".join(changed))
    if failed:
        print("Failed:")
        for source_id, err in failed:
            print(f"  - {source_id}: {err}")

    # Emit a summary file for the GitHub Actions workflow to use as a PR body.
    summary_path = PIPELINE_DIR / "last_run_summary.md"
    lines = [f"Refreshed {len(sources)} registered sources; {len(changed)} changed.", ""]
    if changed:
        lines.append("### Changed")
        lines += [f"- `{c}`" for c in changed]
        lines.append("")
    if failed:
        lines.append("### Failed (left as previously fetched)")
        lines += [f"- `{i}`: {e}" for i, e in failed]
    summary_path.write_text("\n".join(lines) + "\n")

    return 1 if failed and not changed and len(failed) == len([s for s in sources if s.get("status") == "fetch"]) else 0


if __name__ == "__main__":
    sys.exit(main())
