# Source reconciliation before requirements classification

Create `projects/<ProjectName>/_registry/source-reconciliation.yaml` from
`references/source-reconciliation-template.yaml`. Assign each material source
statement a stable `SRC-###` ID and cite its source. Map it to one or more
requirement IDs, or to an `AMB-###` record when meaning, priority, scope, or
the relationship to another statement remains unresolved. Link every affected
statement to the same ambiguity record. Preserve alternatives and name an
accountable owner, or record `unassigned`; do not choose an outcome during
analysis.

Run `python -X utf8 scripts/validate_source_reconciliation.py
projects/<ProjectName>` before the Phase 02 gate. The validator checks record
shape, declared links, and decision evidence. It cannot detect omitted source
statements or determine whether two statements are semantically contradictory;
the analyst and independent reviewer must assess and record those matters.
Use a faithful summary and source reference instead of copying sensitive text
when that is sufficient.
