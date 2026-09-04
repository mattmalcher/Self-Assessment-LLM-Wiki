---
title: How this wiki stays current
---

# How this wiki stays current

The wiki is built in three stages. Only the first runs in CI; the two LLM
stages run locally, on the maintainer's own Claude or OpenAI subscription.

```
  (1) FETCH                (2) EXTRACT               (3) COMPOSE
  deterministic            LLM, cached by            LLM, cached by
  HTTP, in CI              chunk hash                page input hash

  legislation.gov.uk
  GOV.UK Content API  -->  corpus/*.md    -->   extracts/*.json   -->  docs/*.md
  Find Case Law            (raw mirror)         (structured notes)     (this wiki)
  other sites
```

Each stage is separately cached, and every cache is content-addressed, so a
refresh costs work only in proportion to what actually changed upstream.

## Stage 1 — fetch (deterministic, runs in CI)

`pipeline/sources.yml` is the registry of every tracked source. `pipeline/fetch.py`
dispatches each entry to a fetcher by `type` and writes markdown into `corpus/`.

Change detection is layered:

1. **HTTP validators.** Every request sends `If-None-Match` / `If-Modified-Since`
   from the previous run's `ETag` / `Last-Modified`, stored in
   `pipeline/manifest.json`. A `304` ends the work for that source.
2. **Upstream timestamps.** The GOV.UK Content API reports `public_updated_at`;
   the pipeline compares it before re-rendering.
3. **Content hash.** The rendered markdown is SHA-256'd and compared to the
   stored hash. Unchanged content is never rewritten, so it never shows up in
   a diff and never invalidates the LLM stages downstream.
4. **Cursors.** Case law feeds are read incrementally from the last-seen entry.

This runs weekly under `.github/workflows/refresh.yml`, which opens a pull
request when the corpus moves — and tells you in the PR body which wiki pages
the change has made stale.

## Stage 2 — extract (LLM, cached per chunk)

Corpus documents are far too large to summarise in one pass: the Taxes
Management Act 1970 mirror alone is ~2MB. So each document is split into
heading-aware chunks (`synth/chunk.py`), and each chunk is passed to a model
that returns a **structured JSON note** — not prose:

- a relevance judgement (`core` / `related` / `none`, for Self Assessment
  specifically)
- topic tags and a short summary
- lists of obligations, deadlines, amounts, penalties, definitions,
  cross-references and caveats, each carrying a citation `ref`

Notes land in `extracts/`, one JSON file per corpus document, **keyed by the
SHA-256 of the chunk text**. That key is the whole efficiency mechanism:
chunk boundaries follow headings, so amending three sections of an Act changes
three chunk hashes and leaves the rest cached. The next run re-reads three
chunks, not 141. Notes whose chunk no longer exists are pruned automatically.

The extract files are committed. They are both the cache and the structured
intermediate that a future head-of-duty implementation would consume directly
— see the [data model notes](../reference-implementation/data-model-notes.md).

## Stage 3 — compose (LLM, cached per page)

`synth/pages.yml` defines each wiki page: its title, output path, a brief, and
a **deterministic selector** — which corpus paths to draw from, which relevance
tiers to admit, and regexes that a note's heading, summary, topics or citations
must match. Selection involves no model call, which is what makes staleness
cheap to compute:

> A page's `input_hash` is the SHA-256 of its brief, the compose prompt, the
> model name, and the sorted set of chunk hashes selected for it. If that hash
> matches `synth/manifest.json`, the page is up to date and is skipped.

So a corpus change only recomposes the pages whose selected notes actually
moved. Editing one page's brief recomposes that page alone.

The composer is told to use **only** the supplied notes, to cite every rule and
figure, to distinguish statute from HMRC interpretation from customer guidance,
and to declare gaps rather than fill them from its own knowledge. Each page is
written with front matter recording the model, date, input hash and note count,
and a footer listing every source it drew on.

## Running it

```bash
python -m pipeline.fetch          # stage 1 — no API access needed
python -m synth.build status      # what's stale, no model calls
python -m synth.build extract     # stage 2
python -m synth.build compose     # stage 3
python -m synth.report            # regenerate this site's status page
```

`synth.build` defaults to `--backend claude-cli`, which shells out to the
`claude` CLI and therefore runs on a Claude Code subscription with no API key.
`--backend codex-cli` does the same through `codex exec`; `--backend anthropic`
and `--backend openai` use API keys instead. See the repository's
`synth/README.md` for the full set of options and cost controls.

## Adding a source, or a page

- **A source:** add an entry to `pipeline/sources.yml` with a unique `id`,
  a `type` matching a fetcher, `status: fetch` and an `output` path under
  `corpus/`. Run `python -m pipeline.fetch --only <id>`.
- **A page:** add an entry to `synth/pages.yml` with an `id`, `title`,
  `output` under `docs/`, a `brief`, and a `select` block. Check the selector
  with `python -m synth.build compose --dry-run`, which reports how many notes
  it picks up, before spending a model call on it.

[Wiki status](wiki-status.md) reports how much of the corpus has been through
stage 2 and when each page last went through stage 3.
