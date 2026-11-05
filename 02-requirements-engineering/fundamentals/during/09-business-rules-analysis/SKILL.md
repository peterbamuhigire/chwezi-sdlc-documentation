---
name: 09-business-rules-analysis
description: "Use when capturing and reconciling policies, calculations, eligibility, decisions, constraints, ownership, and effective dates; use requirements-patterns to express the approved behaviour structurally."
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---

# Business Rules Analysis Skill

<!-- local-contract-start -->
<!-- dual-compat-start -->
## Use When

- capturing and reconciling policies, calculations, eligibility, decisions, constraints, ownership, and effective dates; use requirements-patterns to express the approved behaviour structurally.
- Use this procedure when the required source artefacts are available and `Business rule catalogue and contradiction log` is the next lifecycle deliverable.

## Do Not Use When

- Use `requirements-patterns` when that neighbouring route owns the decision or deliverable.
- Do not invent missing project evidence, standards clauses, thresholds, or stakeholder decisions.

## Required Inputs

| Artefact | Source or provider | Required? | Behaviour when missing |
| --- | --- | --- | --- |
| Policies, process evidence, calculations, exceptions, terminology, and rule owners | Policy owners, domain experts, and elicitation evidence | Yes | Stop the affected step, name the missing source, and return only a qualified gap record. |

## Workflow

1. Inspect the required inputs and log the exact sources, versions, and unresolved assumptions.
2. Apply this skill's existing domain workflow and decision rules to produce `Business rule catalogue and contradiction log`.
3. Stop when a required source, accountable decision owner, or deterministic test oracle is absent.
4. Recover by preserving valid work, marking the blocked scope, and returning the narrowest qualified artefact plus the next evidence needed.

## Outputs

| Artefact | Consumer | Acceptance condition |
| --- | --- | --- |
| Business rule catalogue and contradiction log | Requirements, design, test, compliance, and operations | Required sections are populated, source links resolve, and every material requirement or decision has an observable review or test oracle. |

## Evidence Produced

| Evidence | Reviewer | Acceptance condition |
| --- | --- | --- |
| Source, decision, trace, and validation record for `Business rule catalogue and contradiction log` | Requirements quality reviewer | Inputs used, decisions made, checks run, failures, and unassessed items are explicit. |

## Capability and permission boundaries

Read and search are required. This procedure is read-only by default. Editing the reviewed artefact, publishing, production mutation, destructive action, spending, or certification requires explicit authority.

## Degraded mode

Fallback: if a required file, reviewer, standard source, network check, renderer, or execution capability is unavailable, return the narrowest useful qualified result and mark the affected check `not assessed`; never convert an unassessed check into a pass.

## Decision Rules

| Choice or condition | Action | Failure or risk avoided |
| --- | --- | --- |
| Two rules overlap with different outcomes or effective periods | Escalate to the rule owner and block affected requirements until resolved. | Contradictory automated decisions. |
| Required inputs and test oracles are complete | Continue through the existing workflow and record evidence. | A deliverable whose acceptance cannot be reproduced. |
| A mandatory source or owner is missing | Stop the affected branch and issue a qualified gap record. | Fabricated context or unauthorised decisions. |

## Quality Standards

- Preserve stable identifiers and bidirectional traceability from project evidence to `Business rule catalogue and contradiction log` and its acceptance checks.
- Apply ISO/IEEE measures only with a named metric, method, threshold, evidence source, and responsible reviewer; run the anti-slop gate before release.

## Anti-Patterns

- Producing `Business rule catalogue and contradiction log` from assumed context. Fix: cite the project source or mark the scope blocked.
- Accepting a material requirement without a deterministic oracle. Fix: add a measurable result, boundary, and verification method.
- Crossing into `requirements-patterns` without routing the decision. Fix: hand off the named input and preserve trace links.
- Treating an unavailable check as passed. Fix: mark it `not assessed` and state the release consequence.
- Claiming standards, statutory, or stakeholder approval without evidence. Fix: cite the source and reviewer or qualify the claim.

## References

- [Skill authoring and release standard](../../../../docs/skill-authoring-standard.md)
- [Rule Catalog Pattern](references/rule-catalog-pattern.md)
- [Document numbering requirements](../../../references/document-numbering-requirements.md): load when rules govern invoice, receipt, order or other document numbers; catalogue each type's issue event, format and void rule from its document type register.
<!-- dual-compat-end -->
<!-- local-contract-end -->

## Overview

This skill isolates the domain rules that govern decisions, calculations, constraints, eligibility, timing, and compliance. It prevents rule logic from being buried inside requirements prose or code assumptions and turns it into a reviewable catalog that can drive requirements, test cases, and design controls.

## When to Use

- When requirements depend on policy, eligibility, pricing, approval, compliance, or timing logic
- When multiple stakeholders describe the same rule differently
- When calculations, thresholds, or conditional decisions affect acceptance criteria
- Before formal SRS logic modeling or workflow design is finalized

## Quick Reference

| Attribute | Value |
|-----------|-------|
| **Inputs** | `projects/<ProjectName>/<phase>/<document>/elicitation_log.md`, `projects/<ProjectName>/<phase>/<document>/business_process_models.md` (recommended), `projects/<ProjectName>/_context/business_rules.md` (optional), `vision.md` |
| **Output** | `projects/<ProjectName>/<phase>/<document>/business_rules_catalog.md` |
| **Tone** | Precise, policy-aware, test-oriented |
| **Standards** | Wiegers & Beatty, Volere-style rule analysis |

## Core Instructions

### Step 1: Discover Candidate Rules

Extract candidate rules from:
- stakeholder statements
- process decisions
- compliance obligations
- calculations and thresholds
- timing or sequencing constraints
- exception handling

### Step 2: Classify the Rules

Classify each rule as one of:
- policy rule
- decision rule
- calculation rule
- validation rule
- compliance rule
- temporal rule

### Step 3: Normalize Each Rule

For each rule, capture:
- rule ID
- plain-language statement
- source or authority
- triggering condition
- action or expected outcome
- exception or override path
- example scenario

See `references/rule-catalog-pattern.md` for a normalized row structure.

### Step 4: Detect Rule Problems

Flag:
- contradictory rules
- duplicate rules
- rules without a named source
- rules with no measurable fit or test condition
- rules embedded as implementation choices rather than business intent

### Step 5: Map Rules Downstream

For each rule, identify its effect on:
- functional requirements
- non-functional constraints
- process controls
- test scenarios
- data model or audit needs

### Step 6: Write Output

Write `projects/<ProjectName>/<phase>/<document>/business_rules_catalog.md` with the normalized rule catalog, issue log, and downstream mapping.

## Output Format

1. Rule inventory summary
2. Classified rule catalog
3. Contradictions and gaps
4. Downstream requirement and test impacts
5. Open questions and source gaps

## Common Pitfalls

- Mixing business policy with UI or implementation detail
- Omitting rule sources, making disputes impossible to resolve
- Recording rules without examples or exceptions
- Leaving calculations untestable or unit-less

## Verification Checklist

- [ ] Every rule has an ID and classification.
- [ ] Every rule has a source or is flagged as needing confirmation.
- [ ] Exceptions or overrides are documented where relevant.
- [ ] Contradictions and duplicates are identified.
- [ ] Downstream requirement and test impacts are mapped.

## References

- `references/rule-catalog-pattern.md` -- Normalized business rule structure and review prompts
