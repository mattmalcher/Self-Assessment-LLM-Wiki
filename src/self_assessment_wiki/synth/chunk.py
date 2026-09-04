"""Split a corpus markdown file into heading-aware, hash-addressed chunks.

Chunk boundaries follow markdown headings rather than a fixed character
window, so a chunk is a coherent run of sections (e.g. TMA 1970 s.8-s.9) and
its hash stays stable when an unrelated part of the same Act is amended.
That stability is what makes the extract cache worth having.
"""
from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .config import CHUNK_CHARS, MIN_CHUNK_CHARS

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)

# legislation.gov.uk editorial annotations: a bare title line followed by one
# entry per amendment. They are not all the same kind of thing, and only one
# kind is expensive - measured share of the mirrored text:
#
#                                  TMA     ITEPA   CRCA    FTT rules
#   Textual Amendments             42.3%   30.1%   24.2%   29.0%
#   Commencement Information         -       -     13.7%     -
#   Modifications etc.              0.8%    0.1%    3.1%     -
#   Marginal Citations              0.0%     -       -      0.4%
#
# Textual Amendments are pure history ("S. 1 substituted (18.4.2005) by ..."),
# and since the mirror holds only the *current* consolidated text they cannot
# tell you what a provision used to say - just that it changed, which the
# surviving inline F-markers already flag and corpus/ still records in full.
#
# The rest carry live content and are nearly free, so they are kept:
# "Modifications etc." records another enactment *applying* a section (a
# cross-reference, not history) and "Commencement Information" is what makes a
# provision prospective (a caveat). Both are fields in the extract schema.
_STRIPPED_ANNOTATIONS = tuple(
    a.strip() for a in os.environ.get("SYNTH_STRIP_ANNOTATIONS", "Textual Amendments").split(",")
    if a.strip()
)
_ANNOTATION_TITLE = re.compile(
    r"^(" + "|".join(re.escape(a) for a in _STRIPPED_ANNOTATIONS) + r")\b.*$"
) if _STRIPPED_ANNOTATIONS else None
# An annotation entry opens with its commentary key, either as a back-link
# ("[F1](#reference-key-…)S. 1 substituted …") or bare ("C2S. 1 applied …").
_ANNOTATION_ENTRY = re.compile(r"^\[?[FCIEMPX]\d+\]?\b")
# Commentary anchors carry a hash and no information once the hover title is
# gone: "[F204](#commentary-key-8c03…)" -> "F204".
# The lookahead keeps "[F2](#…)2 General Commissioners" from becoming the
# unreadable "F22 General Commissioners".
_COMMENTARY_LINK = re.compile(r"\[([FCIEMPX]\d+)\]\(#[^)]*\)(?=\S)")
_COMMENTARY_LINK_EOW = re.compile(r"\[([FCIEMPX]\d+)\]\(#[^)]*\)")


@dataclass
class Chunk:
    doc: str               # corpus-relative path
    index: int
    heading_path: list[str]
    text: str
    hash: str = field(default="")

    def __post_init__(self) -> None:
        if not self.hash:
            self.hash = hashlib.sha256(self.text.encode("utf-8")).hexdigest()[:16]

    @property
    def heading(self) -> str:
        return " > ".join(self.heading_path) if self.heading_path else "(document start)"


def split_front_matter(text: str) -> tuple[dict, str]:
    match = _FRONT_MATTER.match(text)
    if not match:
        return {}, text
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, text[match.end():]


def _strip_annotations(text: str) -> str:
    """Drop the annotation blocks named in SYNTH_STRIP_ANNOTATIONS.

    An annotation block is a title line ("Textual Amendments") followed by
    blank-separated entries, each opening with its commentary key (F1, C2,
    I3, M1). A block runs until the first paragraph that is not an entry - in
    practice, the next heading.

    Set SYNTH_STRIP_ANNOTATIONS to a comma-separated list of titles to change
    what goes, or to the empty string to keep every annotation.
    """
    if _ANNOTATION_TITLE is None:
        return text
    out: list[str] = []
    lines = text.splitlines(keepends=True)
    i = 0
    while i < len(lines):
        if not _ANNOTATION_TITLE.match(lines[i].rstrip("\n")):
            out.append(lines[i])
            i += 1
            continue
        i += 1  # the title line
        while i < len(lines):
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i >= len(lines) or not _ANNOTATION_ENTRY.match(lines[i].lstrip()):
                break
            while i < len(lines) and lines[i].strip():  # the entry paragraph
                i += 1
    return "".join(out)


def _clean(text: str) -> str:
    """Strip the mirroring artefacts that would otherwise dominate a chunk.

    legislation.gov.uk markdown carries a hover title on nearly every link
    ("Go to S. 1"), which is pure noise to a summariser and can be a third of
    the characters in a section, and repeats every amendment's history under
    the provision it touched.

    Chunk hashes are computed over the cleaned text, so changing this
    function invalidates the extract cache for every document it touches.
    """
    text = re.sub(r'\]\(([^)\s]+)\s+"[^"]*"\)', r"](\1)", text)
    text = _strip_annotations(text)
    text = _COMMENTARY_LINK.sub(r"\1 ", text)
    text = _COMMENTARY_LINK_EOW.sub(r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def _coalesce(chunks: list[Chunk], min_chars: int) -> list[Chunk]:
    """Merge undersized chunks into a neighbour rather than paying a model
    call for a bare `---` or an orphan heading.

    Nothing is discarded: a runt is appended to the preceding chunk, or to
    the following one when it is the first. The merged chunk keeps the
    earlier heading path, and hashes/indices are recomputed from the joined
    text.
    """
    if len(chunks) < 2:
        return chunks
    merged: list[Chunk] = []
    for chunk in chunks:
        if merged and len(chunk.text.strip()) < min_chars:
            prev = merged[-1]
            merged[-1] = Chunk(doc=prev.doc, index=prev.index, heading_path=prev.heading_path,
                               text=prev.text.rstrip("\n") + "\n\n" + chunk.text)
        else:
            merged.append(chunk)
    # A runt in first position has no predecessor to join, so fold it forward.
    while len(merged) > 1 and len(merged[0].text.strip()) < min_chars:
        first, second = merged[0], merged[1]
        merged[:2] = [Chunk(doc=first.doc, index=0, heading_path=first.heading_path,
                            text=first.text.rstrip("\n") + "\n\n" + second.text)]
    return [Chunk(doc=c.doc, index=i, heading_path=c.heading_path, text=c.text)
            for i, c in enumerate(merged)]


def chunk_file(path: Path, corpus_root: Path, *, target_chars: int = CHUNK_CHARS) -> tuple[dict, list[Chunk]]:
    raw = path.read_text()
    meta, body = split_front_matter(raw)
    body = _clean(body)
    rel = path.relative_to(corpus_root).as_posix()

    # Walk the body building (heading_path, block) pairs, then greedily pack
    # them into chunks up to target_chars.
    blocks: list[tuple[list[str], str]] = []
    stack: list[tuple[int, str]] = []
    current: list[str] = []
    current_path: list[str] = []

    def flush() -> None:
        if current and "".join(current).strip():
            blocks.append((list(current_path), "".join(current)))
        current.clear()

    for line in body.splitlines(keepends=True):
        match = _HEADING.match(line.rstrip("\n"))
        if match:
            flush()
            level = len(match.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, match.group(2).strip()))
            current_path = [h for _, h in stack]
        current.append(line)
    flush()

    chunks: list[Chunk] = []
    buf: list[str] = []
    buf_path: list[str] = []
    size = 0

    def emit() -> None:
        nonlocal buf, buf_path, size
        if buf:
            chunks.append(Chunk(doc=rel, index=len(chunks), heading_path=buf_path, text="".join(buf).strip() + "\n"))
        buf, buf_path, size = [], [], 0

    for heading_path, block in blocks:
        # A single section longer than the target is split on paragraph
        # boundaries rather than truncated - some ITEPA sections are huge.
        if len(block) > target_chars * 2:
            emit()
            paras = block.split("\n\n")
            part: list[str] = []
            part_size = 0
            for para in paras:
                if part_size + len(para) > target_chars and part:
                    chunks.append(Chunk(doc=rel, index=len(chunks), heading_path=heading_path,
                                        text="\n\n".join(part).strip() + "\n"))
                    part, part_size = [], 0
                part.append(para)
                part_size += len(para) + 2
            if part:
                chunks.append(Chunk(doc=rel, index=len(chunks), heading_path=heading_path,
                                    text="\n\n".join(part).strip() + "\n"))
            continue
        if size + len(block) > target_chars and buf:
            emit()
        if not buf:
            buf_path = heading_path
        buf.append(block)
        size += len(block)
    emit()

    return meta, _coalesce(chunks, MIN_CHUNK_CHARS)
