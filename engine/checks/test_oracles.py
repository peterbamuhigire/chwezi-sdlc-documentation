"""Test artifacts must contain meaningful oracles and requirement traces."""
from __future__ import annotations
import re
from typing import Iterable
from engine.artifact_graph import ArtifactGraph
from engine.findings import Finding, FindingCollection, Severity

# A requirement identifier: FR, NFR, IR, DR or CON, with optional module segments (FR-META-006).
_REQUIREMENT_ID = re.compile(r"(?:FR|NFR|IR|DR|CON)(?:-[A-Z][A-Z0-9]{0,7})*-\d{3,5}")


def _values(obj) -> list[str]:
    if obj is None:
        return []
    if isinstance(obj, str):
        return [obj.strip()] if obj.strip() else []
    if isinstance(obj, Iterable) and not isinstance(obj, (bytes, bytearray, dict)):
        out: list[str] = []
        for item in obj:
            if isinstance(item, str) and item.strip():
                out.append(item.strip())
        return out
    return []


class TestOraclesCheck:
    def __init__(self, gate_id: str) -> None:
        self.gate_id = gate_id

    def run(self, graph: ArtifactGraph, findings: FindingCollection) -> None:
        for art in graph.artifacts:
            if art.phase != "05":
                continue
            inputs = _values(art.frontmatter.get("inputs"))
            expected = _values(art.frontmatter.get("expected_results"))
            traced = _values(art.frontmatter.get("requirement_trace"))
            if "requirement_trace" in art.frontmatter and not traced:
                findings.add(Finding(
                    gate_id=self.gate_id,
                    severity=Severity.HIGH,
                    message=f"Test artifact '{art.path}' has empty requirement_trace",
                    location=art.path,
                    line=None,
                ))
            if "expected_results" in art.frontmatter and not expected:
                findings.add(Finding(
                    gate_id=self.gate_id,
                    severity=Severity.HIGH,
                    message=f"Test artifact '{art.path}' has empty expected_results",
                    location=art.path,
                    line=None,
                ))
            if "inputs" in art.frontmatter and not inputs:
                findings.add(Finding(
                    gate_id=self.gate_id,
                    severity=Severity.HIGH,
                    message=f"Test artifact '{art.path}' has empty inputs",
                    location=art.path,
                    line=None,
                ))
            bad_trace = [ref for ref in traced if not _REQUIREMENT_ID.fullmatch(ref)]
            if bad_trace:
                findings.add(Finding(
                    gate_id=self.gate_id,
                    severity=Severity.HIGH,
                    message=(
                        f"Test artifact '{art.path}' has non-requirement identifiers in "
                        f"requirement_trace: {', '.join(sorted(bad_trace))}"
                    ),
                    location=art.path,
                    line=None,
                ))
