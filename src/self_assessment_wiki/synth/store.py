"""Read/write the per-document extract files under extracts/.

One JSON file per corpus document, mirroring its path:

    corpus/legal-system/.../tma-1970.md  ->  extracts/legal-system/.../tma-1970.json

    {
      "doc": "legal-system/.../tma-1970.md",
      "source_url": ..., "source_id": ...,
      "chunks": { "<chunk-hash>": {"index":..,"heading":..,"note":{...}} }
    }

Keyed by chunk hash, so a refresh that changes three sections of an Act
re-runs the model on three chunks and reuses the rest verbatim. These files
are committed: they are both the cache and the structured intermediate a
future head-of-duty implementation would consume.
"""
from __future__ import annotations

import json
from pathlib import Path

from .config import EXTRACTS_DIR


def path_for(doc_rel: str) -> Path:
    return EXTRACTS_DIR / Path(doc_rel).with_suffix(".json")


def load(doc_rel: str) -> dict:
    path = path_for(doc_rel)
    if not path.exists():
        return {"doc": doc_rel, "chunks": {}}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return {"doc": doc_rel, "chunks": {}}
    data.setdefault("chunks", {})
    return data


def save(doc_rel: str, data: dict) -> None:
    path = path_for(doc_rel)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def load_all() -> dict[str, dict]:
    """Every extract file on disk, keyed by corpus-relative document path."""
    out: dict[str, dict] = {}
    if not EXTRACTS_DIR.exists():
        return out
    for path in sorted(EXTRACTS_DIR.rglob("*.json")):
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        out[data.get("doc") or path.relative_to(EXTRACTS_DIR).with_suffix(".md").as_posix()] = data
    return out


def prune_orphans(doc_rel: str, data: dict, live_hashes: set[str]) -> int:
    """Drop cached chunks whose text no longer appears in the document."""
    stale = [h for h in data["chunks"] if h not in live_hashes]
    for h in stale:
        del data["chunks"][h]
    return len(stale)
