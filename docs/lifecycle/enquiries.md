---
title: Enquiries into a return
generated: true
generated_on: '2026-09-08'
generated_by: claude-cli:opus
input_hash: f3dbff2c4b47c26e
note_count: 80
sources:
- hmrc-manual-artg
- hmrc-manual-ch
- hmrc-manual-em
- hmrc-manual-salf
- hmrc-manual-sam
- tma-1970
---

# Enquiries into a return

!!! danger "Unofficial - not HMRC, not advice, written by an LLM"

    This page is **not** an HMRC publication and has no connection to HMRC or
    any government body. It was **written by a language model** from mirrored
    source material, and can be wrong, incomplete or out of date. It is not
    tax advice. Check every figure, date and rule against the cited source
    before relying on it, and see
    [GOV.UK](https://www.gov.uk/self-assessment-tax-returns) for official
    guidance.

This page describes the Self Assessment enquiry regime for income tax and capital gains tax: when HMRC may open an enquiry, what opening one changes, how information is obtained during it, how it is closed by partial or final closure notice, how a taxpayer can force closure through the tribunal, and where the enquiry regime stops and the discovery regime begins. It separates what the Taxes Management Act 1970 requires from what HMRC's internal manuals say about how it runs enquiries in practice. It is an independent summary, not an HMRC publication.

## 1. Source status

The primary rules are in TMA 1970 (ss.9A–9C, 28A–28B, 28ZA–28ZE, 29, 34–36, Sch.1A) and FA 2008 Sch.36. The Enquiry Manual (EM), Compliance Handbook (CH), Self Assessment manual (SAM) and Self Assessment Legal Framework manual (SALF) are HMRC's own internal guidance: they record HMRC's interpretation and operating practice, and in several places describe targets and conventions that have no statutory force (see §10). Parts of the EM and CH are redacted under FOIA 2000 exemptions, so the published guidance is incomplete in places (e.g. EM1952, EM1805, EM1895).

## 2. The enquiry window

An officer may enquire into a return under s.8 or s.8A only if notice of enquiry is given to the taxpayer within the statutory period (TMA 1970 s.9A(1)).

| Trigger | Last date for notice of enquiry | Ref |
|---|---|---|
| Return delivered on or before the filing date | End of 12 months after the day the return was delivered | TMA 1970 s.9A(2)(a) |
| Return delivered after the filing date | Quarter day next following the first anniversary of the day the return was delivered | TMA 1970 s.9A(2)(b) |
| Return amended by the taxpayer under s.9ZA | Quarter day next following the first anniversary of the day the amendment was made | TMA 1970 s.9A(2)(c) |
| Partnership return / partnership amendment | Same structure, under s.12AC(2) | EM7553 |
| Voluntary return (no notice to file given) | 12 months from the day the return was delivered to HMRC | SAM121140; EM7553 |

"Quarter days" are 31 January, 30 April, 31 July and 31 October (TMA 1970 s.9A(2)). "The filing date" is the last day for delivering the return under s.8 or s.8A (s.9A(6)).

Machine-implementable form:

```
inputs: return_delivered_date, filing_date, amendment_date (optional)
if amendment_date: window_end = next_quarter_day(amendment_date + 1 year)
elif return_delivered_date <= filing_date: window_end = return_delivered_date + 12 months
else: window_end = next_quarter_day(return_delivered_date + 1 year)
```

Notes and edge cases:

- A voluntary (unsolicited) return is treated, since 12 February 2019 and with both retrospective and prospective effect, as made in response to a notice to file given on the day HMRC received it; it can never be late, so the 12-month rule applies (SAM121140; SAM123140). HMRC's manual states no late filing penalty arises on a voluntary return (EM, Voluntary Returns).
- Historic windows differ and should not be applied to modern years: for returns up to 2000-01 the last date was 30 January following the fixed filing date; for 2001-02 to 2006-07 it was 31 January following; the 12-months-from-receipt rule applies from 1 April 2008 (SAM31020; EM1506).
- The late-return rule can extend the window materially. EM4570 gives the example of a return received on 1–2 February producing a window running to 30 April the following year. EM7554's worked example: a partnership return delivered 31 January 2022 can be enquired into until 31 January 2023; an amendment made 20 June 2022 can be enquired into until 31 July 2023.
- Notice must be **in writing** (EM0067, by reference to s.989 ITA 2007 / s.1119 CTA 2010) and must actually be **received** by the taxpayer or nominated partner before the window closes, not merely posted (EM7552; SAM31100). SAM31100 assumes receipt 2 working days after first-class posting and 4 working days after second class, unless evidence of actual receipt is produced. EM1506 tells officers to use tracked delivery where notice is issued within a week of the deadline. EM7528 flags that Royal Mail's second-class delivery position changed from 28 July 2025, affecting those assumptions.
- Only one notice of enquiry may be given per return (TMA 1970 s.9A(3)), the sole exception being a notice given in consequence of a s.9ZA amendment. EM1530 calls this the "single enquiry rule" and applies it equally to s.12AC and Sch.1A para.5 claims: a return, amendment or claim can be enquired into once only, even if the first enquiry closed while the window was still open.
- Before issuing a notice, EM1535 requires the case owner to confirm the time limit has not passed and that an enquiry into that year has not already been opened and closed.

## 3. What opening an enquiry does

Legal and practical consequences of a valid s.9A notice:

- **Repayments may be withheld.** s.59B(4A) TMA 1970 allows HMRC to withhold all or part of a repayment from the opening of the enquiry until a closure notice is issued (SAM31020).
- **Taxpayer amendments are suspended.** A s.9ZA amendment made while an enquiry is open does not restrict the scope of the enquiry and does not take effect on the amount of tax self-assessed until a closure notice is issued (TMA 1970 s.9B; EM1906). The taxpayer's own amendment window is unchanged and is not extended by the enquiry: 12 months from the filing date (s.9ZA; SAM124040; EM7554 for partnerships).
- **Sch.36 taxpayer notices become available.** Where an SA return has already been made for the chargeable period, a taxpayer notice can only be given if there is an open enquiry, a potential discovery position, or the information is needed to check another tax or a reduction/repayment (FA 2008 Sch.36 para.21; CH23526; CH23540).
- **Jeopardy amendment becomes possible** under s.9C (see §6).
- **Records must be kept longer.** Retention runs to the latest of the normal date, completion of any enquiry, and the day the enquiry window closes — the fifth anniversary of 31 January following the year of assessment for a trade, profession or business (property letting counts as a trade) (CH14530; TMA 1970 s.12B), or the first anniversary of that 31 January for a non-business taxpayer (CH14550).
- **Discovery is displaced in practice.** HMRC's guidance is that officers should open an enquiry wherever the window is open rather than use discovery (EM3201), and that a discovery assessment on a director's employment income must not be made while a s.9A enquiry is open or the window is unexpired — the income must instead go into the s.28A closure notice (EM8250/EM3265).

HMRC procedural expectations at opening (guidance, not statute): send the notice with factsheet CC/FS1 (EM1551); address correspondence to the agent where one acts, copying the taxpayer (EM1560); do not tell the taxpayer why the enquiry was opened (EM1560); never disclose that a case was selected under the random enquiry programme, and work random cases to the same standard as risk-based ones (EM0093); open neutrally, seeking information rather than asserting inaccuracy (EM1805; EM1503). There is no statutory form of words for the opening notice (EM1530).

## 4. Scope

**Default scope is the whole return.** EM1905 states that, legally, an enquiry covers the full return even if the opening letter indicated only certain matters would be examined; EM1560 nevertheless tells officers to make clear whether the enquiry is into the whole return or particular entries, and that it could be extended. If scope is widened, EM1905 requires the officer to update the enquiry plan and tell the taxpayer what is now covered.

**Enquiry into an amendment.** Where notice is given in consequence of a s.9ZA amendment, and either the ordinary window under s.9A(2)(a)/(b) had already closed or a final or partial closure notice had already been issued, the enquiry is **limited to matters to which the amendment relates or which are affected by it** (TMA 1970 s.9A(5)). The equivalents are s.12AC(5) (partnerships) and FA 1998 Sch.18 para.25(2) (companies). HMRC's guidance is that where an amendment is "fundamental", officers should look to the discovery legislation rather than treat the amendment enquiry as a route into the whole return (EM1521).

**Partnerships.** A s.12AC notice into the partnership return is deemed to include notice of intention to enquire into each partner's return, but only as regards partnership matters (TMA 1970 s.12AC(6); EM7554). Any risk on a partner's return unrelated to the partnership requires a separate s.9A notice, subject to its own time limits (EM7554). Separate notices should be issued rather than combined (EM7552).

**Companies and directors.** There is no statutory link between a company tax return enquiry and a director's personal return; a separate s.9A notice is required (EM8205, EM8210).

## 5. Information gathering during an enquiry

Informal requests come first. EM1555 instructs officers to ask in the opening letter only for documents and information that are reasonably required to check the accuracy of the return **and** that could later be required under a FA 2008 Sch.36 para.1 information notice; anything outside that must be flagged as voluntary (EM1560). EM1561 and EM1570 restrict routine requests for private bank, building society and credit card records unless relevance to a return entry or an identified means risk can be demonstrated. Requests for statements of assets or capital statements in the opening letter are described as exceptional (EM1560).

If information is not produced within the stated time and no revised timescale is agreed, EM1590 directs the officer to issue a Sch.36 para.1 notice.

Formal notice mechanics:

| Point | Rule | Ref |
|---|---|---|
| Service | Deliver to the person or leave at usual/last known residence; email only with the customer's explicit informed consent specific to that notice | CH23440 |
| Compliance | Within the period specified, and at the time, by the means and in the form specified | FA 2008 Sch.36 para.7; CH23480 |
| "Open enquiry" for para.21 purposes | Notice of enquiry given (s.9A / s.12AC / Sch.1A para.5) and no closure notice yet issued for the matters the request relates to; if a partial closure notice has issued, requests are restricted to matters not closed by it | CH23540 |
| "Reason to suspect" | Facts leading an officer to think tax may have been under-assessed or relief excessive; a lower threshold than being able to assess, but does not permit speculative or fishing enquiries | FA 2008 Sch.36 para.21(6); CH23560 |
| Partnerships | Each partner is treated as having made the partnership return, claim or election | FA 2008 Sch.36 para.37; CH23528 |
| Penalties | Initial, daily, increased daily, tax-related and inaccuracy penalties; payable within 30 days of the assessment; appeal must reach HMRC within 30 days of issue; reasonable excuse defence if the failure is remedied without unreasonable delay | FA 2008 Sch.36 paras.45–49; CH26820–CH26900; CH26320 |

Formal defects do not automatically void a notice provided it meets the intention of the law and identifies the affected person adequately, though substantial errors may require a fresh notice (CH23440).

## 6. During the enquiry: amendments, referrals, delay

**Jeopardy amendment (s.9C).** While an enquiry is in progress, an officer who forms the opinion that the tax stated is insufficient and that a loss of tax to the Crown is likely unless the assessment is amended immediately may amend the self-assessment (TMA 1970 s.9C(2)). The legislation is silent on the circumstances that warrant this; the examples in HMRC's guidance (asset disposal, becoming non-resident, bankruptcy, imprisonment) are guidance, not statutory criteria (EM1951–EM1953). HMRC's position is that a jeopardy amendment must not be issued once a company is in liquidation or an individual has been made bankrupt (EM1951). Appeal lies within 30 days, but the appeal cannot be heard or determined until the enquiry matters are closed by partial or final closure notice (TMA 1970 s.31(2); EM1955, EM3865); only the postponement decision can go to the tribunal in the meantime, within 30 days of notification (EM1955; ARTG2530).

**Joint referral (ss.28ZA–28ZE).** HMRC and the taxpayer may jointly refer a question arising in connection with the subject matter of an open enquiry to the tribunal for determination during the enquiry (SALF; EM1910; for partnerships, EM7554). Neither party can compel the other to join, and there is no right of appeal against a refusal (EM, "Making a joint application to the tribunal"). EM2150 tells officers who refuse to explain their reasons in writing and remind the taxpayer of the appeal right at the end of the enquiry.

**Delay.** EM1811–EM1815 set internal expectations: maintain an intervention plan and audit trail, avoid material delay, aim for a 15 working day turnaround on correspondence, and take positive action rather than issuing bare reminders. These are HMRC targets, not statutory deadlines. EM1813 acknowledges that HMRC delay may support a taxpayer's closure application and may undermine penalties.

## 7. Closure notices

On completing an enquiry the officer must issue a formal closure notice informing the taxpayer that the enquiry is complete, stating the conclusions, and either stating that no amendment is required or making the amendment (TMA 1970 s.28A(1)–(2); EM0065).

| Type | Function | Ref |
|---|---|---|
| Final closure notice (FCN) | Concludes the enquiry into the return. One per return or claim enquired into (and one per return where a PCN has been issued) | TMA 1970 s.28A; EM3831 |
| Partial closure notice (PCN) | Concludes the enquiry as to specified "matters" while leaving the rest open. Available for enquiries into returns only, not claims made outside a return | TMA 1970 s.28A/28B; EM3831A; CH23440 |
| Partnership FCN | Given to the nominated partner (or successor), stating conclusions and amending the partnership return; consequential amendments then made to each partner's return | TMA 1970 s.28B; EM7560 |
| Claim outside a return | Notice states conclusions and either amends the claim or allows/disallows it wholly or partly; effect must be given within 30 days | TMA 1970 Sch.1A paras.7–8; EM3860 |

Consequences and constraints:

- Appeal against the conclusions or amendment must reach HMRC within 30 days of issue (TMA 1970 ss.31(1)(b), 31A; EM3831). If no appeal is made, the amendment becomes final 30 days after issue (EM3867). Where an appeal goes to statutory review, the taxpayer has 30 days from the review conclusion letter to notify the tribunal (EM3867; ARTG4830); if the taxpayer neither accepts a review offer nor notifies the tribunal, the appeal is treated as settled on HMRC's stated view (TMA 1970 s.49C(4); ARTG4070).
- Review scope, where a closure notice is appealed, is limited to the specific conclusions and amendments in that notice; a review cannot alter the scope of the appeal (ARTG4070).
- Appeals on matters outside a PCN's scope cannot be determined until a further partial or final notice issues (EM3865, EM3867).
- HMRC's guidance is that FCNs should not be issued for pre-SA years or years where the enquiry window is closed; further tax in those years is assessable only under the discovery provisions (EM3811).
- EM3868 warns officers against using post-closure information requests to continue a formally completed enquiry, particularly after a tribunal-directed early closure.
- A closure notice is not the only exit: the enquiry can be concluded by contract settlement (SALF407; EM6002). SAM notes that a closure notice is not issued in contract settlement cases unless the taxpayer or agent asks for one. HMRC's practice is to seek a certificate of full disclosure before concluding where returns or accounts have been established to be incorrect — EM3811 states expressly that there is **no statutory authority** to demand one.

## 8. Applications to the tribunal to close an enquiry

The taxpayer may apply to the tribunal for a direction that HMRC issue a partial or final closure notice (TMA 1970 s.28A(4); for a partnership enquiry, s.28B(5)). The tribunal must give a direction specifying when the notice is to be issued **unless HMRC shows reasonable grounds for not doing so** (TMA 1970 s.28A(4); EM1976).

- There is no right of appeal against the enquiry notice itself (s.9A, s.12AC), but the taxpayer can apply for closure at any time after it is issued, and applications may be repeated (EM1976). EM1981 tells officers to be prepared to contest an application made immediately on receipt of the opening letter.
- For a partnership, only the nominated partner may apply in respect of the partnership enquiry; an individual partner applies under s.28A(4) only in respect of the enquiry into their own return (EM7558, EM7559). EM1995 states HMRC's position that the deemed enquiry arising under s.12AC(6) is not itself challengeable under s.28A(4).
- Where the tribunal directs closure, HMRC's guidance is that the notice must be issued within the directed timeframe even if HMRC hoped to reach a contract settlement (EM3831; EM7559).
- There is no appeal right against a determination of tax where a return is outstanding, so EM1982 says the taxpayer's remedy is to file the return rather than apply for closure.
- ADR may be offered as an alternative, though EM1976 says it is not usually appropriate at the earliest stage, and EM1951 says it is unsuitable where co-operation has been refused or withdrawn.

## 9. Interaction with discovery

Once the s.9A window has closed, no enquiry can be opened; the only route to additional tax is a discovery assessment under s.29 (SALF; EM1545). The relationship works in both directions:

- **s.29(5) protection is anchored to the enquiry.** Where the taxpayer has made a s.8/8A return, a discovery assessment is barred unless the loss of tax was brought about carelessly or deliberately (s.29(4)), or the officer could not reasonably have been expected to be aware of the situation on the basis of information made available before the enquiry window closed or the closure notice was issued (s.29(5)). "Information made available" is defined by s.29(6) to cover the return, accompanying documents, claims made in the same capacity, documents produced during the enquiry, and what is reasonably inferable from them. Objections that the s.29(4)/(5) conditions are not met can only be raised on appeal against the assessment (s.29(8)).
- **Prevailing practice.** s.29(2) protects a return made on the basis generally prevailing at the time (and see s.30B(3), Sch.18 FA 1998 para.45 for the partnership/company analogues).
- **Discovery during an open window.** EM2795 and EM, "Making a joint application to the tribunal", both note that an officer can *legally* make a discovery assessment while the enquiry window is open where the loss of tax was careless or deliberate — but HMRC's operational rule is to use the enquiry powers wherever possible (EM3201), to issue a determination rather than a discovery assessment where a notice to file has been issued and no return submitted (EM3202), and to require HO-grade authorisation for discovery assessments (EM3265).
- **Doctrines rejected.** Following *HMRC v Tooth* [2021] UKSC 17, EM3260 records that a discovery does not become "stale", and that there is no collective-knowledge principle: what matters is whether the officer making the assessment has subjectively made a discovery.
- **Time limits.** Sources in the notes differ. EM3235, citing ss.34 and 36 TMA 1970, gives a 4-year limit extendable to 20 years where the loss was careless or deliberate. EM3265/EM3220 states that where a return was submitted too late for the taxpayer to self-assess — normally treated by HMRC as carelessness — a discovery assessment may be made up to 6 years after the end of the tax year, and 20 years where there was a failure to notify chargeability. The ordinary limit for assessments other than self-assessments is 4 years after the end of the year of assessment (s.34(1)); a self-assessment itself must be made within 4 years (s.34A(1)), with a transitional 5 April 2017 backstop for years before 2012-13 (s.34A(4)).
- **Partnerships.** Where a partnership statement exists, HMRC uses a s.30B(1) discovery amendment to the partnership return, with consequential amendments to each partner's return under s.30B(2); otherwise s.29 assessments are made on individual partners. EM3235 states HMRC cannot use s.29 to challenge a partner's figure that simply matches the partnership return.
- **Sch.36 in a discovery context.** A taxpayer notice can be issued outside an open enquiry where a "potential discovery position" exists — reason to suspect under-assessment or excessive relief which, if true, could be corrected by assessment (CH23540; CH206600).

## 10. Statute compared with HMRC's own account

| Point | Statute | HMRC guidance |
|---|---|---|
| Types of enquiry | No distinction; one enquiry into "the return" | "Full" and "aspect" enquiries are internal classifications only; EM7551 says the legislation does not distinguish them and the terms should not be used in taxpayer communications |
| Scope stated in the opening letter | Enquiry covers the whole return | EM1905: legally the whole return is in scope even where the letter said otherwise; EM1560: officers should still say whether the enquiry is into the whole return or specific entries |
| Reason for opening | Not required to be given | EM1560: officers must not tell the taxpayer why the enquiry was opened; EM0093: random selection must never be disclosed. Contrast CH206150 ("openness and early dialogue"), under which caseworkers tell the person the risk or reason for the check at the start |
| Jeopardy amendment triggers | s.9C states only the insufficiency/loss-of-tax test | EM1951–EM1953: the listed circumstances are HMRC guidance; EM1952 is partly withheld under FOIA |
| Certificate of full disclosure | No statutory basis | EM3811: HMRC practice only; a fraudulently false certificate may be a criminal offence (*Regina v Hudson*, 36 TC 561) |
| Timeliness | No statutory duty on HMRC to progress an enquiry | EM1814: 15 working day turnaround target; EM1811: intervention plan and audit trail. Both are internal targets |
| Confirming no enquiry | None | SALF: HMRC is under no obligation to confirm that a return has been accepted without enquiry |
| Discovery while the window is open | Permitted where the loss of tax was careless or deliberate | EM3201/EM2795: HMRC's normal practice is to enquire instead; EM3265: HO-grade authorisation required |
| Extra-statutory relief for HMRC delay | — | SAM121450 and SAM101120 state HMRC's view that ESC A19 will not normally apply in SA cases, because the enquiry window and the greater responsibility placed on the taxpayer under SA displace it |

## Gaps in the sources

- The supplied notes contain **no customer-facing GOV.UK guidance**. Everything here is legislation or HMRC internal manuals; the page therefore cannot compare the simplified public-facing account with the statute.
- Only ss.9A–9C, 29, 30B, 34–35 and Sch.18 FA 1998 paras.41–45 are present as **primary legislative text**. Sections 28A, 28B, 28ZA–28ZE, 12AC and Sch.1A, and FA 2008 Sch.36, are known here only through manual summaries; the exact statutory wording of the closure-notice provisions (including the "reasonable grounds" test in s.28A(4) and the s.28A(6) mechanics) is not in the notes.
- The **commencement of partial closure notices** is referenced only obliquely ("From 16 November 2017", EM1521 caveat); no note states the enacting provision or its transitional rules.
- **Discovery time limits** are stated inconsistently across EM3235 and EM3265/EM3220 (4/20 versus 6/20 years); both are given above without resolution, since s.36 itself is not reproduced in the notes.
- No **tribunal decisions on closure notice applications** are in the notes; the only case authority supplied is *HMRC v Tooth* (via EM3260), *Regina v Hudson*, *Rose v Humbles* and *Scorer v Olin Energy Systems*, cited only in passing.
- Codes of Practice 8 and 9 are not covered; COP11 is mentioned only in the context of enquiries into earlier years (EM3576/EM1552).
- Several relevant manual passages are **withheld under FOIA 2000** (EM1952, EM1805, EM1895, EM1981, EM2001–EM2002, EM7558, SAM32001/SAM32010, CH206550), so HMRC's full position on those points is not publicly available.

---

## Sources used on this page

This page was written by an LLM from structured notes extracted from the mirrored sources below. Always check the upstream source before relying on any figure or deadline.

- [hmrc-manual-artg](https://www.gov.uk/hmrc-internal-manuals/appeals-reviews-and-tribunals-guidance) - 1 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/artg.md`
- [hmrc-manual-ch](https://www.gov.uk/hmrc-internal-manuals/compliance-handbook) - 11 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/ch.md`
- [hmrc-manual-em](https://www.gov.uk/hmrc-internal-manuals/enquiry-manual) - 35 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/em.md`
- [hmrc-manual-salf](https://www.gov.uk/hmrc-internal-manuals/self-assessment-legal-framework) - 2 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/salf.md`
- [hmrc-manual-sam](https://www.gov.uk/hmrc-internal-manuals/self-assessment-manual) - 28 note(s) - mirrored at `corpus/hmrc-publications/policy-and-interpretation/manuals/sam.md`
- [tma-1970](https://www.legislation.gov.uk/ukpga/1970/9/contents) - 3 note(s) - mirrored at `corpus/legal-system/primary-legislation/acts/tma-1970.md`
