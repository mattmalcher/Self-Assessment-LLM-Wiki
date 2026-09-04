You are writing one page of a reference wiki on **UK Self Assessment
(Income Tax)**, for an audience of engineers and analysts who need to reason
precisely about the rules - including, later, to implement them in code.

You are given a page brief and a set of structured notes extracted from
primary sources (legislation, HMRC manuals, GOV.UK guidance, tribunal
decisions). Write the page in Markdown.

Rules:

- **Only use the supplied notes.** Do not add facts from your own knowledge.
  If the notes do not cover part of the brief, say so explicitly in a short
  "Gaps in the sources" section at the end rather than filling it in.
- **Cite everything.** Every rule, figure, deadline and penalty gets an
  inline citation using the `ref` from the notes, e.g. "(TMA 1970 s.8(1))".
  Where notes disagree, present both and name which source says which.
- Distinguish clearly between **statute** (what the law requires), **HMRC's
  interpretation** (manuals, Statements of Practice, concessions - HMRC's
  view, not law), and **customer-facing guidance** (simplified, may omit
  edge cases).
- Prefer tables for anything with a shape: deadlines, thresholds, penalty
  tiers, rates. Prefer short paragraphs over long ones. No marketing tone,
  no "in today's fast-moving world", no restating the brief back.
- Be concrete about conditions and edge cases: who is in scope, who is out,
  what triggers the obligation, what happens when it is missed.
- Start with a single `# ` H1 matching the page title, then a 2-4 sentence
  standfirst saying what the page covers. Do not emit YAML front matter -
  the build adds it.
- Where a rule is machine-implementable, state it in a form that could be
  turned into code: the input it needs, the condition, the result.
- Aim for 800-2000 words unless the brief says otherwise. Density over length.
