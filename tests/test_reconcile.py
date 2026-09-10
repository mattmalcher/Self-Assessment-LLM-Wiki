"""Regression tests for cache/artifact reconciliation (see
`self_assessment_wiki.pipeline.reconcile`).

The failure these lock down is the one `taxaid-self-assessment` actually hit:
the manifest recorded a content hash, the file it described was gone, and
every later run said "unchanged" and left the corpus short. A warm cache must
rebuild a deleted artifact, and an artifact that never comes back must fail a
command rather than sit in the registry unnoticed. No model calls, no network.
"""
from __future__ import annotations

import json

import pytest

from self_assessment_wiki.pipeline import fetch, reconcile
from self_assessment_wiki.pipeline.common import FetchResult
from self_assessment_wiki.pipeline.fetchers import caselaw, legislation, web_page

TAXAID = {"id": "taxaid-self-assessment", "type": "web_page", "status": "fetch",
          "title": "Self Assessment advice - TaxAid",
          "url": "https://taxaid.org.uk/self-assessment",
          "output": "corpus/external-explainers.md", "section": "taxaid"}
OTHER_SECTION = {**TAXAID, "id": "other-explainer", "title": "Other",
                 "url": "https://example.org/other", "section": "other"}
ACT = {"id": "tma-1970", "type": "legislation", "status": "fetch",
       "title": "Taxes Management Act 1970", "category": "legal-system.primary-legislation",
       "url": "https://www.legislation.gov.uk/ukpga/1970/9",
       "output": "corpus/acts/tma-1970.md"}
FEED = {"id": "ftt-tax", "type": "caselaw_feed", "status": "fetch",
        "title": "First-tier Tribunal (Tax)", "category": "legal-system.case-law",
        "url": "https://caselaw.nationalarchives.gov.uk/atom.xml?court=ukftt/tc",
        "output": "corpus/case-law/ftt-tax.md"}


class FakeUpstream:
    """`conditional_get` that answers 304 to anyone holding a validator.

    That is the state a warm cache is in, and the state in which the bug
    used to be invisible: the only way to get the body back is to ask
    without validators.
    """

    def __init__(self, body: str):
        self.body = body
        self.caches_seen: list[dict] = []

    def __call__(self, url, cache, *, as_json=False, retries=3):
        self.caches_seen.append(dict(cache))
        if cache.get("etag"):
            return FetchResult(changed=False, status_code=304, etag=cache["etag"])
        return FetchResult(changed=True, status_code=200, text=self.body, etag="v1")


@pytest.fixture(autouse=True)
def in_tmp_corpus(monkeypatch, tmp_path):
    """Fetchers resolve `output` relative to the working directory."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


# --- the audit itself ------------------------------------------------------

def test_missing_file_is_a_reconciliation_failure():
    assert reconcile.problem(TAXAID) == "missing output file: corpus/external-explainers.md"


def test_empty_file_is_a_reconciliation_failure(in_tmp_corpus):
    path = in_tmp_corpus / TAXAID["output"]
    path.parent.mkdir(parents=True)
    path.write_text("")
    assert "empty output file" in reconcile.problem(TAXAID)


def test_shared_file_is_checked_section_by_section(in_tmp_corpus):
    """A present file is no evidence for the sources that share it."""
    path = in_tmp_corpus / TAXAID["output"]
    path.parent.mkdir(parents=True)
    path.write_text("# External explainers\n\n"
                    "<!-- section:other -->\n## Other\n<!-- /section:other -->\n")
    assert reconcile.problem(OTHER_SECTION) is None
    assert reconcile.problem(TAXAID) == (
        "missing section `taxaid` in shared output corpus/external-explainers.md")


def test_unterminated_section_is_a_reconciliation_failure(in_tmp_corpus):
    path = in_tmp_corpus / TAXAID["output"]
    path.parent.mkdir(parents=True)
    path.write_text("<!-- section:taxaid -->\n## truncated mid-write\n")
    assert "unterminated section `taxaid`" in reconcile.problem(TAXAID)


def test_audit_covers_every_fetchable_source_and_ignores_the_rest():
    sources = [TAXAID, {**ACT, "status": "registered"}, FEED]
    report = reconcile.audit(sources)
    assert report.attempted == 2
    assert {f["unit"] for f in report.failed} == {"taxaid-self-assessment", "ftt-tax"}
    assert report.exit_code() == 1


def test_a_fetch_source_with_no_output_configured_fails():
    assert reconcile.problem({"id": "x", "type": "web_page", "status": "fetch"}) == (
        "status: fetch but no output path configured")


# --- restoring from a warm cache -------------------------------------------

def test_web_page_restores_a_deleted_section_from_a_warm_cache(monkeypatch, in_tmp_corpus):
    upstream = FakeUpstream("<h2>TaxAid</h2><p>Self Assessment advice.</p>")
    monkeypatch.setattr(web_page, "conditional_get", upstream)
    manifest_entry: dict = {}

    assert web_page.fetch(TAXAID, manifest_entry) is True
    cached_hash = manifest_entry["content_hash"]
    path = in_tmp_corpus / TAXAID["output"]
    assert "<!-- section:taxaid -->" in path.read_text()

    # Warm cache, artifact intact: nothing to do.
    assert web_page.fetch(TAXAID, manifest_entry) is False

    path.unlink()
    assert web_page.fetch(TAXAID, manifest_entry) is True
    assert "<!-- section:taxaid -->" in path.read_text()
    # Restored from an unchanged response: the content never moved.
    assert manifest_entry["content_hash"] == cached_hash
    # ... and it only came back because the validators were dropped.
    assert upstream.caches_seen[-1] == {}


def test_restoring_one_section_keeps_the_others(monkeypatch, in_tmp_corpus):
    monkeypatch.setattr(web_page, "conditional_get", FakeUpstream("<p>taxaid</p>"))
    taxaid_manifest: dict = {}
    web_page.fetch(TAXAID, taxaid_manifest)

    monkeypatch.setattr(web_page, "conditional_get", FakeUpstream("<p>other</p>"))
    web_page.fetch(OTHER_SECTION, {})

    path = in_tmp_corpus / TAXAID["output"]
    path.write_text("# External explainers\n\n"
                    "<!-- section:other -->\n## Other\n<!-- /section:other -->\n")

    monkeypatch.setattr(web_page, "conditional_get", FakeUpstream("<p>taxaid</p>"))
    assert web_page.fetch(TAXAID, taxaid_manifest) is True
    restored = path.read_text()
    assert "<!-- section:taxaid -->" in restored
    assert "<!-- section:other -->" in restored


def test_legislation_restores_a_deleted_page_from_a_warm_cache(monkeypatch, in_tmp_corpus):
    upstream = FakeUpstream("<h1>Taxes Management Act 1970</h1><p>Section 8.</p>")
    monkeypatch.setattr(legislation, "conditional_get", upstream)
    manifest_entry: dict = {}

    assert legislation.fetch(ACT, manifest_entry) is True
    path = in_tmp_corpus / ACT["output"]
    assert path.exists()
    assert legislation.fetch(ACT, manifest_entry) is False

    path.unlink()
    assert legislation.fetch(ACT, manifest_entry) is True
    assert "Taxes Management Act 1970" in path.read_text()


def test_caselaw_restores_a_deleted_index_from_a_warm_cache(monkeypatch, in_tmp_corpus):
    atom = ('<feed xmlns="http://www.w3.org/2005/Atom"><entry>'
            '<title>Smith v HMRC</title><published>2026-01-02T00:00:00Z</published>'
            '<link rel="alternate" href="https://caselaw.example/1"/>'
            '</entry></feed>')
    monkeypatch.setattr(caselaw, "conditional_get", FakeUpstream(atom))
    manifest_entry: dict = {}

    assert caselaw.fetch(FEED, manifest_entry) is True
    path = in_tmp_corpus / FEED["output"]
    assert caselaw.fetch(FEED, manifest_entry) is False

    path.unlink()
    assert caselaw.fetch(FEED, manifest_entry) is True
    assert "Smith v HMRC" in path.read_text()


# --- the run report --------------------------------------------------------

def test_fetch_fails_when_a_successful_source_leaves_no_artifact(monkeypatch, in_tmp_corpus):
    """The exact TaxAid failure mode: a fetcher reports success, writes nothing,
    and the run has to say so instead of banking a hollow refresh."""
    monkeypatch.setattr(fetch, "PIPELINE_DIR", in_tmp_corpus)
    monkeypatch.setattr(fetch, "load_sources", lambda: [TAXAID])
    monkeypatch.setattr(fetch.manifest_store, "load", lambda: {})
    monkeypatch.setattr(fetch.manifest_store, "save", lambda manifest: None)
    monkeypatch.setattr(fetch.render_sources_index, "main", lambda: 0)
    monkeypatch.setitem(fetch._DISPATCH, "web_page", lambda source, entry: False)
    monkeypatch.setattr("sys.argv", ["fetch"])

    assert fetch.main() == 1

    payload = json.loads((in_tmp_corpus / "last_run.json").read_text())
    stages = {s["stage"]: s for s in payload["stages"]}
    assert payload["ok"] is False
    assert stages["fetch"]["succeeded"] == ["taxaid-self-assessment"]
    assert stages["reconcile"]["failed"][0]["unit"] == "taxaid-self-assessment"
    assert "missing output file" in stages["reconcile"]["failed"][0]["error"]

    summary = (in_tmp_corpus / "last_run_summary.md").read_text()
    assert "Configured but missing from the corpus" in summary


def test_keep_going_downgrades_a_reconciliation_failure(monkeypatch, in_tmp_corpus):
    monkeypatch.setattr(fetch, "PIPELINE_DIR", in_tmp_corpus)
    monkeypatch.setattr(fetch, "load_sources", lambda: [TAXAID])
    monkeypatch.setattr(fetch.manifest_store, "load", lambda: {})
    monkeypatch.setattr(fetch.manifest_store, "save", lambda manifest: None)
    monkeypatch.setattr(fetch.render_sources_index, "main", lambda: 0)
    monkeypatch.setitem(fetch._DISPATCH, "web_page", lambda source, entry: False)
    monkeypatch.setattr("sys.argv", ["fetch", "--keep-going"])

    assert fetch.main() == 0
    payload = json.loads((in_tmp_corpus / "last_run.json").read_text())
    assert payload["ok"] is False  # the report still tells the truth
