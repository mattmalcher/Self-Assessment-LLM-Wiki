---
title: Data model notes
---

# Reference implementation: data model notes

**Nothing here is built.** This page is groundwork for a future "head of
duty" reference implementation - a system that can actually compute Self
Assessment obligations (who must file, what's owed, by when, and the
consequences of getting it wrong) - and records what such a system would
need to pull from the sources this wiki mirrors, and where each piece
lives. It's a reading list with structure, not a spec.

A head of duty engine needs each of the following as **queryable facts with
a validity period and a citation**, not as prose. The gap between what this
wiki currently holds (mirrored documents) and what the engine would need
(structured, versioned data extracted from those documents) is the real
scope of that future project.

## 1. Who has the duty (registration/filing triggers)

Who must register for Self Assessment, and who must file a return once
registered.

- **Primary source**: [TMA 1970](../legal-system/primary-legislation/acts/tma-1970.md)
  s.7 (obligation to notify chargeability), s.8 (obligation to file a
  return once given notice).
- **HMRC interpretation**: [SALF manual](../hmrc-publications/policy-and-interpretation/manuals/salf.md)
  (SALF100 overview), [SAM manual](../hmrc-publications/policy-and-interpretation/manuals/sam.md).
- **Customer-facing criteria**: [GOV.UK SA guidance](../hmrc-publications/customer-facing-guidance/govuk-guidance.md)
  ("who must send a tax return" criteria - self-employment income
  threshold, untaxed income, high income child benefit charge, etc).
- **What's needed as data**: a versioned rule set (criteria -> boolean),
  since the threshold criteria themselves change (e.g. the self-employment
  income notification threshold, or MTD for Income Tax phasing-in
  thresholds by tax year).

## 2. Key dates (the calendar)

- Registration deadline (5 October following the tax year).
- Paper filing deadline (31 October) vs online (31 January).
- Payments on account (31 January, 31 July) and the balancing payment
  (31 January).
- **Sources**: TMA 1970 s.8, s.9, s.59A/59B; rendered in plain terms in
  [GOV.UK SA guidance](../hmrc-publications/customer-facing-guidance/govuk-guidance.md)
  and the [SAM manual](../hmrc-publications/policy-and-interpretation/manuals/sam.md).
- **What's needed as data**: dates as a function of tax year (and, for
  in-year registrations, of the "notice to file" date - TMA s.8(1D)), not
  hardcoded calendar dates.

## 3. Enquiry windows and assessment time limits

- Normal enquiry window: 12 months from filing (TMA s.9A).
- Discovery assessment time limits: 4 / 6 / 20 years depending on
  carelessness/deliberate behaviour (TMA s.34, s.36).
- **Sources**: TMA 1970 Part 4/5; [EM manual](../hmrc-publications/policy-and-interpretation/manuals/em.md);
  [ARTG manual](../hmrc-publications/policy-and-interpretation/manuals/artg.md) for what happens after.
- **What's needed as data**: time-limit rules as (trigger event, duration,
  condition) triples, since the duration depends on taxpayer behaviour
  (careless/deliberate/neither) which is itself a determination, not a
  fixed fact.

## 4. Penalties

- Late filing (TMA Sch 55) and late payment (TMA Sch 56) penalty regimes -
  fixed penalties, daily penalties, tax-geared penalties, and reasonable
  excuse.
- The points-based penalty reform for MTD for Income Tax (replacing Sch 55
  for those in scope).
- **Sources**: [CH manual](../hmrc-publications/policy-and-interpretation/manuals/ch.md)
  (the actual penalty calculation logic HMRC applies);
  [Revenue & Customs Briefs](../hmrc-publications/policy-and-interpretation/revenue-and-customs-briefs.md)
  for policy changes in transition.
- **What's needed as data**: penalty amounts and trigger conditions as
  versioned tables (they change by Finance Act), plus the MTD-vs-non-MTD
  branch, since two different regimes now coexist depending on taxpayer
  category and tax year.

## 5. Interest

- Late payment interest and repayment interest rates, tied to the Bank of
  England base rate by a published formula, not a fixed number.
- **Source**: [HMRC rates and allowances](../hmrc-publications/rates-and-allowances.md)
  (published rate history - this is the one place in this wiki that is
  already closest to "data" rather than "document").
- **What's needed as data**: a rate history table (effective date -> rate),
  which `rates-and-allowances.md` already tracks per HMRC's own
  publication cadence - the pipeline could parse this into structured
  values rather than a rendered page, if/when the engine needs it
  programmatically.

## 6. Thresholds and allowances

- Personal allowance, dividend allowance, trading/property allowance
  (£1,000), the £1,000 payments-on-account threshold, Marriage Allowance,
  High Income Child Benefit Charge threshold, etc.
- **Source**: [HMRC rates and allowances](../hmrc-publications/rates-and-allowances.md).
- **What's needed as data**: same as interest rates - a (tax year ->
  value) table per threshold, not prose. This is the most
  "implementation-ready" category already, since HMRC itself publishes it
  as a structured collection.

## 7. Appeals and reviews

- Right to internal review vs direct appeal to tribunal; time limits;
  which tribunal (FTT Tax Chamber) and under what procedure.
- **Sources**: TMA 1970 Part 5; [ARTG manual](../hmrc-publications/policy-and-interpretation/manuals/artg.md);
  [Tribunal Procedure (FTT)(Tax Chamber) Rules 2009](../legal-system/secondary-legislation/statutory-instruments.md).
- **What's needed as data**: a decision-type -> appeal-route mapping (not
  every HMRC decision carries the same appeal rights), plus the review/
  appeal time limits as the same (trigger, duration) structure as time
  limits in §3.

## 8. Case law as an override/interpretation layer

Legislation and HMRC's own manuals are not always the last word - tribunal
and court decisions can narrow, confirm, or occasionally contradict HMRC's
stated interpretation (see the disclaimer at the top of
[Statements of Practice](../hmrc-publications/policy-and-interpretation/statements-of-practice.md):
HMRC's interpretation "does not affect a taxpayer's right to argue for a
different interpretation").

- **Sources**: [Upper Tribunal](../legal-system/case-law/upper-tribunal-tax-chancery.md)
  and [FTT](../legal-system/case-law/first-tier-tribunal-tax-chamber.md)
  decision indexes.
- **What's needed as data**: this is the hardest category to make
  machine-usable - it needs case outcomes linked to the specific statutory
  provision(s) they interpret, which isn't something a feed of case
  titles provides. Realistically this stays a human-curated layer
  (flagging specific leading cases against specific provisions) rather
  than something the pipeline can extract automatically.

## Summary: document mirror vs data model

Everything above falls into two categories:

- **Already close to data** (§5, §6): HMRC publishes rates/allowances/
  thresholds in a structured, versioned way already. A future engine could
  parse `rates-and-allowances.md` (or better, the underlying GOV.UK content
  API response) into a rate table with modest effort.
- **Requires genuine extraction work** (§1-4, §7-8): the rules live in
  prose - legislation, manual guidance, case law - and turning "s.9A(1):
  the officer has notice of enquiry... within 12 months of the filing date"
  into a queryable rule is an interpretation step, not a parsing step. That
  extraction is the actual work of a "head of duty" implementation, and is
  out of scope here.
