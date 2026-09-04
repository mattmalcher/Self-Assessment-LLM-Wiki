"""Load/save pipeline/manifest.json - the cache-validator + hash store.

Kept separate from sources.yml so the registry stays human-edited while
this file is entirely machine-generated/updated by fetch.py.
"""
from __future__ import annotations

import json
from pathlib import Path

MANIFEST_PATH = Path(__file__).parent / "manifest.json"


def load() -> dict:
    if not MANIFEST_PATH.exists():
        return {}
    return json.loads(MANIFEST_PATH.read_text())


def save(manifest: dict) -> None:
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def entry(manifest: dict, source_id: str) -> dict:
    return manifest.setdefault(source_id, {})
