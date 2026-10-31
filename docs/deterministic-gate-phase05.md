# Deterministic Gate: Phase 05

## Scope

Phase 05 validates testing artefacts and evidence quality.

## Standard Anchor

- BS ISO/IEC/IEEE 29119-3:2013 clauses 7.2 to 7.6

## Enforced Checks

- `phase05.normative_test_structure`
- `phase05.test_oracles`
- `phase05.required_evidence`
- `phase05.coverage_measurable`
- `phase05.exit_evidence`

## Intent

- Require test-plan frontmatter for `inputs`, `expected_results`, and `requirement_trace`
- Require meaningful test oracles and requirement-linked traces (`FR`, `NFR`, `IR`, `DR` or `CON` identifiers, with optional module segments such as `FR-META-006`)
- Require deterministic-check and completion evidence files
- Require measurable FR-to-TC coverage

## Pass Condition

Testing artefacts contain structured evidence, objective expected results, and measurable coverage back to requirements.
