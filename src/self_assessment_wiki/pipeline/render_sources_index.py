"""Regenerate docs/meta/sources.md from pipeline/sources.yml + manifest.json.

Run automatically at the end of fetch.py so the published registry table
never drifts from the actual sources.yml / manifest state.
"""
from __future__ import annotations

from pathlib import Path

PIPELINE_DIR = Path(__file__).parent
REPO_ROOT = PIPELINE_DIR.parent.parent.parent
OUTPUT = REPO_ROOT / "docs" / "meta" / "sources.md"
GITHUB_BLOB = "https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main"


def _link(source: dict) -> str:
    output = source.get("output")
    if output:
        # The mirror lives in corpus/, which is not part of the published
        # site, so link it on GitHub rather than as a site-relative page.
        return f"[{source['id']}]({GITHUB_BLOB}/{Path(output).as_posix()})"
    return source["id"]


def render(sources: list[dict], manifest: dict) -> str:
    by_category: dict[str, list[dict]] = {}
    for s in sources:
        by_category.setdefault(s["category"], []).append(s)

    lines = [
        "---",
        "title: Sources",
        "---",
        "",
        "# Sources",
        "",
        "Generated from `pipeline/sources.yml` - **do not hand-edit this "
        "file**, it is overwritten on every pipeline run "
        "(`uv run sources-index`, or "
        "automatically at the end of "
        "`uv run fetch`).",
        "",
        "These are the *raw* sources. The fetch pipeline mirrors them into "
        "`corpus/` in the repository; the wiki pages you are reading are "
        "written from that mirror by the synthesis layer - see "
        "[How this wiki stays current](refresh-process.md).",
        "",
        f"{len(sources)} registered sources: "
        f"{sum(1 for s in sources if s.get('status') == 'fetch')} mirrored, "
        f"{sum(1 for s in sources if s.get('status') == 'registered')} registered-only.",
        "",
    ]

    for category in sorted(by_category):
        lines.append(f"## {category}")
        lines.append("")
        lines.append("| Source | Status | Type | Last checked | Upstream updated |")
        lines.append("|---|---|---|---|---|")
        for s in sorted(by_category[category], key=lambda s: s["title"]):
            m = manifest.get(s["id"], {})
            status = s.get("status", "?")
            page = _link(s) if status == "fetch" else s["title"]
            last_checked = m.get("last_checked", "-") if status == "fetch" else "-"
            upstream = m.get("upstream_updated_at", "-") if status == "fetch" else "-"
            lines.append(f"| {page} | {status} | `{s['type']}` | {last_checked} | {upstream} |")
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    import yaml

    sources = yaml.safe_load((PIPELINE_DIR / "sources.yml").read_text())
    manifest = {}
    manifest_path = PIPELINE_DIR / "manifest.json"
    if manifest_path.exists():
        import json

        manifest = json.loads(manifest_path.read_text())

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render(sources, manifest))


if __name__ == "__main__":
    main()
