from pathlib import Path
from engine.workspace import Workspace
from engine.artifact_graph import ArtifactGraph
from engine.findings import FindingCollection
from engine.checks.stimulus_response import StimulusResponseCheck


def _ws(tmp_path, body):
    (tmp_path / "_context").mkdir()
    (tmp_path / "02/srs.md").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "02/srs.md").write_text(body)
    return ArtifactGraph.build(Workspace.load(tmp_path))


def test_passes_when_fr_uses_shall_with_action(tmp_path):
    graph = _ws(tmp_path, "---\nphase: '02'\n---\n- **FR-001** When a provider submits a claim, the system shall persist it within 2 seconds.")
    findings = FindingCollection()
    StimulusResponseCheck("phase02.stimulus_response").run(graph, findings)
    assert len(findings) == 0


def test_flags_fr_without_shall(tmp_path):
    graph = _ws(tmp_path, "---\nphase: '02'\n---\n- **FR-002** The system can submit claims.")
    findings = FindingCollection()
    StimulusResponseCheck("phase02.stimulus_response").run(graph, findings)
    assert len(list(findings)) == 1


def test_titled_fr_with_shall_passes(tmp_path):
    """M10-08 hand-off: '**FR-nnn Title.** ... shall ...' is a stimulus-response FR."""
    graph = _ws(tmp_path, "---\nphase: '02'\n---\n**FR-108 Retry after timeout.** When the gateway times out, the system shall retry once within 5 seconds.")
    findings = FindingCollection()
    StimulusResponseCheck("phase02.stimulus_response").run(graph, findings)
    assert len(findings) == 0


def test_titled_fr_without_shall_is_flagged(tmp_path):
    graph = _ws(tmp_path, "---\nphase: '02'\n---\n**FR-109 Receipt printing.** The system can print receipts.")
    findings = FindingCollection()
    StimulusResponseCheck("phase02.stimulus_response").run(graph, findings)
    assert [f.message for f in findings] == ["FR-109 does not use the prescriptive verb 'shall'"]


def test_titled_fr_is_recognised_for_sequence_mapping(tmp_path):
    from engine.checks.diagram_trace import stimulus_response_frs
    graph = _ws(tmp_path, "---\nphase: '02'\n---\n**FR-108 Retry after timeout.** When the gateway times out, the system shall retry once.\n**FR-001** When a claim arrives, the system shall store it.")
    assert stimulus_response_frs(graph) == {"FR-001", "FR-108"}
