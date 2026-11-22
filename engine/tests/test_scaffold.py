from pathlib import Path
from click.testing import CliRunner
from engine.cli import main


def test_new_project_creates_canonical_workspace(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    rc = CliRunner().invoke(main, [
        "new-project", "TestProject",
        "--methodology", "hybrid",
        "--domain", "uganda",
        "--example", "uganda-public-sector",
    ])
    assert rc.exit_code == 0, rc.output
    project = tmp_path / "projects" / "TestProject"
    assert (project / "_context" / "vision.md").exists()
    methodology_body = (project / "_context" / "methodology.md").read_text(encoding="utf-8").lower()
    assert "methodology: hybrid" in methodology_body
    assert (project / "_registry" / "controls.yaml").exists()
    assert (project / "_registry" / "baseline-trace.yaml").exists()
    assert (project / "export").is_dir()
    assert (project / "export" / ".gitkeep").exists()
    assert (project / "export-docs.ps1").exists()
    assert (project / "export-docs.sh").exists()


def test_new_project_without_example_seeds_minimum_context(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    rc = CliRunner().invoke(main, [
        "new-project", "Minimal",
        "--methodology", "agile",
        "--domain", "retail",
    ])
    assert rc.exit_code == 0, rc.output
    project = tmp_path / "projects" / "Minimal"
    assert (project / "_context" / "vision.md").exists()
    assert (project / "_context" / "methodology.md").exists()
    assert (project / "export").is_dir()
    assert (project / "export-docs.ps1").exists()
    assert (project / "export-docs.sh").exists()
    # No example => no baseline-trace.yaml for agile
    assert not (project / "_registry" / "baseline-trace.yaml").exists()
    from engine.artifact_graph import ArtifactGraph
    from engine.findings import FindingCollection
    from engine.gates.phase01 import Phase01Gate
    from engine.workspace import Workspace

    strategy = project / "01-strategic-vision" / "digital-marketing-social-media-and-website-strategy.md"
    brief = strategy.read_text(encoding="utf-8")
    def strategy_findings():
        findings = FindingCollection()
        Phase01Gate().evaluate(ArtifactGraph.build(Workspace.load(project)), findings)
        return [f for f in findings if f.gate_id == "phase01.product_market_strategy"]

    assert strategy_findings()
    strategy.unlink()
    assert strategy_findings()
    (project / "01-strategic-vision" / "existing-strategy.md").write_text(
        brief.replace("strategy_status: draft", "strategy_status: reviewed"), encoding="utf-8")
    assert not strategy_findings()
