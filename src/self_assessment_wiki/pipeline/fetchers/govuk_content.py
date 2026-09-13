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
                            page. Fetches every section by default; set
                            `max_sections` on the entry to cap it.

Caching. One source is many requests here, so validators are kept per API
path in `pipeline/cache/<source-id>.json` (see `pipeline/httpcache.py`) and
every request carries them. What a `304` then buys depends on the shape:

- a single document: the whole source is skipped, attachments included. So
  is a `200` whose `public_updated_at` matches the one recorded in
  `manifest.json` - the timestamp skip, for upstreams that answer `200` to a
  conditional request regardless.
- a collection: the index page is left exactly as it was (its rows come from
  the collection document, which has not moved) and members are still
  checked individually, so a changed member invalidates only its own page.
- a manual section: a `304` carries no body, so the previous run's own
  output is the body cache - the rendered block is lifted out of the corpus
  file and reused verbatim. A changed section re-renders on its own and the
  rest of the manual is byte-identical.

A cache hit is only ever trusted while the artifact it describes is still on
disk; `reconcile.artifact_missing` decides that, exactly as in the other
fetchers. The remembered manual tree is additive - a section that 404s stays
in it so the page keeps reporting it - so deleting a source's cache file is
how you force a manual to be re-walked from the root.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import requests

from .. import httpcache
from ..common import conditional_get, sha256
from ..reconcile import artifact_missing
from ..render import build_page, html_to_markdown, write_if_changed

API_BASE = "https://www.gov.uk/api/content"
WEB_BASE = "https://www.gov.uk"


@dataclass
class DocResult:
    """One content-API response: the document, or why there isn't one."""

    doc: dict | None
    status: str  # "changed" | "unchanged" | "missing"

    @property
    def unchanged(self) -> bool:
        return self.status == "unchanged"

    @property
    def missing(self) -> bool:
        return self.status == "missing"


def _validators(result, doc: dict | None) -> dict:
    stored = {"etag": result.etag, "last_modified": result.last_modified,
              "public_updated_at": (doc or {}).get("public_updated_at")}
    return {k: v for k, v in stored.items() if v}


def _get_doc(path: str, docs: dict | None = None, *, force: bool = False) -> DocResult:
    """GET one content-API document, conditionally on what `docs` remembers.

    `docs` is the source's path -> validators store, updated in place on a
    full response. Pass `force=True` (or no store at all) when a `304` would
    be useless because the caller has no cached body to fall back on.
    """
    if force and docs is not None:
        docs.pop(path, None)
    cache = {} if (force or docs is None) else docs.get(path, {})
    try:
        result = conditional_get(f"{API_BASE}{path}", cache, as_json=True)
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 404:
            # Manual section trees list some sections (withdrawn/renumbered)
            # that 404 on the content API - skip rather than fail the run.
            if docs is not None:
                docs.pop(path, None)
            return DocResult(None, "missing")
        raise
    if not result.changed:
        return DocResult(None, "unchanged")
    if docs is not None:
        docs[path] = _validators(result, result.json)
    return DocResult(result.json, "changed")


def _api_path(base_path: str) -> str:
    return base_path.replace(WEB_BASE, "")


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


def fetch_single(entry: dict, manifest_entry: dict, docs: dict | None = None) -> bool:
    # A cached hit only licenses a skip while the page it produced is still on
    # disk; otherwise re-fetch in full and rewrite it.
    restoring = artifact_missing(entry)
    cached = bool(manifest_entry.get("content_hash")) and not restoring

    result = _get_doc(entry["url"], docs, force=restoring)
    if result.missing:
        return False
    if result.unchanged:
        if cached:
            return False  # 304 on the document itself: attachments not touched
        result = _get_doc(entry["url"], docs, force=True)
        if result.doc is None:
            return False
    doc = result.doc

    # Some upstreams answer 200 to a conditional request whatever the state of
    # the document; GOV.UK's own `public_updated_at` is the second line of
    # defence, and skipping here also skips every attachment request below.
    stamp = doc.get("public_updated_at")
    if cached and stamp and manifest_entry.get("upstream_updated_at") == stamp:
        return False

    details = doc.get("details", {})
    body_html = details.get("body", "") or ""
    parts = [html_to_markdown(body_html)] if body_html.strip() else []
    for att in _html_attachments(details, entry.get("html_attachments", "latest")):
        att_path = _api_path(att["url"])
        att_result = _get_doc(att_path, docs, force=restoring)
        if att_result.unchanged:
            # The document itself moved, so the page has to be rebuilt, and a
            # 304 carries no body to rebuild it from. Ask again unconditionally.
            att_result = _get_doc(att_path, docs, force=True)
        att_doc = att_result.doc
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
        "upstream_updated_at": stamp,
    }
    page = build_page(front_matter, doc.get("title", entry["title"]), body_md)
    manifest_entry["upstream_updated_at"] = stamp
    return write_if_changed(entry["output"], page, manifest_entry)


def _member_entry(entry: dict, item: dict) -> tuple[dict, str]:
    """The synthetic single-document source for one expanded collection member."""
    item_slug = _slugify(item["title"])
    return {
        "id": f"{entry['id']}:{item['content_id']}",
        "url": _api_path(item["base_path"]),
        "title": item["title"],
        "output": f"{entry['items_dir']}/{item_slug}.md",
        "category": entry["category"],
        # Helpsheets arrive as members of a collection; the real text
        # is in their HTML attachment, not in details.body.
        "html_attachments": entry.get("html_attachments", "latest"),
    }, item_slug


def _fetch_member(entry: dict, manifest_entry: dict, item: dict,
                  docs: dict | None) -> tuple[bool, str]:
    item_manifest = manifest_entry.setdefault("items", {}).setdefault(item["content_id"], {})
    item_entry, item_slug = _member_entry(entry, item)
    return fetch_single(item_entry, item_manifest, docs), item_slug


def fetch_collection(entry: dict, manifest_entry: dict, store: dict | None = None) -> bool:
    restoring = artifact_missing(entry)
    docs = None if store is None else store.setdefault("documents", {})

    root = _get_doc(entry["url"], docs, force=restoring)
    if root.missing:
        return False

    stored_items = (store or {}).get("items")
    if root.unchanged and not (stored_items and manifest_entry.get("content_hash")):
        # Nothing cached to rebuild the index from - ask for the whole thing.
        root = _get_doc(entry["url"], docs, force=True)
        if root.doc is None:
            return False

    if root.doc is None:
        # The collection document has not moved, so neither have the index's
        # rows: leave the page alone and check the members on their own
        # validators, so only a changed member rewrites anything.
        changed_any = False
        for item in stored_items:
            if entry.get("expand_items") and _fetch_member(entry, manifest_entry, item, docs)[0]:
                changed_any = True
        return changed_any

    doc = root.doc
    documents = doc.get("links", {}).get("documents", [])
    documents.sort(key=lambda d: d.get("title", ""))
    if store is not None:
        store["items"] = [{"content_id": d["content_id"], "base_path": d["base_path"],
                           "title": d.get("title", "")} for d in documents]

    changed_any = False
    rows = []
    for item in documents:
        item_link = f"{WEB_BASE}{item['base_path']}"
        if entry.get("expand_items"):
            item_changed, item_slug = _fetch_member(entry, manifest_entry, item, docs)
            changed_any = changed_any or item_changed
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


_SOURCE_LINE = re.compile(r"^\*Source: <(?P<url>[^>]+)>\*$", re.M)


def _block_hash(block: str) -> str:
    """Enough of the block's hash to notice it is not the block we wrote."""
    return sha256(block)[:16]


def _section_block(title: str, doc: dict) -> str:
    section_id = doc.get("details", {}).get("section_id", "")
    heading = f"## {section_id} — {title}" if section_id else f"## {title}"
    return "\n".join([
        heading,
        f"*Source: <{WEB_BASE}{doc['base_path']}>*",
        "",
        html_to_markdown(doc["details"]["body"]),
        "\n---\n",
    ])


def _cached_blocks(output_path: str) -> dict[str, str]:
    """The section blocks already in the manual's page, keyed by source URL.

    A 304 for a section carries no body, so the previous run's own output is
    the body cache: each block runs from its `## ` heading to the one before
    the next section's heading, which is exactly what `_section_block` built.
    Reusing the slice verbatim is what keeps an unchanged manual byte-identical
    - anything else would churn the corpus and invalidate the extract cache
    downstream for no upstream change at all.
    """
    path = Path(output_path)
    if not path.exists():
        return {}
    text = path.read_text()
    marks = list(_SOURCE_LINE.finditer(text))
    starts = []
    for mark in marks:
        heading = text.rfind("\n## ", 0, mark.start())
        starts.append(None if heading < 0 else heading + 1)

    blocks: dict[str, str] = {}
    for i, (mark, start) in enumerate(zip(marks, starts)):
        if start is None:
            continue
        following = next((s for s in starts[i + 1:] if s is not None), None)
        end = len(text) if following is None else following - 1
        blocks[mark.group("url")] = text[start:end]
    return blocks


def fetch_manual(entry: dict, manifest_entry: dict, store: dict | None = None) -> bool:
    max_sections = entry.get("max_sections")
    restoring = artifact_missing(entry)
    docs = None if store is None else store.setdefault("documents", {})
    manual = {} if store is None else store.setdefault("manual", {})
    # A page that is gone cannot supply the bodies a 304 leaves out.
    blocks = {} if restoring else _cached_blocks(entry["output"])

    root = _get_doc(entry["url"], docs, force=restoring)
    known = {s["path"]: s for s in manual.get("sections", [])}
    if root.unchanged and not (known and manual.get("description") is not None):
        root = _get_doc(entry["url"], docs, force=True)
    if root.doc is None and not known:
        return False
    intro = manual.get("description", "") if root.doc is None else (root.doc.get("description") or "")
    if store is not None and root.doc is not None:
        manual["description"] = intro

    # The tree the last run walked, plus whatever the root lists today. A 304
    # for a branch section carries no `child_section_groups`, so without the
    # remembered order the walk would stop at the first unchanged branch.
    frontier: list[tuple[str, str]] = [(s["title"], s["path"]) for s in known.values()]
    seen = set(known)
    for group in (root.doc or {}).get("details", {}).get("child_section_groups", []):
        for section in group.get("child_sections", []):
            path = _api_path(section["base_path"])
            if path not in seen:
                seen.add(path)
                frontier.append((section["title"], path))

    order: list[dict] = []
    leaves: list[str] = []
    missing: list[tuple[str, str]] = []
    fetched = 0
    index = 0
    while index < len(frontier) and (max_sections is None or fetched < max_sections):
        title, path = frontier[index]
        index += 1
        prior = known.get(path, {})
        # Normally the section's own `base_path`, but a section that answers on
        # a different path than the tree advertises is keyed by what was written.
        block_url = prior.get("url", f"{WEB_BASE}{path}")
        reused = blocks.get(block_url) if prior.get("body") else None
        if reused is not None and prior.get("hash") != _block_hash(reused):
            # The page is the body cache, so a block that is not the one this
            # run wrote (a hand edit, a half-written file) is not a cache hit.
            reused = None
        # Only accept a 304 when this section can be rebuilt without a body:
        # its block from the last run, or the knowledge that it had none.
        result = _get_doc(path, docs, force=not (reused or (prior and not prior.get("body"))))
        fetched += 1

        if result.missing:
            # Still part of the tree: a 404 is reported on the page every run,
            # and dropping the section here would make that warning disappear
            # the moment its parent section started answering 304.
            missing.append((title, path))
            order.append({"title": title, "path": path, "body": False})
            continue
        if result.unchanged:
            order.append({"title": title, "path": path, "body": bool(reused),
                          **({"hash": prior["hash"], "url": block_url} if reused else {})})
            if reused:
                leaves.append(reused)
            continue

        doc = result.doc
        body = doc.get("details", {}).get("body", "") or ""
        block = _section_block(title, doc) if body.strip() else None
        order.append({"title": title, "path": path, "body": bool(block),
                      **({"hash": _block_hash(block),
                          "url": f"{WEB_BASE}{doc['base_path']}"} if block else {})})
        if block:
            leaves.append(block)
        for group in doc.get("details", {}).get("child_section_groups", []):
            for section in group.get("child_sections", []):
                child_path = _api_path(section["base_path"])
                if child_path not in seen:
                    seen.add(child_path)
                    frontier.append((section["title"], child_path))

    remaining = len(frontier) - index
    if store is not None:
        # Sections past `max_sections` were not visited this run but are still
        # part of the tree; forgetting them would re-walk from scratch.
        manual["sections"] = order + [
            {"title": title, "path": path, **{k: v for k, v in known.get(path, {}).items()
                                              if k in ("body", "hash", "url")}}
            for title, path in frontier[index:]]
        if docs is not None:
            keep = {entry["url"]} | {s["path"] for s in manual["sections"]}
            for path in [p for p in docs if p not in keep]:
                docs.pop(path)

    body_lines = [intro, ""]
    if remaining:
        body_lines.append(
            f"> This manual has more sections than were mirrored this run "
            f"(`max_sections: {max_sections}` in `pipeline/sources.yml`, "
            f"~{remaining} more queued). Raise the cap and re-run to pull the rest. "
            f"Full manual: <{WEB_BASE}{entry['url']}>."
        )
        body_lines.append("")
    if missing:
        body_lines.append(
            f"> {len(missing)} section(s) listed in this manual's navigation "
            f"404'd on GOV.UK's content API and were skipped - likely withdrawn "
            f"or renumbered sections the manual's own contents page hasn't "
            f"caught up with. Content here may be incomplete as a result:"
        )
        for title, path in missing:
            body_lines.append(f"> - {title}: <{WEB_BASE}{path}>")
        body_lines.append("")

    front_matter = {
        "source_url": f"{WEB_BASE}{entry['url']}",
        "source_id": entry["id"],
        "category": entry["category"],
        "document_type": "manual",
        "sections_mirrored": len(leaves),
        "sections_404": len(missing),
    }
    page = build_page(front_matter, entry["title"], "\n".join(body_lines + leaves))
    return write_if_changed(entry["output"], page, manifest_entry)


def fetch(entry: dict, manifest_entry: dict) -> bool:
    kind = entry["type"]
    store = httpcache.load(entry["id"])
    if kind == "govuk_content":
        changed = fetch_single(entry, manifest_entry, store.setdefault("documents", {}))
    elif kind == "govuk_content_collection":
        changed = fetch_collection(entry, manifest_entry, store)
    elif kind == "govuk_content_manual":
        changed = fetch_manual(entry, manifest_entry, store)
    else:
        raise ValueError(f"govuk_content fetcher can't handle type={kind}")
    # Only after the write: a run that died half way through has no page to
    # rebuild unchanged sections from, and must not claim otherwise.
    httpcache.save(entry["id"], store)
    return changed
