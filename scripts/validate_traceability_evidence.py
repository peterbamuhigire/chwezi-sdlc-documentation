#!/usr/bin/env python3
"""Validate a traceability evidence report without equating links with testability."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "references/traceability-evidence.schema.json"


def validate(path: Path) -> tuple[list[str], dict[str, int]]:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    report = json.loads(path.read_text(encoding="utf-8"))
    errors = [e.message for e in Draft202012Validator(schema).iter_errors(report)]
    requirements = report.get("requirements", []) if isinstance(report, dict) else []
    ids = [item.get("requirement_id") for item in requirements if isinstance(item, dict)]
    if len(ids) != len(set(ids)):
        errors.append("requirement_id values must be unique")
    counts = {
        "requirements": len(requirements),
        "goal_linked": sum(bool(x.get("business_goal_ids")) for x in requirements),
        "design_linked": sum(bool(x.get("design_ids")) for x in requirements),
        "test_linked": sum(bool(x.get("test_case_ids")) for x in requirements),
        "oracle_executable": sum(x.get("oracle_status") == "executable" for x in requirements),
        "open_owner_decisions": sum(bool(x.get("open_owner_decisions")) for x in requirements),
        "executed": sum(x.get("execution_status") != "not_run" for x in requirements),
    }
    return errors, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        errors, counts = validate(args.report)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    print(json.dumps(counts, sort_keys=True))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
