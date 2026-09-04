"""Shared HTTP + hashing helpers for the fetch pipeline."""
from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass

import requests

USER_AGENT = "self-assessment-llm-wiki/0.1 (+https://github.com/mattmalcher/Self-Assessment-LLM-Wiki)"

_session = requests.Session()
_session.headers.update({"User-Agent": USER_AGENT})


@dataclass
class FetchResult:
    changed: bool
    status_code: int
    text: str | None = None
    json: dict | None = None
    etag: str | None = None
    last_modified: str | None = None


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def conditional_get(url: str, cache: dict, *, as_json: bool = False, retries: int = 3) -> FetchResult:
    """GET url, using If-None-Match/If-Modified-Since from `cache` when present.

    `cache` is the manifest entry's http sub-dict (or {}), with optional
    "etag" / "last_modified" keys from a previous run. Returns changed=False
    only on an actual 304 - a 200 always comes back as changed=True and it's
    up to the caller to also compare a content hash, since not every upstream
    sends validators.
    """
    headers = {}
    if cache.get("etag"):
        headers["If-None-Match"] = cache["etag"]
    if cache.get("last_modified"):
        headers["If-Modified-Since"] = cache["last_modified"]

    last_exc = None
    for attempt in range(retries):
        try:
            resp = _session.get(url, headers=headers, timeout=60)
            break
        except requests.RequestException as exc:  # network blip - retry with backoff
            last_exc = exc
            time.sleep(2 * (attempt + 1))
    else:
        raise RuntimeError(f"Failed to fetch {url}: {last_exc}")

    if resp.status_code == 304:
        return FetchResult(changed=False, status_code=304,
                            etag=cache.get("etag"), last_modified=cache.get("last_modified"))

    resp.raise_for_status()
    return FetchResult(
        changed=True,
        status_code=resp.status_code,
        text=resp.text,
        json=resp.json() if as_json else None,
        etag=resp.headers.get("ETag"),
        last_modified=resp.headers.get("Last-Modified"),
    )
