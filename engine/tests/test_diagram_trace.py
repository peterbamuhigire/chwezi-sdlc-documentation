"""M10-07-T03: DiagramTraceCheck codes, phase03 registration, validate CLI."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from engine.artifact_graph import ArtifactGraph
from engine.checks.diagram_trace import DiagramTraceCheck
from engine.cli import main
from engine.diagram_ir import NO_DELETION_GUARD, read_validated
from engine.findings import FindingCollection, Severity
from engine.gates.phase03 import Phase03Gate
from engine.workspace import Workspace

FIX = Path(__file__).resolve().parent / "fixtures" / "diagram_trace"
DIAGRAMS = Path("03-design-documentation") / "01-high-level-design" / "diagrams"
CASES = sorted(p.name for p in (FIX / "cases").iterdir())


def _project(tmp_path: Path, case: str) -> Path:
    dst = tmp_path / case
    shutil.copytree(FIX / "base", dst)
    target = dst / DIAGRAMS
    target.mkdir(parents=True)
    for ir in (FIX / "cases" / case).glob("*.ir.json"):
        shutil.copy(ir, target / ir.name)
    return dst


def _run(project: Path) -> FindingCollection:
    graph = ArtifactGraph.build(Workspace.load(project))
    findings = FindingCollection()
    DiagramTraceCheck("phase03.diagram_trace", project).run(graph, findings)
    return findings


def test_all_codes_have_a_case():
    assert set(CASES) == {
        "valid", "unknown-trace-id", "uncovered-requirement", "unexpected-root",
        "unexpected-terminal", "required-edge", "required-path", "dead-end-state",
        "unmapped-sequence", "unknown-edge-endpoint"}


@pytest.mark.parametrize("case", [c for c in CASES if c != "valid"])
def test_negative_fixture_fails_with_exactly_its_code(tmp_path, case):
    findings = list(_run(_project(tmp_path, case)))
    assert {f.code for f in findings} == {f"diagram/{case}"}
    for f in findings:
        assert f.gate_id == "phase03.diagram_trace"
        assert f.subject and "figure_id" in f.subject
        assert f.supported_fixes
        assert all(NO_DELETION_GUARD in fix for fix in f.supported_fixes)
    expected = Severity.MEDIUM if case in ("uncovered-requirement", "unmapped-sequence") else Severity.HIGH
    assert {f.severity for f in findings} == {expected}


def test_valid_fixture_passes(tmp_path):
    assert list(_run(_project(tmp_path, "valid"))) == []


def test_check_is_silent_without_ir(tmp_path):
    project = tmp_path / "p"
    shutil.copytree(FIX / "base", project)
    assert list(_run(project)) == []
    assert DiagramTraceCheck("g", None).diagnostics(ArtifactGraph(artifacts=())) == []


def test_registry_absent_falls_back_with_info(tmp_path):
    project = _project(tmp_path, "valid")
    (project / "_registry" / "identifiers.yaml").unlink()
    findings = list(_run(project))
    assert [(f.code, f.severity) for f in findings] == [("diagram/registry-absent", Severity.INFO)]


def test_unknown_prefix_is_reported(tmp_path):
    project = _project(tmp_path, "valid")
    ir = project / DIAGRAMS / "lifecycle.ir.json"
    data = json.loads(ir.read_text(encoding="utf-8"))
    data["nodes"][0]["trace"].append("ZZ-001")
    ir.write_text(json.dumps(data), encoding="utf-8")
    findings = list(_run(project))
    assert [f.evidence["reason"] for f in findings] == ["prefix not in engine.idscan.KIND_PREFIXES"]


def test_schema_failures_surface_through_the_check(tmp_path):
    project = _project(tmp_path, "valid")
    (project / DIAGRAMS / "lifecycle.ir.json").write_text('{"schema_version": 2}', encoding="utf-8")
    codes = {f.code for f in _run(project)}
    assert "schema/const" in codes and "diagram/uncovered-requirement" in codes


def test_phase03_gate_runs_the_check_with_clause(tmp_path):
    project = _project(tmp_path, "dead-end-state")
    graph = ArtifactGraph.build(Workspace.load(project))
    findings = FindingCollection()
    Phase03Gate().evaluate(graph, findings)
    hits = findings.for_gate("phase03.diagram_trace")
    assert hits and hits[0].code == "diagram/dead-end-state"
    assert "42010" in hits[0].message


def test_validate_cli_freezes_only_clean_documents(tmp_path):
    runner = CliRunner()
    good = _project(tmp_path, "valid")
    result = runner.invoke(main, ["diagrams", "validate", str(good), "--json",
                                  str(tmp_path / "d.json")])
    assert result.exit_code == 0, result.output
    assert "DIAGRAMS: PASS" in result.output
    assert read_validated(good / DIAGRAMS.parent)["FIG-001"]["ir_sha256"]
    bad = _project(tmp_path, "required-edge")
    result = runner.invoke(main, ["diagrams", "validate", str(bad), "--doc",
                                  str(bad / DIAGRAMS.parent)])
    assert result.exit_code == 1
    assert "diagram/required-edge" in result.output and "NOT VALIDATED" in result.output
    assert read_validated(bad / DIAGRAMS.parent) == {}
    result = runner.invoke(main, ["diagrams", "validate", str(bad), "--doc", str(tmp_path)])
    assert result.exit_code == 2
