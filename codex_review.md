# Repository review: will it achieve its goals?

Reviewed 2026-09-08.

## Executive verdict

**Not yet.** The repository is a credible prototype of a content-addressed,
LLM-assisted publishing pipeline, and it can already build and publish a small
wiki. It does not yet provide enough evidence, source coverage, validation, or
failure handling to achieve its larger stated goal: a continuously refreshed,
dependable reference on UK Self Assessment that can serve as groundwork for a
head-of-duty implementation.

The design has a good spine: deterministic acquisition, chunk-level extraction,
page-level composition, prominent disclaimers, committed provenance, and a
deliberate separation between statute, HMRC interpretation, and public guidance.
Those choices make the project recoverable. The problems are not cosmetic,
though. Several cache and exit-status behaviours can silently leave stale or
missing content while reporting success; malformed model output is already
cached as complete; and much of the primary law required by the planned pages
is absent. The generated prose therefore cannot currently be treated as a
complete or consistently traceable reference, even with the disclaimers.

In practical terms:

- **As an experimental LLM-written tax wiki:** viable after a focused hardening
  pass.
- **As a continuously refreshed reference:** not reliable yet.
- **As input to a rules engine/head-of-duty implementation:** not suitable yet;
  the present JSON notes are lossy summaries, not validated executable legal
  rules.

## What is working well

1. **The pipeline boundaries are sensible.** `corpus/`, `extracts/`, and
   `docs/` separate acquired material, model interpretation, and publication.
   This is far easier to audit than a single retrieval-and-generation step.

2. **Chunk-level caching is a strong cost-control idea.** Heading-aware chunks
   and checkpointing after each successful extraction make long local runs
   resumable (`synth/chunk.py`, `synth/extract.py`).

3. **The project is unusually candid about risk.** The site-wide announcement,
   per-page disclaimer, status page, and source footer make the unofficial and
   LLM-written nature difficult to miss.

4. **The compose prompt has good editorial constraints.** It requires use of
   supplied notes only, citations for rules and figures, acknowledgement of
   gaps, and separation of statute from HMRC interpretation
   (`synth/prompts/compose.md`).

5. **The basic package and site build work.** Using the checked-in virtual
   environment, `.venv/bin/status` completed, Python byte-compilation passed,
   and `.venv/bin/mkdocs build --strict` completed. The build emitted one
   informational broken-anchor message for `external-explainers.md`, but did
   not fail.

6. **There is meaningful content, not just scaffolding.** The local planner
   currently sees 42 corpus documents and 1,264 chunks, with all 1,264 treated
   as cached. Three of seventeen planned pages exist and are considered current
   by the compose manifest; fourteen pages remain ungenerated.

## Findings, ordered by impact

### Critical: composition does not invalidate when an extracted note changes

`synth/compose.py:108-116` hashes the page spec, compose prompt, compose model,
and each selected `(document, chunk_hash)`. It does **not** hash the selected
note content, its extraction prompt hash, or its extraction model.

That defeats an important refresh path. Re-extracting the same source chunk
with a corrected prompt or better model keeps the chunk hash unchanged. The
resulting JSON note can change substantially, but every composed page can still
be reported as "up to date" and retain the old prose. Manual correction of a
bad note has the same problem. `--stale-prompt` therefore does not propagate
reliably into stage 3.

Hash the canonical serialized selected-note payload (including extraction
prompt/schema version and model), not merely the source chunk identity. Add a
regression test that changes a note without changing its chunk hash and expects
the dependent page to become stale.

### Critical: model output is parsed but never schema-validated

`synth/llm.py:216-256` accepts the first JSON object it can parse.
`synth/extract.py:114-128` immediately saves it as a successful note. There is
no validation of required keys, types, enum values, nested record shapes, or
citations.

This has already caused data loss. Of 1,261 stored chunk records inspected,
three have a `note` that is only one nested obligation/penalty object rather
than the required top-level schema:

- `extracts/legal-system/primary-legislation/acts/itepa-2003.json`, chunk
  `8a28aa5fc406f491`
- `extracts/legal-system/primary-legislation/acts/tma-1970.json`, chunk
  `4ad6263f238b0d57`
- `extracts/hmrc-publications/policy-and-interpretation/manuals/sam.json`, chunk
  `4357c9ab35c2a681`

Because their chunk hashes are present, the planner counts them as cached and
will not retry them. Because they have no `relevance`, the selector normally
drops them. Source content has therefore disappeared silently between stages
while the status command reports full extraction coverage.

Define and validate a strict schema (Pydantic, JSON Schema, or equivalent),
reject invalid results, retry with a validation error, and make `status` count
only valid notes. Validate nested `ref` fields as non-empty strings too.

### Critical: the source corpus cannot support the advertised scope

The registry has only three Acts: TMA 1970, ITEPA 2003, and CRCA 2005, plus the
FTT procedure rules. It omits primary legislation central to planned pages,
including at least ITTOIA 2005, ITA 2007, TCGA 1992, the main National Insurance
legislation, FA 2008 Schedule 41, FA 2009 Schedules 55 and 56, and FA 2021
Schedules 24 and 25. Relevant MTD regulations are also not mirrored.

This is incompatible with pages promising comprehensive coverage of income
charges, reliefs, rates, penalties, payment, and MTD. Those pages may quote
HMRC manuals or helpsheets describing the law, but the project explicitly
presents itself as condensed from primary material and tells the composer to
distinguish legal authority. A manual citation is not a substitute for the
enactment that creates the rule.

Several registered GOV.UK sources contain only collection indexes, not member
content: the detailed Self Assessment guide is about 2.6 KB, the rates and
allowances collection about 5 KB, and the policy collections are likewise
indexes unless `expand_items` is enabled. The case-law inputs contain only the
40 most recent titles/dates/links for each tribunal, not judgments. That is
enough for a recent-decisions list, but not to identify recurring themes,
holdings, statutory interpretation, or precedent reliably.

Create a source-to-page coverage matrix and prevent a page from being labelled
complete until its minimum authoritative sources are present. Either narrow
the advertised scope/page briefs or add and expand the required sources.

### High: partial failures usually return a successful exit status

The fetch command continues after per-source errors, which is useful, but
`pipeline/fetch.py:113` returns non-zero only if every fetch source failed and
nothing changed. One failed source among nineteen successful/unchanged sources
returns zero. Similarly, extract and compose return zero whenever at least one
unit succeeds, even if other units failed (`synth/build.py:79` and `:91`).

This makes automation and unattended runs unable to distinguish complete work
from partial work. The weekly workflow can open and merge a partial refresh as
if it succeeded, directly undermining "continuously refreshed".

Return non-zero for any failure by default. If best-effort behaviour is wanted,
make it an explicit flag and preserve a machine-readable run report listing
failed/stale sources, chunks, and pages. CI should fail or visibly mark the PR
as incomplete.

### High: a missing generic-web output can be permanently treated as cached

`pipeline/fetchers/web_page.py:34-36` skips the write when the new block hash
matches the manifest, without checking whether the output file exists. This is
not hypothetical: the manifest contains a successful cache entry for
`taxaid-self-assessment`, but its configured `corpus/external-explainers.md`
does not exist. A later identical fetch will return "unchanged" and still not
restore the file.

Use the same existence check as `pipeline/render.py:57`, and add a reconciliation
check ensuring every `status: fetch` source has its configured output (or, for
shared files, its named section). Cache state must never be accepted as proof
that an artifact exists.

### High: the project has no automated correctness tests or quality gate

There is no test suite. The deployment workflow tests only `mkdocs build
--strict`; the refresh workflow runs fetch and prints status. Neither validates
source registry structure, path containment, chunk stability, extract schema,
selector behaviour, cache invalidation, citations, generated page structure,
or corpus/manifest consistency.

This is especially risky because output is generated and legally sensitive.
The repository already contains a visible citation error propagated from an
HMRC-manual extract: `docs/lifecycle/who-must-file.md` cites partnership returns
as **TMA 1970 s.122AA**, while the Act contains **s.12AA**. The composition
prompt cannot catch a bad input citation, and there is no post-generation
checker.

Add unit tests for fetchers/chunking/caches and deterministic integrity checks
for committed artifacts. At minimum, CI should validate all extract records,
verify every source output, detect unknown citation references where possible,
ensure every generated H1/title/source footer is present, and fail when the
status report disagrees with the manifests.

### Accepted scope constraint: current law only

The pipeline mirrors current consolidated legislation and usually only the
latest helpsheet attachment. The chunk cleaner intentionally removes
textual-amendment blocks. This is appropriate for the now-explicit current-law
scope, but it cannot answer what law or guidance applied to an earlier tax year
or derive historical commencement and transition logic.

The extract schema also has no first-class `effective_from`, `effective_to`,
jurisdiction, authority, amendment, or supersession fields. An `amount.period`
string and free-text caveats are insufficient for executable temporal rules.

The README, site home page, and data-model notes now document that limitation.
Historical support should remain out of scope unless a later project adds dated
source snapshots and a versioned rule schema deliberately.

### Medium: extraction model changes are not considered stale

`synth/extract.py:53-55` identifies stale cached notes only by extraction prompt
hash. Although each record stores `model`, changing from one extraction model
to another does not schedule a re-extraction. This contradicts the nearby
comment that the metadata prevents notes from a weaker model being silently
mixed with current notes.

Include backend/model and schema version in the extraction cache key or stale
test. Offer an intentional `--accept-old-model` escape hatch if avoiding cost is
important.

### Medium: published status and navigation drift from the real repository

The checked-in `docs/meta/wiki-status.md` says 25 of 402 chunks (6%) were
extracted and only one page exists. The actual status command reports 1,264 of
1,264 cached and three current pages. `docs/lifecycle/.pages` still names only
`who-must-file.md`, so the other two generated lifecycle pages fall through the
ellipsis rather than receiving their planned order.

`report.py` says it is run at the end of extract/compose, but neither command
calls it; users must remember the separate `uv run report`. Generated status is
part of the project's safety case, so it should not be optional housekeeping.

Run report/nav generation automatically after successful extract/compose work,
or add a CI integrity check that regenerates them and requires a clean diff.
Display invalid/failed chunks, source-fetch failures, page validation failures,
and the last successful end-to-end refresh—not only raw cache presence.

### Medium: GOV.UK change-detection claims do not match implementation

`pipeline/fetchers/govuk_content.py:_get_doc` always calls
`conditional_get(..., {})`, discarding the saved HTTP validator. The stored
`upstream_updated_at` is written but never used for a skip. Collection items and
every manual section are therefore downloaded again on every run. Content
hashing prevents needless file writes, but the README's claims about layered
HTTP and upstream-timestamp skipping do not hold for this fetcher.

Pass cache entries through for documents/items/sections or qualify the
documentation. Per-section manifests would also allow a large manual refresh
to avoid hundreds or thousands of unnecessary API requests.

### Medium: path and configuration validation is too trusting

Registry and page YAML values are used as paths and regular expressions without
a schema or containment checks. A typo in `output`, `items_dir`, a regex, or a
required key fails late; an absolute or `..` output could write outside the
intended corpus/docs tree. This matters even in a personal project because CI
executes the checked-in registry.

Validate both YAML files up front: required fields and enums, unique IDs,
compilable regexes, allowed output roots, distinct outputs except explicitly
declared shared sections, and correspondence between fetchable sources and
artifacts.

### Low: documentation and content have smaller inconsistencies

- `synth/README.md` says the Claude invocation includes `--bare`, but
  `synth/llm.py` explicitly does not use it.
- `data-model-notes.md` calls the late-filing and late-payment regimes "TMA
  Sch 55" and "TMA Sch 56"; these are Finance Act 2009 schedules.
- `mkdocs build --strict` reports that `external-explainers.md` links to a
  missing `#content` anchor.
- The fetch summary says it refreshed `len(sources)` registered sources even
  though entries with `status: registered` are skipped, which overstates the
  attempted count.

These are straightforward fixes, but they reinforce the need for generated
artifact checks.

## Recommended route to a viable release

### 1. Make pipeline state truthful

Before generating more prose, fix note-content cache invalidation, strict
extract validation, artifact existence checks, and non-zero partial-failure
statuses. Delete/re-extract the three malformed cached notes. Regenerate status
and navigation automatically.

### 2. Add a deterministic integrity test suite

Cover schema/config validation, output containment, cache propagation,
missing-artifact recovery, duplicate IDs, chunking fixtures, and representative
fetcher fixtures. Add an artifact audit command that can run without network or
LLM access and make both workflows run it.

### 3. Define an authority/coverage contract for each page

For every planned page, list mandatory legislation, secondary legislation,
HMRC material, and any case law. Block or visibly label composition as
"insufficient sources" when those are missing. Do not let `max_notes` silently
turn a supposedly comprehensive inventory into the top 80/120 regex matches
without reporting what was excluded.

### 4. Expand or narrow the scope

Add the core tax and penalty enactments, substantive GOV.UK pages, and specific
case judgments needed by the briefs. Alternatively, rename the product as a
partial Self Assessment administration/manual digest and remove claims it
cannot substantiate.

### 5. Add post-generation assurance

Treat generated pages as build artifacts that must pass checks: expected title,
disclaimer, source footer, citations for numeric/legal assertions, references
resolvable to selected notes, no citations absent from the inputs, no empty
sections disguised as coverage, and an explicit source-gap section. A small
human review checklist is still appropriate before publishing tax content.

### 6. Separate the wiki model from the executable-rule model

Keep narrative extraction if it works for writing pages, but do not use it
directly as an implementation contract. Design a stricter rule representation
with typed inputs, predicates, outputs, legal authority, effective dates,
territorial scope, exceptions, precedence, and source quotations/anchors. Have
humans approve rules that will drive computation.

## Bottom line

The repository has the right broad architecture for an auditable experiment,
and it is much better than an opaque "ask an LLM to write a tax site" design.
Its current success signals, however, measure file/cache presence rather than
legal or data integrity. Until cache propagation, schema validation, failure
semantics, authoritative source coverage, and CI checks are
addressed, it will produce an attractive but selectively sourced wiki whose
staleness and omissions are not reliably surfaced. That falls short of the
stated goals, but the existing separation of stages makes a sounder second
iteration entirely feasible.

## Verification performed

- Inspected the README, page plan, source registry, prompts, fetchers,
  synthesis modules, manifests, workflows, generated pages, and status/meta
  documentation.
- Ran `.venv/bin/status` successfully.
- Ran `.venv/bin/mkdocs build --strict` successfully (one informational
  missing-anchor message).
- Ran `python3 -m compileall -q src` successfully.
- Audited all stored extract-note top-level shapes: 1,258 valid-shaped records
  and three invalid-shaped records out of 1,261 stored records.
- Confirmed the working tree was clean before this review; this file is the
  only intended change.
- The system `uv` executable could not be used in this environment because its
  Snap confinement refused to start; the repository's existing `.venv`
  entrypoints were used instead.
