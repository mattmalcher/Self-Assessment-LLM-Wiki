---
title: What income is charged, and where it goes on the return
generated: true
generated_on: '2026-09-09'
generated_by: claude-cli:opus
input_hash: 067e755371f5e20a
note_count: 100
sources:
- hmrc-manual-ch
- hmrc-manual-em
- hmrc-manual-salf
- hmrc-manual-sam
- hmrc-manuals-index
- hmrc-tools-calculators
- itepa-2003
- sa-helpsheets
- sa-helpsheets:5f67cefb-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67db85-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dbe3-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dc31-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dcd2-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dd70-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67defe-7631-11e4-a3cb-005056011aef
- sa-helpsheets:f689f4a2-7da1-41a3-b37d-b18c346219ed
---

# What income is charged, and where it goes on the return

!!! danger "Unofficial - not HMRC, not advice, written by an LLM"

    This page is **not** an HMRC publication and has no connection to HMRC or
    any government body. It was **written by a language model** from mirrored
    source material, and can be wrong, incomplete or out of date. It is not
    tax advice. Check every figure, date and rule against the cited source
    before relying on it, and see
    [GOV.UK](https://www.gov.uk/self-assessment-tax-returns) for official
    guidance.

This page maps the main income types a Self Assessment return has to carry onto the provisions that charge them, the helpsheets that explain them, and the return pages or boxes where the notes say the figures belong. For each type it states what determines the amount charged — the measurement rule an implementation would need. It is an unofficial page assembled from legislation, HMRC manuals and HMRC helpsheets; where a position is HMRC's interpretation rather than statute, that is flagged.

---

## 1. The structural picture

ITEPA 2003 s.1 sets out the Act's own structure: charges on employment income, pension income and social security income, the high income child benefit charge, the winter fuel payment charge, PAYE, and payroll giving (ITEPA 2003 s.1). The notes supplied cover ITEPA in depth; trading, property and savings income are covered here mainly through helpsheets and HMRC manuals rather than through their charging Acts (see **Gaps in the sources**).

Return pages referenced across the notes:

| Page | Covers | Source |
|---|---|---|
| SA100 (main return) TR 3 | Dividends (box 4), other UK income (boxes 17, 18), pension amounts (box 11) | HS305; HS325; HS345 |
| SA101 Additional information, page Ai 2 | Share schemes (box 1), employment lump sums (boxes 3–10), other tax reliefs (box 5) | HS305; HS325; HS340 |
| SA101 page Ai 4 | Pension savings tax charges (boxes 10–18) | HS345 |
| SA102 Employment | Employment income, incl. post-P45 share amounts | HS305 |
| SA106 Foreign (F2/F3) | Foreign income, overseas pensions, foreign life policy gains, remitted amounts | HS264; HS321; HS345 |
| SA108 Capital gains summary | Chargeable gains (must be accompanied by a full CG computation) | SAM general points, item 6 |
| SA109 Residence / FIG | FIG regime and TRF designations | HS264 s.4; HS305 |
| SA904 | Trust and estate foreign gains | HS321 s.6.2 |

HMRC's internal capture guidance treats a return as **unsatisfactory** if a supplementary page flagged on TR2 is not completed, or mandatory boxes are missing (SAM121260; SAM121170). Omission of Class 4 NIC is an express exception and does not make a return unsatisfactory (SAM121260).

---

## 2. Employment income and benefits

**Charging structure.** "Employment income" means earnings within Chapter 1 of Part 3, amounts treated as earnings, or amounts counting as employment income (ITEPA 2003 s.7(2)). It splits into **general earnings** (earnings and amounts treated as earnings, excluding exempt income — s.7(3)) and **specific employment income** (amounts counting as employment income under Parts 6, 7, 7A or another enactment, excluding exempt income — s.7(4)). "Employment" covers contracts of service, apprenticeship, and Crown service (s.4(1)); "office" covers any position with independent existence fillable by successive holders (s.5(3)).

**Amount charged.**

| Component | Rule | Ref |
|---|---|---|
| Net taxable earnings | TE (total taxable earnings for the year) − DE (deductions allowed under s.327(3)–(5)); negative treated as nil | ITEPA 2003 s.11(1)–(2) |
| Net taxable specific income | TSI − DSI (deductions under Tax Acts provisions outside the s.327(3)–(4) lists); negative treated as nil | ITEPA 2003 s.12(1)–(2) |
| Who is liable | The employee; personal representatives where earnings are received or remitted after death | ITEPA 2003 s.13(2)–(4C) |
| Allocation to a year | Earnings earned in or in respect of a period; if the period spans two or more years, apportioned on a just and reasonable basis | ITEPA 2003 s.29 |

Deductions are constrained: they cannot exceed the earnings (s.329), cannot be taken twice (s.330(2)), and ss.336–342 only apply where earnings are "earnings charged on receipt" (taxable under s.15 or s.27) — s.353 applies instead to "earnings charged on remittance" (taxable under s.22 or s.26) (ITEPA 2003 s.335(4)). Reimbursed expenses are deductible only to the extent the reimbursement is itself in earnings (s.334).

**Benefits.** The benefits code produces "amounts treated as earnings". Machine-implementable examples in the notes:

| Benefit | Amount charged | Ref |
|---|---|---|
| Living accommodation costing over £75,000 | Basic cash equivalent plus "additional yearly rent" computed at Step 2 of s.106(2) using the official rate of interest and cost C | ITEPA 2003 s.106 |
| Car | List price adjustments and accessories, less employee capital contributions capped at £5,000, × appropriate percentage | ITEPA 2003 ss.131–132A, 139–141 |
| Car appropriate percentage | 4% at 0 g/km CO2; 4/7/10/14/16% for 1–50 g/km by electric range band; 17–21% for 51–74; then 21% + 1pp per 5 g/km above 75, capped at 37% | ITEPA 2003 s.139(1), (3) |
| Diesel supplement | +4 percentage points, capped at 35%; not applied where the car meets the Euro 6d standard | ITEPA 2003 s.141(2), (2A) |
| Car fuel | Appropriate percentage × £29,200 | ITEPA 2003 s.150(1) |
| Optional remuneration (salary sacrifice) | Compare cash equivalent with "amount foregone"; charge the greater | ITEPA 2003 ss.149A, 154A |

Nil car fuel benefit requires the employee to make good the whole private-use fuel expense **on or before 6 July following the tax year**, or that fuel was available only for business travel (ITEPA 2003 s.151(2)–(3)). The same 6 July date applies to van fuel (s.163(3)(c)) and to rent counting against the excess-rent calculation for over-£75,000 accommodation (s.106(3)(a)(iv)).

Exemptions remove amounts from charge entirely: mobile telephones (s.319), eye tests (s.320A), health screening and one medical check-up per employer per year (s.320B), recommended medical treatment capped at £500 a year and lost entirely if exceeded or provided by salary sacrifice (s.320C(2), (6)), flu vaccinations (s.320D), suggestion awards (encouragement awards up to £25; financial benefit awards subject to a £5,000 cap) (ss.321–322), pooled cars and vans (ss.167–168), and a long list for special classes of employee — ministers, armed forces, consular staff, offshore workers (ss.295–306).

**Reporting mechanics.** Employers give a P60 by **31 May** and P11Ds to HMRC and to the employee by **6 July**; third parties providing benefits not on the P11D must give written details by **6 July following the tax year** (PAYE Regulations; TMA 1970 s.15, as described in SALF). SALF records HMRC's estimate that around 4 million of 28 million PAYE taxpayers are sent SA returns because of higher-rate liability or complex affairs.

**Mandatory boxes.** SAM121170 says the Employment page requires box 4 (employer's PAYE reference) and box 6 (company director status). HMRC's view is that a return should not be rejected for a missing box 4 if the employer's name is in box 5, even where the PAYE reference cannot be traced (SAM, "In SA in one or more earlier years").

### Employment-related securities and share schemes

"Employment-related securities" are securities acquired because of employment where the employer or a connected person gave an opportunity to acquire them — shares in UK or overseas companies or unincorporated bodies, and debentures, loan stock, bonds and other debt instruments (HS305).

- **Where it goes.** HS305 says the taxable amount goes in box 1 "Share schemes" on page Ai 2 of SA101, using the relevant working sheet, where the employer has not deducted tax on the whole amount or used a PAYE valuation that was too low. Amounts already fully taxed by the employer (P60/P45) should not be entered there. Amounts notified separately after a P45 has been issued go on the Employment pages (SA102) (HS305).
- **Amount charged.** The general formula given by HS305 is **UMV × (IUP − PCP − OP) − CE**, where UMV is unrestricted market value, IUP the initial uncharged proportion, PCP the previously charged proportion, OP the outstanding proportion and CE consideration given and expenses incurred (HS305, "How to calculate the Income Tax"). The statutory version for restricted securities is at ITEPA 2003 s.428, with IUP, PCP, OP and CE each defined by formula in s.428(2)–(7).
- **Restricted securities.** Defined by ITEPA 2003 s.423 as securities subject to a contract, agreement, arrangement or condition providing for transfer, reversion, forfeiture or restriction, where that reduces market value. No charge on acquisition (s.425(2)), but a chargeable event later (s.426) — cessation of restriction, variation, or disposal for consideration to a non-associated person (s.427(3)). Employer and employee may jointly elect to disapply the exemption; the election **may not be made more than 14 days after the acquisition** (s.425(5)(b)) — the same 14-day limit applies to a s.431 election (s.431(5)(b)) and to a s.430 election to ignore outstanding restrictions, measured from the chargeable event (s.430(3)(b)).
- **Convertible securities** (ITEPA 2003 s.436) and **securities options** (Chapter 5) have their own chargeable events. For options the taxable amount is the gain realised less deductible amounts (s.478(1)); the gain on acquisition of securities is MV − C (s.479(2)–(4)).
- **Anti-avoidance thresholds.** A charge arises under s.446B where market value was artificially reduced by **at least 10%** by things done otherwise than for genuine commercial purposes in the **7 years** ending with the acquisition. HS305 uses the same 10% / 7-year figures for artificially enhanced or reduced value.
- **Tax-advantaged plans.** SIP (Schedule 2), SAYE (Schedule 3), CSOP (Schedule 4) and EMI (Chapter 9 / Schedule 5) carry exemptions. EMI qualifying options must be exercised on or before the **fifteenth anniversary** of grant (tenth for a specified Northern Ireland company) (ITEPA 2003 s.529(2), (2A)); exercise more than **90 days** after a disqualifying event triggers modified consequences (s.532(1)(b)). HS305 says dividend shares ceasing to be subject to a SIP within 3 years for a non-exempt reason are reported in the box 4 dividend boxes on page TR 3.
- **NIC agreements.** HS305 states that employee-paid employer's NICs are deductible only if paid to the employer **before 5 June following the tax year** of the share transaction; the statute sets the same 5 June cut-off for relief under s.481(2)(a) and s.428A(2)(a).

### Employment lump sums and terminations

HS325 directs employment lump sums, compensation and deductions to **boxes 3 to 10 on page Ai 2** of SA101, with Working Sheet 2 for complex cases. It states a £30,000 exemption limit for redundancy/termination payments and gives illustrative examples (a £10,000 redundancy; a £40,000 redundancy with £1,000 post-employment notice pay).

Statutory backing: amounts charged under s.403 are treated as the **highest part of total income** for most income tax purposes, but not for top-slicing relief under ITTOIA 2005 ss.535–537 (ITEPA 2003 s.404A). Exceptions and reductions include legal costs (s.413A), foreign service (s.413, with thresholds mirrored in s.395B for EFRBS lump sums: full exemption where three-quarters or more of reckonable service is foreign service; or the whole of the last 10 years where the period exceeds 10 years; or one-half or more including any 10 of the last 20 where it exceeds 20 years).

HS325 also defines an **employer-financed retirement benefits scheme** as one providing retirement and death benefits, usually employer-established but not registered by HMRC.

---

## 3. Pensions

**UK pensions.** Taxable pension income is the **full amount accruing in the tax year**, and the liable person is the recipient (ITEPA 2003 ss.569–572A; for social security pensions, ss.577–579 apply the same "full amount accruing, regardless of when actually paid" rule — s.578). "Pension" includes a pension paid voluntarily or capable of being discontinued (s.570).

**Foreign pensions.** Chapter 4 charges foreign pensions (ss.573–576). Taxable pension income is the full amount arising in the year, or the UK part where the year is split (s.575(1), (1A)), and is treated as relevant foreign income for ITTOIA 2005 Part 8 Chapters 2–4 purposes. Relevant lump sums under non-registered overseas schemes are brought in by s.574A with a three-step deduction calculation. HS264 notes that the **10% reduction for foreign pensions no longer applies from 6 April 2017**.

**Temporary non-residence.** Both s.576A (relevant non-UK schemes) and s.579CA (registered schemes) treat "relevant withdrawals" taken while temporarily non-resident as arising in the period of return — but only where the aggregate of withdrawals under both sections for the same temporary period **exceeds £100,000** (ITEPA 2003 s.576A(2); s.579CA(2)). Double taxation relief arrangements do not prevent the charge (s.576A(7); s.579CA(5)). HS345 defines temporary non-residence broadly as leaving the UK, later resuming UK residence, having been solely UK resident for part of at least 4 of the 7 tax years preceding departure and not solely resident for a period of less than 5 full tax years. HS345 says drawdown taken during such a period goes in **box 11 of the pension section on the main return** (registered schemes) or the **overseas pensions boxes on page F2 of SA106** (overseas schemes).

**Exemptions.** Wounds and disability pensions (s.641), National-Socialist persecution compensation, certain Malawi/Trinidad and Tobago/Zambia government pensions (s.643), disablement pensions (s.644, exempt only up to a computed "exempt amount"), coal allowances for former miners (s.646), consular employees' foreign pensions (s.646A), awards for bravery (s.638), and pensions for death due to military or war service (s.639). Chapter 18 exempts several overseas pensions where a **foreign residence condition** is met — the recipient is not UK resident *and* has claimed non-residence to HMRC and HMRC is satisfied (ITEPA 2003 s.647(2)–(3)).

### Pension savings tax charges (SA101 page Ai 4)

HS345 (2026 edition, figures for **2025 to 2026**):

| Item | Figure | Ref |
|---|---|---|
| Standard annual allowance | £60,000 | HS345 |
| Money purchase annual allowance | £10,000 | HS345 |
| Alternative annual allowance | £50,000 (i.e. AA − £10,000) | HS345 |
| Threshold / adjusted income for taper | £260,000 | HS345 |
| Taper rate | £1 reduction per £2 of adjusted income above £260,000 | HS345 |
| Minimum tapered AA | £10,000 (floor, even if formula gives less) | HS345 |
| Carry-forward | Previous 3 tax years; cannot be added to the £10,000 money purchase allowance | HS345 |
| Pension savings statement deadline | 6 October 2026, where scheme input exceeds £60,000 (or £10,000 money purchase) | HS345 |
| AA charge rates | 45%, 40% or 20% (may differ under Scottish/Welsh rates) | HS345 |

Defined benefits input amount = closing value − opening value; the opening value is annual pension × **16** plus any separate lump sum, increased by **3.1%**; the closing value uses × 16 without the 3.1% step (HS345). Where negative, the input is nil. Overseas scheme inputs are adjusted by (TE + TSI) / EI.

Boxes: excess pension savings in **box 10**; tax the scheme is paying in **box 11**; PSTR in **box 12**; overseas transfer charge transferred value in **box 11.1** and tax paid by the scheme in **box 11.2**; unauthorised payment not subject to surcharge in **box 13**, subject to surcharge in **box 14**; foreign tax on an unauthorised payment in **box 15**; short service refund from an overseas scheme in **box 16**; foreign tax on that refund in **box 18** (HS345).

| Charge | Rate | Ref |
|---|---|---|
| Overseas transfer charge | 25% of the "transferred value" (transfers requested on or after 9 March 2017) | HS345 |
| Unauthorised payments charge | 40% | HS345 |
| Unauthorised payments surcharge | further 15%, where 25% of scheme rights threshold reached | HS345 |
| Short service refund (overseas scheme), 2025–26 | 20% on the first £20,000; 50% above | HS345 |

HS345 notes that the unauthorised payments charge/surcharge and short service refund charge are **not charges on income** and so are not exempted by double taxation agreements, though foreign tax credit relief can still be claimed against them. Taxable lump sums from overseas schemes (trivial commutation, winding-up, serious ill-health, UFPLS, certain death benefits) go in **box 17 "other taxable income" on page TR 3** and must not also be entered in box 16 on page Ai 4 (HS345).

---

## 4. Trading and property income

The supplied notes describe the return mechanics and registration thresholds rather than the charging provisions.

**When trading or property income puts someone in SA (HMRC's internal criteria, SAM100060):**

| Trigger | Threshold | Ref |
|---|---|---|
| Self-employment, partnership, minister of religion, sharefisherman | any (receipt of such income) | SAM100060 |
| Property letting — gross | over £10,000 | SAM100060 / SAM100050 note 6 |
| Property letting — net | more than £2,500 | SAM100060 |
| Trading Income Allowance (2017-18 on) | turnover up to £1,000: usually no need to register, subject to exceptions | SAM100060 |
| Property Income Allowance (2017-18 on) | turnover up to £1,000: usually no need to register, subject to exceptions (e.g. non-resident landlords) | SAM100060 |
| Non-resident landlord reclaiming NRL-scheme tax | must register even if within the Property Income Allowance | SAM100060 |

SAM100050 adds that self-employment income shown on a self-employment page but included in the PAYE code always requires an SA return regardless of the £2,500 threshold, and that property loss cases with gross income below £10,000, or Rent a Room income below the exempt amount, do not require an SA record unless the taxpayer cannot give details of a new source.

**Standard Accounts Information (SAI).** HMRC's position is that a taxpayer with self-employment turnover of **£85,000 or more** must complete the SAI boxes, not just a single profit or loss figure; attaching detailed accounts and computations does *not* satisfy the requirement, and the return is treated as unsatisfactory, except for partnerships with turnover of £15 million or more and CT partnerships (SAM121220). HMRC treats this as flowing from the statutory notice under TMA 1970 s.8. For **trust** returns the SAI threshold is stated as £30,000 (SAM123180). The Short Tax Return (SA200) has a turnover threshold of £90,000 for both self-employment and land and property (SAM121260).

**Period boxes.** The *accounting period* is the period to which the income, expenses, tax adjustments and balance sheet relate (SEF1 boxes 8/9, or SA200 box 3.4, end date only). The *basis period* identifies the profits taxable in a tax year, normally the 12 months to the annual accounting date (SEF4 boxes 64/65, or SA200 boxes 3.12A/3.12B) (SAM121150). HMRC's view is that it is not reasonable to reject a return solely because dates appear in one set of boxes but not the other (SAM121141).

**Prior year adjustments.** Claims for relief now for trading losses go in TCS 2 box 16; claims to carry back loss relief to an earlier year go in TCS 2 box 15 (SAM121180). HMRC checks that the accounting period for the year of loss has finished before processing a brought-back claim; where the earlier year's return is outstanding it holds the case and deals with the claim manually (SAM121180). Farmer's averaging and literary/artistic spreading are handled as prior year adjustments (SAM121180; HS234 is the relevant helpsheet).

**Own goods.** EM3510 records HMRC's approach to goods taken by a trader for personal use, adjusting turnover, cost of sales, or the tax-adjustment boxes on the SA return.

**Furnished holiday lettings** are the subject of helpsheet **HS253** (helpsheet index; SAM Help Sheets index). The notes supplied contain the title only — see **Gaps in the sources**.

**Qualifying loan interest** is not income but is relevant to the same pages: HS340 puts relief for interest and alternative finance payments on qualifying loans in **box 5 of "other tax reliefs", page Ai 2** of SA101. Qualifying purposes include buying shares in a close company, acquiring a partnership interest, and buying business equipment (equipment relief only if capital allowances could be claimed, restricted to the business-use proportion). Overdraft and credit card interest do not qualify. The overall limit on income tax reliefs is the greater of £50,000 and 25% of adjusted total income (HS340 s.2; HS204). For 6 April 2025 to 5 April 2026, HS340 says relief cannot be claimed for finance costs on residential property in a partnership's property business — instead these feed a reduction in Income Tax at box 12.

**Making Tax Digital.** HS325, HS340 and HS345 all carry the same customer-facing note: taxpayers required to use Making Tax Digital for Income Tax make claims and adjustments for self-employment and property income through compatible software and quarterly digital updates rather than the SA boxes described.

---

## 5. Savings and dividends

The notes cover savings and dividend income mainly through SA registration thresholds and through the interaction with the remittance basis.

| Item | Threshold / rate | Period | Ref |
|---|---|---|---|
| Savings/investment income (tax deducted) requiring SA record | £10,000 or more before tax | up to 2015-16 and 2016-17 onwards | SAM100060 |
| Savings/investment income not requiring a return | £10,000 or less before tax | 2016-17 onwards | SAM100050 note 4 |
| Dividend income requiring SA record | £10,000 or more before tax | 2016-17 onwards | SAM100060 |
| Untaxed interest requiring SA | £2,500 | 2015-16 and earlier only | SAM100050 note 3 |
| Dividend Allowance | £500 | 2024 to 2025 | HS264 |
| Dividend rates | 8.75%, 33.75%, 39.35% | — | HS264 |
| Foreign dividends de minimis for PAYE coding review | less than £300 | — | SAM (coding income from the SA return, item 12) |

HMRC's guidance in the "paying tax on foreign income" material is that a UK resident receiving **any** foreign interest, however small and even if already taxed abroad, must complete a tax return (SAM, foreign income section) — a stricter position than the domestic thresholds above.

Dividend shares leaving a SIP within 3 years for a non-exempt reason are reported at box 4 on page TR 3 (HS305).

**Accrued Income Scheme** is covered by helpsheet **HS343**; the notes give the title only.

---

## 6. Foreign income, the remittance basis, and the FIG regime

Three regimes appear in the notes, applying to different periods.

### 6.1 The FIG regime (from 6 April 2025)

A **qualifying new resident** may claim relief on **qualifying foreign income** — profits of a trade carried on wholly outside the UK, a UK resident partner's share of a wholly-overseas firm, profits of an overseas property business, dividends from non-UK resident companies, foreign interest, and foreign pension income other than disqualified pension income (RFIG45100, via HS266). Income only qualifies if it **arises on or after 6 April 2025**; a claim cannot be made for an earlier tax year (HS266 caveats).

Two things are expressly outside the FIG relief:

- **Disqualified income** — certain settlements-legislation income, income from a UK-situated security following a share exchange involving a non-UK incorporated close company, transferred income streams, performance income, and certain pension income (RFIG45200).
- **Relevant foreign earnings and foreign specific employment income** — these are not qualifying foreign income; separate relief may be available via an Overseas Workday Relief election (HS266; EIM43550).

**Effects of a claim.** Foreign Tax Credit Relief cannot be claimed on income covered by a FIG claim — only on the proportion not covered (HS266 s.5.4). Pension relief may be reduced, but not below the **basic amount of £3,600** (HS266 s.5.4; PTM044100).

The employment-income analogue is in statute: a qualifying new resident may make a **foreign employment election** under ITEPA 2003 s.41M and then a **foreign employment relief claim** under s.41P. Both must be made in a return under TMA 1970 s.8, and both must be made before the end of **12 months beginning with the 31 January after the end of** the qualifying year (election, s.41M(8)) or the tax year of claim (claim, s.41P(6)). Relief is capped at the lesser of **30% of relevant qualifying employment income and £300,000** (ITEPA 2003 s.41R(2)).

### 6.2 The remittance basis (pre-2025-26) and the Temporary Repatriation Facility

For tax years before 2025-26 the remittance basis (ITA 2007 ss.809B, 809D, 809E) determined taxable earnings under ITEPA 2003 Chapter 5 of Part 2. Chargeable overseas earnings are taxed on remittance where the employee did not meet the s.26A requirement, the employer was foreign, and duties were performed wholly outside the UK (ITEPA 2003 ss.22, 23). Section 24 limits this where there are associated UK employments; s.24A restricts access to the remittance basis altogether where five conditions are met, including a tax-saving threshold test comparing X% with Y%, where **Y% is 65% of the additional rate** for the year (ITEPA 2003 s.24A(15)).

**HS264 completion rules for SA106:**

| Situation | What HS264 says to do |
|---|---|
| Unremittable income (box 1) | A remittance basis taxpayer should **not** complete box 1 |
| Partial remittance with foreign tax (box 2) | Claim only the proportionate share of foreign tax corresponding to the amount remitted; apportion (Example 7: £10,000 rents, £2,000 foreign tax, £7,500 in column B, £1,500 in column C) |
| Remitted foreign dividends | Do **not** use the "Dividends from foreign companies" rows; use "Remitted foreign dividend income" rows on pages F2 and F3, separate sheets per country, totals of columns D and F into boxes 7.3 and 7.4 |
| Overseas property income on the remittance basis | Do **not** fill boxes 14–24, 26, 31 or 32; complete columns A to F and boxes 25 and 27–30 in the Summary section |
| Treaty-exempt foreign pension | Give the payer and the relevant treaty in "Any other information" or on a separate sheet |
| Currency | Convert at the exchange rate on the date of remittance (or the bank's rate if credited to a sterling account); enter all amounts in sterling on F2 and F3 |

**Rate treatment of remitted dividends.** HS264 states that remitted foreign dividends are taxed at **normal UK rates (20%, 40%, 45%)**, not the dividend rates, and that the Dividend Allowance and dividend nil rate do not apply to them. Dividends paid on or after 6 April 2016 carry no dividend tax credit on remittance; those paid or accrued before that date do.

**Mixed funds.** A mixed fund is a fund of money or other property containing more than one type of income or capital (including foreign chargeable gains), or income or capital from more than one tax year — for example a bank account with different types of income paid in, or an overseas asset bought with money from more than one source or year (HS264). Statutory ordering rules apply; HS264 directs readers to RDR1 for pre-2017 treatment and notes that **mixed fund cleansing was available only from 6 April 2017 to 5 April 2019**.

**Special Withholding Tax (SWT)** is tax withheld on certain payments to UK residents under the European Savings Directive and equivalent agreements, in addition to foreign tax deducted at source (HS264). To have SWT treated as a payment on account, the taxpayer makes a claim on the return and supplies certificates from the Swiss paying agent. HS264 says the set-off or repayment is itself treated as a remittance, and that the set-off is **normally regarded as occurring at 31 January following the tax year**.

**Temporary Repatriation Facility (TRF).** Available from 6 April 2025 for three tax years, allowing former remittance basis users to designate pre-6 April 2025 foreign income and gains ("qualifying overseas capital") at a reduced rate (HS264 s.4):

| Tax year | TRF rate |
|---|---|
| 2025-26 | 12% |
| 2026-27 | 12% |
| 2027-28 | 15% |

Designation is made on **SA109**. Designated "TRF capital" is remitted in priority to other amounts in a mixed fund regardless of the year it arose. HS264 says there is no obligation to designate the full amount — partial designations are permitted — and that designation does not require an actual remittance during the TRF period, though remittances in the same year as designation must still be reported. HS305 applies the same 12% figure to internationally mobile employees' chargeable foreign securities income remitted in 2025-26 under the TRF, reported on **SA109** rather than through the HS305 working sheets.

HS266 flags an important limit: a former remittance basis user returning after **10 consecutive tax years** of non-UK residence cannot claim FIG relief for foreign income or gains arising before 6 April 2025 while UK resident and on the remittance basis, regardless of when remitted.

### 6.3 Internationally mobile employees and securities

ITEPA 2003 Chapter 5B (ss.41F–41L) governs taxable specific income from employment-related securities for internationally mobile employees. Section 41F applies where one of three "international mobility conditions" is met — the remittance basis applied, the individual was not UK resident, or the period falls in the overseas part of a split year (s.41F(2)). Section 41G sets the "relevant period" differently by charging chapter (e.g. acquisition to chargeable event for restricted and convertible securities), subject to a just-and-reasonable override (s.41G(9)). Section 41H splits securities income into **chargeable foreign securities income** and **unchargeable foreign securities income**. HS305 says unchargeable foreign securities income should **never** be included in the working sheets; and that where the employer had enough information and handled it correctly via PAYE/P60, completing SA101 box 1 on page Ai 2 is sufficient.

---

## 7. Chargeable event gains on life policies

Gains on life insurance policies are taxable **as income, not capital gains**; capital losses and the annual exempt amount cannot be set against them (HS320; HS321).

| Feature | UK policies (HS320) | Foreign policies (HS321) |
|---|---|---|
| Basic rate treated as paid | Yes — and it is not repayable in any circumstances | Normally no such non-repayable credit |
| Where reported | Not stated in the supplied notes for individuals (see Gaps) | Foreign section, "Other overseas income and gains" / SA106; trustees use SA904 |
| Qualifying policy | Min. 10-year term, fairly even premiums, and (if taken out or varied on/after 21 March 2012) premiums under £3,600 a year | A single premium policy can never be qualifying |
| Pre-1968 policies | A policy made before 20 March 1968 and unchanged since gives rise to no gain; changes after that date may bring it in scope | Same |

**Amount charged.**

| Event | Formula | Ref |
|---|---|---|
| Maturity / full surrender | TB − (TD + PG) | HS320 s.12.1; HS321 s.12.1 |
| Death | TB = surrender value immediately before death | HS320 s.12.2 |
| Sale / assignment | TB = sale price, or market value if connected persons | HS320 s.12.3 |
| Part surrender | Excess over the unused 5% per year allowance (max 100% of premiums after 20 consecutive years) | HS320 s.13; HS321 s.13 |
| Personal Portfolio Bond | 15% × (A + B − C), where A = cumulative premiums, B = cumulative prior PPB gains, C = cumulative part-surrender gains; **no PPB gain in the final insurance year** | HS320 s.14; HS321 s.14 |

TB is total benefits, TD total deductions (generally all premiums), PG previous gains taxed as someone's income in an earlier year (HS320 s.12.1).

**Timing.** The insurance year is normally the 12 months beginning on the anniversary of the policy start; all part surrenders in the same insurance year are treated as arising at its end. The final insurance year is the one in which the policy ends; if it would begin and end in the same tax year it is extended to include the previous insurance year (HS321 s.7). Where part surrenders and a full surrender fall in the same insurance year, only the gain on the full surrender is reported (HS321 caveats).

**Reliefs and ordering.**

- **Top slicing relief (TSR)** — a reduction in *tax*, not in the gain; the full gain is still reported on the return (HS320 s.10.1). Not available to trustees or personal representatives (HS320 s.10.1; HS321 s.6.1 caveats).
- **Time apportioned reduction** — available to individuals (not trustees or PRs) who were non-UK resident during part of the material interest period; computed as A/B (foreign days ÷ total days in the material interest period), with whole non-UK-resident years also subtracted from the "number of years" on the certificate (HS321 s.9.2).
- **Deficiency relief** — individuals only; reduces tax on other income at relevant rates (higher, default higher, savings higher, dividend upper, Scottish higher, Scottish advanced, Welsh higher) but **not** additional rate tax (HS320 s.10.3; HS321 s.10.3).
- **Order of calculation.** HS320 states: Restricted Relief Qualifying Policy first, then time-apportionment reduction, then top slicing relief. HS321 gives the reduction first, then TSR.
- A **loss** on a policy with no earlier gains attracts no relief, cannot be set against other gains or income, and requires no return entries (HS320 s.10.2).
- **Wholly disproportionate gains** on part surrenders can, on application to HMRC, be recalculated on a just and reasonable basis (HS320 s.11; IPTM3596).

**Registration.** HS321 s.6.1 sets a bright-line rule for someone not already in SA: if the gain plus other savings/investment income **exceeds £10,000**, register for SA and report it on the return; if it is £10,000 or less, report instead by contacting Self Assessment general enquiries or sending a copy of the chargeable event certificate with the National Insurance number to HMRC, BX9 1AS.

**Certificates.** UK and foreign insurers must issue a chargeable event certificate if they know a gain has been made (HS320 Part 1 s.3; HS321 Part 1 s.3). Both helpsheets are explicit that absence of a certificate does not mean no gain arose — certificates may have gone to trustees, nominees, lenders or an old address, or the insurer may not know of the event; policies taken out before 6 April 2000 may carry no certificate obligation at all. The taxable person must report the gain regardless (HS320 Part 2 s.6). Where more than one certificate is issued for the same gain, HS321 says use the later, revised figures.

**Joint ownership.** Each owner enters their own share — equal by default, or half where jointly owned with a spouse or civil partner (HS321 s.9.1).

HMRC's internal capture guidance treats chargeable event gains and top-slicing as an item to be obtained and entered during capture in Revenue Calculation cases (SAM121200).

---

## 8. Other taxable income

HS325 puts miscellaneous and casual income — casual earnings, commission, freelance income — in **boxes 17 and 18 of "Other UK income" on page TR 3**, using Working Sheet 1. A **£1,000 trading and miscellaneous income allowance** applies from 6 April 2017 (HS325). Two limits are stated: losses on "other income" can be used only against income of the same type, and expenses claimed under the trading income allowance cannot create a loss.

HS325 flags that detailed conditions apply to third-party arrangement income taxable under box 3 and advises seeking a tax adviser.

Box 17 is also the destination for taxable overseas-scheme lump sums under HS345 (see §3).

---

## 9. Other income the return has to carry

| Income / charge | Trigger | Where / rate | Ref |
|---|---|---|---|
| Trust and estate income | Further tax due on trust or estate income | Beneficiary enters income attributed to their interest, plus the tax credit, on their own SA return; PRs use form R185 (Estate Income) | SAM100060; SALF806; ITTOIA 2005 Ch.6 Pt.5 |
| Estate income — limited interest | Life tenant taxed on payments made, treated as net of tax | ITTOIA 2005 ss.654, 661 | SALF806 |
| Estate income — absolute interest | Taxed on payments up to the "aggregated income entitlement", as income of the year of payment, net of tax | ITTOIA 2005 ss.652, 660 | SALF806 |
| Residue | Residuary beneficiaries taxed on the **lower** of sums paid out in the year or income arising on their share | SALF806 | SALF806 |
| Lloyd's names/members | Status alone | SA record required | SAM100060 |
| High Income Child Benefit Charge | Adjusted net income exceeds **£60,000** and P or P's partner entitled to child benefit for a week in the year | Appropriate percentage = 100%, or a lower figure from a formula using ANI, L (£60,000) and X (£200), rounded down | ITEPA 2003 ss.681B, 681C |
| HICBC and SA | SA criteria from 2012-13; **from 2024/25 only if the customer chooses not to pay via PAYE** | SAM100060; SAM100050 | |
| Unauthorised pension payments | Receipt | SA record required (see §3 for rates) | SAM100060 |
| Capital gains | CGT due after the annual exemption | SA record with CGT pages, unless already paid via the Real Time Transaction Service and no other SA criteria; SA108 must be accompanied by a full CG computation (attached or in box 35, CG2) | SAM100060; SAM general points item 6 |

**Other SA registration triggers** in SAM100060 that are not income as such: Community Investment Tax Relief claims (any amount); EIS/SEIS relief totalling £10,000 or more; student/postgraduate loan repayment combined with off-payroll working. SAM100050 records a total taxable income criterion of £100,000 for 2017-18 to 2022-23 and £150,000 for 2023-24, and states it does **not** apply for 2024-25 onwards. Seafarers: a UK resident wanting Seafarers' Earnings Deduction must register for SA and claim on the return; a non-UK resident should claim on form R43M and not register (SAM100050 note 8).

**General untaxed income:** SAM100060 gives a £2,500 threshold for untaxed income with a tax liability, for all years, excluding State Pension dealt with through PAYE. From 2016-17 State Pension cases where allowances do not cover the income are handled under PAYE rather than SA.

---

## 10. Figures the taxpayer cannot pin down

HMRC distinguishes two cases (SAM121190; SAM123170 for trusts):

- **Provisional figure** — supplied pending the final or accurate figure.
- **Estimated figure** — the taxpayer wants it accepted as final because an accurate figure is not possible, e.g. records lost.

HMRC's guidance is that the reason for using estimated figures should be given in the "Any other information" box; ticking box 20 on TR7/TR8 is no longer required (SAM121190). Box numbering moved from TR7 to TR8 from 2025-26 (SAM121180 caveats). HMRC tells trustees to provide reasonable provisional figures based on available information rather than delay submission (SAM123170).

**Corrections.** HMRC may repair obvious errors — arithmetical errors, wrong carry-forward between boxes, or missing information HMRC holds — within **9 months** beginning with the day the return is received (SAM121530). The taxpayer may reject a repair, but must do so **in writing within 30 days of the issue of the Revision Notice** (TMA 1970 s.9ZB(4)–(5)); HMRC then reinstates the original figure (SAM121520). SAM121530 notes that in practice the 30-day rule only bites where a return is filed 11 months or more after the filing date, since on-time filers have a 12-month amendment window instead. A tolerance is applied to State Retirement Pension: HMRC accepts a figure up to **£150 less** than the pre-populated figure (SAM121530).

On accuracy penalties: CH81125 says a person who takes reasonable care to check information supplied by another and still files an inaccurate document is not liable to a penalty; "careless" means a failure to take reasonable care judged by the standard of a prudent and reasonable person in that person's position (CH81140; FA 2007 Sch.24 para.3(1)(a), citing *HMRC v David Collis*). CH81125 expressly notes there is **no error correction regime for direct taxes** equivalent to the indirect tax one.

---

## Gaps in the sources

The brief asks for coverage that the supplied notes do not fully support. The following are not covered, or only named:

- **Charging provisions for trading, property, savings and dividend income.** ITTOIA 2005 is referenced only incidentally (e.g. ss.652–661 for estate income, ss.535–537 for top slicing, Part 8 for relevant foreign income). There is no note giving the trading profit or property business charge, the cash basis, the savings/dividend nil rates, or the rates themselves other than the HS264 figures quoted above.
- **Furnished holiday lettings.** HS253 appears only as a title in the helpsheet index (note 10; note 46). The notes contain no FHL qualifying conditions, no treatment of the regime's abolition or continuation, and no return boxes.
- **Which boxes UK life policy gains go in for an individual.** HS321 gives the foreign destination (SA106 / "Other overseas income and gains"); the HS320 notes supplied do not state the equivalent UK box.
- **The SA100 dividend and savings boxes generally.** Only box 4 (dividends, page TR 3) is identified, and only via HS305.
- **Return filing deadlines and penalties** are outside this page's brief and are only touched on incidentally (e.g. the voluntary-return filing dates in SAM121141).
- **Basis period reform.** Only a passing reference survives — a transition profit tool for 2023-24 (HMRC tools and calculators). No substantive rules.
- **Rates and allowances for 2025-26 generally** (personal allowance, income tax bands, savings allowance) are not in the notes.
- **HS266's own return boxes** for making a FIG claim are not given; the notes cover the effects of a claim and what qualifies, and identify SA109 only in the TRF context.
- **Where "chargeable event gains" figures are captured by HMRC** is described (SAM121200, top-slicing calculations during capture) but the corresponding taxpayer-facing box for UK policies is not.

---

## Sources used on this page

This page was written by an LLM from structured notes extracted from the mirrored sources below. Always check the upstream source before relying on any figure or deadline.

- [sa-helpsheets:5f67dc31-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/employee-shares-and-securities-further-guidance-hs305-self-assessment-helpsheet) - 2 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/employment-related-shares-and-securities-self-assessment-helpsheet-hs305.md`
- [sa-helpsheets:f689f4a2-7da1-41a3-b37d-b18c346219ed](https://www.gov.uk/government/publications/foreign-income-and-gains-fig-regime-self-assessment-helpsheet-hs266) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/foreign-income-and-gains-fig-regime-self-assessment-helpsheet-hs266.md`
- [sa-helpsheets:5f67db85-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/gains-on-foreign-life-insurance-policies-hs321-self-assessment-helpsheet) - 3 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/gains-on-foreign-life-insurance-policies-self-assessment-helpsheet-hs321.md`
- [sa-helpsheets:5f67dcd2-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/gains-on-uk-life-insurance-policies-hs320-self-assessment-helpsheet) - 3 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/gains-on-uk-life-insurance-policies-self-assessment-helpsheet-hs320.md`
- [sa-helpsheets](https://www.gov.uk/government/collections/self-assessment-helpsheets-main-self-assessment-tax-return) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/index.md`
- [sa-helpsheets:5f67dd70-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/interest-and-alternative-finance-payments-eligible-for-relief-on-qualifying-loans-and-alternative-finance-arrangements-hs340-self-assessment-helpshee) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/interest-and-alternative-finance-payments-eligible-for-relief-on-qualifying-loans-and-alternative-finance-arrangements-self-assessment-helpsheet-hs340.md`
- [sa-helpsheets:5f67dbe3-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/other-taxable-income-hs325-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/other-taxable-income-for-self-assessment-helpsheet-hs325.md`
- [sa-helpsheets:5f67cefb-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/remittance-basis-hs264-self-assessment-helpsheet) - 2 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/paying-tax-on-the-remittance-basis-self-assessment-helpsheet-hs264.md`
- [sa-helpsheets:5f67defe-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/pensions-tax-charges-on-any-excess-over-the-lifetime-allowance-annual-allowance-special-annual-allowance-and-on-unauthorised-payments-hs345-self) - 5 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/pension-savings-tax-charges-self-assessment-helpsheet-hs345.md`
- [hmrc-tools-calculators](https://www.gov.uk/guidance/hmrc-tools-and-calculators) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-tools.md`
- [hmrc-manual-ch](https://www.gov.uk/hmrc-internal-manuals/compliance-handbook) - 1 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/ch.md`
- [hmrc-manual-em](https://www.gov.uk/hmrc-internal-manuals/enquiry-manual) - 2 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/em.md`
- [hmrc-manuals-index](https://www.gov.uk/government/collections/hmrc-manuals) - 1 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/index.md`
- [hmrc-manual-salf](https://www.gov.uk/hmrc-internal-manuals/self-assessment-legal-framework) - 1 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/salf.md`
- [hmrc-manual-sam](https://www.gov.uk/hmrc-internal-manuals/self-assessment-manual) - 15 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/sam.md`
- [itepa-2003](https://www.legislation.gov.uk/ukpga/2003/1/contents) - 60 note(s) - mirrored at `corpus/legal-system/primary-legislation/acts/itepa-2003.md`
