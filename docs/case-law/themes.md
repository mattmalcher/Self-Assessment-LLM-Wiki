---
title: Case law - what the tribunals are deciding
generated: true
generated_on: '2026-09-09'
generated_by: claude-cli:opus
input_hash: 2166a8a261fb0daa
note_count: 2
sources:
- caselaw-ftt-tc
- caselaw-ut-tcc
---

# Case law - what the tribunals are deciding

!!! danger "Unofficial - not HMRC, not advice, written by an LLM"

    This page is **not** an HMRC publication and has no connection to HMRC or
    any government body. It was **written by a language model** from mirrored
    source material, and can be wrong, incomplete or out of date. It is not
    tax advice. Check every figure, date and rule against the cited source
    before relying on it, and see
    [GOV.UK](https://www.gov.uk/self-assessment-tax-returns) for official
    guidance.

This page describes what the wiki's mirrored tribunal sources actually contain, and — just as importantly — what they do not. The two sources are Atom feed listings of recent First-tier Tribunal (Tax Chamber) and Upper Tribunal (Tax and Chancery Chamber) decisions from Find Case Law. Both are **index pages**: they capture decision metadata (date, neutral citation, case name, link) and no judgment text (caselaw-ftt-tc; caselaw-ut-tcc). Nothing on this page should be read as a statement of the law, and none of it is HMRC material.

## What the two sources are

| Property | First-tier Tribunal (Tax Chamber) | Upper Tribunal (Tax and Chancery Chamber) |
|---|---|---|
| Ref | caselaw-ftt-tc | caselaw-ut-tcc |
| Feed | `caselaw.nationalarchives.gov.uk/atom.xml?tribunal=ukftt/tc` | `caselaw.nationalarchives.gov.uk/atom.xml?tribunal=ukut/tcc` |
| Items captured | 40 most recent decisions | 40 most recent decisions |
| Date span in the mirror | 2026-07-22 to 2026-08-28 | 2026-05-05 to 2026-09-03 |
| Fields per entry | Decision date, neutral citation, case name, link to full judgment | Decision date, neutral citation, case name, link to full judgment |
| Judgment text included? | No | No |

Both feeds are rolling windows of the 40 most recent decisions, and the Upper Tribunal note is explicit that the list "will change as new decisions are issued" (caselaw-ut-tcc). The same is structurally true of the FTT feed, which is described on identical terms as an index of the 40 most recent decisions (caselaw-ftt-tc).

## Why this is not a survey of Self Assessment case law

Three limitations follow directly from the source notes, and they are severe enough to be stated up front.

**1. No holdings, no reasoning.** Neither chunk contains "substantive legal content, reasoning, or holdings" (caselaw-ftt-tc); the Upper Tribunal chunk likewise contains "no judgment content, legal reasoning, or Self Assessment-specific detail" (caselaw-ut-tcc). Any Self Assessment-relevant finding "would require following the individual links" (caselaw-ftt-tc).

**2. No subject-matter filter.** The tribunals hear the full range of tax appeals. The FTT note warns that "case names alone do not indicate whether a decision concerns Self Assessment specifically (some may relate to VAT, PAYE, corporation tax, etc.)" (caselaw-ftt-tc). The Upper Tribunal position is worse: the Tax and Chancery Chamber also hears financial services references, and "some listed cases involve the Financial Conduct Authority rather than HMRC and may not relate to tax at all" (caselaw-ut-tcc). A case name in the form "X v HMRC" is the only tax signal available in the metadata, and it does not identify the tax.

**3. Recency, not precedent.** These are the most recent 40 decisions at the time of retrieval (caselaw-ftt-tc; caselaw-ut-tcc). A recency window is close to the opposite of a precedential survey: the leading authorities on any Self Assessment point are, by definition, older than the window and therefore absent. Nothing here supports a claim that any listed decision is binding, distinguishable, appealed, or followed.

## The decisions the sources list

**First-tier Tribunal.** The mirrored chunk records 40 decisions dated between 2026-07-22 and 2026-08-28, but the note preserved no individual case names, citations or links — only the summary description of the listing and the feed URL (caselaw-ftt-tc). No FTT decision can be named from this source.

**Upper Tribunal.** The mirrored chunk preserved per-decision links for 40 judgments dated between 2026-05-05 and 2026-09-03, but not the associated case names (caselaw-ut-tcc). What survives is the decision identifier embedded in each URL, all of them in the 2026 series:

| # | Decision no. | # | Decision no. | # | Decision no. | # | Decision no. |
|---|---|---|---|---|---|---|---|
| 1 | 343 | 11 | 300 | 21 | 259 | 31 | 217 |
| 2 | 342 | 12 | 290 | 22 | 258 | 32 | 219 |
| 3 | 335 | 13 | 289 | 23 | 256 | 33 | 216 |
| 4 | 333 | 14 | 288 | 24 | 249 | 34 | 213 |
| 5 | 330 | 15 | 285 | 25 | 297 | 35 | 212 |
| 6 | 329 | 16 | 284 | 26 | 246 | 36 | 211 |
| 7 | 324 | 17 | 281 | 27 | 248 | 37 | 195 |
| 8 | 304 | 18 | 282 | 28 | 261 | 38 | 193 |
| 9 | 306 | 19 | 275 | 29 | 227 | 39 | 194 |
| 10 | 305 | 20 | 271 | 30 | 223 | 40 | 173 |

Each resolves to `https://caselaw.nationalarchives.gov.uk/ukut/tcc/2026/<n>` (caselaw-ut-tcc). Because the notes did not carry the case names, these numbers are pointers, not citations to a named party, and none of them can be attributed to a Self Assessment issue without retrieving the judgment.

Two structural observations, drawn from the list itself rather than from any judgment:

- **The list is not in citation-number order.** 304 precedes 306 and 305; 297 sits between 249 and 246; 261 sits between 248 and 227 (caselaw-ut-tcc). The feed is ordered by decision date, and decision numbers are not a reliable proxy for chronology. Sorting a mirror by number will reorder it incorrectly.
- **FTT throughput is much higher.** Forty FTT decisions span about five weeks; forty UT decisions span about four months (caselaw-ftt-tc; caselaw-ut-tcc). A 40-item window is therefore a far shorter memory on the FTT feed.

## Implementable rules

These are derivable from the source structure alone.

| Input | Condition | Result |
|---|---|---|
| A UT (TCC) decision number `n` and year `y` | Always | Judgment URL is `https://caselaw.nationalarchives.gov.uk/ukut/tcc/{y}/{n}` (caselaw-ut-tcc) |
| Mirror timestamp `t`, feed = FTT | `now - t` exceeds roughly five weeks | Assume decisions have fallen out of the 40-item window; a re-fetch will not recover them (caselaw-ftt-tc) |
| Mirror timestamp `t`, feed = UT | `now - t` exceeds roughly four months | Same conclusion for the UT feed (caselaw-ut-tcc) |
| A feed entry | Any entry | Treat "is this Self Assessment?" as unknown; case name is not a subject-matter classifier (caselaw-ftt-tc) |
| A UT feed entry | Respondent is the FCA, not HMRC | Exclude from any tax dataset (caselaw-ut-tcc) |
| Ordering of a mirrored list | Any | Preserve feed order (date); do not sort by decision number (caselaw-ut-tcc) |

A defensible pipeline built on these feeds needs a second stage that fetches each linked judgment and classifies it. The feeds are a discovery mechanism; they are not a dataset of tax holdings.

## Gaps in the sources

The brief for this page asked for the recurring themes in Self Assessment litigation — reasonable excuse, discovery assessments, validity of notices to file, penalty quantum, and late appeals — and for the decisions the sources name. **The supplied notes do not support any of this**, and the gap is total rather than partial:

- **No thematic content.** Neither note records a single issue, ground of appeal, statutory provision, or outcome. There is no material in the sources from which to describe reasonable excuse, discovery, notice validity, penalty quantum or late appeals — as concepts, as trends, or as anything else. Those themes are not mentioned in the notes at all.
- **No case names.** The FTT note captured no citations or names (caselaw-ftt-tc). The UT note captured 40 links but no names (caselaw-ut-tcc). The brief's instruction to "name the decisions the sources actually list" cannot be met: the sources, as mirrored, name none.
- **No FTT decision identifiers.** The FTT chunk yields only a count (40) and a date range (caselaw-ftt-tc).
- **No indication of which listed decisions are tax cases**, let alone income tax or Self Assessment cases (caselaw-ftt-tc; caselaw-ut-tcc).
- **No appellate history, no precedential weight, no statistics** on outcomes, success rates or penalty reductions.
- **No coverage of older or leading authority.** The windows begin at 2026-05-05 (UT) and 2026-07-22 (FTT); anything earlier is outside the mirror.

Filling these gaps requires retrieving the individual judgments from the links, which the mirrored chunks explicitly defer to (caselaw-ftt-tc; caselaw-ut-tcc). Until that is done, this page can only describe the index, not the case law.

---

## Sources used on this page

This page was written by an LLM from structured notes extracted from the mirrored sources below. Always check the upstream source before relying on any figure or deadline.

- [caselaw-ftt-tc](https://caselaw.nationalarchives.gov.uk/atom.xml?tribunal=ukftt/tc) - 1 note(s) - mirrored at `corpus/legal-system/case-law/first-tier-tribunal-tax-chamber.md`
- [caselaw-ut-tcc](https://caselaw.nationalarchives.gov.uk/atom.xml?tribunal=ukut/tcc) - 1 note(s) - mirrored at `corpus/legal-system/case-law/upper-tribunal-tax-chancery.md`
