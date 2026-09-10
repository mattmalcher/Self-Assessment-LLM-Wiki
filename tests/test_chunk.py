"""Regression tests for corpus chunking (see `synth.chunk`).

Chunking is the extract cache's key, so its properties are economic as much
as structural: a chunk hash must stay stable when an unrelated part of the
same Act is amended (or a refresh re-extracts hundreds of chunks nobody
touched), it must move when the text a chunk actually contains changes, and
no text may be dropped on the way through. These tests pin all three, plus
the cleaning rules that decide what the model is charged to read.

No model calls, no network. Run with `uv run pytest`.
"""
from __future__ import annotations

import pytest

from self_assessment_wiki.synth import chunk as chunk_mod
from self_assessment_wiki.synth.chunk import Chunk, chunk_file, split_front_matter

FRONT_MATTER = """---
source_url: https://www.legislation.gov.uk/ukpga/1970/9/contents
source_id: tma-1970
---

"""


def write(tmp_path, body: str, *, name: str = "tma-1970.md", front: bool = True):
    corpus = tmp_path / "corpus"
    path = corpus / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text((FRONT_MATTER if front else "") + body)
    return path, corpus


def section(number: int, *, filler: str = "text", chars: int = 600) -> str:
    body = (filler + " ") * (chars // (len(filler) + 1))
    return f"## {number} Section {number}\n\n{body}\n\n"


# --- front matter ----------------------------------------------------------

def test_front_matter_is_parsed_and_removed():
    meta, body = split_front_matter("---\nsource_id: tma-1970\n---\n\n# Act\n")
    assert meta == {"source_id": "tma-1970"}
    assert body == "\n# Act\n"


def test_a_document_without_front_matter_is_left_alone():
    meta, body = split_front_matter("# Act\n")
    assert meta == {}
    assert body == "# Act\n"


def test_unparseable_front_matter_is_not_fatal():
    meta, _ = split_front_matter("---\n: : :\n---\n\nbody\n")
    assert meta == {}


def test_chunk_file_returns_the_documents_provenance(tmp_path):
    path, corpus = write(tmp_path, section(1))
    meta, _ = chunk_file(path, corpus)
    assert meta["source_id"] == "tma-1970"


# --- boundaries ------------------------------------------------------------

def test_chunks_follow_headings_rather_than_a_character_window(tmp_path):
    path, corpus = write(tmp_path, "".join(section(i) for i in range(1, 6)))
    _, chunks = chunk_file(path, corpus, target_chars=700)
    assert len(chunks) == 5
    for i, c in enumerate(chunks, 1):
        assert c.text.startswith(f"## {i} Section {i}")


def test_small_sections_share_a_chunk_up_to_the_target(tmp_path):
    path, corpus = write(tmp_path, "".join(section(i) for i in range(1, 5)))
    _, chunks = chunk_file(path, corpus, target_chars=1400)
    assert len(chunks) == 2


def test_the_heading_path_records_where_a_chunk_sits(tmp_path):
    path, corpus = write(tmp_path, "# Part I\n\n" + section(1))
    _, chunks = chunk_file(path, corpus)
    assert chunks[0].heading_path[:1] == ["Part I"]
    assert "Part I" in chunks[0].heading


def test_a_section_longer_than_the_target_is_split_on_paragraphs(tmp_path):
    paragraphs = "\n\n".join(f"Paragraph {i} " + "word " * 60 for i in range(20))
    path, corpus = write(tmp_path, f"## 1 Long section\n\n{paragraphs}\n")
    _, chunks = chunk_file(path, corpus, target_chars=800)
    assert len(chunks) > 1
    assert all(c.heading_path == ["1 Long section"] for c in chunks)


def test_no_text_is_dropped_by_chunking(tmp_path):
    body = "".join(section(i) for i in range(1, 8))
    path, corpus = write(tmp_path, body)
    _, chunks = chunk_file(path, corpus, target_chars=700)
    rejoined = " ".join("".join(c.text.split()) for c in chunks)
    assert "".join(body.split()) in rejoined.replace(" ", "")


def test_indices_are_contiguous_from_zero(tmp_path):
    path, corpus = write(tmp_path, "".join(section(i) for i in range(1, 6)))
    _, chunks = chunk_file(path, corpus, target_chars=700)
    assert [c.index for c in chunks] == list(range(len(chunks)))


def test_the_doc_path_is_corpus_relative(tmp_path):
    path, corpus = write(tmp_path, section(1), name="acts/tma-1970.md")
    _, chunks = chunk_file(path, corpus)
    assert chunks[0].doc == "acts/tma-1970.md"


# --- runts -----------------------------------------------------------------

def test_a_tiny_trailing_section_is_merged_backwards(tmp_path):
    path, corpus = write(tmp_path, section(1) + "## 2 Stub\n\nShort.\n")
    _, chunks = chunk_file(path, corpus, target_chars=700)
    assert len(chunks) == 1
    assert "2 Stub" in chunks[0].text


def test_a_tiny_leading_section_is_folded_forwards(tmp_path):
    path, corpus = write(tmp_path, "## 0 Stub\n\nShort.\n\n" + section(1))
    _, chunks = chunk_file(path, corpus, target_chars=700)
    assert len(chunks) == 1
    assert chunks[0].text.startswith("## 0 Stub")


def test_a_lone_short_document_is_still_one_chunk(tmp_path):
    path, corpus = write(tmp_path, "## 1 Stub\n\nShort.\n")
    _, chunks = chunk_file(path, corpus)
    assert len(chunks) == 1


# --- hashes: what the extract cache is keyed on ----------------------------

def test_the_same_text_hashes_the_same_way(tmp_path):
    path, corpus = write(tmp_path, "".join(section(i) for i in range(1, 4)))
    _, first = chunk_file(path, corpus, target_chars=700)
    _, second = chunk_file(path, corpus, target_chars=700)
    assert [c.hash for c in first] == [c.hash for c in second]


def test_amending_one_section_leaves_the_other_hashes_alone(tmp_path):
    body = "".join(section(i) for i in range(1, 6))
    path, corpus = write(tmp_path, body)
    _, before = chunk_file(path, corpus, target_chars=700)

    path.write_text(FRONT_MATTER + body.replace("## 3 Section 3", "## 3 Section 3 (amended)"))
    _, after = chunk_file(path, corpus, target_chars=700)

    changed = [i for i, (a, b) in enumerate(zip(before, after)) if a.hash != b.hash]
    assert changed == [2]


def test_changing_a_chunks_own_text_moves_its_hash(tmp_path):
    path, corpus = write(tmp_path, section(1))
    _, before = chunk_file(path, corpus)
    path.write_text(FRONT_MATTER + section(1) .replace("text", "other"))
    _, after = chunk_file(path, corpus)
    assert before[0].hash != after[0].hash


def test_front_matter_is_not_part_of_the_hash(tmp_path):
    path, corpus = write(tmp_path, section(1))
    _, before = chunk_file(path, corpus)
    path.write_text(FRONT_MATTER.replace("tma-1970", "tma-1970-mirror") + section(1))
    _, after = chunk_file(path, corpus)
    assert before[0].hash == after[0].hash


def test_an_explicit_hash_is_kept():
    assert Chunk(doc="d.md", index=0, heading_path=[], text="x", hash="fixed").hash == "fixed"


# --- cleaning: what the model is charged to read ---------------------------

def test_link_hover_titles_are_stripped():
    assert chunk_mod._clean('See [s. 1](/id/ukpga/1970/9/section/1 "Go to S. 1").') == \
        "See [s. 1](/id/ukpga/1970/9/section/1)."


def test_commentary_anchors_collapse_to_their_key():
    cleaned = chunk_mod._clean("[F2](#commentary-key-8c03)2 General Commissioners")
    assert cleaned == "F2 2 General Commissioners"


def test_textual_amendments_are_dropped(tmp_path):
    body = ("## 1 Section 1\n\nThe rule.\n\n"
            "Textual Amendments\n\n"
            "[F1](#reference-key-8c03 \"Go back to reference\") "
            "S. 1 substituted (18.4.2005) by Finance Act 2005\n\n"
            "## 2 Section 2\n\nAnother rule.\n")
    path, corpus = write(tmp_path, body)
    _, chunks = chunk_file(path, corpus)
    text = "".join(c.text for c in chunks)
    assert "substituted (18.4.2005)" not in text
    assert "The rule." in text and "Another rule." in text


@pytest.mark.parametrize("title", ["Modifications etc. (not altering text)",
                                   "Commencement Information",
                                   "Marginal Citations"])
def test_live_annotations_are_kept(tmp_path, title):
    """Only pure amendment history goes; cross-references and commencement
    caveats are fields in the extract schema."""
    body = (f"## 1 Section 1\n\nThe rule.\n\n{title}\n\n"
            "[C2](#reference-key-4eb1) S. 1 applied by another Act\n")
    path, corpus = write(tmp_path, body)
    _, chunks = chunk_file(path, corpus)
    assert "applied by another Act" in "".join(c.text for c in chunks)
