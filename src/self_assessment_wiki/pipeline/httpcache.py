"""Per-source HTTP validator store for the GOV.UK content API.

`manifest.json` records one entry per source: the content hash of what was
written and the validators for the one request that produced it. That shape
does not fit the GOV.UK fetchers, which make many requests per source - a
publication plus its HTML attachments, a collection plus every member, a
manual plus every section of its tree (the Compliance Handbook alone is
~2,100 sections). Keeping thousands of `ETag`s in `manifest.json` would bury
the human-readable cache state under machine noise, so each source gets its
own file here instead:

    pipeline/cache/<source-id>.json

    {
      "documents": {"<api path>": {"etag", "last_modified", "public_updated_at"}},
      "manual":    {"description": ..., "sections": [{"title", "path", "body"}]},
      "items":     [{"content_id", "base_path", "title"}]
    }

`documents` is what gets sent back as `If-None-Match` / `If-Modified-Since`.
The rest is what a `304` costs us: a response with no body carries no section
tree and no member list either, so the parts of the last full response that
the fetcher still needs are kept alongside the validators.

These files are committed. A weekly CI refresh starts from a fresh clone, so
an uncommitted cache is a cache that never hits.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"

_UNSAFE = re.compile(r"[^A-Za-z0-9._-]")


def path_for(source_id: str) -> Path:
    return CACHE_DIR / f"{_UNSAFE.sub('_', source_id)}.json"


def load(source_id: str) -> dict:
    path = path_for(source_id)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        # A corrupt cache is not worth failing a fetch over: an empty one just
        # means the next run re-downloads and rewrites it.
        return {}


def save(source_id: str, cache: dict) -> None:
    path = path_for(source_id)
    if not any(cache.values()):
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    # indent=0: one key per line, so a refresh diff shows which documents moved
    # rather than one rewritten line thousands of entries long.
    path.write_text(json.dumps(cache, indent=0, sort_keys=True) + "\n")
