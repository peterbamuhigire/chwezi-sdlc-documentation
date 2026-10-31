#!/usr/bin/env python3
"""Ratchet on citations of superseded standards and on engine templates that prescribe WCAG 2.1.

The count of each stale pattern in live content (tracked `.md` and `.py` files outside `docs/`)
may fall but never rise above the ceiling committed in `tests/standards-currency-baseline.json`.
The scan does not decide whether a citation is acceptable (IEEE 830 is kept as an SRS layout
reference by the router) and does not remap clauses; it stops the debt growing unnoticed and
shows when a ceiling can be lowered. Edition status is recorded, with sources and review dates,
in the source register of the current kaizen cycle.

Patterns:
- `ieee-830`, `iso-42010-2011`, `iso-29119-3-2013`, `iso-25010-2011`, `iso-29148-2011`,
  `iso-26514-2008`: citations of editions that the issuers list as superseded or withdrawn.
- `wcag-2.1-engine`: a line outside `domains/` naming WCAG 2.1, except a line that says it is
  superseded. Engine templates target WCAG 2.2 AA.
- `wcag-2.1-domain-packs`: the same under `domains/`, where the packs record jurisdiction-bound
  baselines that need an owner decision before they change.

Exit codes: 0 within ceilings, 1 above a ceiling, 2 not assessed (not a git checkout).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_portable_paths import NotAssessed, tracked_files  # noqa: E402

BASELINE = ROOT / "tests" / "standards-currency-baseline.json"
SCANNED_SUFFIXES = (".md", ".py")
# The checker, its tests and its baseline hold the patterns as data, not as citations.
SELF = {
    "scripts/check_standards_currency.py",
    "engine/tests/test_standards_currency.py",
}
CITATIONS = {
    "ieee-830": re.compile(r"IEEE (?:Std )?830", re.IGNORECASE),
    "iso-42010-2011": re.compile(r"42010[: -]*2011"),
    "iso-29119-3-2013": re.compile(r"29119-3[: -]*2013"),
    "iso-25010-2011": re.compile(r"25010[: -]*2011"),
    "iso-29148-2011": re.compile(r"29148[: -]*2011"),
    "iso-26514-2008": re.compile(r"26514[: -]*2008"),
}
WCAG_21 = re.compile(r"WCAG[ -]*2\.1", re.IGNORECASE)
PATTERN_NAMES = (*CITATIONS, "wcag-2.1-engine", "wcag-2.1-domain-packs")


def live_files(files: list[str]) -> list[str]:
    return [
        rel for rel in files
        if rel.endswith(SCANNED_SUFFIXES) and not rel.startswith("docs/") and rel not in SELF
    ]


def count_lines(root: Path, files: list[str]) -> dict[str, int]:
    counts = dict.fromkeys(PATTERN_NAMES, 0)
    for rel in live_files(files):
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line in text.splitlines():
            for name, pattern in CITATIONS.items():
                if pattern.search(line):
                    counts[name] += 1
            if WCAG_21.search(line) and "superseded" not in line.lower():
                counts["wcag-2.1-domain-packs" if rel.startswith("domains/") else "wcag-2.1-engine"] += 1
    return counts


def load_ceilings(path: Path = BASELINE) -> dict[str, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    ceilings = data["ceilings"]
    missing = [name for name in PATTERN_NAMES if name not in ceilings]
    if missing:
        raise ValueError(f"baseline lacks ceilings for: {', '.join(missing)}")
    return {name: int(ceilings[name]) for name in PATTERN_NAMES}


def check(counts: dict[str, int], ceilings: dict[str, int]) -> tuple[list[str], list[str]]:
    """Return (findings, notes). A count above its ceiling is a finding; below it is a note."""
    findings, notes = [], []
    for name in PATTERN_NAMES:
        if counts[name] > ceilings[name]:
            findings.append(f"{name}: {counts[name]} lines exceed the ceiling of {ceilings[name]}")
        elif counts[name] < ceilings[name]:
            notes.append(f"{name}: {counts[name]} lines, ceiling {ceilings[name]} can be lowered")
    return findings, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (default: this checkout)")
    parser.add_argument("--baseline", type=Path, default=BASELINE)
    parser.add_argument("--print-counts", action="store_true", help="print the current counts as JSON and exit")
    args = parser.parse_args()
    try:
        counts = count_lines(args.root, tracked_files(args.root))
    except NotAssessed as exc:
        print(f"NOT_ASSESSED: {exc}", file=sys.stderr)
        return 2
    if args.print_counts:
        print(json.dumps(counts, indent=2))
        return 0
    findings, notes = check(counts, load_ceilings(args.baseline))
    for line in findings:
        print(f"standards-currency {line}")
    for line in notes:
        print(f"note {line}")
    print(f"standards-currency: {'FAIL' if findings else 'PASS'} ({len(findings)} finding(s))")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
