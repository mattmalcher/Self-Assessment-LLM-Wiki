"""Generic HTML page fetcher, for non-API sources (e.g. LITRG, TaxAid).

Multiple sources can share one output file via `section` - each writes a
`<!-- section:ID -->...<!-- /section:ID -->` block into the target file
without clobbering the others' blocks.
"""
from __future__ import annotations

import re
from pathlib import Path

from ..common import conditional_get
from ..render import html_to_markdown, sha256

_SECTION_RE_TEMPLATE = r"<!-- section:{sid} -->.*?<!-- /section:{sid} -->\n?"


def fetch(entry: dict, manifest_entry: dict) -> bool:
    result = conditional_get(entry["url"], manifest_entry.setdefault("http", {}))
    if not result.changed:
        return False
    manifest_entry["http"] = {"etag": result.etag, "last_modified": result.last_modified}

    body_md = html_to_markdown(result.text or "")
    section_id = entry.get("section", entry["id"])
    block = (
        f"<!-- section:{section_id} -->\n"
        f"## {entry['title']}\n\n"
        f"*Source: <{entry['url']}> - not HMRC/government content; an independent explainer.*\n\n"
        f"{body_md}\n"
        f"<!-- /section:{section_id} -->\n"
    )

    new_hash = sha256(block)
    if manifest_entry.get("content_hash") == new_hash:
        return False
    manifest_entry["content_hash"] = new_hash

    path = Path(entry["output"])
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text() if path.exists() else "# External explainers\n\n"

    pattern = re.compile(_SECTION_RE_TEMPLATE.format(sid=re.escape(section_id)), re.DOTALL)
    if pattern.search(existing):
        updated = pattern.sub(block, existing)
    else:
        updated = existing.rstrip() + "\n\n" + block

    path.write_text(updated)
    return True
