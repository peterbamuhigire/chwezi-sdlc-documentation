# Deterministic Gate: Phase 03

## Scope

Phase 03 validates design artefacts against requirements and architecture expectations.

## Standard Anchor

- ISO/IEC/IEEE 42010:2011 clauses 5.3 to 5.6

## Enforced Checks

- `phase03.architecture_decisions_recorded`
- `phase03.interfaces_have_contracts`
- `phase03.data_model_has_keys`
- `phase03.nfrs_link_to_design_choices`
- `phase03.requirements_have_design_evidence`
- `phase03.security_threat_model_present`
- `phase03.iot_signal_inventory_present`
- `phase03.design_docs_have_figures`
- `phase03.diagram_trace`

## Intent

- Ensure architecture decisions are explicitly recorded
- Require API contracts and primary-key declarations
- Require NFR references and FR-linked design evidence
- Require a threat model for security-sensitive design
- Require signal inventory when IoT scope is present
- Require each HLD/LLD document to carry at least one design figure a reader can see: an image whose file exists, or a Mermaid block whose rendering is recorded in `_figures/render-manifest.json` by `scripts/render_diagrams.py` with a matching source-block SHA-256. A Mermaid code block alone is source, not a figure (M10-01-T12). `engine/figures.py` `FIGURE_PROVIDERS` is the extension point; M10-07 registers the diagram-IR provider, so a `<!-- diagram-ir: FIG-nnn -->` marker whose IR is the candidate accepted by `python -m engine diagrams validate` also counts as a figure
- When a project holds diagram IR (`<doc-dir>/diagrams/*.ir.json`), check it against `engine/registry/schemas/diagram-ir.schema.json`, the identifier registry and its declared semantic checks (`phase03.diagram_trace`, M10-07-T03). Codes: `schema/<keyword>`, `diagram/unknown-trace-id`, `diagram/unknown-edge-endpoint`, `diagram/unexpected-root`, `diagram/unexpected-terminal`, `diagram/required-edge`, `diagram/required-path`, `diagram/dead-end-state` (HIGH); `diagram/uncovered-requirement` and `diagram/unmapped-sequence` (MEDIUM, report-only in this release). Coverage proves an FR is drawn somewhere, not that the drawing is correct

## Pass Condition

Design artefacts contain enough concrete evidence to show how requirements and quality attributes are implemented.
