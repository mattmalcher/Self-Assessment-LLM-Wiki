# Reliability remediation plan

This plan resolves the actionable findings in `codex_review.md`. Historical
tax-year support is deliberately excluded: the project is current-law only.

## Goal

Make the pipeline's success, freshness and coverage claims trustworthy enough
for an experimental current-law Self Assessment wiki. Generated material will
remain unofficial and human review will remain necessary.

## Delivery order

### Phase 1 — make pipeline state truthful

1. **Invalidate composed pages when extract notes change.** Hash the canonical
   selected-note payload, extraction prompt/schema version and extraction model
   as page inputs. Add regression tests proving a changed note makes dependent
   pages stale.

2. **Validate extraction output and repair the cache.** Introduce a strict
   top-level and nested schema, retry validation failures, count only valid
   notes as cached, and re-extract the three known malformed records.

3. **Make partial failures fail visibly.** Return non-zero on any fetch,
   extraction or composition failure by default. Emit a machine-readable run
   summary and offer best-effort behaviour only behind an explicit option.

4. **Reconcile cached state with artifacts.** Restore a missing web-page output
   even when its content hash is cached. Audit every fetched source for its
   expected file or named shared-file section.

### Phase 2 — add deterministic assurance

5. **Add tests and an offline artifact audit.** Cover fetchers, chunking, cache
   propagation, configuration, extract schemas, selectors, generated-page
   structure, citation provenance, status consistency and missing artifacts.
   Run the audit in refresh and Pages workflows.

6. **Validate configuration and constrain paths.** Define schemas for
   `sources.yml` and `pages.yml`; check required fields, enums, IDs, regexes,
   output roots and intentional shared outputs before doing work.

7. **Keep status and navigation synchronized.** Regenerate the report and nav
   after successful extract/compose work, and have CI fail if regeneration
   leaves a diff. Report invalid/failed chunks and the last complete run.

### Phase 3 — make coverage claims defensible

8. **Define page authority requirements and expand sources.** Create a
   source-to-page coverage matrix. Add the missing primary legislation and
   substantive GOV.UK content needed for each page; treat case metadata as a
   listing only unless judgments are mirrored. Block or label pages whose
   required authorities are absent, and report notes excluded by caps.

9. **Implement real GOV.UK conditional caching.** Preserve validators and
   upstream timestamps per document, collection item and manual section so
   unchanged material can be skipped as documented.

### Phase 4 — clean up and release

10. **Resolve documentation and generated-content defects.** Fix the `--bare`
    documentation mismatch, Finance Act schedule attribution, broken anchor,
    fetch-summary count and known `s.122AA` citation typo. Regenerate and review
    affected pages.

## Completion criteria

- Every source, chunk and page failure produces a failing default command and
  is represented in a durable run report.
- All committed extract records pass the strict schema; invalid records are
  never counted as cached.
- Any change to a selected note, its prompt/schema version or extraction model
  makes dependent pages stale.
- Every configured fetched artifact exists and can be reconstructed from a
  warm cache.
- Offline tests and artifact audits run in both GitHub workflows.
- Status and navigation match the manifests and generated files after every
  successful run.
- Each published subject page declares whether its minimum authority set is
  satisfied; missing sources prevent an unqualified completeness claim.
- The documented GOV.UK caching behaviour is covered by tests.
- The current-law-only scope is visible in the repository README, site home
  page and reference-implementation notes.

## Out of scope

- Historical/backdated tax-year calculations.
- Treating generated prose or extracted notes as tax advice.
- Fully automated legal approval; publication still requires human review.
