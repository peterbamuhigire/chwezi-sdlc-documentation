#!/usr/bin/env python3
"""Repo-level engine contract validator (legacy entry-point).

Behaviour is preserved verbatim from the previous version. New work should
prefer `python -m engine validate <project-path>`, which validates a single
project workspace; this script validates the repo-level engine contract.
"""
from __future__ import annotations
import re as _re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_CHECK_ID_PATTERN = _re.compile(r'gate_id=f"\{self\.id\}\.(\w+)"')
_GATE_ID_PATTERN = _re.compile(r'^\s*id\s*=\s*"(phase\d{2})"', _re.MULTILINE)

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def must_exist(rel_path: str, errors: list[str]) -> Path | None:
    path = ROOT / rel_path
    if not path.exists():
        errors.append(f"Missing required file: {rel_path}")
        return None
    return path

def require_substrings(rel_path: str, required: list[str], errors: list[str]) -> None:
    path = must_exist(rel_path, errors)
    if path is None:
        return
    body = read_text(path)
    for needle in required:
        if needle not in body:
            errors.append(f"{rel_path} missing required text: {needle}")

def validate_root_pathing(errors: list[str]) -> None:
    canonical = "projects/<ProjectName>/"
    alias_a = "../project_context/"
    alias_b = "../output/"
    alias_language = "alias"
    for rel_path in ["README.md", "AGENTS.md"]:  # CLAUDE.md is a thin @AGENTS.md bridge (M10-02)
        require_substrings(rel_path, [canonical], errors)
        body = read_text(ROOT / rel_path)
        if alias_a in body or alias_b in body:
            if alias_language not in body.lower():
                errors.append(
                    f"{rel_path} references legacy relative paths without explicitly calling them aliases"
                )
    phase_docs = [
        "01-strategic-vision/README.md",
        "02-requirements-engineering/agile/README.md",
        "03-design-documentation/README.md",
        "06-deployment-operations/README.md",
    ]
    for rel_path in phase_docs:
        path = must_exist(rel_path, errors)
        if path is None:
            continue
        body = read_text(path)
        mentions_legacy = alias_a in body or alias_b in body
        if mentions_legacy:
            if "projects/<ProjectName>/" not in body:
                errors.append(
                    f"{rel_path} references legacy relative paths without the canonical project workspace"
                )
            if alias_language not in body.lower():
                errors.append(
                    f"{rel_path} references legacy relative paths without explicit alias wording"
                )

def validate_deterministic_gates(errors: list[str]) -> None:
    gate_files = {f"{n:02d}": f"docs/deterministic-gate-phase{n:02d}.md" for n in range(1, 10)}
    gate_files["hybrid"] = "docs/deterministic-gate-hybrid.md"
    for rel_path in gate_files.values():
        must_exist(rel_path, errors)
    governance = must_exist("docs/deterministic-governance.md", errors)
    if governance is None:
        return
    body = read_text(governance)
    for phase, rel_path in gate_files.items():
        if rel_path.split("/")[-1] not in body:
            errors.append(
                f"docs/deterministic-governance.md does not reference the Phase {phase} gate file"
            )

def _collect_check_ids_from_source(errors: list[str]) -> set[str]:
    """Scan engine/gates/phase*.py for every emitted check ID.

    Scans gate source files (not the CLI registry) so the assertion stays
    robust even if a gate is temporarily unregistered. Also adds kernel-level
    check IDs that live outside engine/gates/.
    """
    ids: set[str] = set()
    gates_dir = ROOT / "engine" / "gates"
    for path in sorted(gates_dir.glob("phase*.py")):
        src = read_text(path)
        gate_id_match = _GATE_ID_PATTERN.search(src)
        if not gate_id_match:
            errors.append(
                f"{path.relative_to(ROOT)} does not declare an id = 'phaseNN' attribute"
            )
            continue
        gate_id = gate_id_match.group(1)
        for check_name in _CHECK_ID_PATTERN.findall(src):
            ids.add(f"{gate_id}.{check_name}")
    # Kernel-level check IDs (hard-coded: the kernel markers check lives
    # outside engine/gates/, so source scanning would miss it).
    ids.add("kernel.no_unresolved_fail_markers")
    ids.add("kernel.legacy_skill_paths")
    # Phase 09 traceability delegates to TraceabilityCheck, so it never
    # appears as a literal gate_id=f"{self.id}.<name>" string. Add it
    # explicitly so the registry assertion covers it.
    ids.add("phase09.traceability")
    # Phase 09 identifier_registry and glossary_registry delegate to
    # IdentifierRegistryCheck / GlossaryRegistryCheck, which emit their
    # own nested gate IDs (e.g. `phase09.id_registry.<name>`,
    # `phase09.glossary_registry.<name>`) from engine/checks/. Add them
    # explicitly so the registry assertion covers them.
    ids.add("phase09.id_registry.unknown_id")
    ids.add("phase09.id_registry.orphan_id")
    ids.add("phase09.glossary_registry.missing_term")
    ids.add("phase09.glossary_registry.orphan_term")
    # Phase 09 nfr_threshold_dedup delegates to NfrThresholdDedupCheck, which
    # emits its own nested gate ID `phase09.nfr_threshold_dedup.contradiction`
    # from engine/checks/. Add it explicitly so the registry assertion covers
    # it.
    ids.add("phase09.nfr_threshold_dedup.contradiction")
    # Phase 09 controls delegates to ControlsCheck (engine/checks/controls.py),
    # which emits nested gate IDs. Add them explicitly so the registry
    # assertion covers them.
    ids.add("phase09.controls.no_selection")
    ids.add("phase09.controls.unknown_control")
    ids.add("phase09.controls.missing_evidence")
    ids.add("phase09.controls.unused_in_artifacts")
    # Phase 09 obligations delegates to ObligationsCheck
    # (engine/checks/obligations.py).
    ids.add("phase09.obligations.missing_framework_coverage")
    ids.add("phase09.obligations.unsatisfied")
    # Phase 09 enterprise-artifact checks (Plan 07): adr_catalog,
    # change_impact, baseline_delta, sign_off each delegate to a Check
    # class in engine/checks/, so their nested gate IDs are not scanned
    # from gate source. Add them explicitly.
    ids.add("phase09.adr_catalog.uncatalogued")
    ids.add("phase09.adr_catalog.missing_file")
    ids.add("phase09.adr_catalog.dangling_supersession")
    ids.add("phase09.adr_catalog.schema_violation")
    ids.add("phase09.change_impact.missing_rollback_plan")
    ids.add("phase09.change_impact.schema_violation")
    ids.add("phase09.baseline_delta.current_missing")
    ids.add("phase09.baseline_delta.diagram_delta")
    # Phase 03 diagram_trace delegates to DiagramTraceCheck (M10-07-T03).
    ids.add("phase03.diagram_trace")
    ids.add("phase09.sign_off.missing_artifact")
    ids.add("phase09.sign_off.schema_violation")
    # Phase 02 delegates its four checks (smart_nfr, stimulus_response,
    # id_registry, glossary_registry) to engine/checks/ modules. None of
    # them emit findings via the `gate_id=f"{self.id}.<name>"` literal the
    # regex scanner looks for, so add them explicitly.
    ids.add("phase02.smart_nfr")
    ids.add("phase02.stimulus_response")
    ids.add("phase02.id_registry.unknown_id")
    ids.add("phase02.id_registry.orphan_id")
    ids.add("phase02.glossary_registry.missing_term")
    ids.add("phase02.glossary_registry.orphan_term")
    # Hybrid gate delegates to HybridTracesCheck (engine/checks/) and emits
    # two direct gate-level findings. Register all five IDs explicitly so the
    # clause-registry assertion covers them.
    ids.add("hybrid.traces.missing")
    ids.add("hybrid.traces.unknown_trace")
    ids.add("hybrid.traces.orphan_baseline")
    ids.add("hybrid.dor_dod_missing")
    ids.add("hybrid.dor_dod_decoupled")
    return ids

def validate_standards_clause_registry(errors: list[str]) -> None:
    """Assert every emitted check ID has a row in standards-clause-registry.md."""
    registry_path = must_exist("docs/standards-clause-registry.md", errors)
    if registry_path is None:
        return
    registry_body = read_text(registry_path)
    emitted = _collect_check_ids_from_source(errors)
    for check_id in sorted(emitted):
        if f"`{check_id}`" not in registry_body:
            errors.append(
                f"docs/standards-clause-registry.md does not cover check id `{check_id}` — "
                f"add a row mapping it to a standard and clause"
            )

def validate_hybrid_and_regulated_models(errors: list[str]) -> None:
    required_docs = [
        "docs/hybrid-operating-model.md",
        "docs/regulated-evidence-model.md",
    ]
    for rel_path in required_docs:
        must_exist(rel_path, errors)
    require_substrings(
        "README.md",
        ["docs/hybrid-operating-model.md", "docs/regulated-evidence-model.md"],
        errors,
    )

def main() -> int:
    errors: list[str] = []
    validate_root_pathing(errors)
    validate_deterministic_gates(errors)
    validate_standards_clause_registry(errors)
    validate_hybrid_and_regulated_models(errors)
    if errors:
        print("ENGINE CONTRACT: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ENGINE CONTRACT: PASS")
    print("- Canonical pathing and alias semantics are documented.")
    print("- Deterministic gate docs exist for phases 01-09.")
    print("- Standards clause registry is complete.")
    print("- Hybrid operating model is documented.")
    print("- Regulated evidence model is documented.")
    print()
    print("NOTE: For per-project validation, use `python -m engine validate <projects/<Name>>`.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
