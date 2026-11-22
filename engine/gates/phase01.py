"""Phase 01 — Strategic Vision gate."""
from __future__ import annotations
import re
from engine.artifact_graph import ArtifactGraph
from engine.findings import Finding, FindingCollection, Severity
from engine.gates.base import Gate
from engine.gates._shared import ClauseRef, attach_clause

_REQUIRED = ("vision.md", "stakeholders.md", "features.md", "glossary.md")
_FEATURE = re.compile(r"-\s+(F-\d+)\s+([^—]+)—\s+driven\s+by\s+(.+)", re.IGNORECASE)
_CLAUSE = ClauseRef("IEEE Std 29148-2018", "5.2")

class Phase01Gate(Gate):
    id = "phase01"
    title = "Strategic Vision phase gate"
    severity = Severity.HIGH

    def evaluate(self, graph: ArtifactGraph, findings: FindingCollection) -> None:
        required = any(a.path.as_posix() == "_context/methodology.md" and
                       a.frontmatter.get("product_market_strategy") == "required"
                       for a in graph.artifacts)
        if required:
            strategies = [a for a in graph.artifacts if a.document == "product-market-strategy"]
            if len(strategies) != 1 or strategies[0].frontmatter.get("strategy_status") != "reviewed":
                findings.add(Finding(
                    gate_id="phase01.product_market_strategy", severity=Severity.HIGH,
                    message="Register one reviewed product marketing and website strategy or internal adoption plan.",
                    location=strategies[0].path if strategies else None, line=None,
                ))
        # Check 1: canonical inputs present
        present = {a.path.name for a in graph.artifacts if a.path.parts[0] == "_context"}
        for fname in _REQUIRED:
            if fname not in present:
                findings.add(attach_clause(Finding(
                    gate_id=f"{self.id}.canonical_inputs_present",
                    severity=Severity.HIGH,
                    message=f"Missing required canonical input: _context/{fname}",
                    location=None, line=None,
                ), _CLAUSE))

        # Check 2: every feature has a driving stakeholder
        stakeholders_text = ""
        for art in graph.artifacts:
            if art.path.name == "stakeholders.md":
                stakeholders_text = art.body
        for art in graph.artifacts:
            if art.path.name == "features.md":
                for lineno, line in enumerate(art.body.splitlines(), start=1):
                    m = _FEATURE.search(line)
                    if not m:
                        continue
                    fid, _name, driver = m.group(1), m.group(2), m.group(3).strip()
                    if driver.lower() in {"no-one", "noone", "none", "unknown"}:
                        findings.add(attach_clause(Finding(
                            gate_id=f"{self.id}.feature_has_stakeholder",
                            severity=Severity.HIGH,
                            message=f"{fid} has no identified driving stakeholder",
                            location=art.path, line=lineno,
                        ), _CLAUSE))
                    elif driver and driver not in stakeholders_text:
                        findings.add(attach_clause(Finding(
                            gate_id=f"{self.id}.feature_has_stakeholder",
                            severity=Severity.MEDIUM,
                            message=f"{fid} cites stakeholder '{driver}' not in stakeholders.md",
                            location=art.path, line=lineno,
                        ), _CLAUSE))
