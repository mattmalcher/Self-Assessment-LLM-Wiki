"""Regression tests for the extract note schema (see `synth/schema.py`).

Covers the validator itself, the planner's treatment of a malformed cached
note, the validation-driven retry, and the committed contents of `extracts/`.
No model calls, no network. Run with `uv run pytest`.
"""
from __future__ import annotations

import copy
import json

import pytest

from self_assessment_wiki.synth import compose, extract, schema
from self_assessment_wiki.synth.chunk import Chunk
from self_assessment_wiki.synth.config import EXTRACTS_DIR
from self_assessment_wiki.synth.llm import Backend, LLMError

VALID = {
    "relevance": "core",
    "summary": "A person given notice under s.8 must deliver a return.",
    "topics": ["filing-obligations"],
    "obligations": [{"who": "A person given notice", "must": "deliver a return",
                     "trigger": "notice under s.8", "deadline": "31 January",
                     "ref": "TMA 1970 s.8(1)"}],
    "deadlines": [{"name": "Filing date", "rule": "31 January following the tax year",
                   "applies_to": "Online returns", "ref": "TMA 1970 s.8(1D)"}],
    "amounts": [{"name": "Initial penalty", "value": "£100", "period": "n/a",
                 "ref": "FA 2009 Sch 55 para 3"}],
    "penalties": [{"trigger": "return filed late", "consequence": "£100 penalty",
                   "ref": "FA 2009 Sch 55 para 3"}],
    "definitions": [{"term": "return", "meaning": "a Self Assessment return",
                     "ref": "TMA 1970 s.8"}],
    "cross_references": ["TMA 1970 s.9"],
    "caveats": ["Different dates apply to paper returns."],
}


def without(key: str) -> dict:
    note = copy.deepcopy(VALID)
    del note[key]
    return note


def with_note(**fields) -> dict:
    return copy.deepcopy(VALID) | fields


def test_valid_note_passes():
    assert schema.validate_note(VALID) == []


def test_empty_lists_are_valid():
    """"Empty lists are correct and expected" - prompts/extract.md."""
    note = with_note(**{k: [] for k in (*schema.STRING_LISTS, *schema.RECORD_LISTS)})
    assert schema.validate_note(note) == []


@pytest.mark.parametrize("key", schema.KEYS)
def test_every_documented_key_is_required(key):
    assert any("missing key" in e and key in e for e in schema.validate_note(without(key)))


def test_note_that_is_not_an_object_fails():
    assert schema.validate_note(["obligations"])
    assert schema.validate_note(None)


def test_invalid_relevance_fails():
    assert any("relevance" in e for e in schema.validate_note(with_note(relevance="maybe")))
    assert any("relevance" in e for e in schema.validate_note(with_note(relevance=None)))


def test_empty_summary_fails():
    assert schema.validate_note(with_note(summary="   "))
    assert schema.validate_note(with_note(summary=["a list"]))


def test_wrong_types_fail():
    assert schema.validate_note(with_note(topics="filing-obligations"))
    assert schema.validate_note(with_note(topics=[42]))
    assert schema.validate_note(with_note(obligations={"who": "someone"}))
    assert schema.validate_note(with_note(caveats=None))


def test_nested_record_must_be_an_object():
    assert schema.validate_note(with_note(penalties=["a late return costs £100"]))


def test_nested_record_missing_key_fails():
    """The `may`-for-`must` drift found in the committed extracts."""
    obligation = dict(VALID["obligations"][0])
    obligation["may"] = obligation.pop("must")
    errors = schema.validate_note(with_note(obligations=[obligation]))
    assert any("missing key 'must'" in e for e in errors)
    assert any("unexpected key 'may'" in e for e in errors)


def test_nested_record_wrong_value_type_fails():
    assert schema.validate_note(
        with_note(amounts=[dict(VALID["amounts"][0], value=100)]))


def test_empty_citation_fails():
    """A note whose `ref` is blank cannot be checked against its source."""
    for field in schema.RECORD_LISTS:
        record = dict(VALID[field][0], ref="  ")
        assert any(".ref" in e for e in schema.validate_note(with_note(**{field: [record]}))), field


def test_unexpected_top_level_key_fails():
    assert schema.validate_note(with_note(effective_from="2024-04-06"))


def test_the_shape_that_caused_the_data_loss_fails():
    """A bare nested obligation, cached as if it were a note (codex_review.md)."""
    assert not schema.is_valid({"who": "A person", "must": "file", "trigger": "notice",
                                "deadline": "31 January", "ref": "TMA 1970 s.8"})


def test_entry_is_valid_reads_the_note():
    assert schema.entry_is_valid({"index": 0, "heading": "s.8", "note": VALID})
    assert not schema.entry_is_valid({"index": 0, "heading": "s.8", "note": without("summary")})
    assert not schema.entry_is_valid({"index": 0, "heading": "s.8"})
    assert not schema.entry_is_valid("not an entry")


@pytest.mark.xfail(strict=True, reason="7 records predate the validator; "
                                       "re-extract them, then delete this marker")
def test_committed_extracts_all_validate():
    """Every note in `extracts/` passes the schema.

    This is the gate the three malformed records in `codex_review.md` failed,
    plus four quieter ones (`may` for `must`, `meaine` for `meaning`, a stray
    `meaning_ref`). They cannot be fixed by hand - a note is what the model
    said about a chunk - so they stay until `uv run extract` re-asks for those
    seven chunks. `uv run status` lists them.

    Marked strict, so it fails again the moment they are re-extracted: that is
    the reminder to drop the marker in the same commit.
    """
    bad = []
    for path in sorted(EXTRACTS_DIR.rglob("*.json")):
        data = json.loads(path.read_text())
        for chunk_hash, entry in data.get("chunks", {}).items():
            for error in schema.validate_note((entry or {}).get("note")):
                bad.append(f"{path.relative_to(EXTRACTS_DIR)} {chunk_hash}: {error}")
    assert not bad, "\n".join(bad[:20])


# --- planner ---------------------------------------------------------------

CHUNKS = [Chunk(doc="d.md", index=0, heading_path=["s.8"], text="x", hash="aaa111"),
          Chunk(doc="d.md", index=1, heading_path=["s.9"], text="y", hash="bbb222")]


def _plan_for(cached: dict, monkeypatch) -> extract.Plan:
    """`extract.plan()` over one synthetic document with `cached` already stored."""
    monkeypatch.setattr(extract, "corpus_docs", lambda only: [extract.CORPUS_DIR / "d.md"])
    monkeypatch.setattr(extract, "chunk_file", lambda path, root: ({}, CHUNKS))
    monkeypatch.setattr(extract.store, "load",
                        lambda doc: {"doc": doc, "chunks": copy.deepcopy(cached)})
    return extract.plan()[0]


def cached_entry(note: dict, prompt_hash: str | None = None) -> dict:
    return {"index": 0, "heading": "s.8", "chars": 1,
            "prompt_hash": extract.PROMPT_HASH if prompt_hash is None else prompt_hash,
            "model": "claude-cli:haiku", "note": note}


def test_a_valid_cached_note_is_not_work(monkeypatch):
    plan = _plan_for({"aaa111": cached_entry(VALID)}, monkeypatch)
    assert [c.hash for c in plan.todo] == ["bbb222"]
    assert plan.invalid == []


def test_a_malformed_cached_note_is_reported_as_work(monkeypatch):
    """The planner counted these as cached, so they were never retried."""
    plan = _plan_for({"aaa111": cached_entry(without("relevance"))}, monkeypatch)
    assert [c.hash for c in plan.invalid] == ["aaa111"]
    assert [c.hash for c in plan.todo] == ["aaa111", "bbb222"]


def test_a_malformed_note_is_not_also_counted_as_stale_prompt(monkeypatch):
    """Invalid outranks old-prompt: it is one re-extraction, not two."""
    plan = _plan_for({"aaa111": cached_entry(without("relevance"), prompt_hash="old")},
                     monkeypatch)
    assert [c.hash for c in plan.invalid] == ["aaa111"]
    assert plan.stale_prompt == []


def test_compose_does_not_select_an_invalid_note():
    spec = {"id": "p", "title": "P", "output": "docs/p.md",
            "select": {"relevance": ["core"]}}
    extracts = {"d.md": {"doc": "d.md", "chunks": {
        "aaa111": cached_entry(VALID),
        "bbb222": cached_entry(without("summary")),
    }}}
    assert [s.chunk_hash for s in compose.select(spec, extracts)] == ["aaa111"]


# --- extraction retry ------------------------------------------------------

class ScriptedBackend(Backend):
    """Returns each canned response in turn, recording the prompts it saw."""
    name = "scripted"

    def __init__(self, responses: list[str]):
        super().__init__("scripted-model")
        self.responses = list(responses)
        self.prompts: list[str] = []

    def complete(self, system: str, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.responses.pop(0)


def test_a_valid_first_answer_costs_one_call():
    backend = ScriptedBackend([json.dumps(VALID)])
    assert extract.extract_note(backend, CHUNKS[0], {}) == VALID
    assert len(backend.prompts) == 1


def test_an_invalid_answer_is_re_asked_with_the_errors():
    backend = ScriptedBackend([json.dumps(without("relevance")), json.dumps(VALID)])
    assert extract.extract_note(backend, CHUNKS[0], {}) == VALID
    assert "missing key 'relevance'" in backend.prompts[1]


def test_an_unparseable_answer_is_re_asked():
    backend = ScriptedBackend(["I'm afraid I can't do that.", json.dumps(VALID)])
    assert extract.extract_note(backend, CHUNKS[0], {}) == VALID
    assert len(backend.prompts) == 2


def test_a_note_that_never_validates_raises_rather_than_being_cached():
    backend = ScriptedBackend([json.dumps(without("summary"))] * extract.VALIDATION_ATTEMPTS)
    with pytest.raises(LLMError, match="invalid note"):
        extract.extract_note(backend, CHUNKS[0], {})
    assert len(backend.prompts) == extract.VALIDATION_ATTEMPTS
