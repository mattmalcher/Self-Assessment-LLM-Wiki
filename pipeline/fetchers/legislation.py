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

from ..common import conditional_get
from ..render import build_page, html_to_markdown, write_if_changed

_PART_LINK_RE = re.compile(r'href="/[a-z]+/\d+/\d+/part/([A-Za-z0-9]+)"')


def fetch(entry: dict, manifest_entry: dict) -> bool:
    base_url = entry["url"].rstrip("/")

    contents = conditional_get(f"{base_url}/contents", manifest_entry.setdefault("http", {}))
    if not contents.changed and manifest_entry.get("content_hash"):
        return False  # contents page unchanged - assume body unchanged too

    part_ids = list(dict.fromkeys(_PART_LINK_RE.findall(contents.text or "")))

    sections_md = []
    if part_ids:
        for part_id in part_ids:
            part = conditional_get(f"{base_url}/part/{part_id}/data.xht", {})
            if part.text:
                sections_md.append(html_to_markdown(part.text))
    else:
        whole = conditional_get(f"{base_url}/data.xht", {})
        if whole.text:
            sections_md.append(html_to_markdown(whole.text))

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
