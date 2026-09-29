"""M10-08-T08: agent build brief derived from an approved SRS."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from engine.agent_brief import BRIEF_NAME, Entry, collect, render, untraced, write_brief
from engine.artifact_graph import ArtifactGraph
from engine.checks.markers import NoUnresolvedFailMarkersGate
from engine.findings import FindingCollection
from engine.parsers.markers import find_markers
from engine.workspace import Workspace

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / "fixtures" / "healthcare_admissions"
GOLDEN = Path(__file__).parent / "fixtures" / "agent_brief" / "healthcare_admissions.golden.md"
_ENTRY_LINE = re.compile(r"^- .+ \((?P<source>[^()]+)\)$")


def _complete_project(tmp_path: Path, with_test_commands: bool = True) -> Path:
    """Healthcare fixture plus commands, conventions and (optionally) test commands."""
    project = tmp_path / "healthcare_admissions"
    shutil.copytree(FIXTURE, project)
    env = [
        "---", 'phase: "02"', "---", "# Operating environment", "",
        "## Build and run commands", "",
        "- `composer install` installs the locked dependencies",
        "- `php artisan serve` runs the admissions service locally", "",
    ]
    if with_test_commands:
        env += ["## Test commands", "", "- `vendor/bin/phpunit` runs TC-001 to TC-004", ""]
    (project / "02-requirements-engineering" / "environment.md").write_text(
        "\n".join(env), encoding="utf-8")
    conv = project / "04-development-artifacts" / "coding-guidelines.md"
    conv.parent.mkdir(parents=True)
    conv.write_text("# Coding guidelines\n\n## Coding conventions\n\n"
                    "- PSR-12 formatting for all PHP source\n"
                    "- One controller per bounded context\n\n"
                    "## Prohibited practices\n\n- Raw SQL built by string concatenation\n",
                    encoding="utf-8")
    return project


def test_fixture_brief_is_fully_traced_and_matches_golden():
    entries = collect(FIXTURE)
    assert untraced(entries) == []
    text = render(FIXTURE, entries)
    assert text == GOLDEN.read_text(encoding="utf-8")
    body_lines = [l for l in text.splitlines() if l.startswith("- ")]
    assert len(body_lines) == len(entries)
    assert all(_ENTRY_LINE.match(l) for l in body_lines), "every entry ends with its source"
    assert "{{" not in text


def test_fixture_areas_are_derived_from_the_srs():
    entries = collect(FIXTURE)
    areas = {e.area for e in entries}
    assert areas == {"objective", "commands", "structure", "conventions", "testing",
                     "always", "ask_first", "never"}
    assert [e.source.split(",")[0] for e in entries if e.area == "objective"] == \
        ["BG-001", "BG-002", "BG-003"]
    always = [e.text.split(":")[0] for e in entries if e.area == "always"]
    assert always == [f"FR-00{i}" for i in range(1, 7)]
    ask = " ".join(e.text for e in entries if e.area == "ask_first")
    assert "D-005" in ask and "D-006" in ask and "CIA-001" in ask
    assert "D-001" not in ask


def test_complete_project_has_no_gaps(tmp_path):
    project = _complete_project(tmp_path)
    entries = collect(project)
    assert [e for e in entries if e.is_gap] == []
    assert untraced(entries) == []
    cmds = [e for e in entries if e.area == "commands"]
    assert len(cmds) == 2 and cmds[0].source.endswith("§ Build and run commands")
    assert any("PSR-12" in e.text for e in entries if e.area == "conventions")
    assert any("Raw SQL" in e.text for e in entries if e.area == "never")


def test_missing_test_commands_yields_one_gap_that_the_kernel_blocks(tmp_path):
    project = _complete_project(tmp_path, with_test_commands=False)
    out = write_brief(project)
    assert out == project / BRIEF_NAME
    markers = [m for m in find_markers(out.read_text(encoding="utf-8")) if m.tag == "CONTEXT-GAP"]
    assert len(markers) == 1
    assert "test commands" in markers[0].reason
    graph = ArtifactGraph.build(Workspace.load(project))
    findings = FindingCollection()
    NoUnresolvedFailMarkersGate().evaluate(graph, findings)
    brief_findings = [f for f in findings if f.location == Path(BRIEF_NAME)]
    assert len(brief_findings) == 1
    assert findings.is_blocking
    # Regeneration ignores the previous brief rather than feeding on it.
    assert collect(project) == collect(project)
    assert write_brief(project).read_text(encoding="utf-8") == out.read_text(encoding="utf-8")


def test_empty_project_reports_every_missing_area_as_a_gap(tmp_path):
    (tmp_path / "_context").mkdir()
    entries = collect(tmp_path)
    gaps = {e.area for e in entries if e.is_gap}
    assert gaps == {"objective", "commands", "structure", "conventions", "testing", "always"}
    assert untraced(entries) == []


def test_untraced_detects_a_missing_source():
    assert untraced([Entry("objective", "x", " ")]) == [Entry("objective", "x", " ")]


def test_write_brief_rejects_bad_targets(tmp_path):
    with pytest.raises(ValueError):
        write_brief(tmp_path / "absent")
    with pytest.raises(ValueError):
        write_brief(FIXTURE, tmp_path / "brief.txt")


def test_script_writes_beside_the_handoff(tmp_path):
    feature = tmp_path / "feature"
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "create_agent_build_brief.py"),
         "--project", str(FIXTURE), "--feature-dir", str(feature)],
        capture_output=True, text=True, cwd=ROOT, check=True)
    assert "untraced=0" in result.stdout
    assert (feature / BRIEF_NAME).read_text(encoding="utf-8") == GOLDEN.read_text(encoding="utf-8")
