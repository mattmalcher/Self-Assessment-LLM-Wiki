"""Regression tests for note selection and cache propagation.

Selection (`synth.compose.select`) is the whole reason a page's staleness can
be decided without a model call, so it has to be deterministic and it has to
mean what `pages.yml` says: path prefixes, relevance tiers, `match` regexes
and a note cap. A selector that quietly matches nothing composes a page from
no evidence; one that matches everything makes every page stale on every
refresh.

The second half follows one corpus edit all the way through - re-chunk, cache
hit/miss, orphan prune, page staleness - because that propagation is the
promise the whole three-stage design rests on and no single unit test sees
it. No model calls, no network. Run with `uv run pytest`.
"""
from __future__ import annotations

import pytest

from self_assessment_wiki.synth import compose, extract, store
from self_assessment_wiki.synth.chunk import chunk_file

FRONT = """---
source_url: https://www.legislation.gov.uk/ukpga/1970/9/contents
source_id: tma-1970
---

"""


def note(summary: str = "A person must deliver a return.", *,
         relevance: str = "core", topics: tuple[str, ...] = (),
         obligations: tuple[dict, ...] = ()) -> dict:
    return {"relevance": relevance, "summary": summary, "topics": list(topics),
            "obligations": [dict(o) for o in obligations], "deadlines": [],
            "amounts": [], "penalties": [], "definitions": [],
            "cross_references": [], "caveats": []}


def extracts(*docs: tuple[str, dict[str, dict]]) -> dict[str, dict]:
    """`{doc: {"chunks": {hash: {"note": ...}}}}`, as `store.load_all` returns."""
    return {doc: {"doc": doc, "source_id": doc.split("/")[-1].removesuffix(".md"),
                  "chunks": {h: {"index": i, "heading": h, "note": n}
                             for i, (h, n) in enumerate(chunks.items())}}
            for doc, chunks in docs}


def spec(**select) -> dict:
    return {"id": "page", "title": "Page", "section": "S",
            "output": "docs/lifecycle/page.md", "brief": "A brief.",
            "select": select}


# --- what the selector picks ----------------------------------------------

def test_a_selector_with_no_filters_takes_every_core_note():
    data = extracts(("acts/tma-1970.md", {"h1": note(), "h2": note()}))
    assert len(compose.select(spec(), data)) == 2


def test_only_the_named_relevance_tiers_are_selected():
    data = extracts(("acts/tma-1970.md", {
        "h1": note(relevance="core"), "h2": note(relevance="related"),
        "h3": note(relevance="none")}))
    assert len(compose.select(spec(relevance=["core"]), data)) == 1
    assert len(compose.select(spec(relevance=["core", "related"]), data)) == 2


def test_doc_prefixes_restrict_the_selection_to_a_subtree():
    data = extracts(("acts/tma-1970.md", {"h1": note()}),
                    ("manuals/sam.md", {"h2": note()}))
    picked = compose.select(spec(docs=["acts"]), data)
    assert [s.doc for s in picked] == ["acts/tma-1970.md"]


def test_a_prefix_matches_on_path_segments_not_on_characters():
    """`acts` must not select `acts-repealed/`."""
    data = extracts(("acts/tma-1970.md", {"h1": note()}),
                    ("acts-repealed/old.md", {"h2": note()}))
    picked = compose.select(spec(docs=["acts"]), data)
    assert [s.doc for s in picked] == ["acts/tma-1970.md"]


def test_an_exact_document_path_is_a_valid_prefix():
    data = extracts(("acts/tma-1970.md", {"h1": note()}),
                    ("acts/itepa-2003.md", {"h2": note()}))
    picked = compose.select(spec(docs=["acts/tma-1970.md"]), data)
    assert [s.doc for s in picked] == ["acts/tma-1970.md"]


def test_match_regexes_filter_and_a_non_matching_note_is_dropped():
    data = extracts(("acts/tma-1970.md", {
        "h1": note("Penalties for a late return."),
        "h2": note("Rates of income tax.")}))
    picked = compose.select(spec(match=["penalt"]), data)
    assert len(picked) == 1
    assert "Penalties" in picked[0].note["summary"]


def test_matching_is_case_insensitive():
    data = extracts(("acts/tma-1970.md", {"h1": note("PENALTIES apply.")}))
    assert compose.select(spec(match=["penalties"]), data)


def test_a_regex_may_match_the_heading_the_topics_or_a_citation():
    data = extracts(("acts/tma-1970.md", {
        "s.8 Personal return": note("Unrelated prose."),
        "h2": note("Unrelated prose.", topics=("payments on account",)),
        "h3": note("Unrelated prose.",
                   obligations=({"who": "a", "must": "b", "trigger": "c",
                                 "deadline": "d", "ref": "TMA 1970 s.59A"},)),
    }))
    assert len(compose.select(spec(match=["s.8"]), data)) == 1
    assert len(compose.select(spec(match=["payments on account"]), data)) == 1
    assert len(compose.select(spec(match=["s.59A"]), data)) == 1


def test_notes_matching_more_patterns_sort_first():
    data = extracts(("acts/tma-1970.md", {
        "h1": note("Penalties only."),
        "h2": note("Penalties and appeals.")}))
    picked = compose.select(spec(match=["penalt", "appeal"]), data)
    assert picked[0].note["summary"] == "Penalties and appeals."


def test_max_notes_caps_the_selection():
    data = extracts(("acts/tma-1970.md", {f"h{i}": note() for i in range(10)}))
    assert len(compose.select(spec(max_notes=4), data)) == 4


def test_selection_is_deterministic():
    data = extracts(("acts/tma-1970.md", {f"h{i}": note() for i in range(10)}))
    first = compose.select(spec(max_notes=4), data)
    second = compose.select(spec(max_notes=4), data)
    assert [s.chunk_hash for s in first] == [s.chunk_hash for s in second]


def test_a_malformed_note_is_never_selected():
    """A note that fails the schema is not evidence - see `synth/schema.py`."""
    data = extracts(("acts/tma-1970.md", {"h1": {"obligations": "not a list"}}))
    assert compose.select(spec(), data) == []


def test_the_selection_carries_the_provenance_a_page_cites():
    data = extracts(("acts/tma-1970.md", {"h1": note()}))
    data["acts/tma-1970.md"]["source_url"] = "https://example.org/tma"
    picked = compose.select(spec(), data)[0]
    assert picked.source_id == "tma-1970"
    assert picked.source_url == "https://example.org/tma"


# --- one corpus edit, followed through the caches --------------------------

@pytest.fixture
def pipeline(monkeypatch, tmp_path):
    """A corpus of one document and an extract cache that covers it."""
    corpus = tmp_path / "corpus"
    extracts_dir = tmp_path / "extracts"
    corpus.mkdir()
    extracts_dir.mkdir()
    monkeypatch.setattr(extract, "CORPUS_DIR", corpus)
    monkeypatch.setattr(store, "EXTRACTS_DIR", extracts_dir)

    # Sections sized so the default 12,000-character target puts each one in
    # its own chunk; the point of the fixture is one chunk per section.
    body = "".join(f"## {i} Section {i}\n\n" + ("text " * 1400) + "\n\n"
                   for i in range(1, 4))
    path = corpus / "tma-1970.md"
    path.write_text(FRONT + body)

    _, chunks = chunk_file(path, corpus)
    data = {"doc": "tma-1970.md", "source_id": "tma-1970",
            "chunks": {c.hash: {"index": c.index, "heading": c.heading,
                                "prompt_hash": extract.PROMPT_HASH,
                                "model": "fake:model", "note": note()}
                       for c in chunks}}
    store.save("tma-1970.md", data)

    class Pipeline:
        root = tmp_path
        corpus_dir = corpus
        doc_path = path
        original = FRONT + body
        hashes = [c.hash for c in chunks]

        @staticmethod
        def amend(old: str, new: str) -> None:
            path.write_text(path.read_text().replace(old, new))

    return Pipeline


def test_a_fully_extracted_document_is_no_work(pipeline):
    [plan] = extract.plan()
    assert plan.todo == [] and plan.orphans == 0 and plan.invalid == []


def test_amending_one_section_queues_only_that_chunk(pipeline):
    pipeline.amend("## 2 Section 2", "## 2 Section 2 (amended)")
    [plan] = extract.plan()
    assert len(plan.todo) == 1
    assert plan.todo[0].index == 1
    assert plan.orphans == 1  # the pre-amendment chunk


def test_the_superseded_cache_entry_is_pruned(pipeline):
    pipeline.amend("## 2 Section 2", "## 2 Section 2 (amended)")
    [plan] = extract.plan()
    data = store.load(plan.doc)
    pruned = store.prune_orphans(plan.doc, data, {c.hash for c in plan.chunks})
    assert pruned == 1
    assert len(data["chunks"]) == 2


def test_an_unrelated_amendment_does_not_disturb_the_other_chunks(pipeline):
    pipeline.amend("## 2 Section 2", "## 2 Section 2 (amended)")
    [plan] = extract.plan()
    cached = set(store.load(plan.doc)["chunks"])
    untouched = [c.hash for c in plan.chunks if c.hash in cached]
    assert len(untouched) == 2


def test_the_cache_survives_a_round_trip_to_disk(pipeline):
    before = store.load("tma-1970.md")
    store.save("tma-1970.md", before)
    assert store.load("tma-1970.md") == before


def test_an_amendment_reaches_the_pages_that_selected_the_note(pipeline):
    """The point of the whole chain: a moved chunk moves a page's input hash,
    and only for the pages whose selector actually picks that note up."""
    data = store.load("tma-1970.md")
    loaded = {"tma-1970.md": data}
    covers_it = spec(match=["Section 2"])
    ignores_it = spec(match=["nothing here"])

    # The heading is part of what the selector reads and what the page cites.
    before_covered = compose.input_hash(
        covers_it, compose.select(covers_it, loaded), "model")
    before_ignored = compose.input_hash(
        ignores_it, compose.select(ignores_it, loaded), "model")

    chunk_hash = next(h for h, e in data["chunks"].items()
                      if "Section 2" in e["heading"])
    data["chunks"][chunk_hash]["note"] = note("A different rule entirely.")

    assert compose.input_hash(covers_it, compose.select(covers_it, loaded),
                              "model") != before_covered
    assert compose.input_hash(ignores_it, compose.select(ignores_it, loaded),
                              "model") == before_ignored
