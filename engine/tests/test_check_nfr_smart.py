from pathlib import Path
import pytest
from engine.workspace import Workspace
from engine.artifact_graph import ArtifactGraph
from engine.findings import FindingCollection
from engine.checks.nfr_smart import SmartNfrCheck

def _ws(tmp_path: Path, body: str) -> ArtifactGraph:
    (tmp_path / "_context").mkdir()
    (tmp_path / "_context/nfrs.md").write_text(body, encoding="utf-8")
    return ArtifactGraph.build(Workspace.load(tmp_path))

def test_passes_when_nfr_has_metric_and_threshold(tmp_path: Path):
    body = "# NFRs\n- **NFR-001** Response time shall be ≤ 500 ms at P95 under normal load."
    findings = FindingCollection()
    SmartNfrCheck("phase02.smart_nfr").run(_ws(tmp_path, body), findings)
    assert len(findings) == 0

def test_flags_vague_nfr(tmp_path: Path):
    body = "# NFRs\n- **NFR-002** The system shall be fast and reliable."
    findings = FindingCollection()
    SmartNfrCheck("phase02.smart_nfr").run(_ws(tmp_path, body), findings)
    items = list(findings)
    assert len(items) == 1
    assert "fast" in items[0].message


def _run(tmp_path: Path, body: str) -> list:
    findings = FindingCollection()
    SmartNfrCheck("phase02.smart_nfr").run(_ws(tmp_path, body), findings)
    return list(findings)


@pytest.mark.parametrize("statement,word", [
    ("The system shall respond quickly to bursar searches.", "quickly"),
    ("The system shall be available at all times.", "at all times"),
    ("The reporting screen shall be responsive.", "responsive"),
    ("The importer shall process files efficiently.", "efficiently"),
    ("The service shall be highly available.", "highly available"),
])
def test_flags_unmeasured_qualifier_without_any_metric(tmp_path: Path, statement: str, word: str) -> None:
    items = _run(tmp_path, f"# NFRs\n- **NFR-003** {statement}")
    assert len(items) == 1
    assert word in items[0].message


@pytest.mark.parametrize("statement", [
    "The system shall be reliable and shall restore service within ≤ 4 hours after an outage.",
    "The system shall be reliable and restore service within 4 hours of an outage.",
    "The search shall be responsive: results shall appear in <= 2 seconds at P95.",
    "The service shall be highly available, with >= 99.9% monthly uptime.",
    "The export shall be quick, finishing in at most 10 minutes for 1 GB of data.",
    "The page shall stay responsive at >= 320 px viewport width.",
])
def test_accepts_a_stated_threshold_in_common_units(tmp_path: Path, statement: str) -> None:
    assert _run(tmp_path, f"# NFRs\n- **NFR-004** {statement}") == []


def test_does_not_demand_a_number_from_a_conformance_statement(tmp_path: Path) -> None:
    body = "# NFRs\n- **NFR-005** The system shall conform to WCAG 2.2 Level AA on every public page."
    assert _run(tmp_path, body) == []
