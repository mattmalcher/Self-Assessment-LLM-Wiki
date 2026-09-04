# Self Assessment LLM Wiki

An **LLM-written** reference on UK Self Assessment (Income Tax), published to
GitHub Pages, condensed from a continuously refreshed mirror of the primary
material — legislation, tribunal decisions, HMRC manuals and policy
publications, and customer-facing guidance.

**Site:** https://mattmalcher.github.io/Self-Assessment-LLM-Wiki/ (enable
GitHub Pages under Settings → Pages → Source: GitHub Actions, and Settings →
Actions → General → Workflow permissions: Read and write, for the first deploy)

## The three layers

```
  (1) FETCH                (2) EXTRACT               (3) COMPOSE
  deterministic HTTP       LLM, one call per         LLM, one call per
  runs in CI, weekly       corpus chunk              wiki page
                           runs locally              runs locally

  legislation.gov.uk
  GOV.UK Content API  -->  corpus/*.md     -->  extracts/*.json  -->  docs/*.md
  Find Case Law            raw mirror,          structured JSON       the wiki,
  other sites              6MB+                 notes + citations     cited
```

Every layer is content-addressed and cached, so a refresh costs work only in
proportion to what changed upstream:

- **Fetch** skips on HTTP `304`, on an unchanged upstream timestamp, and on an
  unchanged content hash.
- **Extract** is keyed on the SHA-256 of each chunk of corpus text. Chunk
  boundaries follow markdown headings, so amending three sections of an Act
  invalidates three chunks — not the 141 that make up the Act.
- **Compose** is keyed on a page's brief, prompt, model and the set of chunk
  hashes its selector picks up. A corpus change recomposes only the pages whose
  evidence actually moved.

Stages 2 and 3 run **locally against your own Claude or OpenAI subscription**,
not in CI — see [`synth/README.md`](synth/README.md). CI refreshes the corpus
and reports what that made stale; you decide when to spend the model calls.

## Repo layout

```
corpus/         the raw mirror (machine-written; not published to the site)
extracts/       structured JSON notes, one file per corpus doc, keyed by
                chunk hash — both the LLM cache and the structured
                intermediate for a future head-of-duty implementation
docs/           the wiki (LLM-written, plus a few hand-written meta pages)
pipeline/       stage 1: sources.yml (the registry), fetchers/, fetch.py,
                manifest.json (HTTP/hash cache state)
synth/          stages 2-3: pages.yml (the page plan), prompts/, build.py,
                manifest.json (per-page input hashes)
mkdocs.yml      site config (Material theme)
.github/workflows/
  refresh.yml   weekly: refreshes corpus/, opens a PR, reports stale pages
  pages.yml     builds + deploys docs/ to GitHub Pages on push to main
```

Nothing under `corpus/`, `extracts/`, `docs/` (except `docs/index.md`,
`docs/external-explainers.md`, `docs/reference-implementation/data-model-notes.md`
and `docs/meta/refresh-process.md`) is hand-edited — it is all regenerated.
To change what a page says, change its brief or selector in `synth/pages.yml`,
or the prompts in `synth/prompts/`.

## Local development

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

mkdocs serve                                # http://127.0.0.1:8000

# stage 1 — no API access needed
python -m pipeline.fetch --dry-run          # check the registry resolves
python -m pipeline.fetch --only <source-id> # fetch one source
python -m pipeline.fetch                    # fetch everything due

# stages 2-3 — needs a Claude/OpenAI subscription or API key
python -m synth.build status                # what's stale; costs nothing
python -m synth.build extract --limit 20    # try 20 chunks first
python -m synth.build compose --only who-must-file
python -m synth.build all                   # the full run
python -m synth.report                      # refresh docs/meta/wiki-status.md
```

`synth.build` defaults to `--backend claude-cli` (the `claude` CLI, so your
Claude Code subscription, no API key). `--backend codex-cli` uses `codex exec`;
`--backend anthropic` / `--backend openai` use `ANTHROPIC_API_KEY` /
`OPENAI_API_KEY` and need `pip install -r requirements-synth.txt`.

## Where this is going

The wiki is groundwork for a reference implementation of a **head of duty**
system for Self Assessment. The extract schema is shaped for it — obligations,
deadlines, amounts, penalties and definitions, each with a citation — and two
generated pages (`rules-inventory`, `data-requirements`) exist specifically to
inventory what such a system would need. The implementation itself is not
started.

## Not legal advice

Two failure modes, both real: the mirror can lag upstream, and the pages are
written by a language model. The prompts forbid using knowledge outside the
supplied source notes and require a citation for every rule and figure, but
check anything you rely on against the cited source.
