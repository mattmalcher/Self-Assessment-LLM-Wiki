"""Durable run reports, shared by all three pipeline stages.

A run that fetched 40 of 41 sources, or composed 11 of 12 pages, is not a
successful run: without this module the only trace of the missing unit was a
line of stderr that scrolled past. Every stage therefore builds a
`StageReport` of what it attempted, what it finished, what failed and what it
knowingly left for the next run, prints a one-line verdict and writes the
whole thing to a JSON file that CI can read back.

The default is strict: any failed unit makes the command exit non-zero.
Best-effort behaviour is available, but only behind an explicit
`--keep-going`, so no scheduled run can report a partial refresh as a
complete one.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# Schema version of the JSON below: bump when a consumer would have to change.
REPORT_VERSION = 1


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class StageReport:
    """What one stage did to its units of work (a source, chunk or page)."""

    stage: str
    unit: str  # what a unit *is* here, for whoever reads the JSON
    succeeded: list[str] = field(default_factory=list)
    failed: list[dict] = field(default_factory=list)
    remaining: list[str] = field(default_factory=list)
    started_at: str = field(default_factory=now)
    finished_at: str = ""
    # Stage-specific counts (changed sources, pruned cache entries, ...).
    extra: dict = field(default_factory=dict)

    def succeed(self, unit_id: str) -> None:
        self.succeeded.append(unit_id)

    def fail(self, unit_id: str, error: object) -> None:
        self.failed.append({"unit": unit_id, "error": str(error)})

    @property
    def ok(self) -> bool:
        """Remaining work is deliberate (`--limit`); a failure never is."""
        return not self.failed

    @property
    def attempted(self) -> int:
        return len(self.succeeded) + len(self.failed)

    def as_dict(self) -> dict:
        return {
            "stage": self.stage,
            "unit": self.unit,
            "ok": self.ok,
            "started_at": self.started_at,
            "finished_at": self.finished_at or now(),
            "attempted": self.attempted,
            "succeeded": self.succeeded,
            "failed": self.failed,
            "remaining": self.remaining,
            **self.extra,
        }

    def verdict(self, *, keep_going: bool = False) -> str:
        """The line a human reads to know whether the run can be trusted."""
        counts = (f"{len(self.succeeded)} ok, {len(self.failed)} failed"
                  + (f", {len(self.remaining)} not attempted" if self.remaining else ""))
        if self.ok:
            return f"{self.stage}: {counts}"
        note = " (--keep-going: exiting 0 anyway)" if keep_going else ""
        return f"{self.stage}: PARTIAL - {counts}{note}"

    def exit_code(self, *, keep_going: bool = False) -> int:
        return 0 if self.ok or keep_going else 1


def write(path: Path, reports: list[StageReport]) -> None:
    """Write the machine-readable report CI reads back."""
    for report in reports:
        report.finished_at = report.finished_at or now()
    payload = {
        "version": REPORT_VERSION,
        "written_at": now(),
        "ok": all(r.ok for r in reports),
        "stages": [r.as_dict() for r in reports],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def failure_lines(reports: list[StageReport]) -> list[str]:
    """Markdown bullets naming every failed unit, for a PR body."""
    return [f"- `{f['unit']}`: {f['error']}" for r in reports for f in r.failed]
