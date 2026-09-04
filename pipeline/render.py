"""HTML -> Markdown conversion and front-matter/page assembly."""
from __future__ import annotations

from pathlib import Path

import yaml
from bs4 import BeautifulSoup
from markdownify import markdownify

from .common import sha256

# Tags that are page chrome / noise (nav, scripts, embedded JSON-LD, etc.),
# not part of the actual document content. markdownify's own `strip` option
# only removes the wrapping tag and keeps the text inside it - not what we
# want for <script>/<style> - so these are fully deleted with BeautifulSoup
# first, content included.
_REMOVE_TAGS = ["script", "style", "nav", "header", "footer", "svg", "button", "noscript", "iframe", "form"]


def html_to_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(_REMOVE_TAGS):
        tag.decompose()

    md = markdownify(
        str(soup),
        heading_style="ATX",
        bullets="-",
    )
    # collapse runs of 3+ blank lines left behind by stripped chrome
    lines = md.splitlines()
    out = []
    blank_run = 0
    for line in lines:
        if line.strip() == "":
            blank_run += 1
            if blank_run > 2:
                continue
        else:
            blank_run = 0
        out.append(line)
    return "\n".join(out).strip() + "\n"


def build_page(front_matter: dict, title: str, body_md: str) -> str:
    fm = yaml.safe_dump(front_matter, sort_keys=False, default_flow_style=False).strip()
    heading = f"# {title}\n\n" if title else ""
    return f"---\n{fm}\n---\n\n{heading}{body_md}"


def write_if_changed(output_path: str, content: str, manifest_entry: dict) -> bool:
    """Write `content` to output_path if its hash differs from what's recorded
    in manifest_entry. Updates manifest_entry["content_hash"] in place.
    Returns True if the file on disk actually changed.
    """
    new_hash = sha256(content)
    if manifest_entry.get("content_hash") == new_hash and Path(output_path).exists():
        return False
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    manifest_entry["content_hash"] = new_hash
    return True
