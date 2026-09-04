---
title: Who must file a Self Assessment return
generated: true
generated_on: '2026-09-04'
generated_by: claude-cli:opus
input_hash: b7afec02377737e3
note_count: 13
sources:
- hmrc-manual-salf
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

Self Assessment obligations do not arise from being "self-employed" or "a higher rate taxpayer" as such: the return obligation is created by a notice to file under s.8 TMA 1970, and a separate statutory duty to notify chargeability under s.7 TMA 1970 catches people HMRC has not written to. This page sets out both mechanisms, who they apply to, what the supplied sources say about HMRC's operational selection of taxpayers, and what happens when either obligation is missed. It relies only on the source notes listed; where the notes are thin (notably on HMRC's published entry criteria and on withdrawal of a notice), that is flagged at the end.

## 1. The notice to file is what creates the return obligation

A "notice to file" is a notice requiring a tax return, issued to the taxpayer by "an officer of the Board"; some taxpayers instead receive a paper return that itself contains the notice to file (SALF203 / TMA 1970 s.8). Once given, the taxpayer must deliver a completed return by the statutory filing date (TMA 1970 s.8(1)(a), (1D)–(1G)).

Three consequences follow from that framing:

| Consequence | Rule | Ref |
|---|---|---|
| Filing date is fixed by the notice date | 31 October (paper) / 31 January (electronic) where notice given before 31 July; if notice given after 31 July, 3 months beginning with the date of the notice, or 31 January if later | TMA 1970 s.8(1)(a), (1D)–(1G) |
| Late filing is penalised | Fixed penalties under Schedule 55 FA 2009, with daily/tax-geared penalties in some cases (2010-11 onward); s.93 TMA 1970 £100 + £100 for 2009-10 and earlier | Sch 55 FA 2009; SALF208; TMA 1970 s.93(2),(4) |
| Non-filing can be met with a determination | An officer may estimate tax due to the best of their information and belief; treated as a self assessment until superseded by an actual return | TMA 1970 s.28C(1),(1A),(2),(3) |

The return must contain a self assessment of the tax due, even where the result is nil or a repayment (TMA 1970 s.9(1)), unless the taxpayer files the information section early enough for HMRC to calculate the tax (TMA 1970 s.9(2)).

**Implementable rule — filing date.** Inputs: `notice_date`, `tax_year_end`, `filing_medium`. If `notice_date` ≤ 31 July following the tax year: filing date = 31 October (paper) or 31 January (electronic). Otherwise: filing date = max(notice_date + 3 months, 31 January following the tax year) for electronic filing (TMA 1970 s.8(1)(a), (1D)–(1G)).

## 2. Voluntary returns: filing without a notice

A return received from a customer or agent where HMRC has not given a notice to file is a "voluntary return". Since law introduced with retrospective and prospective effect from 12 February 2019, it is treated as made in response to a notice to file given on the same date the return was received (SALF202).

That has a specific consequence: a voluntary return is always treated as delivered on or before the filing date, so no late filing penalty applies (SALF202 / SALF203). Voluntary return filing dates and payment dates track the receipt date:

| Situation | Deemed filing date | Balancing payment due |
|---|---|---|
| Voluntary paper return received on or before 31 July | 31 October following the tax year | 31 January following the tax year |
| Voluntary paper return received after 31 July | 3 months after date received | — |
| Voluntary electronic return received on or before 31 October | 31 January following the tax year | 31 January following the tax year |
| Voluntary electronic return received after 31 October | 3 months after date received | 3 months from the date the voluntary return was received |

Sources: SALF202; TMA 1970 s.59B(3)–(6) and Schedule 3ZA.

Filing voluntarily does not remove the record-keeping duty: s.12B applies where a notice to file is given, a return containing the notice is given, **or** a voluntary return is made and delivered (TMA 1970 s.12B(1),(2)).

## 3. The statutory duty to notify chargeability (s.7 TMA 1970)

Where no notice to file has been issued, the obligation runs the other way: the taxpayer must tell HMRC.

**Rule.** A person who has profits or chargeable gains on which tax is due, and who has not been given a notice to file, must notify an officer of the Board of chargeability to income tax or capital gains tax within six months from the end of the tax year in which the liability arises — the notification must be received on or before 5 October (TMA 1970 s.7(1)).

**Exceptions.** The exceptions to the notify-chargeability requirement apply only where the taxpayer has **no chargeable gains (or gains within the annual exempt amount)** and **either** has no net income tax liability **or** has had sufficient tax deducted at source (SALF210, per Note 1). Both limbs must hold; the gains condition is not optional.

**Implementable rule — s.7 in scope.** Inputs: `notice_to_file_given` (bool), `chargeable_gains`, `annual_exempt_amount`, `net_income_tax_liability`, `tax_deducted_at_source_sufficient` (bool). Notification is required where `notice_to_file_given == false` AND NOT (`chargeable_gains ≤ annual_exempt_amount` AND (`net_income_tax_liability == 0` OR `tax_deducted_at_source_sufficient`)). Deadline: 5 October following the end of the tax year (TMA 1970 s.7(1); SALF210).

**Penalty.** Failure to notify within the six-month time limit attracts a penalty under Schedule 41 FA 2008, up to the net amount of tax due but unpaid at 31 January following the tax year in which the liability arises. Critically, the penalty is eliminated if the full tax is paid on or before that 31 January, even where notification was made late (Schedule 41 FA 2008, per SALF210).

**Coronavirus support payments.** A person who receives a coronavirus support payment they are not entitled to must notify chargeability within a distinct notification period: it starts on the day income tax became chargeable and ends on the later of 20 October 2020 or the 90th day after the income tax became chargeable (SALF210).

Note the interaction with due dates: where a late notice to file or a late voluntary return shifts the balancing payment date to three months from delivery/receipt, the sources describe that as applying where there is **no** failure to notify under s.7 (TMA 1970 s.59B(3)–(6) and Sch 3ZA). A s.7 failure does not buy extra time to pay.

## 4. Who HMRC issues notices to, and why

This is operational practice rather than statute. The SALF manual states that around **4 million** of the **28 million** taxpayers covered by PAYE are sent Self Assessment returns, because of higher rate liability or because their affairs are otherwise complex (SALF, "Who will get tax returns?" — Note 2). SALF separately confirms that PAYE employees can be within Self Assessment (Note 11).

The supporting information HMRC uses to identify such cases comes largely from employer and third-party reporting:

| Report | Who | Deadline | Ref |
|---|---|---|---|
| P60 to employee | Employers | 31 May | PAYE Regulations |
| P11D to HMRC and copy to employee | Employers | 6 July | PAYE Regulations |
| Written details of expenses/benefits to employee where provided by a third party and not on the employer's P11D | Third parties | 6 July following the tax year in which paid or provided | Section 15 |

Section 15 is described as a general information-seeking power letting HMRC require employers and third parties to give details of expenses payments and benefits in kind (Note 2).

## 5. Categories other than individuals

The regime brings in persons other than the individual taxpayer:

| Who | Obligation | Ref |
|---|---|---|
| **Trustees** | Make a return of income, profits or gains arising to the trust and pay income tax/CGT due, on the same fixed timescale as individual SA filing and payment | Section 8A / Section 9 |
| **Any "relevant trustee"** | May notify chargeability, make the return, or deal with an enquiry on behalf of all trustees | Section 107A(1) |
| **Personal representatives** | Make a return for the deceased's estate and pay income tax/CGT; deduct tax at basic (or investment/dividend) rate before distributing income; notify beneficiaries on form R185 (Estate Income) | Section 8 TMA; SALF806 |
| **Beneficiaries of estates** | Enter income attributed to their interest, and the associated tax credit, on their own SA return | Chapter 6 Part 5 ITTOIA |
| **Partners** | Include their share of partnership profits, losses, credits or charges in their own personal return — using exactly the allocated figure, with no adjustments permitted | TMA 1970 s.8(1B),(1C); SALF502 |
| **Partnership (nominated partner)** | File a partnership return establishing each partner's chargeable amounts, income tax payable and profit allocation | TMA 1970 s.12AA(1),(1A),(2),(3) |
| **UK representative of a non-resident** | Fulfil all the non-resident's SA obligations — notification of chargeability, filing the return and self assessment, interim and final payments | FA95/Sch23 paras 1–3; FA2003/S150(3)–(4) |

Two points of nuance. There are **no partnership assessments** under Self Assessment: assessment and collection operate on individual partners as if the partnership did not exist, even though a partnership return is required (Note 5). And trustees are jointly liable in law, though in practice one "principal acting trustee" deals with HMRC; HMRC may recover from any other relevant trustee, except that recovery against someone who became a relevant trustee only after a penalty or surcharge arose is limited to outstanding tax and interest on tax (Section 107A(2)–(4); s.107A(3)).

For non-residents, certain agents — Lloyd's agents, brokers and investment managers — meeting strict conditions are not treated as UK representatives at all, so the representative obligations never bite (Note 10). The investment manager tests turn on the independent agent condition and the "20%" condition (FA95/S127(3); FA2003/Sch26/Para 3–4; SP 01/2001 — HMRC's published view, not statute).

## 6. Being taken out again

The notes contain two mechanisms that reduce or remove obligations, neither of which is withdrawal of a s.8 notice:

- **Coding out instead of a balancing payment.** Where a taxpayer is within PAYE and the additional liability is **less than £3,000**, it may be collected through the PAYE code, provided the return is submitted electronically before 31 December following the end of the tax year, or on paper by 31 October following the end of the tax year (or received after but processed before 31 December) (SALF204).
- **Digital exclusion from MTD obligations.** A person or partner may be excluded from digital obligations where HMRC is satisfied they are a practising member of a religious society whose beliefs bar electronic communications or records, that it is not reasonably possible for them to use electronic communications or keep electronic records (age, disability, where they live), or that they cannot meet identity-verification conditions (SALF1420). The person writes to HMRC to apply, stating the reason and the dates of exclusion; HMRC decides and, if satisfied, must issue an **exclusion notice** stating the start date and any end date (SALF1430). If no end date was specified and the person later believes they have ceased to be excluded, they must give further notice within **3 months** of first having reason to believe that (SALF1430). HMRC anticipates it will be rare for the digital exclusion conditions to be met (SALF1420). Appeals against HMRC decisions under the Schedule A1 regulations must be made in writing, specifying grounds, within 30 days after the day notice of the decision is given (SALF950).

This exclusion removes the *digital* obligations, not the s.8 return obligation — the return remains due 31 January the following year (SALF910; s.8(1)(a) TMA 1970).

## 7. Making Tax Digital: an additional layer for some who already file

MTD for Income Tax applies to "relevant persons" (sole traders and landlords carrying on a "relevant activity") whose qualifying income exceeds the threshold for the relevant tax year (SALF910; SALF930).

| Qualifying income in | Threshold | MTD mandated from |
|---|---|---|
| 2024-25 | over £50,000 | 6 April 2026 |
| 2025-26 | over £30,000 | 6 April 2027 |
| 2026-27 and any subsequent tax year | over £20,000 | 6 April 2028 |

Source: SALF910. A "relevant activity" excludes partnership activities, charitable/exempt unauthorised unit trust trustee activities, Lloyd's underwriting, REIT share distributions and OEIC participation (SALF930); MTD does not yet apply to partnerships, with a future timeline to be set by HMRC (Note 9). The standard digital start date is 6 April in the tax year after the tax year in which the return obligation first applies (SALF1010), and when the notice to file was actually given can shift that date by a year; a calendar quarters election can shift it to 1 April in the prior year (Note 9). The notes warn that the commencement instruments have been repeatedly amended and revoked (SI 2021/1079 → SI 2024/422 → SI 2026/356; SI 2021/1076 amended by SI 2024/167, revoked by SI 2026/336), so the currently operative instrument should be checked.

## 8. Missing the obligation: what HMRC can do

| Failure | HMRC response | Ref |
|---|---|---|
| Notice to file given, no return by the filing date | Determination of tax due, to the best of the officer's information and belief; treated as a self assessment. No right of appeal, but automatically superseded by an actual self assessment | TMA 1970 s.28C(1)–(3) |
| — time limit to make one | No determination after 3 years beginning with the filing date | TMA 1970 s.28C(5) |
| — replacement by the taxpayer's own return | Within that 3-year period, or if later within 12 months of the date of the determination | TMA 1970 s.28C(6) |
| Failure to notify under s.7 | Penalty up to the net tax due but unpaid at 31 January following the tax year; nil if the tax is paid by that date | Schedule 41 FA 2008 |
| Undeclared income/gains discovered later | Discovery assessment; 4 years (ordinary), 6 years (careless), 12 years (offshore matters/transfers), 20 years (deliberate, **failure to notify**, DOTAS/POTAS) after the end of the tax year | TMA 1970 s.29(1), s.34(1), s.36(1),(1A), s.36A |

Note the last row: a failure to notify under s.7 puts the taxpayer into the 20-year discovery assessment window (TMA 1970 s.36(1A)). Tax charged by a discovery assessment is due 30 days after the notice of assessment is given (TMA 1970 s.59B(6)).

## Gaps in the sources

The notes do not cover the following parts of the brief, and nothing here should be inferred from them:

- **Withdrawal of a notice to file.** The supplied notes contain no reference to TMA 1970 s.8B or any equivalent power to withdraw a notice, no conditions for withdrawal, and no time limits. This page therefore cannot describe how a notice is withdrawn or what happens to filing dates and penalties when it is.
- **HMRC's operational entry criteria.** Beyond "higher rate liability or complex affairs" and the 4m-of-28m figure (SALF, Note 2), the notes contain no list of the customer-facing criteria that pull someone into Self Assessment — no self-employment gross-income threshold, no property income threshold, no High Income Child Benefit Charge, no dividend or savings-income triggers, no partnership/director/non-resident-landlord criteria. The £3,000 figure in section 6 is a coding-out threshold (SALF204), **not** an entry criterion.
- **The "check if you need to send a return" customer guidance.** No GOV.UK customer-facing guidance page is among the notes, so the simplified public criteria and their divergences from the statute cannot be described or compared.
- **Registration mechanics.** Nothing in the notes covers how a person registers (SA1, CWF1), how a UTR is issued, or deadlines tied to registration as distinct from the s.7 notification deadline.
- **Exit from Self Assessment.** Beyond MTD digital exclusion, the notes say nothing about how HMRC removes a taxpayer from the SA population once criteria cease to apply.
- **Tribunal material.** The only tribunal source supplied (SI 2009/273) is general Tax Chamber procedure — representatives, time calculation, witness summonses, withdrawal and lead cases — and, as its own note states, does not establish Self Assessment obligations. No case law on the scope of s.7 or s.8 is in the notes.

---

## Sources used on this page

This page was written by an LLM from structured notes extracted from the mirrored sources below. Always check the upstream source before relying on any figure or deadline.

- [hmrc-manual-salf](https://www.gov.uk/hmrc-internal-manuals/self-assessment-legal-framework) - 12 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/salf.md`
- [si-ftt-tax-chamber-rules-2009](https://www.legislation.gov.uk/uksi/2009/273/contents) - 1 note(s) - mirrored at `corpus/legal-system/secondary-legislation/tribunal-procedure-ftt-tax-chamber-rules-2009.md`