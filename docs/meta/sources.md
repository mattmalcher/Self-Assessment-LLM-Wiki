---
title: Sources
---

# Sources

Generated from `pipeline/sources.yml` - **do not hand-edit this file**, it is overwritten on every pipeline run (`uv run sources-index`, or automatically at the end of `uv run fetch`).

These are the *raw* sources. The fetch pipeline mirrors them into `corpus/` in the repository; the wiki pages you are reading are written from that mirror by the synthesis layer - see [How this wiki stays current](refresh-process.md).

32 registered sources: 29 mirrored, 3 registered-only.

## external-explainers

| Source | Status | Type | Last checked | Upstream updated |
|---|---|---|---|---|
| [taxaid-self-assessment](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/external-explainers.md) | fetch | `web_page` | 2026-09-10 | - |
| Self assessment and tax returns - Low Incomes Tax Reform Group (LITRG) | registered | `web_page` | - | - |

## hmrc-publications.customer-facing-guidance

| Source | Status | Type | Last checked | Upstream updated |
|---|---|---|---|---|
| [sa-helpsheets](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/hmrc-publications/customer-facing-guidance/helpsheets/index.md) | fetch | `govuk_content_collection` | 2026-09-04 | 2014-07-04T00:00:00+01:00 |
| [govuk-sa-detailed-information](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/hmrc-publications/customer-facing-guidance/govuk-guidance.md) | fetch | `govuk_content_collection` | 2026-09-10 | 2024-02-12T00:00:00+00:00 |
| [govuk-mtd-income-tax-guide](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/hmrc-publications/customer-facing-guidance/making-tax-digital-income-tax.md) | fetch | `govuk_content_manual` | 2026-09-10 | - |
| VAT notices (numerical order) | registered | `govuk_content_collection` | - | - |

## hmrc-publications.customer-facing-tools

| Source | Status | Type | Last checked | Upstream updated |
|---|---|---|---|---|
| [hmrc-tools-calculators](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/hmrc-publications/customer-facing-tools.md) | fetch | `govuk_content` | 2026-09-04 | 2026-08-14T10:54:46+01:00 |

## hmrc-publications.policy-and-interpretation

| Source | Status | Type | Last checked | Upstream updated |
|---|---|---|---|---|
| [hmrc-escs](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/hmrc-publications/policy-and-interpretation/extra-statutory-concessions.md) | fetch | `govuk_content_collection` | 2026-09-04 | 2017-04-21T13:20:24+01:00 |
| [hmrc-statements-of-practice](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/hmrc-publications/policy-and-interpretation/statements-of-practice.md) | fetch | `govuk_content_collection` | 2026-09-04 | 2010-01-01T00:00:00+00:00 |
| [hmrc-rc-briefs](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/hmrc-publications/policy-and-interpretation/revenue-and-customs-briefs.md) | fetch | `govuk_content_collection` | 2026-09-04 | 2026-08-03T08:34:57+01:00 |

## hmrc-publications.policy-and-interpretation.manuals

| Source | Status | Type | Last checked | Upstream updated |
|---|---|---|---|---|
| [hmrc-manual-artg](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/hmrc-publications/policy-and-interpretation/manuals/artg.md) | fetch | `govuk_content_manual` | 2026-09-04 | - |
| [hmrc-manual-ch](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/hmrc-publications/policy-and-interpretation/manuals/ch.md) | fetch | `govuk_content_manual` | 2026-09-04 | - |
| [hmrc-manual-em](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/hmrc-publications/policy-and-interpretation/manuals/em.md) | fetch | `govuk_content_manual` | 2026-09-04 | - |
| [hmrc-manuals-index](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/hmrc-publications/policy-and-interpretation/manuals/index.md) | fetch | `govuk_content_collection` | 2026-09-04 | 2026-09-02T11:39:31+01:00 |
| [hmrc-manual-salf](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/hmrc-publications/policy-and-interpretation/manuals/salf.md) | fetch | `govuk_content_manual` | 2026-09-04 | - |
| [hmrc-manual-sam](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/hmrc-publications/policy-and-interpretation/manuals/sam.md) | fetch | `govuk_content_manual` | 2026-09-04 | - |

## hmrc-publications.rates-and-allowances

| Source | Status | Type | Last checked | Upstream updated |
|---|---|---|---|---|
| [hmrc-rates-allowances](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/hmrc-publications/rates-and-allowances.md) | fetch | `govuk_content_collection` | 2026-09-10 | 2025-08-22T11:48:48+01:00 |

## legal-system.case-law

| Source | Status | Type | Last checked | Upstream updated |
|---|---|---|---|---|
| [caselaw-ftt-tc](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/legal-system/case-law/first-tier-tribunal-tax-chamber.md) | fetch | `caselaw_feed` | 2026-09-04 | - |
| [caselaw-ut-tcc](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/legal-system/case-law/upper-tribunal-tax-chancery.md) | fetch | `caselaw_feed` | 2026-09-04 | - |

## legal-system.primary-legislation

| Source | Status | Type | Last checked | Upstream updated |
|---|---|---|---|---|
| [crca-2005](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/legal-system/primary-legislation/acts/crca-2005.md) | fetch | `legislation` | 2026-09-04 | - |
| [finance-act-2008](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/legal-system/primary-legislation/acts/finance-act-2008.md) | fetch | `legislation` | 2026-09-10 | - |
| [finance-act-2009](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/legal-system/primary-legislation/acts/finance-act-2009.md) | fetch | `legislation` | 2026-09-10 | - |
| [finance-act-2021](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/legal-system/primary-legislation/acts/finance-act-2021.md) | fetch | `legislation` | 2026-09-10 | - |
| [itepa-2003](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/legal-system/primary-legislation/acts/itepa-2003.md) | fetch | `legislation` | 2026-09-04 | - |
| [ittoia-2005](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/legal-system/primary-legislation/acts/ittoia-2005.md) | fetch | `legislation` | 2026-09-10 | - |
| [ita-2007](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/legal-system/primary-legislation/acts/ita-2007.md) | fetch | `legislation` | 2026-09-10 | - |
| [sscba-1992](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/legal-system/primary-legislation/acts/sscba-1992.md) | fetch | `legislation` | 2026-09-10 | - |
| [tcga-1992](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/legal-system/primary-legislation/acts/tcga-1992.md) | fetch | `legislation` | 2026-09-10 | - |
| [tma-1970](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/legal-system/primary-legislation/acts/tma-1970.md) | fetch | `legislation` | 2026-09-04 | - |

## legal-system.secondary-legislation

| Source | Status | Type | Last checked | Upstream updated |
|---|---|---|---|---|
| [si-income-tax-digital-requirements-2021](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/legal-system/secondary-legislation/income-tax-digital-requirements-regulations-2021.md) | fetch | `legislation` | 2026-09-10 | - |
| Statutory Instruments search (tax) | registered | `web_page` | - | - |
| [si-ftt-tax-chamber-rules-2009](https://github.com/mattmalcher/Self-Assessment-LLM-Wiki/blob/main/corpus/legal-system/secondary-legislation/tribunal-procedure-ftt-tax-chamber-rules-2009.md) | fetch | `legislation` | 2026-09-04 | - |

