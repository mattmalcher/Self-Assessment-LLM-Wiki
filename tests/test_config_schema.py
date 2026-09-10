"""Regression tests for configuration validation (see
`self_assessment_wiki.configcheck`).

Two classes of failure are locked down here. The first is a late error: a
misspelled `type`, `status` or relevance tier used to be discovered by a
fetcher mid-run, or not at all - a page whose `relevance: [cores]` matched no
tier composed from an empty note set and said nothing. The second is a write
outside its root: every writer in the pipeline does
`Path(entry["output"]).write_text(...)`, so `output: /tmp/x` or
`../../secrets.md` went wherever it pointed.

The real `sources.yml` and `pages.yml` are validated too - a committed
registry that does not pass its own schema is the bug these rules exist to
catch. No model calls, no network.
"""
from __future__ import annotations

import pytest

from self_assessment_wiki import configcheck
from self_assessment_wiki.pipeline import fetch
from self_assessment_wiki.synth import compose

SOURCE = {"id": "tma-1970", "category": "legal-system.primary-legislation",
          "type": "legislation", "title": "Taxes Management Act 1970",
          "url": "https://www.legislation.gov.uk/ukpga/1970/9",
          "status": "fetch", "output": "corpus/acts/tma-1970.md"}
PAGE = {"id": "who-must-file", "title": "Who must file", "section": "Lifecycle",
        "output": "docs/lifecycle/who-must-file.md", "brief": "Say who must file.",
        "authorities": ["tma-1970"],
        "select": {"relevance": ["core"], "match": ["notice to file"], "max_notes": 80}}


def source(**overrides) -> dict:
    return {**SOURCE, **overrides}


def page(**overrides) -> dict:
    return {**PAGE, **overrides}


def errors_for_source(**overrides) -> list[str]:
    return configcheck.validate_sources([source(**overrides)])


def errors_for_page(**overrides) -> list[str]:
    return configcheck.validate_pages([page(**overrides)])


# --- the committed configuration ------------------------------------------

def test_committed_sources_are_valid():
    assert configcheck.validate_sources(fetch.load_sources()) == []


def test_committed_pages_are_valid():
    assert configcheck.validate_pages(compose.load_pages()) == []


def test_baseline_fixtures_are_valid():
    """Otherwise every assertion below could be passing for the wrong reason."""
    assert configcheck.validate_sources([SOURCE]) == []
    assert configcheck.validate_pages([PAGE]) == []


# --- shape and required fields --------------------------------------------

@pytest.mark.parametrize("validator", [configcheck.validate_sources,
                                       configcheck.validate_pages])
@pytest.mark.parametrize("data", [None, {}, [], "- id: x", [["id"]]])
def test_non_list_or_empty_config_is_rejected(validator, data):
    assert validator(data)


@pytest.mark.parametrize("key", configcheck.SOURCE_REQUIRED)
def test_missing_required_source_key_is_reported(key):
    entry = source()
    del entry[key]
    assert any(repr(key) in e for e in configcheck.validate_sources([entry]))


@pytest.mark.parametrize("key", configcheck.PAGE_REQUIRED)
def test_missing_required_page_key_is_reported(key):
    entry = page()
    del entry[key]
    assert any(repr(key) in e for e in configcheck.validate_pages([entry]))


@pytest.mark.parametrize("authorities", [None, [], "tma-1970", ["TMA 1970"],
                                           ["tma-1970", "tma-1970"]])
def test_authorities_must_be_a_non_empty_unique_list_of_source_ids(authorities):
    assert any("authorit" in error for error in errors_for_page(authorities=authorities))


def test_page_authorities_must_name_registered_sources():
    assert configcheck.validate_authority_references([PAGE], [SOURCE]) == []
    errors = configcheck.validate_authority_references(
        [page(authorities=["missing-act"])], [SOURCE])
    assert errors == [
        "who-must-file: authority 'missing-act' is not present in sources.yml"]


def test_unknown_keys_are_rejected():
    """A key nothing reads is usually a misspelled key something does."""
    assert any("'outputs'" in e for e in errors_for_source(outputs="corpus/x.md"))
    assert any("'selector'" in e for e in errors_for_page(selector={}))


def test_type_specific_key_on_the_wrong_type_is_rejected():
    """`max_items` caps a caselaw feed and nothing else; on a manual it is a
    silent no-op that reads like a cap."""
    assert errors_for_source(max_items=10)
    assert configcheck.validate_sources(
        [source(type="caselaw_feed",
                url="https://caselaw.nationalarchives.gov.uk/atom.xml?court=ukftt/tc",
                max_items=10)]) == []


def test_unknown_select_key_is_rejected():
    assert any("'matches'" in e for e in
               errors_for_page(select={"matches": ["x"]}))


# --- enums, ids and types --------------------------------------------------

def test_unknown_source_type_is_rejected():
    assert any("type" in e for e in errors_for_source(type="govuk_contents"))


def test_unknown_status_is_rejected():
    assert any("status" in e for e in errors_for_source(status="fetched"))


def test_unknown_relevance_tier_is_rejected():
    """The failure mode: `cores` matches no tier, so the page silently
    composes from no notes at all."""
    assert any("relevance" in e for e in
               errors_for_page(select={"relevance": ["cores"]}))


@pytest.mark.parametrize("bad_id", ["TMA-1970", "tma 1970", "-tma", "", None, 1970])
def test_ids_must_be_slugs(bad_id):
    assert any("id" in e for e in errors_for_source(id=bad_id))
    assert any("id" in e for e in errors_for_page(id=bad_id))


def test_duplicate_source_ids_are_rejected():
    errors = configcheck.validate_sources(
        [source(), source(output="corpus/acts/other.md")])
    assert any("duplicate source id" in e for e in errors)


def test_duplicate_page_ids_are_rejected():
    errors = configcheck.validate_pages(
        [page(), page(output="docs/lifecycle/other.md")])
    assert any("duplicate page id" in e for e in errors)


def test_uncompilable_match_regex_is_rejected():
    assert any("does not compile" in e for e in
               errors_for_page(select={"match": ["notice (to file"]}))


@pytest.mark.parametrize("value", [0, -1, "80", 1.5, True])
def test_max_notes_must_be_a_positive_int(value):
    assert any("max_notes" in e for e in
               errors_for_page(select={"max_notes": value}))


@pytest.mark.parametrize("key,value", [("relevance", "core"), ("match", "x"),
                                       ("docs", "hmrc-publications")])
def test_select_lists_must_be_lists(key, value):
    assert any(f"select.{key}" in e for e in errors_for_page(select={key: value}))


def test_select_must_be_a_mapping():
    assert any("select" in e for e in errors_for_page(select=["core"]))


# --- url shape -------------------------------------------------------------

def test_govuk_url_must_be_a_content_api_path():
    """A full URL here resolves to https://www.gov.uk/api/contenthttps://..."""
    assert any("Content API path" in e for e in
               errors_for_source(type="govuk_content",
                                 url="https://www.gov.uk/guidance/hmrc-tools"))
    assert configcheck.validate_sources(
        [source(type="govuk_content", url="/guidance/hmrc-tools")]) == []


def test_non_govuk_url_must_be_absolute():
    assert any("must be absolute" in e for e in
               errors_for_source(url="/ukpga/1970/9"))


# --- output paths ----------------------------------------------------------

@pytest.mark.parametrize("bad", [
    "/tmp/escape.md",
    "../../escape.md",
    "corpus/../../escape.md",
    "corpus/./escape.md",
    "~/escape.md",
    "corpus\\acts\\tma.md",
    "docs/lifecycle/who-must-file.md",   # fetched material is never under docs/
    "corpus",
    "corpus/acts/tma-1970",              # not a markdown file
    "",
    None,
    42,
])
def test_source_output_must_be_contained_in_corpus(bad):
    assert any("output" in e for e in errors_for_source(output=bad))


@pytest.mark.parametrize("bad", [
    "/etc/motd.md",
    "../corpus/leak.md",
    "docs/../../leak.md",
    "corpus/lifecycle/who-must-file.md",  # a composed page is never in corpus/
    "docs",
    "docs/lifecycle/who-must-file",
])
def test_page_output_must_be_contained_in_docs(bad):
    assert any("output" in e for e in errors_for_page(output=bad))


def test_fetched_source_needs_an_output():
    entry = source()
    del entry["output"]
    assert any("needs an output path" in e for e in configcheck.validate_sources([entry]))


def test_registered_source_needs_no_output():
    entry = source(status="registered")
    del entry["output"]
    assert configcheck.validate_sources([entry]) == []


@pytest.mark.parametrize("protected", sorted(configcheck.PROTECTED_OUTPUTS))
def test_page_may_not_overwrite_a_hand_maintained_file(protected):
    assert any("overwrite" in e for e in errors_for_page(output=protected))


# --- collisions ------------------------------------------------------------

def test_two_pages_may_not_write_one_file():
    errors = configcheck.validate_pages([page(), page(id="the-return")])
    assert any("already written by" in e for e in errors)


def test_two_non_web_page_sources_may_not_share_an_output():
    errors = configcheck.validate_sources(
        [source(), source(id="crca-2005", url="https://www.legislation.gov.uk/ukpga/2005/11")])
    assert any("only web_page sources may share" in e for e in errors)


def test_web_page_sources_may_share_an_output_via_distinct_sections():
    shared = {"type": "web_page", "status": "fetch", "category": "external-explainers",
              "output": "corpus/external-explainers.md"}
    assert configcheck.validate_sources([
        {**shared, "id": "taxaid-self-assessment", "title": "TaxAid",
         "url": "https://taxaid.org.uk/self-assessment", "section": "taxaid"},
        {**shared, "id": "litrg-self-assessment", "title": "LITRG",
         "url": "https://www.litrg.org.uk/self-assessment", "section": "litrg"},
    ]) == []


def test_web_page_sources_may_not_share_one_section():
    shared = {"type": "web_page", "status": "fetch", "category": "external-explainers",
              "output": "corpus/external-explainers.md", "section": "explainer"}
    errors = configcheck.validate_sources([
        {**shared, "id": "taxaid-self-assessment", "title": "TaxAid",
         "url": "https://taxaid.org.uk/self-assessment"},
        {**shared, "id": "litrg-self-assessment", "title": "LITRG",
         "url": "https://www.litrg.org.uk/self-assessment"},
    ])
    assert any("claimed by more than one source" in e for e in errors)


# --- expanded collections --------------------------------------------------

COLLECTION = {"id": "sa-helpsheets", "category": "hmrc-publications.customer-facing-guidance",
              "type": "govuk_content_collection", "title": "Helpsheets",
              "url": "/government/collections/self-assessment-helpsheets",
              "status": "fetch", "output": "corpus/hmrc-publications/helpsheets/index.md"}


def test_expanded_collection_needs_an_items_dir():
    assert any("items_dir" in e for e in
               configcheck.validate_sources([{**COLLECTION, "expand_items": True}]))


def test_items_dir_must_hold_the_index():
    """The index links its members relatively; a directory elsewhere writes
    pages nothing points at."""
    errors = configcheck.validate_sources([
        {**COLLECTION, "expand_items": True,
         "items_dir": "corpus/hmrc-publications/elsewhere"}])
    assert any("must be the directory holding output" in e for e in errors)


def test_items_dir_is_contained_too():
    errors = configcheck.validate_sources([
        {**COLLECTION, "expand_items": True, "items_dir": "/tmp/items"}])
    assert any("items_dir" in e for e in errors)


def test_valid_expanded_collection():
    assert configcheck.validate_sources([
        {**COLLECTION, "expand_items": True, "html_attachments": "latest",
         "items_dir": "corpus/hmrc-publications/helpsheets"}]) == []


def test_unknown_html_attachment_mode_is_rejected():
    errors = configcheck.validate_sources([{**COLLECTION, "html_attachments": "newest"}])
    assert any("html_attachments" in e for e in errors)


# --- how the failure reaches the operator ---------------------------------

def test_load_raises_with_every_problem_listed(tmp_path):
    path = tmp_path / "sources.yml"
    path.write_text(
        "- id: BAD_ID\n"
        "  category: legal-system.primary-legislation\n"
        "  type: legislation\n"
        "  title: Taxes Management Act 1970\n"
        "  url: https://www.legislation.gov.uk/ukpga/1970/9\n"
        "  status: fetch\n"
        "  output: /tmp/escape.md\n")
    with pytest.raises(configcheck.ConfigError) as exc_info:
        configcheck.load_sources(path)
    message = str(exc_info.value)
    assert "2 problem(s)" in message
    assert "BAD_ID" in message and "/tmp/escape.md" in message


def test_load_returns_the_parsed_config(tmp_path):
    path = tmp_path / "pages.yml"
    path.write_text("- id: who-must-file\n"
                    "  title: Who must file\n"
                    "  section: Lifecycle\n"
                    "  output: docs/lifecycle/who-must-file.md\n"
                    "  brief: Say who must file.\n"
                    "  authorities: [tma-1970]\n")
    assert configcheck.load_pages(path)[0]["id"] == "who-must-file"
