"""Split a corpus markdown file into heading-aware, hash-addressed chunks.

Chunk boundaries follow markdown headings rather than a fixed character
window, so a chunk is a coherent run of sections (e.g. TMA 1970 s.8-s.9) and
its hash stays stable when an unrelated part of the same Act is amended.
That stability is what makes the extract cache worth having.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .config import CHUNK_CHARS

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


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


def _clean(text: str) -> str:
    """Strip the mirroring artefacts that would otherwise dominate a chunk.

    legislation.gov.uk markdown carries a hover title on nearly every link
    ("Go to S. 1"), which is pure noise to a summariser and can be a third of
    the characters in a section.
    """
    text = re.sub(r'\]\(([^)\s]+)\s+"[^"]*"\)', r"](\1)", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


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

    return meta, chunks
