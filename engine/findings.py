"""Finding, Severity, and FindingCollection.

M10-07-T04 (AR-08) adds four optional, keyword-only fields to ``Finding`` so a
check can say *what* failed in a machine-readable way: ``code`` (a stable
diagnostic code such as ``diagram/unknown-trace-id``), ``subject`` (what the
finding is about, e.g. ``{"figure_id": ..., "path": <JSON pointer>}``),
``evidence`` (the values that triggered it) and ``supported_fixes`` (repairs
a repairing agent may make). They default to empty, so every existing
``Finding(...)`` call is unchanged and reporters emit them only when present.
The diagnostic shape is adapted from Archify (MIT,
https://github.com/tt-a1i/archify, commit
0e4949f910a8e390bd3b4933883a4dcabad571be), paraphrased; no code copied.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Any, Iterable, Optional

class Severity(IntEnum):
    INFO = 10
    LOW = 20
    MEDIUM = 30
    HIGH = 40

@dataclass(frozen=True)
class Finding:
    gate_id: str
    severity: Severity
    message: str
    location: Optional[Path]
    line: Optional[int]
    code: Optional[str] = field(default=None, kw_only=True)
    subject: Optional[dict[str, Any]] = field(default=None, kw_only=True, compare=False, hash=False)
    evidence: Optional[dict[str, Any]] = field(default=None, kw_only=True, compare=False, hash=False)
    supported_fixes: tuple[str, ...] = field(default=(), kw_only=True)

    @property
    def has_diagnostics(self) -> bool:
        """True when any of the M10-07 optional diagnostic fields is set."""
        return bool(self.code or self.subject or self.evidence or self.supported_fixes)

class FindingCollection:
    def __init__(self) -> None:
        self._items: list[Finding] = []

    def add(self, finding: Finding) -> None:
        self._items.append(finding)

    def extend(self, findings: Iterable[Finding]) -> None:
        self._items.extend(findings)

    def for_gate(self, gate_id: str) -> list[Finding]:
        return [f for f in self._items if f.gate_id == gate_id]

    @property
    def is_blocking(self) -> bool:
        return any(f.severity >= Severity.HIGH for f in self._items)

    def __iter__(self):
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)
