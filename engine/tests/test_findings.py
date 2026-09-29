from pathlib import Path
import pytest
from engine.findings import Finding, Severity, FindingCollection

def test_finding_is_immutable():
    f = Finding(
        gate_id="phase01.context_complete",
        severity=Severity.HIGH,
        message="vision.md missing required section",
        location=Path("_context/vision.md"),
        line=12,
    )
    with pytest.raises(Exception):
        f.message = "changed"  # frozen dataclass

def test_collection_blocks_when_high_severity_present():
    coll = FindingCollection()
    coll.add(Finding("g1", Severity.LOW, "ok-ish", None, None))
    assert coll.is_blocking is False
    coll.add(Finding("g2", Severity.HIGH, "broken", None, None))
    assert coll.is_blocking is True

def test_collection_filters_by_gate():
    coll = FindingCollection()
    coll.add(Finding("phase01.x", Severity.HIGH, "a", None, None))
    coll.add(Finding("phase02.y", Severity.HIGH, "b", None, None))
    assert len(coll.for_gate("phase01.x")) == 1


# -- M10-07-T04: optional diagnostic fields ----------------------------------
import json as _json
from dataclasses import replace as _replace
from xml.etree import ElementTree as _ET

from engine.gates._shared import ClauseRef, attach_clause
from engine.reporters.junit import render_junit
from engine.reporters.markdown import render_markdown
from engine.reporters.sarif import render_sarif

_GOLDEN = Path(__file__).resolve().parent / "fixtures" / "findings_golden"


def _legacy_collection() -> FindingCollection:
    c = FindingCollection()
    c.add(Finding("phase01.x", Severity.HIGH, "broken", Path("a.md"), 3))
    c.add(Finding("phase01.x", Severity.LOW, "warn", Path("b.md"), 5))
    c.add(Finding("phase02.y", Severity.MEDIUM, "no location", None, None))
    return c


def _golden(name: str) -> str:
    return (_GOLDEN / name).read_bytes().decode("utf-8").replace("\r\n", "\n")


def test_findings_without_new_fields_serialise_exactly_as_before():
    c = _legacy_collection()
    waived = [Finding("phase03.z", Severity.HIGH, "waived one", None, None)]
    assert render_markdown(c, waived, project="demo") == _golden("report.md")
    assert render_sarif(c) == _golden("report.sarif.json")
    assert render_junit(c) == _golden("report.junit.xml")
    assert all(not f.has_diagnostics for f in c)


def _diagram_finding() -> Finding:
    return Finding(
        "phase03.diagram_trace", Severity.HIGH, "diagram/dead-end-state: FIG-001: stuck",
        Path("d/x.ir.json"), None, code="diagram/dead-end-state",
        subject={"figure_id": "FIG-001", "path": "/nodes/1", "identity": "review"},
        evidence={"role": "state"},
        supported_fixes=("add the transition that leaves 'review' | safely",))


def test_new_fields_are_keyword_only_with_defaults():
    f = Finding("g", Severity.LOW, "m", None, None)
    assert (f.code, f.subject, f.evidence, f.supported_fixes) == (None, None, None, ())
    with pytest.raises(TypeError):
        Finding("g", Severity.LOW, "m", None, None, "code-positional")  # type: ignore[misc]


def test_diagram_finding_serialises_all_four_fields():
    c = FindingCollection()
    c.add(_diagram_finding())
    c.add(Finding("phase01.x", Severity.LOW, "plain", None, None))
    md = render_markdown(c, [], project="demo")
    assert "| Code | Subject | Supported fixes |" in md
    assert "`diagram/dead-end-state`" in md and '"identity": "review"' in md
    assert r"leaves 'review' \| safely" in md
    assert md.splitlines()[-1].endswith("| - | - | - |")
    sarif = _json.loads(render_sarif(c))
    result = sarif["runs"][0]["results"][0]
    assert result["ruleId"] == "diagram/dead-end-state"
    assert result["properties"] == {
        "gateId": "phase03.diagram_trace",
        "subject": {"figure_id": "FIG-001", "path": "/nodes/1", "identity": "review"},
        "evidence": {"role": "state"},
        "supportedFixes": ["add the transition that leaves 'review' | safely"]}
    assert "properties" not in sarif["runs"][0]["results"][1]
    root = _ET.fromstring(render_junit(c))
    failure = root.find(".//failure")
    assert failure.get("message").endswith("[diagram/dead-end-state]")


def test_attach_clause_keeps_diagnostic_fields():
    f = attach_clause(_diagram_finding(), ClauseRef("ISO/IEC/IEEE 42010:2011", "5.6"))
    assert f.code == "diagram/dead-end-state" and f.subject["identity"] == "review"
    assert f.message.endswith("[ISO/IEC/IEEE 42010:2011 §5.6]")
    assert _replace(f, code=None).has_diagnostics  # subject/evidence still present
