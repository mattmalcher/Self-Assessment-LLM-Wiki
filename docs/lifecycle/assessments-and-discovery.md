---
title: Assessments, discovery and time limits
generated: true
generated_on: '2026-09-08'
generated_by: claude-cli:opus
input_hash: 97647c241799c37a
note_count: 80
sources:
- hmrc-manual-artg
- hmrc-manual-ch
- hmrc-manual-em
- hmrc-manual-salf
- sa-helpsheets:5f67ceae-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67d46f-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67e2d6-7631-11e4-a3cb-005056011aef
- sa-helpsheets:5f67e327-7631-11e4-a3cb-005056011aef
- tma-1970
---

# Assessments, discovery and time limits

!!! danger "Unofficial - not HMRC, not advice, written by an LLM"

    This page is **not** an HMRC publication and has no connection to HMRC or
    any government body. It was **written by a language model** from mirrored
    source material, and can be wrong, incomplete or out of date. It is not
    tax advice. Check every figure, date and rule against the cited source
    before relying on it, and see
    [GOV.UK](https://www.gov.uk/self-assessment-tax-returns) for official
    guidance.

This page covers what HMRC can do after a Self Assessment return is filed late, wrongly, or not at all: determinations under s.28C TMA 1970 where no return arrives, discovery assessments under s.29 TMA 1970 and the two gateway conditions in s.29(4) and s.29(5), and the ladder of assessing time limits keyed on taxpayer behaviour (4 / 6 / 12 / 20 years). It also covers the "staleness" argument rejected by the Supreme Court in *HMRC v Tooth*, and the related question of protective assessments. It is an unofficial, independent reference; HMRC's manual positions are attributed as HMRC's view, not stated as law.

---

## 1. The three routes HMRC has to a figure

| Route | Statute | When available | Appealable? |
|---|---|---|---|
| Enquiry into a filed return, closed by closure notice | TMA 1970 s.9A (individuals/trustees); s.12AC (partnerships); Sch 1A (claims) | Within the enquiry window; one enquiry per return only (s.9A(3), s.12AC(3), Sch 1A para 5(3)) | Yes, against the closure notice conclusions |
| Determination where no return filed | TMA 1970 s.28C | Notice to file issued, return not delivered by the filing date | **No** — no right of appeal and no postponement (EM, "Considering whether a determination is appropriate") |
| Discovery assessment | TMA 1970 s.29 (individuals); s.30B (partnership statements); Sch 18 FA 1998 paras 41–45 (companies) | Enquiry window passed or closed, or no return filed, and s.29(3) conditions met | Yes; objection to a time-barred assessment can *only* be made by appeal (s.34(2)) |

The single enquiry rule means a return, amendment or claim can be enquired into once only; even a completed in-window enquiry bars a fresh enquiry into the same return (TMA 1970 s.9A(3)). Discovery is the exception route, not a second bite (EM1530).

HMRC's internal ordering preference: open an enquiry wherever possible rather than use discovery (EM3201); issue a determination rather than a discovery assessment where a notice to file has been issued but no return submitted and the time limits permit (EM3202).

---

## 2. Determinations where no return is filed

**Trigger.** A notice to file under s.8 or s.8A TMA 1970 has been given, and the return has not been delivered by the filing date. An officer may then determine the tax due "to the best of their information and belief" (s.28C(1A) TMA 1970).

**Time limit.** Three years beginning with the statutory filing date for the return (TMA 1970 s.28C(5); CH52100). CH52100's worked example: the 2012-13 filing date gives a determination deadline of 30 January 2017.

**Statutory filing date for this purpose.** 31 January after the year of assessment, or three months after the return/notice is given if issued later than 31 October following the year of assessment (EM, "Considering whether a determination is appropriate"). The earlier 31 October paper deadline is *not* used when computing determination time limits (same source).

**Displacement.** A self assessment delivered later supersedes the determination if made within the later of (a) three years from the filing date and (b) 12 months from the date of the determination (TMA 1970 s.28C(5), as amended by FA08/Sch39 para 2). The corporation tax analogue is FA98/Sch18 para 40(3).

**Status.** A determination "stands for all purposes as if it were a self assessment" until displaced, and there is no right of appeal or postponement against it (s.28C TMA 1970; EM).

**Machine-implementable form:**

```
determination_deadline   = statutory_filing_date + 3 years
displacement_deadline    = max(statutory_filing_date + 3 years,
                               determination_date + 12 months)
```

**Interaction with penalties.** HMRC's operational guidance is to ensure the initial fixed late-filing penalty has been imposed before raising a determination, or to issue both simultaneously if the time limit is nearly elapsed (SAM61030, cited in EM). HMRC's view is that a determination is "most effective" if issued within 12 months of the filing date (EM). Once a determination has been requested, EM says a s.29 discovery assessment must not be made except where Debt Management cannot make the determination, or the discovery is made after the determination issued.

**Failure to displace an under-stated determination.** A person who receives an assessment or determination understating their liability must tell HMRC within 30 days of the date of the assessment; failure to take reasonable steps to do so exposes them to a penalty under FA07/Sch24 para 2 (CH81090, CH81170). CH82120 puts the maximum at 30% of potential lost revenue. CH81090 notes that a person who files on time never receives an estimated assessment, so this penalty cannot bite on them. HMRC's view (CH401225) is that failing to file after an under-assessed determination is not *itself* evidence of deliberate withholding, though it may support further enquiry.

---

## 3. Discovery assessments: the statutory gateway

### 3.1 The discovery itself

Section 29(1) TMA 1970 permits an assessment where an officer or the Board discover that:

- (a) income tax or CGT ought to have been assessed but has not been;
- (b) an assessment is or has become insufficient; or
- (c) relief given is or has become excessive.

The assessment is made "to make good the loss of tax to the Crown" (s.29(1)).

*Amendment note:* Finance Act 2022 s.97 amended s.29(1)(a) both prospectively and retrospectively, effective for 2021-22 onwards, and retrospectively for 2020-21 and earlier years but only for specified charges — high income child benefit charge, gift aid charge, and certain pensions charges (EM3211). Where an appeal was received before 30 June 2021 on the ground that there was no discovery of income which ought to have been assessed, the pre-FA 2022 version of s.29(1) applies instead (EM3211).

**HMRC's interpretation of "discovery":** EM3220 says a discovery occurs when an officer reaches a conclusion or forms a reasonable opinion that there is an insufficiency of tax. EM3231 adds that it must be more than mere suspicion — reasonable belief is required; that no new facts are needed, only a new conclusion; and that the discovery must be made by an individual officer, not by "HMRC" or a team. EM3220 distinguishes *making* an assessment (the decision to assess) from *issuing* the notice, which may be done by another officer, and says the notice can be issued after the time limit expires provided there is no unreasonable delay.

### 3.2 Where a return has been made: the two conditions

Where a s.8/s.8A return has been made, an assessment under s.29(1) may only be raised if one of the two conditions in s.29(3) is met (EM3211):

| Condition | Test | Burden |
|---|---|---|
| First, s.29(4) | The situation was brought about carelessly or deliberately by the taxpayer or a person acting on their behalf | HMRC (CH54300; EM3259) |
| Second, s.29(5) | At the time the officer ceased to be entitled to enquire (or issued a partial/final closure notice), the officer could not reasonably have been expected, on the information made available, to be aware of the situation | HMRC |

**"Information made available" (s.29(6), (7)).** Information in the relevant return and accompanying accounts, statements or documents; in a relevant claim and accompanying documents; in documents, accounts or particulars supplied in connection with an enquiry; or information reasonably inferable from any of these, or notified in writing by the taxpayer (EM3233; s.29(6)).

**"Relevant returns and claims"** are the returns and claims for the year of assessment and each of the two immediately preceding years (EM3233).

**The hypothetical officer.** HMRC's construct (EM3233) is an officer deemed to have the general competence, knowledge and skills needed to understand the return in front of them, including knowledge of court decisions and HMRC publications.

**"Person acting on behalf."** EM3232, citing *Bessie Taube v HMRC* [2010] UKFTT 473 (approved in *HMRC v John Hicks* [2020] UKUT 0012), describes someone who takes steps the taxpayer could take or would be responsible for taking — completing and filing returns, correspondence with HMRC, providing documents, seeking external advice. They must *represent*, not merely advise. CH53200 says the term is very wide: an employee, a company officer, a fellow group company, a VAT group member, or a settlor or beneficiary.

**Practice generally prevailing.** EM3234 describes this as a practice that is relatively long-established, readily ascertainable and accepted by HMRC, agents and taxpayers; if HMRC has not agreed to a practice it cannot be inferred to be generally prevailing. HMRC's view is that the burden of proof rests on the person asserting it — typically the taxpayer, not HMRC (EM, "Extended Time Limits" caveats). Note the parallel express statutory bars: s.30B(3) TMA 1970 for partnership statement amendments, and para 45 Sch 18 FA 1998 for company discovery assessments, both of which block a discovery where the situation is attributable to a mistake as to the basis of computation made in accordance with prevailing practice at the time.

### 3.3 Where no return was made

Neither the s.29(4) nor the s.29(5) condition needs to be satisfied if the taxpayer did not submit a return, or where there is a failure-to-notify situation (EM, "Extended Time Limits" caveats; EM3235). The same point appears for corporation tax: the para 42/43/44/45 Sch 18 FA 1998 restrictions apply only where a return has been delivered (EM, "Legislation").

### 3.4 Machine-implementable form

```
can_discovery_assess(year, facts):
  if not discovery_made_by_named_officer:      return False   # EM3231
  if return_delivered:
      if not (careless_or_deliberate(s29(4)) or
              hypothetical_officer_unaware(s29(5))):  return False
      if attributable_to_prevailing_practice:   return False  # s.30B(3)/para 45 analogues
  # no return delivered -> s.29(3) conditions not engaged
  return today <= time_limit(behaviour, offshore, year)
```

---

## 4. Staleness and the collective knowledge argument

Two arguments once run against discovery assessments — that a discovery "goes stale" if not acted on promptly, and that knowledge held by one HMRC officer is imputed to the department as a whole — are both treated by HMRC as closed off by the Supreme Court.

| Argument | Position after *HMRC v Tooth* [2021] UKSC 17 (as reported in EM3260) |
|---|---|
| **Staleness** | "There is no principle that a discovery ceases to be valid due to passage of time; assessments may be made at any time up to the statutory time limit." |
| **Collective knowledge** | "One officer's knowledge is not deemed imparted to another; what matters is whether the officer making the assessment has subjectively made a discovery of an under-assessment." |

EM, "Extended Time Limits," draws the operational corollary: a discovery can be made afresh by a different officer.

The practical constraint that survives is not staleness but the statutory time limit plus the "no unreasonable delay" point on issuing the notice after the decision to assess (EM3220), and the requirement that the officer record when they reached their conclusion and the basis for it (EM3232).

---

## 5. Protective assessments and working case reviews

The notes do not contain a statutory concept of a "protective assessment." What they do contain is HMRC's internal handling of assessments made to preserve a position before a time limit expires:

- Officers are told to review all working enquiries annually to identify periods with no open enquiry but a reasonable belief of additional tax due, unlikely to settle by the assessing time limit — recommended **no later than three months before the assessing time limit expires** (EM3254).
- Officers **must not describe an assessment made as part of a working case review as "protective"**, as HMRC's view is that this "could invalidate them" (EM3254 / EM3251).
- Discovery assessments require authorisation at HO grade or above (EM3265).
- An assessment must be accompanied by an explanation letter covering reasons, discovery details, appeal rights, review/postponement options and the legislation used (EM3258).

A discovery assessment may legally be made even while the enquiry window is open where the loss of tax was careless or deliberate; EM2795 flags that HMRC's *operational* restriction against doing so is practice, distinct from the legal position.

A discovery assessment cannot be used to reopen matters already covered by a partial closure notice (EM, Example 4). PCN conclusions carry a 30-day appeal window, after which changes can only be made via discovery (CH279600).

---

## 6. The time limit ladder

### 6.1 The core table (income tax and CGT, HMRC-raised assessments)

All limits run from **the end of the year of assessment to which the assessment relates**. Note that s.34(3) TMA 1970 expressly excludes a self-assessment from the definition of "assessment" for s.34 purposes — these limits govern HMRC-raised assessments, not the taxpayer's own self assessment (which has its own 4-year limit under s.34A).

| Behaviour / trigger | Limit | Statute | Notes |
|---|---|---|---|
| Reasonable care taken (no careless or deliberate conduct) | **4 years** | TMA 1970 s.34(1) | Also the limit for a taxpayer's own self assessment (s.34A) |
| Loss of tax brought about **carelessly** by the person or a person acting on their behalf | **6 years** | TMA 1970 s.36(1), s.36(1B) | |
| Loss involving an **offshore matter or offshore transfer** | **12 years** | TMA 1970 s.36A(2) | Subject to exclusions — see §6.3 |
| Loss brought about **deliberately** | **20 years** | TMA 1970 s.36(1A), s.36(1B) | Applies instead of 12 years where offshore + deliberate (CH53505) |
| **Failure to notify** chargeability under s.7 TMA 1970 | **20 years** | TMA 1970 s.36(1A)(b) | Reduced to 4 years where there is a qualifying reasonable excuse (s.118(2); CH56100) |
| Failure to comply with **DOTAS** obligations (FA 2004 ss.309, 310, 313) | **20 years** | TMA 1970 s.36(1A)(c) | Reduced to 4 years where qualifying reasonable excuse (s.118(2); CH56100) |
| Failure to notify a **promoter reference number** (FA 2014 s.253) | **20 years** | TMA 1970 s.36(1A) | |

s.34(1) is "subject to any other Taxes Acts provision allowing a longer period" (EM, "Time Limits"). s.36A is subject to s.36(1A) and to any other provision allowing longer (TMA 1970 s.36A caveats).

### 6.2 Adjacent and specialised limits

| Situation | Limit | Ref |
|---|---|---|
| HMRC determination, no return filed | 3 years from statutory filing date | s.28C(5); CH52100 |
| Self assessment displacing a determination | Later of 3 years from filing date and 12 months from determination | s.28C(5) |
| Simple assessment | 4 years from end of year of assessment | TMA 1970 s.28; CH56100 |
| Recover over-repayment — no careless/deliberate | Latest of: 4 years from end of year concerned; end of year of assessment next following that in which the excessive repayment was made; closure of enquiry by final closure notice | s.30(5) with s.34; CH56100 |
| Recover over-repayment — careless | As above but 6 years | s.30(5) with s.36 |
| Recover over-repayment — deliberate | As above but 20 years | s.30(5) with s.36 |
| Late-received employment/pension/social security income — no careless/deliberate | Later of 4 years from end of year for which assessable, and 4 years from end of year in which received | s.35; CH56100 |
| Same — careless / deliberate | 6 years / 20 years on the same "later of" basis | s.35 with s.36 |
| Withdraw or reduce **EIS** relief — reasonable care or careless | Later of 6 years from end of year in which the use-of-money requirement falls, or the event causing withdrawal occurs | ITA 2007 s.237; CH52100 |
| Withdraw or reduce EIS relief — deliberate | Same "later of" basis, 20 years | ITA 2007 s.237 |
| Withdraw or reduce **CITR** relief — reasonable care or careless / deliberate | 6 years / 20 years from end of year for which relief obtained | ITA 2007 s.372 |
| Partnership discovery amendment (s.30B(1)) | Before the end of the relevant time limit (6/12/20 as applicable) | s.30B(1); EM |
| Consequential amendment to a partner's return under s.30B(2) | EM, "Legislation" states there is **no time limit**; EM7610/CH56100 state a 4-year limit for a *deceased* partner (see §6.5) | s.30B(2) |
| Consequential amendment under s.28B(4) following partnership enquiry | Not time-barred | s.28B(4); EM7610 |
| Claims for IT/CGT relief (general) | 4 years after end of year of assessment | s.43(1); SALF613 |
| Claim allowable only because of a late assessment | Before the end of the year of assessment following that in which the assessment was made | s.43(2) |
| Consequential claim/election/notice after a s.29 assessment | 1 year from end of the year of assessment in which the assessment was made | s.43A(2) |
| Assessment to give effect to a consequential claim | Not out of time if made within 1 year of final determination of the claim | s.43C(4) |

**Source conflict on s.30B(2):** EM, "Legislation" states flatly that "s30B(2) TMA 1970 consequential amendments to a partner's return have no time limit," and EM, "Extended Time Limits" says officers "should still try to make them within the same time limit where possible." EM7610 and CH56100, dealing with a deceased partner, state a four-year limit running from the end of the year of assessment in which the partner died (s.30B(2) read with s.40). The reconciliation is not spelled out in the notes; the death case is the only one for which a limit is stated.

### 6.3 The 12-year offshore limit (s.36A TMA 1970)

Inserted by FA 2019 s.80 (with IHTA 1984 s.240B inserted by FA 2019 s.81 for IHT).

**Definitions (s.36A(3)–(5)):**

- **Offshore matter** — lost tax charged on or by reference to: income from a source outside the UK; assets situated or held outside the UK; income or assets received outside the UK; activities carried on wholly or mainly outside the UK; or anything having effect as such. CH53520 notes "assets" takes its TCGA 1992 s.21(1) meaning, including currency (including sterling).
- **Offshore transfer** — a case *not* involving an offshore matter, where the income or disposal proceeds (or assets derived from them) on which lost tax is charged are transferred to a territory outside the UK before the relevant date.
- **Relevant date** — the date the return containing the required information was delivered, or, if no such return was delivered, 31 January in the year of assessment after that to which the lost tax relates (s.36A(5)).

**The extra hurdle for transfers.** For an offshore *transfer*, the 12-year limit applies only where HMRC can show the transfer made the lost tax "significantly harder to identify" — i.e. HMRC was significantly less likely to become aware of it, or would only become aware significantly later. CH53540 says "significantly" takes its normal meaning of noteworthy, important or consequential.

**Year-by-year availability (income tax / CGT):**

| Tax year | 12-year limit available? |
|---|---|
| 2012-13 and earlier | No (CH53560; CH53100 caveats) |
| 2013-14 and 2014-15 | Only where the loss resulted from **careless** behaviour (s.36A; CH53560) |
| 2015-16 onwards | Yes, regardless of whether reasonable care was taken or behaviour was careless (CH53505, CH53560) |

Where behaviour is **deliberate**, the 20-year limit applies instead (CH53505); the 20-year limit continues to run alongside (CH53560).

**Exclusions (s.36A):** the 12-year limit is barred where HMRC had already received **relevant overseas information** in time and it was reasonable to expect an assessment before the normal time limit expired; and where the liability arises from TIOPA 2010 Part 4 transfer pricing adjustments.

- **Relevant overseas information** (s.36A(8); CH53550) — information provided to HMRC by an authority outside the UK under an EU-law tax provision or under an agreement to which the UK and that territory are parties (e.g. CRS data, tax treaty exchange of information). CH53550 stresses that partial or insufficient information does not trigger the exclusion; the test is whether the information *reasonably enabled* HMRC to assess the lost tax before the normal time limits expired.

**Caution on terminology.** CH53100 and CH53520 both warn that "offshore matter" and "offshore transfer" for the 12-year time limit differ in meaning from the similarly-named terms used elsewhere in the Taxes Acts, notably for penalties under FA 2007 Sch 24 para 4A. Do not share a single definition across the two regimes in code.

**Worked example (CH, "Income Tax and Capital Gains Tax > Example"):** where an officer demonstrates careless behaviour by the taxpayer or representative on an offshore matter, assessments can be made back to and including 2013-14. Absent careless behaviour, assessments are limited to years back to 2015-16 (or 2016-17 if the discovery is made after 6 April 2028), because the 2015-16 limit expired on 5 April 2028.

### 6.4 Behaviour definitions

| Term | Statutory definition | HMRC gloss |
|---|---|---|
| **Carelessly** | A loss of tax is brought about carelessly if the person fails to take reasonable care to avoid bringing it about; also where information given to HMRC is later discovered to be inaccurate and the person fails to take reasonable steps to inform HMRC (TMA 1970 s.118(5)–(6)) | CH53400 likens it to common-law negligence per Baron Alderson in *Blyth v Birmingham Waterworks Co* (1856): omission to do what a reasonable man would do, or doing what a prudent and reasonable man would not do. EM5125 cites *David Collis v HMRC* [2011] UKFTT 588(TC) for the standard of "a prudent and reasonable taxpayer in the position of the taxpayer in question" — a First-tier Tribunal decision, not binding |
| **Deliberately** | Includes a loss of tax arising as a result of a deliberate inaccuracy in a document given to HMRC by or on behalf of that person (TMA 1970 s.118(7)) | CH53700: occurs when a person knowingly gives HMRC an inaccurate document; a person is treated as deliberately causing a loss of tax if they consciously intended to mislead HMRC, even if they assert no intent to cause a tax loss. EM3220: knowingly or intentionally doing or failing to do something resulting in a tax loss |

`brought about carelessly` in s.29(4) has the same meaning as in s.36(1) (s.118(5); EM3220).

**Burden of proof.** CH54300 states the onus of proving careless or deliberate behaviour rests with HMRC when relying on extended time limits. EM3259 says HMRC must be able to demonstrate that alleged behaviour is sufficiently serious to support an extended time limit assessment if appealed. EM, Example 4, adds HMRC's view that the onus "shifts to the taxpayer once HMRC satisfactorily demonstrates the requisite behaviour, specifically regarding the amount of the assessment on appeal." The standard is the balance of probabilities, though CH81190 says the quality of evidence should be higher for more serious behaviour.

CH53400 cautions officers that repetition of the same inaccuracy does not automatically indicate a failure to take reasonable care — "a sense of proportion must be kept."

**Reasonable excuse relief.** A person is not treated as having failed to do something within a time limit if it was done within extended time allowed by HMRC/tribunal/officer, or if there was reasonable excuse and the thing was done without unreasonable delay after the excuse ceased (TMA 1970 s.118(2)). Applied to time limits, this reduces the 20-year failure-to-notify and DOTAS-failure limits to 4 years (CH56100; CH53900).

### 6.5 Deceased taxpayers

| Situation | Limit | Ref |
|---|---|---|
| Assessment on personal representatives under ss.34, 35, 36 or 36A | Not more than **4 years** after the end of the year of assessment in which the deceased died | TMA 1970 s.40(1) |
| Same, where the loss was brought about carelessly or deliberately by the deceased or someone acting for them before death | Assessment may be made for any year ending **not earlier than 6 years before death**, but still must be made within 4 years of the end of the year of assessment of death | TMA 1970 s.40(2) |
| s.30B(2) consequential amendment to a deceased partner's SA following a s.30B discovery amendment | Within 4 years after the end of the year of assessment in which the partner died; extendable back 6 years before death for careless/deliberate behaviour | s.30B(2) with s.40; EM7610 |

EM7610 notes that s.28B(4) and s.30B(2) amendments cannot be made to a trust and estate return covering *post-death* income, because the personal representative is not a partner; correction there requires a s.9A enquiry and s.28A closure notice.

### 6.6 Corporation tax equivalents

Structurally parallel but legally distinct (EM, "Time Limits"). All run from the end of the accounting period:

| Behaviour | Limit | Ref |
|---|---|---|
| No careless/deliberate | 4 years | FA 1998 Sch 18 para 46(1) |
| Careless | 6 years | FA 1998 Sch 18 para 46(2), (2B) |
| Deliberate | 20 years | FA 1998 Sch 18 para 46(2A), (2B) |
| Avoidance scheme information failure / failure to notify, **with** reasonable excuse | 4 years | TMA 1970 s.118(2) with Sch 18 para 46(1) |
| Same, **without** reasonable excuse | 20 years | Sch 18 para 46(2A), (2B) |
| CT determination (no return / partial compliance) | 3 years from the day the power becomes exercisable | Sch 18 paras 36(5), 37(4) |
| Self-assessment displacing CT determination | Later of 3 years from that day and 12 months from the determination | Sch 18 para 40(3) |

"Related person" for CT is a person acting on behalf of the company, or a person who was a partner of the company at the relevant time (Sch 18 para 46(2B)).

---

## 7. Commencement and transitional traps

The aligned 4/6/20 regime did not switch on cleanly.

| Point | Position | Ref |
|---|---|---|
| Direct taxes: normal limit reduced from 6 years to 4 | Applies to assessments made **on or after 1 April 2010**, regardless of the tax year involved | SI 2009/403 Art 2(2); CH51540; CH50100 |
| Aligned limits generally | Apply to assessments made after the relevant commencement date regardless of the period assessed | CH50100 |
| 20-year limit for **deliberate** loss, IT/CGT | Does **not** apply to 2008-09 and earlier years under SI 2009/403 Article 7, unless the loss is attributable to negligent conduct | CH53700 |
| 20-year limit for deliberate loss, CT | Does not apply to accounting periods ended on or before 31 March 2010 unless attributable to negligent conduct | CH53700 |
| 20-year limit for **failure to notify** under s.7, IT/CGT | For 2008-09 or earlier, HMRC must show **negligent conduct** (not carelessness) with a direct link between the failure and the loss — an older, different standard | CH53600 Exception 1; EM3235 |
| Same, corporation tax | Accounting periods ending on or before 31 March 2010: negligent conduct required | CH53600 Exception 2; EM3235 |
| Avoidance-scheme / failure-to-notify 20-year limit, CT periods ending on or before 31 March 2010 | Additionally requires negligent or fraudulent conduct by the company, an agent, or a partner | SI 2009/403 Art 8; CH56100 |
| Extra time to **reclaim** overpaid IT/CGT for persons not issued an SA notice within a year of the tax year end | Previous time limits continue until 1 April 2012; explicitly does **not** give HMRC further time to assess unpaid tax; does not apply to companies | CH51550, CH51560; SI 2009/403 Art 10 |
| Behaviour test for penalties | FA 2007 Sch 24 (careless/deliberate) applies to periods beginning on or after 1 April 2008 with filing dates on or after 1 April 2009; earlier periods use fraud/negligence (e.g. TMA 1970 s.95) | EM5101, EM5102; CH401300 |
| The s.36 wording itself | From 1 April 2010, TMA 1970 s.36 changed from covering fraudulent or negligent conduct to loss of tax brought about carelessly or deliberately | CH401100 |

CH29770 also warns that transitional provisions meant the 6-to-4 year reduction "did not apply in full immediately on 1 April 2010" — the 6-year window for negligent/careless discovery assessments only fully collapsed to 4 years shortly after that date.

---

## 8. Requirement to Correct (offshore, 2015-16 and earlier)

A separate, time-limited regime sitting on top of the ordinary ladder.

| Element | Rule | Ref |
|---|---|---|
| Scope | Offshore tax non-compliance (failure to notify, failure to file, or inaccuracy involving offshore matters/transfers) for **2015-16 or earlier** | s.67 and Sch 18 FA (No.2) 2017 |
| Correction deadline | **30 September 2018** | Sch 18 FA (No.2) 2017 |
| Consequence of missing it | Failure to Correct (FTC) penalties, minimum 100% of the offshore PLR | CH123450, CH123500 |
| Cap | FTC penalty plus a Sch 55 para 5 penalty must not together exceed 200% of the tax liability | CH123600 |
| Extended assessment window for pre-2013-14 years assessable as at 6 April 2017 | Later of the date assessable under normal rules or **5 April 2021** | CH123200 |
| Superseded for 2013-14 onwards | The normal RTC "as at 6 April 2017" assessability test is superseded by the s.36A 12-year limit | CH manual, "Failing to notify" |

Escape routes from the FTC penalty for those who notified by 30 September 2018 but disclosed after: WDF, 90 days from notification; CDF, 60 days from HMRC acceptance of CDF1; disclosure under an open enquiry, outline by 29 November (CH123260).

---

## 9. Authorisation and procedure for extended time limit assessments

These are HMRC's internal controls, not statutory conditions of validity — but they shape what a taxpayer will see.

**Definition.** An "Extended Time Limit (ETL) assessment" is, from 1 April 2010, any assessment where the assessing time limit is other than the normal time limit: 12-year offshore, 6 or 20 year careless/deliberate, and 20-year failure-to-notify/avoidance-scheme assessments (EM3257).

| Requirement | Ref |
|---|---|
| Authorisation from the Authorising Officer (normally the officer's manager), with evidence of the specific condition and behaviour relied on | EM3257; CH53300; CH282070 |
| Discovery assessments generally authorised at HO grade or above | EM3265 |
| Consult the technical lead/enquiry project manager before ETL assessments in project-managed avoidance scheme cases | EM3257 |
| Explanation letter alongside the assessment: reasons, discovery details, appeal rights, review/postponement options, legislation used; for ETL assessments also the ETL basis, an interest warning, and factsheet CC/FS9 if penalties are in contemplation | EM3258 |
| Record when the officer reached the conclusion that there is a loss of tax, and the basis for it | EM3232 |
| Identify what behaviour brought about the loss, why it was careless or deliberate, and the supporting evidence | EM3232 |
| Submit the case to a compliance accountant before issuing a decision letter where HMRC intends to allege accountancy is carelessly or deliberately wrong | CH53200; ARTG2190 |
| Check the tax-specific time limit tables at CH56000+ before making any assessment | CH52100; CH53510 |

---

## 10. Appeals against assessments

| Point | Rule | Ref |
|---|---|---|
| Time limit for notice of appeal | Usually **30 days** from the date the formal decision notice is *issued* (date of posting, not receipt) | ARTG2180, ARTG2040 |
| Late appeals | HMRC must accept a late appeal where there is reasonable excuse and no unreasonable delay after the excuse ended | ARTG2180 |
| Time-barred assessments | Objection can only be made by way of appeal against the assessment, not as a standalone objection | TMA 1970 s.34(2); s.29(8); s.30B(8); Sch 18 FA 1998 |
| Determinations | No right of appeal and no postponement | s.28C; EM |
| Partnership discovery amendment (s.30B) | The nominated partner has the right of appeal | s.31(1)(c); SALF |
| s.30B(2) consequential amendments to partners' returns | No right of appeal | EM3235 |
| Settlement by agreement | Available at any time before the tribunal completes its hearing; the customer has 30 days from the agreement (or written confirmation of a verbal agreement) to withdraw | ARTG3420; s.54 TMA 1970 |
| Review request after appeal | HMRC must write setting out its most recent view of the matter within 30 days of the review request, or other reasonable time | TMA 1970 s.49B(2); ARTG2213 |
| Appeal to tribunal after review | 30 days from the date of the review conclusion letter | ARTG4030 |
| Simple assessment | No right of appeal (and therefore no review) unless the customer has raised a query under s.31AA TMA 1970 and received a final response | ARTG2040, ARTG2190, ARTG4050 |
| Jeopardy amendment during an SA enquiry | May be appealed to HMRC, but cannot be notified to tribunal or reviewed until the enquiry closes | ARTG2160; EM1955 |

An assessment, once finalised, can only be varied on appeal in four specified situations (s.54, s.49C(4)/s.49E(5)/s.49F(2), s.50(6)/(7) TMA 1970); otherwise a further assessment is required rather than a variation (EM3266).

---

## 11. Interaction with claims

Because the ordinary claim limit is four years (s.43(1)), a claim for a year may fall due after that year's return has become final, requiring the Schedule 1A procedure rather than a return amendment (SALF).

**Consequential claims.** Where HMRC makes a further assessment under s.29 *not* for the purpose of recovering tax lost carelessly or deliberately, s.43A(2) allows a relevant claim, election, application or notice to be made, revoked or varied within one year from the end of the year of assessment in which the assessment was made. Section 43A does **not** apply where the s.29 assessment is made to recover tax lost carelessly or deliberately (s.43A caveats). Certain elections are excluded from the definition of "relevant claim" by s.43A(2A), including married couple's/civil partner's allowance transfer elections (ITA 2007 ss.47–49, s.55C) and the 1982 rebasing election (TCGA 1992 s.35(5)).

Where the loss was careless, TMA 1970 s.36(3) permits only consequential **claims**, not elections (CH manual, "Indirect Taxes"). Section 43B limits s.43A: exercising a s.43A(2) power that would alter another person's liability requires that other person's written consent (or their personal representatives'), and relief is capped where reductions would exceed the additional liability from the assessment, with a 30-day apportionment notice window (s.43B(1), (4)(b), (5)).

There are no consequential claim provisions for VAT, IPT, aggregates levy, climate change levy, landfill tax, PRT or excise duty, unlike IT/CGT/CT/SDLT (CH50100; CH manual, "Indirect Taxes").

---

## 12. Related concepts worth not confusing

- **Presumption of continuity** — HMRC's inference that omissions found in one year's returns continued into others, absent contrary evidence. EM3236 states it alone does not justify assessment increases: HMRC must still produce evidence, and a single unexplained omission in one year is insufficient to extend to other years without more.
- **Discovery determination (CT)** — the counterpart to a discovery assessment, made where a discovery relates to reduction of overstated losses or overclaimed relief leading to additional liability in a *different* period or company; it requires the company to have already delivered a return (EM3242; Sch 18 FA 1998 para 41(2)).
- **Partnerships** — discovery assessments must be made on individual partners; s.30B provides the discovery route for the partnership return itself (SALF). HMRC cannot use a s.29 assessment to challenge a partner's individual return figure that simply matches the partnership return — it must enquire into or amend the partnership return first (EM3235). There is no joint liability among partners for tax on partnership profits (SALF511).
- **Assessment time limits vs. penalty assessment time limits** — different regimes. FA 2007 Sch 24 penalty assessments generally run 12 months from the end of the appeal period for the related tax correction (Sch 24 para 13(3), (5)); Sch 55 FA 2009 late-filing penalty assessments run to the later of 2 years from the filing date and 12 months from the end of the appeal period for the tax assessment (Sch 55 para 19; CH64200). CH50100 also notes that aligned time limits govern how far *back* HMRC can assess, a distinct concept from how long HMRC has to make an assessment.

---

## Gaps in the sources

The following points fall within the brief but are not covered, or not fully covered, by the supplied notes:

1. **"Protection" arguments in the taxpayer's favour** — the brief refers to "protection arguments." The notes cover HMRC's internal prohibition on labelling review-driven assessments as "protective" (EM3254) and the s.29(5) information-made-available protection, but contain nothing on taxpayer-side white-space disclosure practice as a shield against discovery beyond a passing reference to SP1/06 in EM7522. The text of SP1/06 is not in the notes.
2. **The reasoning of *HMRC v Tooth*** — only HMRC's summary of the outcome (EM3260) is supplied. The judgment's facts, the treatment of "deliberate inaccuracy in a document," and the Court's reasoning on the discovery/staleness point are not in the notes.
3. **Case law on discovery generally** — apart from *Tooth*, *Bessie Taube*, *HMRC v John Hicks*, *David Collis*, *Blyth v Birmingham Waterworks*, *Derry v Peek*, *Rose v Humbles* and *Morgan and Self*, no tribunal or court authority on s.29 is supplied, and only *Tooth*, *Taube* and *Hicks* are cited on discovery conditions.
4. **s.30B(2) time limit conflict** — the notes disagree on whether the consequential amendment to a living partner's return is time-limited (see §6.2). No source in the notes resolves this.
5. **The 12-year offshore limit for IHT** — the IHTA 1984 s.240B start date is given as running from the later of the date payment/last instalment was made and accepted, or the date tax became due (CH53510), and CH53100 notes there is no time limit at all for IHT where no account has been delivered and the loss was deliberate. IHT is otherwise outside the scope of this page.
6. **Interest on assessed tax** — s.86/s.87A TMA 1970 mechanics and rates are not covered in the notes beyond passing references.
7. **Whether an out-of-time assessment is void or merely voidable** — the notes establish only that the objection route is appeal (s.34(2)), not the underlying characterisation.
8. **The 2016-17 "additional information" element of disclosure quality**, and territory categorisation dates, are described in the notes for *penalty* purposes only (CH112400, CH403145) and do not bear on assessing time limits.

---

## Sources used on this page

This page was written by an LLM from structured notes extracted from the mirrored sources below. Always check the upstream source before relying on any figure or deadline.

- [sa-helpsheets:5f67ceae-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/averaging-for-creators-of-literary-or-artistic-works-hs234-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/averaging-for-creators-of-literary-or-artistic-works-self-assessment-helpsheet-hs234.md`
- [sa-helpsheets:5f67e2d6-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/furnished-holiday-lettings-hs253-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/furnished-holiday-lettings-self-assessment-helpsheet-hs253.md`
- [sa-helpsheets:5f67d46f-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/negligible-value-claims-and-income-tax-losses-on-disposals-of-shares-you-have-subscribed-for-in-qualifying-trading-companies-hs286-self-assessment-he) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/negligible-value-claims-and-income-tax-losses-on-disposal-of-shares-self-assessment-helpsheet-hs286.md`
- [sa-helpsheets:5f67e327-7631-11e4-a3cb-005056011aef](https://www.gov.uk/government/publications/seed-enterprise-investment-scheme-income-tax-and-capital-gains-tax-reliefs-hs393-self-assessment-helpsheet) - 1 note(s) - mirrored at `corpus/hmrc-publications/customer-facing-guidance/helpsheets/seed-enterprise-investment-scheme-income-tax-and-capital-gains-tax-reliefs-self-assessment-helpsheet-hs393.md`
- [hmrc-manual-artg](https://www.gov.uk/hmrc-internal-manuals/appeals-reviews-and-tribunals-guidance) - 4 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/artg.md`
- [hmrc-manual-ch](https://www.gov.uk/hmrc-internal-manuals/compliance-handbook) - 45 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/ch.md`
- [hmrc-manual-em](https://www.gov.uk/hmrc-internal-manuals/enquiry-manual) - 19 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/em.md`
- [hmrc-manual-salf](https://www.gov.uk/hmrc-internal-manuals/self-assessment-legal-framework) - 3 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/salf.md`
- [tma-1970](https://www.legislation.gov.uk/ukpga/1970/9/contents) - 5 note(s) - mirrored at `corpus/legal-system/primary-legislation/acts/tma-1970.md`
