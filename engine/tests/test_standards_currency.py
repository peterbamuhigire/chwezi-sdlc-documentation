from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts import check_standards_currency as currency
from scripts.check_portable_paths import NotAssessed, tracked_files


def write(root: Path, files: dict[str, str]) -> list[str]:
    for name, body in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    return list(files)


def test_each_stale_citation_is_counted_once_per_line(tmp_path: Path) -> None:
    files = write(tmp_path, {
        "skill/SKILL.md": "IEEE Std 830-1998 and IEEE 830 on one line\nISO/IEC/IEEE 42010:2011\n29119-3:2013 here\n",
        "engine/gate.py": "# BS ISO/IEC/IEEE 29119-3:2013, 25010:2011, 29148:2011, 26514:2008\n",
    })
    counts = currency.count_lines(tmp_path, files)
    assert counts["ieee-830"] == 1
    assert counts["iso-42010-2011"] == 1
    assert counts["iso-29119-3-2013"] == 2
    assert counts["iso-25010-2011"] == counts["iso-29148-2011"] == counts["iso-26514-2008"] == 1


def test_history_under_docs_and_non_text_suffixes_are_not_scanned(tmp_path: Path) -> None:
    files = write(tmp_path, {"docs/audit.md": "IEEE 830\n", "data.json": "IEEE 830\n", "a.md": "clean\n"})
    assert sum(currency.count_lines(tmp_path, files).values()) == 0


def test_wcag_21_is_split_between_engine_and_domain_packs_and_superseded_lines_are_skipped(tmp_path: Path) -> None:
    files = write(tmp_path, {
        "03-design/README.md": "Specify WCAG 2.1 AA requirements.\nWCAG 2.1 AA is superseded here.\n",
        "domains/education/INDEX.md": "Key standards: WCAG 2.1 AA\n",
        "domains/retail/INDEX.md": "wcag-2.1 baseline\n",
    })
    counts = currency.count_lines(tmp_path, files)
    assert counts["wcag-2.1-engine"] == 1
    assert counts["wcag-2.1-domain-packs"] == 2


def test_a_count_above_its_ceiling_is_a_finding_and_below_is_a_note() -> None:
    counts = dict.fromkeys(currency.PATTERN_NAMES, 0)
    ceilings = dict.fromkeys(currency.PATTERN_NAMES, 0)
    counts["ieee-830"], ceilings["ieee-830"] = 5, 4
    counts["iso-42010-2011"], ceilings["iso-42010-2011"] = 1, 3
    findings, notes = currency.check(counts, ceilings)
    assert findings == ["ieee-830: 5 lines exceed the ceiling of 4"]
    assert notes == ["iso-42010-2011: 1 lines, ceiling 3 can be lowered"]


def test_baseline_must_name_every_pattern(tmp_path: Path) -> None:
    path = tmp_path / "baseline.json"
    path.write_text(json.dumps({"ceilings": {"ieee-830": 1}}), encoding="utf-8")
    with pytest.raises(ValueError):
        currency.load_ceilings(path)


def test_an_injected_extra_citation_fails_main(tmp_path: Path, monkeypatch, capsys) -> None:
    files = write(tmp_path, {"a.md": "IEEE 830\nIEEE 830\n"})
    ceilings = dict.fromkeys(currency.PATTERN_NAMES, 0)
    ceilings["ieee-830"] = 1
    baseline = tmp_path / "baseline.json"
    baseline.write_text(json.dumps({"ceilings": ceilings}), encoding="utf-8")
    monkeypatch.setattr(currency, "tracked_files", lambda root: files)
    monkeypatch.setattr("sys.argv", ["check_standards_currency.py", "--root", str(tmp_path), "--baseline", str(baseline)])
    assert currency.main() == 1
    assert "ieee-830: 2 lines exceed the ceiling of 1" in capsys.readouterr().out


def test_live_repository_is_within_its_committed_ceilings() -> None:
    try:
        counts = currency.count_lines(currency.ROOT, tracked_files(currency.ROOT))
    except NotAssessed as exc:
        pytest.skip(f"not a git checkout: {exc}")
    findings, _notes = currency.check(counts, currency.load_ceilings())
    assert findings == [], findings
