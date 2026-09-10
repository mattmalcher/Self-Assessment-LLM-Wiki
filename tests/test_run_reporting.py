"""Regression tests for partial-run visibility (see `self_assessment_wiki.runlog`).

A run that finished some of its work and failed the rest must exit non-zero
and leave a machine-readable report behind. Best effort is available, but only
when it is asked for. No model calls, no network. Run with `uv run pytest`.
"""
from __future__ import annotations

import json

import pytest

from self_assessment_wiki import runlog
from self_assessment_wiki.pipeline import fetch
from self_assessment_wiki.synth import build, compose, extract
from self_assessment_wiki.synth.chunk import Chunk
from self_assessment_wiki.synth.llm import Backend, LLMError

NOTE = {"relevance": "core", "summary": "A person must deliver a return.",
        "topics": [], "obligations": [], "deadlines": [], "amounts": [],
        "penalties": [], "definitions": [], "cross_references": [], "caveats": []}

SOURCES = [
    {"id": "good-source", "type": "web_page", "status": "fetch", "output": "corpus/good.md"},
    {"id": "bad-source", "type": "web_page", "status": "fetch", "output": "corpus/bad.md"},
    {"id": "not-fetched", "type": "web_page", "status": "manual", "output": "corpus/skip.md"},
]


class FakeBackend(Backend):
    """A backend that answers for some units and raises for the rest."""

    def __init__(self, fail_on=(), answer=None):
        self.name, self.model = "fake", "fake-model"
        self.fail_on = set(fail_on)
        self.answer = answer or json.dumps(NOTE)

    def call(self, system: str, prompt: str) -> str:
        for marker in self.fail_on:
            if marker in prompt:
                raise LLMError(f"model refused {marker}")
        return self.answer


# --- stage 1: fetch --------------------------------------------------------

@pytest.fixture
def fetch_env(monkeypatch, tmp_path):
    """`fetch.main` against a fake registry, writing its reports to tmp_path."""
    monkeypatch.chdir(tmp_path)  # sources write their output relative to cwd
    monkeypatch.setattr(fetch, "PIPELINE_DIR", tmp_path)
    monkeypatch.setattr(fetch, "load_sources", lambda: SOURCES)
    monkeypatch.setattr(fetch.manifest_store, "load", lambda: {})
    monkeypatch.setattr(fetch.manifest_store, "save", lambda manifest: None)
    monkeypatch.setattr(fetch.render_sources_index, "main", lambda: 0)

    def fetcher(source, entry):
        if source["id"] == "bad-source":
            raise RuntimeError("upstream returned 503")
        output = tmp_path / source["output"]
        output.parent.mkdir(parents=True, exist_ok=True)
        sid = source["id"]
        output.write_text(f"<!-- section:{sid} -->\n# {sid}\n<!-- /section:{sid} -->\n")
        return True

    monkeypatch.setitem(fetch._DISPATCH, "web_page", fetcher)
    return tmp_path


def run_fetch(argv: list[str], monkeypatch) -> int:
    monkeypatch.setattr("sys.argv", ["fetch", *argv])
    return fetch.main()


def test_one_failed_source_fails_the_run(fetch_env, monkeypatch):
    assert run_fetch([], monkeypatch) == 1


def test_keep_going_is_the_only_way_to_pass_with_a_failure(fetch_env, monkeypatch):
    assert run_fetch(["--keep-going"], monkeypatch) == 0


def test_a_wholly_successful_fetch_passes(fetch_env, monkeypatch):
    assert run_fetch(["--only", "good-source"], monkeypatch) == 0


def test_fetch_writes_a_machine_readable_report(fetch_env, monkeypatch):
    run_fetch(["--keep-going"], monkeypatch)
    report = json.loads((fetch_env / "last_run.json").read_text())
    assert report["ok"] is False
    stage = report["stages"][0]
    assert stage["stage"] == "fetch"
    assert stage["succeeded"] == ["good-source"]
    assert stage["changed"] == ["good-source"]
    assert stage["failed"] == [{"unit": "bad-source", "error": "upstream returned 503"}]
    assert stage["attempted"] == 2  # `not-fetched` is not due, so not attempted


def test_partial_refresh_is_flagged_at_the_top_of_the_pr_body(fetch_env, monkeypatch):
    run_fetch(["--keep-going"], monkeypatch)
    summary = (fetch_env / "last_run_summary.md").read_text()
    assert summary.startswith("> [!WARNING]")
    assert "Partial refresh: 1 of 2 source(s) failed" in summary
    assert "- `bad-source`: upstream returned 503" in summary


def test_a_complete_refresh_carries_no_warning(fetch_env, monkeypatch):
    run_fetch(["--only", "good-source"], monkeypatch)
    assert "WARNING" not in (fetch_env / "last_run_summary.md").read_text()


def test_dry_run_reports_everything_as_not_attempted(fetch_env, monkeypatch):
    assert run_fetch(["--dry-run"], monkeypatch) == 0
    stage = json.loads((fetch_env / "last_run.json").read_text())["stages"][0]
    assert stage["attempted"] == 0
    assert stage["remaining"] == ["good-source", "bad-source"]


# --- stage 2: extract ------------------------------------------------------

def chunk(index: int, text: str) -> Chunk:
    return Chunk(doc="legislation/tma-1970.md", index=index,
                 heading_path=[f"s.{index}"], text=text, hash=f"hash{index}")


@pytest.fixture
def extract_env(monkeypatch, tmp_path):
    """Two chunks of one document, with the extract cache redirected to tmp."""
    chunks = [chunk(0, "chunk zero body"), chunk(1, "chunk one body")]
    plan = extract.Plan(doc="legislation/tma-1970.md", meta={"source_id": "tma-1970"},
                        chunks=chunks, todo=list(chunks), orphans=0)
    monkeypatch.setattr(extract, "plan", lambda only=None: [plan])
    monkeypatch.setattr(extract.store, "load", lambda doc: {"chunks": {}})
    monkeypatch.setattr(extract.store, "prune_orphans", lambda doc, data, keep: 0)
    monkeypatch.setattr(extract.store, "save", lambda doc, data: None)
    return plan


def test_a_failed_chunk_is_reported_as_a_failed_unit(extract_env):
    report = extract.run(FakeBackend(fail_on=["chunk one body"]), concurrency=1, verbose=False)
    assert report.succeeded == ["legislation/tma-1970.md#0"]
    assert [f["unit"] for f in report.failed] == ["legislation/tma-1970.md#1"]
    assert report.ok is False
    assert report.exit_code() == 1
    assert report.exit_code(keep_going=True) == 0


def test_a_complete_extract_is_ok(extract_env):
    report = extract.run(FakeBackend(), concurrency=1, verbose=False)
    assert report.ok and len(report.succeeded) == 2


def test_limit_leaves_remaining_work_without_failing(extract_env):
    """Stopping early was asked for; it is outstanding work, not a failure."""
    report = extract.run(FakeBackend(), limit=1, concurrency=1, verbose=False)
    assert report.ok and report.exit_code() == 0
    assert report.remaining == ["legislation/tma-1970.md#1"]


# --- stage 3: compose ------------------------------------------------------

SPECS = [
    {"id": "filing-deadlines", "title": "Filing deadlines", "output": "docs/filing.md",
     "brief": "Explain the deadlines.", "select": {"relevance": ["core"]}},
    {"id": "penalties", "title": "Penalties", "output": "docs/penalties.md",
     "brief": "Explain the penalties.", "select": {"relevance": ["core"]}},
]


@pytest.fixture
def compose_env(monkeypatch, tmp_path):
    """Two stale pages with notes, written under tmp_path."""
    notes = [compose.Selected(doc="legislation/tma-1970.md", chunk_hash="aaa111",
                              heading="s.8", note=dict(NOTE), source_id="tma-1970")]
    works = [compose.PageWork(spec=spec, notes=notes, input_hash="h", stale=True,
                              reason="inputs changed") for spec in SPECS]
    monkeypatch.setattr(compose, "plan", lambda model, only=None, force=False: works)
    monkeypatch.setattr(compose, "load_manifest", lambda: {})
    monkeypatch.setattr(compose, "save_manifest", lambda manifest: None)
    monkeypatch.setattr(compose, "REPO_ROOT", tmp_path)
    return works


def test_a_failed_page_is_reported_as_a_failed_unit(compose_env):
    report = compose.run(FakeBackend(fail_on=["Explain the penalties"], answer="# Filing\n\nBody."),
                         "fake-model", verbose=False)
    assert report.succeeded == ["filing-deadlines"]
    assert [f["unit"] for f in report.failed] == ["penalties"]
    assert report.exit_code() == 1


def test_a_page_with_no_notes_is_a_failure(compose_env):
    compose_env[1].notes = []
    report = compose.run(FakeBackend(answer="# Filing\n\nBody."), "fake-model", verbose=False)
    assert [f["unit"] for f in report.failed] == ["penalties"]
    assert "selector" in report.failed[0]["error"]


def test_a_complete_compose_is_ok(compose_env):
    report = compose.run(FakeBackend(answer="# Filing\n\nBody."), "fake-model", verbose=False)
    assert report.ok and report.exit_code() == 0


# --- the synth CLI ---------------------------------------------------------

@pytest.fixture
def synth_env(monkeypatch, tmp_path):
    monkeypatch.setattr(build, "RUN_REPORT_PATH", tmp_path / "last_run.json")
    monkeypatch.setattr(build, "get_backend", lambda *a, **k: FakeBackend())
    return tmp_path / "last_run.json"


def failing(stage: str):
    def run(*args, **kwargs):
        report = runlog.StageReport(stage=stage, unit="chunk")
        report.succeed("one")
        report.fail("two", "model refused")
        return report
    return run


def test_extract_command_exits_non_zero_on_a_failed_chunk(synth_env, monkeypatch):
    monkeypatch.setattr(extract, "run", failing("extract"))
    assert build.main([], command="extract") == 1
    assert build.main(["--keep-going"], command="extract") == 0


def test_compose_command_exits_non_zero_on_a_failed_page(synth_env, monkeypatch):
    monkeypatch.setattr(compose, "run", failing("compose"))
    assert build.main([], command="compose") == 1


def test_all_stops_before_composing_on_a_failed_extract(synth_env, monkeypatch):
    monkeypatch.setattr(extract, "run", failing("extract"))
    monkeypatch.setattr(compose, "run", lambda *a, **k: pytest.fail("composed anyway"))
    assert build.main([], command="all") == 1
    assert [s["stage"] for s in json.loads(synth_env.read_text())["stages"]] == ["extract"]


def test_all_records_both_stages_when_asked_to_keep_going(synth_env, monkeypatch):
    monkeypatch.setattr(extract, "run", failing("extract"))
    monkeypatch.setattr(compose, "run", failing("compose"))
    assert build.main(["--keep-going"], command="all") == 0
    report = json.loads(synth_env.read_text())
    assert [s["stage"] for s in report["stages"]] == ["extract", "compose"]
    assert report["ok"] is False


def test_the_report_names_every_failed_unit(synth_env, monkeypatch):
    monkeypatch.setattr(compose, "run", failing("compose"))
    build.main(["--keep-going"], command="compose")
    stage = json.loads(synth_env.read_text())["stages"][0]
    assert stage["failed"] == [{"unit": "two", "error": "model refused"}]
    assert stage["succeeded"] == ["one"]
    assert stage["attempted"] == 2
