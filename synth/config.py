"""Paths and defaults for the synthesis layer."""
from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CORPUS_DIR = REPO_ROOT / "corpus"
EXTRACTS_DIR = REPO_ROOT / "extracts"
DOCS_DIR = REPO_ROOT / "docs"
SYNTH_DIR = REPO_ROOT / "synth"
PAGES_PATH = SYNTH_DIR / "pages.yml"
PROMPTS_DIR = SYNTH_DIR / "prompts"
MANIFEST_PATH = SYNTH_DIR / "manifest.json"

# Target size of a corpus chunk handed to the extract stage, in characters.
# Legislation runs to ~2M characters per Act, so extraction is chunked and
# cached per chunk: a refresh that touches three sections re-extracts three
# chunks, not the whole Act.
CHUNK_CHARS = int(os.environ.get("SYNTH_CHUNK_CHARS", "12000"))

# Defaults; every one is overridable on the command line.
DEFAULT_BACKEND = os.environ.get("SYNTH_BACKEND", "claude-cli")
DEFAULT_CONCURRENCY = int(os.environ.get("SYNTH_CONCURRENCY", "4"))

# Per-backend default model. Deliberately the cheap/fast tier for extraction
# and the strong tier for composition - see build.py, which picks per stage.
DEFAULT_MODELS = {
    "claude-cli": {"extract": "sonnet", "compose": "opus"},
    "codex-cli": {"extract": "gpt-5-codex", "compose": "gpt-5-codex"},
    "anthropic": {"extract": "claude-sonnet-5", "compose": "claude-opus-5"},
    "openai": {"extract": "gpt-5-mini", "compose": "gpt-5"},
}
