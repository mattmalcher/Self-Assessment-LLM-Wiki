---
title: Who must file a Self Assessment return
generated: true
generated_on: '2026-09-04'
generated_by: claude-cli:opus
input_hash: b1fa40a58374ef7a
note_count: 39
sources:
- hmrc-escs
- hmrc-manual-artg
- hmrc-manual-ch
- hmrc-manual-em
- hmrc-manual-salf
- hmrc-manual-sam
- hmrc-tools-calculators
- sa-helpsheets:5f67c90c-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67ceae-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67d46f-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67d5b1-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67db85-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dc31-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dcd2-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dfee-7631-11e4-a3cb-005056011aef
- si-ftt-tax-chamber-rules-2009
---

# Who must file a Self Assessment return

!!! danger "Unofficial - not HMRC, not advice, written by an LLM"

    This page is **not** an HMRC publication and has no connection to HMRC or
    any government body. It was **written by a language model** from mirrored
    source material, and can be wrong, incomplete or out of date. It is not
    tax advice. Check every figure, date and rule against the cited source
    before relying on it, and see
    [GOV.UK](https://www.gov.uk/self-assessment-tax-returns) for official
    guidance.

This page sets out how a person is brought into UK Self Assessment for income tax and capital gains tax: the notice to file that creates the filing obligation, the separate statutory duty to notify chargeability where no notice has been given, who HMRC issues notices to in practice, and how a person can be taken back out. It is an independent reference, not an HMRC publication; HMRC manual material is identified as HMRC's own view rather than law.

## Two distinct obligations

The statutory scheme has two separate triggers. Confusing them is the most common modelling error.

| | Notice to file | Notify chargeability |
|---|---|---|
| Statutory source | TMA 1970 s.8 (individuals), s.8A (trustees), s.8 TMA (personal representatives), s.12AA (partnerships) | TMA 1970 s.7(1) |
| Trigger | HMRC gives a notice requiring a return (SALF203) | Having profits or chargeable gains on which tax is due, **and** no notice to file has been given (TMA 1970 s.7(1)) |
| What it requires | Delivery of a completed return containing a self assessment by the filing date (TMA 1970 s.8(1)(a); s.9(1)) | Notification to an officer of the Board within six months of the end of the tax year (TMA 1970 s.7(1)) |
| Sanction if missed | Fixed, daily and tax-geared penalties under Schedule 55 FA 2009; HMRC may make a determination under TMA 1970 s.28C | Penalty under Schedule 41 FA 2008 |

A person who has been given a notice to file must file **even if no tax is due**: the return must include a self assessment "even if nil or a repayment is due" (TMA 1970 s.9(1), as described at SALF204). The notice, not the underlying tax position, is what creates the filing duty.

## The notice to file

SALF203 describes the notice to file as "a notice requiring a tax return, issued to the taxpayer by 'an officer of the Board'", noting that some taxpayers receive a paper return that itself contains the notice. Any notice relating to income tax, CGT or corporation tax must be in writing (S989 ITA 2007 / S1119 CTA 2010, per EM0067).

Filing dates flow from the notice and its issue date:

| Case | Filing date | Ref |
|---|---|---|
| Paper return, notice given before 31 July following the tax year | 31 October following end of year of assessment | TMA 1970 s.8(1)(a) |
| Electronic return, notice given before 31 July | 31 January following end of year of assessment | TMA 1970 s.8(1)(a) |
| Notice given after 31 July following end of tax year | 3 months beginning with the date of the notice, or 31 January if later (electronic filing) | TMA 1970 s.8(1D)–(1G) |
| Taxpayer wants HMRC to calculate the tax; notice given after 31 August | 2 months beginning with the day the notice is given | TMA 1970 s.9(2); SALF202 |

HMRC's operational manual (SAM, "Filing date – 2007-08 and later years") states the late-issue rule slightly differently, as "3 months and 7 days after issue date", and records exceptions to the standard dates for non-resident companies (SA700), registered pension scheme trustees (SA970) and certain elected representatives (MPs, MSPs, Welsh and NI Assembly Members). Where the notes disagree, SALF/statute gives 3 months; the SAM operational entry gives 3 months and 7 days.

## Voluntary returns

A return received where HMRC has not given a notice to file is a **voluntary return**. Since law put beyond doubt from 12 February 2019, with retrospective and prospective effect, it is treated as made in response to a notice to file given on the date the return was received (SALF202). Consequences:

- A voluntary return is always treated as delivered on or before the filing date, so no late-filing penalty arises (SALF202/SALF203).
- Its filing date for other purposes is 31 October (paper) or 31 January (electronic) following the tax year, unless received after 31 July (paper) or 31 October (electronic), in which case 3 months after the date received (SALF202).
- Any balancing payment is due three months from the date the voluntary return was received where it is delivered after 31 October following the year (TMA 1970 s.59B(3)–(6) and Schedule 3ZA).

## Who HMRC issues notices to

This is administrative practice, not statute. SALF ("Who will get tax returns?") states that around 4 million of the 28 million taxpayers covered by PAYE are sent Self Assessment returns, because of higher rate liability or because their affairs are complex. SALF706 separately confirms that PAYE employees can be within Self Assessment.

Notices are also given to persons other than individuals:

| Person | Return obligation | Ref |
|---|---|---|
| Trustees | Return of trust income, profits or gains and payment of IT/CGT, on the same fixed timescale as individuals | TMA 1970 s.8A / s.9 |
| Any "relevant trustee" | May notify chargeability, make the return, or deal with an enquiry on behalf of all trustees | TMA 1970 s.107A(1); "relevant trustee" defined at s.7(9) and s.118 |
| Personal representatives | Return of estate income, profits or gains; deduct tax before distributing income; issue form R185 to beneficiaries | TMA 1970 s.8; SALF806 |
| Beneficiaries of estates | Enter income attributed to their interest, with the tax credit, on their own SA return | Chapter 6 Part 5 ITTOIA 2005 |
| Partnerships (nominated partner) | Partnership return establishing each partner's chargeable amounts and the profit allocation | TMA 1970 s.12AA(1)–(3) |
| Individual partners | Include their share of partnership profits, losses, credits or charges in their own personal return, using exactly the allocated figure | TMA 1970 s.8(1B), (1C); SALF502 |
| UK representative of a non-resident | Must fulfil the non-resident's SA obligations, including notification, filing and payments | FA95/Sch23 paras 1–3; FA2003/S150(3)–(4) |

There are no partnership assessments under Self Assessment; assessment and collection operate on the individual partners as if the partnership did not exist, despite the partnership return requirement (SALF, discovery/partnership sections).

## Notifying chargeability where no notice is given

**Rule (implementable).** Input: whether a notice to file under s.8/s.8A was given for the year; whether the person has profits or chargeable gains on which tax is due. Condition: tax due **and** no notice given. Result: notification to an officer of the Board required within six months of the end of the tax year in which the liability arises — i.e. received on or before 5 October (TMA 1970 s.7(1); SALF210; EM0050 states the same six-month rule for 1995-96 onwards).

**Exceptions.** SALF210 states that exceptions to the notify-chargeability requirement apply only where the taxpayer has no chargeable gains (or gains within the annual exempt amount) **and** either has no net income tax liability or has had sufficient tax deducted at source.

**Coronavirus support payments.** Where a person receives a support payment they were not entitled to, the notification period starts on the day income tax became chargeable and ends on the later of 20 October 2020 or the 90th day after the income tax became chargeable (SALF210).

**Penalty.** Failure to notify within the six-month limit attracts a penalty under Schedule 41 FA 2008 of up to the net amount of tax due but unpaid at 31 January following the tax year in which the liability arises. SALF210 records that the penalty is eliminated if the full tax is paid on or before that 31 January, even where notification was late. The Compliance Handbook describes the same regime as a percentage of "potential lost revenue", varying with behaviour (careless/deliberate) and whether disclosure was prompted or unprompted (FA08/SCH41; CH70100).

**Notifiable events (HMRC's framing).** CH70100 lists the events a person must tell HMRC about as including having tax to pay without a notice to file, starting a new taxable activity, turnover reaching a threshold, and a change in the nature of an activity.

**Related registration duty.** A person starting their own business must register for Class 2 NIC within 3 months, from 31 January 2001 (EM0050; Regulation 87A of SI 2001/1004 is cross-referenced at SALF210).

Missing the 5 October date does not shift the payment dates: where a return is issued after 5 October because of a failure to notify, SAM's "Failure to Notify" entry states the balancing charge remains due 31 January after the end of the tax year, and payments on account are unchanged. (By contrast, where HMRC issues a return late through its own error, SAM says the due dates are amended accordingly.)

## Thresholds in customer-facing guidance

Self Assessment helpsheets state registration thresholds in simplified terms. For chargeable event gains on life insurance policies:

| Situation | Guidance | Ref |
|---|---|---|
| Individual already within SA | Report the gain on the SA return (Foreign section / "UK other income") | HS320 s.6.1; HS321 s.6.1 |
| Not within SA; gain **plus other savings and investment income** exceeds £10,000 | Register for SA and report the gain on the return | HS320 s.6.1; HS321 s.6.1 |
| Not within SA; gain plus other savings/investment income is £10,000 or less | Contact SA general enquiries, or send a copy of the chargeable event certificate with the NI number to HMRC, BX9 1AS | HS320 s.6.1; HS321 s.6.1 |

Note that the £10,000 test is on the gain **together with** other savings and investment income, not the gain alone (HS320 s.6.1 caveats). This is customer-facing guidance rather than statute; the underlying statutory duty for a person with tax to pay and no notice to file remains s.7(1).

## Being taken out again: withdrawal of a notice and Simple Assessment

EM0050 records that, for 2016-17 onwards, where a person's notice to file a return is **withdrawn to allow a Simple Assessment**, that person must notify chargeability in respect of any income or gains **not included** in that Simple Assessment. The notes do not give the statutory provision governing withdrawal itself, nor the deadline for that residual notification.

Simple Assessment has restricted challenge rights: there is no right of appeal (and no right of review) unless the person first raises a query under TMA 1970 s.31AA within 60 days of the date the notice of Simple Assessment was issued (or such longer period as HMRC may allow) and receives a final response (ARTG; s.31AA TMA 1970).

## Overlay: Making Tax Digital for Income Tax

MTD does not change who is required to file, but changes how relevant persons meet the obligation. SALF910 sets out qualifying income thresholds and mandation dates:

| Qualifying income in return for | Threshold | MTD applies from |
|---|---|---|
| 2024-25 | over £50,000 | 6 April 2026 |
| 2025-26 | over £30,000 | 6 April 2027 |
| 2026-27 and later | over £20,000 | 6 April 2028 |

A "relevant person" is one carrying on (or who has carried on) a "relevant activity" — an activity giving rise to profits or income chargeable under Part 2 (trade, profession, vocation) or Part 3 (property business) ITTOIA 2005 if the person were UK resident, excluding partnership activities, charitable/exempt unauthorised unit trust trustee activities, Lloyd's underwriting, REIT share distributions and OEIC participation (SALF930). MTD for Income Tax does not yet apply to partnerships; SALF states HMRC will set a future timeline. The self assessment return remains due 31 January the following year (SALF910; TMA 1970 s.8(1)(a)).

Digital exclusion exemptions (religious belief; not reasonably possible to use electronic communications or keep electronic records because of age, disability or location; inability to meet identity verification conditions) require an application in writing and an exclusion notice from HMRC; SALF1420 states it is anticipated to be rare for the conditions to be met.

## What happens when the obligation is missed

| Failure | Consequence | Ref |
|---|---|---|
| Return not filed by the filing date (notice given) | Fixed penalties, sometimes daily and tax-geared penalties | Schedule 55 FA 2009; SALF208 |
| Return not filed at all | HMRC may make a determination of tax due to the best of the officer's information and belief, treated as a self assessment until superseded | TMA 1970 s.28C(1),(3) |
| — time limit for determination | No determination after 3 years beginning with the filing date | TMA 1970 s.28C(5) |
| — replacing a determination | Actual self assessment must be filed within that 3-year period or, if later, within 12 months of the determination date | TMA 1970 s.28C(6) |
| Failure to notify chargeability | Penalty up to the net tax unpaid at the following 31 January | Schedule 41 FA 2008 |

There is no right of appeal against a determination, but it is automatically superseded once an actual self assessment is filed (SALF209).

Filing also triggers record-keeping duties under TMA 1970 s.12B(1),(2): retention to the fifth anniversary of the 31 January next following the year of assessment for a person with a business, and the first anniversary of that 31 January otherwise, extended where an enquiry is open. Where the notice to file or voluntary return is made or delivered after the normal retention-triggering date, SALF211 says the requirement is reduced to records still in the taxpayer's possession.

## Gaps in the sources

The supplied notes do not cover, and this page therefore does not state:

- The statutory provision permitting HMRC to **withdraw** a notice to file, the conditions for withdrawal, or the deadline for the residual notification of income not in a Simple Assessment. Only the EM0050 summary of the effect is available.
- Any HMRC operational **SA criteria list** (for example, self-employment turnover triggers, high-income child benefit charge, dividend or untaxed income thresholds, or criteria for taking a taxpayer out of SA). The only operational statement in the notes is the SALF figure of roughly 4 million of 28 million PAYE taxpayers receiving returns because of higher rate liability or complex affairs. SAM106000 is not among the supplied notes.
- The full statutory text of the s.7 exceptions (only SALF210's summary of them is available), and the s.7(2)–(7) detail.
- Registration mechanics (SA1/CWF1 forms, UTR issue, deadlines for registering).
- Thresholds for capital gains reporting into SA, other than the 60-day UK residential property reporting rule mentioned in HS292 for completions on or after 27 October 2021, which is a separate return obligation.
- Non-resident individual filing requirements beyond the UK representative provisions.

---

## Sources used on this page

This page was written by an LLM from structured notes extracted from the mirrored sources below. Always check the upstream source before relying on any figure or deadline.

- [sa-helpsheets:5f67dfee-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/accrued-income-scheme-hs343-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/accrued-income-scheme-self-assessment-helpsheet-hs343.md`
- [sa-helpsheets:5f67ceae-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/averaging-for-creators-of-literary-or-artistic-works-hs234-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/averaging-for-creators-of-literary-or-artistic-works-self-assessment-helpsheet-hs234.md`
- [sa-helpsheets:5f67d5b1-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/land-and-leases-the-valuation-of-land-and-capital-gains-tax-hs292-self-assessment-helpsheet) - 2 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/capital-gains-tax-land-and-leases-self-assessment-helpsheet-hs292.md`
- [sa-helpsheets:5f67dc31-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/employee-shares-and-securities-further-guidance-hs305-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/employment-related-shares-and-securities-self-assessment-helpsheet-hs305.md`
- [sa-helpsheets:5f67db85-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/gains-on-foreign-life-insurance-policies-hs321-self-assessment-helpsheet) - 3 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/gains-on-foreign-life-insurance-policies-self-assessment-helpsheet-hs321.md`
- [sa-helpsheets:5f67dcd2-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/gains-on-uk-life-insurance-policies-hs320-self-assessment-helpsheet) - 7 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/gains-on-uk-life-insurance-policies-self-assessment-helpsheet-hs320.md`
- [sa-helpsheets:5f67d46f-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/negligible-value-claims-and-income-tax-losses-on-disposals-of-shares-you-have-subscribed-for-in-qualifying-trading-companies-hs286-self-assessment-he) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/negligible-value-claims-and-income-tax-losses-on-disposal-of-shares-self-assessment-helpsheet-hs286.md`
- [sa-helpsheets:5f67c90c-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/non-taxable-payments-or-benefits-for-employees-hs207-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/non-taxable-payments-or-benefits-for-employees-self-assessment-helpsheet-hs207.md`
- [hmrc-tools-calculators](https://www.gov.uk/guidance/hmrc-tools-and-calculators) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-tools.md`
- [hmrc-escs](https://www.gov.uk/government/collections/extra-statutory-concessions) - 1 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/extra-statutory-concessions.md`
- [hmrc-manual-artg](https://www.gov.uk/hmrc-internal-manuals/appeals-reviews-and-tribunals-guidance) - 3 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/artg.md`
- [hmrc-manual-ch](https://www.gov.uk/hmrc-internal-manuals/compliance-handbook) - 1 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/ch.md`
- [hmrc-manual-em](https://www.gov.uk/hmrc-internal-manuals/enquiry-manual) - 2 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/em.md`
- [hmrc-manual-salf](https://www.gov.uk/hmrc-internal-manuals/self-assessment-legal-framework) - 12 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/salf.md`
- [hmrc-manual-sam](https://www.gov.uk/hmrc-internal-manuals/self-assessment-manual) - 1 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/sam.md`
- [si-ftt-tax-chamber-rules-2009](https://www.legislation.gov.uk/uksi/2009/273/contents) - 1 note(s) - mirrored at `corpus/legal-system/secondary-legislation/tribunal-procedure-ftt-tax-chamber-rules-2009.md`
