---
name: 03-test-report
description: Use when producing or updating evidence-backed test report for executed results, defects, coverage, deviations, residual risk, and release recommendation. Use test-plan for the neighbouring concern; this skill owns the named document contract and its acceptance evidence.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---


# Test Report Skill

<!-- dual-compat-start -->
## Use When

- Produce or update evidence-backed test report from approved project evidence.
- Resolve decisions about executed results, defects, coverage, deviations, residual risk, and release recommendation.
- Prepare a reviewable handoff for Release owner and stakeholders.

## Do Not Use When

- The task is primarily owned by test-plan; route there and use this skill only for its named output.
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
| Evidence-backed Test Report | Release owner and stakeholders | Every result links to execution evidence; failures and unassessed checks remain visible in the release recommendation. |
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
| Evidence is complete and authority is explicit | Choose the verdict from observed evidence and approved exit criteria and produce the full artefact. | Reporting an unexecuted check as passed. |
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
- Mixing the neighbouring test-plan concern into this artefact without a boundary. Fix: cross-reference its output and keep ownership explicit.
- Omitting failure, rollback, empty-state, security, tenancy, or escalation behaviour. Fix: specify the trigger, safe action, verification, and owner for each applicable case.
- Mutating a repository, environment, tenant, ledger, or external system while drafting guidance. Fix: remain read-only until the exact mutation and authority are explicit.
- Claiming compliance, certification, readiness, or release from prose alone. Fix: require source-attributed evidence and a named acceptance decision.

## Worked Example

Given an approved project source and a conflicting implementation detail, record both with provenance, stop the affected branch, and obtain the accountable owner's decision. Then update the relevant contract, define a reproducible acceptance check, and retain its observed result. The artefact is accepted only when every result links to execution evidence; failures and unassessed checks remain visible in the release recommendation.

## References

- [logic.prompt](logic.prompt) - load only when its template, logic, or detail is needed.
- [README.md](README.md) - load only when its template, logic, or detail is needed.
<!-- dual-compat-end -->
## Overview

This is the third and final skill in Phase 05 (Testing Documentation). It reads the test plan to produce a reusable test execution report template containing an executive summary, test execution log, defect log, coverage metrics, failed test analysis, and recommendations. The template includes structured placeholders for actual results to be filled during test execution. The output conforms to BS ISO/IEC/IEEE 29119-3 Sections 9-10 and references the deterministic gate checklist plus the incident/test completion templates.

## When to Use

- After 02-test-plan completes and `Test_Plan.md` exists in `projects/<ProjectName>/<phase>/<document>/` with test cases and traceability matrix.
- When the project requires a standardized report template for recording test execution outcomes.

## Quick Reference

| Attribute   | Value |
|-------------|-------|
| **Inputs**  | `projects/<ProjectName>/<phase>/<document>/Test_Plan.md` |
| **Output**  | `projects/<ProjectName>/<phase>/<document>/Test_Report_Template.md` |
| **Tone**    | Structured, metrics-driven, stakeholder-facing |
| **Standard** | BS ISO/IEC/IEEE 29119-3 Sec 9-10 |

## Input Files

| File | Location | Required | Purpose |
|------|----------|----------|---------|
| Test_Plan.md | `projects/<ProjectName>/<phase>/<document>/Test_Plan.md` | Yes | Test case inventory, traceability matrix, and schedule driving report structure |

## Output Files

| File | Location | Description |
|------|----------|-------------|
| Test_Report_Template.md | `projects/<ProjectName>/<phase>/<document>/Test_Report_Template.md` | Reusable report template with placeholders for test execution results |

## Core Instructions

Follow these seven steps in order. Halt and notify the user if the required input file is missing.

### Step 1: Read Test Plan

Read `Test_Plan.md` from `projects/<ProjectName>/<phase>/<document>/`. Log the absolute path. If the file is missing, halt execution and report the gap. Extract the total test case count, test case groupings, and traceability matrix.

### Step 2: Generate Executive Summary Template

Create an executive summary section with placeholders for: total tests executed, tests passed, tests failed, tests blocked, tests skipped, overall pass rate (%), requirement coverage percentage, and a release readiness recommendation field. Include a summary dashboard table.

### Step 3: Generate Test Execution Log

Create a test execution log table with columns: TC-ID, Test Case Name, Result (Pass/Fail/Blocked/Skipped), Execution Date, Tester, Defect Reference (if failed), and Notes. Pre-populate TC-IDs from Test_Plan.md with placeholder values for results.

### Step 4: Generate Defect Log

Create a defect log table with columns: DEF-ID (auto-incrementing), Severity (Critical/Major/Minor/Trivial), Priority (P1-P4), Status (Open/In Progress/Resolved/Verified/Closed), Summary Description, Steps to Reproduce, Linked TC-ID, Assigned To, and Resolution Date. Include placeholder rows demonstrating the expected format.

### Step 5: Generate Coverage Metrics Section

Create a coverage metrics section with: Requirement Coverage (percentage of REQ-IDs with at least one executed test case), Feature Coverage (percentage of SRS Section 3.2 features tested), Code Coverage Targets (from Test_Strategy.md if available), and a coverage gap list referencing unexecuted or failed traceability entries.

### Step 6: Generate Failed Test Analysis and Recommendations

Create a failed test analysis section with a template per failure: TC-ID, Failure Description, Root Cause Category (defect, environment, test data, requirement ambiguity), Impact Assessment, and Remediation Action. Create a recommendations section with fields for: release readiness decision (Go/No-Go/Conditional), outstanding risks, and required follow-up actions.

### Step 7: Write Template with Sign-Off

Before writing output, confirm the deterministic gate in `../references/29119-deterministic-checks.md` is satisfied and that incident-report.md plus test-completion-report.md templates are referenced for use during execution reporting. Write the completed template to `projects/<ProjectName>/<phase>/<document>/Test_Report_Template.md`. Include a sign-off section with fields for: QA Lead (name, date, signature), Project Manager (name, date, signature), and stakeholder approval fields. Log the total number of template sections and placeholder test case entries.

## Output Format

The generated `Test_Report_Template.md` shall contain these sections in order: Document Header (project name, date, version, standards), 1. Executive Summary, 2. Test Execution Log, 3. Defect Log, 4. Coverage Metrics, 5. Failed Test Analysis, 6. Recommendations, 7. Sign-Off.

## Common Pitfalls

| Pitfall | Remedy |
|---------|--------|
| Executive summary without numeric placeholders | The summary shall include placeholder fields for all quantitative metrics |
| Defect log missing severity/priority columns | Every defect entry shall classify both severity and priority independently |
| Coverage metrics without gap identification | The coverage section shall list specific unexecuted or failed traceability entries |
| Missing sign-off fields | The template shall include named approval fields for QA Lead and Project Manager |

## Reporting a runner change across machines

For each comparison give the observation window, time zone, machine label, revision in use, eligible tasks, accepted tasks and incomplete attempts. Identify repeated observations of the same commit or session on another PC. Record paired full-gate counts and queue time separately. A shorter test or fewer invocations can support a specific mechanism; a production throughput claim also needs comparable accepted work and elapsed time.

Record operator recollection of earlier usage limits as testimony. Only report incident counts or wait durations where the provider or runner events identify distinct episodes and their bounds.

## Verification Checklist

- [ ] `Test_Report_Template.md` exists in `projects/<ProjectName>/<phase>/<document>/` with all seven sections populated.
- [ ] Executive summary includes placeholders for total, passed, failed, blocked, and coverage metrics.
- [ ] Test execution log table pre-populates TC-IDs from Test_Plan.md.
- [ ] Defect log includes severity, priority, status, steps to reproduce, and linked TC-ID columns.
- [ ] Coverage metrics section references the traceability matrix and identifies gap categories.
- [ ] Failed test analysis template includes root cause categories and remediation actions.
- [ ] Sign-off section includes QA Lead and Project Manager approval fields.

## Integration

| Direction | Skill | Relationship |
|-----------|-------|-------------|
| Upstream | 02-test-plan | Consumes test case inventory and traceability matrix for report structure |
| Upstream | 01-test-strategy | Inherits defect severity/priority taxonomy and metrics definitions |
| Downstream | Phase 09 (Governance) | Feeds completed test reports as audit evidence for compliance verification |

## Standards

- **BS ISO/IEC/IEEE 29119-3** -- Current international standard for test documentation; governs test execution reports, incident logging, and completion reporting structure (Sections 9-10).

## Resources

- `logic.prompt` -- Executable prompt containing the step-by-step test report template generation logic.
- `README.md` -- Quick-start guide for this skill.
