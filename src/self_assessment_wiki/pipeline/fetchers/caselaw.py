"""caselaw.nationalarchives.gov.uk Atom feed fetcher.

Writes an index page of the most recent decisions for a tribunal (title,
neutral citation, date, link to the judgment). This is deliberately an
index, not full judgment text - judgments are long, unevenly structured,
and best read at the source; the wiki's job is to make them discoverable
and to flag which ones are recent enough to be worth checking.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET

from ..common import conditional_get
from ..reconcile import artifact_missing
from ..render import build_page, write_if_changed

ATOM_NS = "{http://www.w3.org/2005/Atom}"
TNA_NS = "{https://caselaw.nationalarchives.gov.uk}"


def _parse_entries(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    entries = []
    for entry in root.findall(f"{ATOM_NS}entry"):
        title = entry.findtext(f"{ATOM_NS}title", default="")
        published = entry.findtext(f"{ATOM_NS}published", default="")
        link = ""
        for link_el in entry.findall(f"{ATOM_NS}link"):
            if link_el.get("rel") == "alternate" and "type" not in link_el.attrib:
                link = link_el.get("href", "")
                break
        citation = ""
        for ident in entry.findall(f"{TNA_NS}identifier"):
            if ident.get("type") == "ukncn":
                citation = ident.text or ""
                break
        entries.append({"title": title, "published": published, "link": link, "citation": citation})
    return entries


def fetch(entry: dict, manifest_entry: dict) -> bool:
    # A 304 means nothing if the index page it wrote has since gone missing:
    # forget the validators and rebuild it from a full response.
    http_cache = {} if artifact_missing(entry) else manifest_entry.setdefault("http", {})

    result = conditional_get(entry["url"], http_cache)
    if not result.changed:
        return False

    manifest_entry["http"] = {"etag": result.etag, "last_modified": result.last_modified}

    decisions = _parse_entries(result.text or "")
    max_items = entry.get("max_items", 40)
    decisions = decisions[:max_items]

    body_lines = [
        f"The {max_items} most recent decisions from this tribunal, via the "
        f"[Find Case Law]({entry['url']}) Atom feed. Full judgment text lives "
        "at the source link - this page tracks what's recent, not full text.",
        "",
        "| Date | Citation | Case | Judgment |",
        "|---|---|---|---|",
    ]
    for d in decisions:
        date = d["published"][:10]
        body_lines.append(f"| {date} | {d['citation']} | {d['title']} | [link]({d['link']}) |")

    front_matter = {
        "source_url": entry["url"],
        "source_id": entry["id"],
        "category": entry["category"],
        "document_type": "caselaw_feed",
        "item_count": len(decisions),
    }
    page = build_page(front_matter, entry["title"], "\n".join(body_lines) + "\n")
    return write_if_changed(entry["output"], page, manifest_entry)
