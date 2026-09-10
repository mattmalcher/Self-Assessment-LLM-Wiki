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
uv run status              # what's stale — costs nothing
uv run extract --limit 20  # try 20 chunks first
uv run compose --only who-must-file
```

Then the full run:

```bash
uv run synth all
```

`extract` and `compose` regenerate `docs/meta/wiki-status.md` and the `.pages`
nav files at the end of any run that wrote something, so neither can be left
describing a tree that has moved on. `uv run report` does it on its own, and
`uv run report --check` writes nothing and exits non-zero if what is committed
is out of date - which is how CI catches drift on a pull request.

The status page is derived entirely from committed state - the corpus, the
extract cache, both manifests and the page plan - and nothing from the clock,
so the same tree always produces the same bytes. It reports valid cache
entries separately from the malformed ones, names any fetched source with no
artifact, and says plainly whether the committed artifacts are the output of a
complete end-to-end run or what is still outstanding.

## Backends

| `--backend` | Needs | Auth |
|---|---|---|
| `claude-cli` (default) | the `claude` CLI on PATH | your Claude Code subscription — no API key |
| `codex-cli` | the `codex` CLI on PATH | your ChatGPT subscription — no API key |
| `anthropic` | `uv sync --extra synth` | `ANTHROPIC_API_KEY` |
| `openai` | `uv sync --extra synth` | `OPENAI_API_KEY` |

Each backend has a per-stage default model (cheap tier for extraction, strong
tier for composition — see `DEFAULT_MODELS` in `config.py`); `--model` overrides
both. Extra CLI flags can be passed through `SYNTH_CLAUDE_CLI_ARGS` /
`SYNTH_CODEX_CLI_ARGS`.

The CLI backends invoke the tool once per chunk, reading the prompt from stdin
and parsing the structured result. For `claude` that is `--restricted --tools ""`
(no tool access at all — `--restricted` alone still leaves Read/Glob/Grep, so
the model can spend turns exploring whatever repo it is run from), plus
`--bare` (no hooks, no `CLAUDE.md` discovery, no memory) and
`--no-session-persistence` (otherwise a 400-chunk run leaves 400 transcripts in
`~/.claude/projects`).

Failures retry with backoff; a chunk that fails five times is reported and
skipped rather than sinking the run. A response that parses but isn't a valid
note is a separate, cheaper failure: it goes back to the model up to
`extract.VALIDATION_ATTEMPTS` times with the validator's complaints appended
(see "The note schema" below). A refusal that looks like a rate limit
backs off 60s → 5min → 10min → 15min rather than the few seconds an ordinary
flake gets, because a subscription window resets in minutes — the difference
between an unattended overnight run and a babysat one.

## Cost control

Extraction is the bulk of the spend — one call per corpus chunk, currently
~400 chunks for a full cold run. Everything is designed so you rarely pay that
twice:

- `--limit N` stops after N chunks. Safe to interrupt and resume: the extract
  file is written after **every completed chunk**, so a Ctrl-C or a rate limit
  an hour into ITEPA keeps everything already paid for.
- `--stale-prompt` also re-runs chunks whose cached note was written under an
  older `prompts/extract.md`. Every note records the prompt hash and the model
  that produced it, so `status` can tell you how many are stale instead of
  leaving old and new notes indistinguishable.
- `--only <path>` restricts extraction to specific corpus documents (a path or
  a directory prefix), and composition to specific page ids.
- `--dry-run` prints the plan and the call count without calling anything.
- `--concurrency N` (default 4) parallelises extraction.
- Re-running after a corpus refresh only touches chunks whose text changed:
  chunk boundaries follow markdown headings, so an amendment to three sections
  of an Act invalidates three chunks, not the document.

The chunker also decides what you pay to read. `chunk._clean` drops
legislation.gov.uk's **Textual Amendments** blocks — 42% of TMA 1970, 30% of
ITEPA 2003 — which record only that a provision changed and by what, never
what it used to say (the mirror holds the current consolidated text, so that
wording is not there to recover either way). The inline `F38` markers survive,
so amended passages are still flagged, and `corpus/` keeps the notes in full;
this only decides what the extract stage reads.

The other annotation types are **kept**, because they carry live content and
cost almost nothing (3 chunks in 407): "Modifications etc." records another
enactment *applying* a section — a `cross_references` entry, not history — and
"Commencement Information" is what makes a provision prospective, a `caveats`
entry. Override with `SYNTH_STRIP_ANNOTATIONS` (comma-separated titles; empty
keeps everything).

Chunks below `SYNTH_MIN_CHUNK_CHARS` (400) are merged into a
neighbour rather than costing a call of their own — nothing is discarded, the
text moves into the chunk beside it.

**Chunk hashes are computed over the cleaned text**, so any edit to `_clean`
invalidates the extract cache for every document it touches. Decide it before a
big run, not after.

Composition is ~17 calls for the whole site, and only runs for pages whose
selected notes changed.

## The note schema

`prompts/extract.md` describes the note shape; `schema.py` enforces it. A note
that fails validation is not a note: it is never written to `extracts/`, never
counted as cached by `status`/`report`, and never selected for a page.

Validation is strict on purpose - every documented key present, every value a
string, every `ref` non-empty, and no keys the prompt never asked for. Before
it existed, `llm.extract_json` returned the first balanced `{...}` it found and
`extract.run` cached it: three committed records turned out to be a single
nested obligation object rather than a note, and because their chunk hash was
present the planner counted them as done while the selector silently dropped
them. Their source text had disappeared between stages with `status` reporting
full coverage.

A cached note that fails the schema now shows up as work to do - `status`
counts it under "invalid" and the next `extract` run re-asks for that chunk, no
flag needed.

## Partial runs

Every stage keeps a report of the units it attempted - a source for `fetch`, a
chunk for `extract`, a page for `compose` - and one failed unit makes the
command exit non-zero. Best effort exists, but you have to ask for it:
`--keep-going` reports the same failures and exits 0 anyway. Work left over
because of `--limit` is `remaining`, not failed, and never fails the run.

The report is written to `pipeline/last_run.json` (fetch) and
`synth/last_run.json` (extract/compose, both stages when you run `synth all`),
listing what succeeded, what failed with which error, and what is outstanding.
Both files are gitignored; the refresh workflow uploads its copy as a job
artifact, flags a partial refresh at the top of the PR body and in the PR
title, and then fails the job.

## The invalidation contract

A page's `input_hash` in `manifest.json` decides whether composing it again
would change anything. It covers, and only covers:

- `prompts/compose.md`;
- the page's entry in `pages.yml`, minus the nav-only keys (`section`), which
  never reach the prompt;
- the compose model;
- every note the selector picks, fingerprinted by `compose.note_fingerprint`:
  the note's full content, its heading, source id and URL, the chunk hash it
  came from, the hash of `prompts/extract.md` it was written under, and the
  extraction `backend:model` that wrote it.

So a re-extracted or hand-corrected note makes every page that selects it
stale, even though its chunk hash is unchanged — as does re-extracting under a
new extract prompt or a different extraction model. Notes the selector does
**not** pick have no effect on the page, whatever happens to them.

Fingerprints are combined in a fixed `(doc, chunk_hash)` order and serialized
as compact sorted-key JSON, so the hash depends on note content rather than on
dict insertion order or the order `select()` happened to return.

`compose.NOTE_FINGERPRINT_VERSION` is bumped if that layout ever changes shape;
bumping it restages every page.

## Files

| Path | What it is |
|---|---|
| `pages.yml` | the page plan: title, output, brief, minimum authorities and note selector per page |
| `prompts/extract.md` | system prompt for stage 2 — defines the note schema |
| `prompts/compose.md` | system prompt for stage 3 — citation and sourcing rules |
| `chunk.py` | heading-aware chunker, stable hashes |
| `schema.py` | the note schema, enforced - nothing invalid is ever cached |
| `llm.py` | the four backends behind one `complete()` |
| `extract.py` | stage 2 driver + cache planning |
| `compose.py` | stage 3: note selection, staleness, page assembly |
| `store.py` | read/write/prune `extracts/` |
| `report.py` | writes `docs/meta/wiki-status.md`; `--check` gates drift in CI |
| `nav.py` | writes the `.pages` nav files, in `pages.yml` order |
| `build.py` | the CLI |
| `manifest.json` | per-page input hashes — machine-written, do not edit |

## Changing what the wiki says

Two levers, and neither involves editing `docs/` by hand (anything you write
there is overwritten on the next compose):

1. **`pages.yml`** — the brief steers what a page argues and how it's laid out;
   `authorities` declares the minimum source IDs its selected evidence must
   contain, and the `select` block steers what evidence it sees. Selection
   reserves one matching note per required authority before filling
   `max_notes`; any other matching notes hidden by that cap are counted in
   `status`, compose `--dry-run`, and the generated wiki status page. Missing
   authorities visibly label the next composed page as incomplete. Widen
   `match`, add `related` to `relevance`, or raise `max_notes` if a page is
   coming out thin.
2. **`prompts/`** — the house style and the sourcing rules for every page.
   Changing `compose.md` invalidates every page's input hash, so the next
   compose run rewrites the whole site.
