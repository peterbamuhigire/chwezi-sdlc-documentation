#!/usr/bin/env python3
"""Fail when a current source record has no review date or its review date has passed.

Registers are Markdown tables kept per kaizen cycle at `docs/kaizen/<cycle>/standards-source-register.md`.
A record row starts with a claim identifier (`C-...`) and carries a review-by date in the column whose
header contains "review". Registers are read oldest to newest and a newer register supersedes an older
one for the same claim identifier, so a re-verified claim replaces its earlier record. Only the winning
record is checked.

A record with no review date must say why in that column ("no review date needed"); anything else is a
finding. A record that is due within `--warn-days` produces a note, not a failure.

Exit codes: 0 no findings, 1 findings, 2 no register found or unreadable.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GLOB = "docs/kaizen/*/standards-source-register.md"
CLAIM_ID = re.compile(r"^C-[A-Z0-9][A-Z0-9-]*$")
ISO_DATE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
EXEMPT = re.compile(r"no review date needed|historical-only", re.IGNORECASE)


@dataclass(frozen=True)
class Record:
    claim_id: str
    register: str
    line: int
    review_cell: str
    review_date: date | None


def split_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def first_date(text: str) -> date | None:
    """First valid ISO date in the text, using the 'review by' date when the cell has several."""
    preferred = re.search(r"review(?: by| date)?[: ]+(\d{4}-\d{2}-\d{2})", text, re.IGNORECASE)
    source = preferred.group(1) if preferred else (ISO_DATE.search(text).group(0) if ISO_DATE.search(text) else None)
    if source is None:
        return None
    try:
        return date.fromisoformat(source)
    except ValueError:
        return None


def parse_register(path: Path, name: str) -> tuple[list[Record], list[str]]:
    records: list[Record] = []
    problems: list[str] = []
    review_column: int | None = None
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.lstrip().startswith("|"):
            continue
        cells = split_cells(line)
        if cells and cells[0].lower() == "claim id":
            review_column = next((i for i, cell in enumerate(cells) if "review" in cell.lower()), None)
            continue
        if not cells or not CLAIM_ID.match(cells[0]):
            continue
        if review_column is None or review_column >= len(cells):
            problems.append(f"{name}:{number}: {cells[0]} has no review column to read")
            continue
        cell = cells[review_column]
        records.append(Record(cells[0], name, number, cell, first_date(cell)))
    return records, problems


def effective_records(paths: list[Path], root: Path) -> tuple[list[Record], list[str]]:
    winners: dict[str, Record] = {}
    problems: list[str] = []
    for path in sorted(paths):
        name = path.relative_to(root).as_posix() if path.is_relative_to(root) else path.name
        records, issues = parse_register(path, name)
        problems.extend(issues)
        for record in records:
            winners[record.claim_id] = record
    return list(winners.values()), problems


def check(records: list[Record], today: date, warn_days: int) -> tuple[list[str], list[str]]:
    findings: list[str] = []
    notes: list[str] = []
    horizon = today + timedelta(days=warn_days)
    for record in records:
        where = f"{record.register}:{record.line}"
        if record.review_date is None:
            if not EXEMPT.search(record.review_cell):
                findings.append(f"missing-review-date {record.claim_id} ({where}): add a review-by date or state why none is needed")
        elif record.review_date < today:
            findings.append(f"overdue {record.claim_id} ({where}): review date {record.review_date} is before {today}")
        elif record.review_date <= horizon:
            notes.append(f"due-soon {record.claim_id} ({where}): review date {record.review_date}")
    return findings, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (default: this checkout)")
    parser.add_argument("registers", nargs="*", type=Path, help="register files (default: every kaizen cycle register)")
    parser.add_argument("--today", type=date.fromisoformat, default=None, help="override today's date (YYYY-MM-DD)")
    parser.add_argument("--warn-days", type=int, default=14, help="report records due within this many days")
    args = parser.parse_args()
    paths = args.registers or sorted(args.root.glob(DEFAULT_GLOB))
    if not paths:
        print(f"ERROR: no source register found under {DEFAULT_GLOB}", file=sys.stderr)
        return 2
    try:
        records, problems = effective_records([Path(p) for p in paths], args.root)
    except OSError as exc:
        print(f"ERROR: cannot read register: {exc}", file=sys.stderr)
        return 2
    today = args.today or date.today()
    findings, notes = check(records, today, args.warn_days)
    findings = [f"unreadable-row {item}" for item in problems] + findings
    for line in findings:
        print(line)
    for line in notes:
        print(f"note {line}")
    print(
        f"source-register: {'FAIL' if findings else 'PASS'} ({len(findings)} finding(s)); "
        f"{len(records)} effective record(s) from {len(paths)} register(s) checked as of {today}"
    )
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
