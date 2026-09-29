"""Markdown reporter."""
from __future__ import annotations
import json
from typing import Iterable
from engine.findings import Finding, FindingCollection


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def render_markdown(
    findings: FindingCollection, waived: Iterable[Finding], project: str
) -> str:
    lines = [f"# Engine Validation Report — {project}", ""]
    if len(findings) == 0:
        lines.append("**Status:** PASS — no findings.")
    else:
        lines.append(f"**Status:** {'FAIL' if findings.is_blocking else 'WARN'}")
        lines.append(f"**Findings:** {len(findings)}")
        lines.append("")
        # Code / Subject / Supported fixes columns appear only when a finding
        # carries the optional diagnostic fields (M10-07-T04), so reports
        # without them are byte-identical to earlier releases.
        extended = any(f.has_diagnostics for f in findings)
        if extended:
            lines.append("| Gate | Severity | Location | Line | Message | Code | Subject | Supported fixes |")
            lines.append("|---|---|---|---|---|---|---|---|")
        else:
            lines.append("| Gate | Severity | Location | Line | Message |")
            lines.append("|---|---|---|---|---|")
        for f in findings:
            loc = f.location.as_posix() if f.location else "-"
            line = f.line if f.line is not None else "-"
            row = f"| `{f.gate_id}` | {f.severity.name} | `{loc}` | {line} | {f.message} |"
            if extended:
                code = f"`{f.code}`" if f.code else "-"
                subject = _cell(json.dumps(f.subject, sort_keys=True)) if f.subject else "-"
                fixes = _cell("; ".join(f.supported_fixes)) if f.supported_fixes else "-"
                row += f" {code} | {subject} | {fixes} |"
            lines.append(row)
    waived_list = list(waived)
    if waived_list:
        lines.extend(["", "## Waived findings", ""])
        for f in waived_list:
            lines.append(f"- `{f.gate_id}` — {f.message}")
    return "\n".join(lines) + "\n"
