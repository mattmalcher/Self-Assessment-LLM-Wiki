---
title: Payments, payments on account and collection
generated: true
generated_on: '2026-09-08'
generated_by: claude-cli:opus
input_hash: 7a79e88fd10472c8
note_count: 80
sources:
- govuk-sa-detailed-information
- hmrc-manual-ch
- hmrc-manual-em
- hmrc-manual-salf
- hmrc-manual-sam
- hmrc-rates-allowances
- itepa-2003
- sa-helpsheets:5f67cf48-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67d41e-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dc31-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dd70-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dfee-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67e282-7631-11e4-a3cb-005056011aef
- tma-1970
---

# Payments, payments on account and collection

!!! danger "Unofficial - not HMRC, not advice, written by an LLM"

    This page is **not** an HMRC publication and has no connection to HMRC or
    any government body. It was **written by a language model** from mirrored
    source material, and can be wrong, incomplete or out of date. It is not
    tax advice. Check every figure, date and rule against the cited source
    before relying on it, and see
    [GOV.UK](https://www.gov.uk/self-assessment-tax-returns) for official
    guidance.

This page covers how Self Assessment liabilities are actually paid: the two payments on account under TMA 1970 s.59A, the balancing payment under s.59B, the exclusions that switch payments on account off, claims to reduce them, collection through a PAYE code, Time to Pay, and interest on tax paid late or repaid. It is an unofficial reference compiled from legislation, HMRC internal manuals and HMRC guidance; where a rule comes from an HMRC manual rather than statute, that is flagged. Penalties are covered only insofar as they attach to late payment.

---

## 1. The three payment dates

For a given tax year, a taxpayer within Self Assessment may face three separate payment obligations.

| Payment | Statutory basis | Due date | Notes |
|---|---|---|---|
| First payment on account (POA1) | TMA 1970 s.59A(2) | 31 January **within** the year of assessment | Payable without demand (s.59A(2)) |
| Second payment on account (POA2) | TMA 1970 s.59A(2) | 31 July next following the year of assessment | |
| Balancing payment | TMA 1970 s.59B(1), (4) | 31 January next following the year of assessment | Same date as the return filing date (EM0050) |

Both payments on account fall due "without demand" — the obligation exists regardless of whether HMRC issues a statement (TMA 1970 s.59A(2)).

Capital gains tax is **not** included in payments on account; it is payable in full with the balancing payment on 31 January after the end of the tax year (SALF302; EM0050). Class 4 NIC **is** within the payments on account regime (SALF302, calculated by reference to ss.15–16 Social Security Contributions and Benefits Act 1992). Student Loan and Postgraduate Loan repayments are excluded from payments on account and are collected as part of the balancing payment (SAM, "Contract settlement: Student Loans and Postgraduate Loans"). Class 2 NIC, from 2015-16, was collected as part of the SA Balancing Charge and expressly excluded from the expected liability calculation for payments on account (SAM121665; SAM1001) — HMRC notes mandatory Class 2 NIC was abolished from 6 April 2024 following the Autumn Statement of 22 November 2023 (SAM121665).

### 1.1 Alternative balancing payment dates

The 31 January date is displaced in several cases (TMA 1970 s.59B(3)–(6) and Schedule 3ZA; SALF302):

| Circumstance | Balancing payment due |
|---|---|
| Notice to file given after 31 October following the tax year, and no failure to notify under s.7 | Three months from the date the notice to file was given |
| Voluntary return received after 31 October following the year to which it relates, no s.7 failure | Three months from the date the voluntary return was received |
| Additional tax (not postponed) from an amendment, correction, or a s.29 discovery assessment | Later of the normal due date or 30 days from the date notice of amendment is given |

Where HMRC issues the return late, SAM guidance sets the filing date and balancing payment relevant date at **3 months and 7 days after the date of issue** for returns issued after 31 July (SAM60050) or after 31 October (SAM126080) following the end of the return year — but if failure to notify chargeability applies (i.e. the taxpayer did not notify by 5 October following the return year), the balancing charge and POA1 due date remains 31 January (SAM126080; SAM60052 Example 2). This concessionary treatment is HMRC's administrative practice recorded in its internal manual, not a statutory rule in TMA 1970.

---

## 2. Calculating payments on account

Each payment on account is **50% of the "relevant amount" for the preceding year** (TMA 1970 s.59A(2); SALF303 "Example: Calculation of relevant amount").

The relevant amount is defined (s.59A(1)/(8)) as:

> total income tax assessed for the preceding year **less** income tax deducted at source for that year, **plus** Class 4 NIC assessed less any deducted at source. Capital gains tax is excluded.

"Tax deducted at source" for s.59A(8) includes income tax deducted or treated as deducted from income, PAYE tax deducted under ITEPA 2003 s.684 (including future-year deductions relating to that year, but excluding amounts deducted this year for a previous year), and dividend tax credits under ITTOIA 2005 ss.397 and 397A. Foreign tax is excluded (SALF302).

### 2.1 Worked example (SALF, 2003-04 → 2004-05)

| Item | Amount |
|---|---|
| Gross income tax assessed 2003-04 | £8,500 |
| Less tax deducted at source | (£1,750) |
| Less credits on dividends received | (£345) |
| **Relevant amount — income tax** | **£6,405** |
| **Relevant amount — Class 4 NIC** | **£650** |

Payments on account for 2004-05: £3,202.50 income tax + £325 Class 4 NIC due 31 January 2005, and the same again due 31 July 2005 (SALF, "Example: Calculation of payments on account").

### 2.2 Machine-implementable form

```
relevant_amount_IT  = IT_assessed_prev_year - IT_deducted_at_source_prev_year
relevant_amount_C4  = C4NIC_assessed_prev_year - C4NIC_deducted_at_source
relevant_amount     = relevant_amount_IT + relevant_amount_C4
POA1 = POA2 = 0.50 * relevant_amount        # each capped at 50% (s.59A(2))
# CGT, Student Loan/PGL and (2015-16 to 2023-24) Class 2 NIC are excluded
```

The cap matters for interest: the amount that *should* have been paid on account "can never exceed 50% of the relevant amount for the preceding year", even if the current year's liability turns out higher (SALF, note on s.86(4)-(9)/Schedule 53 FA 2009).

---

## 3. When payments on account are not required

Two de minimis exclusions are set by the Income Tax (Payments On Account) Regulations 1996 (SI 1996/1654), as described in SALF302:

| Exclusion | Test | Value in SI 1996/1654 as originally made |
|---|---|---|
| Small amount | Relevant amount below a fixed cash figure | £1,000 |
| Majority taxed at source | Ratio of relevant amount to total assessed amount is less than 1 to 5 — i.e. more than 80% of the assessed liability was met by tax deducted at source | ratio < 1:5 |

**Caution on the figures.** SALF302 expressly warns that these limits "have been further amended by subsequent regulations" and that the figures quoted are as originally set by SI 1996/1654. Two HMRC manual pages independently quote £1,000 as the current threshold below which payments on account are not required (SAM1110 Note 1; SAM1100 Notes). The notes supplied do not give a current figure for the proportion test other than the original 1-in-5 / 80% formulation.

Note the interaction with claims: SAM1110 Note 1 states that payments on account totalling less than £1,000 **after a claim to adjust has been processed** are still payable — the de minimis operates on the original calculation, not the reduced one.

### 3.1 Directions that no payments on account are required

An officer may direct under TMA 1970 s.59A(9), before the 31 January next following the year in question, that no payments on account are required, with consequential adjustments. SALF notes this power is used only in specific circumstances — where the taxpayer has ceased to be within SA, or for tax-equalised foreign nationals under a modified PAYE agreement (EP Appendix 6) (SALF, caveats to s.59A; SAM121620). HMRC's stated position is that it does **not** issue such directions merely because a source has ceased or an unusual payment was received; the taxpayer must instead claim to reduce or cancel.

---

## 4. Claims to reduce (or increase) payments on account

### 4.1 The statutory test

A taxpayer may claim under TMA 1970 s.59A(3) or (4) where they believe the relevant amount for the current year will be less than for the preceding year, or nil. The claim must **state the grounds for that belief** (s.59A(3)–(4); SAM1020). The time limit is **before 31 January next following the year of assessment** (s.59A(3)&(4); SAM1040) — so a claim for 2005-06 must be made before 31 January 2007.

SALF notes that HMRC has **no power to reject a properly made claim**, though it may later review it for negligent or fraudulent claims.

### 4.2 HMRC's view on validity

SAM1040 sets out HMRC's working definition of a valid claim: in writing, by telephone, or via online services; giving a reason for the reduction; received before 31 January following the end of the tax year; stating or allowing deduction of the adjusted amounts; and, if on paper, signed by taxpayer or agent and showing an acceptable year.

SAM1020 records a divergence worth flagging for implementers: the legislation "does not stipulate that the grounds for a claim must be valid", but HMRC guidance treats claims with no reason, or with an unsatisfactory reason such as "unable to pay", as not constituting a valid claim. That is HMRC's interpretation, not a statutory condition. There is also an internal inconsistency: SAM1030 says only written or SA Online claims should be considered (with an exception for telephone claims to a Contact Centre), while SAM1040 lists telephone generally (SAM1020 caveats).

The basis on which the taxpayer should estimate: the "expected liability" is the total estimated liability to income tax and Class 4 NIC for the year on all sources, including any giving rise to higher rate tax (SAM1001). HMRC officers are told to explain this if queried, but "are not expected to question whether a claim to reduce payments on account was made on the correct basis" (SAM1001; SAM/W045-W061 caveats).

### 4.3 Consequences of getting it wrong

| Trigger | Consequence | Source |
|---|---|---|
| Fraudulent or negligent incorrect statement in connection with a claim | Penalty up to the difference between what would have been paid but for the incorrect statement and what was actually paid on account; determined by an officer, appealable to the tribunal | TMA 1970 s.59A(6); s.100; s.100B |
| Innocent error in good faith (wrong sums with no reason to suspect; reliance on information correct at the time) | No penalty | SALF (caveats to s.59A(6)) |
| Claim proves excessive | Late payment interest on the shortfall from the original POA due dates | SAM1020; CH142240 |
| EIS/VCT relief claimed against POA proves excessive | Interest on the reinstated amount from the relevant POA due dates | SAM1001 |
| CITR anticipated but relief due is less than expected | HMRC will charge interest on the shortfall | HS237 (caveat) |

A worked penalty maximum appears in SALF: for a 2004-05 claim relating to the 2003-04 relevant amount, the maximum penalty in the example was £4,250.

### 4.4 Other mechanics

- Processing a claim or amendment **does not change the payment on account due dates** (SAM1020).
- Claims to carry-back relief cannot be rejected even though carry-back relief has no effect on the level of payments on account for the year (SAM1020).
- A claim to increase payments on account can be made after a reduction claim is realised to have been excessive; SAM warns that simply making an extra payment without a formal claim means "the interest charge raised will not take the extra payment into consideration" (SAM glossary, "Claim to increase payment on account").
- Payments on account can only be reduced on an equal basis — TMA 1970 s.59A(4) (SAM110100).
- A claim to reduce POA cannot be made against a Revenue Determination; only against POA created for the following year, if that year's return is not overdue (SAM50040/50050 caveats).
- A part payment is not treated as a request to reduce payments on account (SAM1080 caveats).
- Where a valid claim is made in writing or by phone (but not on the return itself, and not via the GOV.UK SA303 i-form which carries a built-in warning), HMRC issues form SA614 advising of the interest implications (SAM1040; SAM1050). Invalid written claims are rejected with form SA303 and SEES letter SA811 (SAM, "Invalid claim received").
- Automatic review: capture of a return or amended return triggers verification of POA at their original amounts, or recalculation/reduction where the total liability (less CGT and tax deducted at source) is lower (SAM1020).

---

## 5. The balancing payment

### 5.1 Definition

The balancing payment is the difference between the self assessment liability for the year and the total of payments on account and tax deducted at source (TMA 1970 s.59B(1); CH142240). It sweeps up income tax, CGT and Student Loan repayments (SALF, s.59B(1)), and Class 4 NIC and student loan payments are confirmed as part of it (CH142220 / TMA 1970 s.59B).

### 5.2 Worked example (SALF, 2017-18)

| Item | Tax | NICs |
|---|---|---|
| Income tax assessed | £2,450 | |
| Capital gains tax assessed | £5,250 | |
| Class 4 NICs assessed | | £600 |
| Less tax deducted at source | (£640) | |
| Less POA paid 31 January 2018 | (£3,000) | (£275) |
| Less POA paid 31 July 2018 | (£3,000) | (£275) |
| **Balancing payment due 31 January 2019** | **£6,060** | **£50** |

Note how the CGT of £5,250, absent from the payments on account, drives most of the balancing payment.

### 5.3 Machine-implementable form

```
balancing_payment = (IT_assessed + CGT_assessed + C4NIC_assessed + SL_PGL_due)
                    - IT_deducted_at_source
                    - POA1_paid_or_due - POA2_paid_or_due
# negative result => balancing repayment / set-off (s.59B(1))
```

For **interest** purposes only, CH142240 warns that any amount paid on account in addition to the two required payments is ignored, as is any amount payable as CGT or student loan repayments (FA09/Sch53 para 1) or CGT only (para 2).

---

## 6. Collection through the PAYE code ("coding out")

Coding out is authorised by the PAYE regulations made under ITEPA 2003 s.684, which permits regulations providing for the recovery of self assessment underpayments and "relevant debts" through a tax code, subject to a cap on non-consensual deductions of **£17,000 per tax year** (ITEPA 2003 s.684(3A)) — a figure the Treasury may amend by order (s.684(3B)). "Relevant debt" means a sum payable to the Commissioners under an enactment (other than an excluded debt) or under a contract settlement (s.684(7AA)).

### 6.1 Conditions for automatic transfer of a balancing payment

HMRC's operational conditions (SAM141010; SAM141001; SAM333) are:

| Condition | Value |
|---|---|
| Balancing payment (BCD plus any outstanding POAs) | £2,999.99 or less |
| Threshold at or above which coding out does not apply | £3,000 or more |
| Paper return filed by | 31 October following the end of the return year |
| Paper return logged and captured by | before 31 December following the end of the return year |
| Online return submitted by | on or before 30 December (SAM141001); logged and fully captured before 31 December (SAM141010) |
| Automatic consideration window | 6 April to 31 December each year |

Amended returns: the customer amendment must be received on or before 30 December and the AMEND RETURN function used on or before 31 December (SAM141010).

HMRC's manual states officers must **not** code out where a paper return is received after 31 October and not processed before 31 December, and must not manually code out where an online return is submitted after 30 December (SAM141001 Notes).

### 6.2 Exclusions and edge cases

- **Class 2 NIC** included in a balancing payment from 2015-16 must not be transferred or coded out, "as this is not covered by legislation" — only the tax element is transferred (SAM141021; SAM141010 Note 6; SAM141001).
- The automatic process is **an estimated process only**: it transfers only if it believes the whole underpayment can be collected over one year (SAM141001; SAM141010). Where a customer appeals against non-coding, the balancing payment must be transferred to NPS with a manual update to the NPS Accounting Financial Events Summary screen (SAM141001).
- A customer **cannot** reduce the balancing charge by direct payment in order to bring the reduced amount within the coding-out limit (SAM141001), and HMRC officers are told not to remit an amount to reduce a balancing payment below £3,000 as a means of transferring it to PAYE (SAM50040).
- New or adjusted balancing payments arising from CREATE RETURN CHARGE, AMEND RETURN FOR ENQUIRY and CREATE RETURN CHARGE FOR ENQUIRY are not automatically transferred (SAM141001).
- Early filers: where at capture the balancing payment appeared to be £3,000 or more only because unpaid POA were added, no work item is created; SAM directs officers to code out manually where possible, since otherwise "the customer will be penalised for submitting the return early" (SAM141010; SAM141020).
- From 4 March 2020, SA debts can be coded over 2 tax years (noted without further detail at SAM141045).

### 6.3 Coding-out limits for other HMRC debt

A separate graduated income scale, introduced October 2014, governs how much *general* HMRC debt can be coded per tax year. SAM141045 is explicit that this scale and the debt-splitting rules do **not** apply to SA balancing charges or PAYE underpayments — those remain subject to the £3,000 limit.

| PAYE earnings | Coding out limit (from October 2014) |
|---|---|
| Up to £29,999.99 | £3,000 |
| £30,000 – £39,999.00 | £5,000 |
| £40,000 – £49,999.99 | £7,000 |
| £50,000 – £59,999.99 | £9,000 |
| £60,000 – £69,999.99 | £11,000 |
| £70,000 – £79,999.99 | £13,000 |
| £80,000 – £89,999.99 | £15,000 |
| £90,000 and above | £17,000 |

A debt exceeding the limit is split: SAM141045 gives an example of a £900 total, £600 coded and £300 residual, and a further example where a £12,000 total SA debt with £3,000 already in the code leaves £9,000, of which £5,000 is the maximum codeable and £2,000 of the remainder is rejected (SAM, "Splitting outstanding debts").

### 6.4 When coding out fails: stranded underpayments

If coding out proves wholly or partly unsuccessful, the amount is brought back onto the SA record as a "Stranded Underpayment" via CREATE SUNDRY CHARGE (SAM140030). The interest due date for a balancing payment transferred back from PAYE is:

> **the later of (a) 31 January following the end of the year for which the payment is due, or (b) 6 weeks following reinstatement to SA** (SAM140001; SAM140030).

HMRC officers are instructed to write to the taxpayer or agent explaining why the underpayment is being transferred back and the date from which interest is payable, and not to issue an SA return in these cases (SAM, "Taxpayer has ceased SA and PAYE source subsequently ceases / becomes NNL").

A taxpayer can stop further underpayments being coded by entering 'x' in box 2 page TR5 of the main return, or box 12.8 page 4 of the short return (SAM140030).

Interest accrues on a coded debt from the original due date but is not visible while a "Type 16 remission" is in place (SAM, "Splitting outstanding debts"). Effective dates of payment for coded debt: for debts coded in-year, the date the charge was passed from IDMS; for debts coded in the following year, 6 April of the year coding out takes place; for partially coded debts, the EDP of the following year's collected amount is the start date of that tax year (SAM, "Effective date of payment").

### 6.5 PAYE underpayments brought into SA

A P800(T) underpayment cannot itself be transferred to SA — an SA return must be issued to formalise the liability (SAM140001). Where a P800(T) shows an underpayment of **£3,000 or more** (or less, if it cannot be collected through PAYE) and it is not paid voluntarily, HMRC brings the case into SA (SAM140020). There is a firm time bar: the return cannot be issued later than **23 December three years after the end of the tax year in which the underpayment arose** — HMRC's worked example is that a 2006-07 return cannot be issued after 23 December 2010 (SAM140010/140020/140021).

---

## 7. Time to Pay and instalments

### 7.1 Time to Pay (TTP)

TTP is a negotiated arrangement to pay liabilities by instalments over an agreed period beyond the due date. SAM's glossary is clear that a TTP agreement exists **only where negotiated**, distinct from a promise or statement of intent to pay (SAM glossary, "Negotiated arrangement"). Recovery action ceases once agreed, **but late payment interest still accrues** (SAM glossary, "Time to Pay"; CH140280 — HMRC charges late payment interest on amounts unpaid after the due and payable date, "including on reducing balances during instalment/Time to Pay arrangements").

TTP requests made verbally or by telephone in a processing office must be referred to Debt Management and Banking; written requests are forwarded to the relevant SPOC (SAM80071). A pre-8 March 2001 local office procedure for liabilities under £5,000 no longer applies (SAM80071 caveats).

**Effect of TTP on late payment penalties** (SAM61380). Note that this is about penalties, not interest — interest is unaffected:

| Timing of acceptable TTP proposal that fully settles the liability | Effect |
|---|---|
| On or before the first trigger date (30 days after due date) | No late payment penalties imposed |
| After first trigger date but by 30 days + 5 months from due date | Avoids only the second and third penalties |
| After second trigger date but by 30 days + 11 months from due date | Avoids only the third penalty |

If a TTP was agreed before the trigger date but the customer later defaults, SAM61380 directs that an appeal against the penalty should be rejected (not sent to DMB).

### 7.2 Statutory Instalment Arrangements (SIA)

An SIA is a taxpayer's **statutory right** to pay certain SA liabilities by instalments (SAM80072), arising under provisions including S137 ICTA 1988, S280 and S281 TCGA 1992, and S299 ITTOIA 2005. Approval must be given by the office with SA Technical Responsibility before collection is arranged (SAM80072).

| SIA type | Instalment timing |
|---|---|
| Schedule E Group N net underpayment, 1st instalment (S137 ICTA 1988) | 14 days after issue of the first application or the balancing payment due date, whichever is later |
| Same, 5th instalment | 5 April of the fifth year after the end of the relevant year |
| Same, 2nd–4th instalments | At equal intervals between the 1st and 5th instalment due dates |
| CGT where consideration received in instalments (S280 TCGA 1992) | Up to 8 yearly or 16 half-yearly instalments; last no more than 8 years from the original due date |

For SIA instalments other than S281 TCGA 1992 cases, the Statutory Due Date of the instalment becomes the Relevant Due Date; for S281 cases the original RDD is retained (SAM80072).

### 7.3 Managed payment plans

TMA 1970 s.59G permits a person to agree with an officer to pay income tax due under s.59A(2) or s.59B (or corporation tax under s.59D) by **balanced instalments** — some before and some after the due date. Instalments are "balanced" where the time value of pre-due-date instalments is equal, or approximately equal, to the time value of post-due-date instalments (s.59H(2)), time value being a function of the instalment amount and the number of days before or after the due date (s.59H(4)). Where the person makes one or more post-due-date payments under such a plan, fails to pay a specified payment, and HMRC issues a notice specifying those payments, the person is not liable to a penalty or surcharge for that failure (s.59G(7)). Section 59G does not apply where a s.59F arrangement has already been made for that amount.

### 7.4 Instalments within contract settlements

Where an enquiry is settled by contract, HMRC's internal policy (EM6251) is that instalment settlement is not used if the expected offer is less than **£5,000** or would produce monthly instalments of less than **£100** each — such cases are settled by the formal route. Manager approval is required for instalment periods over 3 years, and periods over 5 years are described as not normally desirable. An "addition for time granted" (forward interest) is added to reflect the time value of money; EM worked examples show a reduction where the offer is settled early (e.g. an original total of £21,800 reduced by £670 to £21,130 at an assumed 9.5% rate under the "Original Method"; £15,125 reduced by £340 to £14,785 at 8.5% under the "New Method").

---

## 8. Interest on late payment

### 8.1 Which regime applies

| Period | Regime |
|---|---|
| Amounts becoming payable on or before 30 October 2011 | TMA 1970 s.86 |
| From 31 October 2011 | FA 2009 s.101 and Schedule 53 |

SALF states the harmonised FA 2009 regime "does not materially change the substantive position" (SALF, caveat). EM3980 notes the older EM4001–EM4010 guidance applies only to amounts outstanding prior to 31 October 2011. CH140160 is the gateway page: HMRC tells its own caseworkers to check whether, and from which date, the FA 2009 rules apply to the tax in question before applying the guidance (CH149950/CH140160).

The interest rate is set by regulations under FA 1989 s.178 (and, from 31 October 2011, under FA 2009 s.103) and changes automatically with bank base rate changes, so no fixed figure is quoted in the source material (SALF; TMA 1970 s.86(1)).

### 8.2 Core rules

- Interest is **simple, not compound**: late payment interest does not apply to late payment interest already charged, and repayment interest does not apply to repayment interest already accrued (CH140260; FA09/S101(8); FA09/S102(7)).
- Interest runs from the **late payment interest start date** to the **late payment interest end date**, being the date payment is made (CH149950).
- Interest applies **separately to each payment on account and to the balancing payment**, each running from its own due date (CH140290; TMA 1970 s.59A).
- Interest applies even where the relevant date falls on a non-business day within the meaning of s.92 Bills of Exchange Act 1882 (TMA 1970 s.86).
- Liability to interest is automatic. There is **no statutory right of appeal against interest itself**; only the underlying tax can be appealed, which then automatically adjusts the interest (CH140260). EM4030–EM4040 confirms there is no specific statutory power to mitigate interest, only the general collection and management discretion under CRCA 2005 s.5.
- Interest continues to accrue on all SA liabilities (except interest itself) until the debt is cleared, and does not stop at commencement of enforcement proceedings (SAM50050).

### 8.3 Start dates in special cases

| Situation | Late payment interest start date | Source |
|---|---|---|
| Payment on account | Its own s.59A(2) due date | TMA 1970 s.86(2)(a) |
| Balancing payment | Last day of the s.59B(3) three-month period, or the s.59B(4) date | TMA 1970 s.86(2)(b) |
| Tax postponed under TMA 1970 s.55 pending appeal, later found payable | The date payment would have been due had the appeal not been made | FA09/Sch53 para 4; CH143280 |
| Over-repayment recovered by s.30 assessment | 31 January following the tax year in respect of which the assessment is made | FA09/Sch53 para 5; CH143320 |
| Notice to file withdrawn, income later discovered | The date payment would have been due had the notice not been withdrawn | CH143 Example 3 |
| Taxpayer dies before the charge becomes due | Later of the normal start date and the day after 30 days from grant of probate / letters of administration / confirmation | FA09/Sch53 para 12; CH143360 |
| Non-discovery Revenue assessment | 30 days after the date of issue of the Assessment Notice | SAM20110; SAM20120 Example 3 |
| Discovery assessment | The statutory dates for the year of assessment | SAM20010 Note 2 |
| Balancing payment reinstated to SA after failed coding out | Later of 31 January following the year, or 6 weeks after reinstatement | SAM140001; SAM140030 |
| Additional tax found on enquiry | Payable within 30 days of enquiry settlement, but interest computed from the original POA and balancing payment dates | CH143 Example 2; EM6008 |

The death exception applies only where executors or administrators genuinely lack access to funds pending probate or confirmation (CH143 caveats).

Breathing Space (Debt Respite Scheme), in force from 4 May 2021, freezes interest, fees and charges during a moratorium period for eligible individuals; late payment interest is calculated to exclude amounts accrued during that period (CH140320). VAT is only eligible for Breathing Space if the debt relates to a sole trader who has deregistered (CH140260 caveat) — the notes do not state an equivalent restriction for income tax.

### 8.4 Interest where a claim to reduce POA was excessive

This is the most arithmetically specific rule in the sources. Under FA09/Sch53 para 1, where a claim to reduce payments on account proves excessive, late payment interest is charged on the **lesser of**:

- (a) the total of each reduced payment on account **plus 50% of the balancing payment**; and
- (b) the amount that would have been payable as a payment on account had the claim to reduce not been made.

(CH142240; SALF, remission provisions; TMA 1970 s.86(4)-(9) for pre-31 October 2011 amounts.)

```
def poa_interest_base(reduced_poa, balancing_payment, poa_absent_claim):
    # per payment on account, FA09/Sch53 para 1
    return min(reduced_poa + 0.5 * balancing_payment, poa_absent_claim)
```

CH142260 worked examples:

| Taxpayer | Year | Original POA (each) | Reduced POA (each) | Balancing payment |
|---|---|---|---|---|
| Alan | 2012-13 | £18,000 | £9,000 | £6,000 |
| Siobhan | 2013-14 | £25,000 | £10,000 | £8,000 |

For Alan, limb (a) gives £9,000 + £3,000 = £12,000; limb (b) gives £18,000; interest is charged on the lower, £12,000, per payment on account, running from 31 January and 31 July respectively — not from the balancing payment due date, "even though the underpayment is only identified later" (CH142240 caveat).

A parallel provision (FA09/Sch53 para 2) applies where the payments on account were paid late but the year turns out to be overpaid: interest is charged on **the amount by which each late-paid payment on account exceeds 50% of the overpayment for the year** (CH142240). CH142300 gives Eileen: POA of £5,000 each, tax liability shown on the return of £6,000, overpayment £4,000.

### 8.5 Remission where payments on account were excessive

TMA 1970 s.86(7)–(9) (and, from 31 October 2011, FA09/Sch53 para 2) provide for remission of interest where payments on account are later found to have been excessive: interest is recalculated on the true liability, capped at 50% of the preceding year's relevant amount (SALF, "Remission of interest charges on excessive payments on account"). The worked example uses a 2010-11 self assessment of £5,000 revised to £3,600, against a 2011-12 liability of £4,400.

### 8.6 Interest and enquiry settlements

EM6008–EM6009 set out how additional tax agreed on enquiry generates interest from the *original* due dates, and how it feeds into the following year's payments on account. EM6009's worked example (2022-23):

| Charge | Original | Revised | Interest |
|---|---|---|---|
| POA1 due 31 Jan 2023 | £2,500 | £3,500 | on £1,000 from 31 January 2023 |
| POA2 due 31 Jul 2023 | £2,500 | £3,500 | on £1,000 from 31 July 2023 |
| Balancing payment due 31 Jan 2024 | £4,000 | £2,000 | — |

Crucially, EM6009 records that interest on additional POAs runs only **to the balancing payment due date (31 January 2024), not to the settlement date**, "because the intent is not to charge interest on unpaid tax generally but only on amounts that should have been paid earlier via POA". If the post-enquiry year's return shows a liability less than the sum of the original POAs, there is no additional interest to include.

If the enquiry is finalised **before** the balancing payment date for the post-enquiry year, the POAs are amended on the SA system per SAM31040; if **after**, interest on the increased POAs is normally included in the contract settlement (EM6009).

### 8.7 Objections, not appeals

Because there is no appeal right against interest, disputes are handled as "objections". SAM60020 defines an objection as arising where the relevant date or effective date of payment is disputed, special circumstances are claimed, legislation is questioned, or an explanation is not accepted. HMRC's stated process:

- The underlying liability must be **paid in full** before the objection is considered, and the objection must be in writing (SAM60020).
- The officer acknowledges the objection, informally stands over the disputed interest, and refers unresolved cases to the Debt Management and Banking / Banking Operations **Interest Review Unit** at Cumbernauld (SAM60021; SAM134040; EM4040).
- The IRU will not accept cases for review unless the interest charge is **final** (not still accruing) (SAM50530 caveats).
- Disputed interest continues to appear on statements during investigation; inhibiting statements is possible only in exceptional circumstances and is not standard practice (SAM134040).
- Where a person claims excessive HMRC delay caused or contributed to the interest charge, caseworkers seek advice from the Specialist Technical team (CH140310; EM21000).

### 8.8 Contract settlements

Once a contract settlement is agreed, HMRC gives up the statutory right to charge tax, interest and penalties in exchange for a contractual payment; the statutory FA 2009 interest provisions cease to apply and contractual interest terms apply instead (CH140310). VAT and VAT penalties must never be included in a direct tax contract settlement (EM6006; EM6336).

---

## 9. Interest on overpaid tax (repayment interest)

Repayment interest is payable under FA 2009 s.102 and Schedule 54 (previously repayment supplement under ICTA 1988 s.824 / TCGA 1992 s.283) (SALF306). It is simple, not compound (CH146020).

### 9.1 Start dates

| Rule | Start date | Applies to |
|---|---|---|
| Rule 1 (amount paid to HMRC) | The **later** of the date the amount was paid to HMRC and the date it became due and payable | All taxes covered by the FA 2009 provisions, including ITSA |
| Rule 2 (amount not paid, due via return/claim) | The **later** of the date the return/claim was required and the date it was actually filed/made | Currently VAT only, for prescribed accounting periods starting on or after 1 January 2023 |

(CH146020; CH146040.) The repayment interest end date is the date the amount is repaid, paid to another person, or set off against a liability (CH146020; CH149950).

CH146020 draws out the practical consequence for SA: **early payment does not increase repayment interest** — interest runs from the due date, not the earlier actual payment date. CH146060's example: Russell paid two POAs of £15,000 for 2014-15 against an actual liability of £24,000, giving a £6,000 overpayment refunded.

Special start dates under Schedule 54 (SALF306):

| Repayment type | Repayment interest start date |
|---|---|
| Tax deducted at source, e.g. PAYE | 31 January next following that year (Sch 54 para 6) |
| Loss carry-back or averaging claims | 31 January next following the **later** year in relation to the claim (Sch 54 para 7) |

### 9.2 Allocation of an overpayment

For determining the repayment interest start date, FA09/Sch54 para 13 requires an income tax overpayment to be allocated in a specific order (CH146120):

1. First to any **balancing payment**;
2. Then in **two equal parts** to payments on account and to tax deducted at source.

This applies only "in so far as it is able to be allocated"; where payments were made in instalments, repayment is allocated to **later instalments before earlier ones** (CH146120 caveat). Worked examples in CH146120 cover James (£8,000 income tax overpayment for 2013-14) and Richard (£2,500 overpayment of a first payment on account).

### 9.3 Exclusions

- No repayment interest where an amount is payable by HMRC as a result of a court or tribunal order or judgment that already carries interest (FA09/S102(6)) — e.g. successful First-tier Tribunal appeals (CH146020; CH146xxx).
- Exclusions also apply to amounts described in a Treasury order (CH146020).
- Repayment supplement is **not** payable on an overpayment resulting from amendment of an interest charge, nor where set-off is made to an earlier year under the same UTR (SAM114070).
- RPS is not applicable to CIS in-year repayment freestanding credits (SAM110100).
- Overpayment of interest on tax paid late is treated as unallocated and does not attract RPS (SAM glossary, "Overpayment (RPS purposes)").

SAM60030 notes RPS and interest can both accrue for an overlapping period, which may disadvantage the taxpayer; HMRC's instruction is to correct the SA record where that has happened, "regardless of cause".

---

## 10. Late payment penalties

Full treatment belongs on the penalties page; what follows is the payment-side summary.

### 10.1 Current regime (2010-11 onwards): Schedule 56 FA 2009

| Trigger | Penalty | Source |
|---|---|---|
| Tax unpaid at the penalty date (30 days after the due date) | 5% of tax unpaid | CH155120; SAM61250; SAM61390 |
| Tax still unpaid 5 months after the penalty date (i.e. 30 days + 5 months after the due date) | Further 5% | CH155140; SAM61390 |
| Tax still unpaid 11 months after the penalty date (i.e. 30 days + 11 months after the due date) | Further 5% | CH155160; SAM61390 |

Note a presentational discrepancy in the sources: SAM (glossary, "Penalties") describes the three charges as arising "at 30 days, 6 months and 12 months after the due date", whereas SAM61390 and CH155160 express them as 30 days, 30 days + 5 months, and 30 days + 11 months. These describe the same dates; the CH/SAM61390 formulation is the precise one.

Penalty dates where the tax arises other than on a timely return (CH155200):

| Route | Penalty date |
|---|---|
| Determination or assessment made in the absence of a return | 31 days after the due date that would have applied if the tax had been shown on a timely return |
| Assessment, amendment or correction of a return | 31 days after the due date for the further tax |

Payments on account do not themselves attract a late payment penalty or surcharge, but an unpaid POA balance rolling into the following 31 January balancing payment does: SAM61250 lists the penalty base as including "outstanding POA at balancing payment due date", and EM4100 makes the same point for the surcharge regime.

CH155180 gives a worked total of £2,150 on a £21,000 balancing payment for 2011/12.

Class 2 NIC voluntary contributions are outside DMB pursuit: if unpaid after 31 January the amount collected is reduced to what was paid, or to zero (SAM50040 caveats).

### 10.2 The former surcharge regime (2009-10 and earlier)

TMA 1970 s.59C imposed a 5% surcharge on tax unpaid more than 28 days after the due date (s.59C(2)) and a further 5% on tax still unpaid more than six months after the due date (s.59C(3)). The surcharge was payable within 30 days of imposition (s.59C(6)), with interest charged on it thereafter. Inability to pay was expressly not a reasonable excuse and not grounds for appeal (s.59C(10)). No surcharge was due where a tax-geared penalty under ss.7, 93(5), 95 or 95A was sought on the same tax (s.59C(4)).

Surcharges have not been charged for years after 2009-10; they were replaced by Schedule 56 FA 2009 penalties for balancing payments due on or after 31 January 2012 (CH404300 Note; EM4100). CH404300 warns that Schedule 56 late payment penalties "must not be withdrawn in the same way surcharges are cancelled, as they apply independently of other penalties".

### 10.3 Coming change

Schedule 26 FA 2021 late payment penalties (currently VAT-only, for periods starting on or after 1 January 2023) are stated to apply to ITSA **from April 2026** (CH150500; CH193080). The Schedule 26 structure is a 15-day grace period, then a first penalty (2% of the amount outstanding at day 15 plus 2% at day 30; 3%/3% for periods with tax due on or after 31 May 2025 where the period began on or after 1 April 2025), then a second penalty accruing daily from day 31 at 4% per year (10% for the later periods) (CH193120; CH193140; CH193160). Under that regime a Time to Pay proposal made within the first 15 days prevents penalties entirely, and proposing TTP stops penalties accruing from the date proposals were made; breaking a TTP allows HMRC to cancel it and charge penalties as if it had never had effect (CH193160). **These rules are not yet in force for Self Assessment income tax** — the sources give an April 2026 commencement for ITSA but no further ITSA-specific detail.

---

## 11. Payment mechanics, allocation and enforcement

### 11.1 Allocation of payments

A posted payment is automatically linked to overdue SA charges, or to charges becoming due within the next **45 days** — a variable parameter that can be changed. Otherwise it is held as an excess credit or unallocated amount (SAM glossary, "Payment allocation"). Where a re-allocation involves more than one payment, payments are re-allocated in effective date of payment order, most recent EDP first (SAM glossary, "Multiple payment re-allocations").

The payslip reference is the UTR plus the suffix "K" (e.g. 3453897644K), identifying the payment as being for SA (SAM glossary, "Payslip reference number"). Bank lodgement transaction limits: a maximum of 20 cheques with one payslip, or 99 payslips with one cheque (SAM glossary).

TMA 1970 s.70A provides that a payment by cheque is treated as made on the date the cheque is received, if it is honoured on first presentation, for the purposes of the repayment supplement and interest provisions.

A "payment shortfall" arises on a balancing payment where an arrangement includes an earlier liability paid before the balancing payment due date, causing interest to be cleared ahead of the balancing payment — which triggered a surcharge under the old regime (SAM glossary, "Payment shortfall").

### 11.2 Recovery

Penalties under Parts 2, 5A and 10 TMA, Schedule 18 FA 1998, Schedule 26 FA 2021, certain items of Schedule 56 FA 2009, and interest charged under TMA or FA 2009 s.101 are treated **as if they were tax** for the collection and enforcement provisions in TMA 1970 ss.61, 63, 65–68 (TMA 1970 s.69). The cash limit for magistrates' court recovery proceedings is **£2,000** (TMA 1970 s.65(1)).

An executor or administrator is liable for the deceased's tax, payable out of the estate, and may be proceeded against as any other defaulter on neglect or refusal (TMA 1970 s.74).

Where a claim to reduce payments on account is made **after** a levy/poinding or a judgment/decree, the taxpayer remains liable for the full costs incurred in distraint or court action (SAM1080). Where an invalid claim is received and the balancing payment due date has passed, HMRC's instruction is to continue enforcement, maintain full costs, and accept only an SA return as evidence that the POA are excessive (SAM, "Recovery action following an invalid claim").

### 11.3 Revenue Determinations

If a return is not filed, HMRC may raise a Revenue Determination of tax due and unpaid (TMA 1970 s.28C), notified on form SA323. Time limits: within 5 years from the filing date up to 31 March 2010; **within 3 years from the filing date from 1 April 2010** (SAM50040; TMA 1970 s.28C(5)). A self assessment can only supersede a determination before the end of 12 months from the date of the determination (s.28C(5)). There is **no right of appeal** against a determination; filing the return displaces it and automatically amends tax, interest, surcharge and payments on account (SAM50040). DMB policy — not a legislative requirement — is to allow 30 days after a determination before enforcement action such as distraint or county court proceedings (SAM50040).

### 11.4 Payments on account requested during an enquiry

HMRC officers may ask for a payment on account once additional tax and NICs due are established but the enquiry is not complete; they must not ask for more than the amount already established as due (EM1936). If the taxpayer declines, the officer is to consider a jeopardy amendment and/or discovery assessment (EM1936; EM1950; EM3250). Before repaying a general payment on account, the officer must contact DMB to check for outstanding debts and reallocate where any exist (EM1937). A payment on account made for a period before the FA07/FA08 penalty rules may be taken into account in abatement for co-operation (EM1936; EM6075), but the reduction for quality of disclosure is not affected by payments on account (CH82400).

### 11.5 Reducing payments on account in anticipation of a relief

Two helpsheets describe using a POA reduction claim to obtain in-year benefit of a relief:

- **CITR (HS237)**: an investor may write to HMRC to ask to reduce SA payments on account to reflect expected Community Investment Tax Relief, or to change the current year's PAYE code. A formal claim cannot be made until the Tax Relief Certificate is received and the tax year has ended. If POA are reduced but the relief due turns out to be less than expected, HMRC will charge interest on the shortfall (HS237 s.4 and caveats).
- **EIS/VCT (SAM1001)**: where a PAYE code adjustment is not possible, relief can be given against payments on account via a claim to adjust; if the claim proves excessive on receipt of the return, interest is charged on the reinstated amount from the relevant POA due dates.

---

## 12. Gaps in the sources

The supplied notes do not cover, and this page therefore does not state:

- **Current de minimis figures.** SALF302 quotes £1,000 and the 1-in-5 (80%) ratio as originally set by SI 1996/1654 while warning the limits have been amended by later regulations. SAM1100/SAM1110 quote £1,000 as current. No note gives the current statutory instrument or a current proportion figure.
- **Current interest rates.** The notes describe the rate-setting mechanism (FA 1989 s.178; FA 2009 s.103, tracking bank base rate) and reference the GOV.UK page "Rates and allowances: HMRC interest rates for late and early payments", but no actual percentage rates for late payment or repayment interest are supplied. The differential between the late payment and repayment rates is not given.
- **Payment methods and timing.** No note describes the practical payment channels available to taxpayers (Direct Debit, faster payments, debit card, at a bank, by post), the working-day rules for when each is treated as received, or the GOV.UK "Pay your Self Assessment tax bill" guidance content, beyond the internal SAM references to BACS, CHAPS, Bank Giro, Girobank and cheque processing and the s.70A cheque rule.
- **Current Time to Pay eligibility criteria and the online self-serve threshold.** The notes describe TTP mechanics and penalty interaction but give no current debt threshold, maximum instalment period for ordinary SA TTP, or online arrangement limits.
- **Budget Payment Plans.** Not mentioned in any note.
- **Schedule 26 FA 2021 as applied to ITSA.** The notes state it applies to ITSA from April 2026 but give only the VAT-specific mechanics; no ITSA-specific due dates, thresholds or transitional rules are supplied.
- **Certificates of Tax Deposit.** EM6020 notes CTDs closed to new purchases from 23 November 2017 with existing certificates honoured for six years only; the notes do not indicate whether any remain live.
- **The £17,000 coding-out cap under ITEPA 2003 s.684(3A)** is stated, but the notes do not reconcile it with the £3,000 SA balancing payment coding limit or the graduated scale, beyond SAM141045's statement that the graduated scale does not apply to SA balancing charges.

---

## Sources used on this page

This page was written by an LLM from structured notes extracted from the mirrored sources below. Always check the upstream source before relying on any figure or deadline.

- [govuk-sa-detailed-information](https://www.gov.uk/government/collections/self-assessment-detailed-information) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/govuk-guidance.md`
- [sa-helpsheets:5f67dfee-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/accrued-income-scheme-hs343-self-assessment-helpsheet) - 2 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/accrued-income-scheme-self-assessment-helpsheet-hs343.md`
- [sa-helpsheets:5f67d41e-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/employee-share-and-security-schemes-and-capital-gains-tax-hs287-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/capital-gains-tax-and-employee-share-schemes-self-assessment-helpsheet-hs287.md`
- [sa-helpsheets:5f67cf48-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/community-investment-tax-relief-hs237-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/community-investment-tax-relief-self-assessment-helpsheet-hs237.md`
- [sa-helpsheets:5f67dc31-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/employee-shares-and-securities-further-guidance-hs305-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/employment-related-shares-and-securities-self-assessment-helpsheet-hs305.md`
- [sa-helpsheets:5f67dd70-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/interest-and-alternative-finance-payments-eligible-for-relief-on-qualifying-loans-and-alternative-finance-arrangements-hs340-self-assessment-helpshee) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/interest-and-alternative-finance-payments-eligible-for-relief-on-qualifying-loans-and-alternative-finance-arrangements-self-assessment-helpsheet-hs340.md`
- [sa-helpsheets:5f67e282-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/limit-on-income-tax-reliefs-hs204-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/limit-on-income-tax-reliefs-self-assessment-helpsheet-hs204.md`
- [hmrc-manual-ch](https://www.gov.uk/hmrc-internal-manuals/compliance-handbook) - 13 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/ch.md`
- [hmrc-manual-em](https://www.gov.uk/hmrc-internal-manuals/enquiry-manual) - 9 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/em.md`
- [hmrc-manual-salf](https://www.gov.uk/hmrc-internal-manuals/self-assessment-legal-framework) - 5 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/salf.md`
- [hmrc-manual-sam](https://www.gov.uk/hmrc-internal-manuals/self-assessment-manual) - 40 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/sam.md`
- [hmrc-rates-allowances](https://www.gov.uk/government/collections/rates-and-allowances-hm-revenue-and-customs) - 1 note(s) - mirrored at `corpus/hmrc-publications/rates-and-allowances.md`
- [itepa-2003](https://www.legislation.gov.uk/ukpga/2003/1/contents) - 1 note(s) - mirrored at `corpus/legal-system/primary-legislation/acts/itepa-2003.md`
- [tma-1970](https://www.legislation.gov.uk/ukpga/1970/9/contents) - 3 note(s) - mirrored at `corpus/legal-system/primary-legislation/acts/tma-1970.md`
