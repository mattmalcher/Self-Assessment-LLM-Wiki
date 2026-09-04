# Synth pipeline review - before the first full extract/compose run

Reviewed 2026-09-04, ahead of running the extract and compose stages against a
claude.ai subscription via the `claude-cli` backend.

## Current state

- 42 corpus documents, 541 chunks, 5.3M characters.
- 33 chunks already extracted (SALF manual, FTT procedure rules).
- One page composed (`docs/lifecycle/who-must-file.md`, 2,764 words) - reads well.
- Cost is dominated by extraction: 508 calls remain. Composition is 17 calls.

## Status (worked through 2026-09-04)

| Item | State |
|---|---|
| 1. Per-document save | **done** - `store.save` after every completed chunk |
| 2. Annotation stripping | **done, narrowed** - Textual Amendments only; 536 -> 407 chunks |
| 3. Prompt/model in cache | **done** - `prompt_hash` + `model` per note, `--stale-prompt` |
| 4. Helpsheet stubs | **done** - HTML attachments fetched; all 22 refetched |
| 5. ITEPA scope | **decision open** - see the recommended order below |
| 6. Manual `max_sections` | **decision open** - not a re-run risk |
| 7. Disclaimers | **done** - site banner, footer, per-page admonition, prompt rule |
| 8. CLI hygiene | **done** - `--tools ""`, `--bare`, `--no-session-persistence` |
| 9. Rate-limit backoff | **done** - 60s/5m/10m/15m on rate limits, 5 attempts |
| Minor: tiny chunks | **done differently** - coalesced into a neighbour, not skipped |

Item 2 was narrowed on review: the four annotation types are not equivalent.
Textual Amendments are 42%/30%/24% of TMA/ITEPA/CRCA and are pure history;
"Modifications etc." (a section *applied* by another enactment - a
cross-reference), "Commencement Information" (prospective provisions) and
"Marginal Citations" together are 0.1-3% and are substantive, so they are
kept. Keeping them costs 3 chunks out of 407. `SYNTH_STRIP_ANNOTATIONS`
controls the set; empty keeps everything.

Two extras found on the way: `items_dir` for the helpsheets pointed at `docs/`
rather than `corpus/`, so a refetch would have written 22 pages into the site;
and a failing `claude` exit was reported as a bare exit code because the CLI
puts its error on stdout, not stderr.

Not verified: no live model call was made (the `claude` CLI is not
authenticated from inside this session). `scratchpad/check_backend.py` smoke-
tests the flags, the backend class and one real chunk.

## Fix before running

These either lose work on interruption or force a re-extraction later.

### 1. Per-document save loses a whole Act on interruption

`extract.run` writes the extract file only after every chunk of a document has
completed (`src/self_assessment_wiki/synth/extract.py:107`). ITEPA is 238
chunks; TMA is 141. A Ctrl-C, a crash, or the plan's rate limit throwing
repeatedly an hour in discards everything done for that document.

**Fix:** call `store.save` after each completed future (or every N), not once
per document.

### 2. Legislation chunks are mostly amendment boilerplate, and the cleaner decides the cache key

Measured share of "Textual Amendments / Modifications etc. / Commencement
Information" annotation blocks in the legislation.gov.uk markdown:

| Document | Chars | Annotation blocks | Anchor-link hashes |
|---|---|---|---|
| TMA 1970 | 1.39M | 62% | 10% |
| ITEPA 2003 | 2.44M | 32% | 8% |
| CRCA 2005 | 0.32M | 60% | 5% |
| FTT rules 2009 | 0.08M | 29% | 8% |

The extract prompt already tells the model to classify these as `none`, so we
pay to have them read and discarded. Stripping them in `chunk._clean` would
roughly halve legislation input. The anchor links (`[F204](#reference-key-…)`)
carry no information once the hash is dropped.

Chunk hashes are computed over the *cleaned* text, so any later change to
`_clean` invalidates every legislation chunk. Decide this now, before the run,
not after.

**Fix:** in `chunk._clean`, drop annotation blocks (heading plus the `[F…]`,
`[C…]`, `[I…]` paragraphs that follow) and collapse `[Fn](#…)` to `Fn`. This
invalidates the 33 cached chunks, which is cheap.

### 3. The extract cache records neither prompt nor model

The cache key is the chunk hash alone. If `prompts/extract.md` is tuned after
200 chunks, nothing re-extracts and old notes are indistinguishable from new.

**Fix:** store a prompt hash and the model name in each chunk entry; add a way
to re-run only entries whose prompt hash is stale (e.g. `extract --stale-prompt`).
Either way, finalise `extract.md` before starting.

### 4. All 22 helpsheets are stubs

The GOV.UK fetcher (`pipeline/fetchers/govuk_content.py`, `fetch_single`)
takes `details.body`, which for helpsheet publications is a one-paragraph
summary (200-500 chars). The real helpsheet is an HTML attachment listed in
`details.attachments` (for HS204: `…/hs204-limit-on-income-tax-reliefs-2026`).

The `reliefs-and-claims` and `income-charges` pages lean on these. Fixing later
costs only 22 small re-extracts plus a few recomposes, so it is not blocking,
but it is cheap to fix first. The manuals index page is also empty ("0
documents") - harmless.

## Scope decisions worth making first

### 5. ITEPA is 44% of all calls

238 of 541 chunks. It is employment-income charging law - mostly `related`
for Self Assessment, and much of it (Part 7 share schemes, Part 7A disguised
remuneration, Part 11 PAYE) will rarely be selected by any page.

**Suggestion:** extract everything else first, compose, then decide whether
ITEPA earns its cost. `--only` takes directory prefixes, so this is easy.

### 6. Manuals are truncated by `max_sections`

Unmirrored sections: SAM ~997, CH ~656, EM ~461, ARTG ~209, SALF ~13. Not a
re-run risk (adding sections later is incremental), but the wiki's HMRC-view
content is thin relative to the statute.

### 7. Missing disclaimers
This is published on the open internet, people may arrive at it via search and mistake it for official advice. We must add obvious disclaimers so this does not happen. We must not pretend or leave any possible impression that this is official or related to or endorsed by HMRC.

## CLI backend hygiene

`src/self_assessment_wiki/synth/llm.py:69` (`ClaudeCLI.complete`):

7. `--restricted` removes code-running tools but leaves Read/Glob/Grep, so the
   model can burn turns exploring the repo. Add `--tools ""`. Add
   `--no-session-persistence` (otherwise 541 session transcripts land in
   `~/.claude/projects`) and `--bare` (skips hooks, CLAUDE.md discovery, memory).
8. Retry backoff is 3/6/9 seconds. Plan rate limits will exceed that, so chunks
   will "fail" and be retried on the next run. Acceptable once item 1 is fixed,
   but a longer backoff on rate-limit errors avoids babysitting.

## Minor

- 34 chunks are under 1,500 characters; three are under 50 (a bare `---` in
  SAM, two orphan headings in TMA). Skipping chunks below ~200 characters
  avoids junk notes.

## Recommended order

1. Code fixes: items 1, 2, 3, 7.
2. Fix the helpsheet fetcher and refetch (item 4).
3. `extract --only corpus/hmrc-publications corpus/legal-system/secondary-legislation corpus/legal-system/case-law`
4. `extract --only corpus/legal-system/primary-legislation/acts/tma-1970.md corpus/legal-system/primary-legislation/acts/crca-2005.md`
5. `compose`, review the pages.
6. Only then consider ITEPA.
