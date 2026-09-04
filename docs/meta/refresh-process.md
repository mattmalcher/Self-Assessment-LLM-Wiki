# How this wiki stays current

Every source this wiki mirrors is registered once, in
[`pipeline/sources.yml`](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/pipeline/sources.yml),
and refreshed by a small Python pipeline rather than by hand. This page is
for anyone extending the wiki - it explains the mechanism and how to add a
source.

## The pipeline

`pipeline/fetch.py` reads the registry and, for every source marked
`status: fetch`, calls the fetcher named by its `type`
(`pipeline/fetchers/`). Each fetcher:

1. Requests the source (using conditional GET - `If-None-Match` /
   `If-Modified-Since` - where the upstream supports it, so an unchanged
   source costs one cheap round trip rather than a full re-download).
2. Converts what comes back into markdown with a front-matter block
   recording `source_url`, `source_id`, `category`, and where available the
   upstream's own `upstream_updated_at`.
3. Hashes the result and compares it against
   [`pipeline/manifest.json`](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/pipeline/manifest.json)
   (committed, one entry per source id). Only a changed hash triggers a
   write to `docs/`.

That hash comparison is what makes "efficient refresh" mean something
concrete: a scheduled run touches every registered source, but only
**writes** (and therefore only shows up in a PR diff) the ones that
actually changed. `pipeline/render_sources_index.py` then regenerates
[Sources](sources.md) from the registry + manifest, so that table is always
in sync.

### Source types

| `type` | Covers | How change is detected |
|---|---|---|
| `legislation` | Acts, SIs (legislation.gov.uk) | Part-level fetch, `Last-Modified`/hash |
| `govuk_content` | A single GOV.UK guidance/policy page | Content-API `public_updated_at` + hash |
| `govuk_content_collection` | A GOV.UK `document_collection` (index of documents, e.g. helpsheets, R&C Briefs) | Same, one index page (optionally with `expand_items: true` to also mirror each member document) |
| `govuk_content_manual` | An HMRC internal manual (a section tree) | Walks `child_section_groups` breadth-first, capped at `max_sections` fetches per run |
| `caselaw_feed` | A tribunal's Atom feed on Find Case Law | Feed `ETag`/`Last-Modified`; writes a recent-decisions index, not full judgment text |
| `web_page` | A plain HTML page (used for non-API, non-government sources) | `ETag`/`Last-Modified` + hash |

### Automation

- **`.github/workflows/refresh.yml`** runs the pipeline weekly (and on
  manual dispatch). If anything changed, it opens a pull request with a
  summary of what changed, generated from `pipeline/last_run_summary.md`.
  Nothing is ever pushed straight to `main` - a human merges the PR.
- **`.github/workflows/pages.yml`** builds and deploys the site with MkDocs
  whenever `main` changes under `docs/` or `mkdocs.yml`.

A source that fails to fetch (site down, blocked, schema changed) doesn't
stop the run - it's logged and left as previously fetched, and shows up in
the PR/run summary as a failure to investigate. See
`litrg-self-assessment` in the registry for a real example: LITRG blocks
non-browser requests, so that source is `status: registered` with a plain
link in [External explainers](../external-explainers.md) instead of a
perpetually-failing fetch.

## Adding a source

1. Add an entry to `pipeline/sources.yml` with a unique `id`, the right
   `type`, and `status: registered` if you're not ready to mirror it yet.
2. To actually pull it, set `status: fetch` and an `output` path under
   `docs/`.
3. Run `python -m pipeline.fetch --only <id>` locally to check the result
   before committing.
4. If no existing `type` fits (a new upstream shape), add a fetcher module
   under `pipeline/fetchers/` and register it in `_DISPATCH` in
   `pipeline/fetch.py`.

## Known limitations

- `govuk_content_manual` sections are capped per run (`max_sections`) so
  the very large manuals (Enquiry Manual, Compliance Handbook) are
  partially mirrored - the most central sections first, since traversal is
  breadth-first from the manual root. Raise the cap in `sources.yml` and
  re-run to pull further.
- `caselaw_feed` sources are a recent-decisions index (title, citation,
  date, link), not full judgment text - judgments are long and
  unevenly structured; the source link is the citable copy.
- Sites with bot protection (e.g. LITRG) can't be mirrored without a
  headless browser, which this pipeline deliberately doesn't carry. Such
  sources stay `registered` with a direct link instead.
