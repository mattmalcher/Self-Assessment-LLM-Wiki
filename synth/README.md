# `synth/` — the LLM layer

Turns the raw mirror in `corpus/` into the written wiki in `docs/`.

This is the part you run **locally**, against a subscription you already pay
for. It is deliberately not in CI: the scheduled workflow refreshes the corpus
and tells you what that made stale, and you do the model work on your own
machine with your own account.

```
corpus/*.md  --[extract]-->  extracts/*.json  --[compose]-->  docs/*.md
             per chunk,                        per page,
             cached by chunk hash              cached by input hash
```

## Quick start

```bash
python -m synth.build status              # what's stale — costs nothing
python -m synth.build extract --limit 20  # try 20 chunks first
python -m synth.build compose --only who-must-file
```

Then the full run:

```bash
python -m synth.build all
python -m synth.report                    # refresh docs/meta/wiki-status.md
```

## Backends

| `--backend` | Needs | Auth |
|---|---|---|
| `claude-cli` (default) | the `claude` CLI on PATH | your Claude Code subscription — no API key |
| `codex-cli` | the `codex` CLI on PATH | your ChatGPT subscription — no API key |
| `anthropic` | `pip install -r requirements-synth.txt` | `ANTHROPIC_API_KEY` |
| `openai` | `pip install -r requirements-synth.txt` | `OPENAI_API_KEY` |

Each backend has a per-stage default model (cheap tier for extraction, strong
tier for composition — see `DEFAULT_MODELS` in `config.py`); `--model` overrides
both. Extra CLI flags can be passed through `SYNTH_CLAUDE_CLI_ARGS` /
`SYNTH_CODEX_CLI_ARGS`.

The CLI backends invoke the tool once per chunk with no tool access
(`--restricted` for `claude`), reading the prompt from stdin and parsing the
structured result. Failures retry with backoff; a chunk that fails three times
is reported and skipped rather than sinking the run.

## Cost control

Extraction is the bulk of the spend — one call per corpus chunk, currently
~540 chunks for a full cold run. Everything is designed so you rarely pay that
twice:

- `--limit N` stops after N chunks. Safe to interrupt and resume — everything
  already extracted is written out as it completes.
- `--only <path>` restricts extraction to specific corpus documents (a path or
  a directory prefix), and composition to specific page ids.
- `--dry-run` prints the plan and the call count without calling anything.
- `--concurrency N` (default 4) parallelises extraction.
- Re-running after a corpus refresh only touches chunks whose text changed:
  chunk boundaries follow markdown headings, so an amendment to three sections
  of an Act invalidates three chunks, not the document.

Composition is ~17 calls for the whole site, and only runs for pages whose
selected notes changed.

## Files

| Path | What it is |
|---|---|
| `pages.yml` | the page plan: title, output, brief and note selector per page |
| `prompts/extract.md` | system prompt for stage 2 — defines the note schema |
| `prompts/compose.md` | system prompt for stage 3 — citation and sourcing rules |
| `chunk.py` | heading-aware chunker, stable hashes |
| `llm.py` | the four backends behind one `complete()` |
| `extract.py` | stage 2 driver + cache planning |
| `compose.py` | stage 3: note selection, staleness, page assembly |
| `store.py` | read/write/prune `extracts/` |
| `report.py` | writes `docs/meta/wiki-status.md` |
| `build.py` | the CLI |
| `manifest.json` | per-page input hashes — machine-written, do not edit |

## Changing what the wiki says

Two levers, and neither involves editing `docs/` by hand (anything you write
there is overwritten on the next compose):

1. **`pages.yml`** — the brief steers what a page argues and how it's laid out;
   the `select` block steers what evidence it sees. Widen `match`, add
   `related` to `relevance`, or raise `max_notes` if a page is coming out thin.
   `--dry-run` shows the note count before you spend anything.
2. **`prompts/`** — the house style and the sourcing rules for every page.
   Changing `compose.md` invalidates every page's input hash, so the next
   compose run rewrites the whole site.
