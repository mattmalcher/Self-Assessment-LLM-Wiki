---
title: Reliefs, claims and elections
generated: true
generated_on: '2026-09-09'
generated_by: claude-cli:opus
input_hash: 8c38647fcbd0078f
note_count: 100
sources:
- hmrc-manual-ch
- hmrc-manual-em
- hmrc-manual-salf
- hmrc-manual-sam
- hmrc-manuals-index
- itepa-2003
- sa-helpsheets
- sa-helpsheets:5f67cd23-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67ceae-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67cefb-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67cf48-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67d41e-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67d46f-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67d5b1-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67db85-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dbe3-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dc31-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dcd2-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dd70-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67ddc2-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67de13-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67defe-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67e282-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67e2d6-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67e327-7631-11e4-a3cb-005056011aef
- sa-helpsheets:f689f4a2-7da1-41a3-b37d-b18c346219ed
- tma-1970
---

# Reliefs, claims and elections

!!! danger "Unofficial - not HMRC, not advice, written by an LLM"

    This page is **not** an HMRC publication and has no connection to HMRC or
    any government body. It was **written by a language model** from mirrored
    source material, and can be wrong, incomplete or out of date. It is not
    tax advice. Check every figure, date and rule against the cited source
    before relying on it, and see
    [GOV.UK](https://www.gov.uk/self-assessment-tax-returns) for official
    guidance.

This page covers the reliefs and claims a Self Assessment (SA) return commonly carries — EIS, SEIS, CITR, charitable giving, qualifying loan interest, averaging, qualifying care relief, negligible value and share loss claims, pension savings charges and the cap on income tax reliefs — together with the general statutory machinery for claims made inside and outside a return. For each item it states the conditions, the limits, the claim mechanism and the time limit, distinguishing statute (TMA 1970, ITA 2007) from HMRC's own interpretation (manuals) and from customer-facing helpsheets. It is an unofficial reference; the helpsheets cited are HMRC's simplified guidance, not law.

---

## 1. The general machinery for claims

### 1.1 Claims in a return (TMA 1970 s.42)

Section 42 TMA 1970 sets the general procedure for claims to relief, allowances or repayments under the Taxes Acts (TMA 1970 s.42). The core rules:

| Rule | Statute | Effect |
|---|---|---|
| Claim must be made **in the return** where a notice under s.8, s.8A or s.12AA has been given and the claim could be included in that return | TMA 1970 s.42(2) | Separate claims are not permitted where inclusion is possible |
| Claim must be **quantified** at the time it is made | TMA 1970 s.42(1A) | Provisional or contingent claims are not permitted; a "best estimate" is acceptable pending a final figure, and fixed-amount reliefs (e.g. personal allowance) count as quantified (SALF602) |
| **Supplementary claim** to correct an error or mistake | TMA 1970 s.42(9) | Permitted only within the time allowed for the original claim |
| Partnership-level claims and elections | TMA 1970 s.42(6)–(7) | Made in the partnership return where s.42(2) applies, otherwise by a nominated partner |
| Claims by/for incapacitated persons | TMA 1970 s.42(8), s.118(1) | May be made by trustees, guardians, tutors and curators |
| Elections | TMA 1970 s.42(10) | s.42 applies to elections as it applies to claims |

Carve-outs from the "must be in the return" rule in s.42(2) include PAYE-related claims, certain charitable trust exemptions, Gift Aid repayments, GAAR counteraction relief claims and marriage allowance transfer elections (TMA 1970 s.42(3), (3ZA)–(3ZC), (10A)). Where a claim is given effect in-year through a PAYE coding adjustment, SALF603 says it must still be repeated on the SA return so the self assessment takes account of it.

**General time limit:** a claim must be made not later than **four years after the end of the year of assessment** to which it relates (TMA 1970 s.43(1); SALF613). For companies, four years from the end of the accounting period (FA 1998 Sch.18 para.55).

Machine-implementable: `if notice_to_file_given(s8|s8A|s12AA) and claim_can_be_included_in_return: claim_route = IN_RETURN else claim_route = SCHEDULE_1A`.

### 1.2 Claims outside a return (Schedule 1A TMA 1970)

Schedule 1A applies to claims and elections made otherwise than in a return (TMA 1970 s.42(11)). It runs a parallel "process now, check later" regime (SALF604).

| Step | Rule | Ref |
|---|---|---|
| Form of claim | To an officer of the Board, in prescribed form if one exists; documentary proof of tax paid required if repayment claimed | Sch.1A paras 2(1)–(3) |
| HMRC correction of obvious mistakes | Within 9 months beginning with the day the claim is made | Sch.1A para 3(1)(a) |
| Claimant amendment | Within 12 months beginning with the day the claim is made | Sch.1A para 3(1)(b), (2) |
| Giving effect | As soon as practicable (discharge/repay, coding adjustment, or partner discharge) | Sch.1A para 4 |
| Records | Keep until the later of the date a formal enquiry is treated as complete or the date it becomes impossible to open one | Sch.1A paras 2A(1)–(3) |
| Notice of enquiry | Later of: quarter date following the first anniversary of the date the claim/amendment was made; first anniversary of 31 January next following the year of assessment; first anniversary of the end of the relevant period | Sch.1A para 5 |
| Closure notice | States conclusions; for repayment claims either confirms no amendment or amends to the correct figure; other claims allowed or disallowed | Sch.1A para 7(1)–(4) |
| Giving effect after enquiry | Within 30 days after the closure notice was issued | Sch.1A para 8 |
| Appeal | Normally 30 days after the closure notice; 3 months for non-resident personal reliefs, residence/domicile questions and ICTA 1988 s.615(3) pension funds | Sch.1A para 9 |

**Penalty:** failure to keep or preserve adequate records supporting a claim outside a return attracts a penalty of **up to £3,000** for each failure (Sch.1A para 2A(4); see also CH11500).

Neither claimant nor officer can amend a claim while it is under enquiry, and effect is deferred until the enquiry is complete, though the officer may give provisional effect in whole or part (SALF604). A claim already enquired into under Sch.1A para 5 cannot then be enquired into again under that paragraph, or under s.9A(1)/s.12AC(1) if later included in a return.

### 1.3 Claims involving two or more years (Schedule 1B TMA 1970)

Where relief for one year is quantified by reference to an earlier year, Schedule 1B gives effect to the claim in **"the later year"** — the year in which the event giving rise to relief occurs — even though it is quantified by reference to "the earlier year" (Sch.1B para 2(3), (6); SALF611). The claim does **not** revise or reopen the self assessment for the earlier year, and does not reopen or extend enquiry time limits for that year.

The relief is measured as the "tax difference": the tax that would not have been due in the earlier year if the claim could have been and had been given effect in that earlier year (Sch.1B para 2(4)).

SAM calls these "Schedule 1B claims" and lists them as: carry-back of pension relief, carry-back of losses, farmer's averaging and literary and artistic spreading (SAM110010). Processing produces an **automatic freestanding credit (FSC)** on the SA record with automatically allocated effective dates of payment (SAM110010). For trust returns, trading loss relief and loss carry-back claims are handled as stand-alone claims via CREATE FREESTANDING CREDIT after the return charge is recorded, not entered directly (SAM123161).

**Repayment interest** on a Schedule 1B claim runs from the **31 January next following "the later year"** (ICTA 1988 s.824(2C) & (3)(ab); and, under the FA 2009 regime, FA09/Sch.54 para.7, per CH146280). It does not run from the earlier year's due dates.

### 1.4 Time limits for two-year claims — a source conflict

The notes carry two different formulations, from different vintages of HMRC guidance:

| Claim | SAM114050 (citing ICTA 1988) | SAM114080 (citing ICTA 1988) |
|---|---|---|
| Trading loss relief / carry-back (S380/381) | 1 year 10 months from end of the loss year | One year after the fixed filing date of the later year's return |
| Loss on unquoted shares (S574) | 1 year 10 months from end of the year of assessment | One year after the fixed filing date of the later year's return |
| Farmers' averaging (S96(8)) | 1 year 10 months from end of the later year | One year after the fixed filing date; if profits later adjusted, a further claim up to 12 months after 31 January next following the tax year in which the adjusted profits are made |
| Post-cessation receipts (S108) | 1 year 10 months from end of the year received | One year after the fixed filing date of the later year's return |
| Artistic/literary spreading (S534(5A) etc.) | 1 year 10 months from end of the later year | One year after the fixed filing date |
| Creators' averaging (Sch.4A) | — | One year after the fixed filing date; further claim if profits adjusted |
| Carry-back of retirement annuity relief (S619(4)) | — | Election no later than the fixed filing date of the later year's return |
| Other Schedule 1B claims | 4 years from the end of the later year | — |

SAM114050 itself warns that its ICTA 1988 references "may be historic/superseded by later legislation (e.g. ITA 2007/ITTOIA 2005)". Both formulations are HMRC internal guidance, not statute. Implementers should treat the s.43(1) four-year rule as the statutory default and check the specific relief's own provision.

### 1.5 Late claims and amendment of claims

There is no statutory right to a late overpayment relief claim; HMRC's stated position is that acceptance is discretionary and fact-dependent (SAM114050, citing SACM10040). Where a claim is made in time but is deficient, SACM10010 says the officer should explain what is needed and allow a reasonable extension — **usually 14 days**, longer if circumstances warrant (e.g. the person is overseas). Requesting missing details on an incomplete claim does not amount to opening an enquiry, so the normal enquiry time limit is preserved (SAM114050).

Where a claim is processed after the time limit for amending the return has expired, legislation does not permit the self assessment to be amended, but SAM114070 says interest, penalty or surcharge may be **mitigated to what would have been due had amendment been possible**. Relief is given by set-off where liability is outstanding or due within 45 days, otherwise by repayment (SAM114070). The minimum tax-geared late filing penalty (£300, or 5% of the tax due, for 2010-11 onwards) cannot be reduced below that minimum by these procedures (SAM114070/SAM61240). Once a year's self assessment can no longer be amended, payments on account for the following year are final and unaffected by a later out-of-time claim (SAM114070).

**Amendment of a claim (time limits):** to a claim made in a return, up to 12 months after the fixed filing date (TMA 1970 s.9(4)(b)); to a claim made outside a return, up to 12 months after HMRC receives it (Sch.1A para 3(1)(b)) (SAM114070).

**Consequential claims:** where HMRC assesses or amends to recover lost tax, a claim, election, revocation or variation for the same year may be made outside the normal time limit (CH55100). Where the loss of tax was careless or deliberate, only consequential **claims** (not elections) are permitted, under TMA 1970 s.36(3); notified before the officer makes the amendment, or at any time before the end of the year of assessment following that in which the amendment was made (s.43(2)). Where there was no careless or deliberate conduct, claims **and** elections may be made within one year from the end of the year of assessment in which the assessment is made (s.43A(2), s.43C(2)) (SALF407A). Elections excluded from s.43A by s.43A(2A): transfer of married couple's allowance, transfer of children's tax credit, and the election to re-base assets to 1982. Section 43C applies only where notice of the amendment was issued after 10 July 2003. Where another person's liability would be altered, that person's written consent is required (s.43B(1)).

### 1.6 Withdrawal of reliefs — assessment time limits

| Relief withdrawn | Behaviour | Time limit | Ref |
|---|---|---|---|
| EIS | none/careless | Later of 6 years from end of the year in which the use-of-money requirement falls, or the event causing withdrawal occurs | ITA 2007 s.237 |
| EIS | deliberate | 20 years, same starting points | ITA 2007 s.237 |
| CITR (income tax) | none/careless | 6 years from the end of the year of assessment for which the relief was obtained | ITA 2007 s.372 |
| CITR (income tax) | deliberate | 20 years, same starting point | ITA 2007 s.372 |

CH52100 separately gives the EIS withdrawal limit as "6 years from the end of the relevant tax year".

---

## 2. The cap on income tax reliefs

Statutorily in force from 6 April 2013; HS204 (the 2026 edition) explains it for 2025-26 and later years.

**The limit:** aggregate relief claimed against total income is restricted to the **greater of £50,000 or 25% of adjusted total income** (HS204 s.1.1).

**Reliefs within the cap ("limited reliefs")** (HS204 s.2.1):

- trade loss relief against general income, and early trade losses relief
- property loss relief (capital allowances / agricultural expenses)
- post-cessation trade and property relief
- employment loss relief
- former employees' deduction for liabilities
- losses on deeply discounted securities and strips of government securities
- share loss relief — **except** EIS/SEIS share loss relief
- qualifying loan interest

**Outside the cap** (HS204 caveats; HS286):

- trading losses used against capital gains
- losses used against profits of the same trade or property business
- share loss relief on shares to which EIS or SEIS relief is attributable

**Adjusted total income** need only be calculated where total income exceeds **£200,000**; HS204 Working Sheet 1 does the calculation, and Working Sheet 2 tracks loss allocation (HS204 s.3.1).

**Edge case:** loan interest relief that cannot be given in full because of the limit **cannot be carried forward as a trade loss**, unlike certain other excess loan interest for partnership trades (HS204 caveat).

Machine-implementable:
```
limit = max(50_000, 0.25 * adjusted_total_income if total_income > 200_000 else 0.25 * total_income)
allowable = min(sum(limited_reliefs), limit)
```
HS204 also gives worked examples of the ordering of relief claims, and lists affected boxes across SA103S, SA103F, SA103L, SA104S, SA104F, SA105, SA106, SA101 and SA108. HS342 records that **Payroll Giving relief** is subject to the same cap: the greater of £50,000 or 25% of adjusted total income (HS342 s.4).

Under Making Tax Digital for Income Tax, HS204 notes that claims and adjustments will be made via compatible software rather than the SA boxes listed, so box references may not apply to all taxpayers going forward.

---

## 3. Venture capital reliefs

### 3.1 EIS — income tax relief (HS341)

| Item | Value (2025-26) | Ref |
|---|---|---|
| Relief rate | 30% | HS341 s.6 |
| Maximum subscription eligible for relief | £2 million | HS341 s.2 / s.6 |
| Maximum where not a knowledge-intensive company (KIC) | £1 million | HS341 s.2 / s.6 |

**Certificate condition:** relief is only available once form **EIS3** (or **EIS5**, for investment through an approved knowledge-intensive fund) has actually been received. An investor cannot claim where the certificate has not yet been issued (HS341 introduction, s.2). If the form arrives after the return has been sent, the claim form inside EIS3/EIS5 is completed and sent to HMRC (HS341 s.2).

**Claim mechanism:** total subscriptions claimed go in **box 2 of "Other tax reliefs" on page Ai 2 of SA101**; details of each investment (UIR, company name, amount claimed, share issue date, and the attribution choice if over the limits) go in **box 19 "Any other information" on page TR 7** (HS341 s.2). SAM121400 says HMRC expects details of each investment in the Additional Information box or form EIS3, and that where an EIS claim is made without sufficient supporting information the officer should refuse the relief as a repair of an obvious error, capture the rest of the return, and issue a customer service message giving the right to reject the amendment.

**Carry-back:** an investor may choose to treat shares as issued in the previous tax year, completing the claim form in EIS3/EIS5 showing the amount claimed for that year (HS341 s.5).

**Disqualifying factors** (HS341 caveat, s.3): connection with the company (employee, partner or "paid director"; control; more than 30% of ordinary share capital, voting power or winding-up entitlement, personally or via an associate); lack of commercial purpose; loans linked to the investment; options to require repurchase; the "replacement capital" rules; risk-protection arrangements; holding other non-qualifying shares issued on or after 18 November 2015. Relief may be restricted where value has been received from the company; the restricted amount is stated on form EIS3.

**Definitions** (HS341 s.3): an *associate* includes a spouse or civil partner, lineal ancestor or descendant, a business partner, and certain persons connected through a trust. A *paid director* is a director receiving or entitled to receive any payment from the company other than items such as reimbursement of allowable expenses.

**Records:** form EIS3/EIS5 need not be sent with the return, but should be kept as HMRC may ask to see it (HS341 s.2).

### 3.2 SEIS — income tax and CGT reliefs (HS393)

| Item | Value | Ref |
|---|---|---|
| Income tax relief rate | 50% | HS393 s.1.6; SAM121405 gives 50% of the cost of qualifying shares acquired on or after 6 April 2012 |
| Maximum subscription for income tax relief (2025-26) | £200,000 | HS393 s.1.2 / s.1.6 |
| Maximum subscription for carry-back to 2024-25 | £100,000 | HS393 s.1.6 |
| Reinvestment relief — proportion of gain exempt | 50% | HS393 s.2.1 / s.2.2 |
| Reinvestment relief — cap | 50% of the amount on which SEIS income tax relief is received, and £100,000 maximum | HS393 s.3.1, s.2.2 |
| Disposal relief — minimum holding period | 3 years | HS393 s.4 |
| Substantial interest threshold | more than 30% of share capital, voting power or winding-up entitlement | HS393 s.1.3 |
| Annual Exempt Amount used in HS393 examples (2025-26) | £6,000 | HS393 s.3.2 |

**Certificate condition:** relief cannot be claimed before form **SEIS3** is received, even if the shares were issued in the relevant tax year (HS393 caveat, s.3.4). Jointly issued shares require each owner to obtain their own SEIS3 (HS393 s.1.4).

**Income tax claim mechanism:** total subscription (max £200,000) in **box 10 of "Other tax reliefs" on page Ai 2 (SA101)**, with investment details (UIR, company name, amount, date of issue) in **box 19 on page TR 7** (HS393 s.1.2). SAM121405 confirms box 10 of Ai 2.

**Reinvestment relief claim mechanism:** complete the claim form attached to SEIS3 and attach it to the Capital Gains Tax summary pages; put code **"OTH" in box 28 on page CG 2**; give claim details in **box 54** or in the computation; enter the total of gains claimed exempt (not exceeding £100,000) in **box 40** (HS393 s.3.3). If claiming after the return has already been sent, complete the SEIS3 claim form and send it to HMRC.

**Time limits:** SAM121405 states the latest date for a SEIS relief claim is **five years after the normal SA filing date** of the relevant tax year (its example: for 2020-21, 31 January 2027). HS393 s.3.4 gives 31 January 2032 as the latest date for making a SEIS reinvestment relief claim in the context of that helpsheet (2025-26 tax year) — consistent with a five-year-after-filing-date rule.

**Restrictions:** reinvestment relief is only available if SEIS income tax relief is also obtained; it cannot be claimed independently (HS393 caveat). It cannot be claimed for 2024-25 in respect of shares treated as issued in 2023-24 (a carry-back restriction one year removed). Disposal relief is not due, wholly or partly, if shares are disposed of within 3 years of issue (except to a spouse/civil partner), which also triggers withdrawal of income tax relief and CGT chargeability on any gain. If there was no income tax liability before the SEIS subscription, no income tax relief is received and any gain on disposal is fully chargeable (HS393 s.3.1 caveats).

### 3.3 CITR (HS237)

| Item | Value | Ref |
|---|---|---|
| Annual relief | up to 5% of the invested amount, for each of 5 tax years | HS237 s.1 |
| Total maximum relief | up to 25% of the invested amount | HS237 s.1 |
| Relief against | Income Tax only — cannot reduce CGT | HS237 caveat |

**Conditions:** investment must be in an accredited **Community Development Finance Institution (CDFI)**. The CDFI issues a **Tax Relief Certificate** for each qualifying investment (HS237 s.1). The investor must be the beneficial owner, must be unprotected from investment risk, and the investment must not be part of a tax avoidance scheme (HS237 caveat). Relief may be reduced if part of a loan or deposit is repaid or withdrawn within 5 years, or if the investor receives value, financial advantage or benefit from the CDFI.

**Invested amount:** for shares/securities, the amount subscribed; for loans/deposits, generally the original advance or deposit, subject to reduction if part is repaid or withdrawn within 5 years (HS237 s.3).

**Timing:** a formal claim cannot be made until the Tax Relief Certificate has been received **and** the tax year to which the claim relates has ended (HS237 s.2).

**Claim mechanism:** the invested amount(s) go in **box 3 of "Other tax reliefs" on page Ai 2 of SA101**; details of each investment go in **box 19 "Any other information" on page TR7** (HS237 s.2). The certificate is kept, not sent, but may be requested during an enquiry.

**In-year benefit:** an investor may write to HMRC asking for a PAYE code change to include expected CITR, or to reduce SA payments on account (HS237 s.4). If the relief ultimately due is less than expected, HMRC will charge interest on the shortfall.

**SA registration:** SAM100060 lists a CITR claimant as requiring an SA record. It also requires an SA record where total EIS/SEIS relief claimed is **£10,000 or more**.

**Payments on account:** SAM1001 confirms that EIS or VCT relief can be given against payments on account via a claim to adjust, and that interest is charged on any reinstated amount from the relevant due dates if the claim proves excessive. HMRC officers are told not to question whether a claim to reduce payments on account was made on the correct basis, though the claim must give full consideration to expected final liability.

---

## 4. Charitable giving (HS342)

Four reliefs are reported on the return: Gift Aid, gifts of shares/securities, gifts of land/buildings, and Payroll Giving.

### 4.1 Gift Aid

Gift Aid is a relief for gifts of money to UK-based charities meeting the UK tax definition of a charity, treated as made after deduction of basic rate income tax (HS342 s.1). Grossing-up factor: **100/80** (basic rate 20%).

| Donor's rate | Relief on a £100 gift | Ref |
|---|---|---|
| Higher (40%) | £25 | HS342 s.1.1 |
| Additional (45%) | £31.25 | HS342 s.1.1 |
| Basic | No additional relief due, unless claiming certain allowances for people aged over 65 | HS342 caveat |

**Donor condition:** the donor must have paid enough Income Tax or Capital Gains Tax to cover the tax reclaimed by the charity/CASC, or must pay an additional amount of Income Tax (HS342 s.1). The SAM glossary states the same and adds that the donor must give the charity a Gift Aid declaration, which can be backdated **up to 6 years before the date of the declaration**, provided the donation was made after 6 April 2000 (SAM, "Gift aid — Gift aid rules").

**CASC:** a Community Amateur Sports Club registered with HMRC as such when the donation is made. Broadly the same Gift Aid rules apply, but a CASC cannot claim Gift Aid on membership subscriptions (HS342 s.1).

**Carry-back:** payments made between 6 April 2026 and the date of submitting the return for the year ended 5 April 2026 can be carried back — but the claim **must be made in the original return, before the appropriate filing date**. HS342 states that HMRC cannot accept a first claim, or a higher claim, for Gift Aid carry-back in an **amended** return for the year ended 5 April 2026.

**Boxes:** Gift Aid payments in boxes 5, 6, 7 and 8 on page TR 4 (HS342 s.1.1).

### 4.2 Gifts of shares, securities, land and buildings

*Qualifying investments* for the share/security relief: shares or securities listed on a recognised stock exchange, dealt on AIM or the PLUS-Quoted Market, units in an Authorised Unit Trust, shares in an OEIC, or interests in certain overseas collective investment schemes (HS342 s.2).

*Qualifying interest in land*: the whole of a person's beneficial interest in freehold or leasehold land in the UK (HS342 s.3).

*Disposal-related liabilities*: liabilities to which the charity becomes subject in connection with the transfer, deducted when calculating relief (HS342 ss.2–3).

Boxes: relief for gifts of shares/securities in **box 9 on page TR 4**; relief for gifts of land/buildings in **box 10 on page TR 4** (HS342 ss.2–3).

### 4.3 Payroll Giving

Reported on the Additional Information pages, and **not** entered elsewhere on the return (HS342 s.4). Subject to the cap described in section 2 above.

### 4.4 Non-UK charities

Charities based in the EU, Iceland, Liechtenstein or Norway can no longer apply for tax relief; relief obtained on or before 14 March 2023 continued only until April 2024, and **no reliefs will be given on gifts to non-UK charities after 5 April 2024** (HS342 caveats).

### 4.5 Devolved rates

Gift Aid is claimed by charities at the **UK** basic rate; higher/additional rate Scottish or Welsh customers reclaim at their respective devolved rates (SAM, "Exceptions" — terminology). Investment income is taxed at UK rates regardless of Scottish/Welsh customer status.

### 4.6 Repayments to charity

SAM notes that the facility to direct SA repayments to charity via return boxes was **withdrawn from April 2012** for all tax years; earlier years' boxes remain visible but non-functional, and requested charity repayments are sent to the customer instead (SAM 3.14 caveat).

---

## 5. Qualifying loan interest and alternative finance payments (HS340)

Relief is claimed in **box 5 of "Other tax reliefs" on page Ai 2 (SA101)** (HS340).

**Qualifying purposes** include: buying shares in, or lending to, a close company; investment in an employee-controlled company; investment in a co-operative; acquiring an interest in a partnership; and buying business equipment or machinery (HS340 s.1).

**Definitions:**
- *Full-time employee* (for employee-controlled company relief): someone who works for the greater part of their time as a director or employee of the company, or of a subsidiary in which the company has an interest of 51% or more (HS340 s.1).

**Exclusions and restrictions:**

| Restriction | Detail | Ref |
|---|---|---|
| Overdraft / credit card interest | No relief | HS340 caveat |
| Equipment/machinery | Relief only if capital allowances could be claimed on the item(s); only the business-use proportion qualifies if used partly for other purposes | HS340 caveat |
| Residential property in a partnership property business (2025-26) | Relief cannot be claimed for the cost of getting the loan or the interest on it; instead used to calculate a reduction in Income Tax at box 12 | HS340 caveat |
| Overall cap | Greater of £50,000 and 25% of adjusted total income | HS340 s.2 |
| Excess relief | Cannot be carried forward as a trade loss | HS204 caveat |

**Records:** the claimant must obtain and keep a certificate of interest or alternative finance payments from the lender (HS340 s.3).

Related but distinct: for beneficial (employer-provided) loans, ITEPA 2003 s.180 sets a **£10,000** threshold below which the benefit of a cheap loan is not treated as earnings; a *qualifying loan* for that purpose is one where the interest would be eligible for relief under ICTA s.353/ITA 2007 s.383, would be so eligible but for mortgage interest deduction-at-source rules, or is deductible in computing trade or UK property business profits (ITEPA 2003 s.180(5)). A notice electing for the alternative method of calculating official-rate interest must be given on or before the **first anniversary of the normal self assessment filing date** for the tax year (ITEPA 2003 s.183(2)).

---

## 6. Averaging for creators of literary or artistic works (HS234)

**Relief:** profits for two tax years (2024-25 and 2025-26 in the 2026 edition) are added together and the taxpayer is taxed on the average (HS234 s.1).

**Condition to claim:** the profits of one year are **less than 75% of the profits of the other**, or one tax year's profits are **nil** (HS234 s.4).

**Eligible income:** profits from disposing of works, or royalties for allowing reproduction of works — e.g. authors selling written work, software writers earning royalties on copyrighted code (HS234 s.2).

**Ineligible income:** profits from services provided rather than from the works themselves — e.g. architects or programmers paid for services, even if some of the work is copyright-protected (HS234 s.3).

**Exclusions** (HS234 caveats):
- profits calculated on the **cash basis**
- the business started or ended in either of the two years
- a partner joined or left the partnership in either of the two years

**Claim mechanism:** sole traders enter the increase/decrease at **box 72 of the Self-employment (full) pages** (HS234 s.8); partners at **box 11 of the Partnership pages** (HS234 s.9).

**Effect on earlier years:** averaging does not alter tax or NIC actually payable for earlier years — those must still be paid in full; the adjustment is made through the later year's tax and NIC calculation (HS234 s.1; note the helpsheet text is internally inconsistent about which year, with s.11 stating the adjustment is via the 2025-26 liability).

**If profits later change:** a previously made averaging claim is **ignored** and must be re-made by amending the return, or, if the amendment time limit has expired, by writing to HMRC without delay because of a time limit (HS234 s.12). SAM114080 gives the corresponding rule: where profits are later adjusted, a further claim is allowed up to 12 months after 31 January next following the tax year in which the adjusted profits are made.

**Time limits:** see the table at §1.4. EM gives the normal time limit for averaging claims (farmers and creative artists) as **22 months after the end of the later of the two years of assessment concerned**. Under ITTOIA 2005 s.225, where profits of either year in an averaging pair are adjusted, the claim is treated as never having been made, giving the taxpayer the opportunity to re-elect (EM, citing BIM84150).

**Late averaging claims during an enquiry:** HMRC's guidance is that late averaging claims made via an enquiry are limited to the amount by which profits are increased as a result of the enquiry; in failure-to-notify cases there is no such restriction, because the whole increase results from the enquiry (EM, "Averaging for farmers and creative artists").

**Repayment interest:** for averaging claims (and loss carry-backs), the repayment interest start date is 31 January following the "later year" in relation to the claim (FA09/Sch.54 para.7; CH146280).

**MTD:** SALF1500 lists a temporary exemption from MTD digital obligations for tax year 2026-27 for farmers and creative artists making averaging claims.

---

## 7. Qualifying care relief (HS236)

**Who:** foster carers, adult placement carers, kinship carers, staying put carers and Shared Lives carers, where the child or adult is placed by a local authority, health and social care trust, fostering service provider or Shared Lives service provider (HS236 introduction).

**Out of scope:** private arrangements with friends or relatives (HS236 caveat). Supported lodging schemes qualify **unless** the relationship is more akin to landlord and tenant than family members.

**Definitions:** *staying put care* is where a young person who was fostered continues to receive care after their 18th birthday; *parent and child arrangements* are where the parent is aged 18 or over and the child is not a "looked after child" (HS236 s.1).

**Qualifying amount** (HS236 s.2) — figures are those in the 2026 edition of HS236:

| Component | Amount |
|---|---|
| Fixed household amount, full year | £19,690 |
| Weekly amount — child under 11 | £415 |
| Weekly amount — child aged 11 or over | £495 |
| Weekly amount — each adult | £495 |

The qualifying amount is apportioned for partial years or where there is more than one carer (HS236 s.2).

**Two methods** (HS236 s.3):

| Method | Taxed on | Relief retained? | Reporting |
|---|---|---|---|
| Receipts below the qualifying amount | Nothing | Yes | Self-employment (short) pages (SA103S), claiming qualifying care relief (s.3.1) |
| Simplified method | Receipts **less** qualifying amount | Yes | SA103S, showing total receipts and the qualifying amount (s.3.4) |
| Profit method | Total receipts less expenses and capital allowances | **No** — relief forgone | Self-employment (full) pages (SA103F) (s.3.3) |

Carers using qualifying care relief (whether under the qualifying amount or via the simplified method) cannot claim expenses or capital allowances (HS236 caveat).

**Apportionment:** where the annual accounting date is not on or between 31 March and 5 April, receipts must be apportioned to calculate total receipts for the tax year (HS236 s.4).

**MTD:** HS236 states qualifying care receipt customers are exempt from Making Tax Digital for Income Tax **for tax year 2026-27**, with the caveat that this may not extend to other years. SALF1460 requires the relevant person to give notice to HMRC that the relevant activity falls within the specified descriptions (which include qualifying care receipts under ITTOIA 2005 Part 7 Chapter 2) in order to claim the exemption; SALF1450 excludes qualifying care receipts from "qualifying income" for MTD threshold purposes.

---

## 8. Negligible value claims and share loss relief (HS286)

Two distinct claims, often made together.

### 8.1 Negligible value claim

**What it does:** treats an asset as disposed of and immediately reacquired at the specified value, even though still owned (HS286). "Negligible value" means worth next to nothing.

**Conditions:**
- the claimant must **still own the asset** when making the claim, and
- the asset must have become of negligible value **while owned** (HS286).

**Earlier specified time:** the claim may specify an earlier deemed disposal date, up to **2 years before the start of the tax year in which the claim is made** (HS286). Delay in submitting the claim or return affects how far back the earlier specified time can be set. The date chosen could affect the ability to claim some other reliefs.

**Dissolved companies:** a negligible value claim **cannot** be made after the company has been dissolved; the shareholder is instead automatically treated as having disposed of the shares at the time of dissolution, and must make a calculation of the loss and send it to HMRC for it to be an allowable loss (HS286).

**Mechanism:** give details in **box 54 "Any other information" on page CG 4 of SA108**, or in computations included with the return. Notifying HMRC of the resulting capital loss is a **separate claim**: include the loss in boxes 7, 19, 27 or 35 of SA108, with code **"NVC"** (or **"MUL"** if multiple codes apply) in boxes 8, 20, 28 or 36, with an accompanying computation (HS286).

**Valuation check:** form **CG34** may be sent to HMRC to check a valuation, at least **3 months before the return filing date** (HS286).

### 8.2 Share loss relief — setting the loss against income

**What it does:** sets certain allowable capital losses on disposal of shares subscribed for in a qualifying trading company against income, rather than only against chargeable gains (HS286).

**Qualifying disposal:** a disposal by way of a negligible value claim, an arm's length bargain, a distribution in the course of winding up the company, or the dissolution of the company. **A gift of shares is not a qualifying disposal** (HS286).

**Qualifying shares** (HS286): must not be fixed-rate dividend preference shares; must have been subscribed for individually (including jointly or via a nominee); shares transferred from a spouse or civil partner during their lifetime who subscribed for them are treated as subscribed for by the recipient. Subscribed shares are those issued for money or money's worth. Where a holding includes both subscribed and non-subscribed (bought, gifted or inherited) shares, only the subscribed portion qualifies and apportionment rules apply.

**Qualifying trading company — shares issued on or after 6 April 1998** (HS286): must not exceed the gross assets limit in force at issue; must not be listed on a recognised stock exchange (or have arrangements to be) at issue, unless listed on or after 7 March 2001; must not be a building society or registered industrial and provident society; must be a trading company (wholly for qualifying trades, or a group whose non-qualifying activities are not substantial — broadly not more than about **20%**).

**Qualifying trading company — shares issued before 6 April 1998**: must not have had shares listed on a recognised stock exchange since incorporation (or one year before issue if later); must not be a building society or registered industrial and provident society; must be a trading company whose business consisted wholly or mainly of carrying on a trade, or have subsidiaries meeting that test.

**Gross assets rule:**

| Shares issued | Immediately before issue | Immediately after issue |
|---|---|---|
| Before 6 April 2006 | £15 million | £16 million |
| On or after 6 April 2006 | £7 million | £8 million |

**Non-qualifying trades** (HS286): post-6 April 1998 — trade consisting wholly or mainly of dealing in land, commodities, futures, shares/securities/financial instruments; not a qualifying trade for EIS purposes; or not pursued on a commercial basis with an expectation of profit. Pre-6 April 1998 — dealing in shares, securities, land or commodity futures, or not pursued on a commercial basis with an expectation of profit.

**Trading period:** the company must have been a trading company throughout the **6 years to the date of disposal**, or throughout its active existence if less than 6 years (HS286). Relief remains available where the company stopped trading **no more than 3 years** before disposal, has not started a non-qualifying activity, and satisfied the qualifying conditions at the date it stopped trading.

**Other exclusions:** no relief for losses on shares in the holding company of a non-trading group; relief on shares acquired via a reorganisation or share exchange is only available in limited circumstances unless ownership of the new company exactly mirrors that of the old (HS286).

**Interaction with EIS relief:** the allowable loss is reduced by EIS relief attributable to the shares. HS286 Example 5: £10,000 subscribed in 2003, EIS relief £2,000 (20%), negligible value claim August 2025 — loss relief claimable **£8,000**.

**How relief is given** (HS286):
- the loss is deducted from **total income before personal allowances**; relief cannot be restricted to preserve allowances
- if income tax relief is claimed for a capital loss, the same loss cannot also be set against capital gains
- ordering of priority within a tax year: share losses in-year first, then carried-back share losses, then other income tax losses
- where a claim covers more than one tax year, the claim must state which year takes priority

**Cap:** the £50,000 / 25%-of-income limit applies from 2013-14 onwards, but **does not** apply to losses on shares to which EIS or SEIS relief is attributable (HS286).

**Time limit:** **one year from 31 January following the tax year in which the loss occurred** (HS286).

| Loss year | Claim deadline | Route |
|---|---|---|
| 2025-26 | 31 January 2028 | In the 2025-26 return |
| 2024-25 | 31 January 2027 | Amend the 2024-25 return (relief against 2024-25 or 2023-24 income) |

**Boxes:**

| Loss year | Entries |
|---|---|
| 2025-26 | Relief in box 41 on page CG 2 of SA108; capital losses in box 35; details in box 54 or computations |
| 2024-25 | Relief in box 43 on page CG 2 of SA108; losses in box 35; details in box 54 or computations; calculate the tax difference and enter it in box 15 on page TC 2 of SA110 |

**Minimum information required in the claim** (HS286): company name; registration number; country of incorporation; country of tax residency if different; date the loss arose; and, where more than one year is claimed, a statement of which year takes priority.

---

## 9. Pension savings tax charges (HS345)

These are charges reported on **page Ai 4 of SA101**, not reliefs — but they are commonly handled alongside reliefs at the return-preparation stage.

### 9.1 Annual allowance (2025-26 figures)

| Item | 2025-26 value | Ref |
|---|---|---|
| Standard / default annual allowance | £60,000 | HS345 |
| Money purchase annual allowance (after flexi-access) | £10,000 | HS345 |
| Alternative annual allowance | £50,000 (i.e. £60,000 − £10,000) | HS345 |
| Threshold income limit | £260,000 | HS345 |
| Adjusted income limit | £260,000 | HS345 |
| Taper rate | £1 reduction per £2 of adjusted income above £260,000 | HS345 |
| Minimum tapered annual allowance | £10,000 (floor, even if the formula gives less) | HS345 |
| Carry-forward window | Previous 3 tax years | HS345 |
| Annual allowance charge rates | 45%, 40% or 20% (may differ for Scottish or Welsh Income Tax) | HS345 |

**Definitions:** *threshold income* is income excluding pension contributions, unless paid as salary sacrifice by an employer; *adjusted income* is income plus any pension contributions made by the individual or employer (HS345). *Flexi-accessed* means having flexibly accessed a money purchase arrangement at any time from 6 April 2015.

**Carry-forward:** unused allowance can be added to the tapered/default annual allowance or the alternative annual allowance, but **not** to the £10,000 money purchase allowance. Membership of a registered pension scheme is required in each carry-forward year. No SA disclosure or claim is needed for carry-forward if no annual allowance charge arises (HS345).

**Valuing defined benefits / cash balance input:** opening value = annual pension × **16**, plus any separate lump sum, increased by **3.1%**; closing value = annual pension × 16 plus lump sum, without the 3.1% step. Cash balance opening value = pot value immediately before the start of the year, increased by 3.1%. For hybrid arrangements, the pension input amount is the greatest of the amounts calculated under each relevant method. Contributions required to be paid to a DB or cash balance arrangement are not counted; only the increase in value is tested (HS345).

**Overseas schemes:** the adjusted pension input amount is the pension input amount × (TE + TSI) / EI, where EI is total employment income from a sponsoring employer, TE is so much of EI as is UK taxable earnings, and TSI is so much as constitutes taxable specific income (HS345).

**Boxes:** excess pension savings in **box 10**; amount the scheme is paying in **box 11**; the scheme's PSTR in **box 12** (HS345). Personal representatives completing a return for someone who died during 2025-26 may ignore boxes 10, 11 and part of box 12 for the period up to death. If, after filing, the scheme agrees to pay (or pay more of) the charge so box 11 is no longer correct, HMRC must be contacted to amend the return.

**Scheme obligation:** a pension scheme administrator must send a **pension savings statement** by **6 October 2026** where the pension input amount for that scheme alone exceeds £60,000 for 2025-26, or the money purchase input amount exceeds £10,000 for a flexibly-accessed money purchase arrangement (HS345).

### 9.2 Overseas transfer charge

| Item | Value | Ref |
|---|---|---|
| Rate | 25% of the "transferred value" | HS345 |
| Trigger date | Transfers requested on or after 9 March 2017 | HS345 |
| Relevant period for re-imposition on change of circumstances | 5 full tax years from the original transfer | HS345 |

Liability is **joint** — individual and scheme administrator (transfer from a registered pension scheme), or individual and scheme manager (transfer from a QROPS or former QROPS). The individual must give the scheme administrator all prescribed information **before** transferring to a QROPS. Boxes: transferred value in **box 11.1**; tax paid by the scheme in **box 11.2**; PSTR in box 12 (or the scheme manager's name and address in "Any other information" for overseas schemes) (HS345).

### 9.3 Unauthorised payments and short service refunds

| Charge | Rate | Ref |
|---|---|---|
| Unauthorised payments charge | 40% | HS345 |
| Unauthorised payments surcharge | further 15% | HS345 |
| Surcharge threshold | 25% of the value of rights under the scheme (or of UK tax-relieved / UK transferred funds for overseas schemes) | HS345 |
| Short service refund of contributions | 20% on the first £20,000; 50% above £20,000 | HS345 Box 16 |

*Surcharge period*: starts on the date the first unauthorised payment was made and ends 12 months later, or when the surcharge threshold is reached if earlier (HS345).

Boxes: unauthorised payment not subject to surcharge — **box 13**; subject to surcharge — **box 14**; foreign tax paid on it — **box 15** (sterling, spot rate at date of tax payment); overseas short service refund — **box 16**; foreign tax on that — **box 18** (HS345). Amounts must be entered **gross**, before any deduction the administrator made to cover its own tax liability.

The unauthorised payments charge/surcharge and the short service refund charge are **not charges on income** and so are not exempted by UK double taxation agreements, though foreign tax credit relief can still be claimed against them (HS345). Where foreign tax is paid *after* the return is submitted on a payment already charged, a claim must be made for an appropriate adjustment to UK tax liability.

Boxes 13–16 relating to overseas schemes can be ignored if the individual was not UK resident in 2025-26 or in any of the previous 5 tax years (HS345).

**SA registration:** SAM100060 lists recipients of unauthorised pension scheme payments liable to the charge or surcharge as requiring an SA record.

---

## 10. Other elections commonly appearing on the return

These are outside the brief's core list but appear in the same helpsheet family, and the notes cover their mechanics:

| Election / claim | Condition | Time limit | Ref |
|---|---|---|---|
| FHL **averaging election** (letting condition applied to average occupancy across a single UK or EEA FHL business) | Not mixed UK/EEA | Up to one year after 31 January following the end of the tax year (e.g. 2024-25: by 31 January 2027) | HS253 |
| FHL **period of grace election** | Letting condition met in the immediately preceding year (alone or via averaging); genuine intention to let; other two conditions met. After two consecutive elections without meeting the threshold, the property ceases to qualify | Same as above | HS253 |
| **Disapply deemed disposal on demolition** (SBA) | Written, irrevocable; identifies the building and demolition date; via box 54 or computations | On or before the first anniversary of 31 January following the year of assessment of the demolition (2025-26 demolition: by 31 January 2028) | HS292 s.8.2 |
| **Same day acquisition election** (shares) | No statutory form; must give acquisition date, company, number/class/cost of shares, and details of the first disposal; if included in a return, must be in that return; must be referenced on each later disposal of remaining shares | Before the time limit is up | HS287 s.15 |
| **FIG regime claim** (foreign income and/or gains, from 6 April 2025) | Qualifying new resident; claim per year and per source; tick box 28 / 29 / 30 on SA109 | Anniversary of 31 January following the end of the tax year (2025-26: 31 January 2028); amendment within the same limit unless notice to file issued after 31 October 2026 | HS266 s.4 |
| **TRF designation** (pre-6 April 2025 foreign income and gains) | Former remittance basis user; boxes 50, 51, 52 and 54 on SA109; charge 12% (2025-26 and 2026-27), 15% (2027-28); no foreign tax credit against the charge | Available for 3 tax years from 6 April 2025 | HS264 s.4 |
| **Business investment relief** (pre-6 April 2025 funds) | Box 38 of SA109 with a breakdown by company at box 54 | Claims cannot be made after 5 April 2028 | HS264 s.1.2 |

FHL occupancy conditions for reference (HS253): pattern of occupation — not met if the total of all lettings exceeding 31 continuous days is more than **155 days**; availability — at least **210 days** (140 days for 2011-12 and earlier); letting — at least **105 days** (70 days for 2011-12 and earlier). HS253 covers FHL rules only up to the end of the 2025 tax year.

---

## 11. Interaction with enquiries, penalties and record-keeping

**Enquiry into a claim outside a return:** Sch.1A para 5, time limits as at §1.2. A claim or amendment can be enquired into only **once** (TMA 1970 Sch.1A para 5(3); EM1530).

**Enquiry into a claim in a return:** normal s.9A machinery applies (SALF604).

**Withholding repayments:** EM1609 says an officer must open an enquiry into the return before withholding all or part of a repayment shown by the self assessment (TMA 1970 s.59B(4A)), must carry out a full risk assessment of the whole return first, and must write to the taxpayer stating the intention not to repay or to make a provisional repayment.

**Late claims and enquiries:** EM1610 states that an enquiry should not be opened *solely* to challenge a late claim or election that is ineffective under TMA 1970 s.43C, unless another aspect of the return is also being enquired into — because such an enquiry may be ineffective for that purpose.

**Records:** a person wishing to make a direct tax claim not included in a return must keep all records needed to make a correct and complete claim (TMA 1970 Sch.1A para 2A; CH11500), retained until the later of completion of an enquiry into the claim or the day after the enquiry window closes (CH14900). Penalty for failure: see §1.2.

**Overpayment relief:** claims must be made in writing, stating that it is an overpayment relief claim, the tax year, the grounds, whether a previous appeal was made, the amount overpaid, and must include a signed declaration by the customer (or, for a company, an officer — **not** the tax agent) (SAM114050). Statutory time limit: not later than four years after the end of the tax year concerned (TMA 1970 s.33, Sch.1AB). Relief is not available where the mistake concerned the basis of calculation reflecting generally prevailing practice at the time, nor for errors or mistakes in claims included in the return (a separate procedure applies) (SALF206).

**Inaccuracy penalties:** careless or deliberate inaccuracies in a return or other document, including claims, attract penalties under FA 2007 Sch.24, up to **100%** of the additional tax (SALF408; CH81001). The Sch.24 regime applies where the document was due to be filed on or after 1 April 2009 relating to a tax period beginning on or after 1 April 2008 (CH81012).

**Provisional figures in claims:** SALF602 confirms that s.42(1A) requires quantification but permits a "best estimate" pending a final figure. HS345/SALF206 note that unjustified or unreasonable use of a provisional figure, or unreasonable delay in submitting the correct figure, can attract a penalty even if the original estimate was not careless when submitted.

---

## Gaps in the sources

The supplied notes do not cover, and this page therefore does not state:

- **Farmers' averaging** conditions and mechanics in their own right. The notes reference HS224 by title only (SAM Help Sheets index) and cover farmers' averaging only incidentally through claims machinery (SAM114050/114080, CH146280, EM). The 75%/nil-profit test, the five-year averaging option, and the current statutory basis (ITTOIA 2005 Part 2 Chapter 16) are not in the notes.
- **The statutory provisions underlying EIS, SEIS and CITR themselves** (ITA 2007 Parts 5, 5A and 7). The notes give only the withdrawal-of-relief assessment time limits (ITA 2007 ss.237, 372) and the customer-facing helpsheets. Company-level qualifying conditions, the risk-to-capital condition, gross assets and employee-number limits for EIS/SEIS, and annual company investment limits are not covered.
- **EIS and SEIS carry-back time limits** as distinct statutory rules — the notes describe the mechanism (complete the claim form in EIS3/SEIS3) but give no separate carry-back deadline for EIS.
- **CITR claim time limit.** The notes give the earliest point for a claim (after the certificate is received and the year has ended) but no statutory deadline.
- **Gift Aid statutory basis** (ITA 2007 Part 8 Chapter 2) and the detailed conditions for gifts of qualifying investments and land — only HS342's summary is available.
- **Qualifying loan interest statutory basis** (ITA 2007 Part 8 Chapter 1) and the full list of qualifying purposes with their conditions — only HS340's summary list is available.
- **Qualifying care relief statutory basis** (ITTOIA 2005 Part 7 Chapter 2) beyond its use as an MTD exemption trigger.
- **Share loss relief statutory basis** (ITA 2007 Part 4 Chapter 6) — the notes cite VCM70000 and CG13120P by reference only.
- **The cap on income tax reliefs statutory basis** (ITA 2007 s.24A) — only HS204 is available.
- **Current-year figures for tax years other than 2025-26** for most reliefs; the helpsheets cited are the 2026 editions and their own caveats warn that figures are year-specific.
- **Any tribunal decisions** on these reliefs. The case law in the notes (Roberts v McGregor, HMRC v Tooth, Steeden v Carver, Scorer v Olin Energy, Rowland v HMRC) concerns burden of proof, discovery, filing deadlines and reasonable excuse, not the reliefs on this page.
- **The full MTD treatment of each relief.** Several helpsheets state that MTD users will make claims and adjustments through compatible software instead of the SA boxes cited, but the notes do not say which software fields correspond to which boxes.

---

## Sources used on this page

This page was written by an LLM from structured notes extracted from the mirrored sources below. Always check the upstream source before relying on any figure or deadline.

- [sa-helpsheets:5f67ceae-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/averaging-for-creators-of-literary-or-artistic-works-hs234-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/averaging-for-creators-of-literary-or-artistic-works-self-assessment-helpsheet-hs234.md`
- [sa-helpsheets:5f67d41e-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/employee-share-and-security-schemes-and-capital-gains-tax-hs287-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/capital-gains-tax-and-employee-share-schemes-self-assessment-helpsheet-hs287.md`
- [sa-helpsheets:5f67d5b1-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/land-and-leases-the-valuation-of-land-and-capital-gains-tax-hs292-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/capital-gains-tax-land-and-leases-self-assessment-helpsheet-hs292.md`
- [sa-helpsheets:5f67ddc2-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/charitable-giving-hs342-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/charitable-giving-tax-relief-self-assessment-helpsheet-hs342.md`
- [sa-helpsheets:5f67cf48-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/community-investment-tax-relief-hs237-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/community-investment-tax-relief-self-assessment-helpsheet-hs237.md`
- [sa-helpsheets:5f67dc31-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/employee-shares-and-securities-further-guidance-hs305-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/employment-related-shares-and-securities-self-assessment-helpsheet-hs305.md`
- [sa-helpsheets:5f67de13-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/enterprise-investment-scheme-income-tax-relief-hs341-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/enterprise-investment-scheme-income-tax-relief-self-assessment-helpsheet-hs341.md`
- [sa-helpsheets:f689f4a2-7da1-41a3-b37d-b18c346219ed](https://www.gov.uk/government/publications/foreign-income-and-gains-fig-regime-self-assessment-helpsheet-hs266) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/foreign-income-and-gains-fig-regime-self-assessment-helpsheet-hs266.md`
- [sa-helpsheets:5f67e2d6-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/furnished-holiday-lettings-hs253-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/furnished-holiday-lettings-self-assessment-helpsheet-hs253.md`
- [sa-helpsheets:5f67db85-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/gains-on-foreign-life-insurance-policies-hs321-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/gains-on-foreign-life-insurance-policies-self-assessment-helpsheet-hs321.md`
- [sa-helpsheets:5f67dcd2-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/gains-on-uk-life-insurance-policies-hs320-self-assessment-helpsheet) - 3 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/gains-on-uk-life-insurance-policies-self-assessment-helpsheet-hs320.md`
- [sa-helpsheets](https://www.gov.uk/government/collections/self-assessment-helpsheets-main-self-assessment-tax-return) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/index.md`
- [sa-helpsheets:5f67dd70-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/interest-and-alternative-finance-payments-eligible-for-relief-on-qualifying-loans-and-alternative-finance-arrangements-hs340-self-assessment-helpshee) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/interest-and-alternative-finance-payments-eligible-for-relief-on-qualifying-loans-and-alternative-finance-arrangements-self-assessment-helpsheet-hs340.md`
- [sa-helpsheets:5f67e282-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/limit-on-income-tax-reliefs-hs204-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/limit-on-income-tax-reliefs-self-assessment-helpsheet-hs204.md`
- [sa-helpsheets:5f67d46f-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/negligible-value-claims-and-income-tax-losses-on-disposals-of-shares-you-have-subscribed-for-in-qualifying-trading-companies-hs286-self-assessment-he) - 3 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/negligible-value-claims-and-income-tax-losses-on-disposal-of-shares-self-assessment-helpsheet-hs286.md`
- [sa-helpsheets:5f67dbe3-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/other-taxable-income-hs325-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/other-taxable-income-for-self-assessment-helpsheet-hs325.md`
- [sa-helpsheets:5f67cefb-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/remittance-basis-hs264-self-assessment-helpsheet) - 4 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/paying-tax-on-the-remittance-basis-self-assessment-helpsheet-hs264.md`
- [sa-helpsheets:5f67defe-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/pensions-tax-charges-on-any-excess-over-the-lifetime-allowance-annual-allowance-special-annual-allowance-and-on-unauthorised-payments-hs345-self) - 5 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/pension-savings-tax-charges-self-assessment-helpsheet-hs345.md`
- [sa-helpsheets:5f67cd23-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/qualifying-care-relief-foster-carers-adult-placement-carers-kinship-carers-and-staying-put-carers-hs236-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/qualifying-care-relief-for-carers-self-assessment-helpsheet-hs236.md`
- [sa-helpsheets:5f67e327-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/seed-enterprise-investment-scheme-income-tax-and-capital-gains-tax-reliefs-hs393-self-assessment-helpsheet) - 2 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/seed-enterprise-investment-scheme-income-tax-and-capital-gains-tax-reliefs-self-assessment-helpsheet-hs393.md`
- [hmrc-manual-ch](https://www.gov.uk/hmrc-internal-manuals/compliance-handbook) - 16 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/ch.md`
- [hmrc-manual-em](https://www.gov.uk/hmrc-internal-manuals/enquiry-manual) - 17 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/em.md`
- [hmrc-manuals-index](https://www.gov.uk/government/collections/hmrc-manuals) - 1 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/index.md`
- [hmrc-manual-salf](https://www.gov.uk/hmrc-internal-manuals/self-assessment-legal-framework) - 15 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/salf.md`
- [hmrc-manual-sam](https://www.gov.uk/hmrc-internal-manuals/self-assessment-manual) - 17 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/sam.md`
- [itepa-2003](https://www.legislation.gov.uk/ukpga/2003/1/contents) - 1 note(s) - mirrored at `corpus/legal-system/primary-legislation/acts/itepa-2003.md`
- [tma-1970](https://www.legislation.gov.uk/ukpga/1970/9/contents) - 1 note(s) - mirrored at `corpus/legal-system/primary-legislation/acts/tma-1970.md`
