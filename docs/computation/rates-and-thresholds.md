---
title: Rates, allowances and thresholds
generated: true
generated_on: '2026-09-09'
generated_by: claude-cli:opus
input_hash: 076cc4e278dc88db
note_count: 80
sources:
- hmrc-manual-ch
- hmrc-manual-em
- hmrc-manual-salf
- hmrc-manual-sam
- itepa-2003
- sa-helpsheets:5f67ceae-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67d29a-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67d46f-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67db85-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dcd2-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67defe-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67e2d6-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67e327-7631-11e4-a3cb-005056011aef
- sa-helpsheets:f689f4a2-7da1-41a3-b37d-b18c346219ed
- tma-1970
---

# Rates, allowances and thresholds

!!! danger "Unofficial - not HMRC, not advice, written by an LLM"

    This page is **not** an HMRC publication and has no connection to HMRC or
    any government body. It was **written by a language model** from mirrored
    source material, and can be wrong, incomplete or out of date. It is not
    tax advice. Check every figure, date and rule against the cited source
    before relying on it, and see
    [GOV.UK](https://www.gov.uk/self-assessment-tax-returns) for official
    guidance.

This page collects every rate, allowance, threshold and monetary limit that appears in the mirrored source set for UK Self Assessment, keyed by tax year where the source states one. It covers filing- and payment-related thresholds, penalty tiers, relief limits and registration thresholds. Many of the "headline" figures an implementer would expect — income tax bands, the personal allowance for most years, the CGT annual exempt amount, NIC rates — are **not stated in these sources**; where that is so, it is flagged rather than filled in. Nothing here is HMRC's own publication; HMRC manual and helpsheet positions are attributed as HMRC's view.

---

## 1. What the sources do and do not give

The mirrored set is dominated by procedural material (Taxes Management Act 1970, the Self Assessment Legal Framework manual, the Self Assessment manual, the Compliance Handbook, the Enquiry Manual) plus a scattering of Self Assessment helpsheets. Procedural manuals state penalty amounts and administrative thresholds precisely; they do not tabulate tax rates.

Consequently:

- **Penalty and administrative thresholds are well covered** and are given below with the tax years to which the sources say they apply.
- **Income tax rates and bands, NIC rates and limits, and most allowances are absent.** The sources do not point at a live GOV.UK rates page either — there is no "Income Tax rates and Personal Allowances" URL in the note set. See §9.
- Several figures appear **with no tax year attached at all**. These are collected in §8 and must not be assumed to be current.

---

## 2. Allowances and reliefs with a stated tax year

| Figure | Value | Tax year(s) as stated | Source | Source type |
|---|---|---|---|---|
| Personal allowance (used in a worked example) | £12,570 | 2024-25 and 2025-26 | HS286 Example 6 | Helpsheet (customer-facing) |
| Pensions: standard annual allowance | £60,000 | 2025-26 | HS345 – Your annual allowance for 2025 to 2026 | Helpsheet |
| Pensions: money purchase annual allowance | £10,000 | 2025-26 | HS345 – Flexi-accessed but no high income | Helpsheet |
| Pensions: alternative annual allowance | £50,000 | 2025-26 | HS345 – Flexi-accessed but no high income | Helpsheet |
| Pensions: adjusted income threshold for tapering | £260,000 | 2025-26 | HS345 – Your annual allowance for 2025 to 2026 | Helpsheet |
| Pensions: taper rate | £1 reduction per £2 of adjusted income above £260,000 | 2025-26 | HS345 – High income but not flexi-accessed | Helpsheet |
| Pensions: minimum tapered annual allowance | £10,000 | 2025-26 | HS345 – High income but not flexi-accessed | Helpsheet |
| Pensions: carry-forward window for unused annual allowance | previous 3 tax years | not year-specific | HS345 | Helpsheet |
| SEIS: maximum subscription attracting Income Tax relief | £200,000 | 2025-26 | HS393 s.1.2 / s.1.6 | Helpsheet |
| SEIS: Income Tax relief rate | 50% | 2025-26 | HS393 s.1.6 | Helpsheet |
| SEIS: maximum subscription for carry-back to previous year | £100,000 | 2024-25 | HS393 s.1.6 | Helpsheet |
| SEIS: reinvestment relief — proportion of gain exempt | 50% | 2025-26 | HS393 s.2.1 / s.2.2 | Helpsheet |
| SEIS: reinvestment relief — maximum exempt gain | £100,000 | 2025-26 | HS393 s.2.2 | Helpsheet |
| SEIS: "substantial interest" test | more than 30% of share capital, voting power, or winding-up entitlement | not year-specific | HS393 s.1.3 | Helpsheet |
| CGT rate for personal representatives and trustees | 24% | disposals on or after 30 October 2024 | HS282 s.9 | Helpsheet |
| CGT annual exempt amount available to personal representatives | full AEA for the period from death to the following 5 April, and for each of the 2 following tax years; none thereafter | not year-specific (the AEA *amount* is not given) | HS282 s.8 | Helpsheet |

Note the important gap in the last row: HS282 tells you *how many* annual exempt amounts personal representatives get, but the sources nowhere state the *value* of the CGT annual exempt amount for any year.

HS345 explicitly caveats that its figures "apply specifically to tax year 2025 to 2026 and may differ for other years" (HS345 caveats). HS393 states it applies to shares issued in the year ended 5 April 2026 and that its figures are specific to 2025-26 and 2024-25.

### Loss of allowances under the FIG regime

Making a claim under the foreign income and gains regime (in force from 6 April 2025, replacing the remittance basis) costs the claimant the personal allowance, the CGT annual exempt amount, blind person's allowance and marriage-related tax reductions — regardless of whether the claim is for income only, gains only, or Overseas Workday Relief only (HS266, caveats and summary). Relieved foreign income is disregarded when computing adjusted net income (HS266 s.5.3).

---

## 3. Thresholds that trigger a Self Assessment obligation

These come from HMRC's internal Self Assessment manual (SAM100060) and are HMRC's operational criteria for whether an SA record is required — not, in themselves, statute. The statutory obligation is to notify chargeability under TMA 1970 s.7 by 5 October following the end of the tax year (CH manual, "Failing to notify").

| Trigger | Threshold | Tax years as stated | Ref |
|---|---|---|---|
| Untaxed income, with a tax liability | £2,500 or more | all years (State Pension cases only up to 2015-16; from 2016-17 handled under PAYE) | SAM100060 |
| Property letting — gross income | more than £10,000 | all years | SAM100060 |
| Property letting — net income | more than £2,500 | all years | SAM100060 |
| Savings/investment income (tax deducted) | £10,000 or more before tax | up to 2015-16 and 2016-17 onwards | SAM100060 |
| Dividend income | £10,000 or more before tax | 2016-17 onwards | SAM100060 |
| EIS/SEIS relief claimed | £10,000 or more | not year-specific | SAM100060 |
| Trading Income Allowance — turnover below which SA registration not usually needed | £1,000 | 2017-18 onwards | SAM100060 |
| Property Income Allowance — turnover below which SA registration not usually needed | £1,000 | 2017-18 onwards | SAM100060 |
| Chargeable event gain on a life policy (foreign), plus other savings/investment income, requiring registration | more than £10,000 | not year-specific | HS321 s.6.1 |
| Chargeable event gain on a UK policy, plus savings/investment income, requiring registration | more than £10,000 | not year-specific | HS320 s.6.1 |

Machine-implementable form for the last two: `if (chargeable_event_gain + other_savings_and_investment_income) > 10000 then register_for_SA else notify_by_certificate_route` (HS321 s.6.1; HS320 s.6.1).

SAM100060 carries several caveats worth reproducing: the reduced-age-allowance criterion was withdrawn from May 2013; the High Income Child Benefit Charge has been SA criteria since 2012-13, but from 2024-25 only where the customer chooses **not** to pay via PAYE; and a non-resident landlord reclaiming tax under the NRL scheme must register even if within the £1,000 Property Income Allowance.

---

## 4. Making Tax Digital for Income Tax: qualifying amounts

Stated in SALF1440, keyed to the tax year, with the obligation determined by qualifying income two tax years earlier (Y-2):

| Tax year | Qualifying amount | Ref |
|---|---|---|
| 2024-25 | £50,000 | SALF1440 |
| 2025-26 | £30,000 | SALF1440 |
| 2026-27 and subsequent | £20,000 | SALF1440 |

SALF1420–1480 add: phased introduction dates are April 2026, 2027 and 2028; from 2029-30 a person already subject to the digital obligation stays subject to it until three consecutive years below the qualifying amount; and qualifying income excludes trustee receipts, visiting performer payments (ITTOIA 2005 s.13) and qualifying care receipts (ITTOIA 2005 Pt 7 Ch 2), adjusted proportionately for periods other than 12 months.

Implementation sketch: `obligation(Y) = qualifying_income(Y-2) > qualifying_amount(Y)`, subject to exemption and digital-exclusion notices.

---

## 5. Administrative thresholds keyed to a tax year

| Figure | Value | Tax year(s) | Ref |
|---|---|---|---|
| Three-line account / Standard Accounts Information turnover threshold (aligned to VAT threshold) | £79,000 | 2013-14 | SAM122130 |
| " | £81,000 | 2014-15 | SAM122130 |
| " | £82,000 | 2015-16 | SAM122130 |
| " | £83,000 | 2016-17 | SAM122130 |
| " | £85,000 | 2017-18 to 2023-24 | SAM122130 |
| " | £90,000 | 2024-25 onwards | SAM122130 |
| Short Tax Return (SA200) exclusion — self-employment turnover | £90,000 | 2024-25 onwards | SAM121030 |
| Short Tax Return (SA200) exclusion — land and property turnover | £90,000 | 2024-25 onwards | SAM121030 |
| Class 2 NIC: profits threshold for contributions treated as paid | £7,105 a year | not stated; SAM121665 flags this as historical, reference only | SAM121665 |

On Class 2: SAM121665 records that mandatory Class 2 NI was abolished with effect from 6 April 2024 following the Autumn Statement of 22 November 2023, so the £7,105 figure and its mechanics are historical. From 2015-16 to 2023-24 Class 2 formed part of the SA balancing payment but was excluded from payments on account (SAM1001; SAM61250).

Note the tension in the SA200 turnover figures: SAM120020 (a different page of the same manual) gives £90,000 as the self-employment and land-and-property exclusion thresholds without stating a tax year, while SAM121030 gives £90,000 for 2024-25 onwards. SAM120020 also warns its box references relate to the 2014-15 SA100.

---

## 6. Penalty amounts and tiers

### 6.1 Late filing — 2010-11 and later (Schedule 55 FA 2009)

| Stage | Amount | Trigger | Ref |
|---|---|---|---|
| Initial fixed penalty | £100 (£100 per partner for a partnership return) | Return not filed by the due date | SAM61220; CH62020 |
| Daily penalties | £10 per day, maximum 90 days (max £900) | Return still unfiled 3 months after the due date | SAM61281; SAM "Late Filing Daily Penalties"; CH62020 |
| 6-month penalty | greater of £300 and 5% of tax due | Return still unfiled 6 months after the due date | SAM "Late Filing Tax Geared Penalties"; CH62020 |
| 12-month penalty | greater of £300 and 5% of tax due; rising to 70% or 100% for deliberate failure | Return still unfiled 12 months after the due date | SAM "Late Filing Tax Geared Penalties"; CH62020 |

The £100 fixed penalty is not reduced even where there is no tax liability or a refund is due (SAM61220). The system will not reduce a tax-geared late filing penalty below the statutory minimum of £300 (SAM, "Events impacting late filing penalties"). Combined 6- and 12-month tax-geared penalties are capped at 100% of the duty by Sch 55 FA 2009, requiring manual adjustment in NPPS where they would exceed 95% of the liability after the automatic 5% deduction (CH403322; CH404300; CH404475).

### 6.2 Late filing — 2009-10 and earlier (s.93 / s.93A TMA 1970)

| Stage | Individual/trustee | Partnership | Ref |
|---|---|---|---|
| Initial fixed penalty | £100 | £100 per partner | TMA 1970 s.93(2); s.93A(2) |
| Further fixed penalty at 6 months | £100 (total £200) | £100 per partner | TMA 1970 s.93(4); s.93A(4) |
| Daily penalty (tribunal leave) | — | up to £60 per relevant partner per day | TMA 1970 s.93A(3) |
| Tax-geared penalty (12+ months late) | up to 100% of tax unpaid at the filing date, subject to abatement | not applicable to partnership returns | SAM61110 |

Fixed penalties under s.93 could not exceed the tax liability for the year, or the amount outstanding at the filing date (TMA 1970 s.93(7); SALF208) — a cap SAM61060 calls "capping", with a worked example reducing a £200 penalty to £80. SALF506 notes there is **no** equivalent restriction for partnership fixed penalties where the tax on partnership profits is minimal.

### 6.3 Late payment — 2010-11 onwards (Schedule 56 FA 2009)

| Stage | Amount | Trigger | Ref |
|---|---|---|---|
| First | 5% of tax unpaid | more than 30 days after the due date for the balancing payment | Sch 56 FA 2009 para 3(2); SAM61250 |
| Second | 5% of tax unpaid | 5 months after the penalty date | Sch 56 FA 2009 para 3(3); SAM61250 |
| Third | 5% of tax unpaid | 11 months after the penalty date | Sch 56 FA 2009 para 3(4); SAM61250 |

SALF308A gives a worked example (Abigail, 2011-12): three penalties of £187.50 each, being £3,750 at 5%. SAM61250 gives another (2010-11): a £5,000 balancing payment producing a £250 30-day penalty. Late payment penalties apply to balancing payments, determinations, amendments and revenue assessments — **not** to interest, late filing penalties, or payments on account (SAM61250).

### 6.4 Late payment — 2009-10 and earlier (surcharges, s.59C TMA 1970)

| Stage | Amount | Trigger | Ref |
|---|---|---|---|
| First surcharge | 5% of tax/NICs unpaid | 28 days after the due date | TMA 1970 s.59C(2) |
| Second surcharge | 5% of tax/NICs unpaid | 6 months after the due date | TMA 1970 s.59C(3) |

Surcharges applied only to 1996-97 to 2009-10 and never to 1995-96 or earlier, even where assessed now under s.29 or s.36 (EM, "Contract Settlements"). They were replaced by Sch 56 FA 2009 late payment penalties for balancing payments due on or after 31 January 2012 (CH404300). A surcharge and a tax-geared penalty cannot both apply to the same tax (TMA 1970 s.59C(4)).

### 6.5 PAYE/CIS employer default penalties (Schedule 56 FA 2009)

Included for completeness; these sit outside SA but share the Sch 56 architecture.

| Defaults in the tax year | Penalty rate on the tax in that default |
|---|---|
| 1–3 | 1% |
| 4–6 | 2% |
| 7–9 | 3% |
| 10–11 | 4% |

Source: CH152550. Plus 5% of tax unpaid 6 months after the penalty date and a further 5% at 12 months (CH152600). The first failure in a tax year is not a "default" and attracts no default penalty, but can still attract the 6- and 12-month penalties (CH152450). A shortfall of £100 or less is treated as payment of the full amount (CH152450).

---

## 7. Offshore penalty percentage ranges

HMRC's Compliance Handbook categorises overseas territories 1, 2 and 3 by Treasury Order; any territory not listed in category 1 or 3 falls into category 2 (CH112400; CH114400). Category is fixed as at the date of the failure, not the current date.

### 7.1 Failure to file — 12-month further penalty maxima (CH112600)

| Behaviour | Cat 1 | Cat 2 | Cat 3 |
|---|---|---|---|
| Deliberate and concealed | 100% | 150% | 200% |
| Deliberate not concealed | 70% | 105% | 140% |
| Any other case | 5% | 5% | 5% |

Minimum penalty for a 12-month offshore-matter failure: £300 (CH112700).

### 7.2 Failure to file — full ranges (CH112700)

| Category / behaviour / disclosure | Up to and incl. 2015-16 | 2016-17 and later |
|---|---|---|
| Cat 1 deliberate, unprompted | 20%–70% | 30%–70% |
| Cat 1 deliberate, prompted | 35%–70% | 45%–70% |
| Cat 1 del. & concealed, unprompted | 30%–100% | 40%–100% |
| Cat 1 del. & concealed, prompted | 50%–100% | 60%–100% |
| Cat 2 deliberate, unprompted | 30%–105% | 40%–105% |
| Cat 2 deliberate, prompted | 52.5%–105% | 62.5%–105% |
| Cat 2 del. & concealed, unprompted | 45%–150% | 55%–150% |
| Cat 2 del. & concealed, prompted | 75%–150% | 85%–150% |
| Cat 3 deliberate, unprompted | 40%–140% | 50%–140% |
| Cat 3 deliberate, prompted | 70%–140% | 80%–140% |
| Cat 3 del. & concealed, unprompted | 60%–200% | 70%–200% |
| Cat 3 del. & concealed, prompted | 100%–200% | 110%–200% |

### 7.3 Inaccuracy penalties — offshore ranges (CH116600)

| Category / behaviour / disclosure | Up to and incl. 2015-16 | 2016-17 and later |
|---|---|---|
| Cat 1 careless, unprompted | 0%–30% | 0%–30% |
| Cat 1 careless, prompted | 15%–30% | 15%–30% |
| Cat 1 deliberate, unprompted | 20%–70% | 30%–70% |
| Cat 1 deliberate, prompted | 35%–70% | 45%–70% |
| Cat 1 del. & concealed, unprompted | 30%–100% | 40%–100% |
| Cat 1 del. & concealed, prompted | 50%–100% | 60%–100% |
| Cat 2 careless, unprompted | 0%–45% | 0%–45% |
| Cat 2 careless, prompted | 22.5%–45% | 22.5%–45% |
| Cat 2 deliberate, unprompted | 30%–105% | 40%–105% |
| Cat 2 deliberate, prompted | 52.5%–105% | 62.5%–105% |
| Cat 2 del. & concealed, unprompted | 45%–150% | 55%–150% |
| Cat 2 del. & concealed, prompted | 75%–150% | 85%–150% |
| Cat 3 careless, unprompted | 0%–60% | 0%–60% |
| Cat 3 careless, prompted | 30%–60% | 30%–60% |
| Cat 3 deliberate, unprompted | 40%–140% | 50%–140% |
| Cat 3 deliberate, prompted | 70%–140% | 80%–140% |
| Cat 3 del. & concealed, unprompted | 60%–200% | 70%–200% |
| Cat 3 del. & concealed, prompted | 100%–200% | 110%–200% |

### 7.4 Failure to notify — offshore ranges (CH114600, selected)

Category 1 non-deliberate, unprompted within 12 months: 0%–30% (both periods). Category 1 deliberate & concealed, prompted: 50%–100% up to 2015-16, 60%–100% from 2016-17. Category 2 equivalent: 75%–150% then 85%–150%. Category 3 equivalent: 100%–200% then 110%–200%. CH114600 notes minimum penalties for deliberate and deliberate-and-concealed behaviours rose by 10 percentage points from 2016-17 by virtue of Schedule 21 FA 2016.

Aggregate caps where penalties fall on more than one person for the same inaccuracy: 100% (Cat 1), 150% (Cat 2), 200% (Cat 3) of potential lost revenue (CH116800; FA07/Sch24 paras 1, 1A).

### 7.5 Quality-of-disclosure weightings (CH63220)

| Element | Weighting |
|---|---|
| Telling | 30% |
| Helping | 40% |
| Giving access | 30% |
| **Total possible reduction** | **100%** |

An "additional information" element applies to offshore matters and transfers under Schedule 21 FA 2016. CH63220 says this applies for 2016-17 and later; CH117400/CH117500 say Schedule 21 FA 2016 came into force on 1 April 2017 and, for income tax and CGT, applies to **tax years starting on or after 6 April 2017**, with no change to penalty calculation for earlier years. **These two Compliance Handbook pages disagree on the start year** — CH63220 and CH112400 say 2016-17; CH117400 says 2017-18 onwards. Implementers should treat this as an open question.

### 7.6 Asset-based penalty (Schedule 22 FA 2016)

| Element | Value | Ref |
|---|---|---|
| Offshore potential lost revenue threshold | more than £25,000 per tax year | CH122010 / CH122020 |
| Standard penalty | lower of 10% of asset value, and offshore PLR × 10 | CH122500; FA16/Sch22 para 7 |

Applies for 2016-17 onwards (commencement 1 April 2017), or to earlier years only where charged alongside a failure-to-correct penalty under Schedule 18 FA (No.2) 2017 (CH122010). Worked example (Mr E, 2020-21): asset value £1,500,000, offshore PLR £35,000, standard asset-based penalty £150,000 (CH122060).

---

## 8. Figures whose tax year the source does not state

These appear in the sources without any tax year. Do not assume currency.

| Figure | Value | Ref | Notes |
|---|---|---|---|
| Cap on total Income Tax losses set against a year's income | £50,000, or 25% of that income if greater | HS286, "How the relief is given" | Stated as applying "2013 to 2014 onwards"; no end year given. Does not apply to losses on shares with EIS or SEIS relief attributable. |
| Averaging (creators of literary/artistic works) — variance test | one year's profits less than 75% of the other's, or one year nil | HS234 s.4 | Condition, not an amount |
| Rent a Room exemption (SA100) | £7,500 | SAM121560 | No tax year stated |
| Rent a Room higher reporting threshold (SA100) | £15,000 | SAM121560 | No tax year stated |
| Rent a Room exemption (SA200, no mention required) | £4,250 | SAM121560 | Conflicts in level with the £7,500 SA100 figure; SAM does not date either |
| UK property income threshold for SA200 eligibility | £90,000 | SAM121560 | No tax year stated |
| Restricted Relief Qualifying Policy annual premium limit | £3,600 | HS320 s.9.2 | Tied to policies issued before 21 March 2012 and varied after |
| PAYE coding-out threshold for SA balancing payments | £2,999.99 or less codes out; £3,000 or more does not | SAM141010; SALF204 | No tax year stated |
| Statement de minimis — periodic statements | £32 | SAM, "Statement lower limit" | Administrative |
| Statement de minimis — standard statements | £2 | SAM, "Statement lower limit" | Administrative |
| Reminder issue threshold (SA359) | £100 or more outstanding | SAM61210 | Administrative |
| "Low means" threshold (national default) | £10,000 | SAM, "Low means threshold" | Can be varied locally by postcode |
| "Low risk" overdue amount range | £100 to £100,000 | SAM, "Low risk" | Debt management classification |
| Class 2 NIC auto-correction tolerance | £25 | SAM124035 | Administrative |
| Agent client list cap | 4,000 clients | SAM126001 | Administrative |
| Multiple cheque / payslip transaction limits | 20 cheques; 99 payslips | SAM glossary | Administrative |

### FHL occupancy day-counts (conditions, not monetary)

| Condition | Current | 2011-12 and earlier | Ref |
|---|---|---|---|
| Availability | at least 210 days | 140 days | HS253 |
| Letting | at least 105 days | 70 days | HS253 |
| Pattern of occupation (failure trigger) | lettings over 31 continuous days totalling more than 155 days | — | HS253 |

HS253 states it covers FHL rules "only up to the end of the 2025 tax year", implying the rules change or cease afterwards; the source does not say what replaces them.

---

## 9. Gaps in the sources

The following are within the brief's scope but **not present in the supplied notes**, and are not supplied here from any other knowledge:

1. **Income tax rates and bands** for any tax year — basic, higher and additional rates; Scottish and Welsh rates; savings and dividend rates. Absent entirely. HS321 s.10.1 refers to top slicing relief being available where a gain pushes a taxpayer from basic to higher/additional rate, but never states what those rates or band limits are.
2. **The personal allowance for any year other than 2024-25/2025-26**, where £12,570 appears only inside a worked example (HS286 Example 6), not as a stated rate table entry. The personal allowance taper is not described.
3. **The CGT annual exempt amount** for any year. HS282 and HS266 both refer to it operationally without a figure. The only CGT rate given is 24% for personal representatives and trustees on disposals on or after 30 October 2024 (HS282 s.9); individual CGT rates are absent.
4. **National Insurance rates and limits** — Class 1, Class 2 (post-abolition voluntary rate), Class 4 rates, lower/upper profits limits, small profits threshold value. Only the historical £7,105 Class 2 profits figure appears (SAM121665), undated and flagged as reference-only.
5. **Dividend allowance and savings allowance** amounts. SAM100060 references gov.uk dividend allowance guidance as a cross-reference but the note does not carry a URL or a figure.
6. **Marriage Allowance / transferable allowance** amount. SAM124021 and SAM125200 describe the mechanics of transferring allowances between spouses and civil partners; no value is given.
7. **Blind person's allowance** amount. Mentioned only as an allowance lost on a FIG claim (HS266).
8. **Interest rates** — late payment interest and repayment interest rates are nowhere stated. CH146220 and EM4030 describe *when* interest starts running, not at what rate.
9. **A live GOV.UK rates page.** The brief anticipates the possibility that sources point at a live page rather than stating figures. In fact **no source in this set does so** for rates and allowances. The nearest pointers are the helpsheet landing pages on GOV.UK (for example, [HS345 Pension savings — tax charges](https://www.gov.uk/government/publications/pensions-tax-charges-on-any-excess-over-the-lifetime-allowance-annual-allowance-special-annual-allowance-and-on-unauthorised-payments-hs345-self) and [HS393 Seed Enterprise Investment Scheme](https://www.gov.uk/government/publications/seed-enterprise-investment-scheme-income-tax-and-capital-gains-tax-reliefs-hs393-self-assessment-helpsheet)), which carry the figures reproduced in §2 for their own stated years only.
10. **The VAT registration threshold as such.** SAM122130 tracks a turnover threshold "aligned to the VAT threshold" year by year, which is the closest the sources come; SAM does not state that these figures *are* the VAT threshold for all purposes.
11. **Amendment time limits are given in the sources but are not rates** — for completeness: taxpayer amendment within 12 months of the statutory filing date (TMA 1970 s.9ZA), HMRC correction within 9 months of delivery (TMA 1970 s.9ZB), overpayment relief within 4 years of the end of the tax year (TMA 1970 s.33 and Sch 1AB), and assessment time limits of 4/6/12/20 years (TMA 1970 ss.34, 36, 36A). These are covered on other pages of this wiki.

---

## Sources used on this page

This page was written by an LLM from structured notes extracted from the mirrored sources below. Always check the upstream source before relying on any figure or deadline.

- [sa-helpsheets:5f67ceae-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/averaging-for-creators-of-literary-or-artistic-works-hs234-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/averaging-for-creators-of-literary-or-artistic-works-self-assessment-helpsheet-hs234.md`
- [sa-helpsheets:5f67d29a-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/death-personal-representatives-and-legatees-hs282-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/capital-gains-tax-when-someone-dies-self-assessment-helpsheet-hs282.md`
- [sa-helpsheets:f689f4a2-7da1-41a3-b37d-b18c346219ed](https://www.gov.uk/government/publications/foreign-income-and-gains-fig-regime-self-assessment-helpsheet-hs266) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/foreign-income-and-gains-fig-regime-self-assessment-helpsheet-hs266.md`
- [sa-helpsheets:5f67e2d6-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/furnished-holiday-lettings-hs253-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/furnished-holiday-lettings-self-assessment-helpsheet-hs253.md`
- [sa-helpsheets:5f67db85-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/gains-on-foreign-life-insurance-policies-hs321-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/gains-on-foreign-life-insurance-policies-self-assessment-helpsheet-hs321.md`
- [sa-helpsheets:5f67dcd2-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/gains-on-uk-life-insurance-policies-hs320-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/gains-on-uk-life-insurance-policies-self-assessment-helpsheet-hs320.md`
- [sa-helpsheets:5f67d46f-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/negligible-value-claims-and-income-tax-losses-on-disposals-of-shares-you-have-subscribed-for-in-qualifying-trading-companies-hs286-self-assessment-he) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/negligible-value-claims-and-income-tax-losses-on-disposal-of-shares-self-assessment-helpsheet-hs286.md`
- [sa-helpsheets:5f67defe-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/pensions-tax-charges-on-any-excess-over-the-lifetime-allowance-annual-allowance-special-annual-allowance-and-on-unauthorised-payments-hs345-self) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/pension-savings-tax-charges-self-assessment-helpsheet-hs345.md`
- [sa-helpsheets:5f67e327-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/seed-enterprise-investment-scheme-income-tax-and-capital-gains-tax-reliefs-hs393-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/seed-enterprise-investment-scheme-income-tax-and-capital-gains-tax-reliefs-self-assessment-helpsheet-hs393.md`
- [hmrc-manual-ch](https://www.gov.uk/hmrc-internal-manuals/compliance-handbook) - 21 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/ch.md`
- [hmrc-manual-em](https://www.gov.uk/hmrc-internal-manuals/enquiry-manual) - 7 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/em.md`
- [hmrc-manual-salf](https://www.gov.uk/hmrc-internal-manuals/self-assessment-legal-framework) - 7 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/salf.md`
- [hmrc-manual-sam](https://www.gov.uk/hmrc-internal-manuals/self-assessment-manual) - 34 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/sam.md`
- [itepa-2003](https://www.legislation.gov.uk/ukpga/2003/1/contents) - 1 note(s) - mirrored at `corpus/legal-system/primary-legislation/acts/itepa-2003.md`
- [tma-1970](https://www.legislation.gov.uk/ukpga/1970/9/contents) - 1 note(s) - mirrored at `corpus/legal-system/primary-legislation/acts/tma-1970.md`
