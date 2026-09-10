"""Recognise the citations a generated page makes, so they can be checked.

`prompts/compose.md` tells the model to cite every rule, figure, deadline and
penalty with a `ref` taken from the supplied notes, and to invent nothing. The
first half of that is visible in the output; the second is not. A page can
carry a perfectly formatted `(TMA 1970 s.122AA(2))` that appears in no note it
was given - and the citation *looks* like provenance, which is worse than
having none.

So the audit reads both sides as a set of citation tokens and asks whether
each token on the page also appears in the notes the page selected. Two token
families are recognised, because they are the two the sources actually use:

- **manual references** - `SAM100050`, `CH61180`, `EM7524`, `SALF910`: two to
  six capitals then three to seven digits. Form and leaflet numbers (`SA100`,
  `CWF1`, `IHT400`) share that shape and are not citations of text, so their
  prefixes are excluded.
- **section references** - normalised to `s.<number><letters>`, dropping any
  subsection. One provision is written at least four ways across the corpus
  (`TMA 1970 s.12B(5)`, `Section 12B(5)`, `TMA70/S12B`, `s 12B`), so all four
  spellings normalise to the same token; otherwise the check would report a
  citation as unsupported purely because the note spelled it differently.

Matching is deliberately at provision level rather than subsection level. A
page that cites `s.9(2)` from a note about `s.9(1)` is doing ordinary drafting
work; a page that cites a section no note mentions is not.
"""
from __future__ import annotations

import re

# `SAM100050`, `CH61180`, `EM7524`. Bounded on the right by a non-digit so a
# longer number is not read as a shorter code plus digits.
_MANUAL = re.compile(r"\b([A-Z]{2,6})(\d{3,7})\b")

# Prefixes of the same shape that name a *form* or leaflet rather than a piece
# of manual text: SA100, SA400, CWF1, CF83, IHT400, HS340, CT600, TC600. The
# corresponding manuals all have longer prefixes (SAM, CTM, ...), so excluding
# these costs no real citation.
_FORM_PREFIXES = frozenset({"SA", "CWF", "CF", "IHT", "VAT", "NIC",
                            "HS", "CT", "COP", "TC"})

# The section spellings seen in the corpus, all yielding the bare provision:
#   "s.12B(5)" / "s. 12B"   "section 12B" / "Sections 12B"   "TMA70/S12B"
#   "s 12B"
_SECTION_FORMS = (
    re.compile(r"\bs\.\s?(\d+[A-Z]{0,3})"),
    re.compile(r"\b[Ss]ections?\s+(\d+[A-Z]{0,3})"),
    re.compile(r"/[Ss]\.?\s?(\d+[A-Z]{0,3})"),
    re.compile(r"\bs\s(\d+[A-Z]{0,3})\b"),
)


def tokens(text: str) -> set[str]:
    """Every manual and section citation `text` makes, normalised."""
    found: set[str] = set()
    for prefix, digits in _MANUAL.findall(text):
        if prefix not in _FORM_PREFIXES:
            found.add(f"{prefix}{digits}")
    for pattern in _SECTION_FORMS:
        found.update(f"s.{m}" for m in pattern.findall(text))
    return found


def unsupported(page_text: str, note_text: str) -> list[str]:
    """Citations the page makes that its own notes do not, sorted."""
    return sorted(tokens(page_text) - tokens(note_text))
