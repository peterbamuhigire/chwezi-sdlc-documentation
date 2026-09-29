"""M10-08-T03 (GR-10): as-built provenance markers parse and never block."""
from collections import Counter
from pathlib import Path

from engine.artifact_graph import ArtifactGraph
from engine.checks.markers import NoUnresolvedFailMarkersGate
from engine.findings import FindingCollection
from engine.workspace import Workspace

FIXTURE = Path(__file__).parent / "fixtures" / "as_built"


def _graph() -> ArtifactGraph:
    return ArtifactGraph.build(Workspace.load(FIXTURE))


def test_all_markers_returns_as_built_and_verify_with_expected_counts() -> None:
    markers = [m for _, m in _graph().all_markers()]
    counts = Counter(m.tag for m in markers)
    assert counts == {"AS-BUILT": 3, "VERIFY": 2}
    reasons = sorted(m.reason for m in markers if m.tag == "VERIFY")
    assert reasons == [
        "confirm which rounding the business intends",
        "confirm with the finance lead whether credit notes are raised outside the system",
    ]


def test_as_built_markers_are_not_blocking() -> None:
    findings = FindingCollection()
    NoUnresolvedFailMarkersGate().evaluate(_graph(), findings)
    assert len(findings) == 0
