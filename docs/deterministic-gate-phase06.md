# Deterministic Gate: Phase 06

## Scope

Phase 06 validates deployment and operations readiness.

## Standard Anchor

- IEEE Std 1062-2015 clause 6.3

## Enforced Checks

- `phase06.deployment_guide_has_rollback`
- `phase06.runbook_has_escalation`
- `phase06.monitoring_has_slo`
- `phase06.infra_has_ir_diagram`
- `phase06.go_live_readiness_checklist_complete`
- `phase06.change_window_documented`

## Intent

- Require rollback procedures in deployment guides
- Require escalation paths in runbooks
- Require SLO, SLI, or SLA references in monitoring docs
- Require an incident-response figure in infrastructure docs: the document discusses incident response and carries a figure about it, either an image whose file exists or a Mermaid block whose rendering is recorded in `_figures/render-manifest.json` by `scripts/render_diagrams.py`. The words `mermaid` or `plantuml`, or a code block alone, no longer pass (M10-01-T12). `engine/figures.py` `FIGURE_PROVIDERS` is the extension point for the diagram-IR sidecar (M10-07)
- Require complete go-live readiness checklists
- Require a documented change window

## Pass Condition

Operational artefacts are specific enough to support repeatable release, rollback, monitoring, escalation, and cutover planning.
