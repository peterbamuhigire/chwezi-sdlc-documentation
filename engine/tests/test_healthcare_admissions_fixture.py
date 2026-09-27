from __future__ import annotations

import json
from pathlib import Path

from ruamel.yaml import YAML

from engine.artifact_graph import ArtifactGraph
from engine.checks.change_impact import ChangeImpactCheck
from engine.checks.fixture_manifest import validate_fixture_manifest
from engine.checks.test_oracles import TestOraclesCheck as _TestOraclesCheck
from engine.checks.traceability import TraceabilityCheck
from engine.findings import FindingCollection
from engine.gates.phase02 import Phase02Gate
from engine.workspace import Workspace

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "engine" / "tests" / "fixtures" / "healthcare_admissions"


def _graph_and_findings() -> tuple[ArtifactGraph, dict[str, FindingCollection]]:
    graph = ArtifactGraph.build(Workspace.load(FIXTURE))
    checks = {
        "phase02": FindingCollection(),
        "traceability": FindingCollection(),
        "test_oracles": FindingCollection(),
        "change_impact": FindingCollection(),
    }
    Phase02Gate().evaluate(graph, checks["phase02"])
    TraceabilityCheck("phase09.traceability").run(graph, checks["traceability"])
    _TestOraclesCheck("phase05.test_oracles").run(graph, checks["test_oracles"])
    ChangeImpactCheck("phase09.change_impact", FIXTURE).run(graph, checks["change_impact"])
    return graph, checks


def test_synthetic_admissions_fixture_passes_structural_gates() -> None:
    manifest = json.loads((FIXTURE / "fixture-manifest.json").read_text(encoding="utf-8"))
    assert manifest["classification"] == "behavioural"
    assert manifest["data_classification"] == "synthetic-test-only"
    assert validate_fixture_manifest(manifest) == []
    assert set(manifest["coverage"]) == {
        "facility-scope-denial",
        "interrupted-intake-duplicate",
        "unavailable-reference-data",
        "billing-handoff",
        "missing-signoff",
        "controlled-change-impact",
        "open-contradiction-is-not-approved",
    }

    _, checks = _graph_and_findings()
    assert {name: list(findings) for name, findings in checks.items()} == {
        "phase02": [],
        "traceability": [],
        "test_oracles": [],
        "change_impact": [],
    }


def test_synthetic_scenarios_have_oracles_and_unapproved_decisions_stay_open() -> None:
    requirements = (FIXTURE / "02-requirements-engineering" / "requirements.md").read_text(encoding="utf-8")
    decision_log = (FIXTURE / "03-design-documentation" / "decision-log.md").read_text(encoding="utf-8")
    assert all(f"FR-{number:03d}" in requirements for number in range(1, 7))
    assert all(f"TC-{number:03d}" in requirements for number in range(1, 5))
    assert "OPEN CONFLICT - NOT APPROVED" in decision_log
    assert "OPEN - NOT APPROVED" in decision_log
    assert "No approval is inferred" in decision_log
    assert "not-client-approved" in (FIXTURE / "fixture-manifest.json").read_text(encoding="utf-8").lower()


def test_change_impact_names_affected_baseline_test_and_recovery() -> None:
    yaml = YAML(typ="safe")
    register = yaml.load((FIXTURE / "_registry" / "change-impact.yaml").read_text(encoding="utf-8"))
    entry = register["entries"][0]
    assert entry["affected_baseline_ids"] == ["FR-001"]
    assert "05-testing-documentation/TC-001-facility-denial.md" in entry["downstream_artifacts"]
    assert entry["decision"] == "deferred"
    assert entry["rollback_plan"].strip()
