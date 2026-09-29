---
name: 07-requirements-validation
description: "Use when independently reviewing drafted requirements for correctness, completeness, consistency, feasibility, traceability, and testability before baselining; use requirements-analysis to resolve raw elicitation conflicts."
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---

# Requirements Validation Skill

<!-- local-contract-start -->
<!-- dual-compat-start -->
## Use When

- independently reviewing drafted requirements for correctness, completeness, consistency, feasibility, traceability, and testability before baselining; use requirements-analysis to resolve raw elicitation conflicts.
- Use this procedure when the required source artefacts are available and `Validation findings and release recommendation` is the next lifecycle deliverable.

## Do Not Use When

- Use `requirements-analysis` when that neighbouring route owns the decision or deliverable.
- Do not invent missing project evidence, standards clauses, thresholds, or stakeholder decisions.

## Required Inputs

| Artefact | Source or provider | Required? | Behaviour when missing |
| --- | --- | --- | --- |
| Draft requirements, source evidence, glossary, quality thresholds, and trace links | Requirements owner and independent reviewers | Yes | Stop the affected step, name the missing source, and return only a qualified gap record. |

## Workflow

1. Inspect the required inputs and log the exact sources, versions, and unresolved assumptions.
2. Apply this skill's existing domain workflow and decision rules to produce `Validation findings and release recommendation`.
3. Stop when a required source, accountable decision owner, or deterministic test oracle is absent.
4. Recover by preserving valid work, marking the blocked scope, and returning the narrowest qualified artefact plus the next evidence needed.

## Outputs

| Artefact | Consumer | Acceptance condition |
| --- | --- | --- |
| Validation findings and release recommendation | Requirements management and remediation owners | Required sections are populated, source links resolve, and every material requirement or decision has an observable review or test oracle. |

## Evidence Produced

| Evidence | Reviewer | Acceptance condition |
| --- | --- | --- |
| Source, decision, trace, and validation record for `Validation findings and release recommendation` | Requirements quality reviewer | Inputs used, decisions made, checks run, failures, and unassessed items are explicit. |

## Capability and permission boundaries

Read and search are required. This procedure is read-only by default. Editing the reviewed artefact, publishing, production mutation, destructive action, spending, or certification requires explicit authority.

## Degraded mode

Fallback: if a required file, reviewer, standard source, network check, renderer, or execution capability is unavailable, return the narrowest useful qualified result and mark the affected check `not assessed`; never convert an unassessed check into a pass.

## Decision Rules

| Choice or condition | Action | Failure or risk avoided |
| --- | --- | --- |
| A required source or test oracle is unavailable | Mark the check not assessed and withhold a pass for the affected requirement. | A false validation pass. |
| Required inputs and test oracles are complete | Continue through the existing workflow and record evidence. | A deliverable whose acceptance cannot be reproduced. |
| A mandatory source or owner is missing | Stop the affected branch and issue a qualified gap record. | Fabricated context or unauthorised decisions. |

## Quality Standards

- Preserve stable identifiers and bidirectional traceability from project evidence to `Validation findings and release recommendation` and its acceptance checks.
- Apply ISO/IEEE measures only with a named metric, method, threshold, evidence source, and responsible reviewer; run the anti-slop gate before release.

## Anti-Patterns

- Producing `Validation findings and release recommendation` from assumed context. Fix: cite the project source or mark the scope blocked.
- Accepting a material requirement without a deterministic oracle. Fix: add a measurable result, boundary, and verification method.
- Crossing into `requirements-analysis` without routing the decision. Fix: hand off the named input and preserve trace links.
- Treating an unavailable check as passed. Fix: mark it `not assessed` and state the release consequence.
- Claiming standards, statutory, or stakeholder approval without evidence. Fix: cite the source and reviewer or qualify the claim.

## References

- [Skill authoring and release standard](../../../../docs/skill-authoring-standard.md)
- [Inspection Process](references/inspection-process.md)
- [Prototype Validation](references/prototype-validation.md)
- [Review Checklist](references/review-checklist.md)
- [Review Focus](references/review-focus.md)
## Product-experience validation checks

Where the requirements affect adoption or user experience, validate more than
sentence quality. Check that the set names the first meaningful user outcome,
does not make optional setup mandatory without evidence, and includes skip,
resume, error, empty, loading, accessibility, and recovery behaviour. For
dashboards, require a named decision, metric definitions, comparison basis,
freshness/staleness behaviour, and a first-run state. For financial flows,
require explicit fees/FX, confirmation, status, reversibility, support, and
error-prevention rules where applicable. Each check needs an owner, evidence,
and deterministic oracle; otherwise mark it `not assessed` and block the
affected baseline decision.

When requirements were AI-assisted, verify the summary against source artefacts,
record decisions and unresolved inferences, and inspect the diff after scoped
changes. Plausible generated prose is not validation evidence.

Practitioner cross-checks: [Eleken onboarding](https://www.eleken.co/blog-posts/mobile-app-onboarding-best-practices), [dashboard guidance](https://www.eleken.co/blog-posts/dashboard-design-examples-that-catch-the-eye), and [AI design workflow](https://www.eleken.co/blog-posts/ai-design-workflow). Use [WCAG 2.2](https://www.w3.org/TR/WCAG22/) for accessibility authority.

## Book-informed practice route

Use [the scenario-spine and requirement-contract reference](../../after/09-traceability-engineering/references/scenario-spine-and-requirement-contract.md) to demand measurable oracles, explicit assumptions, and failure-aware validation.
<!-- dual-compat-end -->
<!-- local-contract-end -->

## Overview

This skill performs systematic validation of all requirements artifacts produced during the "during" lifecycle phase. It applies Wiegers' seven quality attributes and IEEE 830's eight quality criteria to every requirement, executes a structured Fagan-style inspection process, and flags defects with `[V&V-FAIL]` tags per the CLAUDE.md protocol. No requirement shall proceed to baselining until all validation gates pass.

## When to Use This Skill

- After requirements analysis, data modeling, and pattern specification are complete
- Before baselining the requirements set for downstream design and development
- When stakeholders require formal evidence that requirements meet quality standards
- When preparing for an external audit or regulatory review
- As a quality gate before the SRS draft is finalized

## Quick Reference

| Attribute     | Value                                                                  |
|---------------|------------------------------------------------------------------------|
| **Inputs**    | All `projects/<ProjectName>/<phase>/<document>/` artifacts generated by skills 04-06                   |
| **Output**    | `projects/<ProjectName>/<phase>/<document>/validation_report.md`                                       |
| **Tone**      | Formal, prescriptive, objective; findings stated without softening     |
| **Standards** | IEEE 1012-2016, IEEE 830-1998, IEEE 29148-2018, Wiegers Practices 13-14 |

## Input Files

| File                              | Location                                        | Required | Purpose                                       |
|-----------------------------------|-------------------------------------------------|----------|-----------------------------------------------|
| requirements_analysis_report.md   | `projects/<ProjectName>/<phase>/<document>/requirements_analysis_report.md`     | Yes      | Classified and prioritized requirements        |
| conceptual_data_model.md          | `projects/<ProjectName>/<phase>/<document>/conceptual_data_model.md`            | No       | Entity-relationship model for data validation  |
| requirements_patterns.md          | `projects/<ProjectName>/<phase>/<document>/requirements_patterns.md`            | No       | Decision tables, state models, CRUD matrices   |
| vision.md                         | `projects/<ProjectName>/_context/vision.md`                  | Yes      | Business goals for traceability validation     |
| features.md                       | `projects/<ProjectName>/_context/features.md`                | Yes      | Feature list for completeness checking         |
| business_rules.md                 | `projects/<ProjectName>/_context/business_rules.md`          | No       | Business rules for consistency checking        |

## Output Files

| File                  | Location                            | Description                                    |
|-----------------------|-------------------------------------|------------------------------------------------|
| validation_report.md  | `projects/<ProjectName>/<phase>/<document>/validation_report.md`    | Complete validation findings with defect log and remediation instructions |

## Core Instructions

Follow these steps in order. Halt and notify the user if a required input file is missing.

### Step 1: Read All Artifacts

Read every file listed in the Input Files table. Inventory all requirements, entities, patterns, and business rules discovered. Log the total artifact count and the file paths read.

### Step 2: Wiegers Quality Attribute Check

Evaluate every requirement against seven quality attributes per Wiegers Practices 13-14:

| Attribute    | Criterion                                                          | Failure Tag               |
|--------------|--------------------------------------------------------------------|---------------------------|
| Correct      | The requirement accurately reflects a stakeholder need documented in `vision.md` or `features.md` | `[V&V-FAIL:CORRECTNESS]` |
| Complete     | The requirement contains all information needed for implementation without assumptions | `[V&V-FAIL:COMPLETENESS]` |
| Feasible     | The requirement can be implemented within known technical and resource constraints | `[V&V-FAIL:FEASIBILITY]` |
| Necessary    | The requirement traces to a business goal; removing it would degrade the product | `[V&V-FAIL:NECESSITY]` |
| Prioritized  | The requirement has an assigned priority level with documented rationale | `[V&V-FAIL:PRIORITY]` |
| Unambiguous  | The requirement has exactly one interpretation; no subjective adjectives without metrics | `[V&V-FAIL:AMBIGUITY]` |
| Verifiable   | A deterministic test case with a clear pass/fail criterion can be written for the requirement | `[V&V-FAIL:VERIFIABILITY]` |

For each requirement that fails one or more attributes, record:
- The requirement identifier
- The failing attribute(s)
- A specific remediation step naming the missing or conflicting element
- The severity (Critical / Major / Minor)

### Step 3: IEEE 830 Quality Criteria Check

Evaluate the requirements set as a whole against eight quality criteria per IEEE 830 Section 4.3:

| Criterion    | Scope           | Evaluation Method                                              |
|--------------|-----------------|----------------------------------------------------------------|
| Correct      | Set-level       | Every requirement traces to a documented stakeholder need      |
| Unambiguous  | Set-level       | No requirement uses undefined terms or subjective language     |
| Complete     | Set-level       | Every feature in `features.md` has at least one requirement    |
| Consistent   | Set-level       | No two requirements contradict each other                      |
| Ranked       | Set-level       | Every requirement has a priority assignment                    |
| Verifiable   | Set-level       | Every requirement has a testable acceptance criterion          |
| Modifiable   | Set-level       | Requirements use unique IDs with no redundancy                 |
| Traceable    | Set-level       | Every requirement has a forward and backward trace link        |

Produce a Quality Criteria Summary Table with pass/fail status for each criterion and supporting evidence.

### Step 4: Structured Inspection Process

Execute a Fagan-style inspection adapted for requirements per IEEE 1012-2016:

**4.1 Preparation Phase:**
- Compile the inspection package: all output artifacts plus the validation checklist
- Identify inspection focus areas based on Steps 2-3 findings
- Calculate the preparation rate: recommended maximum of 20 requirements per hour

**4.2 Inspection Execution:**
- Apply the review checklist from `references/review-checklist.md`
- For each requirement, record one of:
  - **Pass:** Meets all quality attributes
  - **Minor Defect:** Cosmetic or documentation issue; does not block baselining
  - **Major Defect:** Functional gap or ambiguity; blocks baselining until resolved
  - **Critical Defect:** Contradicts a business goal or creates a safety/compliance risk

**4.3 Defect Classification:**

| Defect Type  | Description                                     | Resolution Deadline    |
|--------------|-------------------------------------------------|------------------------|
| Critical     | Contradicts business goal or compliance requirement | Before any downstream work |
| Major        | Missing information or ambiguous behavior        | Before baselining      |
| Minor        | Formatting, naming, or documentation issue       | Before final release   |

**4.4 Metrics Collection:**

Calculate and report:
- $DefectDensity = \frac{TotalDefects}{TotalRequirements}$
- $CriticalDefectRate = \frac{CriticalDefects}{TotalRequirements} \times 100$
- $InspectionEfficiency = \frac{DefectsFound}{InspectionHours}$

See `references/inspection-process.md` for the full Fagan inspection protocol.

### Step 5: Cross-Artifact Consistency Validation

Validate consistency across all output artifacts:

1. **Analysis-to-Data Model:** Every entity referenced in the requirements analysis SHALL appear in the conceptual data model. Flag missing entities with `[V&V-FAIL:ENTITY-MISSING]`.
2. **Analysis-to-Patterns:** Every complex requirement flagged in analysis SHALL have a corresponding pattern artifact (decision table, state model, or CRUD matrix). Flag missing patterns with `[V&V-FAIL:PATTERN-MISSING]`.
3. **Data Model-to-CRUD:** Every entity in the conceptual data model SHALL appear in at least one CRUD matrix. Flag orphan entities with `[V&V-FAIL:CRUD-MISSING]`.
4. **Terminology Consistency:** The same concept SHALL use the same term across all artifacts. Flag terminology divergence with `[V&V-FAIL:TERMINOLOGY]`.

### Step 6: Traceability Validation

Verify bidirectional traceability:

1. **Forward Trace:** Every business goal in `vision.md` SHALL map to at least one requirement. Flag orphan goals with `[V&V-FAIL:GOAL-ORPHAN]`.
2. **Backward Trace:** Every requirement SHALL map to at least one business goal. Flag untraceable requirements with `[V&V-FAIL:REQ-ORPHAN]`.
3. **Feature Coverage:** Every feature in `features.md` SHALL have at least one functional requirement. Flag uncovered features with `[V&V-FAIL:FEATURE-UNCOVERED]`.

### Step 7: Review Focus

List up to five conditions the requirements imply but do not state (for example, reversal of a mobile-money payment made while the device was offline). Each row SHALL carry an acceptance criterion and a disposition: new requirement, clarification, or accepted risk with a named owner. More than five candidates means elicitation is incomplete: stop validation and return to `02-elicitation-toolkit`. Method and worked rows: `references/review-focus.md`.

| No. | Implied condition | Why it matters | Acceptance criterion | Disposition | Owner |
|---|---|---|---|---|---|
| RF-1 | | | | | |

### Step 8: Prototype Validation Guidance (Optional)

If stakeholders have access to a prototype or mockup, provide a structured walkthrough protocol:

- Define the walkthrough scope (which features to validate)
- Prepare scenario scripts aligned with requirements
- Document stakeholder feedback against specific requirement identifiers
- Capture new or changed requirements discovered during the walkthrough

See `references/prototype-validation.md` for the walkthrough protocol and feedback capture template.

### Step 9: Generate Validation Report

Write the completed validation to `projects/<ProjectName>/<phase>/<document>/validation_report.md` using the output format below. Log summary statistics: total requirements validated, pass rate, defect count by severity, and quality criteria results.

## Output Format Specification

The generated `validation_report.md` SHALL contain the following sections:

```
# Requirements Validation Report: [Project Name]

## 1. Document Information
## 2. Validation Summary
### 2.1 Scope and Objectives
### 2.2 Artifacts Validated
### 2.3 Key Findings
## 3. Quality Attribute Results (Wiegers)
### 3.1 Per-Requirement Validation Matrix
### 3.2 Attribute Failure Summary
## 4. Quality Criteria Results (IEEE 830)
### 4.1 Criteria Summary Table
### 4.2 Evidence and Findings
## 5. Inspection Results
### 5.1 Defect Log
### 5.2 Defect Classification Summary
### 5.3 Inspection Metrics
## 6. Cross-Artifact Consistency Findings
## 7. Traceability Validation
### 7.1 Forward Trace Results
### 7.2 Backward Trace Results
### 7.3 Feature Coverage Matrix
## 8. Remediation Plan
### 8.1 Critical Defects (Immediate)
### 8.2 Major Defects (Before Baselining)
### 8.3 Minor Defects (Before Release)
## 9. Review Focus
## 10. Baselining Decision
## 11. Appendix: Standards Traceability
```

## Common Pitfalls

1. **Rubber-stamp reviews:** Marking every requirement as "Pass" without evidence defeats the purpose. Every pass SHALL cite the specific quality attribute evidence.
2. **Ignoring cross-artifact consistency:** Requirements validated in isolation may conflict with data models or pattern artifacts. Always perform cross-artifact checks.
3. **Soft language in defect reports:** "This requirement could be improved" is not actionable. State the specific defect and the required remediation.
4. **Skipping traceability validation:** Orphan requirements and uncovered features are among the most common SRS defects. Always validate bidirectional traces.
5. **Baselining with critical defects:** No requirement set SHALL be baselined while critical defects remain open.

## Verification Checklist

- [ ] All required input files were read and logged.
- [ ] Every requirement was evaluated against all seven Wiegers quality attributes.
- [ ] The requirements set was evaluated against all eight IEEE 830 quality criteria.
- [ ] All defects are tagged with `[V&V-FAIL]` and include specific remediation steps.
- [ ] Cross-artifact consistency was validated across analysis, data model, and patterns.
- [ ] Bidirectional traceability was verified (goals to requirements, requirements to goals).
- [ ] Feature coverage was validated (every feature has at least one requirement).
- [ ] Inspection metrics (defect density, critical rate, efficiency) were calculated.
- [ ] A Review Focus table of at most five implied conditions is recorded, each with an acceptance criterion and a disposition.
- [ ] Baselining decision is documented with justification.
- [ ] No marketing language or subjective findings appear in the report.

## Integration

### SDD phase-boundary companion

When reviewing an SDD-style feature workspace containing `spec.md`, `plan.md`,
and `tasks.md`, run the deterministic companion validator before accepting the
requirements set as implementation-ready:

```powershell
python scripts/validate_sdd_phase_boundaries.py --feature-dir <feature-dir> --stage spec-plan
```

The validator enforces P1 requirement coverage, implementation file/symbol
mapping, and explicit failure for missing evidence. It is a structural gate;
the requirements validation workflow remains authoritative for correctness,
completeness, feasibility, verifiability, standards traceability, and
baselining. See [SDD Phase-Boundary Contract](../../../../docs/sdd-phase-boundary-contract.md).

| Direction  | Skill                                              | Relationship                                    |
|------------|----------------------------------------------------|-------------------------------------------------|
| Upstream   | `02-requirements-engineering/fundamentals/during/04-*` | Validates analysis report                   |
| Upstream   | `02-requirements-engineering/fundamentals/during/05-*` | Validates conceptual data model             |
| Upstream   | `02-requirements-engineering/fundamentals/during/06-*` | Validates pattern artifacts                 |
| Downstream | `02-requirements-engineering/waterfall/05-*`           | Enables SRS specification after baselining  |
| Downstream | `09-governance-compliance/01-*`                        | Feeds into traceability matrix              |
| Downstream | `09-governance-compliance/02-*`                        | Feeds into audit report                     |

## Standards Compliance

| Standard          | Governs                                                    |
|-------------------|------------------------------------------------------------|
| IEEE 1012-2016    | Verification and validation processes and defect management |
| IEEE 830-1998     | Eight quality criteria for requirements specifications     |
| IEEE 29148-2018   | Requirements validation activities                         |
| Laplante Ch.6     | Requirements validation techniques                         |
| Wiegers Ch.13-14  | Quality attributes and structured reviews                  |

## Resources

- `references/review-checklist.md` -- Quality attribute checklist with pass/fail indicators
- `references/inspection-process.md` -- Fagan inspection protocol adapted for requirements
- `references/prototype-validation.md` -- Prototype walkthrough protocol and feedback capture
- `references/uncertainty-and-evidence-review.md` -- claim status, uncertainty, communication, and acceptance checks
- [Java enterprise requirements overlay](../../../references/java-enterprise-requirements-overlay.md) -- validate Java/JVM acceptance oracles and expose unavailable runtime, load, failover, recovery, and support evidence
