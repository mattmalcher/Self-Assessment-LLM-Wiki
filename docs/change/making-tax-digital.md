---
title: Making Tax Digital for Income Tax
generated: true
generated_on: '2026-09-09'
generated_by: claude-cli:opus
input_hash: d65b16166f311ff9
note_count: 14
sources:
- hmrc-manual-salf
- hmrc-manual-sam
- sa-helpsheets:5f67cd23-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dbe3-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dd70-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67de13-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67defe-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67e282-7631-11e4-a3cb-005056011aef
---

# Making Tax Digital for Income Tax

!!! danger "Unofficial - not HMRC, not advice, written by an LLM"

    This page is **not** an HMRC publication and has no connection to HMRC or
    any government body. It was **written by a language model** from mirrored
    source material, and can be wrong, incomplete or out of date. It is not
    tax advice. Check every figure, date and rule against the cited source
    before relying on it, and see
    [GOV.UK](https://www.gov.uk/self-assessment-tax-returns) for official
    guidance.

Making Tax Digital for Income Tax (MTD for ITSA) layers a set of digital record-keeping and quarterly reporting obligations on top of the existing Self Assessment framework for some sole traders and landlords. This page sets out what the mirrored sources say about scope, thresholds, the quarterly update cycle, the annual return, exemptions and penalties — drawing mainly on HMRC's Self Assessment Legal Framework manual (SALF) chapters 900–1600 and the Self Assessment manual (SAM). The sources are uneven: SALF is detailed and current, SAM50530 is badly out of date, and several topics the brief asks about are simply not covered. Those gaps are listed at the end.

## Source status — read this first

| Source | Type | Currency |
|---|---|---|
| SALF900–SALF1600 | HMRC internal manual (HMRC's interpretation of TMA 1970 Sch.A1 and the MTD regulations) | Current; reflects the Income Tax (Digital Obligations) Regulations 2026 (SI 2026/336) |
| SAM144001–SAM144030 | HMRC internal manual (operational process for digital exemption) | Current; written around the April 2026 start |
| SAM50530 "Making Tax Digital for Business" | HMRC internal manual | **Superseded** — describes a £10,000 turnover threshold and mandation "from April 2018 / April 2019" (SAM50530), which conflicts with the phased 2026–2028 timetable in SALF910 |
| HS204, HS236, HS325, HS340, HS341 | Customer-facing helpsheets (simplified) | Mention MTD only as a one-line caveat |

The SALF notes themselves warn that the commencement instruments have been repeatedly amended or revoked — SI 2021/1079 was replaced by SI 2024/422 and then SI 2026/356; SI 2021/1076 was amended by SI 2024/167 and then revoked by SI 2026/336 — "so effective dates changed multiple times and readers should check the currently operative instrument" (SALF910 caveats).

## Legal framework

The enabling provisions cited are TMA 1970 s.12C and Schedule A1, Finance (No.2) Act 2017 ss.60–61 and Sch.14, Finance (No.2) Act 2026, and the Income Tax (Digital Obligations) Regulations 2026 (SI 2026/336) (SALF910). The annual return obligation itself remains TMA 1970 s.8(1)(a), with the 31 January filing date unchanged (SALF910).

## Who is in scope

Three concepts stack:

- **Relevant person** — a person carrying on, or who has carried on, a *relevant activity* (SALF910; SALF930).
- **Relevant activity** — any activity giving rise to profits or income chargeable under ITTOIA 2005 Part 2 (trade, profession, vocation) or Part 3 (property business) if the person were UK resident. **Excluded**: partnership activities, charitable/exempt unauthorised unit trust trustee activities, Lloyd's underwriting, REIT share distributions, and OEIC participation (SALF930).
- **Qualifying income** — either the total **gross** amount from all relevant activities included in the return before deductions, or the **net** amount after deductions where no gross figure is required. It excludes trustee receipts, visiting performer payments (ITTOIA 2005 s.13) and qualifying care receipts (ITTOIA 2005 Pt.7 Ch.2). It is adjusted proportionately for periods other than 12 months, and post-notice-to-file amendments that increase income are disregarded if made after the start of the relevant tax year (SALF1450).

### Thresholds and phasing

The test is on qualifying income **two tax years earlier** (Y-2) (SALF1440 caveats).

| Tax year of the return tested | Qualifying amount | Digital obligations begin |
|---|---|---|
| 2024-25 | over £50,000 | 6 April 2026 (SALF910, SALF1440) |
| 2025-26 | over £30,000 | 6 April 2027 (SALF910, SALF1440) |
| 2026-27 and subsequent | over £20,000 | 6 April 2028 (SALF910, SALF1440) |

Two further rules in the notes:

- **Continuity from 2029-30 onwards**: a person once subject to a digital obligation remains subject to it until they have three consecutive years below the qualifying amount (SALF1440 caveats).
- Where the tax year has ended and no notice to file has yet been given, qualifying income depends on whether quarterly updates were required; otherwise qualifying income is treated as zero (SALF1440 caveats).

### Digital start date and digital obligation tax years

Implementable form:

```
digital_start_date:
  inputs: relevant_person_status, activity_start_date, date_notice_to_file_given,
          calendar_quarters_election_in_Y-1
  standard case: 6 April in the tax year following the tax year in which the
                 return obligation first applies (i.e. the year in which the
                 filing date falls)                              [SALF1010]
  if calendar quarters election: may shift to 1 April in the year prior to
                 the relevant tax year                           [SALF910 caveats, SALF1140]

digital_obligation_tax_years:
  = tax years from the year containing digital_start_date
    to the year containing digital_termination_date              [SALF1030]
  exception: if digital_start_date falls on 1 April of a tax year,
             the obligation begins in the FOLLOWING tax year     [SALF1020 caveats]
  exception: if digital_termination_date < digital_start_date,
             there are NO digital obligation tax years           [SALF1020 caveats]
```

The **digital termination date** is the date the relevant activity ended (SALF1020). A relevant person ceasing a relevant activity must notify HMRC of it by the deadline for the quarterly update period in which the activity ceased. SALF1020's worked example: activity ceasing 1 November falls in standard Period 3 (ending 5 January), so notification is due by 7 February. If no termination date is provided, the obligation to give quarterly updates continues (SALF1020 caveats). Notification is not required where the activity ended before the digital start date, or where the person is excluded so no digital obligation applies (SALF1020 caveats).

## The obligations

### Functional compatible software

**Functional compatible software (FCS)** is a program, or set of programs, that enables a relevant person to meet their tax obligations by interacting with HMRC via the API platform (SALF1110). For a digital obligation tax year, FCS must be used to: keep and correct digital records, send quarterly updates and corrections, and **deliver the return in response to a notice to file under TMA 1970 s.8** (SALF1110). Using FCS to notify amendments to an already-filed return is optional (SALF1020 caveats).

HMRC's stated position is that a return submitted through any other channel for a digital obligation tax year "would not be a valid return as the FCS element of the legal requirement would not be met"; the filing obligation would remain and a penalty for failure to make a return may arise (SALF1110).

### Digital records

A relevant person must keep digital records for each digital obligation tax year using FCS (SALF1200). Retention deadlines per SALF1200: for records feeding quarterly updates, no later than the date the update is given or required, whichever is earlier; for other records, no later than the date the return is delivered or required, whichever is earlier.

### Quarterly updates

A quarterly update is a **cumulative** submission sent via FCS for **each** relevant activity, containing specified information relevant to calculating profits, losses or income (SALF1120; SALF1130). Each period runs from the *relevant start date*, not from the start of the quarter.

**Standard update periods** (no calendar quarters election). Relevant start date = 1 April of tax year Y-1 if a calendar quarters election had effect in Y-1, otherwise 6 April of tax year Y (SALF1150).

| Period | Period end | Deadline |
|---|---|---|
| 1 | 5 July (Y) | 7 August (Y) |
| 2 | 5 October (Y) | 7 November (Y) |
| 3 | 5 January (Y) | 7 February (Y) |
| 4 | 5 April (Y) | 7 May (Y+1) |

*(SALF1150 Table 1)*

**Calendar quarters** (election in force). Relevant start date = 6 April in tax year Y if quarterly updates were required in Y-1 with no election in place that year; otherwise 1 April in tax year Y-1 (SALF1160).

| Period | Period end | Deadline |
|---|---|---|
| 1 | 30 June (Y) | 7 August (Y) |
| 2 | 30 September (Y) | 7 November (Y) |
| 3 | 31 December (Y) | 7 February (Y) |
| 4 | 31 March (end of Y) | 7 May (Y+1) |

*(SALF1160 Table 2)*

The quarterly update period containing the digital termination date ends with that date, shortening the final period (SALF1020 caveats).

The **calendar quarters election** must be notified to HMRC before any quarterly update for that year is submitted; it applies to the year made and continues for later years unless withdrawn (SALF1140).

### Corrections

| Error relates to | Correction deadline |
|---|---|
| Quarterly updates 1–3 / digital records generally | By the day the next quarterly update is required to be given (SALF1300) |
| Fourth quarterly update, or the period containing the digital termination date | No later than the filing date for the return for that digital obligation tax year (SALF1300) |

Corrections must be made using FCS (SALF1300).

### The annual return

SALF910 frames the year-end step as using MTD-compatible software to "submit tax return", with the return due 31 January following the tax year (SALF910; TMA 1970 s.8(1)(a)). The helpsheets add that claims and adjustments that would otherwise go in SA return boxes are instead made through compatible software — see, e.g., HS341 (EIS relief, normally SA101 box 2 and TR 7 box 19), HS340 (qualifying loan interest, SA101 box 5), HS204 (limit on Income Tax reliefs), HS325 (other taxable income) and HS345 (pension savings tax charges).

The phrase "final declaration" does **not** appear in the supplied notes. The only analogous term is SAM50530's "annual declaration", due at the earliest of 31 January or 10 months after the end of the accounting period — but that page is part of the superseded April 2018/2019 rollout description and its 10-month rule is not corroborated anywhere else in the notes.

## Exemptions and exclusions

SALF1410 groups the grounds into: exclusion; income-amount-based; activity-description-based; person-description-based; claim/chargeability-based; and temporary exemptions for 2026-27. Some are automatic, some require application; some are permanent, some temporary ("until April 2027 at the earliest") (SALF1410).

| Ground | Detail | Ref |
|---|---|---|
| Digital exclusion | Religious society membership, practical inability, or identity verification problems; requires writing to HMRC to apply. HMRC must issue an **exclusion notice** stating the start date and any cessation date. HMRC anticipates it "will be rare" for the conditions to be met | SALF1420, SALF1430 |
| Qualifying income below the qualifying amount | £50,000 / £30,000 / £20,000 per the table above | SALF1440 |
| Activity description | Trustees (including executors/administrators liable under TMA 1970 s.74(1)), visiting performers (ITTOIA 2005 s.13), qualifying care receipts (ITTOIA 2005 Pt.7 Ch.2) — notice to HMRC required | SALF930, SALF1460 |
| Overseas activity of a new non-resident | Activity carried on wholly outside the UK (or the outside-UK part); "new non-resident" = resident in Y-2 but not resident, or reasonably expecting not to be, in Y, having notified HMRC | SALF1470 |
| Person description | Donors under powers of attorney (Mental Capacity Act 2005 s.9(1)/Sch.4/s.16(2)(b); Adults with Incapacity (Scotland) Act 2000 ss.15(1), 16(1), 58(1); Enduring Powers of Attorney (NI) Order 1987 art.4(1); Mental Health (NI) Order 1986 art.101(1)), ministers of religion, Lloyd's underwriters, persons without a National Insurance number | SALF1480 |
| Claim / chargeability | Entitlement to marriage allowance (ITA 2007 ss.45(1), 46(1)) or blind person's allowance (ITA 2007 ss.38(1), 39(2)), or company status | SALF1500 |
| Temporary (2026-27) | Trust/settlement/estate income, visiting performers, qualifying care providers, farmers' and creative artists' averaging claims; non-residence, split year, non-resident personal allowance claims, dual residence, remittance basis, new-resident reliefs, temporary repatriation facility | SALF1510, SALF1520 |

Notes on operation:

- Where a person-description exemption applies, any obligation that has arisen "is treated as never having arisen" (SALF1460 area / SALF1500). The same retrospective effect applies where entitlement to a listed allowance arises after a digital obligation has already arisen for year Y (SALF1500).
- Person-description exemptions fail if the power of attorney has been revoked or ended, or (in certain circumstances) if the donor is still capable of providing financial information to HMRC (SALF1440 caveats).
- A person who gave an exclusion notice without an end date must give a further notice within 3 months of first having reason to believe they ceased to be excluded (SALF1430).
- The Commissioners have a power to create further exemptions, which "has not currently been exercised" (SALF1530).
- HS236 states that qualifying care receipt customers are exempt from MTD for Income Tax specifically for 2026-27; the helpsheet's own caveat notes this "may not extend to other years without further confirmation".

### Easements

SALF1020's caveats record that easements exist for jointly let property, turnover below the VAT registration threshold, and retailers, "per Gov.uk website" — but the notes do not contain their content.

## Applying for a digital exemption (HMRC process)

SAM144001 defines **Digital Exemption** as an exemption granted where a customer is *digitally excluded* — where it is not reasonable, due to personal circumstances, to use compatible software. SAM144010 gives examples: age, health condition or disability, religious beliefs, lack of suitable internet access. SAM142050's caveats record that the criteria explicitly exclude, as sole grounds: previously filing a paper return, unfamiliarity with software, a small number of records, and extra time or cost.

| Step | Rule | Ref |
|---|---|---|
| Who applies | The customer, an authorised agent (per client, on that client's personal circumstances), or a friend/family member with prior authorisation (written and signed, or verbal by phone) | SAM144020 |
| Information required | National Insurance number, name and address, and explanation of why exemption is thought to apply, plus additional information if digitally excluded; third-party applicants also give their connection to the applicant | SAM144020 |
| Timing by cohort | 2026 cohort: can apply now. 2027 cohort: from summer 2026. 2028 cohort: from summer 2027 | SAM144020 |
| HMRC response | HMRC aims to respond within 28 calendar days (longer if more information is needed) | SAM144030 |
| Effect of decision | A decision received **before** 1 April 2026 takes legal effect only **from** 1 April 2026 | SAM144030 |
| Appeal — decision before 1 Apr 2026 | Appeal by 30 April 2026, in writing, with new information. HMRC's review of pre-1 April 2026 letters and appeals will not start until 1 April 2026 | SAM144030 |
| Appeal — decision on/after 1 Apr 2026 | Up to 30 days after the date on the letter | SAM144030 |
| Statutory appeal route | Against HMRC decisions under TMA 1970 Sch.A1 regulations: written notice of appeal specifying grounds, within 30 days after the day notice of the decision is given | SALF950 |
| While awaiting a decision | A customer already signed up whose circumstances change must apply and continue using MTD ITSA meanwhile | SAM144030 |
| Voluntary sign-ups | A voluntary participant who believes they have become exempt opts out via their HMRC online services account | SAM144030 |
| VAT carry-over | A VAT digital-exclusion exemption carries over automatically only if circumstances have not changed; otherwise a fresh application is needed. A VAT exemption granted because of an **insolvency** procedure does **not** extend to MTD ITSA | SAM144020 |

A customer granted Digital Exemption remains within Self Assessment and files annual returns, reporting income and gains through the SA return, until they notify HMRC they are no longer exempt (SAM144001). Temporary exemptions still require sign-up once qualifying income exceeds the relevant threshold (SAM144020 caveats).

## Penalties

| Trigger | Consequence | Ref |
|---|---|---|
| Failure to comply with the digital record-keeping requirements in the regulations | Penalty up to £3,000 — **not** charged if a penalty is already charged under TMA 1970 s.12B(5) for the same period | SALF1200 |
| Submitting a return for a digital obligation tax year otherwise than via FCS | Return is not valid; filing obligation remains and a penalty for failure to make a return may arise | SALF1110 |
| MTD **volunteer** misses a "late" quarterly update | No penalty — none of the statutory MTD obligations apply to volunteers | SALF1630 |
| MTD volunteer misses the tax return deadline | Penalty still charged; that deadline is not created by MTD legislation | SALF1630 |
| Being exempt from MTD ITSA during 2026-27 | Customer stays on the existing SA late filing and late payment penalties, not any MTD-specific regime | SAM144030 |

## Volunteers, identity verification and notices

**MTD volunteers** (formerly "participants") are customers who sign up before being required to; the earliest year available was 2024-25 (SALF1630). SALF1630's example refers to someone with obligations commencing 6 April 2027 volunteering for 2026-27.

SALF1610 requires relevant persons subject to digital obligations to meet identity verification conditions set by Commissioners' direction. SALF1620 provides that where the regulations require or permit a notice, it must be given in the form and by the method specified by direction, with any specified evidence, within any specified timeframe; where the regulations set no time, the direction may.

## How this changes obligations described elsewhere in this wiki

- **The return deadline is unchanged.** 31 January following the tax year for electronic returns, 31 October for paper (SALF100); the MTD chapter restates 31 January for returns required by s.8(1)(a) (SALF910). What changes is the *channel*: FCS becomes mandatory (SALF1110).
- **Payments on account are unaffected** — the first payment on account on 31 January in the tax year, the second on 31 July following, and the balancing payment on 31 January following the end of the tax year (SALF100) continue. SAM50530 states payments on account are unaffected by MTD, although that page is otherwise superseded.
- **Box-based claims move into software.** HS204, HS236, HS325, HS340, HS341 and HS345 each carry a caveat that MTD users make claims and adjustments through compatible software instead of the SA boxes those helpsheets describe (e.g. HS341 on SA101 box 2 / TR 7 box 19; HS340 on SA101 box 5; HS345 on SA101 page Ai 4 boxes 10–12). The substantive rules in those helpsheets — the £50,000 / 25% of adjusted total income relief cap (HS204 s.1.1), the £2m / £1m EIS limits and 30% relief rate (HS341 s.2, s.6), the £1,000 trading and miscellaneous income allowance (HS325), the £60,000 annual allowance (HS345) — are not changed by MTD in these sources.
- **Partnerships are out for now.** MTD for Income Tax "does not yet apply to partnerships; HMRC will set a future timeline" (SALF910 caveats), and partnership activities are excluded from the definition of relevant activity (SALF930).
- **Notification duties are unchanged** in the notes: 5 October following the end of the tax year for untaxed income or a capital gain where no notice to file is issued, and notification of new self-employment on starting or within three months for NI purposes (SALF100).

## Conflicts between sources

**SAM50530 vs SALF910.** SAM50530 describes MTDfB mandation from April 2018 for turnover above the VAT registration threshold and April 2019 for turnover below it but above £10,000, with at least 3-monthly summary updates and an annual declaration due at the earlier of 31 January or 10 months after the accounting period end. SALF910 and SALF1440 describe mandation from 6 April 2026/2027/2028 keyed to qualifying income over £50,000/£30,000/£20,000 in year Y-2. SAM50530's own caveat concedes its "functionality and thresholds described reflect the rollout as at the time of writing and may have been superseded by later legislative changes not covered in this chunk". Treat SALF as the operative description; SAM50530's £10,000 figure, April 2018/2019 dates and 10-month declaration rule should not be relied on.

## Gaps in the sources

The notes do not cover, and this page therefore does not state:

1. **The term "final declaration"** and its statutory basis, content or deadline. Only SALF910's reference to submitting the s.8(1)(a) return via FCS and SAM50530's superseded "annual declaration" are available.
2. **What a quarterly update actually contains.** SALF1120/1130 say "specified information relevant to calculating profits, losses or income" — the specified categories, totals and any required breakdown are not in the notes.
3. **MTD-specific late submission and late payment penalties.** No points-based or percentage-based MTD penalty tiers appear. SALF1500 cross-refers to the Compliance Handbook "penalties and penalty reform" but no figures are supplied. The only quantified MTD penalty in the notes is the up-to-£3,000 record-keeping penalty (SALF1200).
4. **The content of the easements** for jointly let property, sub-VAT-threshold turnover and retailers (referenced but not described at SALF1020).
5. **End-of-period statements**, adjustments, accounting-period-to-tax-year alignment, and how cumulative quarterly figures reconcile to the final return.
6. **Retail/agent mechanics**: the Agent Services Account and agent reference number are defined at SAM50530 but only in the superseded MTDfB context.
7. **Thresholds and start dates beyond 2028**, other than the three-consecutive-years continuity rule (SALF1440 caveats).
8. **Whether the 2026-27 temporary exemptions (SALF1510, SALF1520) are extended** — the notes say only "until April 2027 at the earliest" (SALF1410).

---

## Sources used on this page

This page was written by an LLM from structured notes extracted from the mirrored sources below. Always check the upstream source before relying on any figure or deadline.

- [sa-helpsheets:5f67de13-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/enterprise-investment-scheme-income-tax-relief-hs341-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/enterprise-investment-scheme-income-tax-relief-self-assessment-helpsheet-hs341.md`
- [sa-helpsheets:5f67dd70-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/interest-and-alternative-finance-payments-eligible-for-relief-on-qualifying-loans-and-alternative-finance-arrangements-hs340-self-assessment-helpshee) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/interest-and-alternative-finance-payments-eligible-for-relief-on-qualifying-loans-and-alternative-finance-arrangements-self-assessment-helpsheet-hs340.md`
- [sa-helpsheets:5f67e282-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/limit-on-income-tax-reliefs-hs204-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/limit-on-income-tax-reliefs-self-assessment-helpsheet-hs204.md`
- [sa-helpsheets:5f67dbe3-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/other-taxable-income-hs325-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/other-taxable-income-for-self-assessment-helpsheet-hs325.md`
- [sa-helpsheets:5f67defe-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/pensions-tax-charges-on-any-excess-over-the-lifetime-allowance-annual-allowance-special-annual-allowance-and-on-unauthorised-payments-hs345-self) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/pension-savings-tax-charges-self-assessment-helpsheet-hs345.md`
- [sa-helpsheets:5f67cd23-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/qualifying-care-relief-foster-carers-adult-placement-carers-kinship-carers-and-staying-put-carers-hs236-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/qualifying-care-relief-for-carers-self-assessment-helpsheet-hs236.md`
- [hmrc-manual-salf](https://www.gov.uk/hmrc-internal-manuals/self-assessment-legal-framework) - 5 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/salf.md`
- [hmrc-manual-sam](https://www.gov.uk/hmrc-internal-manuals/self-assessment-manual) - 3 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/sam.md`
