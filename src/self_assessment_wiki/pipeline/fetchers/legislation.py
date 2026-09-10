"""legislation.gov.uk fetcher.

Strategy: fetch the Act/SI's `contents` page to enumerate its Parts (if it
has any), then fetch each Part's clean XHTML fragment (`/part/<n>/data.xht`)
and concatenate into one markdown page. Acts/SIs with no Parts fall back to
fetching the whole document's `/data.xht` directly.

This trades page-count for request-count: an Act like ITEPA 2003 becomes
~10-15 requests (one per Part) rather than one per section, which would be
hundreds. Some resulting pages are long (a Part can itself be substantial)
but each is one coherent, correctly-ordered legal document.
"""
from __future__ import annotations

import re

from bs4 import BeautifulSoup, NavigableString, Tag

from ..common import conditional_get
from ..reconcile import artifact_missing
from ..render import build_page, html_to_markdown, write_if_changed

_PART_LINK_RE = re.compile(r'href="/[a-z]+/\d+/\d+/part/([A-Za-z0-9]+)"')

_HOST_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li")
_BLOCK_TAGS = frozenset(
    {"div", "p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "ul", "ol", "table", "tr", "td", "th"}
)

# A heading/paragraph is built from adjacent <span>s with no whitespace between
# them, because the real layout comes from CSS floats. Concatenating the text
# naively welds the pieces together ("1Responsibility", "(a)income tax"), so a
# space is inserted where one side ends and the other starts on a word.
_JOIN_LEFT = ")]."
_JOIN_RIGHT = "[“‘\"'"


def _needs_space(left: str, right: str) -> bool:
    if not left or not right or left[-1].isspace() or right[0].isspace():
        return False
    return (left[-1].isalnum() or left[-1] in _JOIN_LEFT) and (
        right[0].isalnum() or right[0] in _JOIN_RIGHT
    )


def _is_leg_element(node) -> bool:
    return isinstance(node, Tag) and any(c.startswith("Leg") for c in node.get("class", []))


def _is_block(node) -> bool:
    return isinstance(node, Tag) and node.name in _BLOCK_TAGS


def _rstrip_tail(host: Tag) -> None:
    """Trim trailing whitespace from the last text in `host`, however deeply nested."""
    for text in reversed(host.find_all(string=True)):
        if not text.strip():
            text.extract()
            continue
        if text != text.rstrip():
            text.replace_with(NavigableString(text.rstrip()))
        return


def tidy_legislation_html(html: str) -> str:
    """Normalise legislation.gov.uk XHTML fragments before markdown conversion."""
    soup = BeautifulSoup(html, "html.parser")

    # Extent markers ("U.K.", "E+W") are gutter labels typeset inline, so they
    # land mid-heading ("PART IU.K. ADMINISTRATION"). Hoist each to the end of
    # its heading/paragraph, parenthesised.
    for ext in soup.find_all("span", class_="LegExtentRestriction"):
        text = ext.get_text(strip=True)
        host = ext.find_parent(_HOST_TAGS)
        ext.decompose()
        if text and host is not None:
            _rstrip_tail(host)
            host.append(NavigableString(f" ({text})"))

    for tag in soup.find_all(True):
        children = list(tag.children)
        for prev, nxt in zip(children, children[1:]):
            if _is_block(prev) or _is_block(nxt):
                continue  # markdownify already separates block elements
            if not (_is_leg_element(prev) or _is_leg_element(nxt)):
                continue
            if _needs_space(prev.get_text(), nxt.get_text()):
                prev.insert_after(NavigableString(" "))

    return str(soup)


def fetch(entry: dict, manifest_entry: dict) -> bool:
    base_url = entry["url"].rstrip("/")

    # An unchanged contents page only licenses a skip while the page it
    # produced is still on disk; otherwise re-fetch it in full to restore it.
    restoring = artifact_missing(entry)
    http_cache = {} if restoring else manifest_entry.setdefault("http", {})

    contents = conditional_get(f"{base_url}/contents", http_cache)
    if not contents.changed and manifest_entry.get("content_hash") and not restoring:
        return False  # contents page unchanged - assume body unchanged too

    part_ids = list(dict.fromkeys(_PART_LINK_RE.findall(contents.text or "")))

    sections_md = []
    if part_ids:
        for part_id in part_ids:
            part = conditional_get(f"{base_url}/part/{part_id}/data.xht", {})
            if part.text:
                sections_md.append(html_to_markdown(tidy_legislation_html(part.text)))
    else:
        whole = conditional_get(f"{base_url}/data.xht", {})
        if whole.text:
            sections_md.append(html_to_markdown(tidy_legislation_html(whole.text)))

    body_md = "\n\n---\n\n".join(sections_md)
    title = entry["title"]

    front_matter = {
        "source_url": f"{base_url}/contents",
        "source_id": entry["id"],
        "category": entry["category"],
        "legislation_type": "Act of Parliament" if "/ukpga/" in base_url else "Statutory Instrument",
    }
    page = build_page(front_matter, title, body_md)

    changed = write_if_changed(entry["output"], page, manifest_entry)
    manifest_entry["http"] = {"etag": contents.etag, "last_modified": contents.last_modified}
    return changed
