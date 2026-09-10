---
title: Data requirements for a head-of-duty implementation
generated: true
generated_on: '2026-09-10'
generated_by: claude-cli:opus
input_hash: d4fe0163cfdc5548
note_count: 110
sources:
- govuk-sa-detailed-information
- hmrc-manual-artg
- hmrc-manual-ch
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
- sa-helpsheets:5f67dfee-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67e282-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67e2d6-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67e327-7631-11e4-a3cb-005056011aef
- sa-helpsheets:f689f4a2-7da1-41a3-b37d-b18c346219ed
---

# Data requirements for a head-of-duty implementation

!!! danger "Unofficial - not HMRC, not advice, written by an LLM"

    This page is **not** an HMRC publication and has no connection to HMRC or
    any government body. It was **written by a language model** from mirrored
    source material, and can be wrong, incomplete or out of date. It is not
    tax advice. Check every figure, date and rule against the cited source
    before relying on it, and see
    [GOV.UK](https://www.gov.uk/self-assessment-tax-returns) for official
    guidance.

This page derives, from the supplied source notes only, the data model a Self Assessment head-of-duty system would need: the entities, the attributes each entity needs to evaluate the rules the sources describe, the lifecycle transitions and their triggers, and the reference data that must be versioned by tax year. It is an independent analysis, not an HMRC specification. The notes available are heavily weighted towards penalties, interest, time limits, appeals and helpsheet-level claim mechanics; gaps are listed at the end rather than filled from elsewhere.

---

## 1. Scope of the derivation

The notes fall into three evidential tiers, and the data model needs to record which tier a rule came from because they carry different authority:

| Tier | Examples in the notes | Implementation consequence |
|---|---|---|
| Statute | TMA 1970 ss.7, 8, 8A, 9A, 12AC, 12B, 28A, 28C, 29, 31AA, 34, 36, 49–49G, 54, 55, 59A, 59B, 122AA; FA 2007 Sch.24; FA 2008 Sch.36, Sch.41; FA 2009 Sch.53–56; FA 2011 Sch.23 | Binding; the rule engine's authority |
| HMRC interpretation (manuals) | Compliance Handbook (CH…), Appeals Reviews and Tribunals Guidance (ARTG…), plus manuals cited within them (EM, SAM, IPTM, PTM, RDRM, VCM, CG) | HMRC's view; drives operational behaviour but is not law |
| Customer-facing guidance | GOV.UK Self Assessment collection (Note 1); helpsheets HS204, HS234, HS236, HS237, HS253, HS264, HS266, HS286, HS287, HS292, HS305, HS320, HS321, HS325, HS340, HS341, HS342, HS343, HS345, HS393 | Simplified; the notes themselves warn helpsheets "cover most cases but not everything" (HS343 caveats) |

A practical consequence: any stored rule needs a `source_tier` and a `ref` string, because the notes repeatedly show HMRC manual positions that are not statutory rules — e.g. informal "standover" of penalties and surcharges under appeal is described as HMRC *policy*, not a statutory right (ARTG2510), and ARTG2510 states there is "no formal statutory right of postponement… for penalties or surcharges".

---

## 2. Entities

### 2.1 Taxpayer (person "P")

The notes define who can be a person for penalty purposes very widely: individuals, employers, CIS contractors, companies, partners, LLPs, personal representatives, pension scheme administrators, trustees, public bodies, Crown bodies, and persons registered for Machine Games Duty (CH61190, CH71180). For SA specifically the return-filing persons are individuals (TMA 1970 s.8(1)), trustees (TMA 1970 s.8A(1)) and partnerships (TMA 1970 s.122AA) (CH61180).

Attributes required by rules in the notes:

| Attribute | Rule it feeds | Ref |
|---|---|---|
| Capacity (individual / trustee / partner / personal representative / representative partner) | Who may appeal; who files; who is liable | ARTG2150; CH64540 |
| National Insurance number | Reporting a chargeable event gain below the £10,000 threshold outside SA | HS320 s.6.1 |
| Death date | 30-day-post-probate interest rule; assessment window; return to date of death | FA09/Sch53 para 12; CH54200; HS343 s.9 |
| Probate / letters of administration / confirmation date | Late payment interest start date after death | FA09/Sch53 para 12 (CH143380) |
| Bankruptcy / insolvency status; trustee in bankruptcy | Loss of standing to appeal; insolvency practitioner decides appeals | ARTG2150; ARTG2710 |
| Company status (struck off / in administration) | Struck-off companies cannot appeal | ARTG3030 |
| Residence status by tax year; split-year overseas part; "foreign days" | Time apportioned reduction; FIG regime; temporary non-residence | HS320 s.9.3; HS266 s.2; HS345 |
| Years of UK residence / 10-year non-residence run | "Qualifying new resident" test for FIG regime | HS266 s.2 |
| Membership of House of Commons/Lords | Excluded from qualifying new resident | HS266 s.2 |
| Trade/profession/business indicator (incl. property letting) | Record retention period; "trade includes the letting of property" | CH11300; CH14550 |
| Carer status; MTD mandation status | Qualifying care relief; whether SA boxes or software apply | HS236; HS341 intro |
| Agent appointment and agent type (functionary vs adviser) | Reasonable excuse analysis | CH160700 (Lithgow) |
| High Volume Agent flag | Referral to Agent Compliance Team | CH820000 |
| Address / last known place of residence; email consent | Valid service of notices | CH23440 |

Note the two-sided point at CH871000: appointing an agent does not shift legal responsibility for tax affairs off the taxpayer.

### 2.2 Notice to file

The obligation is triggered by a notice, not by the tax year alone: the filing obligations at CH61180 are all expressed as duties arising once a notice to file is issued (TMA 1970 s.8(1)(a)/(b), s.8A(1)(a)/(b), s.122AA(2)/(3)).

Required attributes: notice type (s.8 individual / s.8A trustee / s.122AA partnership); issue date; tax year or period; whether accounts/statements/documents are also required; filing date (paper vs electronic — for 2010-11, 31 October 2011 and 31 January 2012 respectively, CH61120); withdrawal flag and withdrawal date; and whether the return was *voluntary*.

Two transitions matter for machine implementation:

- **Withdrawal.** If HMRC agrees to withdraw the notice to file, late filing penalties already charged are cancelled (FA09/Sch55 para 17A; CH64280, CH61700). CH61700 limits this to relevant periods beginning on or after 6 April 2012 for partnerships including companies, and 2012-13 onwards for other partnerships, individuals and trustees. Withdrawal does not extinguish liability: the person must still notify chargeability under TMA 1970 s.7(1B) (CH143020, CH71240).
- **Voluntary return.** CH820000 states that from 12 February 2019, voluntary returns (received where HMRC gave no notice) are treated as made in response to a notice to file given on the date the return was received, retrospectively and prospectively. A `notice_deemed` flag with `deemed_issue_date = receipt_date` is therefore needed.

Late-issued notices change the payment due date: where a s.8 notice is issued after 31 October following the year of assessment, payment is due 3 months from the date of the notice (CH140220, citing TMA 1970 s.8). CH155010 similarly says the income tax/CGT due date "can be later if the return was issued late".

### 2.3 Return

Attributes: person; capacity; tax year; return type (SA100 core plus supplementary pages SA101 additional information, SA102 employment, SA103S/F/L self-employment, SA104S/F partnership, SA105 UK property, SA106 foreign, SA107 trusts, SA108 capital gains, SA109 residence/FIG, SA110 tax calculation summary, SA900/SA904 trust and estate — all appearing across HS204, HS266, HS320, HS321, HS345); filing date; actual filing date; channel; amendment history; and pre-population interaction flags.

The pre-population flags are a distinct data need: CH206225 describes a mandatory tick box "I have viewed the information HMRC holds about me" on the online return, and CH402350 requires HMRC to issue the Human Rights Act and penalty factsheets before questioning a taxpayer about a discrepancy where they accepted, changed or deleted pre-populated data. Implementations therefore need per-field provenance: `source = prepopulated | user_entered`, and `user_action = accepted | changed | deleted`.

Box-level data is unavoidably part of the model because the notes tie claims to specific boxes. A non-exhaustive extract:

| Claim / entry | Box | Ref |
|---|---|---|
| Gift Aid totals | TR 4 boxes 5–8 | HS342 s.1.1 |
| Gifts of shares/securities; land/buildings | TR 4 boxes 9, 10 | HS342 ss.2–3 |
| Other taxable income | TR 3 boxes 17, 18 | HS325 |
| Accrued income net adjustment (gross interest) | Ai 1 box 3 | HS343 s.8.2 |
| Share schemes | Ai 2 box 1 | HS305 |
| EIS subscriptions | Ai 2 box 2 ("Other tax reliefs") | HS341 s.2 |
| CITR invested amount | Ai 2 box 3 | HS237 s.2 |
| Qualifying loan interest | Ai 2 box 5 | HS340 |
| Annual allowance excess; scheme-paid charge; PSTR | Ai 4 boxes 10, 11, 12 | HS345 |
| Overseas transfer charge | boxes 11.1, 11.2 | HS345 |
| Unauthorised payments (non-surcharge / surcharge); foreign tax | boxes 13, 14, 15 | HS345 |
| Averaging adjustment (sole trader / partner) | SA103F box 72 / SA104 box 11 | HS234 ss.8–9 |
| Share loss relief (2025-26) | SA108 box 41 (2024-25: box 43); losses box 35 | HS286 |
| SEIS reinvestment relief | SA108 box 40; code 'OTH' box 28 | HS393 s.3.3 |
| Negligible value loss | SA108 boxes 7/19/27/35 with code 'NVC' or 'MUL' in 8/20/28/36 | HS286 |
| SBA/demolition disclosure | SA108 box 20 code 'OTH'/'MUL'; box 54 | HS292 s.8.3 |
| Free-text disclosures | TR 7 box 19; SA108 box 54 | HS237, HS341, HS286 |
| FIG regime claims | SA109 boxes 28, 29, 30 | HS266 s.3 |
| TRF designation | SA109 boxes 50, 51, 52, 54 | HS264 s.4.3.2 |
| Business investment relief | SA109 box 38 (breakdown box 54) | HS264 s.1.2 |

Two implementation-relevant quirks: rounding is directional for accrued income (profits rounded **down**, losses rounded **up**, HS343 s.8.2), and some reliefs require the *full* figure on the return with HMRC computing the relief — top slicing relief is given as a reduction in tax, so "the full amount of the gain" is entered (HS320 s.10.1), unlike RRQP and time apportioned reductions which the taxpayer computes and deducts before entry (HS320 s.9.2/9.3).

### 2.4 Claim / election (as a first-class entity, not just a return field)

The notes make claims separable from returns in three ways: they can be made outside a return (TMA 1970 Sch.1A para 2A, CH11500), they carry their own record-retention and enquiry windows (CH14900), and several have their own statutory deadlines.

Required attributes: claim type; tax year claimed for; year in which made; "later year" (for carry-back and averaging, FA09/Sch54 para 7); amount; whether made in original or amended return; supporting certificate reference and receipt date; priority ordering where more than one year is claimed (HS286); irrevocability flag.

| Claim/election | Time limit | Ref |
|---|---|---|
| FIG regime foreign income/gain claim | Anniversary of 31 January following the tax year (2025-26: 31 January 2028) | HS266 s.4 |
| FIG claim amendment | Same, unless notice to file issued after 31 October 2026 | HS266 s.4 |
| FHL averaging election | One year after 31 January following the tax year | HS253 |
| FHL period of grace election | Same | HS253 |
| SBA demolition disapplication (written, irrevocable) | First anniversary of 31 January following year of demolition (2025-26 demolition: 31 January 2028) | HS292 s.8.2 |
| Share loss relief against income | One year from 31 January following the loss year (2025-26 loss: 31 January 2028) | HS286 |
| Negligible value: earliest specifiable disposal date | Up to 2 years before the start of the tax year of claim | HS286 |
| SEIS reinvestment relief (as stated for the 2025-26 helpsheet) | 31 January 2032 | HS393 s.3.4 |
| CG34 valuation check | At least 3 months before the return filing date | HS286 |
| Gift Aid carry-back | Must be in the **original** return for the year ended 5 April 2026, before the filing date; HMRC cannot accept a first or higher claim in an amended return | HS342 s.1 |
| Business investment relief on pre-6 April 2025 FIG | No claims after 5 April 2028 | HS264 s.1.2 |
| CITR formal claim | Not before the Tax Relief Certificate is received **and** the tax year has ended | HS237 s.2 |
| EIS/SEIS claim | Not before EIS3/EIS5/SEIS3 received | HS341 s.2; HS393 s.3.4 |
| Averaging re-claim after profits change | Amend return; if amendment window expired, write to HMRC "without delay due to a time limit" (limit not stated) | HS234 s.12 |

Machine-implementable form for the commonest shape:

> **Input:** tax year `Y`, claim type in {FIG income, FIG gains, FHL averaging, FHL period of grace, share loss relief, SBA demolition election}. **Condition:** claim date ≤ 31 January of year `Y+2`. **Result:** in time. (Refs as tabled; note HS266 s.4 adds the exception where a notice to file was issued after 31 October following the year.)

Certificate dependency is a hard gate, not a soft one: relief "is only available once form EIS3 or EIS5 has actually been received" (HS341 caveats), and CITR cannot be formally claimed until the certificate is in hand (HS237 s.2). Certificates must be retained but not filed (HS237, HS341).

### 2.5 Payment, payments on account and schedule

Attributes: person; tax year; payment type (first POA, second POA, balancing payment, penalty, interest, TRF charge); statutory due date; actual payment or set-off date; amount; allocation; deferral/Time to Pay agreement; and a reduction-claim record for POAs.

Statutory anchors: POAs and balancing payments under TMA 1970 s.59A and s.59B, with due dates of 31 January in the tax year, 31 July following, and 31 January following the end of the tax year respectively (CH142260). CH140290 requires interest to be computed **separately** on each POA and on the balancing payment.

Allocation is a defined algorithm and must be implemented as such. For repayment interest purposes, an income tax overpayment is allocated first to the balancing payment, then in two equal parts to payments on account, then to overpaid PAYE/tax deducted at source (FA09/Sch54 para 13; CH146120). Where POAs were paid in instalments, allocation goes to later instalments before earlier ones (CH146120 caveat).

Reduced-POA claims need their own attributes because an excessive reduction changes the interest base. FA09/Sch53 para 1 sets the interest-bearing amount as the **lesser** of (a) each reduced POA plus 50% of the balancing payment and (b) the amount that would have been payable as a POA had no reduction claim been made (CH142240). FA09/Sch53 para 2 handles the mirror case: where POAs were paid late but the year is overpaid, interest runs on the amount by which each late POA exceeds 50% of the overpayment for the year.

Deferral agreements: requested **before** the due date, they suspend penalties for the deferral period; breaking the agreement makes the person liable to penalties calculated as if the deferral did not exist, from the date of HMRC's notice (FA09/Sch56 para 10; CH156600). Time to Pay does not stop late payment interest, which continues on reducing balances (CH140280).

### 2.6 Interest

Late payment and repayment interest are separate objects with separate start/end date rules, and both are **simple, not compound** (FA09 s.101(8), s.102(7); CH140260).

| Interest type | Start date | End date | Ref |
|---|---|---|---|
| Late payment | Date the amount becomes due and payable, even if a non-business day | Date payment is made or set-off takes place | CH140190/CH140200; FA09 s.101 |
| Repayment, Rule 1 (amount paid to HMRC) | Later of date paid and date it was due and payable | Date repaid, paid to another person, or set off | CH146020/CH146040; FA09 s.102 |
| Repayment, Rule 2 (return/claim, not paid) | Later of date return/claim was required and date actually made | As above | CH146020 — **currently VAT only**, PAPs from 01/01/2023 |
| Repayment, tax deducted at source | 31 January of the year following the year to which the income tax relates | — | FA09/Sch54 para 6; CH146240 |
| Repayment, loss carry-back / farmers' averaging | 31 January following the "later year" of the claim | — | FA09/Sch54 para 7; CH146280 |
| Late payment, after death | Later of normal start date and the day after 30 days from grant of probate/letters of administration/confirmation | — | FA09/Sch53 para 12; CH143380 |
| Late payment, corrected/amended assessment | Date tax would have been due had the original return been complete and accurate — **not** the amendment date | — | CH143020/CH143240 |

Design constraints from the notes: no interest is charged or paid on interest (CH140190); repayment interest is not paid where the amount is payable as a result of a court or tribunal order that already carries interest (FA09 s.102(6)); there is no HMRC discretion to waive interest and no statutory right of appeal against interest itself, though an appeal against the underlying tax flows through automatically (CH140295/CH140300); a contract settlement replaces statutory interest with contractual terms (CH140310); and Breathing Space (in force from 4 May 2021) excludes interest accruing during the moratorium (CH140320). Every calculation must first test applicability: "check whether and from which date the FA 2009 interest rules apply to the tax or duty" (CH140160) — so the model needs an `interest_regime_applicability(tax, date)` lookup.

### 2.7 Enquiry, compliance check and closure

Attributes: enquiry notice date and statutory basis (TMA 1970 s.9A individual/trustee, s.12AC partnership, Sch.1A para 5 for claims); the "matters" under enquiry; jeopardy amendments; partial closure notices; final closure notice; enquiry window state.

Enquiry window closure, as stated at CH14550 for record-retention purposes: **12 months after the date the return was filed** if filed on time; **the first anniversary of the next quarter day after filing** if filed late.

The concept of an *open* enquiry is defined for information-notice purposes: an enquiry is open if a notice of enquiry has been issued and no closure notice covering the matters to which the request relates has yet been issued; where a partial closure notice has been issued, further requests are restricted to matters not closed by it (CH23540).

Partial closure notices (introduced by Finance (No.2) Act 2017) close individual "matters" before the whole check ends. They require approval from an independent officer who has not worked the case, requested on form PCN101 with before-and-after tax calculations (CH279600, CH279610). A taxpayer who wants a PCN that HMRC will not give may apply to the tribunal for a direction (CH279600, EM2163). A final closure notice is issued once all matters are complete, unless settled by contract.

Two scope rules with direct implementation consequences: an appeal against a closure notice is limited to the conclusions and amendments given effect by that notice, and the review process cannot expand that scope (ARTG2190, ARTG4070); and a jeopardy amendment can be appealed to HMRC but cannot be notified to the tribunal or reviewed until the enquiry closes (ARTG2160, EM1955).

Information notices are a related entity: service by delivery to the person, leaving at their usual or last known residence, or **by email only with the customer's explicit informed consent** (CH23440); a compliance period specified in the notice, possibly with time, means and form (FA08/Sch36 para 7; CH23480). Where an SA return has already been made for the period, a taxpayer notice may only be issued if there is an open enquiry, a potential discovery position, or the notice is needed for another tax or for checking reductions/repayments (FA08/Sch36 para 21; CH23540). "Reason to suspect" is a lower threshold than being able to assess, but does not license speculative enquiries (FA08/Sch36 para 21(6); CH23560).

### 2.8 Assessment and determination

Distinct sub-types in the notes, each with its own time limit:

| Type | Time limit | Ref |
|---|---|---|
| Determination where SA return not filed | 3 years beginning with the statutory filing date | CH52100 |
| Normal assessment | 4 years from end of relevant tax period | CH52100 |
| Careless behaviour | 6 years (IT, CGT, CT, SDLT, IHT, SDRT, PRT) | CH53100/CH53400 |
| Offshore matter/transfer (IT, CGT, IHT) | 12 years | CH50100/CH53510 |
| Deliberate behaviour; failure to notify; avoidance-scheme non-disclosure | 20 years | CH53600/CH53700/CH54000 |
| Assessment on deceased (IT/CGT) | Within 4 years of end of year of assessment of death; no year ending more than 6 years before death | TMA70/S40(2); CH54200 |
| Recover over-repayment | Latest of 4/6/20 years (by behaviour), end of following year of assessment, or closure of enquiry by FCN | TMA70/S30(5) with S34/S36; CH56100 |
| Employment/pension/social security income received late | Later of 4/6/20 years from the year assessable and from the year of receipt | TMA70/S35 with S36; CH56100 |
| EIS relief withdrawal | Later of 6 years (20 if deliberate) from year of the use-of-money requirement or the triggering event | ITA07/S237; CH56100 |
| CITR withdrawal | 6 years (20 if deliberate) from end of year relief obtained | ITA07/S372; CH56100 |
| Simple assessment | 4 years from end of year of assessment | TMA70/S28; CH56100 |

The notes flag two constraints an implementation must not lose. First, the 4-year normal limit replaced 6 years for direct taxes for assessments made on or after 1 April 2010 regardless of the year assessed (SI 2009/403 art.2(2); CH51540) — so a `limit_regime(assessment_date)` dimension is needed alongside the tax-year dimension. Second, extended-time-limit assessments require prior authorisation from an Authorising Officer (CH53300, CH282070, EM3257), and HMRC bears the onus of proving careless or deliberate behaviour (CH54300).

Simple assessment needs its own state machine because it has **no right of appeal** unless the taxpayer has raised a s.31AA TMA 1970 query and received a final response — a query which must be raised within 60 days of the notice of Simple Assessment, or such longer period as HMRC may allow (ARTG2040, ARTG2212, s.31AA TMA 1970).

### 2.9 Penalty

Penalties are the most data-hungry entity in the notes and need to be modelled as a class hierarchy over four regimes:

- **FA 2009 Sch.55 — failure to file.** Applies to SA returns for the year ended 5 April 2011 onwards (CH61120, subject to exceptions at SAM121025).
- **FA 2009 Sch.56 — late payment.** For IT/CGT balancing payments due on or after 31 January 2012; explicitly **not** payments on account (CH154550/CH155010).
- **FA 2008 Sch.41 — failure to notify.** From 1 April 2010; for IT/Class 4 NIC and CGT the first period is 2009-10 (CH65040, CH71120).
- **FA 2007 Sch.24 — inaccuracy and under-assessment.** Generally for returns due on or after 1 April 2009 relating to periods beginning on or after 1 April 2008; para 1A (third-party) from 1 April 2010/period from 1 April 2009 (CH81012).

Required attributes: regime; paragraph; tax year/period; behaviour; disclosure type and quality; territory category; potential lost revenue (PLR) or liability-to-tax (LTT) base; percentage before and after reduction; minimum floor; interaction adjustments; suspension state; assessment date; appeal state; special reduction authorisation.

**Sch.55 timeline (penalty model 1: occasional returns and returns for periods of 6 months or more, including IT excluding PAYE and CGT — CH62020):**

| Trigger | Amount | Ref |
|---|---|---|
| Filing date missed → penalty date = day after filing date | £100 initial fixed | CH61160, CH63520; FA09/Sch55 para 3 |
| 3 months after penalty date | £10/day for up to 90 days | CH62120; FA09/Sch55 para 4 |
| 6 months after penalty date | Greater of 5% of liability and £300 | CH63580; FA09/Sch55 para 5 |
| 12 months, not deliberate | 5% of liability (min £300) — **not reducible for disclosure** | CH63600; FA09/Sch55 para 17 |
| 12 months, deliberate not concealed | 70% of liability (min £300) | CH63600; FA09/Sch55 para 11 |
| 12 months, deliberate and concealed | 100% of liability (min £300) | CH63600; FA09/Sch55 para 6 |

CIS variants use different floors (£1,500 deliberate; £3,000 deliberate and concealed) and add a £200 second fixed penalty at 2 months (CH63640, CH62360). PAYE RTI (model 4) has no 6-month further penalty and no further fixed/daily penalties, with a separate 5% "extended failure" penalty (CH62880, CH401222).

**Sch.56 late payment for IT/CGT balancing payments:** due date 31 January following the year of assessment (later if the return was issued late); penalty date 31 days after the due date — 3 March, or 2 March in a leap year, for a 31 January due date; then 5% initial, 5% at 5 months after the penalty date, 5% at 11 months (CH155010, CH155100–CH155160). Where tax becomes due under a determination or assessment made in the absence of a return, the penalty date is 31 days after the due date that would have applied had the tax been shown on a timely return; where it arises from an assessment, amendment or correction, it is 31 days after the due date for the further tax (CH155200).

**Sch.24 inaccuracy maxima:** careless 30% of PLR; deliberate not concealed 70%; deliberate and concealed 100%; inaccuracy due to another person's deliberate behaviour 100%; failure to notify an under-assessment 30% (CH82120).

**Offshore categorisation** multiplies the Sch.55 12-month maxima: Category 1 100%/70%/5%; Category 2 150%/105%/5%; Category 3 200%/140%/5% (CH112600). Categories are defined by information-exchange status — category 1 automatic exchange (the UK itself is category 1), category 3 no exchange, category 2 everything not listed in 1 or 3 (CH403145). Category must be resolved **as at the relevant date** (filing date, or date of the notification failure), not as at the current date, because Treasury Orders move territories (CH112400, CH403145). The tables themselves split on whether the filing date was before or on/after 24 July 2013 (CH112400).

**Disclosure reduction** is a weighted calculation: telling 30%, helping 40%, giving access 30%, totalling 100% of the available reduction band (CH63220, CH73220). For offshore matters and offshore transfers in 2016-17 and later, a fourth element — "additional information" under Schedule 21 FA 2016 — is added (CH63220, CH117000). Where a person took a "significant period" (normally over 3 years, possibly less) to correct non-compliance, or could previously have used an offshore disclosure facility, HMRC is "unlikely to reduce the penalty more than 10 percentage points above the minimum" (CH112700, CH63310) — a rule which requires a documented manager or authorising-officer override to disapply (CH63310).

Failure-to-notify ranges (onshore, and Category 1 offshore up to and including 2015-16) from CH73200:

| Behaviour | Unprompted | Prompted |
|---|---|---|
| Non-deliberate, HMRC aware within 12 months | 0%–30% | 10%–30% |
| Non-deliberate, HMRC aware after 12 months | 10%–30% | 20%–30% |
| Deliberate | 20%–70% | 35%–70% |
| Deliberate and concealed | 30%–100% | 50%–100% |

**Penalty interaction** is a required post-processing pass, not an afterthought. The notes give a table of situations (CH404300) and specific caps:

- Sch.55 6-month plus 12-month tax-geared penalties must not together exceed 100% of the tax liability (FA09/Sch55 para 17; CH404475) — except for Category 2/3 offshore matters where the tax is IT or CGT (CH404200, CH404475).
- Where an inaccuracy is found in an IT or CIS return filed over 6 months late, the inaccuracy penalty must be reduced by the automatic tax-geared failure-to-file penalty charged on the additional liability, and the NPPS2 assessment letter must be dated after the automatic assessment (which can issue up to 10 days after amendment) (CH404450, CH403321).
- Sch.24 para 1/1A penalties on more than one person for the same inaccuracy are capped at 100% of PLR and reduced proportionately (CH404500, CH81125).
- Sch.56 late payment penalties are an exception: they apply independently and must **not** be withdrawn in the way surcharges were cancelled (CH404200, CH404300).
- Historic: TMA 1970 s.59C surcharges were not charged after 2009-10 and were replaced by Sch.56 for balancing payments due on or after 31 January 2012 (CH404425, CH404300). Pre-2010-11 records still need surcharge fields and the discharge logic (assess penalty in full, check the SA system 58 days after the closure notice, discharge the surcharge once the penalty is final — CH404525).
- Double jeopardy: no failure-to-file penalty where the person has been convicted of a criminal offence in respect of the same failure (FA09/Sch55 para 26; CH65100); same for data-holder notices (FA11/Sch23 para 42; CH29890).

**Penalty assessment attributes** (FA09/Sch55 paras 18–19; CH64150): date of assessment, amount, the legislation under which it is assessed, the tax period, and a statement of appeal rights. Time limit: the later of two years beginning with the filing date, and 12 months beginning with the end of the appeal period for the tax assessment (or the date liability is ascertained, or ascertained as nil) (FA09/Sch55 para 19; CH64200). Payment is due within 30 days of issue and the assessment is enforceable as if it were a tax assessment (FA09/Sch55 para 18(2)–(3); CH64300). Sch.56 mirrors this: 30 days to pay, assessment time limit the later of two years from the day before the penalty date and 12 months from the end of the appeal period (FA09/Sch56 paras 11–12; CH156600).

**Reasonable excuse** and **special reduction** are separate flags on the penalty, not one field. Reasonable excuse has no statutory definition, must exist on or before the date of the obligation and throughout the period of default, is judged objectively against a reasonable person with the taxpayer's attributes, and requires the failure to be put right without unreasonable delay after the excuse ends (CH160100, CH160200). Statute treats insufficiency of funds and reliance on a third person as *not* reasonable excuses unless conditions are met (CH160800). Special reduction requires special circumstances, cannot be given without Specialist Technical Team authority, must be considered before issuing any non-automated penalty and on any appeal against an automated penalty whether or not requested, and excludes ability to pay, cross-taxpayer balancing, proportionality arguments, and matters already reflected elsewhere in the penalty scheme (CH170900, CH173000, CH174000, CH175000, CH403265).

**Suspension** applies only to Sch.24 *careless* inaccuracy penalties, requires a SMART condition, has a maximum period of 2 years, and must be entered on NPPS or the penalty cannot later be reinstated (CH405050, CH405070). There is no right of appeal against HMRC's decision to collect a suspended penalty; appeal rights exist only against the decision not to suspend, partial suspension, or the conditions set (CH405050).

### 2.10 Appeal, review and postponement

Appeal attributes: appealed decision reference and type; appellant and capacity; date HMRC issued the decision notice; date of the notice of appeal; grounds of appeal; validity flag; late-appeal state; review state; tribunal state; category; settlement.

The core timings:

| Step | Period | Ref |
|---|---|---|
| Notice of appeal to HMRC | 30 days from the date the decision notice is issued — **date of posting, not receipt** (ARTG2180); ARTG2430/2440 instead say "within 30 days of the date the customer receives" the notice | ARTG2180 vs ARTG2430/2440 |
| HMRC to state its view of the matter after a review request | Within 30 days of the review request, or other reasonable time | s.49B(2) TMA 1970; ARTG2213 |
| Decision maker to submit case to Legal Group review team | 7 calendar days | ARTG2213 |
| Customer to accept a review offer or notify the tribunal | 30 days from the review-offer letter | s.49C TMA 1970; ARTG4220 |
| Review period | 45 days from the date the "view of the matter" letter was sent, unless another period agreed | ARTG2216, ARTG4080, ARTG4690 |
| Notify tribunal after review conclusion | 30 days from the conclusion letter | s.49G(2),(5)(a) TMA 1970; ARTG4820 |
| Notify tribunal where review not completed in time | From the day after the review period expired to 30 days from the date of HMRC's deemed-conclusion letter | ARTG4850 |
| Postponement application | 30 days of the decision or assessment | s.55(3) TMA 1970; ARTG2510 |
| Tribunal referral on a disputed postponement amount | 30 days of HMRC's notification | ARTG2530 |
| s.54 settlement cooling-off | 30 days from the agreement or from written confirmation of a verbal agreement | s.54(2) TMA 1970; ARTG2720 |
| HMRC objection to withdrawal of appeal | 30 days of the withdrawal | ARTG2740 |
| Reinstatement after strike-out | 28 days | ARTG8340 |
| HMRC statement of case (Default Paper) | 42 days from the date the Tribunals Service sent the notice of appeal | ARTG8370 |
| Appellant's reply | 30 days from the date HMRC sent its statement of case | ARTG8370 |

**Note the disagreement in the sources on when the 30 days runs from.** ARTG2180 says the 30-day limit runs from the date HMRC posts the decision notice, and flags this as "a commonly misread point". ARTG2430/ARTG2440 phrase the same limit as 30 days from the date the customer *receives* the formal decision notice. An implementation should store both `notice_issue_date` and, where known, `notice_receipt_date`, and record which basis was used.

Default states matter as much as deadlines. If the customer neither accepts a review offer nor notifies the tribunal within 30 days, the appeal is **treated as settled by agreement** on HMRC's stated view (s.49C(4) TMA 1970; ARTG2730, ARTG4070). The same applies where the tribunal is not notified within 30 days of the review conclusion letter (s.49F TMA 1970). A review conclusion letter treated as a s.54(1) agreement does **not** carry the customer's 30-day withdrawal right (s.49F(3) TMA 1970; ARTG3420) — so the settlement entity needs a `withdrawal_right` boolean rather than an assumed 30 days.

Validity of an appeal is a separate flag from timeliness. Where grounds appear invalid, HMRC must contact the customer, explain why, and seek valid grounds or withdrawal; if the customer maintains invalid grounds, HMRC applies to the tribunal to strike out and the tribunal decides validity (ARTG2171, ARTG2172, ARTG8340). Appealing to the tribunal without first appealing to HMRC leaves the tribunal without jurisdiction and results in a strike-out application (ARTG2440). Late appeals must be accepted where the customer shows a reasonable excuse and appealed without unreasonable delay after it ended (s.49(3) TMA 1970; ARTG2180, ARTG2215) — and the amount of tax involved is explicitly *not* relevant to whether the excuse is reasonable (ARTG2215).

Postponement needs a hard precondition: there must be a valid appeal before tax may be postponed; a postponement application cannot be accepted without one (ARTG2510). Accelerated payment notices override postponement, terminating any existing postponement and preventing new applications for that tax (ARTG2510). Postponed tax paid late still attracts interest (ARTG2560).

Tribunal case category is stored data because it drives procedure: Default Paper (SA and CTSA fixed filing penalties, income tax surcharges, s.93(3) TMA 1970 daily penalty applications), Basic (late filing and late payment including daily penalties; incorrect return penalties under Sch.24 para 15 FA 2007 except where deliberate or where the tax assessment is also appealed), Standard, and Complex (ARTG8350). The tribunal may reallocate at any time (ARTG8340).

### 2.11 Record-keeping obligation

A separate entity because retention periods differ from enquiry windows and carry their own penalty.

| Person / claim | Retention until | Ref |
|---|---|---|
| SA taxpayer, no trade/profession/business | Latest of: first anniversary of 31 January following the year of assessment; completion of any enquiry; end of the day the enquiry window closes | CH14550; TMA70/S12B |
| Trade/profession/business (incl. property letting) | Per CH14530 (period not reproduced in the notes) | CH14550 |
| Company | Latest of 6th anniversary of end of accounting period, completion of enquiry, day enquiry window closes | CH14600; FA98/Sch18 para 21 |
| Direct tax claim not in a return | Later of completion of enquiry into the claim, or the day after the claim enquiry window closes | CH14900; TMA70/Sch1A para 2A |
| PAYE / CIS | 3 years after the end of the tax year | CH14700 |

Where the same record is needed for multiple tax purposes with different periods, the longer applies (CH14100). HMRC may specify shorter periods in writing but never where avoidance is suspected and never for PAYE/CIS records — and CH14100 states no shorter periods have been specified so far. Failure to keep or retain records attracts a penalty (CH11200, CH11500, EM4650, SACM4020).

---

## 3. Lifecycle state machines

### 3.1 Obligation → return

```
(no obligation)
  → notice_issued            trigger: HMRC issues s.8 / s.8A / s.122AA notice   [CH61180]
  → notice_deemed            trigger: voluntary return received on/after 12 Feb 2019, deemed
                                      notice issued on receipt date              [CH820000]
notice_issued
  → filed_on_time            trigger: return received ≤ filing date
  → in_default               trigger: filing date passes; penalty date = filing date + 1 day
                                                                                  [CH61160]
  → notice_withdrawn         trigger: HMRC agrees withdrawal → cancel late filing
                                      penalties; s.7(1B) notification duty revives
                                                                    [CH64280; CH143020]
in_default
  → determination_made       trigger: return >12 months overdue and third-party info
                                      indicates liability above normal pattern; then
                                      wait ≥30 days before contacting the person
                                                                                 [CH401225]
  → filed_late               trigger: return received after filing date
```

Note the interaction at CH401225: a person's failure to file after an under-assessed determination is *not* itself evidence of deliberate withholding, though it may support further enquiry — and if they fail to notify the under-assessment they are liable under Sch.24 para 2 (CH81090).

### 3.2 Payment

```
due → paid_on_time
due → unpaid → penalty_date (due + 31 days for IT/CGT)      [CH155010]
             → penalty_5pct_initial
             → +5 months  → penalty_5pct_second             [CH155140]
             → +11 months → penalty_5pct_third              [CH155160]
unpaid → deferral_agreed   (requested before due date)      [FA09/Sch56 para 10]
deferral_agreed → complied → no penalty for deferral period
deferral_agreed → broken   → penalties as if no deferral, from date of HMRC notice
```

Late payment interest runs in parallel and is unaffected by the penalty state (CH140280).

### 3.3 Enquiry

```
return_filed → enquiry_open        trigger: s.9A / s.12AC notice        [CH23540]
enquiry_open → jeopardy_amended    (appealable to HMRC only; tribunal/review
                                    blocked until closure)              [ARTG2160]
enquiry_open → matter_closed       trigger: PCN issued (needs independent
                                    approving officer; form PCN101)     [CH279600]
enquiry_open → closed              trigger: FCN issued, or contract settlement
enquiry_open → tribunal_directed_pcn  trigger: taxpayer application     [EM2163]
```

### 3.4 Appeal

```
decision_issued
  → appeal_to_HMRC        (30 days; grounds required)                 [ARTG2180]
  → no_appeal → decision stands                                       [ARTG2220]
appeal_to_HMRC
  → grounds_challenged → withdrawn / amended / strike-out application [ARTG2171/2172]
  → discussions
  → review_offered_by_HMRC → (30 days) accepted / tribunal / no reply
        no reply ⇒ settled by agreement on HMRC's view      [s.49C(4) TMA 1970]
  → review_requested_by_customer → HMRC states view within 30 days    [s.49B(2)]
  → notified_to_tribunal (only if HMRC appeal exists first)           [ARTG2410]
review_in_progress (45 days)
  → conclusion_issued → (30 days) tribunal / settled                  [s.49F]
  → period_expired → deemed upheld; HMRC writes; 30-day window        [ARTG4850]
any_state
  → settled_by_s54_agreement (offer + acceptance; verbal must be confirmed in
    writing; 30-day cooling-off)                       [s.54 TMA 1970; ARTG2720]
  → withdrawn (HMRC may object within 30 days)                        [ARTG2740]
tribunal
  → struck_out → 28-day reinstatement window                          [ARTG8340]
  → decided
```

### 3.5 Penalty

```
liability_arises → assessed → paid (30 days)                [FA09/Sch55 para 18]
assessed → amended     trigger: return filed / failure remedied and actual liability
                       known; percentage may be increased for more serious behaviour
                       but never reduced                    [CH64250; CH64150]
assessed → cancelled   trigger: notice to file withdrawn    [FA09/Sch55 para 17A]
assessed → suspended   (Sch.24 careless only; SMART condition; ≤2 years)   [CH405070]
suspended → cancelled  trigger: conditions met at end of period
suspended → collected  trigger: condition breached or another careless inaccuracy
                       penalty during the period; no appeal against collection
                                                                       [CH405050]
assessed → appealed    → review / tribunal (may vary amount; on special reduction
                        only where HMRC's decision was "flawed" on judicial review
                        principles)                    [FA09/Sch55 para 22(4); CH64600]
```

---

## 4. Reference data to version by tax year

The notes are explicit that helpsheet figures are year-specific: "figures … apply for the relevant tax year and should not be assumed to apply to other years" (HS236). Every item below needs `(value, tax_year_from, tax_year_to, ref)`.

### 4.1 Dates and deadlines

| Item | Value | Ref |
|---|---|---|
| Paper filing date (2010-11) | 31 October 2011 | CH61120 |
| Electronic filing date (2010-11) | 31 January 2012 | CH61120 |
| POA due dates | 31 January in year; 31 July following | CH142260 |
| Balancing payment due date | 31 January following end of tax year | CH142260, CH155010 |
| Late-issued notice payment due date | 3 months from date of s.8 notice (notice after 31 October following the year) | CH140220 |
| IT/CGT penalty date | Due date + 31 days (3 March; 2 March in a leap year) | CH155010 |
| Notification of chargeability (IT/CGT) | 5 October following the end of the tax year | CH71220, CH71280 |
| Notification of an under-assessment | 30 days from the assessment date | FA07/Sch24 para 2; CH81170 |
| Pension savings statement | By 6 October 2026 for 2025-26 | HS345 |
| NIC agreement deduction cut-off | NICs paid to employer before 5 June following the tax year of the share transaction | HS305 |
| Non-resident UK residential property disposal notification | Within 30 days of conveyance | HS264 |
| SWT set-off deemed remittance date | Normally 31 January following the tax year | HS264 s.2.2 |

### 4.2 Rates, thresholds and penalty parameters

| Item | Value | Period | Ref |
|---|---|---|---|
| Sch.55 initial fixed penalty | £100 | — | CH63540 |
| Sch.55 daily penalty | £10/day, max 90 days, from 3 months after penalty date | — | CH62120 |
| Sch.55 6-month / 12-month floor | £300 (CIS: £1,500 deliberate, £3,000 deliberate and concealed) | — | CH63580, CH63640 |
| Sch.56 IT/CGT penalty tiers | 5% + 5% + 5% at penalty date, 5 months, 11 months | Balancing payments due on/after 31 Jan 2012 | CH155010 |
| Sch.24 maxima | 30% / 70% / 100% of PLR; 30% under-assessment; 100% third-party | — | CH82120 |
| Offshore 12-month maxima | 100/150/200% (concealed); 70/105/140% (deliberate); 5% otherwise | Table splits at filing date 24 July 2013 | CH112600, CH112400 |
| Disclosure weightings | Telling 30%, helping 40%, access 30% (+ additional information for offshore, 2016-17 on) | — | CH63220, CH117000 |
| Significant-period restriction | Normally >3 years; max reduction 10 percentage points above minimum | Disclosures after 5 Sep 2016 | CH63310 |
| PAYE late payment de minimis | £100 or less difference | — | CH152175 |
| Limit on income tax reliefs | Greater of £50,000 and 25% of adjusted total income | 2025-26 and later (from 6 April 2013) | HS204 s.1.1 |
| Threshold requiring ATI calculation | Total income over £200,000 | — | HS204 s.3.1 |
| Share loss / income loss cap | £50,000 or 25% of income if greater (not for EIS/SEIS share loss relief) | 2013-14 onwards | HS286 |
| Payroll Giving relief cap | Greater of £50,000 or 25% of adjusted total income | — | HS342 s.4 |
| Gift Aid grossing factor | 100/80 (basic rate 20%) | — | HS342 s.1 |
| Pension annual allowance | £60,000 | 2025-26 | HS345 |
| Money purchase annual allowance | £10,000 | 2025-26 | HS345 |
| Alternative annual allowance | £50,000 | 2025-26 | HS345 |
| Threshold / adjusted income | £260,000; taper £1 per £2 above; floor £10,000 | 2025-26 | HS345 |
| DB opening value multiplier / uprating | ×16; +3.1% | — | HS345 |
| AA charge rates | 45% / 40% / 20% (may differ for Scottish or Welsh taxpayers) | — | HS345 |
| Overseas transfer charge | 25% of transferred value; applies to transfers requested on/after 9 March 2017 | — | HS345 |
| Unauthorised payments charge / surcharge | 40%; +15%; surcharge threshold 25% of rights | — | HS345 |
| Short service refund | 20% on first £20,000; 50% above | 2025-26 | HS345 |
| EIS relief rate and caps | 30%; £2m (£1m non-KIC) | 2025-26 | HS341 |
| SEIS caps | IT relief £200,000; reinvestment relief 50% capped at £100,000; AEA £6,000; 3-year holding | 2025-26 | HS393 |
| CITR | 5% per year for 5 years, 25% total | — | HS237 |
| TRF charge rate | 12% (2025-26, 2026-27); 15% (2027-28) | 2025-26 to 2027-28 | HS264 s.4 |
| Qualifying care relief | £19,690 fixed; £415/week under 11; £495/week 11+ and adults | Per HS236 (2026 version) | HS236 s.2 |
| Trading and miscellaneous income allowance | £1,000 | From 6 April 2017 | HS325 |
| Termination payment exemption | £30,000 | — | HS325 |
| AIS small holdings exemption | £5,000 nominal | — | HS343 s.6 |
| Qualifying / RRQP premium limit | £3,600 per year | — | HS320 s.1.1, s.9.2 |
| SA registration threshold (chargeable event gains plus other savings/investment income) | £10,000 | — | HS320 s.6.1, HS321 s.6.1 |
| PPB gain formula | 15% × (A + B − C) | — | HS320 s.14 |
| Part surrender deferred allowance | 5% of premiums, max 100% over 20 years | — | HS320 s.13 |
| FHL occupancy conditions | Pattern 155 days; availability 210 (140 for 2011-12 and earlier); letting 105 (70 for 2011-12 and earlier) | To end of 2025 tax year | HS253 |
| Averaging trigger | Lower year's profit <75% of the other, or one year nil | — | HS234 s.4 |
| ESS CGT exemption / lifetime cap / material interest | £50,000; £100,000 (agreements from 17 March 2016); 25% | — | HS287 |
| Employment-related loan de minimis | £10,000 | — | HS305 WS8 |
| Market value artificial reduction/enhancement threshold | >10% (10% for depressed value); 7-year look-back | — | HS305 |
| Dividend allowance (as stated for remitted-dividend context) | £500 | 2024-25 | HS264 |

### 4.3 Lookup tables and enumerations

- **Territory categories 1/2/3**, effective-dated by Treasury Order, with "not listed ⇒ category 2" as the default and the UK in category 1 (CH403145, CH403147, CH112400).
- **Penalty models 1–4** mapped to return types (CH62020).
- **Interest-regime applicability by tax and date** (CH140160) — a mandatory pre-check before any interest calculation.
- **Assessment time-limit regime by assessment date** (4 vs 6 years from 1 April 2010; SI 2009/403).
- **Penalty-regime commencement by tax** (Sch.24 from 1 April 2009/period 2008; Sch.41 from 1 April 2010, IT/CGT first period 2009-10; Sch.55 for SA returns from year ended 5 April 2011) (CH81012, CH71120, CH61120).
- **Return and supplementary page codes** (SA100/101/102/103S/103F/103L/104S/104F/105/106/107/108/109/110; SA900/904) and **disposal type codes** ('OTH', 'MUL', 'NVC') (HS204, HS286, HS292, HS393).
- **Tribunal case categories** (ARTG8350).
- **Behaviour, disclosure and concealment enumerations** shared across Sch.24/41/55 (CH402050).

### 4.4 Effective-dated rule switches

The notes contain many rules whose applicability turns on a date rather than a tax year, and each needs storing as a switch:

| Switch | Date | Ref |
|---|---|---|
| Remittance basis abolished; FIG regime begins | 6 April 2025 | HS264, HS266 |
| TRF window | 6 April 2025 for 3 years | HS264 s.4 |
| Voluntary returns deemed made under notice | 12 February 2019 | CH820000 |
| Partial closure notices available | Finance (No.2) Act 2017 | CH279600 |
| Avoidance-arrangement reasonable care presumption | Documents submitted on/after 16 November 2017, period beginning on/after 6 April 2017 and ending after 15 November 2017 | CH81122 |
| Offshore "additional information" disclosure element | 2016-17 onwards | CH63220 |
| Offshore penalty ranges change | 2015-16 / 2016-17 boundary | CH112700 |
| Offshore category tables split | Filing date before vs on/after 24 July 2013 | CH112400 |
| Sch.56 replaces s.59C surcharges | Balancing payments due on/after 31 January 2012 | CH404425 |
| Restricted securities post-acquisition charges | Acquired on/after 16 April 2003 | HS305 |
| EMI disqualifying event window | 90 days (40 days before 17 July 2013) | HS305 |
| Non-UK charity reliefs cease | After 5 April 2024 | HS342 |
| Mixed fund cleansing window | 6 April 2017 – 5 April 2019 | HS264 |
| Breathing Space regulations | From 4 May 2021 | CH140320 |

---

## 5. Cross-cutting design notes

**Interest and penalties are computed on different bases and must not share a single "amount due" field.** Penalties under Sch.55 are geared to "the liability that would have been shown in the return" — net of tax deducted at source but **not** reduced by amounts already paid towards it (CH63560). Interest is geared to the amount unpaid from the due date. Sch.24 penalties are geared to PLR. Sch.41 penalties are geared to PLR with tax-specific definitions: for IT/CGT, PLR is the tax unpaid at 31 January next following the tax year, or — where a notice to file was withdrawn — the later of 30 days from the day after withdrawal, 31 January following the tax year, and the day after a refund of a payment on account was issued (FA08/Sch41 para 7(2); CH72700).

**Tax-geared penalties are provisional until the liability is known.** Where a return remains unfiled, HMRC estimates liability "to the best of information and belief" using prior years, VAT returns and industry knowledge, then amends the penalty once the return is filed (CH63560, CH64250). If the liability is later increased on enquiry, the 6- and 12-month penalties are increased and Sch.24 inaccuracy penalties are also considered (CH63560, CH65060). The percentage set in an original tax-geared assessment can be increased for more serious behaviour but never reduced (CH64150).

**Partnership penalties fan out to partners.** A late partnership return makes the penalty payable by every partner, and an appeal brought by the representative partner (or successor) covers all partners (FA09/Sch55 paras 20, 25; CH64540). For income tax, CGT and corporation tax the partnership itself has no penalty liability for failure to pay on time — liability is shared among the relevant partners (CH156600).

**Multiple categories mean multiple failures.** Where withheld information falls into more than one offshore category, the failure is treated as separate failures per category, with tax liability apportioned on a just and reasonable basis and penalties calculated separately (CH112500, CH112800, CH114100).

**Audit fields are part of the domain, not just logging.** The notes require: authorisation records for extended-time-limit assessments (CH53300); Specialist Technical Team authority for special reduction with reasons recorded (CH175000, CH403265); independent-officer approval and retained form PCN101 for partial closure notices (CH279600); the compliance-check case identifier in the SA system's Case Summary free-format notes, with removal of user interest on completion and cancellation of the EIP signal on closure (CH206275); and recording of penalty decisions including "No"/"Nil" outcomes with the reason selected and approval recorded (CH407500, CH407620).

---

## 6. Gaps in the sources

The brief asks for a full head-of-duty data model; the notes do not support several parts of it.

- **Core rates and allowances.** The notes give no income tax rate bands, no personal allowance for years other than an example figure of £12,570 used illustratively for 2024-25 and 2025-26 (HS286 Example 6), no dividend or savings rates other than incidental mentions in a remittance context (20/40/45% and 8.75/33.75/39.35% at HS264), no NIC rates or Class 2/Class 4 thresholds, and no CGT rates. The current CGT annual exempt amount is given only as £6,000 for 2025-26 in HS393 s.3.2, which cannot be reconciled against other sources here.
- **Current-year filing deadlines.** Only the 2010-11 dates (31 October 2011 / 31 January 2012) appear as concrete filing dates (CH61120). The general "31 October paper / 31 January electronic" pattern is implied but never stated as a rule in the notes.
- **Registration and notification mechanics.** The notes state the s.7 notification duty and the 5 October deadline (CH71220) but do not give the criteria for who must register, the content of a registration, or how a UTR is issued.
- **Payments on account: the trigger.** The notes describe POAs as "based on the previous year's liability" (CH142240) but give neither the de minimis threshold below which POAs are not required nor the proportion-of-liability-deducted-at-source test.
- **Amendment windows.** The taxpayer's window to amend a return is referred to only obliquely ("time limit for amending tax return (not specified in chunk)", HS234 s.12). HMRC's correction power is referenced (CH143020) without its time limit.
- **Record retention for business taxpayers.** CH14550 defers to CH14530 and CH14510 for the trade/profession/business and general IT/CGT periods, and those pages are not in the notes.
- **Discovery assessment conditions.** TMA 1970 s.29(4)/(5) is cited (CH23540) but the substantive conditions for a valid discovery assessment, and the "officer could not have been reasonably expected to be aware" protection, are not set out.
- **Repayment mechanics and overpayment relief.** Repayment interest is covered in detail, but the notes do not describe how repayments are claimed, the overpayment relief regime, or nomination of repayments (beyond a passing mention of HVAs receiving repayments as nominee, CH820000).
- **MTD for Income Tax.** Repeatedly flagged as replacing SA boxes with software-based claims and quarterly updates (HS204, HS237, HS264, HS266, HS325, HS340, HS341, HS342, HS343), and as exempting qualifying care recipients for 2026-27 (HS236), but no rules on mandation thresholds, quarterly update deadlines, or how quarterly updates relate to the annual return.
- **Simple assessment.** Appeal restrictions and the 4-year assessment limit are given (ARTG2040, CH56100), but not the conditions under which HMRC may issue one instead of a notice to file, or its content.
- **Withheld manual content.** Several relevant pages are noted as withheld under FOIA exemptions or moved to internal systems — CH500000, CH920000, CH930000, CH290000, parts of CH206250, CH206225, CH279600, CH73180, CH81195, CH402252, and content on bankruptcy and appeal standing at ARTG2150. Guidance in those areas is therefore incomplete in the notes.
- **Archived/superseded pages.** CH171000 (special reduction) is archived; CH402150 (evasion) contains no content; CH402330 and CH402336/CH402338 are marked "under review" as duplicated elsewhere. Any implementation citing them should treat them as unstable.
- **Conflicting basis for the appeal clock.** As noted in §2.10, ARTG2180 (posting) and ARTG2430/2440 (receipt) state the 30-day appeal period differently. The notes do not resolve which governs.

---

## Sources used on this page

This page was written by an LLM from structured notes extracted from the mirrored sources below. Always check the upstream source before relying on any figure or deadline.

- [govuk-sa-detailed-information](https://www.gov.uk/government/collections/self-assessment-detailed-information) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/govuk-guidance.md`
- [sa-helpsheets:5f67dfee-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/accrued-income-scheme-hs343-self-assessment-helpsheet) - 2 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/accrued-income-scheme-self-assessment-helpsheet-hs343.md`
- [sa-helpsheets:5f67ceae-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/averaging-for-creators-of-literary-or-artistic-works-hs234-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/averaging-for-creators-of-literary-or-artistic-works-self-assessment-helpsheet-hs234.md`
- [sa-helpsheets:5f67d41e-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/employee-share-and-security-schemes-and-capital-gains-tax-hs287-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/capital-gains-tax-and-employee-share-schemes-self-assessment-helpsheet-hs287.md`
- [sa-helpsheets:5f67d5b1-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/land-and-leases-the-valuation-of-land-and-capital-gains-tax-hs292-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/capital-gains-tax-land-and-leases-self-assessment-helpsheet-hs292.md`
- [sa-helpsheets:5f67ddc2-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/charitable-giving-hs342-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/charitable-giving-tax-relief-self-assessment-helpsheet-hs342.md`
- [sa-helpsheets:5f67cf48-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/community-investment-tax-relief-hs237-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/community-investment-tax-relief-self-assessment-helpsheet-hs237.md`
- [sa-helpsheets:5f67dc31-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/employee-shares-and-securities-further-guidance-hs305-self-assessment-helpsheet) - 3 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/employment-related-shares-and-securities-self-assessment-helpsheet-hs305.md`
- [sa-helpsheets:5f67de13-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/enterprise-investment-scheme-income-tax-relief-hs341-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/enterprise-investment-scheme-income-tax-relief-self-assessment-helpsheet-hs341.md`
- [sa-helpsheets:f689f4a2-7da1-41a3-b37d-b18c346219ed](https://www.gov.uk/government/publications/foreign-income-and-gains-fig-regime-self-assessment-helpsheet-hs266) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/foreign-income-and-gains-fig-regime-self-assessment-helpsheet-hs266.md`
- [sa-helpsheets:5f67e2d6-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/furnished-holiday-lettings-hs253-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/furnished-holiday-lettings-self-assessment-helpsheet-hs253.md`
- [sa-helpsheets:5f67db85-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/gains-on-foreign-life-insurance-policies-hs321-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/gains-on-foreign-life-insurance-policies-self-assessment-helpsheet-hs321.md`
- [sa-helpsheets:5f67dcd2-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/gains-on-uk-life-insurance-policies-hs320-self-assessment-helpsheet) - 4 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/gains-on-uk-life-insurance-policies-self-assessment-helpsheet-hs320.md`
- [sa-helpsheets:5f67dd70-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/interest-and-alternative-finance-payments-eligible-for-relief-on-qualifying-loans-and-alternative-finance-arrangements-hs340-self-assessment-helpshee) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/interest-and-alternative-finance-payments-eligible-for-relief-on-qualifying-loans-and-alternative-finance-arrangements-self-assessment-helpsheet-hs340.md`
- [sa-helpsheets:5f67e282-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/limit-on-income-tax-reliefs-hs204-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/limit-on-income-tax-reliefs-self-assessment-helpsheet-hs204.md`
- [sa-helpsheets:5f67d46f-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/negligible-value-claims-and-income-tax-losses-on-disposals-of-shares-you-have-subscribed-for-in-qualifying-trading-companies-hs286-self-assessment-he) - 2 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/negligible-value-claims-and-income-tax-losses-on-disposal-of-shares-self-assessment-helpsheet-hs286.md`
- [sa-helpsheets:5f67dbe3-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/other-taxable-income-hs325-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/other-taxable-income-for-self-assessment-helpsheet-hs325.md`
- [sa-helpsheets:5f67cefb-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/remittance-basis-hs264-self-assessment-helpsheet) - 4 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/paying-tax-on-the-remittance-basis-self-assessment-helpsheet-hs264.md`
- [sa-helpsheets:5f67defe-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/pensions-tax-charges-on-any-excess-over-the-lifetime-allowance-annual-allowance-special-annual-allowance-and-on-unauthorised-payments-hs345-self) - 5 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/pension-savings-tax-charges-self-assessment-helpsheet-hs345.md`
- [sa-helpsheets:5f67cd23-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/qualifying-care-relief-foster-carers-adult-placement-carers-kinship-carers-and-staying-put-carers-hs236-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/qualifying-care-relief-for-carers-self-assessment-helpsheet-hs236.md`
- [sa-helpsheets:5f67e327-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/seed-enterprise-investment-scheme-income-tax-and-capital-gains-tax-reliefs-hs393-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/seed-enterprise-investment-scheme-income-tax-and-capital-gains-tax-reliefs-self-assessment-helpsheet-hs393.md`
- [hmrc-manual-artg](https://www.gov.uk/hmrc-internal-manuals/appeals-reviews-and-tribunals-guidance) - 11 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/artg.md`
- [hmrc-manual-ch](https://www.gov.uk/hmrc-internal-manuals/compliance-handbook) - 64 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/ch.md`
