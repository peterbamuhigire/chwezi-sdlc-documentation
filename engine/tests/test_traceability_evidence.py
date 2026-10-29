import json
from pathlib import Path

from scripts.validate_traceability_evidence import validate


FIXTURE = Path(__file__).parent / "fixtures/traceability-evidence.json"


def test_report_separates_links_oracles_decisions_and_execution():
    errors, counts = validate(FIXTURE)
    assert errors == []
    assert counts == {
        "requirements": 10,
        "goal_linked": 0,
        "design_linked": 10,
        "test_linked": 10,
        "oracle_executable": 3,
        "open_owner_decisions": 7,
        "executed": 0,
    }


def test_duplicate_requirement_ids_are_rejected(tmp_path):
    report = json.loads(FIXTURE.read_text(encoding="utf-8"))
    report["requirements"].append(report["requirements"][0])
    path = tmp_path / "duplicate.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    errors, _ = validate(path)
    assert "requirement_id values must be unique" in errors
