from pathlib import Path
from engine.workspace import Workspace
from engine.artifact_graph import ArtifactGraph
from engine.findings import FindingCollection
from engine.gates.phase06 import Phase06Gate


def _ws(tmp_path, files):
    for rel, body in files.items():
        full = tmp_path / rel
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(body, encoding="utf-8")
    return ArtifactGraph.build(Workspace.load(tmp_path))


# -- deployment_guide_has_rollback -----------------------------------------

def test_passes_when_deployment_guide_has_rollback(tmp_path):
    graph = _ws(tmp_path, {
        "_context/vision.md": "# Vision",
        "06-deployment-operations/deployment-guide.md": (
            "# Deployment Guide\n"
            "## Rollback procedure\n"
            "If deployment fails, rollback to the previous release tag."
        ),
    })
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    assert findings.for_gate("phase06.deployment_guide_has_rollback") == []


def test_flags_missing_deployment_guide(tmp_path):
    graph = _ws(tmp_path, {
        "_context/vision.md": "# Vision",
        "06-deployment-operations/runbook.md": "# Runbook",
    })
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    msgs = [f.message for f in findings
            if f.gate_id == "phase06.deployment_guide_has_rollback"]
    assert msgs, "expected a deployment_guide_has_rollback finding"
    assert "No deployment guide found" in msgs[0]


def test_flags_deployment_guide_without_rollback(tmp_path):
    graph = _ws(tmp_path, {
        "_context/vision.md": "# Vision",
        "06-deployment-operations/deployment-guide.md": (
            "# Deployment Guide\nDeploy via the CI pipeline only."
        ),
    })
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    msgs = [f.message for f in findings
            if f.gate_id == "phase06.deployment_guide_has_rollback"]
    assert msgs, "expected a deployment_guide_has_rollback finding"
    assert "no rollback procedure" in msgs[0]


# -- runbook_has_escalation ------------------------------------------------

def test_passes_when_runbook_has_escalation(tmp_path):
    graph = _ws(tmp_path, {
        "_context/vision.md": "# Vision",
        "06-deployment-operations/deployment-guide.md": (
            "# Deployment Guide\nRollback via tag."
        ),
        "06-deployment-operations/runbook.md": (
            "# Runbook\n"
            "## Escalation\n"
            "Page the on-call SRE, then escalate to the platform lead."
        ),
    })
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    assert findings.for_gate("phase06.runbook_has_escalation") == []


def test_flags_runbook_without_escalation(tmp_path):
    graph = _ws(tmp_path, {
        "_context/vision.md": "# Vision",
        "06-deployment-operations/deployment-guide.md": (
            "# Deployment Guide\nRollback via tag."
        ),
        "06-deployment-operations/runbook.md": (
            "# Runbook\nGeneral operations only; no handoff defined."
        ),
    })
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    msgs = [f.message for f in findings
            if f.gate_id == "phase06.runbook_has_escalation"]
    assert msgs, "expected a runbook_has_escalation finding"
    assert "no escalation path" in msgs[0]


# -- monitoring_has_slo ----------------------------------------------------

def test_passes_when_monitoring_doc_has_slo(tmp_path):
    graph = _ws(tmp_path, {
        "_context/vision.md": "# Vision",
        "06-deployment-operations/deployment-guide.md": (
            "# Deployment Guide\nRollback via tag."
        ),
        "06-deployment-operations/runbook.md": (
            "# Runbook\nEscalation: on-call SRE."
        ),
        "06-deployment-operations/monitoring.md": (
            "# Monitoring\nWe track an SLO of 99.9% availability."
        ),
    })
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    assert findings.for_gate("phase06.monitoring_has_slo") == []


def test_flags_monitoring_doc_without_slo(tmp_path):
    graph = _ws(tmp_path, {
        "_context/vision.md": "# Vision",
        "06-deployment-operations/deployment-guide.md": (
            "# Deployment Guide\nRollback via tag."
        ),
        "06-deployment-operations/runbook.md": (
            "# Runbook\nEscalation: on-call SRE."
        ),
        "06-deployment-operations/observability.md": (
            "# Observability\nMetrics dashboards are in Grafana."
        ),
    })
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    msgs = [f.message for f in findings
            if f.gate_id == "phase06.monitoring_has_slo"]
    assert msgs, "expected a monitoring_has_slo finding"
    assert "no SLO/SLI/SLA reference" in msgs[0]


# -- infra_has_ir_diagram --------------------------------------------------

def test_passes_when_infra_doc_has_ir_diagram(tmp_path):
    graph = _ws(tmp_path, {
        "_context/vision.md": "# Vision",
        "06-deployment-operations/deployment-guide.md": (
            "# Deployment Guide\nRollback via tag."
        ),
        "06-deployment-operations/runbook.md": (
            "# Runbook\nEscalation: on-call SRE."
        ),
        "06-deployment-operations/monitoring.md": (
            "# Monitoring\nSLO 99.9%."
        ),
        "06-deployment-operations/infrastructure.md": (
            "# Infrastructure\n\n"
            "Incident response diagram below describes the on-call flow.\n\n"
            "![IR diagram](diagrams/incident-response.png)\n"
        ),
    })
    png = tmp_path / "06-deployment-operations" / "diagrams" / "incident-response.png"
    png.parent.mkdir(parents=True, exist_ok=True)
    png.write_bytes(b"\x89PNG\r\n\x1a\n")
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    assert findings.for_gate("phase06.infra_has_ir_diagram") == []


def test_flags_infra_doc_without_ir_diagram(tmp_path):
    graph = _ws(tmp_path, {
        "_context/vision.md": "# Vision",
        "06-deployment-operations/deployment-guide.md": (
            "# Deployment Guide\nRollback via tag."
        ),
        "06-deployment-operations/runbook.md": (
            "# Runbook\nEscalation: on-call SRE."
        ),
        "06-deployment-operations/monitoring.md": (
            "# Monitoring\nSLO 99.9%."
        ),
        "06-deployment-operations/infrastructure.md": (
            "# Infrastructure\nAWS regions and VPC layout."
        ),
    })
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    msgs = [f.message for f in findings
            if f.gate_id == "phase06.infra_has_ir_diagram"]
    assert msgs, "expected an infra_has_ir_diagram finding"
    assert "no incident-response figure" in msgs[0]


# -- go_live_readiness_checklist_complete ---------------------------------

def test_passes_when_go_live_checklist_all_checked(tmp_path):
    graph = _ws(tmp_path, {
        "_context/vision.md": "# Vision",
        "06-deployment-operations/deployment-guide.md": (
            "# Deployment Guide\nRollback via tag."
        ),
        "06-deployment-operations/runbook.md": (
            "# Runbook\nEscalation: on-call SRE."
        ),
        "06-deployment-operations/monitoring.md": (
            "# Monitoring\nSLO 99.9%."
        ),
        "06-deployment-operations/infrastructure.md": (
            "# Infrastructure\nIR diagram: ![IR](incident-response.png)."
        ),
        "06-deployment-operations/go-live-readiness.md": (
            "# Go-Live Readiness\n\n"
            "- [x] Deployment rehearsed\n"
            "- [x] On-call rota confirmed\n"
            "- [x] Monitoring verified\n"
        ),
    })
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    assert findings.for_gate(
        "phase06.go_live_readiness_checklist_complete"
    ) == []


def test_flags_go_live_checklist_with_unchecked_items(tmp_path):
    graph = _ws(tmp_path, {
        "_context/vision.md": "# Vision",
        "06-deployment-operations/deployment-guide.md": (
            "# Deployment Guide\nRollback via tag."
        ),
        "06-deployment-operations/runbook.md": (
            "# Runbook\nEscalation: on-call SRE."
        ),
        "06-deployment-operations/monitoring.md": (
            "# Monitoring\nSLO 99.9%."
        ),
        "06-deployment-operations/infrastructure.md": (
            "# Infrastructure\nIR diagram: ![IR](incident-response.png)."
        ),
        "06-deployment-operations/go-live-readiness.md": (
            "# Go-Live Readiness\n\n"
            "- [x] Deployment rehearsed\n"
            "- [ ] On-call rota confirmed\n"
            "- [ ] Monitoring verified\n"
        ),
    })
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    msgs = [f.message for f in findings
            if f.gate_id == "phase06.go_live_readiness_checklist_complete"]
    assert msgs, (
        "expected a go_live_readiness_checklist_complete finding"
    )
    assert "2 unchecked item(s)" in msgs[0]


# -- change_window_documented ---------------------------------------------

def test_passes_when_change_window_in_dedicated_file(tmp_path):
    graph = _ws(tmp_path, {
        "_context/vision.md": "# Vision",
        "06-deployment-operations/deployment-guide.md": (
            "# Deployment Guide\nRollback via tag."
        ),
        "06-deployment-operations/change-window.md": (
            "# Change Window\nDeployments occur in the 02:00-04:00 UTC window."
        ),
    })
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    assert findings.for_gate("phase06.change_window_documented") == []


def test_passes_when_change_window_in_deployment_guide(tmp_path):
    graph = _ws(tmp_path, {
        "_context/vision.md": "# Vision",
        "06-deployment-operations/deployment-guide.md": (
            "# Deployment Guide\n"
            "Rollback via tag. All releases ship during the agreed "
            "change window on Tuesday nights."
        ),
    })
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    assert findings.for_gate("phase06.change_window_documented") == []


def test_flags_missing_change_window_everywhere(tmp_path):
    graph = _ws(tmp_path, {
        "_context/vision.md": "# Vision",
        "06-deployment-operations/deployment-guide.md": (
            "# Deployment Guide\nRollback via tag; deploy any time."
        ),
    })
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    msgs = [f.message for f in findings
            if f.gate_id == "phase06.change_window_documented"]
    assert msgs, "expected a change_window_documented finding"
    assert "No change window documentation found" in msgs[0]


# -- clause attachment ------------------------------------------------------

def test_findings_carry_ieee_1062_clause_label(tmp_path):
    graph = _ws(tmp_path, {
        "_context/vision.md": "# Vision",
    })
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    assert len(findings) > 0
    for f in findings:
        assert "IEEE Std 1062-2015" in f.message
        assert "6.3" in f.message
