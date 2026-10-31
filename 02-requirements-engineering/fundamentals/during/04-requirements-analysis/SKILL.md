---
name: 04-requirements-analysis
description: "Use when classifying, reconciling, prioritising, and testing the feasibility of elicited requirements; use requirements-validation for the independent pre-baseline review."
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---

# Requirements Analysis Skill

<!-- local-contract-start -->
<!-- dual-compat-start -->
## Use When

- classifying, reconciling, prioritising, and testing the feasibility of elicited requirements; use requirements-validation for the independent pre-baseline review.
- Use this procedure when the required source artefacts are available and `Analysed requirements set and conflict log` is the next lifecycle deliverable.

## Do Not Use When

- Use `requirements-validation` when that neighbouring route owns the decision or deliverable.
- Do not invent missing project evidence, standards clauses, thresholds, or stakeholder decisions.

## Required Inputs

| Artefact | Source or provider | Required? | Behaviour when missing |
| --- | --- | --- | --- |
| Elicitation evidence, goals, stakeholder priorities, business rules, and constraints | Elicitation outputs and project context | Yes | Stop the affected step, name the missing source, and return only a qualified gap record. |

## Workflow

1. Inspect the required inputs and log the exact sources, versions, and unresolved assumptions.
2. Apply this skill's existing domain workflow and decision rules to produce `Analysed requirements set and conflict log`.
3. Stop when a required source, accountable decision owner, or deterministic test oracle is absent.
4. Recover by preserving valid work, marking the blocked scope, and returning the narrowest qualified artefact plus the next evidence needed.

## Outputs

| Artefact | Consumer | Acceptance condition |
| --- | --- | --- |
| Analysed requirements set and conflict log | Specification, architecture, and validation owners | Required sections are populated, source links resolve, and every material requirement or decision has an observable review or test oracle. |

## Evidence Produced

| Evidence | Reviewer | Acceptance condition |
| --- | --- | --- |
| Source, decision, trace, and validation record for `Analysed requirements set and conflict log` | Requirements quality reviewer | Inputs used, decisions made, checks run, failures, and unassessed items are explicit. |

## Capability and permission boundaries

Read and search are required. This procedure is read-only by default. Editing the reviewed artefact, publishing, production mutation, destructive action, spending, or certification requires explicit authority.

## Degraded mode

Fallback: if a required file, reviewer, standard source, network check, renderer, or execution capability is unavailable, return the narrowest useful qualified result and mark the affected check `not assessed`; never convert an unassessed check into a pass.

## Decision Rules

| Choice or condition | Action | Failure or risk avoided |
| --- | --- | --- |
| Two sources conflict on behaviour or priority | Record the conflict, evidence, owner, and decision deadline; do not choose silently. | Hidden contradictions entering the SRS. |
| Required inputs and test oracles are complete | Continue through the existing workflow and record evidence. | A deliverable whose acceptance cannot be reproduced. |
| A mandatory source or owner is missing | Stop the affected branch and issue a qualified gap record. | Fabricated context or unauthorised decisions. |

## Quality Standards

- Preserve stable identifiers and bidirectional traceability from project evidence to `Analysed requirements set and conflict log` and its acceptance checks.
- Apply ISO/IEEE measures only with a named metric, method, threshold, evidence source, and responsible reviewer; run the anti-slop gate before release.

## Anti-Patterns

- Producing `Analysed requirements set and conflict log` from assumed context. Fix: cite the project source or mark the scope blocked.
- Accepting a material requirement without a deterministic oracle. Fix: add a measurable result, boundary, and verification method.
- Crossing into `requirements-validation` without routing the decision. Fix: hand off the named input and preserve trace links.
- Treating an unavailable check as passed. Fix: mark it `not assessed` and state the release consequence.
- Claiming standards, statutory, or stakeholder approval without evidence. Fix: cite the source and reviewer or qualify the claim.

## References

- [Skill authoring and release standard](../../../../docs/skill-authoring-standard.md)
- [Conflict Detection](references/conflict-detection.md)
- [Feasibility Analysis](references/feasibility-analysis.md)
- [Goal Modeling](references/goal-modeling.md)
- [Requirements Prioritization](references/requirements-prioritization.md)
<!-- dual-compat-end -->
<!-- local-contract-end -->

## Overview

This skill transforms raw elicitation artifacts into a structured analysis report. It classifies requirements by type and priority, detects conflicts between competing requirements, assesses feasibility across five dimensions (TELOS), and applies a stakeholder-selected prioritization method. The output serves as the authoritative analysis baseline before specification and validation activities begin.

## When to Use This Skill

- After elicitation activities have produced `elicitation_log.md` with raw requirements
- When the requirements set has grown large enough that conflicts and redundancies are likely
- Before writing formal SRS specifications to ensure only feasible, conflict-free requirements proceed
- When stakeholders need a defensible prioritization of the requirements backlog

## Quick Reference

| Attribute     | Value                                                                  |
|---------------|------------------------------------------------------------------------|
| **Inputs**    | `projects/<ProjectName>/<phase>/<document>/elicitation_log.md`, `vision.md`, `features.md`, `business_rules.md` |
| **Output**    | `projects/<ProjectName>/<phase>/<document>/requirements_analysis_report.md`                            |
| **Tone**      | Analytical, objective, evidence-based; no subjective adjectives        |
| **Standards** | IEEE 29148-2018 Section 6.5, IEEE 830-1998, IEEE 1233-1998            |

## Input Files

| File               | Location                                  | Required | Purpose                                          |
|--------------------|-------------------------------------------|----------|--------------------------------------------------|
| elicitation_log.md | `projects/<ProjectName>/<phase>/<document>/elicitation_log.md`            | Yes      | Raw requirements gathered from stakeholders       |
| vision.md          | `projects/<ProjectName>/_context/vision.md`            | Yes      | Business goals for traceability and prioritization|
| features.md        | `projects/<ProjectName>/_context/features.md`          | Yes      | Feature descriptions for classification           |
| business_rules.md  | `projects/<ProjectName>/_context/business_rules.md`    | No       | Business rules for conflict detection             |

## Output Files

| File                           | Location                                       | Description                                    |
|--------------------------------|------------------------------------------------|------------------------------------------------|
| requirements_analysis_report.md| `projects/<ProjectName>/<phase>/<document>/requirements_analysis_report.md`    | Complete analysis with classification, conflicts, feasibility, and prioritization |

## Core Instructions

Follow these steps in order. Halt and notify the user if a required input file is missing.

### Step 1: Read and Inventory Context Files

Read `elicitation_log.md`, `vision.md`, `features.md`, and optionally `business_rules.md` from `projects/<ProjectName>/_context/`. Assign a temporary identifier (e.g., RAW-001) to each requirement that lacks one. Log the total count of raw requirements discovered.
Before classification, reconcile sources using `references/source-reconciliation-guide.md`; validate register before Phase 02.

### Step 2: Classify Requirements

Classify each requirement along two axes:

**By Type (IEEE 29148 Section 6.5.2):**

| Type           | Definition                                                       | Identifier Prefix |
|----------------|------------------------------------------------------------------|--------------------|
| Functional     | A capability the system shall provide (stimulus-response)        | FR-                |
| Non-Functional | A quality attribute or constraint the system shall satisfy       | NFR-               |
| Constraint     | A design or implementation restriction imposed externally        | CON-               |
| Interface      | A requirement on system boundaries and external interactions     | IR-                |

**By Obligation (IEEE 1233):**

| Level      | Keyword  | Meaning                                          |
|------------|----------|--------------------------------------------------|
| Mandatory  | shall    | Non-negotiable; system fails acceptance without it|
| Desirable  | should   | Expected but negotiable under constraint pressure |
| Optional   | may      | Nice-to-have; included only if resources permit   |

Produce a classification matrix table listing every requirement with its type, obligation level, and source reference.

### Step 2b: Tag Requirement Provenance

> Adapted from ECC's `product-capability` skill
> (upstream repository github.com/affaan-m/ECC),
> which frames itself as the PRD-to-SRS lane: "exposes constraints,
> invariants, interfaces, and unresolved decisions before multi-service work
> starts."

Tag every requirement a third way, independent of Type and Obligation:

| Tag | Meaning | Evidence required |
|-----|---------|--------------------|
| **Fixed policy** | A business rule, compliance obligation, contractual SLA, pricing rule, or data-retention policy that is not open for engineering judgment. | Cite the source document or stakeholder statement it came from. Never infer a fixed policy from the existing codebase or a prior project's behavior — "the repository tells you how the system behaves today, not what the business requires it to do." |
| **Architecture preference** | A choice engineering is free to make differently without violating stakeholder intent (e.g., synchronous vs. queued processing for a non-time-critical notification). | Name who owns the preference and record it as a candidate for `05-architecture-decision-records`, not as a requirement carved in stone. |
| **Still open** | The requirement's behavior, threshold, or scope is not yet decided. | Do not invent product truth to close the gap. Mark it explicitly with `[OPEN-DECISION]`, name the decision owner, and list it in the Blocking Decisions section of the downstream acceptance-criteria catalogue if it blocks safe progress. |

Add a **Provenance** column to the classification matrix (Fixed Policy /
Architecture Preference / Still Open) alongside Type and Obligation. A
requirement tagged **Still Open** may still carry a Type and Obligation
guess, but it must not be carried into `03-design-documentation` or
`02-acceptance-criteria` as if it were settled — flag it for the reader,
not just the requirements analyst.

Also separate **user-visible promises** (what the requirement commits the
product to, visible to the end user or operator) from **implementation
details** (how it will be built) in the same pass — conflating the two is
the most common cause of a requirement that reads as settled but is actually
an unreviewed architecture choice in disguise.

### Step 3: Detect Conflicts

Scan the classified requirements for four conflict types per Wiegers Practice 8:

1. **Contradiction:** Two requirements specify mutually exclusive behaviors for the same stimulus. Flag both with `[CONFLICT-CONTRADICTION]`.
2. **Redundancy:** Two requirements specify the same behavior in different words. Flag the duplicate with `[CONFLICT-REDUNDANCY]`.
3. **Subsumption:** One requirement is a strict subset of another. Flag the subsumed requirement with `[CONFLICT-SUBSUMPTION]`.
4. **Boundary Conflict:** Two requirements define overlapping numeric ranges or thresholds that cannot simultaneously be satisfied. Flag both with `[CONFLICT-BOUNDARY]`.

For each detected conflict, document:
- The conflicting requirement identifiers
- The conflict type
- A recommended resolution strategy (merge, escalate, defer, remove)
- The escalation path if stakeholder arbitration is required

See `references/conflict-detection.md` for the detection algorithm and resolution strategies.

### Step 4: Assess Feasibility (TELOS Framework)

Evaluate every mandatory requirement against five feasibility dimensions:

| Dimension   | Question                                                        | Score Range |
|-------------|-----------------------------------------------------------------|-------------|
| Technical   | Can the requirement be implemented with available technology?   | 1-5         |
| Economic    | Can the requirement be implemented within budget constraints?   | 1-5         |
| Legal       | Does the requirement comply with applicable regulations?        | 1-5         |
| Operational | Can the organization support this requirement operationally?    | 1-5         |
| Schedule    | Can the requirement be delivered within the project timeline?   | 1-5         |

Compute a composite feasibility score:

$FeasibilityScore = \frac{T + E + L + O + S}{5}$

Apply the following thresholds:
- **Score >= 4.0:** Go (proceed to specification)
- **Score 2.5-3.9:** Conditional (proceed with documented risks)
- **Score < 2.5:** No-Go (defer or remove; flag with `[FEASIBILITY-FAIL]`)

See `references/feasibility-analysis.md` for the scoring rubric and go/no-go decision criteria.

### Step 5: Prioritize Requirements

Apply the prioritization method selected by the stakeholder team. If no method has been chosen, recommend one using the decision tree in `references/requirements-prioritization.md`.

**Supported Methods:**

1. **MoSCoW (Wiegers Practice 9):** Assign each requirement to Must Have, Should Have, Could Have, or Won't Have. Validate that Must Have requirements do not exceed 60% of total effort capacity.

2. **Kano Model:** Classify requirements as Basic (expected), Performance (linear satisfaction), or Excitement (delight). Ensure all Basic requirements are included before Performance requirements.

3. **WSJF (Weighted Shortest Job First):** Calculate priority score:
   $WSJF = \frac{UserValue + TimeCriticality + RiskReduction}{JobSize}$

4. **100-Dollar Method:** Distribute 100 hypothetical dollars across requirements. Aggregate stakeholder allocations and rank by total investment.

Produce a prioritized requirements list sorted by priority score or category, with justification for each ranking decision.

### Step 6: Goal Modeling (Optional)

If business goals in `vision.md` are complex or hierarchical, decompose them using goal-oriented requirements engineering:

- Build AND/OR goal decomposition trees linking business goals to functional requirements
- Identify goal conflicts where satisfying one goal impedes another
- Map agents (actors) to goals they are responsible for achieving

See `references/goal-modeling.md` for KAOS and i* modeling guidance.

### Step 7: Generate Analysis Report

Write the completed analysis to `projects/<ProjectName>/<phase>/<document>/requirements_analysis_report.md` using the output format below. Log summary statistics: total requirements, classifications, conflicts detected, feasibility failures, and priority distribution.

## Output Format Specification

The generated `requirements_analysis_report.md` SHALL contain the following sections:

```
# Requirements Analysis Report: [Project Name]

## 1. Document Information
## 2. Analysis Summary
### 2.1 Scope and Objectives
### 2.2 Input Artifacts Analyzed
### 2.3 Key Findings
## 3. Requirements Classification Matrix
### 3.1 By Type (Functional / Non-Functional / Constraint / Interface)
### 3.2 By Obligation (Mandatory / Desirable / Optional)
### 3.2b By Provenance (Fixed Policy / Architecture Preference / Still Open)
### 3.3 Classification Summary Statistics
## 4. Conflict Detection Report
### 4.1 Contradictions
### 4.2 Redundancies
### 4.3 Subsumptions
### 4.4 Boundary Conflicts
### 4.5 Resolution Recommendations
## 5. Feasibility Assessment
### 5.1 TELOS Scoring Matrix
### 5.2 Go / Conditional / No-Go Summary
### 5.3 Risk Register for Conditional Requirements
## 6. Requirements Prioritization
### 6.1 Method Selected and Rationale
### 6.2 Prioritized Requirements List
### 6.3 Priority Distribution Analysis
## 7. Goal Model (if applicable)
## 8. Recommendations and Next Steps
## 9. Appendix: Standards Traceability
```

## Common Pitfalls

1. **Classifying implementation details as requirements:** A requirement describes *what* the system shall do, not *how* it shall be built. Filter out design decisions during classification.
2. **Ignoring non-functional conflicts:** Two NFRs can conflict (e.g., "response time < 100ms" vs. "encrypt all data at rest with AES-256"). Analyze NFR interactions explicitly.
3. **Feasibility scores without evidence:** Every score SHALL include a one-sentence justification. A number without rationale is an opinion.
4. **MoSCoW inflation:** Stakeholders tend to classify everything as "Must Have." Enforce the 60% capacity cap and challenge classifications with evidence.
5. **Skipping redundancy detection:** Redundant requirements inflate effort estimates and create maintenance burden in the SRS.

## Verification Checklist

- [ ] All required input files were read and logged.
- [ ] Every raw requirement has a unique identifier and classification.
- [ ] Conflict detection covered all four conflict types.
- [ ] Every mandatory requirement has a TELOS feasibility score with justification.
- [ ] No-Go requirements are flagged with `[FEASIBILITY-FAIL]` and excluded from prioritization.
- [ ] Prioritization method is documented with rationale for selection.
- [ ] Must Have requirements do not exceed 60% of capacity (if MoSCoW is used).
- [ ] No subjective adjectives appear without a defined metric.
- [ ] Standards traceability appendix maps sections to IEEE 29148 and IEEE 1233 clauses.

## Integration

| Direction  | Skill                                              | Relationship                                   |
|------------|----------------------------------------------------|-------------------------------------------------|
| Upstream   | `02-requirements-engineering/fundamentals/during/03-*` | Consumes elicitation artifacts              |
| Downstream | `02-requirements-engineering/fundamentals/during/05-*` | Feeds classified requirements to data modeling |
| Downstream | `02-requirements-engineering/fundamentals/during/06-*` | Feeds prioritized requirements to patterns     |
| Downstream | `02-requirements-engineering/waterfall/05-*`           | Feeds into SRS feature decomposition           |

## Standards Compliance

| Standard          | Governs                                                    |
|-------------------|------------------------------------------------------------|
| IEEE 29148-2018   | Requirements analysis activities and classification scheme |
| IEEE 830-1998     | Quality attributes for well-formed requirements            |
| IEEE 1233-1998    | Obligation levels and requirement well-formedness          |
| Laplante Ch.5     | Analysis techniques and feasibility assessment             |
| Wiegers Ch.7-9    | Classification, conflict detection, and prioritization     |

## Resources

- `references/conflict-detection.md` -- Conflict types, detection algorithm, resolution strategies
- `references/feasibility-analysis.md` -- TELOS framework with scoring rubric
- `references/requirements-prioritization.md` -- Four prioritization methods compared
- `references/goal-modeling.md` -- KAOS and i* goal-oriented requirements engineering
- [Java enterprise requirements overlay](../../../references/java-enterprise-requirements-overlay.md) -- analyse Java/JVM constraints as supported lifecycle, correctness, resource, failure, and migration obligations
