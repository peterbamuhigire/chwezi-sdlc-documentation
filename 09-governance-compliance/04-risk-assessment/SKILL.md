---
name: 04-risk-assessment
description: Use when identifying, analysing, treating, and accepting project or system risks with evidence-backed likelihood and impact. Use change-impact-analysis for a proposed change and audit-report for retrospective control findings.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Risk Assessment Skill

<!-- dual-compat-start -->

## Use When

- Use when identifying, analysing, treating, and accepting project or system risks with evidence-backed likelihood and impact. Use change-impact-analysis for a proposed change and audit-report for retrospective control findings.

## Do Not Use When

- Do not use when a more specific upstream or downstream skill owns the task, or when the required project context has not been prepared.
- Do not use this skill to fabricate missing project facts, legal conclusions, test results, approvals, or certification claims.

## Required Inputs

| Artefact | Source or provider | Required? | Missing-input behaviour |
|---|---|---:|---|
| Defined system or change scope; asset and process inventory; threat, dependency, and incident evidence; likelihood/impact scales; risk appetite and owners | System owner, risk owner, security, privacy, operations, and business stakeholders | Yes | Stop dependent work; name the missing item, owner, and decision impact. A review check remains `not assessed`. |
| Scope, audience, baseline/version, and accountable decision owner | Requester or project context | Yes | Ask for or record the gap; do not infer authority or scope. |

## Capability and permission boundaries

Default to read-only. Read and search access to the supplied artefacts are required. Execute only non-mutating validation when authorised; editing remediation, publishing, signature, certification, production mutation, destructive action, spending, and risk acceptance require explicit authority.

## Degraded Mode

When files, tools, network, rendering, fonts, execution, or evidence are unavailable, return the narrowest useful qualified draft or finding set. Name every unavailable check and its consequence; an unassessed check is never a pass. Preserve evidence already gathered and provide the exact next verification step.

## Decision Rules

| Condition | Action | Failure or risk avoided |
|---|---|---|
| Required evidence is missing or inaccessible | Mark the check not assessed, state impact, and stop any pass decision | False assurance from an incomplete review |
| Evidence supports the stated criterion | Record the finding and traceable rationale without mutating sources | Unrepeatable review conclusions |

## Workflow

1. Confirm the requested artefact, audience, scope, decision owner, and applicable baseline or version. Work read-only by default; source mutation, publication, signature, certification, production change, or risk acceptance requires explicit authority.
2. Inspect every required input and record missing, stale, conflicting, or inaccessible evidence. Stop claims that depend on an unresolved required input.
3. Apply the Decision Rules, then execute the existing Core Instructions below in order; preserve project terminology and trace each material statement to its source.
4. Test the draft against the output acceptance conditions and domain quality standards. If a check cannot run, mark it `not assessed` and never convert it into a pass.
5. On failure, recover by preserving completed evidence, identifying the narrowest corrective action and owner, and rerunning only the affected checks before handoff.
6. Produce the named artefact and evidence record; publish, sign, certify, mutate production, or accept risk only under explicit authority.

## Outputs

| Artefact | Consumer | Observable acceptance condition |
|---|---|---|
| Risk Assessment | Accountable reviewer, control owner, auditor, or release authority | Each risk has a cause-event-impact statement, scored rationale, treatment, residual risk, accountable owner, due date, and authorised acceptance where needed. |
| Gap and decision record | Accountable owner and downstream reviewer | Every gap has status, impact, owner, next action, and no unsupported pass or approval. |

## Evidence Produced

| Evidence | Contents | Acceptance condition |
|---|---|---|
| Risk Assessment evidence record | Source identifiers, scope/version, decisions, checks, exceptions, and approval state | A reviewer can reproduce each material conclusion from named sources. |
| Validation record | Check, result (`pass`, `fail`, or `not assessed`), evidence location, date, and actor | No required check is omitted or silently treated as passed. |

## Quality Standards

- Keep outputs grounded in source context, traceable to stated standards, and specific enough to review or verify.
- Use deterministic acceptance conditions and preserve traceability from source to decision and output.
- Separate facts, inferences, assumptions, and approvals; never present one as another.
- Apply `28-anti-ai-slop` during authoring and `29-ai-slop-audit` at major checkpoints and release.

## Anti-Patterns

- **Producing Risk Assessment from assumptions instead of named project sources.** Fix: Cite the source or mark the item unverified.
- **Treating a missing or inaccessible check as passed.** Fix: Mark it `not assessed`, state impact, and block dependent claims.
- **Using vague gates such as `adequate`, `secure`, or `user-friendly`.** Fix: Replace each with an observable criterion, threshold, and evidence source.
- **Copying a generic template without product, control, role, version, or jurisdiction detail.** Fix: Ground every section in the supplied context and remove unused boilerplate.
- **Publishing, signing, certifying, changing production, or accepting risk without authority.** Fix: Prepare a draft and route the decision to the accountable owner.
- **Listing evidence without provenance or an acceptance result.** Fix: Record source, period, integrity check, mapping, and pass/fail/not-assessed status.

## Worked Example

Example: if required evidence is missing or inaccessible, mark the check not assessed, state impact, and stop any pass decision. Record the evidence and result in the validation record; this avoids false assurance from an incomplete review.

## References

- [Generation logic](logic.prompt): load when creating the complete artefact.
- [Skill notes](README.md): consult for local examples and invocation context.
- [Repository operating rules](../../AGENTS.md): apply the engine's routing, evidence, and release gates.

<!-- dual-compat-end -->

## Overview

This skill generates a systematic risk assessment that identifies, analyzes, and evaluates risks across four categories: technical, operational, compliance, and project. Each risk is scored using a probability-impact matrix, assigned a mitigation strategy, and tracked in a formal risk register. The assessment follows the ISO 31000 risk management framework and integrates IEEE 1012 verification concerns to ensure risks threatening V&V integrity are captured.

## When to Use This Skill

- When initiating a new project phase and risks need formal identification
- When the audit report has revealed findings that require risk quantification
- When stakeholders require a formal risk register for governance oversight
- When preparing for external reviews or regulatory submissions
- When significant architectural or scope changes introduce new risk vectors
- When compliance gaps identified in 03-compliance-documentation need risk scoring

## Quick Reference

| Attribute | Value |
|-----------|-------|
| **Input** | vision.md, quality_standards.md, SRS_Draft.md, HLD.md |
| **Output** | Risk_Assessment.md |
| **Standard** | ISO 31000, IEEE 1012 |
| **Estimated Time** | 20-35 minutes |

## Input Files

| File | Purpose | Required? |
|------|---------|-----------|
| `projects/<ProjectName>/_context/vision.md` | Project scope, objectives, and constraints for risk context establishment | Yes |
| `projects/<ProjectName>/_context/quality_standards.md` | Quality thresholds and acceptance criteria for risk tolerance definition | No |
| `projects/<ProjectName>/<phase>/<document>/SRS_Draft.md` | Requirements for technical risk identification and dependency analysis | No |
| `projects/<ProjectName>/<phase>/<document>/HLD.md` | Architecture decisions for technical and operational risk identification | No |
| `projects/<ProjectName>/<phase>/<document>/Audit_Report.md` | Audit findings that may indicate risk areas requiring formal assessment | No |
| `projects/<ProjectName>/<phase>/<document>/Compliance_Docs.md` | Compliance gaps that translate directly into compliance risks | No |

## Output Files

| File | Description |
|------|-------------|
| `projects/<ProjectName>/<phase>/<document>/Risk_Assessment.md` | Complete risk assessment with register, scoring matrix, and mitigation plans |

## Core Instructions

1. The skill SHALL read `projects/<ProjectName>/_context/vision.md` to establish the risk context including project objectives, stakeholders, constraints, and risk appetite. If the file is missing, halt execution and report the error.

2. The skill SHALL read all available optional inputs to build a comprehensive risk inventory. Log each file read.

3. The skill SHALL define the Risk Assessment Methodology based on ISO 31000, including:
   - Risk identification techniques used
   - Probability scale (1-5: Rare, Unlikely, Possible, Likely, Almost Certain)
   - Impact scale (1-5: Negligible, Minor, Moderate, Major, Catastrophic)
   - Risk score calculation: $RiskScore = Probability \times Impact$
   - Risk tolerance thresholds (Low: 1-4, Medium: 5-9, High: 10-15, Critical: 16-25)

4. The skill SHALL identify risks across four categories:
   - **Technical:** Technology failures, integration issues, performance bottlenecks, security vulnerabilities
   - **Operational:** Process failures, resource constraints, skill gaps, vendor dependencies
   - **Compliance:** Regulatory violations, data protection failures, audit non-conformities
   - **Project:** Schedule delays, scope creep, budget overruns, stakeholder misalignment

5. The skill SHALL analyze each risk using the 5x5 probability-impact matrix and assign a composite risk score.

   - For Ugandan government, local-government, public-entity, NGO, or donor-funded engagements, the skill SHALL also evaluate the sector risk-register additions in `09-governance-compliance/05-formal-review-gates/references/uganda-public-sector-and-ngo-delivery-constraints.md` (budget-release/warrant delays, procurement-process delays, PPDA suspension/administrative-review exposure, donor-audit findings and ineligible-cost recovery, political/electoral-cycle disruption, exchange-rate volatility on USD/EUR donor budgets, and procurement/finance staff turnover), scoring and assigning owners per this skill's method. The finance engine (`chwezi-accounting-doctrine`) is the authority for the substance, and no statutory threshold is fixed as current in any mitigation.

6. The skill SHALL construct a Risk Register Table with columns: Risk ID, Category, Description, Probability (1-5), Impact (1-5), Risk Score, Mitigation Strategy, Owner, Status.

7. The skill SHALL assign a Risk Response Strategy to each identified risk:
   - **Avoid:** Eliminate the threat by removing the cause
   - **Mitigate:** Reduce probability or impact through controls
   - **Transfer:** Shift risk to a third party (insurance, outsourcing)
   - **Accept:** Acknowledge the risk with documented rationale

8. The skill SHALL assess Residual Risk after mitigation strategies are applied, recalculating scores to confirm acceptable risk levels.

9. The skill SHALL generate a Risk Monitoring Plan specifying review frequency, trigger conditions for re-assessment, and escalation procedures.

10. The skill SHALL cross-reference identified risks with audit findings (if available) to ensure all V&V anomalies are captured in the risk register.

## Output Format Specification

The generated `Risk_Assessment.md` SHALL contain the following sections:

```
# Risk Assessment
## 1. Document Information
## 2. Risk Assessment Methodology
### 2.1 ISO 31000 Framework
### 2.2 Probability Scale
### 2.3 Impact Scale
### 2.4 Risk Scoring Matrix
### 2.5 Risk Tolerance Thresholds
## 3. Risk Identification
### 3.1 Technical Risks
### 3.2 Operational Risks
### 3.3 Compliance Risks
### 3.4 Project Risks
## 4. Risk Analysis Matrix
## 5. Risk Register
## 6. Risk Response Strategies
## 7. Residual Risk Assessment
## 8. Risk Monitoring Plan
## 9. Risk Summary & Recommendations
## 10. Revision History
```

## Common Pitfalls

- Using vague risk descriptions ("something might go wrong") instead of specific, measurable risk statements
- Applying uniform probability/impact scores without evidence-based differentiation
- Omitting residual risk assessment, leaving stakeholders unaware of post-mitigation exposure
- Failing to assign risk owners, making mitigation strategies unenforceable
- Ignoring compliance risks when the project operates in a regulated domain
- Treating risk assessment as a one-time activity instead of establishing a monitoring cadence

## Verification Checklist

1. All four risk categories (technical, operational, compliance, project) have been assessed.
2. Every risk has a unique identifier and specific, measurable description.
3. Probability and impact scores use the defined 1-5 scales consistently.
4. Risk scores are correctly calculated as $Probability \times Impact$.
5. Every risk has an assigned response strategy (Avoid/Mitigate/Transfer/Accept).
6. Residual risk scores are calculated for all mitigated risks.
7. The risk register includes an owner and status for every entry.
8. The monitoring plan specifies review cadence and escalation triggers.

## Integration

- **Upstream:** Consumes project context, audit findings from 02-audit-report, and compliance gaps from 03-compliance-documentation.
- **Downstream:** Terminal skill -- outputs feed project governance dashboards, steering committee reviews, and external risk disclosures.

## Standards Compliance

| Standard | Governs |
|----------|---------|
| ISO 31000:2018 | Risk management framework, principles, and process |
| IEEE 1012-2016 | V&V risk identification and anomaly-driven risk assessment |

## Resources

- ISO 31000:2018: Risk Management -- Guidelines
- IEEE 1012-2016: Standard for System, Software, and Hardware Verification and Validation
- CLAUDE.md: Project-level V&V and quality constraints
