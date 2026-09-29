"""Phase 06 - Deployment & Operations gate (IEEE Std 1062-2015)."""
from __future__ import annotations
import re
from engine.artifact_graph import Artifact, ArtifactGraph
from engine.findings import Finding, FindingCollection, Severity
from engine.gates.base import Gate
from engine.gates._shared import ClauseRef, attach_clause
from engine.figures import figures_in, load_manifest_index

_CLAUSE = ClauseRef("IEEE Std 1062-2015", "6.3")

_PHASE06_DIR_TOKEN = "06-deployment-operations/"

_DEPLOYMENT_GUIDE_NAMES = ("deployment-guide.md", "deployment.md")
_RUNBOOK_NAMES = ("runbook.md", "operations-runbook.md")

_ROLLBACK_RE = re.compile(r"\b(rollback|roll\s+back)\b", re.IGNORECASE)
_ESCALATION_RE = re.compile(r"\b(escalat(e|ion))\b", re.IGNORECASE)
_SLO_RE = re.compile(r"\b(SLO|SLI|SLA)\b", re.IGNORECASE)
# The document must discuss incident response ...
_IR_MENTION_RE = re.compile(r"(incident[- ]?response|\bIR\b)", re.IGNORECASE)
# ... and carry a figure (an existing image, or a rendering recorded by
# scripts/render_diagrams.py; see engine/figures.py) whose label, target or
# diagram text is about it. The words "mermaid" or "plantuml" are no longer
# accepted as proof that a figure exists (M10-01-T12, AR-03).
_IR_FIGURE_LABEL_RE = re.compile(
    r"(incident|\bIR\b|(?<![a-z])ir[-_.]|escalat)", re.IGNORECASE
)
_UNCHECKED_ITEM_RE = re.compile(r"^\s*-\s+\[\s\]", re.MULTILINE)
_CHANGE_WINDOW_NAME_TOKENS = (
    "change-window",
    "maintenance-window",
    "change_window",
)
_CHANGE_WINDOW_PHRASES = ("change window", "maintenance window")


def _posix(path) -> str:
    return str(path).replace("\\", "/")


def _under_phase06(art: Artifact) -> bool:
    return _PHASE06_DIR_TOKEN in _posix(art.path)


def _find_deployment_guide(graph: ArtifactGraph):
    for art in graph.artifacts:
        if not _under_phase06(art):
            continue
        if art.path.name.lower() in _DEPLOYMENT_GUIDE_NAMES:
            return art
    return None


def _find_runbook(graph: ArtifactGraph):
    for art in graph.artifacts:
        if not _under_phase06(art):
            continue
        if art.path.name.lower() in _RUNBOOK_NAMES:
            return art
    return None


def _find_monitoring_doc(graph: ArtifactGraph):
    for art in graph.artifacts:
        if not _under_phase06(art):
            continue
        name = art.path.name.lower()
        if "monitor" in name or "observability" in name or "slo" in name:
            return art
    return None


def _find_infra_doc(graph: ArtifactGraph):
    for art in graph.artifacts:
        if not _under_phase06(art):
            continue
        name = art.path.name.lower()
        if "infra" in name or "infrastructure" in name:
            return art
    return None


def _find_go_live_doc(graph: ArtifactGraph):
    for art in graph.artifacts:
        if not _under_phase06(art):
            continue
        name = art.path.name.lower()
        if "go-live" in name or "go_live" in name or "readiness" in name:
            return art
    return None


def _find_change_window_doc(graph: ArtifactGraph):
    for art in graph.artifacts:
        if not _under_phase06(art):
            continue
        name = art.path.name.lower()
        if any(tok in name for tok in _CHANGE_WINDOW_NAME_TOKENS):
            return art
    return None


class Phase06Gate(Gate):
    id = "phase06"
    title = "Deployment & Operations phase gate"
    severity = Severity.HIGH

    def evaluate(self, graph: ArtifactGraph, findings: FindingCollection) -> None:
        self._check_deployment_guide_has_rollback(graph, findings)
        self._check_runbook_has_escalation(graph, findings)
        self._check_monitoring_has_slo(graph, findings)
        self._check_infra_has_ir_diagram(graph, findings)
        self._check_go_live_readiness_checklist_complete(graph, findings)
        self._check_change_window_documented(graph, findings)

    # -- Check 1: deployment guide has rollback --------------------------
    def _check_deployment_guide_has_rollback(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        guide = _find_deployment_guide(graph)
        if guide is None:
            findings.add(attach_clause(Finding(
                gate_id=f"{self.id}.deployment_guide_has_rollback",
                severity=Severity.HIGH,
                message=(
                    "No deployment guide found under "
                    "06-deployment-operations/ (expected "
                    "'deployment-guide.md' or 'deployment.md')"
                ),
                location=None,
                line=None,
            ), _CLAUSE))
            return
        if _ROLLBACK_RE.search(guide.body):
            return
        findings.add(attach_clause(Finding(
            gate_id=f"{self.id}.deployment_guide_has_rollback",
            severity=Severity.HIGH,
            message=(
                f"Deployment guide '{_posix(guide.path)}' has no "
                f"rollback procedure"
            ),
            location=guide.path,
            line=None,
        ), _CLAUSE))

    # -- Check 2: runbook has escalation ---------------------------------
    def _check_runbook_has_escalation(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        runbook = _find_runbook(graph)
        if runbook is None:
            findings.add(attach_clause(Finding(
                gate_id=f"{self.id}.runbook_has_escalation",
                severity=Severity.HIGH,
                message=(
                    "No runbook found under 06-deployment-operations/ "
                    "(expected 'runbook.md' or 'operations-runbook.md')"
                ),
                location=None,
                line=None,
            ), _CLAUSE))
            return
        if _ESCALATION_RE.search(runbook.body):
            return
        findings.add(attach_clause(Finding(
            gate_id=f"{self.id}.runbook_has_escalation",
            severity=Severity.HIGH,
            message=(
                f"Runbook '{_posix(runbook.path)}' has no escalation path"
            ),
            location=runbook.path,
            line=None,
        ), _CLAUSE))

    # -- Check 3: monitoring has SLO -------------------------------------
    def _check_monitoring_has_slo(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        doc = _find_monitoring_doc(graph)
        if doc is None:
            findings.add(attach_clause(Finding(
                gate_id=f"{self.id}.monitoring_has_slo",
                severity=Severity.HIGH,
                message=(
                    "No monitoring document found under "
                    "06-deployment-operations/ (expected filename "
                    "containing 'monitor', 'observability', or 'slo')"
                ),
                location=None,
                line=None,
            ), _CLAUSE))
            return
        if _SLO_RE.search(doc.body):
            return
        findings.add(attach_clause(Finding(
            gate_id=f"{self.id}.monitoring_has_slo",
            severity=Severity.HIGH,
            message=(
                f"Monitoring document '{_posix(doc.path)}' has no "
                f"SLO/SLI/SLA reference"
            ),
            location=doc.path,
            line=None,
        ), _CLAUSE))

    # -- Check 4: infrastructure has IR diagram --------------------------
    def _check_infra_has_ir_diagram(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        doc = _find_infra_doc(graph)
        if doc is None:
            findings.add(attach_clause(Finding(
                gate_id=f"{self.id}.infra_has_ir_diagram",
                severity=Severity.HIGH,
                message=(
                    "No infrastructure document found under "
                    "06-deployment-operations/ (expected filename "
                    "containing 'infra' or 'infrastructure')"
                ),
                location=None,
                line=None,
            ), _CLAUSE))
            return
        if _IR_MENTION_RE.search(doc.body):
            root = graph.root
            index = load_manifest_index(root) if root is not None else {}
            for fig in figures_in(doc, root, index):
                if _IR_FIGURE_LABEL_RE.search(fig.label):
                    return
        findings.add(attach_clause(Finding(
            gate_id=f"{self.id}.infra_has_ir_diagram",
            severity=Severity.HIGH,
            message=(
                f"Infrastructure doc '{_posix(doc.path)}' has no "
                f"incident-response figure: expected an image whose file "
                f"exists, or a Mermaid block rendered by "
                f"scripts/render_diagrams.py (a code block alone is not "
                f"a figure)"
            ),
            location=doc.path,
            line=None,
        ), _CLAUSE))

    # -- Check 5: go-live readiness checklist complete -------------------
    def _check_go_live_readiness_checklist_complete(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        doc = _find_go_live_doc(graph)
        if doc is None:
            findings.add(attach_clause(Finding(
                gate_id=f"{self.id}.go_live_readiness_checklist_complete",
                severity=Severity.HIGH,
                message=(
                    "No go-live readiness checklist found under "
                    "06-deployment-operations/ (expected filename "
                    "containing 'go-live' or 'readiness')"
                ),
                location=None,
                line=None,
            ), _CLAUSE))
            return
        unchecked = _UNCHECKED_ITEM_RE.findall(doc.body)
        if not unchecked:
            return
        findings.add(attach_clause(Finding(
            gate_id=f"{self.id}.go_live_readiness_checklist_complete",
            severity=Severity.HIGH,
            message=(
                f"Go-live readiness '{_posix(doc.path)}' has "
                f"{len(unchecked)} unchecked item(s)"
            ),
            location=doc.path,
            line=None,
        ), _CLAUSE))

    # -- Check 6: change window documented -------------------------------
    def _check_change_window_documented(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        if _find_change_window_doc(graph) is not None:
            return
        guide = _find_deployment_guide(graph)
        if guide is not None:
            lower = guide.body.lower()
            if any(phrase in lower for phrase in _CHANGE_WINDOW_PHRASES):
                return
        findings.add(attach_clause(Finding(
            gate_id=f"{self.id}.change_window_documented",
            severity=Severity.HIGH,
            message=(
                "No change window documentation found (expected "
                "dedicated 'change-window.md' or 'change window' "
                "reference in deployment guide)"
            ),
            location=None,
            line=None,
        ), _CLAUSE))
