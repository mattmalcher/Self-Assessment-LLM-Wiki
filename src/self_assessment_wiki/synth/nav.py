"""Write the awesome-pages `.pages` files that order the site navigation.

Nav order comes from synth/pages.yml, but only pages that have actually been
composed are listed - awesome-pages warns on a nav entry it can't find, and
`mkdocs build --strict` turns that warning into a failed deploy. So a page
that hasn't been generated yet is simply absent from the nav rather than
breaking the build.

`render` decides the whole nav in memory and `write` puts it on disk, so
`uv run report --check` can compare what is committed against what the page
plan currently implies without touching the working tree.
"""
from __future__ import annotations

from collections.abc import Iterable
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


def render(also_present: Iterable[Path] = ()) -> dict[Path, str]:
    """Every `.pages` file the current page plan implies, path -> content.

    `also_present` names markdown files that are about to be written in the
    same pass - the status page, in practice. Without it the nav would depend
    on whether the status page happened to exist yet, and a first `uv run
    report` on a clean tree would not converge in one run.
    """
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

    files: dict[Path, str] = {}

    pending = {Path(p) for p in also_present}

    def populated(entry: str) -> bool:
        """A nav entry mkdocs will actually see: an existing page, or a
        directory that already holds at least one."""
        target = DOCS_DIR / entry
        if target.is_file() or target in pending:
            return True
        if target.is_dir() and any(target.rglob("*.md")):
            return True
        return any(p.suffix == ".md" and p.is_relative_to(target) for p in pending)

    files[DOCS_DIR / ".pages"] = (
        "# Written by `uv run report` - do not hand-edit.\n"
        "nav:\n" + "".join(f"  - {e}\n" for e in ROOT_NAV if populated(e))
        + "  - ...\n")

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
        files[target / ".pages"] = "\n".join(lines) + "\n"

    return files


def write() -> list[Path]:
    """Put `render`'s files on disk. Returns the paths written."""
    written = []
    for path, content in render().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        written.append(path)
    return written
