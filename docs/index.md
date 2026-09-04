# Self Assessment LLM Wiki

A reference covering the legal and HMRC-publication landscape around UK
**Self Assessment** (Income Tax): the primary and secondary legislation that
creates the obligations, the case law that interprets them, and HMRC's own
policy, guidance, and customer-facing publications that implement them.

It exists to be a single, well-cited place an LLM (or a person) can draw on
when reasoning about Self Assessment — not a restatement in HMRC's or
Parliament's words, but the actual sourced text, kept current.

## Why this exists

Tax obligations for Self Assessment come from several layers that don't
live in one place upstream:

- **Primary legislation** — Acts of Parliament setting the high-level
  obligations (e.g. [Taxes Management Act 1970](legal-system/primary-legislation/acts/tma-1970.md),
  [ITEPA 2003](legal-system/primary-legislation/acts/itepa-2003.md)).
- **Secondary legislation** — Statutory Instruments filling in detail.
- **Case law** — Tribunal and court decisions interpreting both.
- **HMRC policy and interpretation** — manuals, Statements of Practice,
  Revenue & Customs Briefs, and Extra-Statutory Concessions: HMRC's own
  reading of the above, and how it intends to apply it.
- **Customer-facing guidance** — GOV.UK guidance, helpsheets, and tools:
  HMRC's plain-language explanation for taxpayers.

This wiki mirrors all five layers into one searchable, citation-preserving
site, refreshed automatically as sources change. See
[How this wiki stays current](meta/refresh-process.md) for the mechanism,
and [Sources](meta/sources.md) for the full registry of tracked and
registered-but-not-yet-fetched sources.

## Scope note

Coverage is prioritised for **Self Assessment** specifically. Some
collections referenced in the source registry (e.g. the full HMRC manuals
index, VAT notices) are **registered** — tracked so they can be pulled in
cheaply later — without being fully mirrored yet. Pages built from
registered-but-unfetched sources are marked as such.

## Looking ahead: a "head of duty" reference implementation

The eventual goal beyond this wiki is a reference implementation that can
compute Self Assessment obligations directly (who must file, what's owed,
by when, and what happens if it's late or wrong). This wiki is the
groundwork for that — see
[Reference implementation: data model notes](reference-implementation/data-model-notes.md)
for what such a system would need to extract from these sources. That
implementation is **not** started here.

## Not legal advice

This is a research aid. Content is mirrored from primary and official
sources with provenance metadata (source URL, upstream update date, last
checked date) on every page, but interpretation, currency, and correctness
for any specific situation should always be checked against the original
source.
