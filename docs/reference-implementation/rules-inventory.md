---
title: Rules inventory - the machine-implementable rules found in the sources
generated: true
generated_on: '2026-09-09'
generated_by: claude-cli:opus
input_hash: e2c8dc1c8e164565
note_count: 120
sources:
- govuk-sa-detailed-information
- hmrc-manual-artg
- hmrc-manual-ch
- sa-helpsheets:5f67cd23-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67ceae-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67cefb-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67d41e-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67d46f-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67db85-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dc31-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dcd2-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67ddc2-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67defe-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67dfee-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67e282-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67e2d6-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67e327-7631-11e4-a3cb-005056011aef
- sa-helpsheets:f689f4a2-7da1-41a3-b37d-b18c346219ed
---

# Rules inventory - the machine-implementable rules found in the sources

!!! danger "Unofficial - not HMRC, not advice, written by an LLM"

    This page is **not** an HMRC publication and has no connection to HMRC or
    any government body. It was **written by a language model** from mirrored
    source material, and can be wrong, incomplete or out of date. It is not
    tax advice. Check every figure, date and rule against the cited source
    before relying on it, and see
    [GOV.UK](https://www.gov.uk/self-assessment-tax-returns) for official
    guidance.

This page catalogues, by lifecycle stage, every rule in the supplied source notes that is specific enough to be implemented as code. Each entry gives the inputs a function would need, the condition, the result, and the citation. A final section lists rules the sources state too vaguely to implement, and what additional source detail would be required. Nothing here is HMRC guidance; where a rule comes from an HMRC manual rather than statute, that is flagged in the "Source type" column or in surrounding text.

Source-type shorthand used throughout:

| Code | Meaning |
|---|---|
| **S** | Statute (TMA 1970, FA 2007/2008/2009, ITA 2007, etc. as cited in the notes) |
| **M** | HMRC internal manual (CH, ARTG) — HMRC's interpretation and operational practice, not law |
| **G** | Customer-facing guidance (GOV.UK helpsheets HS***) — simplified, may omit edge cases |

---

## 1. Notification (chargeability, registration)

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| N1 | Notify chargeability to IT/CGT | tax year; whether a notice to file was issued; IT/CGT liability | Person is chargeable to IT or CGT and was not issued a return | Must notify HMRC on or before 5 October following the end of the tax year | TMA 1970 s.7; CH "Failing to notify" | S/M |
| N2 | PAYE/deduction-at-source carve-out | income sources; tax deducted at source; net liability | All income subject to PAYE, or tax deducted at source ≥ net liability for the year | No obligation to notify under N1 | CH71220 | M |
| N3 | Notification obligation survives withdrawal of a notice to file | date notice to file withdrawn; subsequently discovered chargeability | Notice to file withdrawn by agreement, then chargeability found | s.7 notification obligation still arises | TMA 1970 s.7(1B); CH143020; CH71240 | S/M |
| N4 | Date a notification failure occurs | statutory notification deadline | — | Failure occurs on the day *after* the final date for compliance | CH71240 | M |
| N5 | Annual vs single obligation (regime selection) | obligation type; tax year of failure | IT is an *annual* obligation — assess each year separately; VAT registration is a *single* obligation | Pre-1 Apr 2010 failures → old penalty rules (e.g. TMA 1970 s.7(8)); on/after → FA 2008 Sch 41 | CH71260; CH71280; CH401310 | M |
| N6 | Life insurance chargeable event gain — SA registration trigger | chargeable event gain; other savings and investment income; already-in-SA flag | Not already in SA **and** (gain + other savings/investment income) > £10,000 | Must register for SA and report the gain in the return | HS320 s.6.1; HS321 s.6.1 | G |
| N7 | Life insurance gain below threshold | as N6 | Not already in SA **and** (gain + other savings/investment income) ≤ £10,000 | Report by contacting SA general enquiries or sending the chargeable event certificate (with NINO) to HMRC, BX9 1AS | HS320 s.6.1; HS321 s.6.1 | G |
| N8 | Non-resident disposal of UK residential property | residence status; disposal of UK residential property interest; conveyance date | Non-UK resident disposes of whole or part interest | Must tell HMRC within 30 days of conveyance | HS264 (Remittance basis 2025) | G |

---

## 2. Filing

### 2.1 Filing obligations and dates

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| F1 | Individual return obligation | notice to file under s.8(1)(a); filing date | Notice issued | Must deliver return by filing date | TMA 1970 s.8(1)(a); CH61180 | S |
| F2 | Individual accounts/statements obligation | notice under s.8(1)(b) | Notice issued | Must deliver accounts, statements or documents by filing date | TMA 1970 s.8(1)(b); CH61180 | S |
| F3 | Trustee return obligation | notice under s.8A(1)(a)/(b) | Notice issued | Same as F1/F2 for trustees | TMA 1970 s.8A(1); CH61180 | S |
| F4 | Partnership return obligation | notice under s.12AA(2) / s.122AA | Notice issued | Nominated/representative partner must deliver partnership return, accounts, statements | TMA 1970 s.12AA(2); s.122AA(2)-(3); CH61180; CH84720 | S |
| F5 | ITSA filing dates | filing method | Paper return | Filing date = 31 October | CH62100 | M |
| F6 | ITSA filing dates | filing method | Electronic return | Filing date = 31 January | CH62100 | M |
| F7 | Assumed filing date pending evidence | — | Filing method not yet known | Assume 31 January until confirmed by actual paper/electronic filing | CH62100 | M |
| F8 | Penalty date | filing date | Always | Penalty date = day after the filing date | CH61160; FA 2009 Sch 55 para 1 | S/M |
| F9 | Sch 55 commencement for ITSA | tax year of return | ITSA returns for the year ended 5 April 2011 onwards (due 31 Oct 2011 paper / 31 Jan 2012 electronic) | FA 2009 Sch 55 penalty regime applies, subject to exceptions at SAM121025 | CH61120 | M |
| F10 | Withdrawal of notice to file | withdrawal decision; existing late-filing penalties | HMRC agrees to withdraw the obligation to file the SA return | All late-filing penalties for that return are cancelled | FA 2009 Sch 55 para 17A; CH61700; CH64280 | S/M |
| F11 | Withdrawal scope (temporal) | entity type; period | Partnerships including companies: periods beginning on/after 6 Apr 2012; other partnerships, individuals, trustees: 2012-13 onwards | Withdrawal-and-cancellation rule (F10) available | CH61180 | M |

### 2.2 Claims and elections made in or alongside the return

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| F12 | FIG regime claim deadline | tax year of claim | Qualifying new resident claiming FIG relief | Claim by the anniversary of 31 January following the end of the tax year (12 months after normal filing date). 2025-26: normal filing date 31 Jan 2027, claim deadline 31 Jan 2028 | HS266 s.4 | G |
| F13 | FIG amendment deadline | as F12; date notice to file issued | Notice to file issued on/before 31 October 2026 | Amendment time limit = same as claim time limit | HS266 s.4 | G |
| F14 | Qualifying new resident test | UK residence history; membership of Commons/Lords | In one of first 4 years of UK residence following ≥10 consecutive tax years of non-UK residence, and not an MP or peer | Eligible for FIG regime | HS266 s.2 | G |
| F15 | FIG requalification | non-residence run length | 4-year window ended | Requalify only after a further ≥10 consecutive tax years of non-UK residence; unused years cannot be rolled over | HS266 s.2, caveats | G |
| F16 | FIG claim side-effects | claim made (income only, gains only, or OWR only) | Any FIG claim | Loss of personal allowance, CGT annual exempt amount, blind person's allowance, marriage-related tax reductions; foreign losses not claimable and not carried forward/back | HS266, caveats | G |
| F17 | FIG relief excluded from ANI | relieved foreign income amount | FIG claim made | Relieved foreign income disregarded in adjusted net income (affects tax-free childcare, HICBC) | HS266 s.5.3 | G |
| F18 | Gift Aid carry-back | payment date; original vs amended return | Payments made between 6 April 2026 and the date the return for y/e 5 April 2026 is submitted | Can be carried back, **only** if claimed in the original return before the appropriate filing date; HMRC will not accept a first or increased carry-back claim in an amended return | HS342 s.1 | G |
| F19 | Gift Aid grossing | donation amount | Gift Aid donation | Gross = donation × 100/80 (basic rate 20%). Relief on £100 gift: £25 at 40%; £31.25 at 45% | HS342 s.1, s.1.1 | G |
| F20 | Gift Aid tax cover | Gift Aid donations; IT+CGT paid | Tax paid < tax reclaimed by charity/CASC | Donor must pay an additional amount of Income Tax | HS342 s.1 | G |
| F21 | Payroll Giving relief cap | adjusted total income | Payroll Giving participation | Relief capped at greater of £50,000 or 25% of adjusted total income | HS342 s.4 | G |
| F22 | Non-UK charity gifts | date of gift | Gifts after 5 April 2024 | No relief on gifts to non-UK charities | HS342, caveats | G |
| F23 | Averaging eligibility (creators) | profits year 1, year 2 | Lower year's profit < 75% of the other year's, **or** one year's profits are nil | Averaging claim available; averaged profit = mean of the two years | HS234 s.4, s.10.1 | G |
| F24 | Averaging exclusions | basis of accounting; business start/cease; partner joins/leaves | Cash basis used, or business started/ended in 2024-25 or 2025-26, or partner joined/left in those years | Averaging claim not available | HS234, caveats | G |
| F25 | Averaging entry points | claimant type | Sole trader | Enter increase/decrease in box 72, SA103F | HS234 s.8 | G |
| F26 | Averaging entry points | claimant type | Partner | Enter increase/decrease in box 11, partnership pages | HS234 s.9 | G |
| F27 | FHL pattern of occupation | total days in lettings each exceeding 31 continuous days | Total > 155 days in the year | Condition not met — property fails FHL test | HS253 | G |
| F28 | FHL availability | days available for letting (excluding owner occupation) | ≥ 210 days (140 for 2011-12 and earlier) | Availability condition met | HS253 | G |
| F29 | FHL letting | days commercially let to public, excluding reduced-rate lets to friends/relatives and lets >31 days (unless unforeseen circumstances) | ≥ 105 days (70 for 2011-12 and earlier) | Letting condition met | HS253 | G |
| F30 | FHL averaging / period of grace election deadline | tax year | Election made | Up to one year after 31 January following the end of the tax year (2024-25 → 31 January 2027) | HS253 | G |
| F31 | Period of grace eligibility | prior-year letting condition status; consecutive grace elections | Letting condition met in the immediately preceding year (alone or via averaging) | Election available; after two consecutive grace elections without meeting the threshold, property ceases to qualify | HS253, caveats | G |
| F32 | FHL loss ring-fence | UK FHL result; EEA FHL result | Both businesses exist | UK FHL losses cannot offset EEA FHL profits or vice versa; keep separate records; compute FHL profit separately from other rental business | HS253 | G |
| F33 | Limit on Income Tax reliefs | aggregate limited reliefs against general income; adjusted total income | Limited reliefs claimed against general income | Cap = greater of £50,000 or 25% of adjusted total income | HS204 s.1.1 | G |
| F34 | When to compute adjusted total income | total income | Total income > £200,000 | Must compute adjusted total income (Working Sheet 1) to determine the 25% limit | HS204 s.3.1 | G |
| F35 | Reliefs outside the cap | relief type | Trading losses against capital gains; losses against profits of the same trade/property business; EIS/SEIS share loss relief | Excluded from the HS204 limit | HS204, caveats | G |
| F36 | Share loss relief claim deadline | loss year | Allowable loss on qualifying shares set against income | Claim within one year of 31 January following the loss year. 2025-26 loss → 31 Jan 2028; 2024-25 loss → 31 Jan 2027 | HS286 "How and when to claim" | G |
| F37 | Share loss relief cap | claimed losses; income | 2013-14 onwards | £50,000 or 25% of that income if greater; does not apply to shares with EIS/SEIS relief attributable | HS286 "How the relief is given" | G |
| F38 | Relief ordering (share losses) | in-year share losses; carried-back share losses; other IT losses | Multiple loss claims in one year | Order: in-year share losses, then carried-back share losses, then other IT losses; deducted from total income before personal allowances | HS286, caveats | G |
| F39 | Negligible value — earlier deemed disposal date | claim date; chosen earlier date | Making a negligible value claim | Earlier specified time may be up to 2 years before the start of the tax year in which the claim is made | HS286 | G |
| F40 | Negligible value — competence conditions | ownership at claim date; when asset became negligible; dissolution status | Must still own the asset at claim date, and asset became negligible while owned; no claim possible after dissolution (deemed disposal at dissolution instead) | Claim valid / invalid | HS286 | G |
| F41 | CG34 valuation check | intended filing date | Wanting HMRC to check a valuation | Apply at least 3 months before the tax return filing date | HS286 | G |
| F42 | SEIS reinvestment relief cap | amount receiving SEIS IT relief | Reinvestment relief claimed | Relief ≤ 50% of the amount on which SEIS IT relief is received; max IT relief £200,000 → max reinvestment relief £100,000 (2025-26) | HS393 s.3.1 | G |
| F43 | SEIS reinvestment relief claim deadline | tax year | 2025-26 helpsheet reference | Latest date 31 January 2032; cannot claim before receiving form SEIS3 | HS393 s.3.3, s.3.4 | G |
| F44 | SEIS disposal relief | holding period; whether IT relief withdrawn | Shares held ≥3 years and full (non-withdrawn) SEIS IT relief received on the whole subscription | No CGT on the gain; otherwise relief wholly/partly denied (disposals to spouse/civil partner excepted) | HS393 s.4 | G |
| F45 | ESS CGT exemption | ESS acquisition value; agreement date; material interest | First £50,000 of ESS acquired; single £50,000 limit across agreements with the same or associated companies | Exempt, unless individual or connected person has/had a ≥25% material interest at acquisition or in the previous year | HS287 s.19 | G |
| F46 | ESS lifetime cap | agreement date | Agreements entered into on/after 17 March 2016 | £100,000 lifetime cap on gains; agreements before that date unaffected | HS287 s.19.1 | G |
| F47 | ESS relief withdrawal | agreement date | Agreements entered into on/after 1 December 2016 | IT reliefs and CGT exemption removed (transitional rules for some employees advised on 23 November 2016) | HS287, caveats | G |
| F48 | AIS small holdings exemption | nominal value of holdings; person type | Nominal value ≤ £5,000 and holder is an individual, personal representative or trust for disabled people | Accrued Income Scheme does not apply; if > £5,000, the scheme applies to any transfer however small | HS343 s.6 | G |
| F49 | AIS year of assessment | transfer date; next interest payment date | Any AIS transfer | Profit/loss taxed in the tax year in which the **next interest payment date** falls, not the transfer date | HS343, caveats | G |
| F50 | AIS rounding | net accrued income result | Entering in box 3, page Ai 1 | Round profits **down** to nearest whole pound; round losses **up** to nearest whole pound; do not change boxes 1 and 2 | HS343 s.8.2 | G |
| F51 | AIS death exception | date of death; next interest payment date | Death of the holder | Death is not a transfer; no AIS profit/loss arises on death itself. PR completes a return to date of death; use working sheet if securities transferred after the next interest payment is due | HS343 s.9 | G |
| F52 | AIS foreign currency conversion | settlement date; spot rate | Transfer settled in foreign currency | Translate at the spot rate for the day the sale/purchase was settled | HS343 s.7.1 | G |
| F53 | Qualifying care relief — qualifying amount | days in year; number and ages of cared-for persons | Carer using qualifying care relief | Fixed amount £19,690 per household per full year, **plus** £415/week per child under 11, £495/week per child 11+, £495/week per adult | HS236 s.2 | G |
| F54 | Method selection (carers) | total receipts; qualifying amount; expenses/capital allowances | Receipts < qualifying amount | Claim relief on SA103S | HS236 s.3.1 | G |
| F55 | Method selection (carers) | as F54 | Receipts > qualifying amount, simplified method chosen | Taxed on receipts less qualifying amount; report on SA103S | HS236 s.3.2, s.3.4 | G |
| F56 | Method selection (carers) | as F54 | Profit method chosen | Taxed on receipts less expenses and capital allowances; use SA103F; qualifying care relief forgone | HS236 s.3.2, s.3.3 | G |
| F57 | Carer apportionment | accounting date | Accounting date not on or between 31 March and 5 April | Apportion receipts to compute total receipts for the tax year | HS236 s.4 | G |
| F58 | Joint policy apportionment | number of beneficial owners | Policy jointly owned | Each owner reports their own share (equal by default; half where jointly owned with spouse/civil partner) | HS320 s.9.1; HS321 s.9.1 | G |
| F59 | Time apportioned reduction | foreign days in material interest period (A); total days (B); certificate gain; certificate "number of years" | Individual (not trustee/PR) non-UK resident for part of the material interest period | Reduce gain by A/B; also subtract whole non-UK resident years from the "number of years" | HS320 s.9.3; HS321 s.9.2 | G |
| F60 | RRQP gain reduction | certificate gain; total allowable premiums; total premiums | Policy is a Restricted Relief Qualifying Policy (typically issued before 21 March 2012 and varied after, breaching £3,600 annual premium limit) | Report Gain × (allowable premiums / total premiums), not the certificate figure | HS320 s.9.2 | G |
| F61 | Relief ordering (life policy gains) | applicable reliefs | More than one relief applies | Order: RRQP reduction → time apportioned reduction → top slicing relief | HS320, caveats; HS321, caveats | G |
| F62 | TSR entry rule | full gain | Claiming top slicing relief | Enter the **full** gain on the return (not reduced); HMRC calculates the TSR | HS320 s.10.1, caveats | G |
| F63 | TSR eligibility exclusion | taxpayer type | Trustees; personal representatives | Not entitled to time apportioned reduction or top slicing relief; deficiency relief available only to individuals | HS320 s.10.1, s.10.3; HS321, caveats | G |
| F64 | Final insurance year extension | insurance year start/end; tax year | Final insurance year would begin and end within the same tax year | Extended to include the previous insurance year | HS320 s.7; HS321 s.7 | G |
| F65 | Part + full surrender in same insurance year | events in the insurance year | Both a part surrender and a full surrender occur | Report only the gain on the full surrender | HS320, caveats; HS321, caveats | G |
| F66 | Multiple certificates | certificate issue dates | More than one certificate for the same gain | Use the later (revised) certificate's figures | HS320, caveats | G |
| F67 | Gain calculation | Total Benefits (TB); Total Deductions (TD); Previous Gains (PG) | Maturity/full surrender, death, or sale | Gain = TB − (TD + PG). Examples: £10,000−£4,000=£6,000; £8,000−£4,000=£4,000; £10,000−£5,000=£5,000 | HS320 s.12.1, s.15.1-15.3 | G |
| F68 | Part surrender allowance | premiums paid; years elapsed | Part surrender | 5% of premiums per year tax-deferred, max 100% over 20 consecutive years | HS320 s.13 | G |
| F69 | PPB gain | A = premiums to date; B = cumulative prior PPB gains; C = cumulative prior part-surrender gains | Personal Portfolio Bond, not the final insurance year | PPB gain = 15% × (A + B − C); no PPB gain in the final insurance year | HS320 s.14 | G |
| F70 | Spouse transfer (policies) | relationship; cohabitation | Transfer between spouses/civil partners living together | No gain arises; other connected persons use market value | HS320, caveats | G |
| F71 | Pension input amount (DB) | annual pension; separate lump sum | Defined benefits arrangement | Opening value = (annual pension × 16) + lump sum, increased by 3.1%; closing value = (annual pension × 16) + lump sum with no uplift; pension input = closing − opening (nil if negative) | HS345 "opening/closing value" | G |
| F72 | Pension input amount (cash balance) | pot value at start/end | Cash balance arrangement | Opening = pot value immediately before start of year × 1.031; closing = pot value at year end | HS345 | G |
| F73 | Pension input amount (DC) | gross contributions in year | Money purchase | Total gross contributions (incl. tax relief) by individual, employer or third party; exclude post-75 contributions by the individual/non-employer and investment returns | HS345 | G |
| F74 | Hybrid arrangement | amounts under each relevant method | Hybrid | Pension input = greatest of the amounts under each relevant method | HS345 | G |
| F75 | Tapered annual allowance | threshold income; adjusted income | 2025-26: threshold income > £260,000 **and** adjusted income > £260,000 | AA = £60,000 − £1 for every £2 of adjusted income above £260,000, floored at £10,000. Worked example: adjusted income £365,000 → formula gives £7,500 → floor applies | HS345 "Tapered annual allowance" | G |
| F76 | Money purchase annual allowance | flexi-access status; money purchase inputs | Flexi-accessed a money purchase arrangement | MPAA = £10,000 (2025-26); alternative AA = tapered/default AA − £10,000; carry-forward cannot be added to the £10,000 MPAA | HS345 "High income and flexi-accessed" | G |
| F77 | AA carry-forward | membership in each of previous 3 tax years; unused AA | Member of a registered pension scheme during each carry-forward year | Unused AA from previous 3 years may be added to tapered/default or alternative AA; no return disclosure or claim needed if no charge arises | HS345 | G |
| F78 | AA excess reporting | pension input; applicable AA | Total pension input exceeds default/tapered AA | Enter excess in box 10 (or, under the 7-step test for high-income + flexi-access, the greater of excess amount 1 and excess amount 2) | HS345 Step 3, Step 7 | G |
| F79 | Overseas scheme adjustment | pension input amount; EI; TE; TSI | DB/cash balance arrangement in an overseas pension scheme | Adjusted pension input = pension input × (TE + TSI) / EI | HS345 "Defined benefits and cash balance arrangements in overseas pension schemes" | G |
| F80 | Overseas transfer charge | transferred value; exemption conditions; transfer request date | Transfer requested on/after 9 March 2017 to a QROPS that meets none of the 5 conditions, or required information not given | Charge = 25% of the transferred value; individual and scheme administrator/manager jointly liable; report transferred value in box 11.1, tax paid in box 11.2, PSTR in box 12 | HS345 "Overseas transfer charge" | G |
| F81 | Overseas transfer charge — retrospective trigger | residence changes; date of original transfer | Change of country of residence within 5 full tax years after transfer removing residence-based exemption | Charge becomes due | HS345 | G |
| F82 | Unauthorised payments charge | payment amount (gross, pre-deduction) | Payment is an unauthorised payment | 40% charge; enter in box 13 if not subject to surcharge, box 14 if subject | HS345 "Unauthorised payments" | G |
| F83 | Unauthorised payments surcharge | cumulative unauthorised payments; value of rights under the scheme; surcharge period | Payments within the surcharge period reach 25% of the value of the member's rights (or of UK tax-relieved/transferred funds for overseas schemes) | Additional 15% surcharge. Surcharge period runs from the first unauthorised payment and ends 12 months later or when the threshold is reached, if earlier | HS345 "Unauthorised payments surcharge" | G |
| F84 | Short service refund charge | refund amount (sterling, spot rate at payment date) | Refund of UK tax-relieved contributions from an overseas scheme, 2025-26 | 20% on first £20,000; 50% on the excess. Enter in box 16 | HS345 Box 16 | G |
| F85 | Foreign tax conversion (pension charges) | foreign tax paid; payment date spot rate | Foreign tax paid on box 13/14 payment, or on box 16 refund | Enter sterling equivalent in box 15 (or box 18 for box 16); sum multiple payments | HS345 Boxes 15, 18 | G |
| F86 | Temporary non-residence (drawdown) | departure year; years of sole UK residence in the 7 preceding years; length of non-residence | Sole UK resident for any part of ≥4 of the 7 tax years before departure **and** not solely resident for a period of <5 full tax years | Drawdown taken during non-residence taxed as arising in the year UK residence resumes | HS345 "Temporary non-residence" | G |
| F87 | TRF designation and charge | qualifying overseas capital designated; tax year | Designation made on SA109 boxes 50, 51, 52, 54 in sterling | Charge = 12% (2025-26 and 2026-27), 15% (2027-28); treated as taking place at the start of the tax year; no foreign tax credit against the charge | HS264 s.4, s.4.3.2-4.3.3; HS305 (12% for 2025-26) | G |
| F88 | TRF window | tax year | 2025-26, 2026-27, 2027-28 only | TRF designation available; partial designation permitted; designated capital excluded from total taxable income/gains, ANI and pension net/threshold/adjusted income; no effect on next year's payments on account | HS264 s.4, s.4.3, caveats | G |
| F89 | TRF priority rule | mixed fund composition | Designated capital exists | TRF capital is remitted in priority to other amounts in a mixed fund, regardless of the year in which they arose | HS264 s.4 | G |
| F90 | Remittance basis FTCR apportionment | foreign tax paid; proportion of income remitted | Only part of the income remitted | Claim credit only for the proportionate share of foreign tax. Example: £10,000 rents, £2,000 foreign tax, £7,500 in column B, £1,500 in column C | HS264 s.3.1, Example 7 | G |
| F91 | Remittance currency conversion | remittance date; exchange rate (or bank's rate if credited to a sterling account) | Foreign-currency remittance | Convert at the rate on the date of remittance; enter all amounts in sterling on pages F2/F3 | HS264 s.3 | G |
| F92 | SWT set-off deemed remittance | tax year of set-off | SWT set off or repaid to a former remittance basis user | Treated as a remittance; set-off normally regarded as occurring at 31 January following the tax year | HS264 s.2.2 | G |
| F93 | Remitted foreign dividends | dividend payment date | Dividends paid on/after 6 April 2016 | No dividend tax credit on remittance; dividend allowance and dividend nil rate do not apply; taxed at 20%/40%/45% rather than 8.75%/33.75%/39.35% | HS264 "Boxes 7.3, 7.4 and 7.5" | G |
| F94 | Employment-related securities charge | UMV; IUP; PCP; OP; CE | Chargeable event on employment-related securities | Taxable amount = UMV × (IUP − PCP − OP) − CE | HS305 "How to calculate the Income Tax" | G |
| F95 | EMI disqualifying event window | exercise date; disqualifying event date; share value movement | Exercise more than 90 days (40 days before 17 July 2013) after a disqualifying event and shares have risen in value | Additional tax may be due; complete working sheet 5 (and WS4 if discounted: box 15 WS4 + box 12 WS5 → box 1, page Ai 2) | HS305 EMI section | G |
| F96 | Notional loan de minimis | total notional and actual employment-related loans at any time in the year | Total ≤ £10,000 | No benefit arises from an interest-free loan; working sheet 8 not required | HS305 Working sheet 8 guidance | G |
| F97 | Artificially depressed market value | percentage reduction at acquisition; forfeiture risk period; election status | Market value reduced by ≥10% by non-commercial actions | Charge applies (working sheet 11), **unless** shares are subject to a forfeiture risk of ≤5 years and no election was made to pay tax at acquisition | HS305 "Securities with artificially depressed market value" | G |
| F98 | Artificially enhanced market value | percentage enhancement; relevant date | Enhancement > 10% | Charge applies; relevant date = 5 April 2026 or date of disposal, if earlier | HS305 "Securities with an artificially enhanced market value" | G |
| F99 | Artificial reduction look-back | date of receipt; reduction date | Artificial reduction within the 7 years ending on receipt | Complete the working sheet ignoring the artificial reduction | HS305 "Consideration or benefits received" | G |
| F100 | Restricted securities relevant date | disposal/chargeable event date | Restricted securities acquired on/after 16 April 2003 | Relevant date = 5 April 2026 or date of the chargeable event, if earlier; no further IT if an election was made to pay tax at acquisition as if unrestricted | HS305 "Restricted securities" | G |

### 2.3 Record keeping

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| F101 | General record-keeping duty | return/claim obligation | Person liable to make a return or claim (even if not made every year) | Keep records to make a correct and complete return or claim | TMA 1970 s.12B; CH10100; CH11200 | S/M |
| F102 | Trade record content | trade/profession/business status ("trade" includes letting of property) | Carrying on a trade | Keep records of all receipts and expenses, matters relating to them, and all sales/purchases of goods where dealing in goods | TMA 1970 s.12B; CH11300 | S/M |
| F103 | Retention — business (tax-year return) | year of assessment; enquiry status; filing timeliness | Trade/profession/business, tax-year return | Retain until the **latest** of: (a) 5th anniversary of the 31 January next following the year of assessment; (b) completion of any enquiry; (c) close of the enquiry window | TMA 1970 s.12B; CH14530 | S/M |
| F104 | Retention — business (non-tax-year period) | period end date | Return for a period that is not a tax year | Retain until the 6th anniversary of the end of the period (subject to (b) and (c) above) | CH14530 | M |
| F105 | Retention — non-business | year of assessment; enquiry status | Person not carrying on a trade, profession or business | Retain until the latest of: 1st anniversary of the 31 January next following the year of assessment; completion of any enquiry; end of the day the enquiry window closes | TMA 1970 s.12B; CH14550 | S/M |
| F106 | Enquiry window close (record-retention purposes) | return filing date; timeliness | On-time return | 12 months after the date the return was filed | CH14530; CH14550 | M |
| F107 | Enquiry window close (record-retention purposes) | return filing date; timeliness | Late return | First anniversary of the next quarter day falling after the return was filed | CH14530; CH14550 | M |
| F108 | Retention — claims not in a return | claim date; relevant tax year/period; enquiry status | Direct tax claim outside a return | Later of completion of enquiry into the claim, or the day after the enquiry window closes (window closes at the first anniversary of the quarter day following the claim, or of the 31 January following the relevant tax year, or of the end of the relevant period) | TMA 1970 Sch 1A para 2A; CH14900 | S/M |
| F109 | Late notice to file after retention date | notice date; existing records | Notice to make a return given after the normal retention date has passed | Keep any records still held until the later of enquiry completion or enquiry window closure | CH14530; CH14550 | M |
| F110 | Multiple-purpose records | retention periods for each purpose | Same record required for more than one tax purpose | The longer retention period applies | CH14100 | M |
| F111 | Shorter retention periods | HMRC written direction; record type; avoidance suspicion | HMRC may specify shorter periods in writing | Never permitted where avoidance is suspected, nor for PAYE/CIS records. HMRC states no shorter periods have been specified so far | CH14100, caveats | M |
| F112 | Record-keeping penalty | failure to keep/retain | Failure to keep or retain required records | HMRC can charge a penalty | CH11200; CH14550; EM4650; SACM4020 | M |

---

## 3. Payment

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| P1 | Payments on account | previous year's liability | Within ITSA | Two equal payments on account, based on the previous year's liability, due 31 January (in-year) and 31 July (following) | TMA 1970 s.59A; CH142240; CH142260; CH146060 | S/M |
| P2 | Balancing payment | year's liability; payments on account; tax deducted at source | Liability exceeds POAs + tax deducted at source | Balancing payment = difference, due 31 January following the end of the tax year | TMA 1970 s.59B; CH142240; CH143260; CH155010 | S/M |
| P3 | Late-issued notice | date of s.8 notice | s.8 notice issued after 31 October following the year of assessment | Payment due 3 months from the date of the notice; due date for the balancing payment can therefore be later than 31 January | TMA 1970 s.8; CH140220; CH155010 | S/M |
| P4 | Late payment interest — start | due and payable date | Amount unpaid after due date | Interest runs from the date the amount becomes due and payable, even if a non-business day | FA 2009 s.101; CH140190 | S/M |
| P5 | Late payment interest — end | payment or set-off date | Payment made | Interest ends on the date payment is made or set-off takes place | FA 2009 s.101(9); CH140200 | S/M |
| P6 | Simple, not compound | interest already charged/accrued | Always | No interest on interest, in either direction | FA 2009 s.101(8), s.102(7); CH140260 | S/M |
| P7 | Per-instalment interest | each POA; balancing payment; respective due dates | Any unpaid | Interest computed separately on each POA and on the balancing payment | TMA 1970 s.59A; CH140290 | S/M |
| P8 | Interest during Time to Pay | reducing balance; instalment schedule | Instalment or TTP arrangement in place | Late payment interest continues to run on the reducing balance | CH140280 | M |
| P9 | Excessive claim to reduce POAs | reduced POAs; balancing payment; POA that would have been due | Claim to reduce proves excessive | Interest charged on the **lesser** of (a) each reduced POA + 50% of the balancing payment, and (b) the POA that would have been payable absent the claim; interest runs from the original POA due dates | FA 2009 Sch 53 para 1; CH142240; CH142260 | S/M |
| P10 | Overpaid POA interaction | each late-paid POA; overpayment for the year | Overpayment arises alongside late-paid POAs | Interest charged on the amount by which each late-paid POA exceeds 50% of the overpayment | FA 2009 Sch 53 para 2; CH142300 | S/M |
| P11 | Interest on amended/assessed tax | date tax would have been due had the original return been correct | Correction, amendment, or HMRC assessment in place of a self-assessment | Interest start = the original due date, not the date of the amendment/assessment | FA 2009 Sch 53 para 3; CH143020; CH143260 | S/M |
| P12 | Interest after withdrawal of notice to file | original due date | Notice to file withdrawn, then chargeability discovered under s.7(1B) | Interest runs from the date payment would have been due had the notice not been withdrawn | CH143020; Example 3 (CH143xxx) | M |
| P13 | Interest on postponed tax | postponed amount; original due date; appeal outcome | Appeal outcome requires payment of postponed tax | Interest runs from the date that would have applied absent the appeal; interest is payable on postponed tax paid late | TMA 1970 s.55; FA 2009 Sch 53 para 4; ARTG2560; CH143280 | S/M |
| P14 | Interest on over-repayments | over-repaid amount; relevant tax year | Assessment under TMA 1970 s.30 to recover over-repayment | Interest runs from 31 January following the tax year in respect of which the assessment is made | TMA 1970 s.30; FA 2009 Sch 53 para 5; CH143320 | S/M |
| P15 | Death and probate | date of grant of probate/letters of administration/confirmation; normal start date | Person dies before the charge becomes due and executors lack access to funds | Interest start = later of the normal start date and the day after 30 days from grant | FA 2009 Sch 53 para 12; CH143360; CH143380 | S/M |
| P16 | Breathing Space | moratorium start/end dates | Eligible individual in a Debt Respite Scheme moratorium (from 4 May 2021) | Interest, fees and charges frozen; late payment interest calculated to exclude amounts accrued during the period | CH140320; SI 2020/1311 | M |
| P17 | Repayment interest start (Rule 1) | date paid to HMRC; date due and payable | Amount was paid to HMRC | Start = **later** of the two dates (so early payment does not increase repayment interest) | FA 2009 s.102; Sch 54 para 2-4; CH146020; CH146040; CH146060 | S/M |
| P18 | Repayment interest end | repayment/set-off date | — | Date the amount is repaid, paid to another person, or set off | FA 2009 s.102; CH146020 | S/M |
| P19 | Repayment interest — tax deducted at source | year to which the income tax relates | Income tax deducted at source (PAYE, net annuities, net royalties); includes ITTOIA 2005 s.397(1)/397A(2) tax credits; excludes PAYE amounts deducted in respect of previous years | Start = 31 January of the year following the year to which the tax relates | FA 2009 Sch 54 para 6; CH146240 | S/M |
| P20 | Repayment interest — carry-back / averaging | "later year" of the claim | Claim to carry back losses (TMA 1970 Sch 1B para 2) or average farmers' profits (ITTOIA 2005 Pt 2 Ch 16) | Start = 31 January following the "later year" | FA 2009 Sch 54 para 7; CH146280 | S/M |
| P21 | Overpayment allocation order | balancing payment; POAs; tax deducted at source | Computing repayment interest start dates | Allocate the overpayment first to the balancing payment, then in two equal parts to the POAs, then to tax deducted at source; where POAs were paid in instalments, allocate to later instalments before earlier ones | FA 2009 Sch 54 para 13; CH146120 | S/M |
| P22 | No repayment interest where court interest applies | court/tribunal order terms | Amount payable as a result of an order or judgment already carrying interest (e.g. a successful FTT appeal) | No repayment interest | FA 2009 s.102(6); CH146xxx | S |
| P23 | Contract settlement | settlement terms | Contract settlement agreed | Statutory FA 2009 interest ceases to apply; contractual interest terms apply instead | CH140310 | M |
| P24 | No discretion / no appeal on interest | — | Interest charged | Liability to interest is automatic; no HMRC discretion to waive; no statutory right of appeal against interest itself (an appeal against the underlying tax flows through automatically) | CH140260; CH140295; CH140300 | M |
| P25 | Deferral request | due date; request date | Request made **before** the due date and agreed | Penalties suspended for the deferral period | FA 2009 Sch 56 para 10; CH156600 | S/M |
| P26 | Broken deferral | deferral conditions; breach | Deferred amount unpaid, scheduled payments missed, or conditions breached | Person liable to penalties calculated as if the deferral did not exist, from the date of HMRC's notice | FA 2009 Sch 56 para 10; CH156600 | S/M |

---

## 4. Enquiry, closure and information powers

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| E1 | Enquiry notice | return type | Individual/trustee IT/CGT return | Enquiry opened by notice under TMA 1970 s.9A | TMA 1970 s.9A; CH23540; CH279600 | S |
| E2 | Enquiry notice (partnership) | return type | Partnership return | Notice under TMA 1970 s.12AC | TMA 1970 s.12AC; CH23540; CH279600 | S |
| E3 | Enquiry notice (claims not in a return) | claim | Standalone claim | Notice under TMA 1970 Sch 1A para 5 | TMA 1970 Sch 1A para 5; CH23540 | S |
| E4 | "Open enquiry" test | notice date; closure notice status | Notice of enquiry issued and no closure notice yet issued for the matters in question | Enquiry is open; if a partial closure notice has been issued, requests are restricted to matters not closed by it | CH23540 | M |
| E5 | Closure notice | matters concluded | All matters complete | Final closure notice under TMA 1970 s.28A (or s.28C, or Sch 1A para 57) unless settled by contract | TMA 1970 s.28A/s.28C; CH23540; CH279600 | S/M |
| E6 | Partial closure notice | individual "matters" complete | One or more matters complete before the whole check | PCN may be issued (introduced by F(No.2)A 2017); requires approval of an independent officer (form PCN101) unless tribunal-directed; same appeal rights as an FCN, 30-day limit | CH279600; CH279610 | M |
| E7 | Taxpayer application for closure | disagreement over completing a matter | Customer wants a PCN, HMRC disagrees | Customer may apply to the tribunal for a direction requiring issue of a PCN | CH279600; EM2163 | M |
| E8 | Information notice restriction where SA return made | chargeable period; return status; enquiry status; discovery grounds | An SA return has been made for the chargeable period | A taxpayer notice checking the IT/CGT position may be issued only if there is an open enquiry, a potential discovery assessment position, or the notice is needed for another tax or for checking reductions/repayments | FA 2008 Sch 36 para 21; CH23540 | S/M |
| E9 | "Reason to suspect" | facts known to the officer | Facts lead the officer to think tax may have been under-assessed/underpaid or excessive relief claimed | Threshold met — lower than being able to make an assessment, but does not permit speculative or fishing enquiries | FA 2008 Sch 36 para 21(6); CH23560 | S/M |
| E10 | Discovery position | reason to suspect; correctability | Reason to suspect under-assessment/excess relief **and** the tax position could be corrected if true | Potential discovery assessment position exists | TMA 1970 s.29(4)-(5); CH23540 | S/M |
| E11 | Service of an information notice | notice; recipient details; consent flags | Written notice | Serve by delivering to the person or leaving it at their usual or last known place of residence; email only with the customer's explicit informed consent specific to that notice | CH23440 | M |
| E12 | Compliance with notice | period, time, means and form specified | Notice received | Comply within the period specified, and at the time, by the means and in the form specified if stated | FA 2008 Sch 36 para 7; CH23480 | S/M |
| E13 | Defective notice | nature of the error; identification of the person | Formal defect only | Notice not automatically void if it meets the intention and meaning of the law and the affected person is adequately identified; substantial errors may require a fresh notice | CH23440, caveats | M |
| E14 | Joint referral during enquiry | question in dispute | SA enquiry in progress | Joint application to the tribunal to determine a question | TMA 1970 s.28ZA(1); ARTG2040 | S |
| E15 | Pre-population check box | presence of pre-populated data | Online SA return with pre-populated data | Customer must tick "I have viewed the information HMRC holds about me" before starting to file | CH206225 | M |

---

## 5. Assessment, determination and time limits

### 5.1 Determinations and assessments

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| A1 | HMRC determination | statutory filing date | Return required but not filed | Determination may be made within 3 years beginning with the statutory filing date. Example: 2012-13 filing date → determination deadline 30 January 2017 | TMA 1970 s.28C(5); CH52100; CH56100 | S/M |
| A2 | Self-assessment displacing a determination | filing date; determination date | Person files to displace the determination | Later of 3 years from the filing date and 12 months from the date of the determination | TMA 1970 s.28C(5) (as amended by FA 2008 Sch 39 para 2); CH56100 | S/M |
| A3 | Routine self-assessment | year of assessment | No determination made | 4 years from the end of the year of assessment | TMA 1970 s.34A; CH56100 | S/M |
| A4 | Simple assessment | year of assessment | Simple assessment made | 4 years from the end of the year of assessment | TMA 1970 s.28; CH56100 | S/M |
| A5 | Determinations based on third-party data | overdue duration; third-party information; prior-year liability | Direct tax return more than 12 months overdue and third-party information indicates liability significantly above the normal pattern | HMRC may make a determination estimated from the previous year's liability (excluding capital gains); wait at least 30 days before contacting the person | CH401225 | M |

### 5.2 Assessment time limits (IT/CGT)

| # | Behaviour / circumstance | Time limit | Ref | Type |
|---|---|---|---|---|
| A6 | No careless or deliberate behaviour (discovery assessment; partnership statement amendment) | 4 years from the end of the year of assessment | TMA 1970 s.34; CH52100; CH56100 | S/M |
| A7 | Loss of tax brought about carelessly by the person or their agent | 6 years from the end of the year of assessment | TMA 1970 s.36(1), (1B); CH53400; CH56100 | S/M |
| A8 | Offshore matter or offshore transfer | 12 years from the end of the year of assessment, except where a longer limit applies | TMA 1970 s.36A(2) (inserted by FA 2019 s.80-81); CH53100; CH53505 | S/M |
| A9 | Loss of tax brought about deliberately | 20 years from the end of the year of assessment | TMA 1970 s.36(1A), (1B); CH53600; CH56100 | S/M |
| A10 | Failure to provide information about an avoidance scheme | 20 years, **or** 4 years where a qualifying reasonable excuse exists | TMA 1970 s.118(2), s.36(1A)(c); CH54000; CH56100 | S/M |
| A11 | Failure to notify liability | 20 years, **or** 4 years where a qualifying reasonable excuse exists (for 2008-09 and earlier, the 20-year limit also required negligent conduct) | TMA 1970 s.118(2), s.34, s.36(1A)(b); CH53900; CH56100 | S/M |
| A12 | Withdrawal/reduction of EIS relief | Later of 6 years from the end of the year of assessment in which the use-of-money requirement falls, or the event causing withdrawal occurs; 20 years if deliberate | ITA 2007 s.237; CH52100; CH56100 | S/M |
| A13 | Withdrawal/reduction of CITR relief (IT) | 6 years from the end of the year of assessment for which relief was obtained; 20 years if deliberate | ITA 2007 s.372; CH56100 | S/M |
| A14 | Recovery of over-repayment — no careless/deliberate behaviour | Latest of: 4 years from the end of the year of assessment; the end of the year of assessment next following that in which the excessive repayment was made; closure of enquiry by final closure notice | TMA 1970 s.30(5), s.34; CH56100 | S/M |
| A15 | Recovery of over-repayment — careless / deliberate | As A14 but 6 years / 20 years respectively | TMA 1970 s.30(5), s.36; CH56100 | S/M |
| A16 | Employment/pension/social security income received late | Later of 4 years from the end of the year for which assessable and 4 years from the end of the year in which received (6 / 20 years for careless / deliberate) | TMA 1970 s.35, s.36; CH56100 | S/M |
| A17 | Assessment on a deceased person (PRs) — normal | Within 4 years of the end of the year of assessment in which the person died | CH54200; CH56100 | M |
| A18 | Assessment on a deceased person (PRs) — careless/deliberate/failure to notify | May only assess a year of assessment ending not earlier than 6 years before the date of death, and the assessment must be made within 4 years of death | CH54200 | M |
| A19 | Assessment after death (statutory) | No assessment for a year of assessment ending more than 6 years before the date of death | TMA 1970 s.40(2); CH56100 | S |

### 5.3 Offshore time-limit qualifiers

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| A20 | 12-year limit applicability by year | tax year; behaviour | 2013-14 and 2014-15: only if the loss resulted from carelessness. 2015-16 onwards: applies even with reasonable care | 12-year limit engaged or not | CH53560; CH53100 | M |
| A21 | Offshore transfer test | whether lost tax involves an offshore matter; transfer destination; relevant date | Lost tax does **not** involve an offshore matter, and income/proceeds (or derived assets) transferred outside the UK before the relevant date | Treated as an offshore transfer for the 12-year limit, but only where HMRC shows the transfer made the lost tax significantly harder to identify | TMA 1970 s.36A(6)-(8); CH53540 | S/M |
| A22 | Relevant date (IT/CGT) | return delivery date; tax year | Return delivered | Relevant date = date the return was delivered; if no return delivered, 31 January following the end of the year to which the loss relates | CH "Income tax and capital gains tax" | M |
| A23 | Relevant overseas information exclusion | information received from an overseas authority under an EU tax provision or UK agreement; normal time limit expiry | The information reasonably enabled HMRC to assess the lost tax before normal limits expired | 12-year limit disapplied | CH53550 | M |
| A24 | Deliberate override | behaviour | Deliberate behaviour involving an offshore matter | 20-year limit applies instead of 12 | CH53505; CH53560 | M |
| A25 | Requirement to Correct | offshore non-compliance for 2015-16 or earlier; correction date | Not corrected by 30 September 2018 | Failure to Correct penalties due; assessment limit extended to the later of the normal date and 5 April 2021 (pre-2013-14 years assessable as at 6 April 2017) | F(No.2)A 2017 s.67, Sch 18; CH123200 | S/M |
| A26 | RTC safe harbours | disclosure route; dates | WDF: 90 days from notification of intention to disclose; CDF: 60 days from HMRC acceptance of CDF1; open enquiry: inform officer by 30 Sept 2018 and outline disclosure by 29 November | No FTC penalty, if the person complies fully | CH123260 | M |

### 5.4 Transitional and administrative

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| A27 | 6→4 year reduction | assessment date | Assessments made on or after 1 April 2010 | Normal direct-tax assessment limit reduces from 6 to 4 years, regardless of the period assessed | SI 2009 No 403 art 2(2); CH51540 | S/M |
| A28 | Extended-limit assessment authorisation | ETL assessment proposal | Making an extended time-limit assessment | Requires prior authorisation from the appropriate Authorising Officer | CH53300; CH282070; EM3257 | M |
| A29 | Burden of proof | behaviour alleged | Reliance on an extended time limit | HMRC bears the onus of proving careless or deliberate behaviour, on the balance of probabilities; higher-quality evidence expected for more serious behaviour | CH54300; CH81190; CH160xxx "Level of proof" | M |
| A30 | Consequential claims | assessment/amendment to recover lost tax; claim type | Careless behaviour case | Only consequential **claims** (not elections) permitted out of time under TMA 1970 s.36(3); no consequential claims exist for VAT, IPT, aggregates levy, climate change levy, landfill tax, PRT or excise duty | TMA 1970 s.36(3), s.43A-43C; CH55100; CH55200 | S/M |

---

## 6. Penalties

### 6.1 Late filing — FA 2009 Sch 55, model 1 (ITSA and CGT)

| # | Trigger | Amount | Ref | Type |
|---|---|---|---|---|
| PN1 | Return not filed by the filing date | £100 initial fixed penalty, arising on the penalty date | FA 2009 Sch 55 para 3; CH62100; CH63540 | S/M |
| PN2 | Still outstanding 3 months after the penalty date, and HMRC has given written notice specifying a start date at least 3 months after the penalty date | £10 per day, for the lesser of the days elapsed and 90 days | FA 2009 Sch 55 para 4; CH62120 | S/M |
| PN3 | Still outstanding 6 months after the penalty date | Greater of 5% of the liability that would have been shown, and £300. Not reducible for disclosure; behaviour-independent | FA 2009 Sch 55 para 5; CH62140; CH63580; CH63120 | S/M |
| PN4 | Still outstanding 12 months, information **not** deliberately withheld | Greater of 5% of the liability, and £300. Not reducible for disclosure | FA 2009 Sch 55 para 17; CH62200; CH63600 | S/M |
| PN5 | Still outstanding 12 months, deliberate but not concealed | Greater of 70% of the liability, and £300. Reducible for disclosure | FA 2009 Sch 55 para 11; CH62160+; CH63600 | S/M |
| PN6 | Still outstanding 12 months, deliberate and concealed | Greater of 100% of the liability, and £300. Reducible for disclosure | FA 2009 Sch 55 para 6; CH62160+; CH63600 | S/M |

**Supporting rules**

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| PN7 | Liability base | gross liability; tax deducted at source; amounts already paid | Computing a tax-geared penalty | "Liability that would have been shown" = net liability after tax deducted at source; **not** reduced by amounts already paid; disregard deferred relief under CTA 2010 s.458(3)/(4) | CH63560 | M |
| PN8 | Estimation before filing | prior-year liability; VAT returns; industry knowledge | Return still outstanding and true liability unknown | Estimate to the best of information and belief; amend the penalty once the return is filed and the actual liability is known | CH63560; CH64250; FA 2009 Sch 55 para 24 | S/M |
| PN9 | Percentage ratchet | original penalty percentage; later evidence | Penalty already assessed | The percentage set in the original tax-geared assessment cannot be reduced later, only increased if more serious behaviour is evidenced | CH64250 | M |
| PN10 | Multiple behaviours | behaviours evidenced | More than one behaviour demonstrated at 12 months | Use the highest applicable percentage | CH62200; CH63500+ | M |
| PN11 | Independence of penalties | prior penalties charged | Liability to a further or daily penalty arises | The person becomes liable even if some or all previous penalties were not charged | CH63020 "All penalties" | M |
| PN12 | Reasonable excuse defence | excuse existence at the date of the obligation; remedy timing | Reasonable excuse existed and the failure was remedied without unreasonable delay after the excuse ended | No penalty | FA 2008 Sch 41 para 20 (notify); CH160100; CH61500 | S/M |
| PN13 | Cap on combined tax-geared filing penalties | 6-month and 12-month tax-geared penalties; category | Combined total exceeds 100% of the tax liability | Reduce so the total does not exceed 100%. Adjustment triggered in NPPS where the 12-month penalty (after deducting the automatic 5%) exceeds 95% of the liability | FA 2009 Sch 55 para 17; CH403322; CH404475; CH65040 | S/M |
| PN14 | Offshore uplift to the cap | information category | Category 2 or 3 offshore matter, tax at stake IT or CGT | 100% cap raised to 150% (Cat 2) / 200% (Cat 3); category 1 remains 100% | CH65040; CH404200; CH112600 | M |
| PN15 | Deduction of the automatic 12-month penalty | automatic 5% penalty already assessed; new higher penalty | Higher deliberate-withholding penalty charged after an automatic 5% penalty | Deduct the amount already assessed. Worked example: 100% of liability less the £1,000 automatic penalty = £19,000 | CH403321; CH404475 | M |
| PN16 | Contract-settlement deduction | automatically assessed amount vs NPPS-calculated amount | Settling by contract | Deduct only the amount actually assessed by SA or CIS | CH403321 | M |
| PN17 | Assessment-letter timing | date of amendment/discovery assessment/determination | Issuing an NPPS2 penalty assessment letter | Wait 10 days; the PAL must be dated later than the automatic penalty assessment | CH403321 | M |
| PN18 | Double jeopardy | criminal conviction for the same failure | Person convicted of a criminal offence in respect of the failure to file | No filing penalty may be charged | FA 2009 Sch 55 para 26; CH65100 | S/M |
| PN19 | Partnership returns (IT/CGT) | relevant partners (anyone who was a partner at any time in the return period) | Partnership IT/CGT return filed late | Each relevant partner is separately liable to: £100 initial; £10/day for up to 90 days from 3 months after the penalty date; £300 at 6 months; £300 at 12 months. No tax-geared penalty is possible because the partnership has no IT/CGT liability | FA 2009 Sch 55 para 25; CH62940; CH62920 | S/M |
| PN20 | Partnership appeal | representative partner identity | Penalty on relevant partners | Only the representative partner (or successor) may appeal; the appeal covers all partners' penalties | FA 2009 Sch 55 paras 20, 25; CH64540; CH62940 | S/M |

### 6.2 Late filing — offshore penalty percentages (12-month further penalty)

Territory categories: category 1 = automatic exchange with the UK (the UK itself is category 1); category 3 = no exchange; anything not listed in 1 or 3 is category 2 (Crown Dependencies and UK Overseas Territories default to category 2 unless listed). Category is fixed as at the date of the failure, not the current date, because Treasury Orders move territories between categories. Two different category tables apply depending on whether the filing date was before, or on/after, 24 July 2013.

| Behaviour | Cat 1 | Cat 2 | Cat 3 | Ref |
|---|---|---|---|---|
| Deliberate and concealed | 100% | 150% | 200% | CH112600; CH403145 |
| Deliberate but not concealed | 70% | 105% | 140% | CH112600 |
| Any other case | 5% | 5% | 5% | CH112600 |

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| PN21 | Multi-category apportionment | withheld information by category; tax liability | Information falls into more than one category | Treat as separate failures, one per category, and apportion the tax liability on a just and reasonable basis; calculate each penalty separately | CH112500; CH112800; CH114100 | M |
| PN22 | Offshore scope | tax at stake | Offshore percentage ranges apply only to income tax, CGT, bank payroll tax and registered pension schemes | Standard rates for other taxes; higher 12-month penalties do not apply to CIS returns | CH112700, caveats; CH62240, caveats | M |

Disclosure ranges for offshore matters (12-month further penalty) — note the split by period:

| Category / behaviour | Up to and incl. 2015-16 | 2016-17 onwards | Ref |
|---|---|---|---|
| Cat 1 deliberate, unprompted | 20%–70% | 30%–70% | CH112700 |
| Cat 1 deliberate, prompted | 35%–70% | 45%–70% | CH112700 |
| Cat 1 deliberate & concealed, unprompted | 30%–100% | 40%–100% | CH112700 |
| Cat 1 deliberate & concealed, prompted | 50%–100% | 60%–100% | CH112700 |
| Cat 2 deliberate, unprompted | 30%–105% | 40%–105% | CH112700 |
| Cat 2 deliberate, prompted | 52.5%–105% | 62.5%–105% | CH112700 |
| Cat 2 deliberate & concealed, unprompted | 45%–150% | 55%–150% | CH112700 |
| Cat 2 deliberate & concealed, prompted | 75%–150% | 85%–150% | CH112700 |
| Cat 3 deliberate, unprompted | 40%–140% | 50%–140% | CH112700 |
| Cat 3 deliberate, prompted | 70%–140% | 80%–140% | CH112700 |
| Cat 3 deliberate & concealed, unprompted | 60%–200% | 70%–200% | CH112700 |
| Cat 3 deliberate & concealed, prompted | 100%–200% | 110%–200% | CH112700 |

Minimum penalty amount for the 12-month offshore penalty: £300 (CH112700). For CIS returns the 12-month minimums are £3,000 (deliberate and concealed), £1,500 (deliberate not concealed) and £300 (not deliberate) (CH62480; CH63640).

### 6.3 Late payment — FA 2009 Sch 56 (IT and CGT)

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| PN23 | Scope | payment type; due date | Balancing payments due on or after 31 January 2012. **Does not apply to payments on account** | Sch 56 regime engaged | CH155010, caveats | M |
| PN24 | Penalty date | due date | Standard 31 January due date | Penalty date = 31 days after the due date (3 March, or 2 March in a leap year) | CH155010; CH155100 | M |
| PN25 | Initial penalty | amount unpaid at the penalty date | Unpaid | 5% of the amount unpaid | FA 2009 Sch 56 para 3; CH155120 | S/M |
| PN26 | 5-month penalty | amount unpaid 5 months after the penalty date | Still unpaid | Further 5% | CH155140 | M |
| PN27 | 11-month penalty | amount unpaid 11 months after the penalty date | Still unpaid | Further 5% (potential aggregate 15%) | CH155160 | M |
| PN28 | Penalty date — determination/assessment in absence of a return | due date that would have applied on a timely return | Tax due under a determination or assessment made because no return was filed | Penalty date = 31 days after that notional due date | CH155200 | M |
| PN29 | Penalty date — assessment/amendment/correction | due date for the further tax | Further tax arises from an assessment, amendment or correction | Penalty date = 31 days after the due date for the further tax; a Sch 24 inaccuracy penalty may also arise | CH155200 | M |
| PN30 | Penalty notice contents | assessment date; legislation; amount; period | Penalty assessed | Must state the date of assessment, the legislation, the amount, and the period to which it relates | FA 2009 Sch 56 para 11; CH156600 | S/M |
| PN31 | Payment of penalty | assessment issue date | Penalty assessed | Payable within 30 days beginning with the date of issue; enforceable as if it were a tax assessment | FA 2009 Sch 56 para 11(2)-(3); CH156600 | S/M |
| PN32 | Penalty assessment time limit | penalty date; appeal period for the tax assessment | Sch 56 penalty | Later of: 2 years beginning with the day before the penalty date; and 12 months beginning with the end of the appeal period for the tax assessment (or the date liability is established if no assessment) | FA 2009 Sch 56 para 12; CH156600 | S/M |
| PN33 | Partnership liability (Sch 56) | tax type | IT, CGT, corporation tax | The partnership has no penalty liability; liability is shared among the relevant partners. For most other taxes the partnership is treated as a person in its own right | CH156600, caveats | M |
| PN34 | Historic surcharge | tax year | s.59C TMA 1970 surcharges not charged for years after 2009-10 | Replaced by Sch 56 penalties for balancing payments due on or after 31 January 2012; Sch 56 penalties must **not** be withdrawn in the way surcharges were cancelled | TMA 1970 s.59C; CH404300; CH404425 | S/M |

### 6.4 Failure to notify — FA 2008 Sch 41

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| PN35 | Commencement (IT/Class 4 NIC/CGT) | tax year | 2009-10 onwards | Sch 41 applies. Class 2 NIC from 2015-16 only; corporation tax for APs ending on/after 31 March 2010 | CH71120; CH65040 | M |
| PN36 | PLR for IT/CGT | tax unpaid at 31 January following the tax year | Failure to notify IT/CGT chargeability | PLR = amount unpaid at that date. Example: £12,894 − £3,000 = £9,894 | FA 2008 Sch 41 para 7(2); CH72700 | S/M |
| PN37 | PLR where notice to file withdrawn | withdrawal date; 31 January date; refund of POA date | Notice to file withdrawn | PLR measured at the **later** of: 30 days from the day after withdrawal; 31 January following the tax year; the day after a refund of a payment on account is issued | CH72700 | M |
| PN38 | PLR exclusions | other persons' overpayments | Overpayment by another person | Generally excluded, unless that person's liability is legally adjustable by reference to the defaulter's liability (e.g. transfer pricing compensating adjustments) | CH72640; CH72620 | M |

Failure-to-notify penalty ranges (onshore matters for all periods; category 1 offshore up to and including 2015-16):

| Behaviour | Disclosure | Min | Max | Ref |
|---|---|---|---|---|
| Non-deliberate, HMRC aware within 12 months of tax first becoming unpaid | Unprompted | 0% | 30% | CH73200 |
| Non-deliberate, HMRC aware >12 months after | Unprompted | 10% | 30% | CH73200 |
| Non-deliberate, HMRC aware within 12 months | Prompted | 10% | 30% | CH73200 |
| Non-deliberate, HMRC aware >12 months after | Prompted | 20% | 30% | CH73200 |
| Deliberate | Unprompted | 20% | 70% | CH73200 |
| Deliberate | Prompted | 35% | 70% | CH73200 |
| Deliberate and concealed | Unprompted | 30% | 100% | CH73200 |
| Deliberate and concealed | Prompted | 50% | 100% | CH73200 |

The 12-month test is described in CH73180 as "a purely objective test".

### 6.5 Inaccuracies — FA 2007 Sch 24

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| PN39 | Commencement (general) | filing due date; tax period start | Return/document due to be filed on or after 1 April 2009 relating to a tax period beginning on or after 1 April 2008 | Sch 24 paras 1 and 2 apply | CH81012 | M |
| PN40 | Commencement (para 1A, third party) | filing due date; tax period start | Due to be filed on or after 1 April 2010, tax period beginning on or after 1 April 2009 | Sch 24 para 1A applies | CH81012 | M |
| PN41 | Displacement of TMA penalties | penalty basis | Sch 24 penalty applies | TMA 1970 ss.100-103 do not apply | CH81001 | M |
| PN42 | Under-assessment notification | assessment issue date | HMRC assessment under-assesses liability | Must notify HMRC within 30 days of the date of the assessment, or a penalty is due (max 30% of PLR) | FA 2007 Sch 24 para 2; CH81090; CH81170; CH82120 | S/M |
| PN43 | Under-assessment carve-out | return timeliness | Return filed on time | No estimated assessment arises, so the under-assessment penalty cannot apply (the person self-assesses) | CH81170, caveats | M |
| PN44 | Later-discovered inaccuracy | discovery date; steps taken | Inaccuracy neither careless nor deliberate when made, later discovered, and reasonable steps to inform HMRC not taken | Treated as careless (30% of PLR) | FA 2007 Sch 24 para 3(2); CH81080 | S/M |
| PN45 | Avoidance-arrangement presumption | submission date; tax period; whether behaviour was deliberate | Inaccuracy relates to avoidance arrangements, in a document submitted on/after 16 November 2017 relating to a tax period beginning on/after 6 April 2017 and ending after 15 November 2017 | Behaviour presumed **careless** unless the inaccuracy was deliberate or the person proves reasonable care. Burden on the person for reasonable care; on HMRC for deliberate | FA 2007 Sch 24 para 3A; CH81122 | S/M |
| PN46 | Disqualified advice | advisor identity; expertise; whether advice addressed the person's individual circumstances; addressee | Advice given by an interested person, under an arrangement with one, without appropriate expertise, without regard to individual circumstances, or given/addressed to someone other than P | Advice cannot be relied on to show reasonable care, subject to the reasonable-steps exception and Conditions A–E | FA 2007 Sch 24 para 3B; CH81123 | S/M |
| PN47 | Reliance on another person | steps taken to check the information | P takes reasonable care to check information from T but the document is still inaccurate | P not liable; T may be liable if T deliberately supplied false information or withheld information intending P's document to be inaccurate | FA 2007 Sch 24 para 1A; CH81075; CH81125 | S/M |

Maximum and minimum inaccuracy penalties (FA 2007 Sch 24 para 10; CH82470; CH82510). Standard ranges — offshore matters with IT/CGT at stake use the higher ranges at CH116000.

| Behaviour | Max | Min (unprompted) | Min (prompted) |
|---|---|---|---|
| Careless / under-assessment | 30% | 0% | 15% |
| Deliberate not concealed | 70% | 20% | 35% |
| Deliberate and concealed | 100% | 30% | 50% |
| Attributable to another person | 100% | 30% | 50% |

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| PN48 | Penalty calculation | PLR; max %; min %; disclosure reduction % | Any Sch 24 penalty | Penalty % = max − (disclosure reduction % × (max − min)); Penalty = PLR × penalty %. Worked examples: PLR £145,000 × 37.5% = £54,375; PLR £12,000 × 21% = £2,520 | CH82510; CH82511; CH82512 | M |
| PN49 | Cap across persons | penalties on P and T for the same inaccuracy | Same inaccuracy penalises two persons | Aggregate must not normally exceed 100% of PLR; reduce each proportionately. Example: 15% → 13% and 100% → 87% | FA 2007 Sch 24 paras 1, 1A, 12(4)-(5); CH404500; CH84974 | S/M |
| PN50 | Offshore exception to the 100% cap | category; tax at stake | Category 2 or 3 offshore matter, IT or CGT | 100% cap may be exceeded | CH116800; CH404500 | M |

**Partnership inaccuracies**

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| PN51 | Partner's penalty | each partner's revised profit/loss allocation vs that originally declared; partner's own reliefs, allowances and tax rate | Nominated/named partner submits an incorrect SA partnership return | Each affected partner incurs a "partner's penalty" based on their own PLR. Worked example: partners A and B £4,000 × 30% = £1,200 each; partner C £2,000 × 30% = £600 (profits £50,000 → £60,000; IT 22%, Class 4 NIC 8%) | FA 2007 Sch 24 para 20; CH84730; CH84740; CH84741 | S/M |
| PN52 | Partnership appeal (inaccuracy) | nominated partner identity | Penalty for inaccuracy in a partnership return | Only the nominated partner may appeal; the appeal covers all partners' penalties | FA 2007 Sch 24 para 20; CH84760 | S/M |
| PN53 | Partnership suspension | inaccuracy source | Suspension of a partnership-return inaccuracy penalty | Applies jointly to the nominated partner and all affected partners for that inaccuracy; a partner's own separate careless inaccuracies are considered separately | FA 2007 Sch 24 para 20; CH84750 | S/M |

### 6.6 Quality of disclosure

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| PN54 | Element weightings | telling; helping; giving access assessments | Any reducible penalty | Telling 30%, Helping 40%, Giving access 30% — total 100% reduction available. Each element assessed by timing, nature and extent | CH63220; CH73220 | M |
| PN55 | Additional information element | tax year; offshore flag | Offshore matter or offshore transfer, 2016-17 and later | A fourth "additional information" element is taken into account | FA 2016 Sch 21; CH63220; CH117000 | S/M |
| PN56 | Full reduction for unneeded elements | circumstances of the case | An element of disclosure was not required | Full reduction can be given for that element | CH63220 | M |
| PN57 | Timing restriction | date the inaccuracy first occurred (date the document was given to HMRC); date disclosure started; disclosure date | Disclosure begins more than a "significant period" (normally over 3 years, possibly less where the overall disclosure covers a longer period) after the filing date / first occurrence, for disclosures after 5 September 2016 | Maximum reduction restricted by 10 percentage points. Example: unprompted deliberate range 20%–70%, max reduction cut from 50% to 40% | CH63310; CH82465; CH112700 | M |
| PN58 | Waiver of the timing restriction | officer's reasoning; authorisation | Officer decides not to apply the restriction | Requires manager/authorising officer sign-off with recorded reasons | CH63310; CH82465 | M |
| PN59 | Unprompted test | person's belief about HMRC discovery at the time of disclosure | No reason to believe HMRC had discovered, or was about to discover, the inaccuracy/failure | Unprompted; otherwise prompted. Objective test on the facts | FA 2007 Sch 24 para 9(2); CH82420; CH63140 | S/M |
| PN60 | Compliance-check cut-off | check start date; items under check | A compliance check into specific returns/documents has started | Disclosure about those items can no longer be unprompted; other undisclosed items not under check may still qualify | CH82421; CH82442 | M |
| PN61 | Non-reducible penalties | penalty type | 6-month 5% filing penalty (any behaviour) and 12-month 5% filing penalty (non-deliberate) | Cannot be reduced for disclosure | CH63120; CH63520 | M |
| PN62 | Fixed penalties unaffected | CIS gross-payment registrant status | Person registered for gross payment under CIS makes a disclosure | Disclosure does not reduce the fixed-amount penalties incurred | CH63120; CH62500 | M |

### 6.7 Special reduction and suspension

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| PN63 | Special reduction | special circumstances | Special circumstances exist | Penalty may be reduced below the statutory amount. Requires authority from the Specialist Technical Team; officers must not discuss the amount with the taxpayer | FA 2007 Sch 24 para 11; CH170900; CH403265; CH175000 | S/M |
| PN64 | Special reduction — mandatory consideration | penalty type; appeal status | Appeal against an automated penalty with a request for reconsideration; **or** before issuing any non-automated penalty | Must be considered, whether or not requested | CH174000; CH403270 | M |
| PN65 | Special circumstances exclusions | ground argued | Ability to pay; balancing under/overpayments across taxpayers; matters already accounted for elsewhere in the penalty scheme (reasonable excuse, reasonable care, disclosure reductions); deliberate behaviour; size of penalty alone; proportionality alone | Not special circumstances | CH170900; CH173000 | M |
| PN66 | Tribunal power over special reduction | HMRC's decision | Tribunal finds the decision "flawed" applying judicial review principles | Tribunal may substitute a different level of special reduction; otherwise it cannot change the amount of fixed penalties | FA 2007 Sch 24 para 17(4), (6); FA 2009 Sch 55 para 22(4); CH64600; CH82510 | S/M |
| PN67 | Suspension eligibility | behaviour type | Careless inaccuracy under Sch 24 para 1 **only** | Suspension possible. Never available for deliberate inaccuracies, inaccuracies attributable to another person, or failure to notify an under-assessment. Late-filing penalties cannot be suspended at all | FA 2007 Sch 24 para 14; CH83132; CH83142; CH61180 | S/M |
| PN68 | Suspension conditions | proposed conditions | Suspension considered | At least one specific SMART condition (Specific, Measurable, Achievable, Realistic, Time-bound) that would help the person avoid a further careless inaccuracy, plus the generic condition that all returns be filed on time during the suspension period. If no such condition can be set, no suspension | FA 2007 Sch 24 para 14(3)-(4); CH83133; CH83151; CH405070 | S/M |
| PN69 | Suspension period | period set | Suspension granted | Must not exceed 2 years | CH83110; CH405070 | M |
| PN70 | Suspension breach | further para 1 penalty during the period; condition compliance at period end | Person becomes liable to a further para 1 penalty during the period, or fails to satisfy the conditions | The suspended penalty becomes payable. No right of appeal against the decision to collect; appeal rights exist only against the decision not to suspend, partial suspension, or the conditions set | CH83110; CH405050 | M |
| PN71 | Suspension inappropriateness indicators | disclosure quality; presence of deliberate inaccuracies in the check; compliance history; overdue returns/payments; avoidance or fraud history | Any present | Suspension unlikely to be appropriate (not an automatic bar) | CH83134; CH83144; CH83145; CH83146 | M |
| PN72 | Post-cancellation discovery | discovery date relative to cancellation | Inaccurate return submitted during the suspension period but discovered only after the penalty was cancelled | The penalty cannot be brought back into charge | CH405050 | M |

### 6.8 Penalty interaction

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| PN73 | General interaction rule | penalties/surcharges on the same tax liability | More than one of: failure to notify, inaccuracy, failure to notify and withhold, failure to tell about an under-assessment, wrongdoing | Reduce so the combined percentage does not exceed the highest single applicable percentage; cannot reduce below zero; Sch 24 suspendable penalties are reduced last | FA 2007 Sch 24 para 12; CH404200; CH84970; CH65060 | S/M |
| PN74 | Sch 56 exception | penalty types | Sch 56 late payment penalty alongside another penalty | No interaction reduction; both may be charged | CH404200 | M |
| PN75 | Two filing penalties exception | 6-month and 12-month tax-geared filing penalties | Both charged | No mutual reduction, except where the combined total exceeds 100% (see PN13) | CH404200 | M |
| PN76 | Inaccuracy vs automatic filing penalty | automatic 6/12-month tax-geared filing penalty on the additional liability | Inaccuracy found in an IT or CIS return filed over 6 months late, following an amendment or discovery assessment | Reduce the inaccuracy penalty by the amount of the automatic tax-geared filing penalty assessed on the additional liability. NPPS2 must be dated and issued after the automatic assessment (which can issue up to 10 days after) | CH404450; CH403321 | M |
| PN77 | FTN vs late payment surcharge | FTN penalty; s.59C surcharge; finality | Both arise on the same tax | Discharge the surcharge once the FTN penalty is final (appeal period ended or appeal concluded); charge the FTN penalty in full. Example: 25% × £13,520 = £3,380 FTN; 10% × £13,520 = £1,352 surcharge discharged | CH404425; SAM62050 | M |
| PN78 | Inaccuracy vs surcharge timing | closure notice date | Inaccuracy penalty and s.59C surcharge both payable | Tax due 30 days after the closure notice; check the SA system 58 days after the closure notice for the first surcharge, and again at 6 months after the due date; discharge the surcharge once the inaccuracy penalty is final. If the penalty is reduced to 10% or less, withdraw the penalty in favour of the surcharge | CH404525 | M |
| PN79 | Sch 24 vs TMA s.98 | document type | Document triggers a TMA 1970 s.98 penalty | No Sch 24 penalty is payable for that document (mutually exclusive); earlier suspended Sch 24 penalties do not become payable | FA 2007 Sch 24 paras 12(1), 14; CH84960 | S/M |
| PN80 | P11D(b) carve-out | year | Years up to and including 2009-10 | Penalty under reg 81(1) SSCR 2001, not Sch 24; Sch 24 applies from 2010-11 | CH81012; COG914075 | M |
| PN81 | Publication of deliberate defaulters | qualifying PLR per investigation | Qualifying PLR for a single investigation exceeds £25,000 | HMRC may publish details. Qualifying PLR from separate compliance checks cannot be aggregated even where they cover the same or overlapping tax periods. Careless PLR does not count towards the threshold | CH "Example 2"/"Example 3" | M |
| PN82 | Interest on penalties | penalty due date; suspension status | Unpaid Sch 24 penalty past its due date | Late payment interest can be charged; not while the penalty is suspended (adjusted if later cancelled) | CH140240 | M |

### 6.9 Reasonable excuse

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| PN83 | Two-limb test | excuse existence at the date of the obligation and throughout the default; remedy timing after the excuse ended | Both limbs satisfied | No penalty. An excuse arising **after** the date of the obligation cannot be a reasonable excuse for that failure | CH160100; CH160200 | M |
| PN84 | Objective standard | person's attributes and experience | Assessing an excuse | Judged objectively against a reasonable person with the taxpayer's attributes and experience. No statutory definition of "reasonable excuse" or "unreasonable delay" | CH160100; CH160200; Rowland; Clean Car Company; Marlow Rowing Club | M |
| PN85 | Perrin four-stage test | asserted facts; evidence | Determining reasonable excuse | (1) establish the facts asserted; (2) decide which are proven on the balance of probabilities; (3) decide whether, objectively, the proven facts amount to a reasonable excuse and when it ended; (4) decide whether the failure was remedied without unreasonable delay after it ended | CH160900; *Perrin v HMRC* [2018] UKUT 156 (TC) | M |
| PN86 | Insufficiency of funds | cause of the shortage; foreseeability; due diligence | Shortage attributable to events outside the person's control, occurring despite reasonable foresight and due diligence | May be a reasonable excuse; otherwise not. Cash flow problems or anticipated inability to pay are **not** an excuse for late **filing** — the return should be filed and a time to pay arrangement sought | CH "Insufficiency of funds"; CH160800 | M |
| PN87 | Reliance on another person | steps taken (explaining requirements, setting deadlines, checking progress); agent's role | Reliance on a third person | Not a reasonable excuse unless the person took reasonable care. An agent acting as administrator/functionary — their default is attributed to the taxpayer; reasonable reliance on a professional adviser's genuine advice (absent reason to doubt it) may support an excuse | CH160700; *Lithgow* [2012] UKFTT 620 (TC) | M |
| PN88 | Non-excuses | ground argued | Agent's failure to act in time; complexity of affairs; being too busy; non-liability or overpayment of tax; the amount of tax involved | Not reasonable excuses (per ARTG; HMRC states the list is a guide, not exhaustive) | ARTG2215; CH160800 | M |
| PN89 | Ignorance of the law | person's circumstances | Objectively reasonable for that particular taxpayer to be unaware of the requirement | May be a reasonable excuse — fact- and person-specific | CH160600; *Perrin* | M |

---

## 7. Appeal, review and postponement

| # | Rule | Inputs | Condition | Result | Ref | Type |
|---|---|---|---|---|---|---|
| AP1 | Appeal to HMRC | decision notice issue date | Appealable decision received | Appeal in writing within 30 days, with valid grounds. ARTG2180 says the 30 days runs from the date the decision notice is **issued/posted**; ARTG2430/2440 states it runs from the date the customer **receives** the formal decision notice. The notes disagree; both formulations appear in the ARTG | ARTG2040; ARTG2060; ARTG2180; ARTG2430; ARTG2440 | M |
| AP2 | Late appeal acceptance | reasonable excuse; delay after the excuse ended | Reasonable excuse shown and appeal made without unreasonable delay after it ceased | HMRC must accept the late appeal. The tribunal is not limited by reasonable excuse and can accept a late appeal in the interests of justice | TMA 1970 s.49(3); ARTG2180; ARTG2215 | S/M |
| AP3 | Prerequisite for tribunal (direct tax) | prior appeal to HMRC | No written appeal sent to HMRC first | Tribunal lacks jurisdiction; HMRC applies to strike out unless a late appeal is accepted | ARTG2410; ARTG2440 | M |
| AP4 | Notice of appeal to tribunal — contents | party details; representative; address for documents; decision appealed; grounds; result sought | Notifying the tribunal | Must include all of the above plus a copy of the decision/assessment/review conclusion letter | ARTG2410 | M |
| AP5 | Review offer response | review offer letter date | HMRC offers a review | Accept the offer or notify the tribunal within 30 days of the date of the letter | TMA 1970 s.49C; ARTG2215; ARTG4220 | S/M |
| AP6 | No response to review offer | 30-day window | Customer neither accepts nor notifies the tribunal | Appeal treated as settled by agreement on HMRC's stated view | TMA 1970 s.49C(4); ARTG4070 | S/M |
| AP7 | HMRC's "view of the matter" | review request or offer | Review requested or offered | HMRC must set out its current view of the matter; without it, an offer of review is invalid and a fresh offer must be made (the customer retains the right to notify the tribunal instead). The decision maker must write within 30 days of a review request (or other reasonable time) | TMA 1970 s.49B(2), s.49C(2); ARTG2213; ARTG2216 | S/M |
| AP8 | Review period | date the "view of the matter" letter was sent (or, for indirect tax, the date HMRC received acceptance) | Review under way | 45 days unless a different period is agreed | ARTG2216; ARTG4080; ARTG4690 | M |
| AP9 | Review not completed in time | review period expiry | Review officer fails to send the conclusion letter within the review period | Decision treated as upheld; HMRC must write to say so; the customer may notify the tribunal from the day after the review period expired until 30 days from the date of that letter | ARTG4030; ARTG4850; ARTG2420 | M |
| AP10 | Post-review tribunal notification | review conclusion letter date | Customer disagrees with the review outcome | Notify the tribunal within 30 days of the date of the conclusion letter; failure means the appeal is treated as settled by agreement | TMA 1970 s.49F, s.49G(2), (5)(a); ARTG4030; ARTG2420 | S/M |
| AP11 | Tribunal notification during a live appeal | appeal date; review milestones | Appeal made | May notify the tribunal at any time between appealing and accepting a review offer, or between appealing and HMRC sending its latest view following a review request. Cannot notify while a review is being carried out (exceptions at ARTG4640) | TMA 1970 s.49D(1)-(4); ARTG2410 | S/M |
| AP12 | Out-of-time tribunal notification | reasons for delay | Outside the statutory limits | Must ask the tribunal for permission and explain why | TMA 1970 s.49G(3); ARTG2410 | S/M |
| AP13 | Reviewable decisions | decision type; appeal status (direct tax) | Customer has a right of appeal and (for direct tax) has sent an appeal to HMRC | Decision is reviewable. Not reviewable: decisions with no right of appeal; decisions on late review/late appeal; refusals of postponement/hardship; conclusions of review; simple assessments (unless a s.31AA final response given) | ARTG4040; ARTG4050 | M |
| AP14 | Simple assessment | notice issue date | Customer believes the simple assessment is or may be incorrect | Must raise a query under TMA 1970 s.31AA within 60 days of the date the notice was issued (or longer if HMRC allows). No right of appeal or review until a query has been raised and a final response given | TMA 1970 s.31AA; ARTG2040; ARTG2212; ARTG2000 | S/M |
| AP15 | Jeopardy amendment | enquiry status | Jeopardy amendment made during an SA enquiry | May appeal to HMRC, but cannot notify the tribunal or request a review until the enquiry closes | ARTG2160; EM1955 | M |
| AP16 | Closure notice appeal scope | conclusions/amendments in the notice | Appeal against a closure notice | Scope limited to the specific conclusions and amendments given effect by that notice; the review process cannot expand it | ARTG2190; ARTG4070 | M |
| AP17 | Postponement application | decision/assessment date; amount believed overcharged; reasons; existence of a valid appeal | Valid appeal exists | Apply in writing within 30 days of the decision or assessment. No valid appeal → no postponement | TMA 1970 s.55(3); ARTG2510 | S/M |
| AP18 | Disputed postponement | HMRC's notified amount; notification date | Disagreement over the amount to be postponed | Write to the tribunal within 30 days of the notification to ask it to decide. There is no right of appeal or review against HMRC's decision on a postponement application itself | ARTG2530; ARTG2510 | M |
| AP19 | Penalties and surcharges | penalty/surcharge under appeal | No statutory postponement right exists | HMRC policy is to informally stand over payment pending settlement of the appeal | ARTG2510; ARTG2570 | M |
| AP20 | Accelerated payment notice override | APN status | Tax subject to an APN | Cannot be postponed; any existing postponement ceases to have effect | ARTG2510 | M |
| AP21 | Postponement and interest | postponed amount; payment date | Postponed tax paid late | Interest is payable on tax and Class 4 NIC paid late, including postponed amounts | ARTG2560 | M |
| AP22 | Settlement by agreement | offer and acceptance; timing | Agreement reached before the tribunal completes its hearing | Appeal settled under TMA 1970 s.54; a verbal agreement must be confirmed in writing; the customer may withdraw within 30 days of the agreement (or of written confirmation). A review conclusion letter treated as a s.54(1) agreement does **not** carry the 30-day withdrawal right | TMA 1970 s.54(1), s.49F(3); ARTG3420 | S/M |
| AP23 | HMRC objection to withdrawal | withdrawal date | HMRC considers the withdrawal inappropriate | Write to the customer objecting within 30 days of the withdrawal, copying the Tribunals Service | ARTG3430 | M |
| AP24 | Case categorisation | penalty/decision type | SA and CTSA fixed filing penalties, employer end-of-year late return penalties, CIS late return penalties, Class 2 NIC late notification penalties, income tax surcharges, and s.93(3) TMA 1970 daily penalty applications | Default Paper — decided on papers alone unless a hearing is requested or directed | ARTG8350 | M |
| AP25 | Case categorisation | penalty/decision type | Late filing and late payment appeals (including daily penalties); incorrect return penalties under FA 2007 Sch 24 para 15 (except deliberate action or where the tax assessment is also appealed); CIS gross payment status; information notices | Basic — normally decided at a hearing | ARTG8350 | M |
| AP26 | Statement of case | date the Tribunals Service sent HMRC the notice of appeal | Default Paper case | HMRC must send a statement of case within 42 days; extension is not automatic and requires justified reasons | ARTG8370; tribunal rule 5(3)(a) SI 273/2009 | M |
| AP27 | Appellant's reply | date HMRC sent its statement of case | Default Paper case | Appellant may reply within 30 days; after that, neither party may submit further evidence or arguments without permission | ARTG8370 | M |
| AP28 | Strike out and reinstatement | strike out date | Case struck out | Proceedings end and the prior review or HMRC decision stands; the taxpayer may apply for reinstatement within 28 days | ARTG8340 | M |
| AP29 | Daily penalties for continuing failure | continuing failure to make a return | Failure continues | HMRC may apply to the tribunal for daily penalties | TMA 1970 s.93(3); ARTG2040 | S |
| AP30 | Penalty payment before appeal | — | Appeal against a penalty | The person need not pay the penalty before an appeal can be considered | CH64150 area | M |

---

## Rules stated too vaguely to implement

The following appear in the notes but lack a determinate input, condition or output. Each entry names what additional source detail an implementer would need.

**Notification and filing**

1. **Which taxpayers are required to file at all.** The notes describe the *consequences* of a notice to file under TMA 1970 s.8 but never state the criteria HMRC uses to issue one. Needed: the s.8 notice-issuing criteria, and the GOV.UK "check if you need to send a Self Assessment tax return" criteria (referenced only as a link in the collection index, Note 1).
2. **The Self Assessment filing deadlines as a general rule.** CH62100 gives 31 October / 31 January for ITSA, but the notes never cite the statutory provision fixing those dates, nor the rule for returns issued late (beyond the 3-month payment rule at CH140220). Needed: the s.8(1D)-type provision and its exceptions.
3. **Amendment window for a taxpayer's own return.** HS234 s.12 refers to "the time limit for amending tax return (not specified in chunk)"; HS266 refers to amendment limits only for FIG claims. Needed: TMA 1970 s.9ZA and its time limit.
4. **Enquiry window opening/closing for enquiry purposes** (as distinct from record retention). CH14530/CH14550 give the window for retention; the notes never give the s.9A enquiry window itself. Needed: TMA 1970 s.9A(2).
5. **MTD for Income Tax.** Multiple helpsheets (HS343, HS234, HS204, HS286, HS342) state that under MTD claims are made "through compatible software instead of the SA return boxes", and HS236 says qualifying care receipt customers are exempt for 2026-27. Needed: the MTD mandation thresholds, start dates, and quarterly update deadlines — none appear in the notes.
6. **HS234's adjustment year.** The note flags an internal contradiction: one passage says averaging adjustments are made via the 2024-25 tax and NIC calculation, while s.11 says via the 2025-26 liability. Needed: the correct statutory ordering rule.
7. **Which return pages/boxes apply in the current year.** Box numbers cited (TR4 boxes 5-10, Ai1 box 3, CG2 box 40/41/43, CG3 box 54, TC2 box 15, SA109 boxes 28-30 and 50-54, HS345 boxes 10-18) are year-specific and change between editions. Needed: a versioned box map per tax year.
8. **The 5 conditions exempting a QROPS transfer from the overseas transfer charge.** HS345 refers to "the 5 conditions" and to residence-based exemptions but does not enumerate them. Needed: the conditions and their tests (PTM102900, PTM112300 are cited but not reproduced).
9. **Top slicing relief computation.** HS320/HS321 confirm TSR is given as a tax reduction using the number of complete policy years, but explicitly direct readers to IPTM3820 for the calculation. Needed: the IPTM3820 method.
10. **Deficiency relief computation.** Conditions are stated (individual only, negative final result including a deduction for earlier gains, income taxable at a "relevant rate") but not the arithmetic. Needed: IPTM3860.
11. **The 7-step comparison test for high income plus flexi-access.** HS345 says the test exists and produces "excess amount 1" and "excess amount 2", but the steps are not enumerated. Needed: the full step list.
12. **Threshold income and adjusted income definitions.** Given only as "income excluding pension contributions, unless paid as salary sacrifice" and "income added to any pension contributions". Needed: the statutory computations, including which deductions apply.

**Assessment and discovery**

13. **The substantive conditions for a discovery assessment.** The notes give "reason to suspect" as an *information notice* threshold and describe s.29(4)-(5) only obliquely. Needed: the full s.29 conditions, including the taxpayer-protection conditions where a return has been made.
14. **"Significantly harder to identify" (offshore transfers).** CH53540 says it means HMRC was "significantly less likely to become aware" or would become aware "significantly later", with "significantly" bearing its normal meaning of noteworthy, important or consequential. Not codable without a determinate test.
15. **Category 1 and 3 territory lists.** CH112400/CH403147 confirm the lists are set by Treasury Order and are date-sensitive, and CH112400's reproduced text is noted as containing transcription errors ("Lativa", "Lithiania", merged entries). Needed: the authoritative Treasury Order schedules with commencement dates.
16. **Transitional table CH51560.** The notes reference a table mapping claim/assessment dates (1 Feb 2009 – 5 Apr 2013) to the earliest reachable tax year (2003-04 to 2008-09) but do not reproduce it.

**Penalties**

17. **The reduction percentage assigned to a given quality of disclosure.** The weightings (30/40/30) are given, and timing/nature/extent are named as the assessment axes, but no rule maps a fact pattern to a percentage. This is discretionary officer judgement in the sources.
18. **"Significant period".** Normally over 3 years but "may be less where the overall disclosure covers a longer period" (CH63310, CH82465). The shorter case has no stated test.
19. **Multi-year, multi-inaccuracy treatment of the 3-year rule.** CH82465 says treatment "differs depending on whether disclosure covers multiple years/inaccuracies for the same or different reasons" — the rule may apply to all years or be considered separately per inaccuracy — without stating which applies when.
20. **"Special circumstances".** Per *Barry Edwards* (UT), not to be given a restrictive interpretation; any relevant factor meaning the statutory penalty "would not be right in that specific case". Exclusions are listed (PN65) but no positive test is.
21. **Reasonable care.** Defined as the standard of "a prudent and reasonable person in the position of the person in question", assessed against the person's abilities and circumstances. Only illustrative examples are given.
22. **Penalty models 2, 3 and 4 in full.** Model 4 (PAYE RTI) band amounts are given (£100/£200/£300/£400 by employee count) and model 3 escalation (£200/£300/£400) is given, but the notes do not give the RTI monthly filing dates or the model 3 penalty-period mechanics in enough detail to implement. CIS (model 2) is partially given.
23. **Sch 55 minimum penalties table (CH63200).** Referenced repeatedly as the floor below which reductions cannot go, and partially reproduced for onshore/Cat 1 up to 2015-16, but not given for all combinations.
24. **Whether the 12-month further penalty percentages differ for onshore matters in 2016-17+.** CH63200 covers onshore for all periods; CH112700 gives offshore tables split at 2015-16/2016-17. The interaction is stated but the onshore 2016-17+ figures are not separately confirmed.
25. **The 2013 territory-category table split.** CH112400 confirms two tables exist (filing date before vs on/after 24 July 2013) and that using the wrong one is a common error, but reproduces neither in full.
26. **Class 2 and Class 4 NIC.** Class 4 NIC appears in penalty-interaction contexts (CH404300, CH404525) and in the HS234 averaging example, and Class 2 NIC late-notification penalties appear in tribunal categorisation. The notes contain no Class 2/Class 4 rates, thresholds or computation rules.

**Payment**

27. **Interest rates.** No rate, rate-setting mechanism, or rate-change dates appear anywhere in the notes — only the start/end dates and the simple-interest rule.
28. **Time to Pay eligibility and terms.** CH140280 confirms interest continues during a TTP arrangement and CH160xxx suggests contacting HMRC for one, but no eligibility criteria or terms are given.
29. **The de minimis for reducing payments on account, and the mechanics of making the claim.** CH142240 describes the consequences of an excessive claim but not how or when the claim is made.
30. **Payments-on-account exclusions.** CH142240 notes that, for interest purposes, capital gains tax and student loan repayments are excluded from the balancing-payment computation under FA 2009 Sch 53 para 1, and CGT only under para 2 — but the notes do not state the general rule for whether CGT or student loan amounts enter the POA calculation itself.

**Appeals**

31. **The appeal deadline start date.** As flagged at AP1, ARTG2180 (date of posting) and ARTG2430/2440 (date of receipt) are inconsistent within the same manual. An implementer needs the statutory provision (TMA 1970 s.31A) to resolve this.
32. **Hardship applications.** Referenced in ARTG2040 as a tribunal application carrying no right of appeal, but no conditions or process are given.
33. **The exceptions at ARTG4640** to the rule that a customer cannot notify the tribunal while a review is under way.
34. **Withheld content.** Several manual pages are noted as withheld under FOIA exemptions or moved to internal systems (CH500000, CH930000, CH290000, CH920000, parts of CH206250, CH81195, CH84645, CH84665, CH279600, CH402336/402338, CH403145 area). Any rules in those pages are unavailable.

---

## Notes on using this inventory

- Where two entries give different figures for the same concept (for example the 6-month further penalty stated as "£300" in CH62940 for partnerships and as "greater of 5% of tax liability and £300" in CH62140 generally), the difference is real: partnership IT/CGT returns have no tax-geared component because the partnership itself has no IT/CGT liability (CH62920).
- Every rate, threshold and cap sourced from a helpsheet (type **G**) is stated in the notes as applying to a specific tax year, usually 2025-26. These should be modelled as year-keyed parameters, not constants.
- Manual entries (type **M**) record HMRC's operational practice and interpretation. Several — notably the disclosure-reduction percentages, the special-reduction exclusions, and the "significant period" restriction — are HMRC policy positions that a tribunal is not bound to follow, and CH170900 expressly notes that HMRC does not always follow non-binding First-tier Tribunal decisions.

---

## Sources used on this page

This page was written by an LLM from structured notes extracted from the mirrored sources below. Always check the upstream source before relying on any figure or deadline.

- [govuk-sa-detailed-information](https://www.gov.uk/government/collections/self-assessment-detailed-information) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/govuk-guidance.md`
- [sa-helpsheets:5f67dfee-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/accrued-income-scheme-hs343-self-assessment-helpsheet) - 2 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/accrued-income-scheme-self-assessment-helpsheet-hs343.md`
- [sa-helpsheets:5f67ceae-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/averaging-for-creators-of-literary-or-artistic-works-hs234-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/averaging-for-creators-of-literary-or-artistic-works-self-assessment-helpsheet-hs234.md`
- [sa-helpsheets:5f67d41e-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/employee-share-and-security-schemes-and-capital-gains-tax-hs287-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/capital-gains-tax-and-employee-share-schemes-self-assessment-helpsheet-hs287.md`
- [sa-helpsheets:5f67ddc2-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/charitable-giving-hs342-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/charitable-giving-tax-relief-self-assessment-helpsheet-hs342.md`
- [sa-helpsheets:5f67dc31-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/employee-shares-and-securities-further-guidance-hs305-self-assessment-helpsheet) - 2 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/employment-related-shares-and-securities-self-assessment-helpsheet-hs305.md`
- [sa-helpsheets:f689f4a2-7da1-41a3-b37d-b18c346219ed](https://www.gov.uk/government/publications/foreign-income-and-gains-fig-regime-self-assessment-helpsheet-hs266) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/foreign-income-and-gains-fig-regime-self-assessment-helpsheet-hs266.md`
- [sa-helpsheets:5f67e2d6-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/furnished-holiday-lettings-hs253-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/furnished-holiday-lettings-self-assessment-helpsheet-hs253.md`
- [sa-helpsheets:5f67db85-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/gains-on-foreign-life-insurance-policies-hs321-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/gains-on-foreign-life-insurance-policies-self-assessment-helpsheet-hs321.md`
- [sa-helpsheets:5f67dcd2-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/gains-on-uk-life-insurance-policies-hs320-self-assessment-helpsheet) - 3 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/gains-on-uk-life-insurance-policies-self-assessment-helpsheet-hs320.md`
- [sa-helpsheets:5f67e282-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/limit-on-income-tax-reliefs-hs204-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/limit-on-income-tax-reliefs-self-assessment-helpsheet-hs204.md`
- [sa-helpsheets:5f67d46f-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/negligible-value-claims-and-income-tax-losses-on-disposals-of-shares-you-have-subscribed-for-in-qualifying-trading-companies-hs286-self-assessment-he) - 2 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/negligible-value-claims-and-income-tax-losses-on-disposal-of-shares-self-assessment-helpsheet-hs286.md`
- [sa-helpsheets:5f67cefb-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/remittance-basis-hs264-self-assessment-helpsheet) - 3 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/paying-tax-on-the-remittance-basis-self-assessment-helpsheet-hs264.md`
- [sa-helpsheets:5f67defe-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/pensions-tax-charges-on-any-excess-over-the-lifetime-allowance-annual-allowance-special-annual-allowance-and-on-unauthorised-payments-hs345-self) - 4 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/pension-savings-tax-charges-self-assessment-helpsheet-hs345.md`
- [sa-helpsheets:5f67cd23-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/qualifying-care-relief-foster-carers-adult-placement-carers-kinship-carers-and-staying-put-carers-hs236-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/qualifying-care-relief-for-carers-self-assessment-helpsheet-hs236.md`
- [sa-helpsheets:5f67e327-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/seed-enterprise-investment-scheme-income-tax-and-capital-gains-tax-reliefs-hs393-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/seed-enterprise-investment-scheme-income-tax-and-capital-gains-tax-reliefs-self-assessment-helpsheet-hs393.md`
- [hmrc-manual-artg](https://www.gov.uk/hmrc-internal-manuals/appeals-reviews-and-tribunals-guidance) - 10 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/artg.md`
- [hmrc-manual-ch](https://www.gov.uk/hmrc-internal-manuals/compliance-handbook) - 84 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/ch.md`
