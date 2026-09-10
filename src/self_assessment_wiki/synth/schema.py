"""The note schema `prompts/extract.md` asks for, as something enforceable.

`llm.extract_json` will happily return any balanced `{...}` the model emitted,
and before this existed the extract stage cached whatever came back. Three
committed records turned out to be a single nested obligation/penalty object
rather than a note; because their chunk hash was present the planner counted
them as done, and because they had no `relevance` the selector dropped them, so
their source text vanished between stages while `status` reported full
coverage.

So the rule is: a note that does not validate is not a note. It is never
persisted, never counted as cached, and never selected for a page.

Validation is deliberately strict - every documented key present, every value a
string, every `ref` non-empty, nothing extra. A key the prompt does not
describe is a sign the model improvised (`may` for `must`, `meaine` for
`meaning`), which is exactly the drift worth paying a retry to fix.
"""
from __future__ import annotations

RELEVANCE = ("core", "related", "none")

# Lists of plain strings.
STRING_LISTS = ("topics", "cross_references", "caveats")

# Lists of records, and the exact keys each record must carry. Every value is
# a string; `ref` additionally must be non-empty, because a note whose citation
# is blank cannot be checked against the source it claims to come from.
RECORD_LISTS: dict[str, tuple[str, ...]] = {
    "obligations": ("who", "must", "trigger", "deadline", "ref"),
    "deadlines": ("name", "rule", "applies_to", "ref"),
    "amounts": ("name", "value", "period", "ref"),
    "penalties": ("trigger", "consequence", "ref"),
    "definitions": ("term", "meaning", "ref"),
}

KEYS = ("relevance", "summary", *STRING_LISTS, *RECORD_LISTS)


def _check_record(errors: list[str], field: str, i: int, item: object) -> None:
    where = f"{field}[{i}]"
    if not isinstance(item, dict):
        errors.append(f"{where}: expected an object, got {type(item).__name__}")
        return
    required = RECORD_LISTS[field]
    for key in required:
        if key not in item:
            errors.append(f"{where}: missing key {key!r}")
    for key in sorted(set(item) - set(required)):
        errors.append(f"{where}: unexpected key {key!r}")
    for key in required:
        if key not in item:
            continue
        value = item[key]
        if not isinstance(value, str):
            errors.append(f"{where}.{key}: expected a string, got {type(value).__name__}")
        elif key == "ref" and not value.strip():
            errors.append(f"{where}.ref: citation is empty")


def validate_note(note: object) -> list[str]:
    """Every way `note` fails the schema, as human-readable messages.

    An empty list means valid. The messages are fed back to the model on a
    retry, so they name the offending path rather than just the rule.
    """
    if not isinstance(note, dict):
        return [f"note: expected a JSON object, got {type(note).__name__}"]

    errors: list[str] = []
    for key in KEYS:
        if key not in note:
            errors.append(f"missing key {key!r}")
    for key in sorted(set(note) - set(KEYS)):
        errors.append(f"unexpected key {key!r}")

    if "relevance" in note and note["relevance"] not in RELEVANCE:
        errors.append(f"relevance: expected one of {', '.join(RELEVANCE)}, "
                      f"got {note['relevance']!r}")
    if "summary" in note:
        summary = note["summary"]
        if not isinstance(summary, str):
            errors.append(f"summary: expected a string, got {type(summary).__name__}")
        elif not summary.strip():
            errors.append("summary: is empty")

    for field in STRING_LISTS:
        value = note.get(field)
        if field not in note:
            continue
        if not isinstance(value, list):
            errors.append(f"{field}: expected a list, got {type(value).__name__}")
            continue
        for i, item in enumerate(value):
            if not isinstance(item, str):
                errors.append(f"{field}[{i}]: expected a string, got {type(item).__name__}")
            elif not item.strip():
                errors.append(f"{field}[{i}]: is empty")

    for field in RECORD_LISTS:
        value = note.get(field)
        if field not in note:
            continue
        if not isinstance(value, list):
            errors.append(f"{field}: expected a list, got {type(value).__name__}")
            continue
        for i, item in enumerate(value):
            _check_record(errors, field, i, item)

    return errors


def is_valid(note: object) -> bool:
    return not validate_note(note)


def entry_is_valid(entry: object) -> bool:
    """Whether one cached `chunks[<hash>]` record holds a usable note."""
    return isinstance(entry, dict) and is_valid(entry.get("note"))
