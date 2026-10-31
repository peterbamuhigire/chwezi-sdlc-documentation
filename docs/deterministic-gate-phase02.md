# Deterministic Gate: Phase 02

## Scope

Phase 02 validates requirements quality and registry coherence.

## Standard Anchors

- IEEE Std 830-1998 clause 3.2
- IEEE Std 830-1998 clause 3.3.2
- IEEE Std 830-1998 clause 4.3

## Enforced Checks

- `phase02.smart_nfr`
- `phase02.stimulus_response`
- `phase02.requirement_semantics`
- `phase02.id_registry.unknown_id`
- `phase02.id_registry.orphan_id`
- `phase02.glossary_registry.missing_term`
- `phase02.glossary_registry.orphan_term`

## Intent

- Require measurable non-functional requirements: a vague qualifier (for example fast, reliable, quickly, at all times) needs a stated threshold in the same requirement
- Require stimulus-response style where expected
- Require normative, observable, non-ambiguous functional requirements
- Keep identifier and glossary registries aligned with the workspace

## Pass Condition

Requirements are measurable, written as enforceable statements, and kept coherent with the generated registries.
