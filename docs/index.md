# Self Assessment LLM Wiki

!!! danger "Unofficial - not HMRC, not advice, written by an LLM"

    This is an independent personal project. It is **not** HMRC, is **not**
    endorsed by or affiliated with HMRC or any government body, and nothing
    on it is tax advice. Every page is **written by a language model** from
    mirrored source material and can be wrong, incomplete or out of date.
    Official guidance is at
    [GOV.UK](https://www.gov.uk/self-assessment-tax-returns); if something
    here matters to you, check it against the source each page cites, or ask
    a qualified adviser.

A reference on UK **Self Assessment** (Income Tax), written by an LLM from a
continuously refreshed mirror of the primary material: the legislation that
creates the obligations, the tribunal decisions that interpret it, HMRC's own
manuals and policy publications, and the customer-facing guidance that
implements it.

Every page here is generated. Nothing on it is written from the model's own
knowledge of tax law — each page is composed only from structured notes
extracted from mirrored source documents, and every rule, figure and deadline
carries a citation back to the provision it came from. Pages list the sources
they drew on at the foot.

## How to read this site

Use the navigation. The sections, in order:

- **The Self Assessment lifecycle** is the spine: who is brought in, what the
  return is, when it is due, how the money is paid, and what follows through
  enquiry, assessment, penalty and appeal.
- **What the return computes** covers the income charges, the reliefs and
  claims, and the rates and thresholds.
- **HMRC's published position** is about status: what a manual, a Statement of
  Practice or a concession actually binds.
- **Reference implementation** is the forward-looking part — see
  [data model notes](reference-implementation/data-model-notes.md).
- **Meta** explains the machinery
  ([how this wiki stays current](meta/refresh-process.md)), lists every
  [tracked source](meta/sources.md), and reports
  [how much of the corpus has been read](meta/wiki-status.md) so far.

Sections whose pages have not been composed yet do not appear in the
navigation at all; [wiki status](meta/wiki-status.md) lists every planned page
and whether it exists.

## Three layers, not one

```
upstream sources          corpus/              extracts/            docs/
legislation.gov.uk   ->   raw mirrored    ->   structured JSON  ->  this wiki
GOV.UK Content API        markdown,            notes per chunk,     (LLM-written,
HMRC manuals              deterministic        cached by hash       cited)
Find Case Law             fetch                (LLM)                (LLM)
```

The mirror and the notes both live in the repository. That matters for two
reasons: you can always check what a page was written from, and a refresh
only re-reads the chunks that actually changed. See
[How this wiki stays current](meta/refresh-process.md).

## Scope

Coverage is prioritised for Self Assessment specifically. Some sources are
**registered** — tracked in the registry so they can be pulled in cheaply —
without being mirrored yet; [Sources](meta/sources.md) marks which.
[Wiki status](meta/wiki-status.md) shows what proportion of the mirrored
corpus has actually been read by the extraction stage, which is the honest
measure of how complete these pages are.

## Looking ahead: a head-of-duty reference implementation

The goal beyond this wiki is a reference implementation that can compute Self
Assessment obligations directly — who must file, what is owed, by when, and
what follows if it is late or wrong. The rules inventory and data requirements
pages in the reference implementation section are generated specifically to
feed that, alongside the hand-written
[data model notes](reference-implementation/data-model-notes.md). That
implementation is **not** started here.

## Not official, not advice, LLM-written

Nothing here is an HMRC publication, and no part of this site is produced,
reviewed, endorsed or approved by HMRC or any government body. HMRC material
is quoted and linked as a *source*; the words on these pages are not HMRC's.
It is not tax, legal or financial advice, and no professional relationship
arises from reading it.

It is a research aid with three distinct failure modes, and all three matter:

1. The mirror can be stale or incomplete relative to upstream.
2. Only part of the mirrored corpus has been read - see
   [wiki status](meta/wiki-status.md).
3. The pages are **written by a language model**. The prompts forbid adding
   facts not present in the source notes and require a citation for every
   figure, but summarisation errors, missed conditions and dropped edge cases
   are still possible.

Check any figure, date or rule against the cited source before relying on it,
and take advice from a qualified professional for anything that matters.
