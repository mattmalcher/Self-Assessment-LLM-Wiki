"""Regression tests for stage 1 - the fetchers and what they write.

`test_reconcile.py` covers the cache/artifact contract (a warm cache must
rebuild a deleted file). This covers the rest of stage 1: that a GOV.UK
document, collection, manual, Atom feed and plain web page each turn into
the markdown the later stages expect, that the provenance front matter the
extract stage reads is actually written, and that the content-hash cache
skips work only when the file it describes is on disk.

Every upstream response is a fixture; `conditional_get` is monkeypatched in
each module under test, so nothing here touches the network. Run with
`uv run pytest`.
"""
from __future__ import annotations

import pytest

from self_assessment_wiki.pipeline import httpcache, render
from self_assessment_wiki.pipeline.common import FetchResult
from self_assessment_wiki.pipeline.fetchers import caselaw, govuk_content, web_page

WEB_BASE = "https://www.gov.uk"


@pytest.fixture(autouse=True)
def in_tmp_repo(monkeypatch, tmp_path):
    """Fetchers resolve `output` relative to the working directory."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


class FakeApi:
    """`conditional_get` over a dict of path -> JSON document."""

    def __init__(self, docs: dict[str, dict]):
        self.docs = docs
        self.requested: list[str] = []

    def __call__(self, url, cache, *, as_json=False, retries=3):
        self.requested.append(url)
        path = url.replace(f"{govuk_content.API_BASE}", "")
        if path not in self.docs:
            import requests
            response = requests.Response()
            response.status_code = 404
            raise requests.HTTPError(response=response)
        return FetchResult(changed=True, status_code=200, json=self.docs[path])


def doc(base_path: str, title: str, body: str, **extra) -> dict:
    return {"base_path": base_path, "title": title,
            "details": {"body": body, **extra.pop("details", {})},
            **extra}


# --- html -> markdown ------------------------------------------------------

def test_page_chrome_is_removed_content_and_all():
    md = render.html_to_markdown(
        "<nav>Menu</nav><script>tracking()</script><p>The rule.</p>")
    assert "Menu" not in md and "tracking" not in md
    assert "The rule." in md


def test_headings_and_lists_survive_conversion():
    md = render.html_to_markdown("<h2>Returns</h2><ul><li>One</li><li>Two</li></ul>")
    assert "## Returns" in md
    assert "- One" in md and "- Two" in md


def test_runs_of_blank_lines_are_collapsed():
    md = render.html_to_markdown("<p>A</p>" + "<br/>" * 12 + "<p>B</p>")
    assert "\n\n\n\n" not in md


def test_build_page_writes_front_matter_then_the_h1():
    page = render.build_page({"source_id": "tma-1970"}, "TMA 1970", "Body.\n")
    assert page.startswith("---\nsource_id: tma-1970\n---\n\n# TMA 1970\n")


# --- the content-hash cache ------------------------------------------------

def test_unchanged_content_is_not_rewritten(tmp_path):
    entry: dict = {}
    assert render.write_if_changed("corpus/a.md", "same\n", entry) is True
    assert render.write_if_changed("corpus/a.md", "same\n", entry) is False


def test_changed_content_is_rewritten(tmp_path):
    entry: dict = {}
    render.write_if_changed("corpus/a.md", "before\n", entry)
    assert render.write_if_changed("corpus/a.md", "after\n", entry) is True
    assert (tmp_path / "corpus/a.md").read_text() == "after\n"


def test_a_matching_hash_does_not_excuse_a_missing_file(tmp_path):
    """The cache records what was written, not that it is still there."""
    entry: dict = {}
    render.write_if_changed("corpus/a.md", "same\n", entry)
    (tmp_path / "corpus/a.md").unlink()
    assert render.write_if_changed("corpus/a.md", "same\n", entry) is True
    assert (tmp_path / "corpus/a.md").exists()


# --- GOV.UK: a single document --------------------------------------------

GUIDANCE = doc("/guidance/self-assessment", "Self Assessment",
               "<p>You must file by 31 January.</p>",
               document_type="guidance", public_updated_at="2026-01-05T10:00:00Z")

ENTRY = {"id": "sa-guidance", "type": "govuk_content", "status": "fetch",
         "title": "Self Assessment", "url": "/guidance/self-assessment",
         "category": "guidance", "output": "corpus/guidance/sa.md"}


def test_a_govuk_document_becomes_a_page_with_provenance(monkeypatch, tmp_path):
    monkeypatch.setattr(govuk_content, "conditional_get",
                        FakeApi({"/guidance/self-assessment": GUIDANCE}))
    manifest: dict = {}
    assert govuk_content.fetch_single(ENTRY, manifest) is True

    text = (tmp_path / ENTRY["output"]).read_text()
    assert "source_id: sa-guidance" in text
    assert f"source_url: {WEB_BASE}/guidance/self-assessment" in text
    assert "upstream_updated_at: '2026-01-05T10:00:00Z'" in text
    assert "You must file by 31 January." in text
    assert manifest["upstream_updated_at"] == "2026-01-05T10:00:00Z"


def test_a_document_that_404s_is_skipped_rather_than_failing(monkeypatch):
    monkeypatch.setattr(govuk_content, "conditional_get", FakeApi({}))
    assert govuk_content.fetch_single(ENTRY, {}) is False


def test_an_empty_body_still_produces_a_page(monkeypatch, tmp_path):
    monkeypatch.setattr(govuk_content, "conditional_get",
                        FakeApi({"/guidance/x": doc("/guidance/x", "X", "")}))
    govuk_content.fetch_single({**ENTRY, "url": "/guidance/x"}, {})
    assert "*(no body content)*" in (tmp_path / ENTRY["output"]).read_text()


# --- GOV.UK: html attachments (helpsheets) ---------------------------------

def attachment(url: str, title: str) -> dict:
    return {"attachment_type": "html", "url": url, "title": title}


def test_only_the_newest_edition_of_a_helpsheet_is_mirrored(monkeypatch, tmp_path):
    publication = doc("/government/publications/hs340", "HS340",
                      "<p>Summary.</p>", details={"attachments": [
                          attachment("/government/publications/hs340/hs340-2024", "HS340 (2024)"),
                          attachment("/government/publications/hs340/hs340-2025", "HS340 (2025)")]})
    api = FakeApi({
        "/government/publications/hs340": publication,
        "/government/publications/hs340/hs340-2024":
            doc("/government/publications/hs340/hs340-2024", "HS340 2024", "<p>Old.</p>"),
        "/government/publications/hs340/hs340-2025":
            doc("/government/publications/hs340/hs340-2025", "HS340 2025", "<p>New.</p>"),
    })
    monkeypatch.setattr(govuk_content, "conditional_get", api)
    govuk_content.fetch_single({**ENTRY, "url": "/government/publications/hs340"}, {})

    text = (tmp_path / ENTRY["output"]).read_text()
    assert "New." in text and "Old." not in text


def test_html_attachments_can_be_turned_off(monkeypatch, tmp_path):
    publication = doc("/p/hs340", "HS340", "<p>Summary.</p>",
                      details={"attachments": [attachment("/p/hs340/2025", "HS340 (2025)")]})
    monkeypatch.setattr(govuk_content, "conditional_get", FakeApi({
        "/p/hs340": publication,
        "/p/hs340/2025": doc("/p/hs340/2025", "HS340 2025", "<p>Attachment body.</p>")}))
    govuk_content.fetch_single({**ENTRY, "url": "/p/hs340", "html_attachments": "none"}, {})
    assert "Attachment body." not in (tmp_path / ENTRY["output"]).read_text()


# --- GOV.UK: a collection --------------------------------------------------

COLLECTION_ENTRY = {"id": "sa-forms", "type": "govuk_content_collection",
                    "status": "fetch", "title": "SA forms", "category": "guidance",
                    "url": "/government/collections/sa-forms",
                    "output": "corpus/guidance/sa-forms/index.md"}


def collection(*items: dict) -> dict:
    return {"base_path": "/government/collections/sa-forms", "title": "SA forms",
            "details": {"body": ""}, "public_updated_at": "2026-02-01T00:00:00Z",
            "links": {"documents": list(items)}}


def member(base_path: str, title: str, content_id: str) -> dict:
    return {"base_path": base_path, "title": title, "content_id": content_id,
            "public_updated_at": "2026-01-09T00:00:00Z"}


def test_a_collection_becomes_an_index_table(monkeypatch, tmp_path):
    monkeypatch.setattr(govuk_content, "conditional_get", FakeApi({
        "/government/collections/sa-forms": collection(
            member("/g/sa100", "SA100", "id-1"), member("/g/sa102", "SA102", "id-2"))}))
    assert govuk_content.fetch_collection(COLLECTION_ENTRY, {}) is True

    text = (tmp_path / COLLECTION_ENTRY["output"]).read_text()
    assert "| SA100 | 2026-01-09 | [source](https://www.gov.uk/g/sa100) |" in text
    assert "item_count: 2" in text


def test_an_expanded_collection_fetches_each_member(monkeypatch, tmp_path):
    monkeypatch.setattr(govuk_content, "conditional_get", FakeApi({
        "/government/collections/sa-forms": collection(member("/g/sa100", "SA100", "id-1")),
        "/g/sa100": doc("/g/sa100", "SA100", "<p>The main return.</p>")}))
    entry = {**COLLECTION_ENTRY, "expand_items": True,
             "items_dir": "corpus/guidance/sa-forms"}
    assert govuk_content.fetch_collection(entry, {}) is True

    assert "The main return." in (tmp_path / "corpus/guidance/sa-forms/sa100.md").read_text()
    # The index links to the sibling file, not back out to GOV.UK.
    assert "[view](sa100.md)" in (tmp_path / entry["output"]).read_text()


def test_a_collection_with_no_members_keeps_its_prose(monkeypatch, tmp_path):
    """Some collections curate their members in `details.body`; an empty
    table would be worse than the prose."""
    empty = {"base_path": "/government/collections/sa-forms", "title": "SA forms",
             "details": {"body": "<p>See the manuals index.</p>"}, "links": {}}
    monkeypatch.setattr(govuk_content, "conditional_get",
                        FakeApi({"/government/collections/sa-forms": empty}))
    govuk_content.fetch_collection(COLLECTION_ENTRY, {})
    assert "See the manuals index." in (tmp_path / COLLECTION_ENTRY["output"]).read_text()


# --- GOV.UK: a manual ------------------------------------------------------

MANUAL_ENTRY = {"id": "sam", "type": "govuk_content_manual", "status": "fetch",
                "title": "SAM", "category": "hmrc.manuals",
                "url": "/hmrc-internal-manuals/sam", "output": "corpus/manuals/sam.md"}


def branch(base_path: str, title: str, children: list[dict], body: str = "") -> dict:
    return {"base_path": base_path, "title": title, "description": "The manual.",
            "details": {"body": body,
                        "child_section_groups": [{"child_sections": children}]}}


def child(base_path: str, title: str) -> dict:
    return {"base_path": base_path, "title": title}


def test_a_manual_tree_is_walked_to_its_leaves(monkeypatch, tmp_path):
    monkeypatch.setattr(govuk_content, "conditional_get", FakeApi({
        "/hmrc-internal-manuals/sam": branch("/hmrc-internal-manuals/sam", "SAM",
                                             [child("/sam/sam100", "SAM100")]),
        "/sam/sam100": branch("/sam/sam100", "SAM100", [child("/sam/sam100050", "SAM100050")]),
        "/sam/sam100050": doc("/sam/sam100050", "SAM100050", "<p>Criteria for SA.</p>")}))
    assert govuk_content.fetch_manual(MANUAL_ENTRY, {}) is True
    assert "Criteria for SA." in (tmp_path / MANUAL_ENTRY["output"]).read_text()


def test_a_section_that_404s_is_named_rather_than_failing_the_manual(monkeypatch, tmp_path):
    monkeypatch.setattr(govuk_content, "conditional_get", FakeApi({
        "/hmrc-internal-manuals/sam": branch("/hmrc-internal-manuals/sam", "SAM",
                                             [child("/sam/withdrawn", "SAM999")]) }))
    govuk_content.fetch_manual(MANUAL_ENTRY, {})
    text = (tmp_path / MANUAL_ENTRY["output"]).read_text()
    assert "404" in text and "SAM999" in text


def test_max_sections_caps_the_walk_and_says_so(monkeypatch, tmp_path):
    monkeypatch.setattr(govuk_content, "conditional_get", FakeApi({
        "/hmrc-internal-manuals/sam": branch(
            "/hmrc-internal-manuals/sam", "SAM",
            [child("/sam/a", "A"), child("/sam/b", "B"), child("/sam/c", "C")]),
        "/sam/a": doc("/sam/a", "A", "<p>Section A.</p>"),
        "/sam/b": doc("/sam/b", "B", "<p>Section B.</p>"),
        "/sam/c": doc("/sam/c", "C", "<p>Section C.</p>")}))
    govuk_content.fetch_manual({**MANUAL_ENTRY, "max_sections": 1}, {})
    text = (tmp_path / MANUAL_ENTRY["output"]).read_text()
    assert "Section A." in text and "Section C." not in text
    assert "max_sections: 1" in text


# --- Find Case Law ---------------------------------------------------------

ATOM = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:tna="https://caselaw.nationalarchives.gov.uk">
  <entry>
    <title>Smith v HMRC</title>
    <published>2026-03-04T00:00:00Z</published>
    <link rel="alternate" href="https://caselaw.nationalarchives.gov.uk/ukftt/tc/2026/1"/>
    <tna:identifier type="ukncn">[2026] UKFTT 1 (TC)</tna:identifier>
  </entry>
  <entry>
    <title>Jones v HMRC</title>
    <published>2026-02-01T00:00:00Z</published>
    <link rel="alternate" href="https://caselaw.nationalarchives.gov.uk/ukftt/tc/2026/2"/>
    <tna:identifier type="ukncn">[2026] UKFTT 2 (TC)</tna:identifier>
  </entry>
</feed>
"""

FEED_ENTRY = {"id": "ftt-tax", "type": "caselaw_feed", "status": "fetch",
              "title": "First-tier Tribunal (Tax)", "category": "legal-system.case-law",
              "url": "https://caselaw.nationalarchives.gov.uk/atom.xml?court=ukftt/tc",
              "output": "corpus/case-law/ftt-tax.md"}


def test_a_feed_becomes_a_table_of_recent_decisions(monkeypatch, tmp_path):
    monkeypatch.setattr(caselaw, "conditional_get",
                        lambda url, cache, **kw: FetchResult(
                            changed=True, status_code=200, text=ATOM, etag="v1"))
    assert caselaw.fetch(FEED_ENTRY, {}) is True

    text = (tmp_path / FEED_ENTRY["output"]).read_text()
    assert "| 2026-03-04 | [2026] UKFTT 1 (TC) | Smith v HMRC |" in text
    assert "item_count: 2" in text


def test_max_items_caps_the_index(monkeypatch, tmp_path):
    monkeypatch.setattr(caselaw, "conditional_get",
                        lambda url, cache, **kw: FetchResult(
                            changed=True, status_code=200, text=ATOM, etag="v1"))
    caselaw.fetch({**FEED_ENTRY, "max_items": 1}, {})
    text = (tmp_path / FEED_ENTRY["output"]).read_text()
    assert "Smith v HMRC" in text and "Jones v HMRC" not in text


def test_a_304_leaves_the_index_alone(monkeypatch, tmp_path):
    path = tmp_path / FEED_ENTRY["output"]
    path.parent.mkdir(parents=True)
    path.write_text("previous index\n")
    monkeypatch.setattr(caselaw, "conditional_get",
                        lambda url, cache, **kw: FetchResult(changed=False, status_code=304))
    assert caselaw.fetch(FEED_ENTRY, {"http": {"etag": "v1"}}) is False
    assert path.read_text() == "previous index\n"


# --- a plain web page, shared between sources ------------------------------

LITRG = {"id": "litrg-self-assessment", "type": "web_page", "status": "fetch",
         "title": "Self Assessment - LITRG", "category": "explainers",
         "url": "https://litrg.org.uk/self-assessment",
         "output": "corpus/external-explainers.md", "section": "litrg"}
TAXAID = {**LITRG, "id": "taxaid", "title": "TaxAid", "section": "taxaid",
          "url": "https://taxaid.org.uk/self-assessment"}


def test_a_web_page_is_written_as_its_own_section(monkeypatch, tmp_path):
    monkeypatch.setattr(web_page, "conditional_get",
                        lambda url, cache, **kw: FetchResult(
                            changed=True, status_code=200,
                            text="<p>An independent explainer.</p>", etag="v1"))
    assert web_page.fetch(LITRG, {}) is True

    text = (tmp_path / LITRG["output"]).read_text()
    assert "<!-- section:litrg -->" in text and "<!-- /section:litrg -->" in text
    assert "not HMRC/government content" in text
    assert "An independent explainer." in text


def test_two_sources_share_one_file_without_clobbering_each_other(monkeypatch, tmp_path):
    bodies = {LITRG["url"]: "<p>LITRG says.</p>", TAXAID["url"]: "<p>TaxAid says.</p>"}
    monkeypatch.setattr(web_page, "conditional_get",
                        lambda url, cache, **kw: FetchResult(
                            changed=True, status_code=200, text=bodies[url], etag="v1"))
    web_page.fetch(LITRG, {})
    web_page.fetch(TAXAID, {})

    text = (tmp_path / LITRG["output"]).read_text()
    assert "LITRG says." in text and "TaxAid says." in text


def test_a_re_fetch_replaces_only_its_own_section(monkeypatch, tmp_path):
    bodies = {LITRG["url"]: "<p>LITRG first edition.</p>", TAXAID["url"]: "<p>TaxAid says.</p>"}
    get = lambda url, cache, **kw: FetchResult(  # noqa: E731
        changed=True, status_code=200, text=bodies[url], etag="v1")
    monkeypatch.setattr(web_page, "conditional_get", get)
    web_page.fetch(LITRG, {})
    web_page.fetch(TAXAID, {})

    bodies[LITRG["url"]] = "<p>LITRG second edition.</p>"
    web_page.fetch(LITRG, {})

    text = (tmp_path / LITRG["output"]).read_text()
    assert "LITRG second edition." in text
    assert "LITRG first edition." not in text
    assert "TaxAid says." in text
    assert text.count("<!-- section:litrg -->") == 1


# --- GOV.UK: conditional caching -------------------------------------------
#
# The fetchers keep validators per API path (pipeline/httpcache.py) and send
# them on every request. These cover what a second, unchanged run costs, and
# that the two upstreams that don't cooperate - one that never sends a
# validator, one that answers 200 to a conditional request anyway - still
# reach the same "nothing changed" verdict via the timestamp and the content
# hash.


class CachingApi:
    """`conditional_get` over a dict of path -> document, with ETags.

    Answers `304` when the request carries the ETag this path was last served
    with, so a test can assert what a warm run actually downloaded rather than
    only what it wrote. `bump()` republishes a document the way an upstream
    would: new body, new ETag, new `public_updated_at`.
    """

    def __init__(self, docs: dict[str, dict], *, validators: bool = True):
        self.docs = dict(docs)
        self.etags = {path: "v1" for path in docs}
        self.validators = validators
        self.requested: list[str] = []
        self.not_modified: list[str] = []

    def bump(self, path: str, document: dict) -> None:
        self.docs[path] = document
        self.etags[path] = self.etags.get(path, "v1") + "+"

    def reset(self) -> None:
        self.requested = []
        self.not_modified = []

    def __call__(self, url, cache, *, as_json=False, retries=3):
        path = url.replace(govuk_content.API_BASE, "")
        self.requested.append(path)
        if path not in self.docs:
            import requests
            response = requests.Response()
            response.status_code = 404
            raise requests.HTTPError(response=response)
        etag = self.etags[path] if self.validators else None
        if etag is not None and cache.get("etag") == etag:
            self.not_modified.append(path)
            return FetchResult(changed=False, status_code=304, etag=etag)
        return FetchResult(changed=True, status_code=200,
                           json=self.docs[path], etag=etag)


HS340 = doc("/p/hs340", "HS340", "<p>Summary.</p>",
            public_updated_at="2026-01-05T10:00:00Z",
            details={"attachments": [attachment("/p/hs340/2025", "HS340 (2025)")]})
HS340_ATTACHMENT = doc("/p/hs340/2025", "HS340 2025", "<p>First edition.</p>")
HS340_ENTRY = {**ENTRY, "url": "/p/hs340"}


def test_a_second_unchanged_run_is_one_304_and_no_attachment_fetch(monkeypatch):
    api = CachingApi({"/p/hs340": HS340, "/p/hs340/2025": HS340_ATTACHMENT})
    monkeypatch.setattr(govuk_content, "conditional_get", api)
    docs, manifest = {}, {}

    assert govuk_content.fetch_single(HS340_ENTRY, manifest, docs) is True
    assert api.requested == ["/p/hs340", "/p/hs340/2025"]

    api.reset()
    assert govuk_content.fetch_single(HS340_ENTRY, manifest, docs) is False
    assert api.requested == ["/p/hs340"]
    assert api.not_modified == ["/p/hs340"]


def test_a_server_that_ignores_validators_is_skipped_on_its_own_timestamp(monkeypatch):
    """GOV.UK reports `public_updated_at`; a 200 that repeats it is a no-op."""
    api = CachingApi({"/p/hs340": HS340, "/p/hs340/2025": HS340_ATTACHMENT},
                     validators=False)
    monkeypatch.setattr(govuk_content, "conditional_get", api)
    docs, manifest = {}, {}
    govuk_content.fetch_single(HS340_ENTRY, manifest, docs)

    api.reset()
    assert govuk_content.fetch_single(HS340_ENTRY, manifest, docs) is False
    assert api.requested == ["/p/hs340"]  # the attachment is never asked for


def test_no_validators_and_no_timestamp_still_falls_back_to_the_hash(monkeypatch, tmp_path):
    api = CachingApi({"/p/x": doc("/p/x", "X", "<p>Body.</p>")}, validators=False)
    monkeypatch.setattr(govuk_content, "conditional_get", api)
    docs, manifest = {}, {}
    entry = {**ENTRY, "url": "/p/x"}
    assert govuk_content.fetch_single(entry, manifest, docs) is True
    assert govuk_content.fetch_single(entry, manifest, docs) is False
    assert (tmp_path / entry["output"]).read_text().count("Body.") == 1


def test_a_changed_document_re_fetches_its_attachments(monkeypatch, tmp_path):
    api = CachingApi({"/p/hs340": HS340, "/p/hs340/2025": HS340_ATTACHMENT})
    monkeypatch.setattr(govuk_content, "conditional_get", api)
    docs, manifest = {}, {}
    govuk_content.fetch_single(HS340_ENTRY, manifest, docs)

    api.bump("/p/hs340", {**HS340, "public_updated_at": "2026-06-01T10:00:00Z"})
    api.reset()
    assert govuk_content.fetch_single(HS340_ENTRY, manifest, docs) is True
    # The attachment 304s, but the page needs its body: it is asked for again.
    assert api.not_modified == ["/p/hs340/2025"]
    assert "First edition." in (tmp_path / HS340_ENTRY["output"]).read_text()


def test_a_warm_cache_still_rebuilds_a_deleted_page(monkeypatch, tmp_path):
    api = CachingApi({"/p/hs340": HS340, "/p/hs340/2025": HS340_ATTACHMENT})
    monkeypatch.setattr(govuk_content, "conditional_get", api)
    docs, manifest = {}, {}
    govuk_content.fetch_single(HS340_ENTRY, manifest, docs)
    (tmp_path / HS340_ENTRY["output"]).unlink()

    api.reset()
    assert govuk_content.fetch_single(HS340_ENTRY, manifest, docs) is True
    assert api.not_modified == []  # validators dropped; full responses asked for
    assert "First edition." in (tmp_path / HS340_ENTRY["output"]).read_text()


# --- GOV.UK: caching a manual ----------------------------------------------

MANUAL_DOCS = {
    "/hmrc-internal-manuals/sam": branch("/hmrc-internal-manuals/sam", "SAM",
                                         [child("/sam/sam100", "SAM100")]),
    "/sam/sam100": branch("/sam/sam100", "SAM100",
                          [child("/sam/sam100050", "SAM100050"),
                           child("/sam/sam100060", "SAM100060")]),
    "/sam/sam100050": doc("/sam/sam100050", "SAM100050", "<p>Criteria for SA.</p>"),
    "/sam/sam100060": doc("/sam/sam100060", "SAM100060", "<p>Notice to file.</p>"),
}


def warm_manual(monkeypatch, docs=None):
    api = CachingApi(docs or MANUAL_DOCS)
    monkeypatch.setattr(govuk_content, "conditional_get", api)
    store: dict = {}
    manifest: dict = {}
    assert govuk_content.fetch_manual(MANUAL_ENTRY, manifest, store) is True
    api.reset()
    return api, store, manifest


def test_an_unchanged_manual_costs_304s_and_rewrites_nothing(monkeypatch, tmp_path):
    api, store, manifest = warm_manual(monkeypatch)
    before = (tmp_path / MANUAL_ENTRY["output"]).read_text()

    assert govuk_content.fetch_manual(MANUAL_ENTRY, manifest, store) is False
    # Every section is still checked - and every check is a 304, including the
    # branch sections, whose children come from the remembered tree.
    assert set(api.requested) == set(MANUAL_DOCS)
    assert set(api.not_modified) == set(MANUAL_DOCS)
    # Reusing the rendered blocks has to be byte-exact: any churn here would
    # invalidate the extract cache downstream for no upstream change.
    assert (tmp_path / MANUAL_ENTRY["output"]).read_text() == before


def test_only_the_changed_section_of_a_manual_is_re_rendered(monkeypatch, tmp_path):
    api, store, manifest = warm_manual(monkeypatch)
    api.bump("/sam/sam100050", doc("/sam/sam100050", "SAM100050", "<p>New criteria.</p>"))

    assert govuk_content.fetch_manual(MANUAL_ENTRY, manifest, store) is True
    assert "/sam/sam100050" not in api.not_modified
    assert "/sam/sam100060" in api.not_modified

    text = (tmp_path / MANUAL_ENTRY["output"]).read_text()
    assert "New criteria." in text and "Criteria for SA." not in text
    assert "Notice to file." in text  # reused verbatim from the last run


def test_a_section_added_under_an_unchanged_branch_is_picked_up(monkeypatch, tmp_path):
    api, store, manifest = warm_manual(monkeypatch)
    api.bump("/sam/sam100", branch("/sam/sam100", "SAM100",
                                   [child("/sam/sam100050", "SAM100050"),
                                    child("/sam/sam100060", "SAM100060"),
                                    child("/sam/sam100070", "SAM100070")]))
    api.bump("/sam/sam100070", doc("/sam/sam100070", "SAM100070", "<p>Late filing.</p>"))

    assert govuk_content.fetch_manual(MANUAL_ENTRY, manifest, store) is True
    text = (tmp_path / MANUAL_ENTRY["output"]).read_text()
    assert "Late filing." in text and "Criteria for SA." in text


def test_a_deleted_manual_page_is_rebuilt_from_full_responses(monkeypatch, tmp_path):
    api, store, manifest = warm_manual(monkeypatch)
    before = (tmp_path / MANUAL_ENTRY["output"]).read_text()
    (tmp_path / MANUAL_ENTRY["output"]).unlink()

    assert govuk_content.fetch_manual(MANUAL_ENTRY, manifest, store) is True
    # Only the branch section, which never had a body to restore, still 304s.
    assert api.not_modified == ["/sam/sam100"]
    assert (tmp_path / MANUAL_ENTRY["output"]).read_text() == before


def test_a_block_that_is_not_the_one_we_wrote_is_not_a_cache_hit(monkeypatch, tmp_path):
    """The corpus file is the body cache, so each block is hashed into it too;
    an edited page must not be able to feed a 304 back into the next run."""
    api, store, manifest = warm_manual(monkeypatch)
    path = tmp_path / MANUAL_ENTRY["output"]
    path.write_text(path.read_text().replace("Notice to file.", "Edited by hand."))

    govuk_content.fetch_manual(MANUAL_ENTRY, manifest, store)
    assert "/sam/sam100060" not in api.not_modified
    assert "/sam/sam100050" in api.not_modified


# --- GOV.UK: caching a collection ------------------------------------------

EXPANDED = {**COLLECTION_ENTRY, "expand_items": True,
            "items_dir": "corpus/guidance/sa-forms"}
COLLECTION_DOCS = {
    "/government/collections/sa-forms": collection(member("/g/sa100", "SA100", "id-1"),
                                                   member("/g/sa102", "SA102", "id-2")),
    "/g/sa100": doc("/g/sa100", "SA100", "<p>The main return.</p>"),
    "/g/sa102": doc("/g/sa102", "SA102", "<p>Employment pages.</p>"),
}


def warm_collection(monkeypatch):
    api = CachingApi(COLLECTION_DOCS)
    monkeypatch.setattr(govuk_content, "conditional_get", api)
    store: dict = {}
    manifest: dict = {}
    assert govuk_content.fetch_collection(EXPANDED, manifest, store) is True
    api.reset()
    return api, store, manifest


def test_an_unchanged_collection_still_checks_every_member(monkeypatch):
    api, store, manifest = warm_collection(monkeypatch)
    assert govuk_content.fetch_collection(EXPANDED, manifest, store) is False
    # The index document 304s, so its rows cannot have moved - but the members
    # are checked on their own validators, from the remembered member list.
    assert set(api.requested) == set(COLLECTION_DOCS)
    assert set(api.not_modified) == set(COLLECTION_DOCS)


def test_a_changed_member_rewrites_only_its_own_page(monkeypatch, tmp_path):
    api, store, manifest = warm_collection(monkeypatch)
    index_before = (tmp_path / EXPANDED["output"]).read_text()
    sa102_before = (tmp_path / "corpus/guidance/sa-forms/sa102.md").read_text()
    api.bump("/g/sa100", doc("/g/sa100", "SA100", "<p>The main return, revised.</p>"))

    assert govuk_content.fetch_collection(EXPANDED, manifest, store) is True
    assert "revised" in (tmp_path / "corpus/guidance/sa-forms/sa100.md").read_text()
    assert (tmp_path / "corpus/guidance/sa-forms/sa102.md").read_text() == sa102_before
    assert (tmp_path / EXPANDED["output"]).read_text() == index_before


def test_a_deleted_member_page_is_rebuilt_without_touching_the_index(monkeypatch, tmp_path):
    api, store, manifest = warm_collection(monkeypatch)
    (tmp_path / "corpus/guidance/sa-forms/sa100.md").unlink()

    assert govuk_content.fetch_collection(EXPANDED, manifest, store) is True
    assert "The main return." in (tmp_path / "corpus/guidance/sa-forms/sa100.md").read_text()


# --- the cache file itself -------------------------------------------------

def test_fetch_persists_validators_per_source(monkeypatch, tmp_path):
    monkeypatch.setattr(httpcache, "CACHE_DIR", tmp_path / "cache")
    api = CachingApi(MANUAL_DOCS)
    monkeypatch.setattr(govuk_content, "conditional_get", api)

    govuk_content.fetch(MANUAL_ENTRY, {})
    cached = httpcache.load(MANUAL_ENTRY["id"])
    assert set(cached["documents"]) == set(MANUAL_DOCS)
    assert cached["documents"]["/sam/sam100050"]["etag"] == "v1"
    assert [s["path"] for s in cached["manual"]["sections"]] == [
        "/sam/sam100", "/sam/sam100050", "/sam/sam100060"]


def test_a_cache_with_nothing_in_it_leaves_no_file(monkeypatch, tmp_path):
    monkeypatch.setattr(httpcache, "CACHE_DIR", tmp_path / "cache")
    httpcache.save("sam", {"documents": {}})
    assert not httpcache.path_for("sam").exists()


def test_a_404_section_is_still_reported_on_a_cached_run(monkeypatch, tmp_path):
    """Withdrawn sections must not quietly drop out of the page the first time
    their parent answers 304 - the warning is the only record of the gap."""
    docs = {**MANUAL_DOCS}
    docs["/sam/sam100"] = branch("/sam/sam100", "SAM100",
                                 [child("/sam/sam100050", "SAM100050"),
                                  child("/sam/sam100060", "SAM100060"),
                                  child("/sam/withdrawn", "SAM999")])
    api, store, manifest = warm_manual(monkeypatch, docs)
    assert "SAM999" in (tmp_path / MANUAL_ENTRY["output"]).read_text()

    assert govuk_content.fetch_manual(MANUAL_ENTRY, manifest, store) is False
    assert "/sam/withdrawn" in api.requested
    text = (tmp_path / MANUAL_ENTRY["output"]).read_text()
    assert "sections_404: 1" in text and "SAM999" in text
