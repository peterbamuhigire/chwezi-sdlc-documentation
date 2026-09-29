"""BaselineDeltaCheck: confirm the declared current baseline file exists.

M10-07-T07: when ``_registry/baselines.yaml`` also declares ``previous`` and
both snapshot files exist, the diagram elements that were added, removed,
changed or moved between the two baselines are reported as one INFO finding
(code ``diagram/baseline-delta``) for review. The report infers no impact,
risk or merge safety (bound adapted from Archify, MIT,
https://github.com/tt-a1i/archify, commit
0e4949f910a8e390bd3b4933883a4dcabad571be; paraphrased).
"""
from __future__ import annotations
from pathlib import Path
from ruamel.yaml import YAML
from engine.artifact_graph import ArtifactGraph
from engine.findings import Finding, FindingCollection, Severity

_yaml = YAML(typ="safe")


class BaselineDeltaCheck:
    def __init__(self, gate_id: str, project_root: Path) -> None:
        self.gate_id = gate_id
        self._project = project_root

    def run(self, _graph: ArtifactGraph, findings: FindingCollection) -> None:
        baselines_path = self._project / "_registry" / "baselines.yaml"
        if not baselines_path.exists():
            return
        try:
            data = _yaml.load(baselines_path.read_text(encoding="utf-8")) or {}
        except Exception as exc:
            findings.add(Finding(
                gate_id=f"{self.gate_id}.current_missing",
                severity=Severity.HIGH,
                message=f"_registry/baselines.yaml parse error: {exc}",
                location=baselines_path, line=None,
            ))
            return
        current = data.get("current")
        if not current:
            return
        snap_path = (
            self._project / "09-governance-compliance" / "07-baseline-delta"
            / f"{current}.yaml"
        )
        if not snap_path.exists():
            findings.add(Finding(
                gate_id=f"{self.gate_id}.current_missing",
                severity=Severity.HIGH,
                message=(
                    f"_registry/baselines.yaml declares current={current} but "
                    f"'09-governance-compliance/07-baseline-delta/{current}.yaml' "
                    f"is missing"
                ),
                location=baselines_path, line=None,
            ))
            return
        previous = data.get("previous")
        if previous:
            self._report_diagram_delta(str(previous), str(current), findings)

    def _report_diagram_delta(self, previous: str, current: str,
                              findings: FindingCollection) -> None:
        from engine.baseline import diagram_diff, load_snapshot
        base = self._project / "09-governance-compliance" / "07-baseline-delta"
        old_path, new_path = base / f"{previous}.yaml", base / f"{current}.yaml"
        if not old_path.exists():
            return
        delta = diagram_diff(load_snapshot(old_path), load_snapshot(new_path))
        if not any(delta.values()):
            return
        summary = ", ".join(f"{k} {len(v)}" for k, v in delta.items())
        findings.add(Finding(
            gate_id=f"{self.gate_id}.diagram_delta",
            severity=Severity.INFO,
            message=(f"Diagram elements between {previous} and {current}: {summary}. "
                     "Review each; this report infers no impact or risk."),
            location=new_path.relative_to(self._project), line=None,
            code="diagram/baseline-delta",
            evidence={k: list(v) for k, v in delta.items()},
        ))
