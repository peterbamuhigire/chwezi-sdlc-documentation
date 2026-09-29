# Standards Clause Registry

Source-of-truth mapping: every check ID emitted by a phase gate or kernel check, and the standards clause it enforces. A reviewer reading this document can audit "what does the engine claim to enforce, and against which authority?" without reading gate source code.

This document is validated by `scripts/validate_engine.py`: every check ID that appears in `engine/gates/phase*.py` (via `gate_id=f"{self.id}.<name>"`) must have a row here, plus the kernel-level `kernel.no_unresolved_fail_markers` check.

## Phase 01 — Strategic Vision

| Check ID | Standard | Clause | Engine module |
|---|---|---|---|
| `phase01.canonical_inputs_present` | IEEE Std 29148-2018 | §5.2 | `engine/gates/phase01.py` |
| `phase01.feature_has_stakeholder` | IEEE Std 29148-2018 | §5.2 | `engine/gates/phase01.py` |

## Phase 02 — Requirements Engineering

| Check ID | Standard | Clause | Engine module |
|---|---|---|---|
| `phase02.smart_nfr` | IEEE Std 830-1998 | §4.3.2 | `engine/checks/nfr_smart.py` |
| `phase02.stimulus_response` | IEEE Std 830-1998 | §4.3.1 | `engine/checks/stimulus_response.py` |
| `phase02.id_registry.unknown_id` | IEEE Std 830-1998 | §4.3 | `engine/checks/identifier_registry.py` |
| `phase02.id_registry.orphan_id` | IEEE Std 830-1998 | §4.3 | `engine/checks/identifier_registry.py` |
| `phase02.glossary_registry.missing_term` | IEEE Std 830-1998 | §4.3 | `engine/checks/glossary_registry.py` |
| `phase02.glossary_registry.orphan_term` | IEEE Std 830-1998 | §4.3 | `engine/checks/glossary_registry.py` |

## Phase 03 — Design Documentation

| Check ID | Standard | Clause | Engine module |
|---|---|---|---|
| `phase03.architecture_decisions_recorded` | ISO/IEC/IEEE 42010:2011 | §5.3 | `engine/gates/phase03.py` |
| `phase03.interfaces_have_contracts` | ISO/IEC/IEEE 42010:2011 | §5.3 | `engine/gates/phase03.py` |
| `phase03.data_model_has_keys` | ISO/IEC/IEEE 42010:2011 | §5.3 | `engine/gates/phase03.py` |
| `phase03.nfrs_link_to_design_choices` | ISO/IEC/IEEE 42010:2011 | §5.3 | `engine/gates/phase03.py` |
| `phase03.security_threat_model_present` | ISO/IEC/IEEE 42010:2011 | §5.3 | `engine/gates/phase03.py` |
| `phase03.iot_signal_inventory_present` | ISO/IEC/IEEE 42010:2011 | §5.3 | `engine/gates/phase03.py` |
| `phase03.design_docs_have_figures` | ISO/IEC/IEEE 42010:2011 | §5.6 | `engine/gates/phase03.py` |
| `phase03.diagram_trace` | ISO/IEC/IEEE 42010:2011 | §5.6 | `engine/checks/diagram_trace.py` |

## Phase 04 — Development Artifacts

| Check ID | Standard | Clause | Engine module |
|---|---|---|---|
| `phase04.coding_standards_referenced` | ISO/IEC/IEEE 12207:2017 | §6.4.5 | `engine/gates/phase04.py` |
| `phase04.env_setup_reproducible` | ISO/IEC/IEEE 12207:2017 | §6.4.5 | `engine/gates/phase04.py` |
| `phase04.tech_spec_links_to_fr` | ISO/IEC/IEEE 12207:2017 | §6.4.5 | `engine/gates/phase04.py` |
| `phase04.contrib_guide_present` | ISO/IEC/IEEE 12207:2017 | §6.4.5 | `engine/gates/phase04.py` |

## Phase 05 — Testing Documentation

| Check ID | Standard | Clause | Engine module |
|---|---|---|---|
| `phase05.normative_test_structure` | BS ISO/IEC/IEEE 29119-3:2013 | §7.2 | `engine/gates/phase05.py` |
| `phase05.required_evidence` | BS ISO/IEC/IEEE 29119-3:2013 | §7.2 | `engine/gates/phase05.py` |
| `phase05.coverage_measurable` | BS ISO/IEC/IEEE 29119-3:2013 | §7.2 | `engine/gates/phase05.py` |
| `phase05.exit_evidence` | BS ISO/IEC/IEEE 29119-3:2013 | §7.2 | `engine/gates/phase05.py` |

## Phase 06 — Deployment & Operations

| Check ID | Standard | Clause | Engine module |
|---|---|---|---|
| `phase06.deployment_guide_has_rollback` | IEEE Std 1062-2015 | §6.3 | `engine/gates/phase06.py` |
| `phase06.runbook_has_escalation` | IEEE Std 1062-2015 | §6.3 | `engine/gates/phase06.py` |
| `phase06.monitoring_has_slo` | IEEE Std 1062-2015 | §6.3 | `engine/gates/phase06.py` |
| `phase06.infra_has_ir_diagram` | IEEE Std 1062-2015 | §6.3 | `engine/gates/phase06.py` |
| `phase06.go_live_readiness_checklist_complete` | IEEE Std 1062-2015 | §6.3 | `engine/gates/phase06.py` |
| `phase06.change_window_documented` | IEEE Std 1062-2015 | §6.3 | `engine/gates/phase06.py` |

## Phase 07 — Agile Artifacts

| Check ID | Standard | Clause | Engine module |
|---|---|---|---|
| `phase07.dor_references_baseline` | PMBOK Guide 7th Edition | §2.6 | `engine/gates/phase07.py` |
| `phase07.dod_references_compliance` | PMBOK Guide 7th Edition | §2.6 | `engine/gates/phase07.py` |
| `phase07.sprint_artifacts_have_ids` | PMBOK Guide 7th Edition | §2.6 | `engine/gates/phase07.py` |
| `phase07.retro_actions_assigned` | PMBOK Guide 7th Edition | §2.6 | `engine/gates/phase07.py` |
| `phase07.velocity_history_present` | PMBOK Guide 7th Edition | §2.6 | `engine/gates/phase07.py` |

## Phase 08 — End-User Documentation

| Check ID | Standard | Clause | Engine module |
|---|---|---|---|
| `phase08.user_manual_has_screenshots` | IEEE Std 26514-2022 | §8 | `engine/gates/phase08.py` |
| `phase08.release_notes_link_to_fr` | IEEE Std 26514-2022 | §8 | `engine/gates/phase08.py` |
| `phase08.faq_has_at_least_5_qa` | IEEE Std 26514-2022 | §8 | `engine/gates/phase08.py` |

## Phase 09 — Governance & Compliance

| Check ID | Standard | Clause | Engine module |
|---|---|---|---|
| `phase09.traceability` | ISO/IEC 27001:2022 | §9 | `engine/gates/phase09.py` |
| `phase09.audit_report_present` | ISO/IEC 27001:2022 | §9 | `engine/gates/phase09.py` |
| `phase09.risk_register_links_to_fr` | ISO/IEC 27001:2022 | §9 | `engine/gates/phase09.py` |
| `phase09.waivers_have_expiry` | ISO/IEC 27001:2022 | §9 | `engine/gates/phase09.py` |
| `phase09.id_registry.unknown_id` | ISO/IEC 27001:2022 | §9 | `engine/checks/identifier_registry.py` |
| `phase09.id_registry.orphan_id` | ISO/IEC 27001:2022 | §9 | `engine/checks/identifier_registry.py` |
| `phase09.glossary_registry.missing_term` | ISO/IEC 27001:2022 | §9 | `engine/checks/glossary_registry.py` |
| `phase09.glossary_registry.orphan_term` | ISO/IEC 27001:2022 | §9 | `engine/checks/glossary_registry.py` |
| `phase09.nfr_threshold_dedup.contradiction` | IEEE Std 830-1998 | §4.3.2 | `engine/checks/nfr_threshold_dedup.py` |
| `phase09.controls.no_selection` | ISO/IEC 27001:2022 | §9 | `engine/checks/controls.py` |
| `phase09.controls.unknown_control` | ISO/IEC 27001:2022 | §9 | `engine/checks/controls.py` |
| `phase09.controls.missing_evidence` | ISO/IEC 27001:2022 | §9 | `engine/checks/controls.py` |
| `phase09.controls.unused_in_artifacts` | ISO/IEC 27001:2022 | §9 | `engine/checks/controls.py` |
| `phase09.obligations.missing_framework_coverage` | ISO/IEC 27001:2022 | §9 | `engine/checks/obligations.py` |
| `phase09.obligations.unsatisfied` | ISO/IEC 27001:2022 | §9 | `engine/checks/obligations.py` |
| `phase09.adr_catalog.uncatalogued` | ISO/IEC 27001:2022 | §9 | `engine/checks/adr_catalog.py` |
| `phase09.adr_catalog.missing_file` | ISO/IEC 27001:2022 | §9 | `engine/checks/adr_catalog.py` |
| `phase09.adr_catalog.dangling_supersession` | ISO/IEC 27001:2022 | §9 | `engine/checks/adr_catalog.py` |
| `phase09.adr_catalog.schema_violation` | ISO/IEC 27001:2022 | §9 | `engine/checks/adr_catalog.py` |
| `phase09.change_impact.missing_rollback_plan` | ISO/IEC 27001:2022 | §9 | `engine/checks/change_impact.py` |
| `phase09.change_impact.schema_violation` | ISO/IEC 27001:2022 | §9 | `engine/checks/change_impact.py` |
| `phase09.baseline_delta.current_missing` | ISO/IEC 27001:2022 | §9 | `engine/checks/baseline_delta.py` |
| `phase09.baseline_delta.diagram_delta` | ISO/IEC 27001:2022 | §9 | `engine/checks/baseline_delta.py` |
| `phase09.sign_off.missing_artifact` | ISO/IEC 27001:2022 | §9 | `engine/checks/sign_off.py` |
| `phase09.sign_off.schema_violation` | ISO/IEC 27001:2022 | §9 | `engine/checks/sign_off.py` |
| `phase09.evidence_pack_buildable` | ISO/IEC 27001:2022 | §9 | `engine/gates/phase09.py` |

## Hybrid Synchronization (active only when methodology: hybrid)

| Check ID | Standard | Clause | Engine module |
|---|---|---|---|
| `hybrid.traces.missing` | PMI Disciplined Agile (DAD) | Hybrid Lifecycle | `engine/checks/hybrid_traces.py` |
| `hybrid.traces.unknown_trace` | PMI Disciplined Agile (DAD) | Hybrid Lifecycle | `engine/checks/hybrid_traces.py` |
| `hybrid.traces.orphan_baseline` | PMI Disciplined Agile (DAD) | Hybrid Lifecycle | `engine/checks/hybrid_traces.py` |
| `hybrid.dor_dod_missing` | PMI Disciplined Agile (DAD) | Hybrid Lifecycle | `engine/gates/hybrid.py` |
| `hybrid.dor_dod_decoupled` | PMI Disciplined Agile (DAD) | Hybrid Lifecycle | `engine/gates/hybrid.py` |

## Deferred Checks (not yet emitted)

These check IDs are listed in phase-gate frontmatter as deferred — their implementations depend on future plans. Once implemented, move their rows into the appropriate phase section above.

| Check ID | Blocker | Expected Standard / Clause |
|---|---|---|
| `phase09.compliance_controls_have_evidence` | Plan 06 `ControlsCheck` | ISO/IEC 27001:2022 §9 |

## Kernel-Level Checks

| Check ID | Standard | Clause | Engine module |
|---|---|---|---|
| `kernel.no_unresolved_fail_markers` | (internal contract) | — | `engine/checks/markers.py` |
| `kernel.legacy_skill_paths` | (internal contract) | — | `engine/checks/legacy_paths.py` |

## Maintenance

When adding a new gate or check:

1. Emit findings with `gate_id = f"{self.id}.<check_name>"` — the CI assertion scans for this pattern.
2. Add a row to the appropriate phase section here.
3. Run `python scripts/validate_engine.py` to confirm the registry is complete.
