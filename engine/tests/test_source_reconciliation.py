from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from engine.artifact_graph import ArtifactGraph
from engine.checks.source_reconciliation import SourceReconciliationCheck
from engine.findings import FindingCollection
from engine.gates.phase02 import Phase02Gate
from engine.workspace import Workspace


def write_workspace(root: Path, register: str, requirements: str = "") -> ArtifactGraph:
    (root / "_context").mkdir(parents=True)
    (root / "_context" / "vision.md").write_text("# Vision\n", encoding="utf-8")
    if requirements:
        req = root / "02-requirements-engineering" / "requirements.md"
        req.parent.mkdir(parents=True)
        req.write_text(requirements, encoding="utf-8")
    registry = root / "_registry" / "source-reconciliation.yaml"
    registry.parent.mkdir(exist_ok=True)
    registry.write_text(register, encoding="utf-8")
    return ArtifactGraph.build(Workspace.load(root))


def register(status: str = "resolved", decision_ref: str = "DEC-001") -> str:
    decision = f"    decision_ref: {decision_ref}\n" if decision_ref else ""
    return (
        "sources:\n"
        "  - id: SRC-001\n"
        "    source_ref: elicitation_log.md#statement-1\n"
        "    statement: Payment channel alternatives need owner review.\n"
        "    requirement_ids: []\n"
        "    ambiguity_ids: [AMB-001]\n"
        "  - id: SRC-002\n"
        "    source_ref: elicitation_log.md#statement-2\n"
        "    statement: A second statement sets a conflicting payment channel.\n"
        "    requirement_ids: []\n"
        "    ambiguity_ids: [AMB-001]\n"
        "ambiguities:\n"
        "  - id: AMB-001\n"
        "    source_ids: [SRC-001, SRC-002]\n"
        "    summary: The supplied statements conflict on allowed payment channels.\n"
        f"    status: {status}\n"
        "    owner: unassigned\n"
        f"{decision}"
    )


def test_resolved_reconciliation_requires_links_and_decision_evidence(tmp_path: Path) -> None:
    graph = write_workspace(tmp_path, register())
    assert SourceReconciliationCheck().run(graph) == []


def test_unresolved_potential_conflict_blocks_phase02_without_selecting_outcome(tmp_path: Path) -> None:
    graph = write_workspace(tmp_path, register(status="unresolved", decision_ref=""))
    findings = SourceReconciliationCheck().run(graph)
    unresolved = [finding for finding in findings if finding.code == "source-reconciliation/unresolved-ambiguity"]
    assert len(unresolved) == 1
    assert "AMB-001 remains unresolved" in unresolved[0].message

    gate_findings = FindingCollection()
    Phase02Gate().evaluate(graph, gate_findings)
    assert any(f.code == "source-reconciliation/unresolved-ambiguity" for f in gate_findings)


def test_source_without_requirement_or_ambiguity_is_rejected(tmp_path: Path) -> None:
    content = register().replace("ambiguity_ids: [AMB-001]", "ambiguity_ids: []", 1)
    graph = write_workspace(tmp_path, content)
    findings = SourceReconciliationCheck().run(graph)
    assert any(f.code == "source-reconciliation/source-unmapped" for f in findings)


def test_unknown_requirement_and_unapproved_resolution_are_rejected(tmp_path: Path) -> None:
    content = register().replace("requirement_ids: []", "requirement_ids: [FR-999]", 1)
    content = content.replace("decision_ref: DEC-001", "decision_ref: ''")
    graph = write_workspace(tmp_path, content, requirements="**FR-001** The system shall accept a request.\n")
    codes = {finding.code for finding in SourceReconciliationCheck().run(graph)}
    assert "source-reconciliation/requirement-missing" in codes
    assert "source-reconciliation/resolution-evidence" in codes


def test_malformed_link_shapes_return_findings_instead_of_crashing(tmp_path: Path) -> None:
    content = register().replace("ambiguity_ids: [AMB-001]", "ambiguity_ids: 1", 1)
    content = content.replace("source_ids: [SRC-001, SRC-002]", "source_ids: [{}]")
    graph = write_workspace(tmp_path, content)
    findings = SourceReconciliationCheck().run(graph)
    assert any(f.code == "source-reconciliation/source-links-shape" for f in findings)
    assert any(f.code == "source-reconciliation/ambiguity-unknown-source" for f in findings)


def test_standalone_validator_reports_missing_register(tmp_path: Path) -> None:
    (tmp_path / "_context").mkdir()
    result = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parents[2] / "scripts" / "validate_source_reconciliation.py"), str(tmp_path)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    assert "required source reconciliation register is missing" in result.stderr
