"""SARIF 2.1.0 reporter."""
from __future__ import annotations
import json
from collections import defaultdict
from engine.findings import FindingCollection, Severity

_LEVELS = {Severity.HIGH: "error", Severity.MEDIUM: "warning",
           Severity.LOW: "note", Severity.INFO: "note"}

def render_sarif(findings: FindingCollection) -> str:
    rules: dict[str, dict] = {}
    results = []
    for f in findings:
        # A finding with a diagnostic code reports it as the SARIF rule and
        # keeps the gate id in properties (M10-07-T04); others are unchanged.
        rule_id = f.code or f.gate_id
        rules.setdefault(rule_id, {
            "id": rule_id,
            "shortDescription": {"text": rule_id},
        })
        result = {
            "ruleId": rule_id,
            "level": _LEVELS[f.severity],
            "message": {"text": f.message},
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": f.location.as_posix() if f.location else "",
                    },
                    "region": {"startLine": f.line or 1},
                },
            }],
        }
        if f.has_diagnostics:
            props: dict = {"gateId": f.gate_id}
            if f.subject:
                props["subject"] = f.subject
            if f.evidence:
                props["evidence"] = f.evidence
            if f.supported_fixes:
                props["supportedFixes"] = list(f.supported_fixes)
            result["properties"] = props
        results.append(result)
    sarif = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [{
            "tool": {"driver": {
                "name": "chwezi-sdlc-documentation-engine",
                "rules": list(rules.values()),
            }},
            "results": results,
        }],
    }
    return json.dumps(sarif, indent=2)
