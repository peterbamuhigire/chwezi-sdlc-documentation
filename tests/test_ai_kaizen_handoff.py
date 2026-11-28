"""Regression checks for the small, versioned AI handoff example."""
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs/plans/ai-engine-kaizen/evidence/S05/handoff.json"


def validate(packet):
    cases = packet["cases"]
    if [case["id"] for case in cases] != ["K1", "K2", "K3", "K4"]:
        raise ValueError("Missing or ambiguous case")
    for case in cases:
        if not case.get("outcome", "").strip():
            raise ValueError(f"Missing outcome for {case['id']}")
        for key in ("spec", "fixture", "evaluation", "decision"):
            if not (ROOT / case[key]).is_file():
                raise ValueError(f"Broken {key} link for {case['id']}")
        spec = (ROOT / case["spec"]).read_text(encoding="utf-8")
        if case["requirement"] not in spec:
            raise ValueError(f"Requirement absent for {case['id']}")
    for case, key in zip(cases[:2], ("dataset", "corpus")):
        fixture = (ROOT / case["fixture"]).read_text(encoding="utf-8")
        if case["revision"] != packet[key] or case["revision"] not in fixture:
            raise ValueError(f"Revision mismatch for {case['id']}")


def packet():
    return json.loads(PACKET.read_text(encoding="utf-8"))


def test_complete_handoff():
    validate(packet())


@pytest.mark.parametrize(
    "field,value,expected",
    [
        ("revision", "tickets-v0", "Revision mismatch"),
        ("outcome", "", "Missing outcome"),
        ("evaluation", "missing-evaluation.md", "Broken evaluation link"),
    ],
)
def test_unusable_handoff(field, value, expected):
    changed = packet()
    changed["cases"][0][field] = value
    with pytest.raises(ValueError, match=expected):
        validate(changed)
