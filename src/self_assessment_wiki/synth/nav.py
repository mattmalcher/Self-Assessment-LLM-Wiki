"""Write the awesome-pages `.pages` files that order the site navigation.

Nav order comes from synth/pages.yml, but only pages that have actually been
composed are listed - awesome-pages warns on a nav entry it can't find, and
`mkdocs build --strict` turns that warning into a failed deploy. So a page
that hasn't been generated yet is simply absent from the nav rather than
breaking the build.
"""
from __future__ import annotations

from pathlib import Path

from . import compose
from .config import DOCS_DIR, REPO_ROOT

# Order of the top-level sections, plus the hand-written pages that bracket
# them. Every entry here is a directory or a file that always exists.
ROOT_NAV = [
    "index.md",
    "lifecycle",
    "computation",
    "hmrc",
    "case-law",
    "change",
    "reference-implementation",
    "external-explainers.md",
    "meta",
]

STATIC_TITLES = {
    "meta": "Meta",
    "reference-implementation": "Reference implementation",
}


def write() -> list[Path]:
    specs = compose.load_pages()
    by_dir: dict[str, list[str]] = {}
    titles: dict[str, str] = dict(STATIC_TITLES)

    for spec in specs:
        out = Path(spec["output"])
        directory = out.parent.relative_to("docs").as_posix()
        if spec.get("section"):
            titles.setdefault(directory, spec["section"])
        if (REPO_ROOT / out).exists():
            by_dir.setdefault(directory, []).append(out.name)

    written: list[Path] = []

    def populated(entry: str) -> bool:
        """A nav entry mkdocs will actually see: an existing page, or a
        directory that already holds at least one."""
        target = DOCS_DIR / entry
        if target.is_file():
            return True
        return target.is_dir() and any(target.rglob("*.md"))

    root = DOCS_DIR / ".pages"
    root.write_text("# Written by `uv run report` - do not hand-edit.\n"
                    "nav:\n" + "".join(f"  - {e}\n" for e in ROOT_NAV if populated(e))
                    + "  - ...\n")
    written.append(root)

    for directory, title in sorted(titles.items()):
        target = DOCS_DIR / directory
        if not populated(directory):
            continue
        lines = ["# Written by `uv run report` - do not hand-edit.",
                 f"title: {title}"]
        pages = by_dir.get(directory, [])
        if pages:
            lines.append("nav:")
            lines += [f"  - {name}" for name in pages]
            lines.append("  - ...")   # anything hand-written, alphabetically
        path = target / ".pages"
        path.write_text("\n".join(lines) + "\n")
        written.append(path)

    return written
