"""Regression tests for the compose staleness contract (see `compose.input_hash`).

Pure functions over in-memory extract data: no model calls, no disk, no
network. Run with `uv run pytest`.
"""
from __future__ import annotations

import copy

from self_assessment_wiki.synth import compose


def note(**fields) -> dict:
    """A schema-valid note (see `synth/schema.py`) with these fields set.

    `compose.select` drops notes that fail the schema, so a fixture note has to
    carry every documented key even when the test only cares about one of them.
    """
    base = {"relevance": "core", "summary": "A note.", "topics": [],
            "obligations": [], "deadlines": [], "amounts": [], "penalties": [],
            "definitions": [], "cross_references": [], "caveats": []}
    return base | fields


SPEC = {
    "id": "payments-on-account",
    "title": "Payments on account",
    "output": "docs/payments-on-account.md",
    "brief": "Explain payments on account.",
    "select": {"docs": ["legislation"], "relevance": ["core"]},
}

# Two documents, one selected note each. `other.md` sits outside the page's
# `select.docs` prefix, so it must never affect this page.
EXTRACTS = {
    "legislation/tma-1970.md": {
        "doc": "legislation/tma-1970.md",
        "source_id": "tma-1970",
        "source_url": "https://www.legislation.gov.uk/ukpga/1970/9",
        "chunks": {
            "aaa111": {
                "index": 0,
                "heading": "s.59A Payments on account",
                "prompt_hash": "prompt-v1",
                "model": "claude-cli:sonnet",
                "note": note(
                    summary="Payments on account are due in two instalments.",
                    topics=["payments on account"],
                    deadlines=[{"name": "Second instalment", "rule": "31 January",
                                "applies_to": "Taxpayers within SA", "ref": "s.59A"}],
                ),
            }
        },
    },
    "other/unrelated.md": {
        "doc": "other/unrelated.md",
        "source_id": "unrelated",
        "source_url": "https://example.invalid/unrelated",
        "chunks": {
            "bbb222": {
                "index": 0,
                "heading": "Something else entirely",
                "prompt_hash": "prompt-v1",
                "model": "claude-cli:sonnet",
                "note": note(summary="Not about tax returns."),
            }
        },
    },
}

MODEL = "opus"


def hash_of(extracts: dict) -> str:
    return compose.input_hash(SPEC, compose.select(SPEC, extracts), MODEL)


def mutate(path: tuple[str, ...], value) -> dict:
    """A deep copy of EXTRACTS with one nested key replaced."""
    extracts = copy.deepcopy(EXTRACTS)
    target = extracts
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    return extracts


def test_baseline_is_deterministic():
    assert hash_of(copy.deepcopy(EXTRACTS)) == hash_of(copy.deepcopy(EXTRACTS))


def test_selected_note_content_change_invalidates():
    """A corrected note under an unchanged chunk hash must make the page stale."""
    changed = mutate(
        ("legislation/tma-1970.md", "chunks", "aaa111", "note", "summary"),
        "Payments on account are due in two instalments, 31 Jan and 31 Jul.",
    )
    assert hash_of(changed) != hash_of(EXTRACTS)


def test_nested_note_change_invalidates():
    changed = copy.deepcopy(EXTRACTS)
    (changed["legislation/tma-1970.md"]["chunks"]["aaa111"]["note"]
     ["deadlines"][0]["rule"]) = "31 July"
    assert hash_of(changed) != hash_of(EXTRACTS)


def test_extraction_prompt_version_change_invalidates():
    changed = mutate(
        ("legislation/tma-1970.md", "chunks", "aaa111", "prompt_hash"), "prompt-v2"
    )
    assert hash_of(changed) != hash_of(EXTRACTS)


def test_extraction_model_change_invalidates():
    changed = mutate(
        ("legislation/tma-1970.md", "chunks", "aaa111", "model"), "claude-cli:opus"
    )
    assert hash_of(changed) != hash_of(EXTRACTS)


def test_unrelated_note_does_not_invalidate():
    """A note the selector never picks has no effect on the page."""
    changed = mutate(
        ("other/unrelated.md", "chunks", "bbb222", "note"),
        note(summary="Rewritten completely.", topics=["x"]),
    )
    assert compose.select(SPEC, changed) == compose.select(SPEC, EXTRACTS)
    assert hash_of(changed) == hash_of(EXTRACTS)


def test_dropping_a_selected_note_invalidates():
    changed = copy.deepcopy(EXTRACTS)
    changed["legislation/tma-1970.md"]["chunks"] = {}
    assert hash_of(changed) != hash_of(EXTRACTS)


def test_compose_model_change_invalidates():
    notes = compose.select(SPEC, EXTRACTS)
    assert compose.input_hash(SPEC, notes, "opus") != compose.input_hash(SPEC, notes, "sonnet")


def test_nav_only_spec_keys_do_not_invalidate():
    notes = compose.select(SPEC, EXTRACTS)
    renav = dict(SPEC, section="Filing")
    assert compose.input_hash(renav, notes, MODEL) == compose.input_hash(SPEC, notes, MODEL)


def test_note_ordering_does_not_affect_the_hash():
    """Fingerprints are combined in a fixed order, whatever order they arrive in."""
    notes = compose.select(SPEC, EXTRACTS)
    extra = compose.Selected(
        doc="legislation/tma-1970.md", chunk_hash="ccc333", heading="s.7 Notice of liability",
        note=note(summary="Duty to notify chargeability."),
        source_id="tma-1970", prompt_hash="prompt-v1", model="claude-cli:sonnet",
    )
    forward = compose.input_hash(SPEC, notes + [extra], MODEL)
    backward = compose.input_hash(SPEC, [extra] + notes, MODEL)
    assert forward == backward
