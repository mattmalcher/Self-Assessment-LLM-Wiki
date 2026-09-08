---
title: Who must file a Self Assessment return
generated: true
generated_on: '2026-09-08'
generated_by: claude-cli:opus
input_hash: 501939e373afc890
note_count: 80
sources:
- hmrc-manual-artg
- hmrc-manual-ch
- hmrc-manual-em
- hmrc-manual-salf
- hmrc-manual-sam
- itepa-2003
- sa-helpsheets:5f67ceae-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67d46f-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67d5b1-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67db85-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dc31-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dcd2-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dfee-7631-11e4-a3cb-005056011aef
- tma-1970
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

This page sets out what actually creates an obligation to file a Self Assessment (SA) return, how HMRC decides who to send a notice to, the separate statutory duty to notify chargeability where no notice has been issued, and the routes by which a person can be taken back out of SA. It distinguishes the statutory position (Taxes Management Act 1970) from HMRC's operational criteria (the Self Assessment Manual) and HMRC's penalty interpretation (the Compliance Handbook). Nothing here is an HMRC publication or a substitute for the legislation.

---

## 1. The two distinct obligations

There are two separate things that can go wrong, and they carry different deadlines and different penalty regimes:

| Obligation | Trigger | Statutory source | Penalty regime if breached |
|---|---|---|---|
| **File a return** | HMRC gives a notice to file | TMA 1970 s.8 (individuals), s.8A (trustees), s.12AA (partnerships) | Schedule 55 FA 2009 (CH61180) |
| **Notify chargeability** | Being chargeable to IT or CGT with *no* s.8 notice (or a withdrawn one) | TMA 1970 s.7 | Schedule 41 FA 2008 (CH71220) |

The distinction matters for implementation. A person can be chargeable to tax and *not* obliged to file (because no notice was issued and s.7(3) exempts them). A person can be obliged to file and owe nothing (because a notice was issued regardless of liability).

---

## 2. The notice to file is what creates the filing obligation

A person becomes liable to file because an officer gives them a notice, not because their affairs cross some threshold. HMRC's Compliance Handbook lists the filing obligations that attract Schedule 55 penalties (CH61180):

| Who | Must deliver | Statutory reference |
|---|---|---|
| Individual (IT or CGT) | Return; and accounts, statements or documents | TMA 1970 s.8(1)(a), s.8(1)(b) |
| Trustee (IT or CGT) | Return; and accounts, statements or documents | TMA 1970 s.8A(1)(a), s.8A(1)(b) |
| Partnership (IT or CT) | Return; and accounts, statements or documents | TMA 1970 s.122AA(2), (3) — as cited at CH61180 |

For partnerships, an officer may give the notice either to a named partner (who then becomes responsible for making and delivering the return) or to the partnership, in which case the partnership must nominate a partner to complete it (EM7524; TMA 1970 s.12AA(2)–(3)). Individual partners must separately include, in their own personal return, the share of partnership profit or loss allocated to them in the partnership statement (TMA 1970 s.8(1B)).

Once a notice exists, the return must include a self-assessment of the IT and CGT chargeable and the balance payable after tax deducted at source (TMA 1970 s.9(1)) — unless the return is filed by 31 October following the year, or within two months of a notice given after 31 August, in which case HMRC makes the assessment on the taxpayer's behalf (TMA 1970 s.9(2), s.9(3)).

### Voluntary returns

A return delivered where HMRC gave no notice is a "voluntary" or "unsolicited" return. HMRC's position (SAM121140; SAM123140) is that, under law with retrospective and prospective effect from **12 February 2019**, such a return is treated as made in response to a notice to file given on the date HMRC received it. The practical consequence recorded in the manual is that the s.9A enquiry window ends 12 months after the day the return was delivered (SAM121140).

For partnerships, the equivalent treatment is that "a notice to file is treated as given to the delivering partner on the date the return was received" (EM7526).

**Machine-implementable:** `filing_obligation_exists(person, year) := notice_under_s8_or_s8A_or_s12AA_given(person, year) AND NOT notice_withdrawn(person, year)`. A voluntary return sets `notice_date := date_received`.

---

## 3. The statutory obligation to notify chargeability (s.7 TMA 1970)

Where no notice to file has been given, the duty runs the other way: the taxpayer must tell HMRC.

**The rule (TMA 1970 s.7(1)):** a person chargeable to income tax or CGT for a year of assessment who falls within subsection (1A) (no s.8 notice received) or (1B) (s.8 notice withdrawn) must give notice to an officer of the Board that they are chargeable, within "the notification period".

| Situation | Notification period | Reference |
|---|---|---|
| No s.8 notice received (s.7(1A)) | 6 months from the end of the year of assessment | TMA 1970 s.7(1C)(a) |
| s.8 notice withdrawn (s.7(1B)) | Later of: 6 months from end of the year of assessment; or 30 days beginning with the day after the notice was withdrawn | TMA 1970 s.7(1C)(b) |

HMRC's manuals render the first limb as a calendar date: notification "must be received on or before 5 October" following the tax year (SALF209/SALF210, citing s.7(1)); the Compliance Handbook says the same (CH71220; CH72700; and "no later than 5 October after the end of the relevant tax year" in the CH failure-to-notify overview).

Trustees are brought in by TMA 1970 s.7(2), with references to a s.8 notice read as references to a s.8A notice. "Relevant trustees" are defined in s.7(9) as the persons who are trustees when the income arises or the gains accrue, plus any who subsequently become trustees. Any relevant trustee may notify chargeability, make the return or deal with an enquiry on behalf of all of them (SALF805, citing s.107A(1)).

Where a person has been notified of a **simple assessment** for the year, s.7(2A) restricts the duty: notice under s.7(1) is only required if they are chargeable to an amount of tax not included in that simple assessment.

### The s.7(3) exemption

Subsection (3) removes the notification duty. The note on s.7 records that all three conditions must be met and that failing any one restores the obligation:

- total income is entirely from sources already taxed at source or under PAYE;
- there are no chargeable gains; and
- no additional tax is owed under s.30 ITA 2007 (other than the winter fuel payment charge).

SALF209 states the exception in slightly different terms — the taxpayer must have no chargeable gains (or gains within the annual exempt amount) and either no net income tax liability or sufficient tax deducted at source. CH71220 puts it more loosely still: the obligation "does not apply where all income is subject to PAYE or sufficient tax has been deducted at source to meet the net liability for the year." **Where these differ, the statute (s.7(3)) governs; the manual summaries are HMRC's paraphrase.** Note in particular that SALF209 admits gains within the annual exempt amount, whereas the s.7 note records the condition as "no chargeable gains".

### Coronavirus support payments

SALF210 records a modified notification period for a person who received a coronavirus support payment they were not entitled to: the period starts on the day income tax became chargeable and ends on the later of 20 October 2020 or the 90th day after the income tax became chargeable.

---

## 4. Who HMRC actually issues notices to, and why

The s.8 power is a discretion. HMRC's operational criteria for putting someone into SA (or keeping them there) are in SAM100050 and are **not law**. They shift over time.

| Criterion | Threshold / condition | Period | Reference |
|---|---|---|---|
| Total taxable income | £100,000 | 2017-18 to 2022-23 | SAM100050 |
| Total taxable income | £150,000 | 2023-24 | SAM100050 |
| Total taxable income | *Criterion does not apply* | 2024-25 onwards | SAM100050 (caveat) |
| Untaxed interest | £2,500 | 2015-16 and earlier | SAM100050 note 3 |
| Savings and investment income | £10,000 or less before tax → no return required | 2016-17 onwards | SAM100050 note 4 |
| Dividend income | £10,000 or less before tax → no return required | 2016-17 onwards | SAM100050 note 4 |
| Gross property income | £10,000 → SA record required | — | SAM100050 note 6 |
| Expenses / professional subscriptions | £2,500 coding threshold | — | SAM100050 |
| Other earnings (part-time, other income, commission, property income, tips) | £2,500 coding threshold | — | SAM100050 |
| High Income Child Benefit Charge | SA criteria from 2012-13; from 2024-25 only if the customer chooses not to pay via PAYE | — | SAM100050 (caveat) |

Edge cases recorded in SAM100050:

- Self-employment income shown on a self-employment page but included in the PAYE code **always** requires an SA return, regardless of the £2,500 threshold.
- Property loss cases with gross income below £10,000, and Rent a Room income below the exempt amount, do not require an SA record — unless the taxpayer cannot provide details of a new source.
- A UK resident seafarer wanting Seafarers Earnings Deduction must register for SA and claim on the return; a non-UK resident seafarer claims via form R43M and does not register (SAM100050 note 8).

Trustees and personal representatives are brought in by their own provisions: trustees file under s.8A and pay under the same SA timetable as individuals (SALF805); personal representatives file under s.8 for the estate, deduct tax before distributing income, and use form R185 (Estate Income) to notify beneficiaries, who then account for that income and its tax credit on their own returns (SALF806).

SALF (in "Who will get tax returns?") records that of roughly 28 million taxpayers covered by PAYE, around 4 million are sent SA returns, because of higher rate liability or complex affairs.

### System routing

HMRC's operational plumbing generates SA cases as well. NPS end-of-year reconciliation creates **work item 117**, and NPS tax coding calculation creates **work item 217**, where conditions are met and the SA indicator is not set (SAM100020). Where a caseworker identifies a PAYE individual with self-employed income meeting SA criteria, the manual instructs them to prepare form CWF1/SA400/SA401/SA402 and set the case up on SA (SAM100020). If the individual failed to inform HMRC of self-employment within 6 months after the end of the tax year in which self-employment commenced, SAM100020 directs referral to the Hidden Economy Risk Team as a failure-to-notify case.

---

## 5. Late issue and reissue of a notice

Where a notice or return is issued late, the filing date moves. Statute sets the outer structure; HMRC's manual sets the operational default.

| Case | Filing date | Reference |
|---|---|---|
| Individual/trustee, standard | 31 October (paper) / 31 January (electronic) following the year | TMA 1970 s.8A(1B); CH62100 |
| Notice given after 31 July but on or before 31 October in Year 2 | Non-electronic: within 3 months of notice; electronic: on or before 31 January | TMA 1970 s.8A(1D) |
| Notice given after 31 October in Year 2 | Within 3 months beginning with the date of the notice | TMA 1970 s.8A(1E) |
| Return/SA316 reissued because the original was never received | 3 months and 7 days after the date of issue | SAM, "Late issue/reissue of returns" |

The three-months-and-seven-days rule is HMRC operational practice for reissues, not the standard statutory annual deadline (SAM, caveat to "Late issue/reissue of returns"). Where a return is issued after 31 October following the return year, the *payment* due date used for interest depends on whether the case is flagged Failure to Notify: 31 January if it is, otherwise 3 months and 7 days after issue (SAM, "Using function RECORD RETURN REQUEST or RECORD DATE OF CLERICAL ISSUE"). The manual instructs that partnership cases are always recorded as "Not Failure to Notify".

---

## 6. Withdrawing a notice to file

A notice can be undone, but only within limits and only for recent years.

### The statutory power

HMRC may withdraw a notice under s.8 or s.8A, and must give the person a notice specifying the date of withdrawal (TMA 1970 s.8B(4)–(6)). The **withdrawal period** is 2 years beginning with the end of the year of assessment to which the notice relates, or, in exceptional circumstances, such extended period as HMRC may determine (s.8B(6)). Withdrawal is not available where a return has already been made or a s.28C determination served (note on s.8A/8B).

For partnerships, a partner required by a s.12AA notice may request withdrawal before the end of the withdrawal period, provided no return has yet been delivered (TMA 1970 s.12AAA(2)–(3), (6)). The period is 2 years from the end of the relevant period (partnerships including companies) or 2 years from the end of the year of assessment (other partnerships), or an extended period agreed by HMRC in exceptional circumstances (s.12AAA(6); EM7526).

| Partnership type | Withdrawal request time limit | Reference |
|---|---|---|
| Includes one or more companies | 2 years from end of the period specified on the notice | TMA 1970 s.12AAA; SAM120100 |
| No company partners | 2 years from end of the year of assessment | TMA 1970 s.12AAA; SAM120100 |

**There is no right of appeal against HMRC's decision *not* to withdraw a notice** (EM7525, caveat).

### HMRC's operational history

SAM120100 records that the availability of withdrawal has varied by year:

| Tax years | Position |
|---|---|
| 2009-10 and earlier | No withdrawal possible |
| 2010-11 and 2011-12 | Informal agreement only; letter SA789 |
| 2012-13 onwards | Formal statutory withdrawal; letter SA832; penalties cancelled under Schedule 55 FA 2009 |

Withdrawal will not proceed, per SAM120100, where a determination is in place, a return has already been received, the record is RLS ("gone away") until a new address is obtained, or the ACI signal is set / Compliance has noted an interest. From April 2015 an automated "Request Removal from SA" (RRSA) function handles withdrawal for individuals within the two-year window; SAM101094 records that RRSA rejects cases where the UTR is not for an individual, or Deceased, Bankruptcy or RLS signals are set, or where a return has been logged/captured, a charge or liability exists, or a determination is in place.

### Effect on penalties

Where HMRC agrees to withdraw a notice, any late filing penalties already charged are cancelled (CH61700; CH64280, citing FA09/Sch55 para 17A). CH62940 confirms the same for partnership returns, where the penalties fall on the relevant partners individually.

### What survives withdrawal

Withdrawal does not extinguish liability. Once a notice is withdrawn, the person falls into s.7(1B), so the s.7 notification duty revives with the extended period at s.7(1C)(b) — the later of 6 months from the end of the year, or 30 days beginning with the day after the notice was withdrawn (TMA 1970 s.7(1C)(b); SAM120100; CH143020, citing TMA70/s7(1B)).

Original payment due dates also survive. SAM120100 records that "original due dates for payment continue to apply under Section 59(B)(4) even where a new notice to file (SA833) is issued after chargeability is established post-withdrawal." The Compliance Handbook says the same for interest: where income is overlooked after withdrawal, late payment interest runs "from the date payment would have been due had the notice not been withdrawn" (CH Example 3).

**Machine-implementable — notification deadline after withdrawal:**
```
inputs: tax_year_end, withdrawal_date
deadline = max(tax_year_end + 6 months, withdrawal_date + 1 day + 30 days)
```

---

## 7. Reissuing a notice after withdrawal

If it later becomes apparent a return is needed, HMRC reactivates the year and issues a fresh notice.

| Reactivated year | New filing date | Reference |
|---|---|---|
| 2010-11 / 2011-12 (notice not legally withdrawn) | Standard filing dates if letter SA822 issued before them; otherwise 30 days from the letter | SAM120120 |
| 2012-13 onwards (letter SA833) | Later of 3 months and 7 days from SA833 issue, or the original filing dates | SAM120100; SAM120120 |
| SA833 reissue (as stated in the action guide) | 3 months from the date of the SA833 letter | SAM120122 step 4 |

Note the internal inconsistency: SAM120100/SAM120120 give "3 months and 7 days from SA833 issue, or the normal filing date, whichever is latest", while SAM120122 step 4 describes the customer deadline as "3 months from the date of the SA833 letter". Both are HMRC operational guidance rather than statute.

SAM120120 records that where there is no response to the SA833 notice, or a late response after the time limit for notifying chargeability following withdrawal, the case is treated as Failure to Notify. Where a late filing penalty was previously cancelled for a 2010-11/2011-12 reactivated year, the original penalty is not re-imposed, but later penalties are charged if the return is filed after the new date stated in the SA822 letter (SAM120120).

A caveat worth flagging for anyone modelling this: SAM120122 warns that whether a case is *recorded* as FTN in HMRC's systems does not necessarily match the substantive FTN determination — officers may record FTN status contrary to the facts purely to generate the correct system-calculated due date (Examples 1 and 2).

---

## 8. Being taken out of SA without a formal withdrawal

Separate from withdrawal, HMRC can make a record dormant and stop issuing returns.

- **Exit letter SA251** is sent when a case is identified as suitable for removal, with the "Final year for SA return signal" set to CY-1 (SAM101043). SAM101043 notes the automatic scan for ceased self-employed/partner cases has not been run in a number of years.
- The **"No SA Criteria" indicator** on NPS is set to 'Y' where the customer should not have been in SA for the year, triggering reconciliation outside SA; it is reset to 'N' on reactivation (SAM120122 step 8). It is only available for the current year back to CY-4, and cannot be set to 'Y' if a return has already been logged or captured or a determination exists (SAM120115 caveats).
- Even where a case is removed by automatic selection, SAM101043 states the return for CY-1 and any earlier outstanding returns is still required, despite not being mentioned on the exit letter.
- A customer or agent who wants to remain in SA despite not meeting criteria can be told that voluntary SA returns can still be filed (SAM101093, "All cases", step 3).

**Simple assessment** is an alternative to a return entirely: HMRC may assess an individual (TMA 1970 s.28H) or relevant trustees (s.28I) on information it holds. It does not apply where the person has already delivered a s.8 return or is currently subject to a s.8 notice requirement — though HMRC may issue a simple assessment simultaneously with withdrawing an s.8 notice (note on s.28C/28H). HMRC may withdraw a simple assessment by notice, and it is then treated as never having had effect (s.28J(1)).

---

## 9. What happens if the obligations are missed

### Failure to file (Schedule 55 FA 2009)

The penalty date is the day after the filing date (CH61160). For income tax and CGT (penalty model 1):

| Stage | Penalty | Reference |
|---|---|---|
| Penalty date | £100 fixed | CH62100 / FA09/Sch55 para 3 |
| 3 months after penalty date | £10/day, up to 90 days (written notice required, start date at least 3 months after penalty date) | CH62120 / para 4 |
| 6 months | Greater of 5% of the tax liability that would have been shown, and £300 | CH62140 / para 5 |
| 12 months — not deliberate | Greater of 5% and £300 (not reducible for disclosure) | CH62080 / CH63020 |
| 12 months — deliberate, not concealed | Greater of 70% and £300 | CH62160+ |
| 12 months — deliberate and concealed | Greater of 100% and £300 | CH62160+ |

CH61120 records that the Schedule 55 regime commenced for ITSA with the return for the year ended 5 April 2011 (due 31 October 2011 paper / 31 January 2012 electronic), subject to exceptions at SAM121025.

For **partnership** IT/CGT returns, the penalties fall on each relevant partner personally, not the partnership, and there is no tax-geared element: £100 initial, £10/day for up to 90 days, then £300 at 6 months and £300 at 12 months per partner (CH62940, citing FA09/Sch55 para 25). Only the representative partner has the right of appeal (CH62940; CH64540).

### Failure to notify (Schedule 41 FA 2008)

The penalty is a percentage of Potential Lost Revenue (PLR). For IT/CGT, PLR is the amount of tax unpaid at **31 January next following the tax year** (CH72700). SALF210 expresses the same ceiling as "the net amount of tax due, but unpaid, at 31 January following the tax year", and adds that the penalty is eliminated if the full tax is paid on or before 31 January even where notification was late.

Where a notice to file was withdrawn, the PLR cut-off shifts to the **later of** three dates (CH72700):

1. 30 days from the day after the notice to file was withdrawn;
2. 31 January following the tax year;
3. the day after any refund of a payment on account was issued.

Penalty ranges for onshore matters (and Category 1 offshore matters up to and including 2015-16) are (CH73200):

| Behaviour | Disclosure | Range |
|---|---|---|
| Non-deliberate, HMRC aware within 12 months | Unprompted | 0% – 30% |
| Non-deliberate, HMRC aware after 12 months | Unprompted | 10% – 30% |
| Non-deliberate, HMRC aware within 12 months | Prompted | 10% – 30% |
| Non-deliberate, HMRC aware after 12 months | Prompted | 20% – 30% |
| Deliberate | Unprompted | 20% – 70% |
| Deliberate | Prompted | 35% – 70% |
| Deliberate and concealed | Unprompted | 30% – 100% |
| Deliberate and concealed | Prompted | 50% – 100% |

Failure to notify is an **annual** obligation: it must be considered separately for each tax year to determine which penalty rules apply (CH71280). Failures occurring before 1 April 2010 fall under the previous rules (for IT, TMA 1970 s.7(8)); on or after that date, Schedule 41 applies (CH71260; CH401310).

**Reasonable excuse** prevents a failure-to-notify penalty, but the excuse must exist at the date the failure occurs — not merely at the date of notification — and the failure must be remedied without unreasonable delay after the excuse ends (CH71240; CH160000). There is no statutory definition of "reasonable excuse"; HMRC applies an objective test against a reasonable person with the taxpayer's attributes (CH160100/CH160200).

### Determinations

If a notice to file was given and the return is not delivered by the filing date, an officer may determine the tax due to the best of their information and belief (TMA 1970 s.28C(1A)), serving notice stating the date of issue (s.28C(2)). The determination is treated as a self-assessment until superseded. There is no right of appeal against a determination (SALF209).

| Limit | Rule | Reference |
|---|---|---|
| Time to make a determination | 3 years beginning with the filing date | TMA 1970 s.28C(5)(a) |
| Time for a self-assessment to supersede it | Within that 3-year period, or if later, 12 months from the date of the determination | TMA 1970 s.28C(5)(b), s.28C(6) |

"Filing date" for this purpose is 31 January of Year 2, or, if the s.8/8A notice was given after 31 October of Year 2, the last day of the three-month period beginning with the day the notice was given (s.28C(6)).

### Criminal offences (offshore)

Where the tax involved exceeds a threshold amount (minimum £25,000, settable by Treasury regulations — TMA 1970 s.106F(2)), failing to give s.7 notice of chargeability in respect of offshore income, assets or activities without reasonable excuse is a criminal offence (s.106B); so is failing to deliver a s.8 return (s.106C) and delivering an inaccurate return uncorrected by the end of the amendment period without reasonable care (s.106D). Persons acting as relevant trustees or as executor/administrator are excluded (s.106E). Penalties on conviction are at s.106G.

---

## 10. Record-keeping consequences of being in scope

Once a notice to file is given, a return containing a notice is given, or a voluntary return is made and delivered, the s.12B record-keeping duty bites (SALF211, citing TMA 1970 s.12B(1)):

| Case | Retention until | Reference |
|---|---|---|
| Taxpayer with a business | 5th anniversary of the 31 January next following the year of assessment | TMA 1970 s.12B(1)(b), (2) |
| Other cases | 1st anniversary of the 31 January next following the year of assessment | TMA 1970 s.12B(1)(b), (2) |

The retention requirement is reduced (to records still in the taxpayer's possession) where a notice to file or voluntary return is made or delivered after the normal retention-triggering date (SALF211). Certain original documents — certificates of tax deducted, tax credit vouchers — must be kept in original form despite the general rule permitting copies (s.12B(4A)).

---

## 11. Decision summary for implementers

```
# Step 1 — filing obligation
if notice_under_s8 / s8A / s12AA given AND not withdrawn:
    return_required = True
    filing_date = per TMA 1970 s.8A(1B)/(1D)/(1E) or s.12AA(4A)-(5C)
elif voluntary_return_delivered (on/after retrospective effect of 12 Feb 2019 rules):
    treated as notice given on date_received   # SAM121140
else:
    return_required = False

# Step 2 — notification obligation (only if no live notice)
if chargeable_to_IT_or_CGT and not s7(3)_exempt:
    if never_given_s8_notice:                  # s.7(1A)
        notify_by = tax_year_end + 6 months    # s.7(1C)(a); "5 October" per SALF209
    elif s8_notice_withdrawn:                  # s.7(1B)
        notify_by = max(tax_year_end + 6 months,
                        withdrawal_date + 1 day + 30 days)   # s.7(1C)(b)

# Step 3 — s.7(3) exemption test (all three must hold)
s7(3)_exempt = all_income_taxed_at_source_or_PAYE
               and no_chargeable_gains
               and no_additional_tax_under_ITA2007_s30 (other than winter fuel payment charge)

# Step 4 — withdrawal eligibility
withdrawable = (now <= tax_year_end + 2 years OR HMRC_agreed_extension)
               and not return_already_made
               and not s28C_determination_served
```

---

## Gaps in the sources

The supplied notes do not cover, and this page therefore does not state:

- **The registration mechanics themselves.** Forms SA1, CWF1, SA400/SA401/SA402 and CIS305 are named in SAM100020 as the routes into SA, but the notes give no detail on their content, deadlines, or online equivalents (e.g. no "register by 5 October" customer-facing framing is sourced beyond the s.7 statutory period).
- **Current-year SA criteria for 2024-25 onwards.** SAM100050 records that the total taxable income criterion ceased to apply from 2024-25, but the notes do not say what replaced it, if anything.
- **The self-employment / trading income thresholds** for entering SA (e.g. any trading allowance or gross-receipts test). SAM100050 covers savings, dividends, property and coding thresholds only.
- **Non-residence, domicile and remittance-basis triggers** for SA. The notes reference SA109 and residence pages in helpsheet material (HS305, HS320/HS321) but contain no criteria for when non-residence itself pulls someone into SA.
- **Capital gains reporting triggers**, including the CGT-on-UK-property 60-day regime. TMA 1970 s.8C (simplified CGT reporting where gains are within the annual exempt amount and disposal consideration does not exceed £50,000) is covered, but the standalone CGT return regime is not.
- **Class 2/Class 4 NIC entry criteria**, beyond the incidental references at SAM101092 step 14 and CH65040.
- **Making Tax Digital for Income Tax** scope and thresholds. HS234 and HS286 note that where MTD applies, claims are made through compatible software instead of SA boxes, but no MTD entry criteria are supplied.
- **Time limits for the s.7(3) exemption interaction with simple assessment** beyond the bare text of s.7(2A).
- **Partnership return filing deadlines under s.12AA in full detail for mixed partnerships** are given at EM7526 and s.12AA(4A)–(5C), but the notes do not resolve how the "later of" rule at EM7526 interacts with the statutory minimum-day rules.

Several SAM and CH pages cited above are noted in the source material as partially withheld under Freedom of Information Act 2000 exemptions, so HMRC's published operational guidance on withdrawal and reactivation is itself incomplete.

---

## Sources used on this page

This page was written by an LLM from structured notes extracted from the mirrored sources below. Always check the upstream source before relying on any figure or deadline.

- [sa-helpsheets:5f67dfee-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/accrued-income-scheme-hs343-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/accrued-income-scheme-self-assessment-helpsheet-hs343.md`
- [sa-helpsheets:5f67ceae-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/averaging-for-creators-of-literary-or-artistic-works-hs234-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/averaging-for-creators-of-literary-or-artistic-works-self-assessment-helpsheet-hs234.md`
- [sa-helpsheets:5f67d5b1-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/land-and-leases-the-valuation-of-land-and-capital-gains-tax-hs292-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/capital-gains-tax-land-and-leases-self-assessment-helpsheet-hs292.md`
- [sa-helpsheets:5f67dc31-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/employee-shares-and-securities-further-guidance-hs305-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/employment-related-shares-and-securities-self-assessment-helpsheet-hs305.md`
- [sa-helpsheets:5f67db85-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/gains-on-foreign-life-insurance-policies-hs321-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/gains-on-foreign-life-insurance-policies-self-assessment-helpsheet-hs321.md`
- [sa-helpsheets:5f67dcd2-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/gains-on-uk-life-insurance-policies-hs320-self-assessment-helpsheet) - 4 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/gains-on-uk-life-insurance-policies-self-assessment-helpsheet-hs320.md`
- [sa-helpsheets:5f67d46f-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/negligible-value-claims-and-income-tax-losses-on-disposals-of-shares-you-have-subscribed-for-in-qualifying-trading-companies-hs286-self-assessment-he) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/negligible-value-claims-and-income-tax-losses-on-disposal-of-shares-self-assessment-helpsheet-hs286.md`
- [hmrc-manual-artg](https://www.gov.uk/hmrc-internal-manuals/appeals-reviews-and-tribunals-guidance) - 8 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/artg.md`
- [hmrc-manual-ch](https://www.gov.uk/hmrc-internal-manuals/compliance-handbook) - 35 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/ch.md`
- [hmrc-manual-em](https://www.gov.uk/hmrc-internal-manuals/enquiry-manual) - 2 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/em.md`
- [hmrc-manual-salf](https://www.gov.uk/hmrc-internal-manuals/self-assessment-legal-framework) - 2 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/salf.md`
- [hmrc-manual-sam](https://www.gov.uk/hmrc-internal-manuals/self-assessment-manual) - 14 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/sam.md`
- [itepa-2003](https://www.legislation.gov.uk/ukpga/2003/1/contents) - 1 note(s) - mirrored at `corpus/legal-system/primary-legislation/acts/itepa-2003.md`
- [tma-1970](https://www.legislation.gov.uk/ukpga/1970/9/contents) - 8 note(s) - mirrored at `corpus/legal-system/primary-legislation/acts/tma-1970.md`
