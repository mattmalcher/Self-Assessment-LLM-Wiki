---
title: HMRC's published interpretation - manuals, SPs, briefs and concessions
generated: true
generated_on: '2026-09-09'
generated_by: claude-cli:opus
input_hash: 3de4e95122eef7cb
note_count: 70
sources:
- hmrc-manual-artg
- hmrc-manual-ch
- hmrc-manual-em
- hmrc-manual-salf
- hmrc-manual-sam
- hmrc-manuals-index
- sa-helpsheets:5f67dcd2-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67defe-7631-11e4-a3cb-005056011aef
---

# HMRC's published interpretation - manuals, SPs, briefs and concessions

!!! danger "Unofficial - not HMRC, not advice, written by an LLM"

    This page is **not** an HMRC publication and has no connection to HMRC or
    any government body. It was **written by a language model** from mirrored
    source material, and can be wrong, incomplete or out of date. It is not
    tax advice. Check every figure, date and rule against the cited source
    before relying on it, and see
    [GOV.UK](https://www.gov.uk/self-assessment-tax-returns) for official
    guidance.

This page is an unofficial guide to the different kinds of material HMRC publishes about Self Assessment - internal manuals, Statements of Practice, concessionary practice and customer-facing guidance - and to how much weight each carries. It sets out what binds whom, how to reason about a conflict between a manual and the statute, and which HMRC publications actually bear on Self Assessment. The source notes behind this page are heavily weighted towards manuals; the coverage of Statements of Practice is thin and there is none at all on Revenue & Customs Briefs or Extra-Statutory Concessions as a category, so a "Gaps in the sources" section at the end says so explicitly.

## 1. The categories, and what each one is

| Category | What it is | Who it binds | Weight for a taxpayer or an implementer |
|---|---|---|---|
| Internal manuals (SAM, SALF, EM, ARTG, CH, etc.) | Instructions written by HMRC for its own officers, published on GOV.UK in an A–Z index ([HMRC manuals index](https://www.gov.uk/government/collections/hmrc-manuals)) | HMRC officers operationally. A review officer, for instance, "has no discretion to depart from current policy/practice without prior approval" (ARTG4070/ARTG4080) | HMRC's stated interpretation and practice, not law. Published incompletely (see §3) |
| Statements of Practice | HMRC's published interpretation of a statutory test | HMRC | Explanatory. SP 01/2001 supplies the factors used to apply the statutory "independent agent" condition in FA95/S127(3) (SALF, Investment managers) |
| Revenue & Customs Briefs | — | — | Not covered in the source notes |
| Extra-Statutory Concessions | — | — | Not covered as a formal category, though concessionary practice appears inside SAM (see §4) |
| Customer-facing guidance (helpsheets, factsheets, forms) | Simplified public material, e.g. HS320, HS345, CC/FS7a, CC/FS9, CC/FS13, form SA353 | Nobody | Deliberately partial. HS320 states it covers "the most common circumstances only" and directs complex cases to the Insurance Policyholder Taxation Manual (HS320) |

Statute is the operative layer throughout. The manuals themselves are structured around it: SALF802 explains that the term "assessment" in the Taxes Acts covers both self assessments (returns under TMA 1970 s.9, amendments under s.9ZB/s.9C/s.28A, determinations under s.28C) and HMRC assessments (discovery assessments under s.29) - a statement about how legislation is construed, not a rule HMRC creates.

## 2. Which manuals bear on Self Assessment

| Manual | Scope relevant to SA |
|---|---|
| Self Assessment Manual (SAM) | Return issue and SA316 notices, filing dates, penalties, repayments, enquiry record-keeping, Scottish/Welsh taxpayer status (Note: SAM is largely system-and-process guidance for HMRC staff) |
| Self Assessment: the legal framework (SALF) | Construction of statutory terms, time limits, Making Tax Digital digital obligations and exemptions (SALF1500 onwards) |
| Self Assessment Claims Manual | Claims within and outside returns (listed in the manuals index) |
| Enquiry Manual (EM) | Opening and running enquiries, factsheets, determinations under TMA 1970 s.28C, contract settlements (EM6214 onwards) |
| Appeals, Reviews and Tribunals Guidance (ARTG) | Appeal rights, reviews, postponement under TMA 1970 s.55(3), tribunal procedure |
| Compliance Handbook (CH) | Record-keeping, information notices under FA08/Sch36, penalties (FA09/Sch55 and Sch56), interest (FA09), reasonable excuse, special reduction |
| Scottish / Welsh Taxpayer Technical Guidance | Devolved taxpayer status |
| Trusts, Settlements and Estates; Savings and Investment | Related income sources |

SAM, EM, ARTG and CH also cross-refer constantly to further manuals - Collection of Student Loans (CSLM8575), Debt Management and Banking (DMBM), Pensions Tax (PTM051100), Insurance Policyholder Taxation (IPTM), Residence Domicile and Remittance (RDRM), Employment Status (ESM) - so a question that starts in SA rarely stays in one manual.

## 3. Structural limits on the manuals

**They are published with holes.** Very large amounts of manual text are withheld under Freedom of Information Act 2000 exemptions. Examples in the SA area: HMRC's determination strategy and the Method 2 calculation stages in the Enquiry Manual (EM, determinations); the special reduction guidance at CH124660; parts of the surcharge appeal decision criteria at SAM62020/SAM62021; parts of SAM110227 and CH206250. An implementer cannot assume the published text is the whole of HMRC's operating rule.

**They move.** CH500000 has been taken off GOV.UK to internal HMRC systems, with the public-facing equivalent being factsheet CC/FS13 (CH, index).

**They are dated in place.** Manual pages routinely carry rules that applied only to particular years - SAM62020 covers surcharge appeals for 2009-10 and earlier, with different rules from 2010-11 (SAM61200 onwards); the Scottish rate tables in SAM are year-by-year and the 2024-25 table introduces an Advanced rate of 45% that does not exist in earlier years' structures.

**They are written for officers.** Much of SAM is system-function guidance (CREATE SUNDRY CHARGE, MAINTAIN STANDOVERS, VIEW COMPLIANCE SUMMARY) with no direct taxpayer-facing content at all.

## 4. Concessionary practice inside the manuals

Where the source notes show concessions, they are stated inside SAM rather than as a separate published ESC, and SAM itself flags them as concessions rather than law:

| Practice | Condition | Effect | Status per the manual |
|---|---|---|---|
| Late-issued return filing/payment date | Paper return or SA316 issued after 31 October following the end of the return year **and** "Not Failure to Notify" applies | Filing/payment date becomes 3 months and 7 days after the date of issue of the return | Described as "by concession" (SAM120070) |
| Same case, but Failure to Notify applies | Return issued after 31 October and taxpayer did not notify chargeability by 5 October following the tax year end | Relevant date for balancing-payment interest stays at 31 January | (SAM120070) |
| Effective Date of Payment on a balancing charge credit | Overpayment arises from a captured return; return received before the filing date | EDP may be amended from the default filing date (31 January following the tax year end) to the logged receipt date | Described as a concession, "not a strict legal rule" (SAM, Balancing charge credits and freestanding credits) |
| Informal standover of penalties and surcharges under appeal | Appeal against a penalty or surcharge | Payment stood over pending settlement | Pure policy: the notes state there is **no** formal statutory right of postponement for penalties or surcharges; only informal standover by HMRC policy (ARTG2510; ARTG2570) |

Machine-implementable form of the first two rules:

```
inputs: return_issue_date, tax_year_end, failure_to_notify (bool)
if return_issue_date > 31 October following tax_year_end:
    if not failure_to_notify:  filing_and_payment_date = return_issue_date + 3 months + 7 days
    else:                      interest_relevant_date  = 31 January following tax_year_end
else: standard dates (31 October paper / 31 January online)
```

A related non-statutory tolerance: SAM62020 records a five-day administrative allowance on surcharge appeals for 2009-10 and earlier, so that the statutory 30 days from the date of the notice is operated as 35 days from the date the surcharge was imposed on the SA record. SAM62020 is explicit that the extra five days are an administrative allowance and not part of the statutory period.

## 5. Statements of Practice

Only one appears in the source notes. SP 01/2001 supplies the factors HMRC uses to decide whether an investment manager meets the statutory "independent agent" condition in FA95/S127(3) and FA2003/Sch26/Para 3 - including the view that services to the non-resident and connected persons are not a "substantial part" of the business where they do not exceed 70%, by fees or another appropriate measure (SALF, Investment managers). SALF records that the list of factors is "not exhaustive" and that cases outside the listed categories are considered on their own facts - which is the characteristic shape of an SP: a safe harbour, not a statutory boundary.

## 6. Reading a conflict between a manual and the statute

The source material does not contain any general statement of legal doctrine on when HMRC guidance can be relied on. What it does contain is several worked examples of manual text that is narrower, wider or simply different from the law, which suggest the following order of resolution:

1. **Start with the statutory text.** Where the manual and the statute both speak, the manual is describing the statute. ARTG2180 sets the 30-day appeal window and ARTG2160 lists appealable decisions, but ARTG2160 says the list "is not exhaustive" - a manual list is evidence of scope, not the definition of it.
2. **Identify whether the manual rule has a statutory anchor at all.** If it does not - "by concession", "HMRC policy is to informally stand over" - it is practice, and the statutory position is the fallback if the practice is not applied.
3. **Check whether a tribunal has already read the statute differently.** CH173000 records that the Upper Tribunal in *Barry Edwards* held that "special circumstances" is "not to be given a restrictive interpretation", and CH160100 records that "the law does not require a reasonable excuse to be based on an unforeseeable or inescapable event", with HMRC guidance saying to avoid that phrase. Both are instances of the manual being amended to follow the courts.
4. **Note where HMRC's constraints do not bind the decision-maker of last resort.** ARTG2215 records that HMRC must accept a late appeal where the customer had a reasonable excuse and did not delay unreasonably (TMA 1970 s.49(3)), but that the tribunal, unlike an HMRC decision maker, is not limited by those conditions and can accept a late appeal in the interests of justice. Similarly, CH156600 records that the tribunal can substitute a different special reduction only where it considers HMRC reached a "flawed decision".
5. **Treat HMRC's illustrative lists as illustrative.** CH160300's reasonable excuse examples are described as "illustrative only, not model answers or guaranteed outcomes" (CH160100). By contrast, statute itself excludes insufficiency of funds and reliance on a third person unless specified conditions are met (CH160800) - that exclusion is legislative, not editorial.

Practical test for an implementer: if a rule can be traced to a section number, code the section and use the manual for interpretation. If it can only be traced to a manual paragraph, code it as a configurable policy parameter, not a constraint.

## 7. Customer-facing guidance

Helpsheets and factsheets are the most simplified layer and are explicitly bounded. HS320 states it covers only the most common circumstances and refers complex cases (purchased life annuities, capital redemption policies) to IPTM. HS345 gives 2025-26 annual allowance figures - £60,000 standard, £10,000 money purchase, £50,000 alternative, £260,000 high-income threshold, tapering at £1 per £2 with a £10,000 floor - and warns that the figures apply to that year only and that the annual allowance calculator cannot be used for all arrangement types.

Factsheets carry procedural weight in enquiries even though they are not law. EM1605 requires an officer to issue the relevant general information factsheet on opening an enquiry, and the relevant penalty factsheet (CC/FS7a, CC/FS11, CC/FS15, CC/FS18(a/b) or CC/FS19) once there is reason to believe a penalty may be due, together with the Human Rights Act message and CC/FS9 where ECHR Article 6 penalties may apply (EM1605; CH300500). Form SA353, issued with a surcharge notice, carried HMRC's guidance on what would likely be accepted as a reasonable excuse (SAM62020).

## Gaps in the sources

The supplied notes do not cover, and this page therefore does not state:

- **Revenue & Customs Briefs** - no note mentions one, so nothing can be said about their status, frequency, or which ones bear on Self Assessment.
- **Extra-Statutory Concessions as a formal published category** - the notes contain concessionary *practice* recorded in SAM (§4) but nothing on the ESC series itself, its numbering, its legislative footing, or the enactment of ESCs into statute.
- **The legal weight of guidance generally** - no note addresses legitimate expectation, judicial review of HMRC guidance, or the consequences of a taxpayer relying on incorrect manual text.
- **Statements of Practice beyond SP 01/2001** - the notes contain no SP index and no other individual SP.
- **How HMRC versions or archives manual pages**, beyond the observations that CH171000 is archived and CH500000 has been moved off GOV.UK.
- **The status of HMRC's toolkits** - CH279500 is titled "Recommending toolkits to help reduce errors", but the note gives no statement of what weight a toolkit carries.

---

## Sources used on this page

This page was written by an LLM from structured notes extracted from the mirrored sources below. Always check the upstream source before relying on any figure or deadline.

- [sa-helpsheets:5f67dcd2-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/gains-on-uk-life-insurance-policies-hs320-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/gains-on-uk-life-insurance-policies-self-assessment-helpsheet-hs320.md`
- [sa-helpsheets:5f67defe-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/pensions-tax-charges-on-any-excess-over-the-lifetime-allowance-annual-allowance-special-annual-allowance-and-on-unauthorised-payments-hs345-self) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/pension-savings-tax-charges-self-assessment-helpsheet-hs345.md`
- [hmrc-manual-artg](https://www.gov.uk/hmrc-internal-manuals/appeals-reviews-and-tribunals-guidance) - 14 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/artg.md`
- [hmrc-manual-ch](https://www.gov.uk/hmrc-internal-manuals/compliance-handbook) - 31 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/ch.md`
- [hmrc-manual-em](https://www.gov.uk/hmrc-internal-manuals/enquiry-manual) - 3 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/em.md`
- [hmrc-manuals-index](https://www.gov.uk/government/collections/hmrc-manuals) - 1 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/index.md`
- [hmrc-manual-salf](https://www.gov.uk/hmrc-internal-manuals/self-assessment-legal-framework) - 2 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/salf.md`
- [hmrc-manual-sam](https://www.gov.uk/hmrc-internal-manuals/self-assessment-manual) - 17 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/sam.md`
