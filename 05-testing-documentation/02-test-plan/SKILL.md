---
name: 02-test-plan
description: Use when producing or updating a detailed test plan with cases, data, environments, schedule, ownership, traceability, and exit evidence. Use test-strategy for programme-level test policy; this skill owns executable test planning.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---


# Test Plan Skill

<!-- dual-compat-start -->
## Use When

- Produce or update a detailed test plan from an approved SRS, test strategy, and implementation scope.
- Resolve test-case, test-data, environment, schedule, ownership, traceability, and exit-evidence decisions.
- Prepare an executable handoff for QA engineers, developers, and the release owner.

## Do Not Use When

- The task sets programme-level test policy, levels, or risk posture; use `test-strategy` and consume it here.
- Required project evidence or decision authority is unavailable and the requester expects a pass, release, certification, or production change.

## Required Inputs

| Artefact | Source/provider | Required? | Behaviour when absent |
|---|---|---|---|
| Project _context/, approved requirements, and relevant architecture | Project owner and upstream phase skills | Required | Stop at a gap register; do not invent scope, thresholds, integrations, or owners. |
| Existing artefact, implementation, configuration, and evidence named below | Repository, delivery team, or service owner | Required when updating or assessing | Mark inaccessible items `not assessed`; do not treat them as passed. |
| Target audience, environment, risk tolerance, and authority | Requester and accountable owner | Required | Produce a read-only outline with explicit assumptions; do not mutate project or production state. |
## Outputs

| Artefact | Consumer | Observable acceptance condition |
|---|---|---|
| Detailed test plan | QA engineers, developers, and release owner | Every in-scope requirement and material risk maps to a test case, data need, environment, owner, expected result, and retained evidence. |
| Decision and gap register | Reviewer and downstream phase owner | Every assumption, rejected option, unresolved dependency, waiver, and owner is explicit. |
| Validation evidence | Release or governance reviewer | Checks identify command or method, date, result, evidence location, and all unassessed items. |

## Evidence Produced

| Evidence | Minimum content | Acceptance |
|---|---|---|
| Traceability record | Source artefact, decision, output section, owner | No mandatory decision is source-free. |
| Quality-gate result | Check, expected result, observed result, evidence path | Failures and unavailable checks cannot appear as passes. |
| Review record | Reviewer, date, disposition, open actions | The consumer can reproduce the acceptance decision. |

## Capability and Permission Boundaries

- Minimum capabilities: read and search the authorised project sources. Execution is optional and limited to non-destructive validation.
- Assessment and planning default to read-only. Create or edit the named project document only when the request explicitly authorises it. Production mutation, publishing, destructive action, spending, external communication, or certification claims require separate explicit authority.
- Treat secrets, tenant data, incident evidence, and financial records as least-privilege inputs; expose only the minimum evidence needed for review.

## Degraded Mode

If files, execution, network, rendering, environment access, fonts, or current evidence are unavailable, return the narrowest useful draft plus a gap register. Label affected checks `not assessed`, retain the intended acceptance oracle, and state who must supply or verify the missing evidence. Never convert an unavailable check into a pass.

## Decision Rules

| Choice | Action | Failure or risk avoided |
|---|---|---|
| Evidence is complete and authority is explicit | Derive cases and priorities from requirement criticality and product risk, then produce the plan. | Untraceable tests or effort spent on low-risk paths while critical paths remain uncovered. |
| A required source or approval is missing | Stop the affected branch; record the gap, owner, and unblock condition. | Fabricated requirements or unauthorised action. |
| Evidence conflicts across sources | Preserve both claims, identify the controlling owner, and request a recorded decision. | Silent selection of a convenient but wrong source. |
| A check cannot run in the available environment | Keep its oracle and mark it `not assessed`; require later execution evidence. | False assurance from capability limits. |

## Workflow

1. Confirm the named deliverable, consumer, scope, environment, authority, and neighbouring-skill boundary.
2. Inventory required sources and validate provenance, freshness, internal consistency, and missing inputs. Stop the affected branch on a mandatory gap.
3. Extract traceable requirements, invariants, risks, and measurable acceptance criteria; record conflicts before choosing a design or procedure.
4. Apply the decision rules and the domain workflow below. For a failed branch, preserve evidence, choose the documented recovery path, or escalate to the named owner.
5. Draft the artefact, decision register, and evidence record together. Do not defer failure handling, rollback, security, tenancy, accessibility, or operational ownership.
6. Run available checks, review every result, repair failures, and hand off only when acceptance is observable. If recovery fails or authority is exceeded, stop and escalate without mutation.

## Quality Standards

- Ground every section in a named project source, decision, measured result, or accountable owner.
- Give each requirement or procedure a deterministic oracle that another reviewer can reproduce.
- Keep assumptions, exclusions, degraded checks, residual risks, and waivers visible at handoff.
- Preserve the domain invariants and more specific controls in the existing workflow below; this contract does not replace them.
- Run the repository anti-AI-slop gate: remove filler, verify named standards and dependencies, and retain purposeful domain detail.

## Anti-Patterns

- Copying a generic template without mapping it to project sources. Fix: attach each section to an approved requirement, configuration, risk, or owner.
- Choosing a threshold because it is common practice. Fix: derive it from a requirement, measured baseline, risk decision, or current verified source.
- Reporting an inaccessible or unexecuted check as passed. Fix: mark it `not assessed`, preserve the oracle, and name the verifier.
- Rewriting the `test-strategy` inside the plan. Fix: reference its policy and use this artefact for executable cases, resources, sequence, and evidence.
- Omitting failure, rollback, empty-state, security, tenancy, or escalation behaviour. Fix: specify the trigger, safe action, verification, and owner for each applicable case.
- Mutating a repository, environment, tenant, ledger, or external system while drafting guidance. Fix: remain read-only until the exact mutation and authority are explicit.
- Claiming compliance, certification, readiness, or release from prose alone. Fix: require source-attributed evidence and a named acceptance decision.

## Worked Example

Given `FR-PAY-014` and a payment retry design, map successful, declined, timeout, duplicate-callback, and reconciliation paths to named cases. Record required fixtures and expected ledger or status outcomes. Stop if the retry authority or idempotency contract conflicts; resume after the accountable owner records the controlling decision.

## References

- [logic.prompt](logic.prompt) - load only when its template, logic, or detail is needed.
- [README.md](README.md) - load only when its template, logic, or detail is needed.
- [references/pairwise-combinatorial-test-design.md](references/pairwise-combinatorial-test-design.md) - load when three or more interacting parameters call for pairwise test design.
<!-- dual-compat-end -->
## Overview

This is the second skill in Phase 05 (Testing Documentation). It transforms the SRS functional and non-functional requirements into a detailed test plan containing test cases, test data definitions, schedule, resource allocation, and a requirement-to-test traceability matrix. Every "shall" statement in SRS Section 3.2 becomes a test case. The output conforms to BS ISO/IEC/IEEE 29119-3 Sections 7-8 and references the deterministic checklist for artifact completeness.

## When to Use

- After 01-test-strategy completes and `Test_Strategy.md` exists in `projects/<ProjectName>/<phase>/<document>/` with test levels, types, and criteria.
- When `SRS_Draft.md` exists in `projects/<ProjectName>/<phase>/<document>/` with functional requirements containing "shall" statements.
- Optionally, when `acceptance_criteria.md` exists in `projects/<ProjectName>/<phase>/<document>/` for agile projects requiring acceptance-test mapping.

## Quick Reference

| Attribute   | Value |
|-------------|-------|
| **Inputs**  | `projects/<ProjectName>/<phase>/<document>/SRS_Draft.md`, `projects/<ProjectName>/<phase>/<document>/Test_Strategy.md`, `projects/<ProjectName>/<phase>/<document>/acceptance_criteria.md` (optional) |
| **Output**  | `projects/<ProjectName>/<phase>/<document>/Test_Plan.md` |
| **Tone**    | Detailed, case-driven, QA-facing |
| **Standard** | BS ISO/IEC/IEEE 29119-3 Sec 7-8 |

## Input Files

| File | Location | Required | Purpose |
|------|----------|----------|---------|
| SRS_Draft.md | `projects/<ProjectName>/<phase>/<document>/SRS_Draft.md` | Yes | Functional (Section 3.2) and non-functional (Sections 3.3, 3.5) requirements as test case sources |
| Test_Strategy.md | `projects/<ProjectName>/<phase>/<document>/Test_Strategy.md` | Yes | Test levels, types, tools, and criteria governing test case structure |
| acceptance_criteria.md | `projects/<ProjectName>/<phase>/<document>/acceptance_criteria.md` | No | Agile acceptance criteria for mapping to UAT test cases |

## Output Files

| File | Location | Description |
|------|----------|-------------|
| Test_Plan.md | `projects/<ProjectName>/<phase>/<document>/Test_Plan.md` | Complete test plan with test cases, traceability matrix, schedule, and resources |

## Core Instructions

Follow these nine steps in order. Halt and notify the user if a required input file is missing.

### Step 1: Read Context Files

Read `SRS_Draft.md` and `Test_Strategy.md` from `projects/<ProjectName>/<phase>/<document>/`. Optionally read `acceptance_criteria.md` from `projects/<ProjectName>/<phase>/<document>/` if it exists. Log the absolute path of each file read. If any required file is missing, halt execution and report the gap.

### Step 2: Extract Testable Requirements

Parse SRS Section 3.2 and extract every "shall" statement as a testable requirement. Assign each requirement a unique identifier (e.g., REQ-FUNC-001). Log the total count of extracted requirements.

### Step 3: Map Acceptance Criteria

If `acceptance_criteria.md` exists, map each acceptance criterion to its corresponding SRS requirement and note which test cases shall validate it at the UAT level. If the file does not exist, skip this step and note that UAT cases derive from SRS requirements directly.

### Step 4: Define Test Design Specification & Test Case Format

Document the selected test design techniques (equivalence partitioning, boundary values, state machine testing, decision tables, use case testing) and cite the applicable 29119-3 clause (§7.3.3). Each technique shall reference the requirements it exercises. Where three or more parameters interact (configuration, permission, device, locale or currency matrices), add pairwise combinatorial design with a coverage statement per [references/pairwise-combinatorial-test-design.md](references/pairwise-combinatorial-test-design.md).

Establish the test case format using the nine normative 29119-3 fields: TC-ID, Objective/Purpose, Priority, Traceability to requirement ID, Preconditions, Test Input, Expected Result (with deterministic pass/fail), Actual Result (filled at execution), and Test Result (Pass/Incident). Include Steps (numbered actions) beneath the structured fields.

### Step 5: Generate Functional Test Cases

For each functional requirement extracted in Step 2, generate one or more test cases. Each test case shall define preconditions, sequential steps, and a deterministic expected result. Group test cases by SRS feature (Section 3.2.x subsections).

### Step 6: Generate Non-Functional Test Cases

Generate test cases for non-functional requirements: Performance tests from SRS Section 3.3 (response time, throughput, capacity), Security tests from SRS Section 3.5.3 (authentication, authorization, data protection). Each NFR test case shall include measurable acceptance thresholds.

### Step 7: Define Test Data Requirements

For each test case group, define the test data required: data entities, volume, generation method (manual, scripted, anonymized production data), and precondition data state. Identify shared test data dependencies across test case groups.

### Step 8: Define Schedule and Resource Allocation

Define the test execution schedule: phases aligned with Test_Strategy.md test levels, estimated duration per phase, resource assignments (roles, not named individuals), and dependencies between phases. Identify parallel execution opportunities.

### Step 9: Generate Traceability Matrix and Write Output

Generate a requirement-to-test traceability matrix mapping every REQ-ID to its TC-IDs, confirming full coverage. Flag any requirements without test cases as coverage gaps. Before writing output, verify the deterministic gate in `../references/29119-deterministic-checks.md` has been satisfied (mandatory artifact tree, clause annotations, entry/exit criteria). Write the completed document to `projects/<ProjectName>/<phase>/<document>/Test_Plan.md`. Log the total count of test cases, coverage percentage, and any gaps.

## Output Format

The generated `Test_Plan.md` shall contain these sections in order: Document Header (project name, date, version, standards), 1. Test Scope, 2. Test Case Summary Table, 3. Detailed Test Cases (grouped by feature), 4. Test Data, 5. Schedule, 6. Resources, 7. Traceability Matrix, Appendix A: Coverage Gap Report.

## Final Step: Write `manifest.md`

After generating all section files, create (or overwrite) `manifest.md` in this document's directory listing the section files in the correct assembly order:

```markdown
# Document Manifest — Test Plan
# Generated by test-plan. Edit to reorder or exclude sections before building.
01-test-scope.md
02-test-cases.md
03-test-data.md
04-schedule.md
05-resources.md
06-traceability.md
07-coverage-gaps.md
```

This ensures `scripts/build-doc.sh` assembles sections in the intended order rather than alphabetical fallback.

## Common Pitfalls

| Pitfall | Remedy |
|---------|--------|
| Test cases without preconditions | Every test case shall state the required system state before execution |
| Expected results without pass/fail criteria | Every expected result shall define a deterministic observable outcome |
| NFR test cases without measurable thresholds | Performance and security tests shall include numeric acceptance criteria |
| Missing traceability for edge-case requirements | Every "shall" statement in SRS Section 3.2 shall have at least one test case |

## Verification Checklist

- [ ] `Test_Plan.md` exists in `projects/<ProjectName>/<phase>/<document>/` with all seven sections populated.
- [ ] Every "shall" statement in SRS Section 3.2 has at least one corresponding test case.
- [ ] Test cases include preconditions, sequential steps, and deterministic expected results.
- [ ] NFR test cases include measurable acceptance thresholds from SRS Sections 3.3 and 3.5.
- [ ] Test data requirements are defined for each test case group.
- [ ] Schedule aligns with test levels from Test_Strategy.md.
- [ ] Traceability matrix achieves full requirement coverage; gaps are flagged in the appendix.

## Integration

| Direction | Skill | Relationship |
|-----------|-------|-------------|
| Upstream | 01-test-strategy | Consumes test levels, types, tools, and criteria framework |
| Upstream | Phase 02 (Requirements Engineering) | Consumes `SRS_Draft.md` for requirement extraction |
| Downstream | 03-test-report | Feeds test case inventory and traceability matrix for report template |
| Downstream | Phase 09 (Governance) | Feeds test plan as audit evidence for compliance verification |

## Standards

- **BS ISO/IEC/IEEE 29119-3** -- Current international standard for test documentation; governs project-level test plans, traceability, and required artifact set (Sections 7-8).

## Resources

- `logic.prompt` -- Executable prompt containing the step-by-step test plan generation logic.
- `README.md` -- Quick-start guide for this skill.

## Worked example

See [`examples/representative/`](examples/representative/).
