"""Find [TAG: reason] markers in markdown.

Markers that appear inside inline code spans (`...`) or fenced code blocks
(```...```) are treated as documentation of the convention and are not
reported as live findings. This lets SRS/SOP documents describe the tag
vocabulary ("flag gaps with `[CONTEXT-GAP: topic]`") without triggering
the kernel.
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import List

_PATTERN = re.compile(r"\[(?P<tag>[A-Z&\-]+)(?::\s*(?P<reason>[^\]]*))?\]")
_FENCE = re.compile(r"^\s*(```|~~~)")
_KNOWN_TAGS = {
    "V&V-FAIL", "CONTEXT-GAP", "GLOSSARY-GAP",
    "SMART-FAIL", "TRACE-GAP", "VERIFIABILITY-FAIL",
    "DPPA-FAIL", "DPIA-REQUIRED", "CONTROL-GAP",
    "DOMAIN-DEFAULT",
    # M10-08-T03 (GR-10): as-built provenance tags. Recognised so the graph
    # reports them; deliberately NOT in checks/markers.py _BLOCKING_TAGS.
    "AS-BUILT", "VERIFY",
}


@dataclass(frozen=True)
class Marker:
    tag: str
    reason: str
    line: int


def _strip_inline_code(line: str) -> str:
    """Replace inline code spans with spaces so markers inside them are
    not matched. Handles single (`x`) and double (``x``) backtick spans."""
    # Double-backtick spans first (so they don't get half-eaten by the
    # single-backtick pass). Non-greedy match.
    line = re.sub(r"``[^`]+?``", lambda m: " " * len(m.group(0)), line)
    line = re.sub(r"`[^`]+?`", lambda m: " " * len(m.group(0)), line)
    return line


def find_markers(body: str) -> List[Marker]:
    out: List[Marker] = []
    in_fence = False
    for lineno, line in enumerate(body.splitlines(), start=1):
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        scan_line = _strip_inline_code(line)
        for m in _PATTERN.finditer(scan_line):
            tag = m.group("tag")
            if tag not in _KNOWN_TAGS:
                continue
            reason = (m.group("reason") or "").strip()
            out.append(Marker(tag=tag, reason=reason, line=lineno))
    return out
