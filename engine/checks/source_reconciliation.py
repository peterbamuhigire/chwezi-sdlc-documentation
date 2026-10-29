"""Check that listed source statements map to requirements or open decisions."""
from __future__ import annotations

import re
from pathlib import Path

from ruamel.yaml import YAML

from engine.artifact_graph import ArtifactGraph
from engine.findings import Finding, Severity

_SOURCE_ID = re.compile(r"^SRC-\d{3,5}$")
_AMBIGUITY_ID = re.compile(r"^AMB-\d{3,5}$")
_REQUIREMENT_ID = re.compile(r"^(?:FR|NFR|IR|DR|CON)-\d{3,5}$")
_REQUIREMENT_IN_TEXT = re.compile(r"\*\*((?:FR|NFR|IR|DR|CON)-\d{3,5})\*\*")


class SourceReconciliationCheck:
    """Validate completeness and ownership fields; do not infer semantics."""

    def __init__(self, gate_id: str = "phase02.source_reconciliation") -> None:
        self.gate_id = gate_id

    def run(self, graph: ArtifactGraph) -> list[Finding]:
        root = graph.root
        if root is None:
            return []
        path = root / "_registry" / "source-reconciliation.yaml"
        if not path.is_file():
            return []

        findings: list[Finding] = []

        def add(code: str, message: str, line: int | None = None) -> None:
            findings.append(Finding(
                gate_id=self.gate_id,
                severity=Severity.HIGH,
                message=message,
                location=path.relative_to(root),
                line=line,
                code=f"source-reconciliation/{code}",
            ))

        try:
            raw = YAML(typ="safe").load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            add("invalid-yaml", f"Source reconciliation register is invalid YAML: {exc}")
            return findings
        if not isinstance(raw, dict):
            add("invalid-shape", "Register must be a mapping with sources and ambiguities")
            return findings

        sources = raw.get("sources")
        ambiguities = raw.get("ambiguities", [])
        if not isinstance(sources, list) or not sources:
            add("sources-required", "Register must contain at least one source statement")
            sources = []
        if not isinstance(ambiguities, list):
            add("ambiguities-shape", "ambiguities must be a list")
            ambiguities = []

        present_requirements = {
            requirement_id
            for artifact in graph.artifacts
            for requirement_id in _REQUIREMENT_IN_TEXT.findall(artifact.body)
        }
        source_by_id: dict[str, dict] = {}
        for index, item in enumerate(sources, start=1):
            if not isinstance(item, dict):
                add("source-shape", f"Source row {index} must be a mapping")
                continue
            source_id = item.get("id")
            if not isinstance(source_id, str) or not _SOURCE_ID.fullmatch(source_id):
                add("source-id", f"Source row {index} requires a unique SRC-### id")
                continue
            if source_id in source_by_id:
                add("duplicate-source-id", f"Duplicate source statement id {source_id}")
                continue
            source_by_id[source_id] = item
            for key in ("source_ref", "statement"):
                if not isinstance(item.get(key), str) or not item[key].strip():
                    add("source-evidence", f"{source_id} requires non-empty {key}")
            requirement_ids = item.get("requirement_ids", [])
            ambiguity_ids = item.get("ambiguity_ids", [])
            if not isinstance(requirement_ids, list) or not isinstance(ambiguity_ids, list):
                add("source-links-shape", f"{source_id} requirement_ids and ambiguity_ids must be lists")
                continue
            if not requirement_ids and not ambiguity_ids:
                add("source-unmapped", f"{source_id} must link to a requirement or an ambiguity")
            for requirement_id in requirement_ids:
                if not isinstance(requirement_id, str) or not _REQUIREMENT_ID.fullmatch(requirement_id):
                    add("requirement-id", f"{source_id} has an invalid requirement id {requirement_id!r}")
                elif requirement_id not in present_requirements:
                    add("requirement-missing", f"{source_id} links to absent requirement {requirement_id}")
            for ambiguity_id in ambiguity_ids:
                if not isinstance(ambiguity_id, str) or not _AMBIGUITY_ID.fullmatch(ambiguity_id):
                    add("ambiguity-id", f"{source_id} has an invalid ambiguity id {ambiguity_id!r}")

        ambiguity_by_id: dict[str, dict] = {}
        for index, item in enumerate(ambiguities, start=1):
            if not isinstance(item, dict):
                add("ambiguity-shape", f"Ambiguity row {index} must be a mapping")
                continue
            ambiguity_id = item.get("id")
            if not isinstance(ambiguity_id, str) or not _AMBIGUITY_ID.fullmatch(ambiguity_id):
                add("ambiguity-id", f"Ambiguity row {index} requires a unique AMB-### id")
                continue
            if ambiguity_id in ambiguity_by_id:
                add("duplicate-ambiguity-id", f"Duplicate ambiguity id {ambiguity_id}")
                continue
            ambiguity_by_id[ambiguity_id] = item
            source_ids = item.get("source_ids")
            if not isinstance(item.get("summary"), str) or not item["summary"].strip():
                add("ambiguity-summary", f"{ambiguity_id} requires a summary")
            if not isinstance(source_ids, list) or not source_ids:
                add("ambiguity-sources", f"{ambiguity_id} requires source_ids")
                source_ids = []
            for source_id in source_ids:
                if not isinstance(source_id, str) or source_id not in source_by_id:
                    add("ambiguity-unknown-source", f"{ambiguity_id} references unknown source {source_id!r}")
                else:
                    linked = source_by_id[source_id].get("ambiguity_ids", [])
                    if not isinstance(linked, list) or ambiguity_id not in linked:
                        add("ambiguity-backlink", f"{source_id} does not link back to {ambiguity_id}")
            status = item.get("status")
            if not isinstance(status, str) or status not in {"unresolved", "resolved"}:
                add("ambiguity-status", f"{ambiguity_id} status must be unresolved or resolved")
            if not isinstance(item.get("owner"), str) or not item["owner"].strip():
                add("ambiguity-owner", f"{ambiguity_id} requires an owner or explicit unassigned state")
            if status == "unresolved":
                add("unresolved-ambiguity", f"{ambiguity_id} remains unresolved; Phase 02 baseline is blocked")
            if status == "resolved" and (
                not isinstance(item.get("decision_ref"), str) or not item["decision_ref"].strip()
            ):
                add("resolution-evidence", f"Resolved {ambiguity_id} requires a decision_ref")

        for source_id, item in source_by_id.items():
            ambiguity_ids = item.get("ambiguity_ids", [])
            if not isinstance(ambiguity_ids, list):
                continue
            for ambiguity_id in ambiguity_ids:
                if not isinstance(ambiguity_id, str):
                    continue
                if ambiguity_id not in ambiguity_by_id:
                    add("unknown-ambiguity", f"{source_id} links to undeclared ambiguity {ambiguity_id}")

        return findings
