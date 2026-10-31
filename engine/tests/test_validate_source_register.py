from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from scripts import validate_source_register as register

HEADER = (
    "| Claim ID | Claim in scope | Source and tier | Publication; accessed | Freshness; review date | Support state |\n"
    "|---|---|---|---|---|---|\n"
)


def row(claim: str, review: str) -> str:
    return f"| {claim} | claim | source | 2026-10-01 | {review} | `supported` |\n"


def write(path: Path, body: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def run(paths: list[Path], root: Path, today: str = "2026-10-31", warn: int = 14):
    records, problems = register.effective_records(paths, root)
    findings, notes = register.check(records, date.fromisoformat(today), warn)
    return records, problems, findings, notes


def test_future_review_date_passes_and_past_date_is_overdue(tmp_path: Path) -> None:
    path = write(tmp_path / "r.md", HEADER + row("C-A", "Time-sensitive; review by 2027-01-31") + row("C-B", "Time-sensitive; review by 2026-10-30"))
    _, _, findings, _ = run([path], tmp_path)
    assert len(findings) == 1 and findings[0].startswith("overdue C-B")


def test_review_date_equal_to_today_is_not_overdue(tmp_path: Path) -> None:
    path = write(tmp_path / "r.md", HEADER + row("C-A", "review by 2026-10-31"))
    _, _, findings, notes = run([path], tmp_path)
    assert findings == [] and notes and notes[0].startswith("due-soon C-A")


def test_row_without_a_date_is_a_finding_unless_it_states_why(tmp_path: Path) -> None:
    path = write(tmp_path / "r.md", HEADER + row("C-A", "Time-sensitive") + row("C-B", "Historical-only; no review date needed for this fact"))
    _, _, findings, _ = run([path], tmp_path)
    assert len(findings) == 1 and findings[0].startswith("missing-review-date C-A")


def test_invalid_calendar_date_counts_as_missing(tmp_path: Path) -> None:
    path = write(tmp_path / "r.md", HEADER + row("C-A", "review by 2026-13-45"))
    _, _, findings, _ = run([path], tmp_path)
    assert len(findings) == 1 and findings[0].startswith("missing-review-date C-A")


def test_review_by_date_wins_over_other_dates_in_the_cell(tmp_path: Path) -> None:
    path = write(tmp_path / "r.md", HEADER + row("C-A", "Checked 2020-01-01; review by 2027-06-30"))
    records, _, findings, _ = run([path], tmp_path)
    assert records[0].review_date == date(2027, 6, 30) and findings == []


def test_newer_register_supersedes_the_same_claim_and_older_claims_remain(tmp_path: Path) -> None:
    old = write(tmp_path / "docs/kaizen/2026-10-a/standards-source-register.md", HEADER + row("C-A", "review by 2026-01-01") + row("C-B", "review by 2026-11-01"))
    new = write(tmp_path / "docs/kaizen/2026-10-b/standards-source-register.md", HEADER + row("C-A", "review by 2027-01-31"))
    records, _, findings, _ = run([old, new], tmp_path)
    assert {r.claim_id: r.review_date for r in records} == {"C-A": date(2027, 1, 31), "C-B": date(2026, 11, 1)}
    assert findings == []


def test_rows_after_a_blank_line_still_use_the_last_header(tmp_path: Path) -> None:
    path = write(tmp_path / "r.md", HEADER + row("C-A", "review by 2027-01-31") + "\n" + row("C-B", "review by 2026-01-01"))
    _, _, findings, _ = run([path], tmp_path)
    assert len(findings) == 1 and findings[0].startswith("overdue C-B")


def test_record_row_before_any_header_is_reported_unreadable(tmp_path: Path) -> None:
    path = write(tmp_path / "r.md", row("C-A", "review by 2027-01-31"))
    records, problems, _, _ = run([path], tmp_path)
    assert records == [] and problems and "C-A" in problems[0]


def test_non_claim_rows_are_ignored(tmp_path: Path) -> None:
    path = write(tmp_path / "r.md", HEADER + "| Other | x | y | z | 2020-01-01 | w |\n" + row("C-A", "review by 2027-01-31"))
    records, _, findings, _ = run([path], tmp_path)
    assert [r.claim_id for r in records] == ["C-A"] and findings == []


def test_main_exit_codes(tmp_path: Path, monkeypatch, capsys) -> None:
    write(tmp_path / "docs/kaizen/c1/standards-source-register.md", HEADER + row("C-A", "review by 2026-01-01"))
    monkeypatch.setattr("sys.argv", ["validate_source_register.py", "--root", str(tmp_path), "--today", "2026-10-31"])
    assert register.main() == 1
    assert "overdue C-A" in capsys.readouterr().out
    monkeypatch.setattr("sys.argv", ["validate_source_register.py", "--root", str(tmp_path / "empty"), "--today", "2026-10-31"])
    assert register.main() == 2


def test_committed_registers_have_no_overdue_record_today() -> None:
    paths = sorted(register.ROOT.glob(register.DEFAULT_GLOB))
    if not paths:
        pytest.skip("no kaizen source register in this checkout")
    records, problems = register.effective_records(paths, register.ROOT)
    findings, _ = register.check(records, date(2026, 10, 31), 14)
    assert records and findings == [] and problems == []
