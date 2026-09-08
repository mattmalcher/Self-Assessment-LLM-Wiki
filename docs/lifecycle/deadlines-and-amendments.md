---
title: Deadlines, amendments and corrections
generated: true
generated_on: '2026-09-08'
generated_by: claude-cli:opus
input_hash: 5bc2f08d143fa4ce
note_count: 80
sources:
- hmrc-manual-artg
- hmrc-manual-ch
- hmrc-manual-em
- hmrc-manual-salf
- hmrc-manual-sam
- sa-helpsheets:5f67ceae-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67d46f-7631-11e4-a3cb-005056011aef
- sa-helpsheets:f689f4a2-7da1-41a3-b37d-b18c346219ed
- tma-1970
---

# Deadlines, amendments and corrections

!!! danger "Unofficial - not HMRC, not advice, written by an LLM"

    This page is **not** an HMRC publication and has no connection to HMRC or
    any government body. It was **written by a language model** from mirrored
    source material, and can be wrong, incomplete or out of date. It is not
    tax advice. Check every figure, date and rule against the cited source
    before relying on it, and see
    [GOV.UK](https://www.gov.uk/self-assessment-tax-returns) for official
    guidance.

This page sets out the statutory dates that govern a Self Assessment return: when it must be filed, how the filing date shifts when the notice to file is issued late, how long the taxpayer has to amend, and how long HMRC has to correct. Each rule is stated in a form that can be evaluated from a small number of inputs — the tax year, the date of the notice to file, the date the return was delivered, and whether filing was on paper or electronically. Statute (Taxes Management Act 1970) is distinguished throughout from HMRC's own manual guidance, which is HMRC's interpretation and not law.

---

## 1. The two anchor concepts

Almost every date on this page derives from one of two anchors.

| Concept | Definition | Source |
|---|---|---|
| **Filing date** | The date by which the return must be delivered, as specified in the legislation for that tax (TMA 1970 s.8(1)(a) for individuals). | CH61140 (HMRC's gloss); TMA 1970 s.8(1)(a) |
| **Penalty date** | The day after the filing date; the day on which liability to the initial fixed penalty first arises. | CH61160; FA09/Sch55/para 1 |

Note the terminological trap: **the "filing date" used to compute the taxpayer's amendment window is not always the date by which the return actually had to be filed.** For s.9ZA purposes the filing date is defined by s.9ZA(3) and is 31 January of Year 2 regardless of whether the return was filed on paper or online (SAM124165 flags this as "commonly misunderstood" — a paper filer for 2007-08 onwards may have longer to amend than the paper filing deadline would suggest).

---

## 2. Filing deadlines — individuals and trustees (s.8 / s.8A returns)

### 2.1 The standard cases

| Case | Filing date | Source |
|---|---|---|
| Paper return, notice to file given on or before 31 July following the end of the tax year | 31 October following the end of the year of assessment | TMA 1970 s.8(1)(a); SALF202 |
| Electronic return, notice given on or before 31 October following the end of the tax year | 31 January following the end of the year of assessment | TMA 1970 s.8(1)(a); SALF202 |
| Notice to file (or a return containing the notice) given **after 31 July** following the end of the tax year | 3 months beginning with the date of the notice — or 31 January if later, where filed electronically | TMA 1970 s.8(1D)–(1G); SALF202 |

CH62100 confirms the same two dates for ITSA in the penalty context — 31 October for paper, 31 January for electronic — and adds an operational instruction that where the filing method is not yet known, HMRC assumes 31 January.

### 2.2 As an implementable rule

```
inputs: tax_year_end (5 April, year Y1), notice_date, method ∈ {paper, electronic}

paper_filing_date =
    if notice_date <= 31 July of Y2  -> 31 October of Y2
    else                              -> notice_date + 3 months

electronic_filing_date =
    if notice_date <= 31 October of Y2 -> 31 January of Y2+1
    else                                -> max(31 January of Y2+1, notice_date + 3 months)
```

Where "Y2" is the calendar year in which the tax year ends (e.g. for 2024-25, Y2 = 2025).

**Two operational caveats from HMRC's manuals, which are practice rather than statute:**

- SAM120070 records that HMRC applies a **concessionary "3 months and 7 days"** from the date of issue where a return or SA316 was issued after 31 October following the end of the return year *and* there was no failure to notify. SAM120100 uses the same 3 months and 7 days for a return filed after a withdrawn notice is reinstated by an SA833. EM1505 explains the extra 7 days as allowance for printing, issue and postal delivery. This is HMRC's administrative practice, not the s.8(1D)–(1G) period.
- EM4570 records a further HMRC practice under the *old* penalty regime: the £100 fixed penalty was charged only where the return was not received by the end of 1 February. The manual is explicit that this was administrative practice and did not move the statutory filing date of midnight on 31 January. SAM (glossary, "Filing date") and SAM125050 record that **from October 2011 a return received on 1 November is treated as late and attracts a penalty**.

### 2.3 Delivery

SALF203 states HMRC's view that "deliver to the officer" generally means the return is received at an HMRC office on or before the relevant day, with delivery accepted up to midnight, including returns found in the post box at the start of the next day.

### 2.4 The HMRC-calculation variant

If the taxpayer wants HMRC to calculate the tax rather than self-assessing, an earlier deadline applies:

| Case | Deadline | Source |
|---|---|---|
| Standard | 31 October following the tax year | TMA 1970 s.9(2)(a) |
| Notice under s.8/8A given **after 31 August** following the tax year | 2 months beginning with the day the notice is given | TMA 1970 s.9(2)(b) |

This is a condition of being excused from including a self-assessment under s.9(1), not a filing deadline in itself. SALF204 notes that a return filed without a tax calculation outside these limits is "in strictness unsatisfactory"; HMRC may still calculate it but does not guarantee timely notification. SALF204 also records that where HMRC exceptionally fails to notify the tax due in time despite the taxpayer having filed within the s.9(2) limit, any interest or penalty attributable to HMRC's delay will be waived — an HMRC concession, not a statutory entitlement.

SAM (All cases) adds that HMRC cannot promise to calculate tax before 31 January following the end of the SA year where a signed return is received close to 31 October.

---

## 3. Voluntary returns

A voluntary return is one delivered where HMRC has not given a notice to file. SALF202 records that, following legislation put beyond doubt from 12 February 2019 with retrospective and prospective effect, such a return is treated as made in response to a notice to file given on the date the return was received.

| Case | Filing date | Source |
|---|---|---|
| Voluntary paper return | 31 October following the end of the tax year, unless received after 31 July, in which case 3 months from the date received | SALF202; EM (Voluntary Returns) |
| Voluntary electronic return | 31 January following the end of the tax year, unless received after 31 October, in which case 3 months from the date received | SALF202; EM (Voluntary Returns) |

Consequence: a voluntary return is always treated as delivered on or before the filing date, so **no late filing penalty can arise** (SALF202/SALF203; EM Voluntary Returns).

---

## 4. Filing deadlines — partnership returns (s.12AA)

The partnership filing date depends on the composition of the partnership.

| Partnership type | Paper | Electronic | Source |
|---|---|---|---|
| Individuals only | 31 October following the tax year | 31 January following the tax year | TMA 1970 s.12AA(4); EM7526 |
| Individuals only, notice given after 31 July (paper) / after 31 October (electronic) | 3 months from date notice given | 3 months from date notice given (or 31 January if later) | TMA 1970 s.12AA(4A)–(4E); EM7526; SALF506 |
| Companies only | Not earlier than 9 months from the end of the period covered | 12 months from the end of the period covered | TMA 1970 s.12AA(5); EM7526 |
| Companies only, notice given more than 9 months after period end | 3 months from date notice/return given | 3 months from date notice/return given | TMA 1970 s.12AA(5A)–(5D) |
| Mixed (individuals and companies) | The later of the individual-partner date and the company-partner date | Same | EM7526 |

SALF506 restates the mixed-partnership position by reference to the accounting date: where it falls 6 April–31 January, 31 October (paper) / 31 January (online); where it falls 1 February–5 April, 9 months (paper) / 12 months (online) after the accounting date. SAM120034/SAM120035 give worked tables for solely-company and solely-individual partnerships and flag an anomaly for 2008-09 online returns where a year to 31 March 2009 produces a filing date of 31 March 2010, not 31 January 2010, because the 12-month rule yields the later date.

Voluntary partnership returns follow the individual pattern: 31 October (paper) / 31 January (online), or 3 months from delivery where received after 31 July / 31 October respectively (EM7526). SAM122090 states that an unsolicited partnership return in proper form is treated as filed on 31 October, or on the date received where received after 31 October following the end of the tax year.

EM7526 warns that the presence of a corporate partner may create non-standard filing dates and cross-refers to PM147000, which is not in the notes supplied.

---

## 5. The taxpayer's amendment window

### 5.1 The rule

| Return type | Amendment window | Source |
|---|---|---|
| Personal or trustee return (s.8 / s.8A) | Not more than **12 months after the filing date** | TMA 1970 s.9ZA(1)–(2) |
| Partnership return | Not more than **12 months after the filing date** | TMA 1970 s.12ABA(2); EM7527; SALF506 |
| Claim made *in* a return | Up to 12 months after the fixed filing date | TMA 1970 s.9(4)(b); SAM114080 |
| Claim made *outside* a return (Sch 1A) | Up to 12 months after the date of receipt of the claim | TMA 1970 Sch 1A para 3(1)(b); SAM114080 |

Amendments must be made by notice to an officer (s.9ZA(1)). SAM124165 and SAM (General) record HMRC's operational requirement that the amendment be **in writing** — a letter, an amended return, or an amended/extra supplementary page — and that HMRC accepts amendments from the taxpayer, trustee or an authorised agent, reserving the right to satisfy itself that an agent-submitted amendment was actually authorised.

### 5.2 "Filing date" for s.9ZA purposes

This is the critical computation. s.9ZA(3) defines the filing date for a return for Year 1 as:

- **31 January of Year 2**; or
- if the notice under s.8/8A was given **after 31 October of Year 2**, the last day of the period of **three months beginning with the date of the notice**.

SALF204 adds the voluntary-return variant: 31 January if the voluntary return was received by 31 October, otherwise the last day of 3 months from delivery.

SAM124165, SAM (General) and SAM (Taxpayer amendments) all restate this as "31 January following the end of the tax year, or 3 months from receipt of a Notice to File (if late issue), whichever is later."

```
inputs: tax_year_end (Y1/Y2), notice_date

s9ZA_filing_date =
    if notice_date <= 31 October of Y2 -> 31 January of Y2+1
    else                                -> notice_date + 3 months

amendment_deadline = s9ZA_filing_date + 12 months
```

**Worked examples from EM1506 (2020-21, reflecting that year's extended dates):**

| Notice given | Filing date | Amend by |
|---|---|---|
| On or before 31 October 2021 | 31 January 2022 | 31 January 2023 |
| 1 November 2021 | 1 February 2022 | 1 February 2023 |

EM1506 flags these as specific to 2020-21 and reflecting a filing-date extension for that year that may not generalise.

### 5.3 Consequences that follow from the definition

- **Paper filers may have longer to amend than the paper filing deadline suggests.** The s.9ZA filing date is 31 January (or the late-notice date) irrespective of filing method. SAM124165 explicitly notes this is commonly misunderstood.
- **Late filing shortens nothing on the amendment side but shortens HMRC's correction window** — see §6. SALF204 makes the point directly: the 9-month HMRC correction window runs from the date the return was delivered, whereas the 12-month amendment window runs from the statutory filing date.
- **An ongoing enquiry does not extend the amendment window.** EM7554 states this for partnership returns; SALF506 says the same for the partnership's amendment right.

### 5.4 Amendments while an enquiry is open

Under s.9B, if a return is under enquiry the taxpayer may still amend within the normal time limit, but the amendment **does not take effect until the enquiry is completed** (SALF204). EM1906 records HMRC's instruction that officers must not process taxpayer amendments received during an enquiry until the enquiry into that matter is concluded by a partial closure notice, final closure notice or contract settlement. Where a partial closure notice is issued, EM1906 says HMRC should consider allowing amendments relating to the matter being settled by that PCN.

EM7556 explains the partnership analogue: an amendment that does not affect amounts in the partnership statement takes effect immediately; one that does is deferred until the enquiry concludes, and may never take effect if the closure notice incorporates it or concludes it was incorrect.

### 5.5 After the amendment window closes

| Situation | Route | Time limit | Source |
|---|---|---|---|
| Taxpayer overpaid | Overpayment relief claim under Sch 1AB TMA 1970 | 4 years from the end of the relevant tax year | SAM124040; Sch 1AB TMA 1970 |
| Taxpayer overpaid (alternative framing in SAM101080) | Overpayment relief, Section 1AB | Within 4 years of the filing date of the return for the year concerned | SAM101080 |
| Taxpayer underpaid | Notify HMRC so corrective action can be taken; HMRC considers enquiry or discovery assessment | — | SALF204; EM1906/EM3250 |
| Mistake in a partnership return affecting a partner | Claim under s.33 / Sch 1AB | No later than 4 years after the end of the relevant tax year | SALF506 |

**Note the source disagreement on the overpayment relief clock.** SAM124040 says "4 years from the end of the relevant tax year"; SAM101080 says "within 4 years of the filing date of the return for the year concerned". These are different dates. The statutory reference given in both is s.1AB / Sch 1AB TMA 1970, and the notes do not reproduce the statutory wording, so the discrepancy cannot be resolved from the sources supplied.

Sch 1AB overpayment relief replaced the old s.33/s.33A "error or mistake relief" from April 2010 (SAM101075; SAM Taxpayer amendments). Older references to s.33 relief do not apply to amendments after that date.

SAM125210 records that HMRC's online service rejects an amendment submitted more than 12 months after the statutory due date and issues a message that the amendment window has closed.

---

## 6. HMRC's correction power

### 6.1 The rule

An officer may amend a return "so as to correct obvious errors or omissions in the return (whether errors of principle, arithmetical mistakes or otherwise)" and anything else the officer has reason to believe is incorrect in light of information available.

| Return type | Correction window | Source |
|---|---|---|
| Personal / trustee return | Not more than **9 months after the day the return was delivered**, or after a s.9ZA amendment was made | TMA 1970 s.9ZB(1),(3) |
| Partnership return | Not more than **9 months after the day the return was delivered**, or after a s.12ABA amendment | TMA 1970 s.12ABB(1),(3); SAM122230 |
| A taxpayer amendment | 9 months from the date the amendment is received | SAM124165; SAM (General) |
| A Sch 1A claim (outside a return) | Before the end of 9 months beginning with the day the claim is made | TMA 1970 Sch 1A para 3(1)(a) |
| Class 2 NIC auto-correction | Within 9 months following the date the completed return was filed | SAM124035 |

```
correction_deadline = date_return_delivered + 9 months
                      (restarts from the date of any s.9ZA amendment)
```

Because the clock runs from **delivery**, not from the filing date, a return filed late has a correspondingly shorter correction window measured from a later start point (SALF204).

### 6.2 Rejecting a correction

The taxpayer may reject a correction by notice, before the end of the period of **30 days beginning with the date of issue of the notice of correction** (TMA 1970 s.9ZB(4),(5)). If rejected, the correction has no effect. The partnership equivalent is s.12ABB(4),(5), exercisable by the partner who made and delivered the return (or successor); SAM122225 cites TMA 1970 s.9BZ(4) and (5) for the partnership rejection right.

**There is no right of appeal against a correction — only the right of rejection** (EM7528; EM1505). EM7528 adds that if the nominated partner does not reject a correction, HMRC can only dispute a subsequent amendment by the partner by enquiring into the amended return.

SAM122225 records HMRC's operational practice that the 30-day rejection rule is "only applied where a return is filed 11 months after the filing date or later."

### 6.3 What may be corrected

SAM122230 defines "obvious errors" as errors shown up by the computer while entering return details, e.g. arithmetical errors or carrying forward the wrong figure from one box to another; it says small mistakes should not be repaired. EM7528 defines an obvious error or omission as one where "there can be no doubt what the correct entry should be", including arithmetical errors and errors of principle.

Internal constraints HMRC imposes on itself (manual guidance, not law):

- HMRC must not use third-party information not supplied by the partnership to repair an obvious error on a partnership return (SAM122225).
- SAM (Information used in making a repair) says HMRC officers must not change the customer's figures if they cannot be checked against information held on HMRC systems, and must inform the customer or agent of any correction made, via a customer service message or SEES letter SA806.
- Entries forming part of Standard Accounts Information must be referred to HO Tech before repair (SAM122231; SAM121531).
- Corrections must be described to the taxpayer as "revisions", not "repairs" (SAM122225).
- Where a repair increases liability, is processed after 31 December following the end of the return year, and no repayment is due, HMRC must not make the repair via CAPTURE RETURN, because the penalty/surcharge dates would be computed incorrectly (SAM121540; SAM123280/SAM123281 for trusts).

### 6.4 Consequential corrections to partners

Where HMRC corrects a partnership return, it must issue a notice to each partner making corresponding amendments to their self assessments and send a copy of the revised partnership statement with SEES letter SA839 (SAM122230). EM7528 states HMRC must correct partners' returns to give effect to corrections to the partnership return and notify partners in writing. The statutory hook is s.12ABB(6)(a) (referenced in s.59B(5)).

### 6.5 Penalties arising from a correction

SALF204 records that penalties can arise where an HMRC correction under s.9ZB increases the tax due and the inaccuracy is shown to be careless or deliberate. CH83040/CH83050 (FA07/Sch24) give the penalty assessment time limit where a person puts an inaccuracy right themselves — e.g. by amending an SA return — as **within 12 months of the date the correction was made**.

---

## 7. Summary timeline for a standard year

For a 2024-25 return, notice to file given in April 2025, filed electronically on 31 January 2026:

| Event | Date | Source |
|---|---|---|
| Tax year ends | 5 April 2025 | — |
| Notify chargeability (if no notice to file received) | 5 October 2025 | TMA 1970 s.7(1); SALF210 |
| Paper filing date | 31 October 2025 | TMA 1970 s.8(1)(a) |
| Electronic filing date | 31 January 2026 | TMA 1970 s.8(1)(a) |
| Balancing payment due | 31 January 2026 | TMA 1970 s.59B(4) |
| Penalty date (electronic filer) | 1 February 2026 | CH61160 |
| HMRC correction window closes (delivered 31 Jan 2026) | 31 October 2026 | TMA 1970 s.9ZB(3) |
| Enquiry window closes (filed on time) | 31 January 2027 | TMA 1970 s.9A(2); EM1506 |
| Taxpayer amendment window closes | 31 January 2027 | TMA 1970 s.9ZA(2)–(3) |
| Ordinary assessment time limit | 5 April 2029 (4 years from end of year) | TMA 1970 s.34(1) |
| Determination time limit (if no return filed) | 3 years from the filing date | TMA 1970 s.28C(5) |

---

## 8. Related windows that depend on these dates

### 8.1 Enquiry window (s.9A(2) / s.12AC(2))

Included because the enquiry window keys off the same delivery and filing dates.

| Case | Enquiry window closes | Source |
|---|---|---|
| Return delivered on or before the filing date (from 1 April 2008) | 12 months from the date the return was delivered | TMA 1970 s.9A(2); EM1506; SAM31100 |
| Return delivered after the filing date | The quarter day next following the first anniversary of the day the return was delivered | TMA 1970 s.9A(2)(b); EM1506 |
| Following a taxpayer amendment | The quarter day next following the first anniversary of the day the amendment was made | TMA 1970 s.9A(2)(c); EM1506 |
| Notice to file given on or after 1 November following the tax year, return filed on time | 12 months after the date the return was made and delivered | TMA 1970 s.8(1G), s.9A(2); EM1508 |
| Voluntary return | 12 months from the date the return is received | EM1506; EM7553 |
| Partnership return following a s.12ABZB tribunal referral | The quarter day next following the first anniversary of the day HMRC received notification of the referral | TMA 1970 s.12AC(2)(d) |

**Quarter days are 31 January, 30 April, 31 July and 31 October** (TMA 1970 s.12AC(2); EM1506).

Historic position: for returns up to and including 2006-07 the window ran to 12 months after the fixed filing date (SAM31100). For years up to 2000-01 with a 31 January filing date, SAM (glossary) records the last date for enquiry as **30 January** of the following year; from 2001-02 it became 31 January. EM1506 attributes the change from 30 January to FA 2001. These historic rules do not apply to modern returns.

For an enquiry to be valid, the s.9A or s.12AC opening notice must actually be **received** by the taxpayer (or nominated partner) by the end of the window, not merely posted (SAM31100; EM1506). SAM31100 gives assumed receipt of 2 working days after posting (first class) and 4 working days (second class), unless evidence of actual receipt is provided. EM1506 instructs officers to use tracked delivery where a notice is issued within one week of the last date for enquiry. Both manuals note that Royal Mail's second-class delivery pattern changed from 28 July 2025, affecting deemed-delivery assumptions.

A return, amendment or claim can be enquired into only once (TMA 1970 s.9A(3), s.12AC(3), Sch 1A para 5(3); EM1530). An amendment does not change the enquiry period for the original return; there is a separate window for the amendment itself (EM1506).

### 8.2 Payment dates driven by amendments and corrections

| Trigger | Payment due | Source |
|---|---|---|
| Standard balancing payment | 31 January next following the year of assessment | TMA 1970 s.59B(4) |
| s.7 notice given within 6 months of year end but s.8/8A notice given after 31 October following the year | End of 3 months beginning with the day the s.8/8A notice was given | TMA 1970 s.59B(3) |
| Voluntary return delivered after 31 October following the year | 3 months from the date the voluntary return was received | s.59B(3)–(6) and Sch 3ZA; SALF303 |
| Amendment or correction (s.9ZA, s.9ZB, s.9C, s.28A, s.12ABZB(8), s.12ABA(3)(a), s.12ABB(6)(a), s.30B(2)(a), s.33A(4)(a), s.50(9)(a)) | The day specified by the relevant provision of Sch 3ZA — in practice the later of the normal due dates or 30 days from the date the notice of amendment is given | TMA 1970 s.59B(5); SALF303 |
| Assessment other than under s.9, s.28H or s.28I (including a discovery assessment) | The day following the end of 30 days beginning with the day the notice of assessment is given | TMA 1970 s.59B(6) |
| Additional tax following a closure notice | Within 30 days after the partial or final closure notice is given | TMA 1970 s.28A(2)(b), s.28B(2)(b), Sch 3ZA para 5; EM3852 |

SALF303 notes an important asymmetry for **interest**: for amendments and discovery assessments, interest runs from the original due dates for the relevant tax year even though the payment due date itself may be later. CH143020 makes the same point in HMRC's own words — the late payment interest start date for a corrected or amended assessment is the date the tax would have been due had the original assessment been complete and accurate, not the date of the amendment, and describes this as "a commonly misread point."

SAM (General) and SAM123280 record HMRC's operational rule that where a repair increases liability, payment is due on the later of the original due date or 30 days from the date the taxpayer is issued with the revised Tax Calculation.

### 8.3 Determinations where no return is filed

| Rule | Time limit | Source |
|---|---|---|
| HMRC may determine the tax due to the best of the officer's information and belief | No determination after 3 years beginning with the filing date | TMA 1970 s.28C(1),(1A),(5) |
| Taxpayer's actual self assessment supersedes the determination | Within the 3-year period, or if later within 12 months of the date of the determination | TMA 1970 s.28C(6) |

There is **no right of appeal against a determination** and no right of postponement; it stands as if it were a self assessment until superseded (EM2026; SALF209). EM2026 records HMRC's internal view that a determination is most effective if issued within 12 months of the filing date, and that the earlier 31 October paper deadline is not used when computing the determination time limit for ITSA.

### 8.4 Withdrawal of a notice to file

For 2012-13 onwards a notice to file can be formally withdrawn on request (SAM120100; TMA 1970 s.12AAA for partnerships).

| Rule | Limit | Source |
|---|---|---|
| Individuals and non-corporate partnerships | Request within 2 years beginning with the end of the year of assessment, or a period agreed with HMRC | SAM120100; TMA 1970 s.12AAA |
| Partnerships including one or more companies | Within 2 years beginning with the end of the relevant period for which the return was required | SAM120100; TMA 1970 s.12AAA |
| Notifying chargeability after a withdrawal notice (SA832) | The later of 6 months from the end of the year of assessment, or 30 days beginning the day after the notice was withdrawn | SAM120100 |
| Filing after a new notice to file (SA833) is issued | The latest of 3 months and 7 days, or the normal filing date | SAM120100 |

If HMRC agrees to withdraw a notice to file, late filing penalties already charged are cancelled (FA09/Sch55 para 17A; CH61700; CH64280). SAM120100 records that withdrawal cannot occur where a determination is in place or a return has already been received, and there is **no right of appeal against HMRC's decision not to withdraw** (EM7525). SAM120100 also notes that original payment due dates continue to apply under s.59B(4) even where a new SA833 notice is issued after chargeability is established post-withdrawal.

---

## 9. Penalty dates keyed to the filing date

These are included only to the extent they are computed from the deadlines above; the penalty regime itself is out of scope for this page.

| Penalty | Trigger date | Amount | Source |
|---|---|---|---|
| Initial fixed | Penalty date (day after filing date) | £100 | FA09/Sch55 para 3; CH62100 |
| Daily | Return outstanding 3 months after the penalty date; HMRC must give written notice specifying the start date, which must be at least 3 months after the penalty date | £10/day, max 90 days | FA09/Sch55 para 4; CH62120 |
| 6-month | 6 months after the penalty date | Greater of 5% of the liability that would have been shown and £300 | FA09/Sch55 para 5; CH62140 |
| 12-month | 12 months after the penalty date | Greater of £300 and 100% (deliberate and concealed) / 70% (deliberate) / 5% (not deliberate) | CH62080; CH62160+ |

Schedule 55 FA 2009 applies to ITSA for returns for the year ended 5 April 2011 onwards, due 31 October 2011 (paper) / 31 January 2012 (electronic), subject to exceptions at SAM121025 (CH61120). For 2009-10 and earlier, the s.93 TMA 1970 regime applied (£100 fixed, further £100 at 6 months, daily penalties up to £60 per day with tribunal leave) — see EM4570 and SALF506.

Penalty assessments must be issued by the later of (a) 2 years beginning with the filing date and (b) 12 months beginning with the end of the appeal period for the tax assessment (FA09/Sch55 para 19; CH64200), and must be paid within 30 days of issue (para 18(2)–(3); CH64300). Appeals against a penalty assessment run 30 days from the date of issue (SAM61240); SAM61290 records HMRC's operational allowance of **37 days** — the 30-day statutory period plus 7 days for printing and despatch.

Late payment penalties under FA09/Sch56 arise at a **penalty date 31 days after the due date**, with further 5% penalties at 5 months and 11 months after that penalty date (CH155100; CH155120; CH155140).

---

## 10. Gaps in the sources

The notes supplied do not cover the following parts of the brief, or cover them only partially:

- **The precise statutory text of s.8(1D)–(1G).** SALF202 and SALF100 paraphrase it as "3 months beginning with the date of the notice, or 31 January if later (return filed electronically)", but the notes do not reproduce the subsection wording, so the exact interaction between the paper and electronic late-notice variants (in particular whether the "or 31 January if later" limb applies to paper) cannot be verified from the sources.
- **Whether the "3 months and 7 days" concession is applied consistently.** SAM120070, SAM120100 and EM1505 all mention it, but the notes do not identify any statutory or published-concession basis for it.
- **Non-standard filing dates for particular taxpayer classes.** SAM (glossary) records exceptions to the standard paper/online dates for non-resident companies (SA700), trustees of registered pension schemes (SA970) and certain elected representatives (MPs, MSPs, Welsh and NI Assembly Members), but the notes do not state what those alternative dates are.
- **PM147000**, cross-referenced by EM7526 for non-standard partnership filing dates where a corporate partner is present, is not among the supplied notes.
- **Reconciliation of the overpayment relief time limit.** As noted in §5.5, SAM124040 and SAM101080 state the 4-year limit differently and the statutory text of Sch 1AB is not supplied.
- **The commencement date and content of the FA21/Sch26 late payment penalty regime for Income Tax Self Assessment.** CH193160 states these rules currently apply only to VAT and "will come into force for other tax regimes (including potentially Income Tax Self Assessment) at a future date"; the notes do not give an ITSA commencement date.
- **Making Tax Digital quarterly update deadlines** are covered (SALF1150/SALF1160) but their interaction with the s.9ZA amendment window and the s.9ZB correction window is not addressed in the sources.
- **Devolved or Scottish-specific variations**, if any, are not covered.

---

*This is an independent, unofficial reference page. It is not produced, endorsed or approved by HM Revenue & Customs. Where HMRC manuals are cited, they represent HMRC's stated view of the law and its internal operating practice, which is not itself law and which tribunals are not bound to follow.*

---

## Sources used on this page

This page was written by an LLM from structured notes extracted from the mirrored sources below. Always check the upstream source before relying on any figure or deadline.

- [sa-helpsheets:5f67ceae-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/averaging-for-creators-of-literary-or-artistic-works-hs234-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/averaging-for-creators-of-literary-or-artistic-works-self-assessment-helpsheet-hs234.md`
- [sa-helpsheets:f689f4a2-7da1-41a3-b37d-b18c346219ed](https://www.gov.uk/government/publications/foreign-income-and-gains-fig-regime-self-assessment-helpsheet-hs266) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/foreign-income-and-gains-fig-regime-self-assessment-helpsheet-hs266.md`
- [sa-helpsheets:5f67d46f-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/negligible-value-claims-and-income-tax-losses-on-disposals-of-shares-you-have-subscribed-for-in-qualifying-trading-companies-hs286-self-assessment-he) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/negligible-value-claims-and-income-tax-losses-on-disposal-of-shares-self-assessment-helpsheet-hs286.md`
- [hmrc-manual-artg](https://www.gov.uk/hmrc-internal-manuals/appeals-reviews-and-tribunals-guidance) - 3 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/artg.md`
- [hmrc-manual-ch](https://www.gov.uk/hmrc-internal-manuals/compliance-handbook) - 14 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/ch.md`
- [hmrc-manual-em](https://www.gov.uk/hmrc-internal-manuals/enquiry-manual) - 17 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/em.md`
- [hmrc-manual-salf](https://www.gov.uk/hmrc-internal-manuals/self-assessment-legal-framework) - 12 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/salf.md`
- [hmrc-manual-sam](https://www.gov.uk/hmrc-internal-manuals/self-assessment-manual) - 28 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/sam.md`
- [tma-1970](https://www.legislation.gov.uk/ukpga/1970/9/contents) - 3 note(s) - mirrored at `corpus/legal-system/primary-legislation/acts/tma-1970.md`
