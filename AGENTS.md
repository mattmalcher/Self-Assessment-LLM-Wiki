# AGENTS.md

Orientation for coding agents. Unofficial LLM-written wiki on UK Self
Assessment, built by a three-stage pipeline and published to GitHub Pages.

## Pipeline

```
fetch (CI, weekly)   extract (local, LLM)   compose (local, LLM)
sources.yml -> corpus/*.md -> extracts/*.json -> docs/*.md -> mkdocs site
```

Every stage is content-addressed: fetch skips on 304/hash, extract is keyed on
chunk SHA-256, compose on brief+prompt+model+chunk hashes. An extracted note
only counts as cached if it passes `synth/schema.py`; a malformed one is
reported by `status` and re-extracted on the next run. Stages 2-3 never run
in CI — they cost model calls on the maintainer's own subscription.

## Do not hand-edit

`corpus/`, `extracts/`, `docs/`, and both `manifest.json` files are generated;
edits are overwritten. Hand-written exceptions: `docs/index.md`,
`docs/external-explainers.md`, `docs/reference-implementation/data-model-notes.md`,
`docs/meta/refresh-process.md`.

To change a page's content, edit its brief/selector in
`src/self_assessment_wiki/synth/pages.yml` or the prompts in
`src/self_assessment_wiki/synth/prompts/`. To add a source, add an entry to
`src/self_assessment_wiki/pipeline/sources.yml`.

Changing `prompts/compose.md` invalidates every page; changing `chunk._clean`
invalidates the whole extract cache. Both mean a full re-run — flag the cost
before doing it. A page is also stale when any note it selects changes content,
extract prompt or extraction model — see "The invalidation contract" in
`src/self_assessment_wiki/synth/README.md`.

## Commands

Requires [`uv`](https://docs.astral.sh/uv/). No linter config.

```bash
uv sync
uv run pytest                  # offline regression tests; no model calls
uv run mkdocs serve            # local preview
uv run mkdocs build --strict   # what CI deploys; strict, so nav must resolve

uv run fetch --dry-run         # stage 1, no API access needed
uv run fetch --only <source-id>
uv run fetch --keep-going      # best effort; any failure exits non-zero without it
uv run reconcile               # audit corpus/ against sources.yml; free, offline

uv run status                  # what's stale; free
uv run extract --limit 20      # stages 2-3, cost money
uv run compose --only <page-id>
uv run synth all
uv run report                  # refresh docs/meta/wiki-status.md
```

Prefer `--dry-run` / `status` / `--limit` when verifying a change; never kick
off a full `synth all` unasked.

`fetch` also audits what it left behind: a source that reported success but
wrote no file (or, for a shared output, no `<!-- section:ID -->` block) fails
the run. A missing artifact makes the fetchers drop their cache validators, so
a warm cache rebuilds the file rather than reporting "unchanged" forever.
`uv run reconcile` runs that audit on its own, and gates the Pages workflow.

Any failed source, chunk or page makes its command exit non-zero and lands in
`pipeline/last_run.json` or `synth/last_run.json` (both gitignored). Pass
`--keep-going` for best-effort behaviour - `synth all` also needs it to compose
after a failed extract.

## Layout

| Path | What |
|---|---|
| `src/self_assessment_wiki/pipeline/` | stage 1: `sources.yml`, `fetchers/`, `fetch.py` |
| `src/self_assessment_wiki/synth/` | stages 2-3: `pages.yml`, `prompts/`, `chunk.py`, `extract.py`, `compose.py`, `llm.py`, `build.py`, `nav.py` |
| `mkdocs.yml`, `overrides/` | Material theme site config |
| `.github/workflows/refresh.yml` | weekly corpus refresh → PR + staleness report |
| `.github/workflows/pages.yml` | build + deploy on push to `main` |

Deeper detail on backends, caching and cost control:
`src/self_assessment_wiki/synth/README.md`.

## Content rules

Pages must cite a source for every rule and figure and must not use knowledge
outside the supplied notes. Nothing here is HMRC material or tax advice; keep
the unofficial framing intact in anything user-facing.
