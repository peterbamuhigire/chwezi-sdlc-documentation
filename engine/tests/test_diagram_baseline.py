"""M10-07-T07: diagram elements in baseline snapshots, diff and delta check."""
from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path

from click.testing import CliRunner

from engine.artifact_graph import ArtifactGraph
from engine.baseline import diagram_diff, element_hashes, load_snapshot, snapshot
from engine.checks.baseline_delta import BaselineDeltaCheck
from engine.cli import main
from engine.findings import FindingCollection, Severity
from engine.workspace import Workspace

FIX = Path(__file__).resolve().parent / "fixtures" / "diagram_baseline"
SNAPS = FIX / "09-governance-compliance" / "07-baseline-delta"


def test_cli_diff_lists_exactly_the_moved_and_removed_node():
    result = CliRunner().invoke(main, ["baseline", "diff", str(FIX), "v1", "v2"])
    assert result.exit_code == 0, result.output
    changes = [ln.strip() for ln in result.output.splitlines()
               if ln.strip()[:2] in ("+ ", "- ", "~ ", "> ")]
    assert changes == ["- FIG-001#auditor", "> FIG-001#clerk"]
    assert "infers no impact or risk" in result.output


def test_legacy_snapshot_still_loads():
    legacy = load_snapshot(SNAPS / "legacy.yaml")
    assert legacy.diagram_elements == {} and legacy.entries
    d = diagram_diff(legacy, load_snapshot(SNAPS / "v1.yaml"))
    assert len(d["added"]) == 11 and not d["removed"]
    result = CliRunner().invoke(main, ["baseline", "diff", str(FIX), "legacy", "legacy"])
    assert "Diagram elements" not in result.output


def _project(tmp_path: Path, ir_name: str) -> Path:
    p = tmp_path / ir_name
    (p / "_context").mkdir(parents=True)
    (p / "_context" / "vision.md").write_text("# V\n", encoding="utf-8")
    d = p / "03-design-documentation" / "01-high-level-design" / "diagrams"
    d.mkdir(parents=True)
    shutil.copy(FIX / "ir" / f"{ir_name}.ir.json", d / "context.ir.json")
    return p


def test_fixture_snapshots_are_reproducible(tmp_path):
    for label in ("v1", "v2"):
        snap = snapshot(ArtifactGraph.build(Workspace.load(_project(tmp_path, label))), label,
                        today=date(2026, 9, 29))
        assert snap.diagram_elements == load_snapshot(SNAPS / f"{label}.yaml").diagram_elements


def test_changed_versus_moved_hashing():
    base = {"id": "n", "label": "A", "role": "system", "boundary": "x"}
    moved = dict(base, boundary="y")
    changed = dict(base, label="B")
    assert element_hashes(base)[0] == element_hashes(moved)[0]
    assert element_hashes(base)[1] != element_hashes(moved)[1]
    assert element_hashes(base)[0] != element_hashes(changed)[0]
    assert element_hashes({"id": "m", "order": 1})[0] == element_hashes({"id": "m", "order": 2})[0]


def test_invalid_ir_is_not_baselined(tmp_path):
    p = _project(tmp_path, "v1")
    (p / "03-design-documentation/01-high-level-design/diagrams/context.ir.json").write_text(
        "{}", encoding="utf-8")
    assert snapshot(ArtifactGraph.build(Workspace.load(p)), "x").diagram_elements == {}


def test_baseline_delta_check_reports_diagram_delta_as_info(tmp_path):
    p = tmp_path / "p"
    shutil.copytree(FIX, p)
    (p / "_registry").mkdir()
    (p / "_registry" / "baselines.yaml").write_text("current: v2\nprevious: v1\n", encoding="utf-8")
    findings = FindingCollection()
    BaselineDeltaCheck("phase09.baseline_delta", p).run(
        ArtifactGraph.build(Workspace.load(p)), findings)
    items = list(findings)
    assert len(items) == 1
    f = items[0]
    assert (f.gate_id, f.severity, f.code) == (
        "phase09.baseline_delta.diagram_delta", Severity.INFO, "diagram/baseline-delta")
    assert f.evidence["removed"] == ["FIG-001#auditor"] and f.evidence["moved"] == ["FIG-001#clerk"]
    (p / "_registry" / "baselines.yaml").write_text("current: v2\nprevious: v9\n", encoding="utf-8")
    findings = FindingCollection()
    BaselineDeltaCheck("phase09.baseline_delta", p).run(
        ArtifactGraph.build(Workspace.load(p)), findings)
    assert list(findings) == []
    (p / "_registry" / "baselines.yaml").write_text("current: v1\nprevious: v1\n", encoding="utf-8")
    findings = FindingCollection()
    BaselineDeltaCheck("phase09.baseline_delta", p).run(
        ArtifactGraph.build(Workspace.load(p)), findings)
    assert list(findings) == []
