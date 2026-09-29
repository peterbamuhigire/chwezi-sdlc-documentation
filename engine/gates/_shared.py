"""Shared helpers for phase gates."""
from __future__ import annotations
from dataclasses import dataclass, replace
from engine.findings import Finding

@dataclass(frozen=True)
class ClauseRef:
    standard: str
    clause: str

    def label(self) -> str:
        return f"[{self.standard} §{self.clause}]"

def attach_clause(finding: Finding, clause: ClauseRef) -> Finding:
    # dataclasses.replace keeps the optional diagnostic fields (M10-07-T04).
    return replace(finding, message=f"{finding.message} {clause.label()}")
