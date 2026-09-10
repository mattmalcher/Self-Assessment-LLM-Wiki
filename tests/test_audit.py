"""Regression tests for the offline artifact audit (see `audit`).

The audit is the gate that reads the published artifacts themselves rather
than the code that wrote them, so these tests build a whole small pipeline on
disk - registry, corpus, extracts, manifests, pages - assert that a healthy
one is silent, then break exactly one thing at a time and check that the
audit names it and gets its severity right.

The severity split is the part worth locking down. A broken artifact must
fail a deploy; outstanding model work (a malformed cached note, an
unsupported citation) must be reported without blocking the pages that are
fine. No model calls, no network. Run with `uv run pytest`.
"""
from __future__ import annotations

import json

import pytest

from self_assessment_wiki import audit, citations, configcheck
from self_assessment_wiki.synth import compose, store

DOC = "legislation/tma-1970.md"

NOTE = {
    "relevance": "core",
    "summary": "A person given a notice under TMA 1970 s.8 must deliver a return.",
    "topics": ["filing"],
    "obligations": [{"who": "the person", "must": "deliver a return",
                     "trigger": "a notice to file", "deadline": "31 January",
                     "ref": "TMA 1970 s.8(1)"}],
    "deadlines": [], "amounts": [], "penalties": [],
    "definitions": [], "cross_references": [], "caveats": [],
}

SOURCE = {"id": "tma-1970", "type": "legislation", "status": "fetch",
          "category": "legal-system.primary-legislation",
          "title": "Taxes Management Act 1970",
          "url": "https://www.legislation.gov.uk/ukpga/1970/9",
          "output": f"corpus/{DOC}"}

SPEC = {"id": "who-must-file", "title": "Who must file", "section": "The lifecycle",
        "output": "docs/lifecycle/who-must-file.md",
        "brief": "Who is brought into Self Assessment.",
        "select": {"relevance": ["core"]}}

CORPUS_TEXT = f"""---
source_url: https://www.legislation.gov.uk/ukpga/1970/9/contents
source_id: tma-1970
category: legal-system.primary-legislation
---

# Taxes Management Act 1970

## 8 Personal return

A person may be required by a notice to deliver a return (TMA 1970 s.8(1)).
"""


def page_text(body: str, *, title: str = SPEC["title"],
              docs: tuple[str, ...] = (DOC,), input_hash: str = "") -> str:
    """A page in the exact shape `compose.run` writes one."""
    front = ("---\n"
             f"title: {title}\n"
             "generated: true\n"
             "generated_on: 2026-09-01\n"
             "generated_by: fake:model\n"
             f"input_hash: {input_hash}\n"
             "note_count: 1\n"
             "sources:\n- tma-1970\n"
             "---\n\n")
    footer = "\n".join(["", "---", "", audit.PROVENANCE_HEADING, ""]
                       + [f"- [tma-1970](https://example.org) - 1 note(s) - "
                          f"mirrored at `corpus/{doc}`" for doc in docs])
    return (front + f"# {title}\n" + compose.DISCLAIMER + "\n" + body
            + "\n" + footer + "\n")


@pytest.fixture
def repo(monkeypatch, tmp_path):
    """A complete, healthy pipeline: one source, one document, one page."""
    corpus = tmp_path / "corpus"
    extracts = tmp_path / "extracts"
    (corpus / DOC).parent.mkdir(parents=True)
    (corpus / DOC).write_text(CORPUS_TEXT)
    extracts.mkdir()

    extract_data = {"doc": DOC, "source_id": "tma-1970",
                    "source_url": "https://www.legislation.gov.uk/ukpga/1970/9",
                    "chunks": {"c0ffee": {"index": 0, "heading": "s.8",
                                          "prompt_hash": "p", "model": "fake:model",
                                          "note": json.loads(json.dumps(NOTE))}}}
    (extracts / "tma-1970.json").write_text(json.dumps(extract_data))

    loaded = {DOC: extract_data}
    notes = compose.select(SPEC, loaded)
    ihash = compose.input_hash(SPEC, notes, "model")
    manifest = {SPEC["id"]: {"input_hash": ihash, "output": SPEC["output"],
                             "generated_on": "2026-09-01",
                             "generated_by": "fake:model", "note_count": len(notes)}}

    page = tmp_path / SPEC["output"]
    page.parent.mkdir(parents=True)
    page.write_text(page_text("The rule is at TMA 1970 s.8(1).", input_hash=ihash))

    monkeypatch.setattr(audit, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(audit, "CORPUS_DIR", corpus)
    monkeypatch.setattr(audit, "EXTRACTS_DIR", extracts)
    monkeypatch.setattr(audit, "REPORT_PATH", tmp_path / "last_audit.json")
    monkeypatch.setattr(compose, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(audit.pipeline_fetch, "load_sources", lambda: [dict(SOURCE)])
    monkeypatch.setattr(audit.pipeline_manifest, "load", lambda: {"tma-1970": {}})
    monkeypatch.setattr(compose, "load_pages", lambda: [dict(SPEC)])
    monkeypatch.setattr(compose, "load_manifest", lambda: manifest)
    monkeypatch.setattr(store, "load_all", lambda: loaded)
    # The status/nav gate has its own suite (`test_report_sync.py`); here it
    # would only re-test `report.drift` through a second front door.
    monkeypatch.setattr(audit.report, "drift", lambda: [])
    # Chunking the fixture corpus is real work `test_chunk.py` covers; the
    # cache check is exercised directly below.
    monkeypatch.setattr(audit.extract, "plan", lambda only=None: [])

    class Repo:
        root = tmp_path
        corpus_dir = corpus
        extracts_dir = extracts
        page_path = page
        extract_path = extracts / "tma-1970.json"

        @staticmethod
        def write_page(body: str, **kwargs) -> None:
            kwargs.setdefault("input_hash", ihash)
            page.write_text(page_text(body, **kwargs))

        @staticmethod
        def write_extract(data: dict) -> None:
            (extracts / "tma-1970.json").write_text(json.dumps(data))
            loaded.clear()
            loaded[data.get("doc", DOC)] = data

    return Repo


def errors(only: list[str] | None = None) -> list[str]:
    return [m for f in audit.run(only).values() for m in f.errors]


def warnings(only: list[str] | None = None) -> list[str]:
    return [m for f in audit.run(only).values() for m in f.warnings]


# --- a healthy tree is silent ----------------------------------------------

def test_a_healthy_pipeline_has_nothing_to_report(repo):
    assert errors() == []
    assert warnings() == []


def test_a_healthy_pipeline_exits_zero(repo, capsys):
    assert audit.main([]) == 0


def test_every_check_runs_by_default(repo):
    assert set(audit.run()) == set(audit.CHECKS)


def test_only_runs_the_named_checks(repo):
    assert set(audit.run(["pages"])) == {"pages"}


# --- configuration ---------------------------------------------------------

def test_invalid_configuration_is_an_error(repo, monkeypatch):
    def explode():
        raise configcheck.ConfigError("sources.yml", ["entry 1: missing key 'id'"])

    monkeypatch.setattr(audit.pipeline_fetch, "load_sources", explode)
    assert any("missing key 'id'" in e for e in errors(["config"]))


def test_a_check_downstream_of_bad_config_stays_quiet(repo, monkeypatch):
    """One broken registry should be reported once, not by every check."""
    def explode():
        raise configcheck.ConfigError("sources.yml", ["entry 1: missing key 'id'"])

    monkeypatch.setattr(audit.pipeline_fetch, "load_sources", explode)
    assert errors(["sources"]) == []
    assert errors(["corpus"]) == []


# --- corpus ----------------------------------------------------------------

def test_a_fetched_source_with_no_artifact_is_an_error(repo):
    (repo.corpus_dir / DOC).unlink()
    assert any("missing output file" in e for e in errors(["sources"]))


def test_a_mirrored_document_without_provenance_is_an_error(repo):
    (repo.corpus_dir / DOC).write_text("---\ntitle: TMA\n---\n\n# TMA\n")
    assert any("front matter is missing source_id, source_url" in e
               for e in errors(["corpus"]))


def test_a_hand_written_corpus_index_needs_no_provenance(repo):
    """`corpus/` also holds hand-written index pages no fetcher owns."""
    (repo.corpus_dir / "secondary-legislation.md").write_text("# SIs\n")
    assert errors(["corpus"]) == []


# --- extracts --------------------------------------------------------------

def test_an_extract_file_with_no_corpus_document_is_an_error(repo):
    repo.write_extract({"doc": "legislation/repealed.md", "chunks": {}})
    assert any("no corpus document" in e for e in errors(["extracts"]))


def test_unparseable_extract_json_is_an_error(repo):
    repo.extract_path.write_text("{not json")
    assert any("not valid JSON" in e for e in errors(["extracts"]))


def test_a_malformed_note_is_a_warning_not_a_deploy_blocker(repo):
    """The design answer to a malformed note is already in place: it is not
    counted as cached and no page may cite it. It is outstanding model work,
    so it must not block the deploy of pages that correctly exclude it."""
    broken = {"index": 0, "heading": "s.8", "note": {"obligations": "not a list"}}
    repo.write_extract({"doc": DOC, "chunks": {"c0ffee": broken}})
    assert errors(["extracts"]) == []
    assert any("missing key" in w for w in warnings(["extracts"]))


def test_strict_promotes_a_malformed_note_to_a_failure(repo):
    broken = {"index": 0, "heading": "s.8", "note": {"obligations": "not a list"}}
    repo.write_extract({"doc": DOC, "chunks": {"c0ffee": broken}})
    assert audit.as_report(audit.run(["extracts"]), strict=False).ok
    assert not audit.as_report(audit.run(["extracts"]), strict=True).ok


# --- manifests -------------------------------------------------------------

def test_a_manifest_entry_for_an_unknown_page_is_an_error(repo, monkeypatch):
    monkeypatch.setattr(compose, "load_manifest",
                        lambda: {"deleted-page": {"output": "docs/x.md"}})
    assert any("not in pages.yml" in e for e in errors(["manifests"]))


def test_a_manifest_entry_whose_page_is_gone_is_an_error(repo):
    repo.page_path.unlink()
    assert any("does not exist" in e for e in errors(["manifests"]))


def test_a_manifest_output_that_contradicts_the_plan_is_an_error(repo, monkeypatch):
    monkeypatch.setattr(compose, "load_manifest",
                        lambda: {SPEC["id"]: {"output": "docs/lifecycle/elsewhere.md"}})
    assert any("records output" in e for e in errors(["manifests"]))


def test_a_fetch_manifest_entry_for_an_unknown_source_is_a_warning(repo, monkeypatch):
    monkeypatch.setattr(audit.pipeline_manifest, "load", lambda: {"retired": {}})
    assert errors(["manifests"]) == []
    assert any("not in sources.yml" in w for w in warnings(["manifests"]))


# --- page structure --------------------------------------------------------

def test_a_page_without_an_h1_is_an_error(repo):
    repo.page_path.write_text(
        page_text("body").replace(f"# {SPEC['title']}\n", ""))
    assert any("exactly one H1" in e for e in errors(["pages"]))


def test_a_page_whose_h1_is_not_its_title_is_an_error(repo):
    repo.page_path.write_text(page_text("body").replace(
        f"# {SPEC['title']}", "# Something else", 1))
    assert any("is not the page plan's" in e for e in errors(["pages"]))


def test_a_hash_comment_inside_a_code_fence_is_not_an_h1(repo):
    repo.write_page("```python\n# step 1: the filing obligation\nx = 1\n```\n")
    assert errors(["pages"]) == []


def test_a_page_without_the_disclaimer_is_an_error(repo):
    repo.page_path.write_text(page_text("body").replace(compose.DISCLAIMER, "\n"))
    assert any("disclaimer is missing" in e for e in errors(["pages"]))


def test_a_page_without_a_provenance_footer_is_an_error(repo):
    repo.page_path.write_text(page_text("body").split(audit.PROVENANCE_HEADING)[0])
    assert any("footer" in e for e in errors(["pages"]))


def test_a_footer_naming_a_document_not_in_the_corpus_is_an_error(repo):
    repo.write_page("body", docs=("legislation/never-mirrored.md",))
    assert any("not in the mirrored corpus" in e for e in errors(["pages"]))


def test_a_page_composed_from_no_notes_is_an_error(repo, monkeypatch):
    monkeypatch.setattr(compose, "load_manifest",
                        lambda: {SPEC["id"]: {"output": SPEC["output"], "note_count": 0}})
    assert any("composed from no notes" in e for e in errors(["pages"]))


def test_a_page_that_was_never_composed_is_not_a_page_error(repo):
    """The plan gap belongs to the status page, not to page structure."""
    repo.page_path.unlink()
    assert errors(["pages"]) == []


# --- citation provenance ---------------------------------------------------

def test_a_citation_absent_from_the_selected_notes_is_detected(repo):
    repo.write_page("Partnership returns are required (TMA 1970 s.122AA(2)).")
    found = warnings(["citations"])
    assert len(found) == 1
    assert "s.122AA" in found[0]


def test_a_citation_present_in_the_notes_is_accepted(repo):
    repo.write_page("A notice may require a return (TMA 1970 s.8(1)).")
    assert warnings(["citations"]) == []


def test_a_manual_reference_absent_from_the_notes_is_detected(repo):
    repo.write_page("HMRC's view is at SAM100050.")
    assert any("SAM100050" in w for w in warnings(["citations"]))


def test_the_generated_footer_is_not_read_as_the_model_s_citations(repo):
    """The provenance footer is written by `compose`, not by the model."""
    repo.write_page("Nothing is cited here.", docs=(DOC,))
    assert warnings(["citations"]) == []


def test_an_unsupported_citation_does_not_block_a_deploy(repo):
    repo.write_page("Partnership returns are required (TMA 1970 s.122AA(2)).")
    assert errors(["citations"]) == []
    assert audit.main(["--only", "citations"]) == 0


def test_strict_promotes_an_unsupported_citation_to_a_failure(repo):
    repo.write_page("Partnership returns are required (TMA 1970 s.122AA(2)).")
    assert audit.main(["--only", "citations", "--strict"]) == 1


def test_a_stale_page_is_still_checked_and_says_so(repo, monkeypatch):
    monkeypatch.setattr(compose, "load_manifest",
                        lambda: {SPEC["id"]: {"output": SPEC["output"],
                                              "generated_by": "fake:model",
                                              "note_count": 1,
                                              "input_hash": "stale"}})
    repo.write_page("Partnership returns are required (TMA 1970 s.122AA(2)).")
    found = warnings(["citations"])
    assert len(found) == 1
    assert "s.122AA" in found[0] and "stale" in found[0]


# --- the citation tokeniser ------------------------------------------------

@pytest.mark.parametrize("text,expected", [
    ("(TMA 1970 s.8(1))", "s.8"),
    ("TMA 1970 s. 12B", "s.12B"),
    ("Section 12B(5)", "s.12B"),
    ("sections 28A and", "s.28A"),
    ("TMA70/S12B(5)", "s.12B"),
    ("per s 59B of", "s.59B"),
])
def test_every_spelling_of_a_section_reads_as_one_provision(text, expected):
    assert expected in citations.tokens(text)


@pytest.mark.parametrize("text,expected", ([
    ("see SAM100050", "SAM100050"),
    ("CH61180 says", "CH61180"),
    ("EM7524", "EM7524"),
    ("SALF910", "SALF910"),
]))
def test_manual_references_are_recognised(text, expected):
    assert expected in citations.tokens(text)


@pytest.mark.parametrize("form", ["SA100", "SA400", "CWF1", "IHT400", "HS340"])
def test_a_form_number_is_not_a_citation(form):
    assert citations.tokens(f"complete form {form}") == set()


def test_a_note_spelling_a_section_differently_still_supports_the_page():
    assert citations.unsupported("(TMA 1970 s.12B(5))", "TMA70/S12B") == []


def test_subsections_do_not_have_to_match():
    assert citations.unsupported("s.9(2)", "TMA 1970 s.9(1)") == []


# --- the report the CLI writes ---------------------------------------------

def test_the_audit_writes_a_machine_readable_report(repo):
    audit.main([])
    payload = json.loads((repo.root / "last_audit.json").read_text())
    stage = payload["stages"][0]
    assert stage["stage"] == "audit"
    assert payload["ok"] is True
    assert set(stage["succeeded"]) == set(audit.CHECKS)


def test_warnings_reach_the_report_even_when_the_run_passes(repo):
    repo.write_page("Partnership returns are required (TMA 1970 s.122AA(2)).")
    audit.main([])
    payload = json.loads((repo.root / "last_audit.json").read_text())
    stage = payload["stages"][0]
    assert payload["ok"] is True
    assert any("s.122AA" in w["error"] for w in stage["warnings"])


def test_an_error_fails_the_run_and_names_the_check(repo):
    (repo.corpus_dir / DOC).unlink()
    assert audit.main([]) == 1
    payload = json.loads((repo.root / "last_audit.json").read_text())
    assert payload["ok"] is False
    assert {f["unit"] for f in payload["stages"][0]["failed"]} >= {"sources"}
