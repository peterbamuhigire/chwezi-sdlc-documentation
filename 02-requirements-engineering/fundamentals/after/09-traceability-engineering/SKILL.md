---
name: 09-traceability-engineering
description: "Use when establishing forward and backward links among goals, requirements, design, code, tests, and evidence; use traceability-matrix for the governance roll-up artefact."
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---

# Traceability Engineering Skill Guidance

<!-- local-contract-start -->
<!-- dual-compat-start -->
## Use When

- establishing forward and backward links among goals, requirements, design, code, tests, and evidence; use traceability-matrix for the governance roll-up artefact.
- Use this procedure when the required source artefacts are available and `Trace model and gap register` is the next lifecycle deliverable.

## Do Not Use When

- Use `traceability-matrix` when that neighbouring route owns the decision or deliverable.
- Do not invent missing project evidence, standards clauses, thresholds, or stakeholder decisions.

## Required Inputs

| Artefact | Source or provider | Required? | Behaviour when missing |
| --- | --- | --- | --- |
| Stable identifiers and approved lifecycle artefacts | Phase owners and project registries | Yes | Stop the affected step, name the missing source, and return only a qualified gap record. |

## Workflow

1. Inspect the required inputs and log the exact sources, versions, and unresolved assumptions.
2. Apply this skill's existing domain workflow and decision rules to produce `Trace model and gap register`.
3. Stop when a required source, accountable decision owner, or deterministic test oracle is absent.
4. Recover by preserving valid work, marking the blocked scope, and returning the narrowest qualified artefact plus the next evidence needed.

## Outputs

| Artefact | Consumer | Acceptance condition |
| --- | --- | --- |
| Trace model and gap register | Requirements management, design, testing, and governance | Required sections are populated, source links resolve, and every material requirement or decision has an observable review or test oracle. |

## Evidence Produced

| Evidence | Reviewer | Acceptance condition |
| --- | --- | --- |
| Source, decision, trace, and validation record for `Trace model and gap register` | Requirements quality reviewer | Inputs used, decisions made, checks run, failures, and unassessed items are explicit. |

## Capability and permission boundaries

Read and search are required. Editing is allowed only when the request authorises creation or repair of the named requirements artefact. Publishing, production mutation, destructive action, spending, and certification require explicit authority.

## Degraded mode

Fallback: if a required file, reviewer, standard source, network check, renderer, or execution capability is unavailable, return the narrowest useful qualified result and mark the affected check `not assessed`; never convert an unassessed check into a pass.

## Decision Rules

| Choice or condition | Action | Failure or risk avoided |
| --- | --- | --- |
| A source or target has no stable identifier | Stop the link operation and assign or reconcile the identifier first. | False coverage and orphaned lifecycle evidence. |
| Required inputs and test oracles are complete | Continue through the existing workflow and record evidence. | A deliverable whose acceptance cannot be reproduced. |
| A mandatory source or owner is missing | Stop the affected branch and issue a qualified gap record. | Fabricated context or unauthorised decisions. |

## Quality Standards

- Preserve stable identifiers and bidirectional traceability from project evidence to `Trace model and gap register` and its acceptance checks.
- Apply ISO/IEEE measures only with a named metric, method, threshold, evidence source, and responsible reviewer; run the anti-slop gate before release.

## Anti-Patterns

- Producing `Trace model and gap register` from assumed context. Fix: cite the project source or mark the scope blocked.
- Accepting a material requirement without a deterministic oracle. Fix: add a measurable result, boundary, and verification method.
- Crossing into `traceability-matrix` without routing the decision. Fix: hand off the named input and preserve trace links.
- Treating an unavailable check as passed. Fix: mark it `not assessed` and state the release consequence.
- Claiming standards, statutory, or stakeholder approval without evidence. Fix: cite the source and reviewer or qualify the claim.

## References

- [Skill authoring and release standard](../../../../docs/skill-authoring-standard.md)
- [Trace Link Types](references/trace-link-types.md)
- [Trace Matrix Template](references/trace-matrix-template.md)
## Book-informed practice route

Use [the scenario-spine and requirement-contract reference](references/scenario-spine-and-requirement-contract.md) for scenario-to-requirement-to-test-to-evidence links.
<!-- dual-compat-end -->
<!-- local-contract-end -->

## Overview

Run this skill after requirements have been baselined and validated. It builds a four-level trace chain linking every requirement to its originating business goal, downstream design element, and verification test case. The skill detects orphan requirements, gold-plating, and coverage gaps, producing a comprehensive traceability matrix that serves both Waterfall auditing and Agile quality gates.

## When to Use This Skill

- After `08-requirements-management` has established a baseline.
- When preparing for design phase handoff to ensure all requirements are traceable.
- As a quality gate before development begins.
- During audits to demonstrate requirements coverage and accountability.
- As an Agile quality gate to verify user stories trace to business goals.

## Quick Reference

- **Inputs:** `projects/<ProjectName>/_context/vision.md`, `projects/<ProjectName>/_context/stakeholder_register.md`, all `projects/<ProjectName>/<phase>/<document>/` artifacts
- **Outputs:** `projects/<ProjectName>/<phase>/<document>/traceability_matrix.md`
- **Tone:** Analytical, systematic, gap-focused

## Input Files

| File | Source | Required? |
|------|--------|-----------|
| `vision.md` | `projects/<ProjectName>/_context/` | Yes |
| `stakeholder_register.md` | `projects/<ProjectName>/_context/` | Yes |
| All `*.md` artifacts | `projects/<ProjectName>/<phase>/<document>/` | Yes |
| `requirements_baseline.md` | `projects/<ProjectName>/<phase>/<document>/` | Recommended |

## Output Files

| File | Contents | Destination |
|------|----------|-------------|
| `traceability_matrix.md` | Four-level trace matrix with gap analysis and coverage metrics | `projects/<ProjectName>/<phase>/<document>/` |

## Core Instructions

### Step 1: Read All Inputs

Read `projects/<ProjectName>/_context/vision.md`, `projects/<ProjectName>/_context/stakeholder_register.md`, and every artifact in `projects/<ProjectName>/<phase>/<document>/`. Log each file path read. Extract:

- **Business Goals:** From `vision.md` -- assign identifiers (BG-001, BG-002, ...) if not already present.
- **Requirements:** From all output artifacts -- collect every requirement ID (REQ-xxx, FR-xxx, NFR-xxx, US-xxx).
- **Design Elements:** From any design or architecture artifacts -- assign identifiers (DE-001, DE-002, ...) if present.
- **Test Cases:** From any test artifacts -- collect test case IDs (TC-001, TC-002, ...) if present.
- **Stakeholders:** From `stakeholder_register.md` -- map each requirement to its source stakeholder.

### Step 2: Define Trace Link Types

Establish the following trace link taxonomy for all connections in the matrix:

| Link Type | Direction | Description |
|-----------|-----------|-------------|
| derives-from | Requirement -> Business Goal | Requirement originates from a business goal |
| satisfies | Design Element -> Requirement | Design element fulfills a requirement |
| implements | Code Component -> Design Element | Code realizes a design element |
| verified-by | Requirement -> Test Case | Test case validates a requirement |
| conflicts-with | Requirement <-> Requirement | Two requirements contradict each other |
| refines | Requirement -> Requirement | Detailed requirement elaborates a parent |
| replaces | Requirement -> Requirement | New requirement supersedes an old one |

All links shall be maintained bidirectionally: if REQ-001 derives-from BG-003, then BG-003 shall list REQ-001 as a derived requirement.

### Step 3: Build Four-Level Trace Chain

For every requirement, establish the complete trace chain:

```
Business Goal (BG-xxx)
  -> Requirement (REQ-xxx) [derives-from]
    -> Design Element (DE-xxx) [satisfies]
      -> Test Case (TC-xxx) [verified-by]
```

For each requirement, record:

| Field | Description |
|-------|-------------|
| Req ID | Unique requirement identifier |
| Business Goal | BG-xxx that this requirement derives from |
| Source Stakeholder | Stakeholder who originated or owns the requirement |
| Design Element | DE-xxx that satisfies this requirement (if available) |
| Test Case ID | TC-xxx that verifies this requirement (if available) |
| Trace Status | Complete, Partial, Orphan, or Untested |

### Step 4: Detect Orphan Requirements

An orphan requirement has no upward trace link to a business goal. For each orphan:

1. Tag the requirement with `[TRACE-GAP]`.
2. Record the gap type: "No business goal linkage."
3. Recommend action: link to an existing goal, create a new goal, or retire the requirement.

### Step 5: Detect Gold-Plating

Gold-plating occurs when a design element or feature exists without a corresponding requirement. For each instance:

1. Tag the element with `[TRACE-GAP]`.
2. Record the gap type: "Design element without requirement justification."
3. Recommend action: create a requirement to justify the element, or remove the element.

### Step 6: Detect Untested Requirements

An untested requirement has no downward trace link to a test case. For each instance:

1. Tag the requirement with `[TRACE-GAP]`.
2. Record the gap type: "No test case linkage."
3. Recommend action: create a test case with verifiable acceptance criteria.

### Step 7: Calculate Traceability Coverage

Compute the following coverage metrics:

$$\text{Upward Coverage} = \frac{\text{Requirements with Business Goal links}}{\text{Total Requirements}} \times 100$$

$$\text{Downward Coverage} = \frac{\text{Requirements with Test Case links}}{\text{Total Requirements}} \times 100$$

$$\text{Full Coverage} = \frac{\text{Requirements with both BG and TC links}}{\text{Total Requirements}} \times 100$$

$$\text{Design Coverage} = \frac{\text{Requirements with Design Element links}}{\text{Total Requirements}} \times 100$$

### Step 8: Detect Conflicts

Scan all requirements for contradictions. Two requirements conflict when they specify mutually exclusive behaviors for the same system element. Tag each conflict pair with `[TRACE-GAP]` and record:

- Conflicting requirement IDs.
- Nature of the conflict.
- Recommended resolution.

### Step 9: Generate Output

Write `projects/<ProjectName>/<phase>/<document>/traceability_matrix.md` following the output format below.

## Output Format

### traceability_matrix.md

```markdown
# Traceability Matrix: [Project Name]

**Generated:** [Date]
**Baseline:** BL-[PROJECT]-[VERSION]
**Standards:** IEEE 1012-2016, IEEE 29148-2018

---

## Coverage Summary

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Upward Coverage (BG links) | N% | >= 85% | [PASS/FAIL] |
| Downward Coverage (TC links) | N% | >= 85% | [PASS/FAIL] |
| Full Coverage (BG + TC) | N% | >= 70% | [PASS/FAIL] |
| Design Coverage (DE links) | N% | >= 60% | [PASS/FAIL] |
| Orphan Requirements | N | 0 | [PASS/FAIL] |
| Gold-Plated Elements | N | 0 | [PASS/FAIL] |
| Conflicts Detected | N | 0 | [PASS/FAIL] |

---

## Trace Matrix

| Req ID | Title | Business Goal | Stakeholder | Design Element | Test Case | Status |
|--------|-------|---------------|-------------|----------------|-----------|--------|
| REQ-001 | ... | BG-001 | [Name] | DE-001 | TC-001 | Complete |
| REQ-002 | ... | [TRACE-GAP] | [Name] | DE-002 | TC-002 | Orphan |

---

## Gap Analysis

### Orphan Requirements (No Business Goal)

| Req ID | Title | Recommended Action |
|--------|-------|--------------------|
| REQ-002 | ... | Link to BG-003 or retire |

### Untested Requirements (No Test Case)

| Req ID | Title | Recommended Action |
|--------|-------|--------------------|
| REQ-005 | ... | Create TC with acceptance criteria |

### Gold-Plated Elements (No Requirement)

| Element ID | Description | Recommended Action |
|------------|-------------|--------------------|
| DE-007 | ... | Create requirement or remove element |

### Requirement Conflicts

| Req A | Req B | Conflict Description | Recommended Resolution |
|-------|-------|---------------------|----------------------|
| REQ-003 | REQ-012 | ... | ... |

---

## Trace Link Summary

| Link Type | Count |
|-----------|-------|
| derives-from | N |
| satisfies | N |
| verified-by | N |
| conflicts-with | N |
| refines | N |
| replaces | N |
```

## Common Pitfalls

- **Shallow tracing:** Linking requirements only to goals but not to test cases creates a false sense of coverage. Always build the full four-level chain.
- **Missing bidirectional maintenance:** If a forward link exists (REQ -> TC), the reverse link (TC -> REQ) must also be maintained. One-way links break audit traversal.
- **Ignoring non-functional requirements:** NFRs are often excluded from trace matrices. Every NFR shall have a business goal link and a verification method.
- **Stale links:** When requirements change, trace links become outdated. Re-run this skill after every baseline update.
- **Over-counting conflicts:** Distinguish genuine contradictions from complementary requirements that address different scenarios of the same feature.

## Verification Checklist

- [ ] Every requirement has been evaluated for upward (BG) and downward (TC) trace links.
- [ ] Orphan requirements are tagged with `[TRACE-GAP]` and have recommended actions.
- [ ] Gold-plated design elements are identified and tagged.
- [ ] Coverage percentages are calculated for all four metrics.
- [ ] Conflicts are documented with resolution recommendations.
- [ ] All trace links use the defined link type taxonomy.
- [ ] Bidirectional link integrity is maintained.

## Integration

- **Upstream:** `08-requirements-management`, all specification and validation skills
- **Downstream:** `10-requirements-metrics`, `waterfall/08-semantic-auditing`
- **Complements:** `waterfall/08-semantic-auditing` (RTM section); this skill produces a standalone, enhanced trace matrix

## Standards

- **IEEE Std 1012-2016:** Software Verification and Validation -- traceability analysis.
- **IEEE Std 29148-2018:** Requirements engineering -- traceability provisions.
- **Laplante Ch.7.3:** Requirements traceability matrices and coverage analysis.
- **Wiegers Practice 18:** Requirements traceability and link management.
- **IEEE Std 610.12-1990:** Terminology definitions.

## Resources

- `references/trace-matrix-template.md`: Traceability matrix template and usage guide.
- `references/trace-link-types.md`: Trace link taxonomy and bidirectional maintenance rules.
- [Java enterprise requirements overlay](../../../references/java-enterprise-requirements-overlay.md): trace Java requirements through implementation, tests, migrations, release evidence, telemetry and runbook ownership.

---
## Traceability evidence states

Report link presence, executable test oracles, unresolved owner decisions and executed results as separate states. The repository-root `references/traceability-evidence.schema.json` schema and `scripts/validate_traceability_evidence.py` validator define a compact machine-checkable report; linked design and test IDs do not establish that an oracle is executable or that a test passed.

**Last Updated:** 2026-10-29
**Skill Version:** 1.1.0
