"""GOV.UK Content API fetcher.

Covers three source `type`s that all key off the same API
(`https://www.gov.uk/api/content<path>`):

- govuk_content            a single document (guidance page, helpsheet, a
                            manual leaf section, a policy paper) -> one page
- govuk_content_collection a `document_collection` -> an index page (table
                            of title / upstream last-updated / link), and if
                            `expand_items: true`, one fetched page per member
- govuk_content_manual     a `manual` hub -> walks `child_section_groups`
                            recursively (manuals are trees; content lives at
                            leaf sections, "contents" nodes are just
                            branches) and writes every leaf's body into one
                            page, capped at `max_sections` per run
"""
from __future__ import annotations

import re

from ..common import conditional_get
from ..render import build_page, html_to_markdown, write_if_changed

API_BASE = "https://www.gov.uk/api/content"
WEB_BASE = "https://www.gov.uk"


def _get_doc(path: str) -> dict | None:
    result = conditional_get(f"{API_BASE}{path}", {}, as_json=True)
    return result.json


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "item"


def _html_attachments(details: dict, mode: str) -> list[dict]:
    """The HTML attachments worth mirroring, newest edition only by default.

    For a helpsheet publication `details.body` is a 200-500 character summary;
    the helpsheet itself is an `html` attachment, one per tax year. Mirroring
    every year would quadruple the corpus for no gain, so `latest` keeps only
    the attachments carrying the highest year seen in their title or URL.
    """
    if mode == "none":
        return []
    html = [a for a in details.get("attachments", []) or []
            if a.get("attachment_type") == "html" and a.get("url")]
    if mode == "all" or len(html) < 2:
        return html

    def year(att: dict) -> int:
        years = re.findall(r"(?:19|20)\d{2}", f"{att.get('title', '')} {att['url']}")
        return max((int(y) for y in years), default=0)

    newest = max(year(a) for a in html)
    return [a for a in html if year(a) == newest] if newest else html[:1]


def fetch_single(entry: dict, manifest_entry: dict) -> bool:
    doc = _get_doc(entry["url"])
    if doc is None:
        return False
    details = doc.get("details", {})
    body_html = details.get("body", "") or ""
    parts = [html_to_markdown(body_html)] if body_html.strip() else []
    for att in _html_attachments(details, entry.get("html_attachments", "latest")):
        att_doc = _get_doc(att["url"] if att["url"].startswith("/") else att["url"].replace(WEB_BASE, ""))
        att_body = (att_doc or {}).get("details", {}).get("body", "") or ""
        if not att_body.strip():
            continue
        parts.append(f"## {att_doc.get('title', att.get('title', 'Attachment'))}")
        parts.append(f"*Source: <{WEB_BASE}{att_doc['base_path']}>*\n")
        parts.append(html_to_markdown(att_body))
    body_md = "\n\n".join(p for p in parts if p.strip()) or "*(no body content)*"
    front_matter = {
        "source_url": f"{WEB_BASE}{doc['base_path']}",
        "source_id": entry["id"],
        "category": entry["category"],
        "document_type": doc.get("document_type"),
        "upstream_updated_at": doc.get("public_updated_at"),
    }
    page = build_page(front_matter, doc.get("title", entry["title"]), body_md)
    manifest_entry["upstream_updated_at"] = doc.get("public_updated_at")
    return write_if_changed(entry["output"], page, manifest_entry)


def fetch_collection(entry: dict, manifest_entry: dict) -> bool:
    doc = _get_doc(entry["url"])
    if doc is None:
        return False
    documents = doc.get("links", {}).get("documents", [])
    documents.sort(key=lambda d: d.get("title", ""))

    changed_any = False
    rows = []
    for item in documents:
        item_link = f"{WEB_BASE}{item['base_path']}"
        if entry.get("expand_items"):
            item_manifest = manifest_entry.setdefault("items", {}).setdefault(item["content_id"], {})
            item_slug = _slugify(item["title"])
            item_output = f"{entry['items_dir']}/{item_slug}.md"
            item_entry = {
                "id": f"{entry['id']}:{item['content_id']}",
                "url": item["base_path"],
                "title": item["title"],
                "output": item_output,
                "category": entry["category"],
                # Helpsheets arrive as members of a collection; the real text
                # is in their HTML attachment, not in details.body.
                "html_attachments": entry.get("html_attachments", "latest"),
            }
            if fetch_single(item_entry, item_manifest):
                changed_any = True
            # index.md and item pages live in the same directory (items_dir)
            item_link = f"{item_slug}.md"
        updated = (item.get("public_updated_at") or "")[:10]
        rows.append((item["title"], updated, item_link))

    if documents:
        body_lines = [
            f"Full index of the **{doc.get('title', entry['title'])}** collection "
            f"from GOV.UK ({len(documents)} documents).",
            "",
            "| Title | Upstream last updated | Link |",
            "|---|---|---|",
        ]
        for title, updated, link in rows:
            body_lines.append(
                f"| {title} | {updated} | [{'source' if not entry.get('expand_items') else 'view'}]({link}) |")
    else:
        # Some collections (HMRC manuals) list their members in a curated
        # `details.body` and leave `links.documents` empty; an empty table is
        # worse than the prose.
        body_lines = [html_to_markdown(doc.get("details", {}).get("body", "") or "")
                      or "*(no member documents listed)*"]

    front_matter = {
        "source_url": f"{WEB_BASE}{doc['base_path']}",
        "source_id": entry["id"],
        "category": entry["category"],
        "document_type": "document_collection",
        "upstream_updated_at": doc.get("public_updated_at"),
        "item_count": len(documents),
    }
    page = build_page(front_matter, doc.get("title", entry["title"]), "\n".join(body_lines) + "\n")
    manifest_entry["upstream_updated_at"] = doc.get("public_updated_at")
    index_changed = write_if_changed(entry["output"], page, manifest_entry)
    return changed_any or index_changed


def _collect_leaf_sections(root_path: str, max_sections: int) -> tuple[list[tuple[str, dict]], int]:
    """BFS over a manual's section tree; returns [(breadcrumb, section_doc), ...]
    for sections that actually have body content, up to max_sections fetches.
    """
    root = _get_doc(root_path)
    if root is None:
        return [], 0
    frontier: list[tuple[str, str]] = []  # (breadcrumb_title, base_path)
    for group in root.get("details", {}).get("child_section_groups", []):
        for section in group.get("child_sections", []):
            frontier.append((section["title"], section["base_path"]))

    leaves = []
    fetched = 0
    while frontier and fetched < max_sections:
        title, path = frontier.pop(0)
        doc = _get_doc(path.replace(WEB_BASE, ""))
        fetched += 1
        if doc is None:
            continue
        body = doc.get("details", {}).get("body", "") or ""
        if body.strip():
            leaves.append((title, doc))
        for group in doc.get("details", {}).get("child_section_groups", []):
            for section in group.get("child_sections", []):
                frontier.append((section["title"], section["base_path"]))

    return leaves, len(frontier)


def fetch_manual(entry: dict, manifest_entry: dict) -> bool:
    max_sections = entry.get("max_sections", 80)
    leaves, remaining = _collect_leaf_sections(entry["url"], max_sections)

    root = _get_doc(entry["url"])
    intro = root.get("description", "") if root else ""

    body_lines = [intro, ""]
    if remaining:
        body_lines.append(
            f"> This manual has more sections than were mirrored this run "
            f"(`max_sections: {max_sections}` in `pipeline/sources.yml`, "
            f"~{remaining} more queued). Raise the cap and re-run to pull the rest. "
            f"Full manual: <{WEB_BASE}{entry['url']}>."
        )
        body_lines.append("")

    for title, doc in leaves:
        section_id = doc.get("details", {}).get("section_id", "")
        heading = f"## {section_id} — {title}" if section_id else f"## {title}"
        body_lines.append(heading)
        body_lines.append(f"*Source: <{WEB_BASE}{doc['base_path']}>*")
        body_lines.append("")
        body_lines.append(html_to_markdown(doc["details"]["body"]))
        body_lines.append("\n---\n")

    front_matter = {
        "source_url": f"{WEB_BASE}{entry['url']}",
        "source_id": entry["id"],
        "category": entry["category"],
        "document_type": "manual",
        "sections_mirrored": len(leaves),
    }
    page = build_page(front_matter, entry["title"], "\n".join(body_lines))
    return write_if_changed(entry["output"], page, manifest_entry)


def fetch(entry: dict, manifest_entry: dict) -> bool:
    kind = entry["type"]
    if kind == "govuk_content":
        return fetch_single(entry, manifest_entry)
    if kind == "govuk_content_collection":
        return fetch_collection(entry, manifest_entry)
    if kind == "govuk_content_manual":
        return fetch_manual(entry, manifest_entry)
    raise ValueError(f"govuk_content fetcher can't handle type={kind}")
