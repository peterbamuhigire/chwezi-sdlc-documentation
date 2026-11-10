---
name: 20-hr-module-srs
description: "Use when specifying the HR module of a multi-tenant system: positions, employee master, contract classes, leave and payroll inputs, workflows, access, audit and personal data. Use the finance doctrine for payroll postings and statutory facts."
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---

# HR Module SRS

<!-- local-contract-start -->
<!-- dual-compat-start -->
## Use When

- Specifying the requirements of an HR module or HR product: organisation and position management, employee master, contract classes, leave, payroll inputs, recruitment to exit, appraisal, disciplinary records, personal-data controls, audit and HR reporting.
- Writing acceptance criteria for an HR go-live or a vendor module assessment.

## Do Not Use When

- The task is payroll journals and statutory postings; use `18-embedded-accounting-engine-srs` and the finance doctrine.
- The task is HR policy or manual text; use the writing engine's `human-resources-documentation`.
- The task is the design or build of the module; use the development engines' `hr-module-design` or `hr-system-implementation`.
- Do not invent missing policy values, statutory rates, section numbers or stakeholder decisions.

## Required Inputs

| Artefact | Source or provider | Required? | Behaviour when missing |
| --- | --- | --- | --- |
| Organisation chart, positions, headcount plan | Client owner | Yes | Specify with draft positions; mark headcount `NOT_ASSESSED`. |
| Contract classes and the treatment each carries | Client HR owner | Yes | Use employee, part-time or fixed-term, consultant; treatment stays an unset parameter. |
| Statutory parameter source register (instrument, section, value, date, status) | Finance or legal owner | Yes | Write the requirement as a parameter with status `NOT_VERIFIED`; never state a rate. |
| Client HR policies (leave, probation, notice, disciplinary steps) | HR manual | Yes | Specify configurability; list each missing value as an open question. |
| Tenant and role model | Product owner | Yes | Stop the access section and name the gap. |
| Named human owner and backup per record type and decision | Client owner | Yes | Open item. AI never owns a record or a decision. |

## Workflow

1. Inspect the inputs and log sources, versions and unresolved assumptions.
2. Write the HR requirements from the template in [HR module requirements](references/hr-module-requirements.md): one section per subsection, each requirement with a stable identifier and a test oracle.
3. Add the acceptance criteria from the same reference; each names its synthetic test data and its reviewer.
4. Mark every statutory value as a parameter with status; no figure appears unless a VERIFIED row cites Act and section.
5. Add the contiguous per-tenant document series for HR documents ([standard](../references/document-numbering-requirements.md)).
6. Record the named owner and backup for each workflow, report and decision; list open items.
7. Stop when a required source, owner or oracle is absent. Recover by preserving valid work, marking the blocked scope and returning a qualified gap record.

## Outputs

| Artefact | Consumer | Acceptance condition |
| --- | --- | --- |
| HR module SRS section | Architecture, HR, finance, security, test owners | Every requirement has an identifier and an observable oracle; statutory values are parameters with status. |
| HR acceptance-criteria set | Test and go-live reviewers | Each criterion maps to a requirement and names synthetic data. |
| Open-item and owner register | HR owner | Every workflow and report has a named human owner and backup. |

## Evidence Produced

| Evidence | Reviewer | Acceptance condition |
| --- | --- | --- |
| Source, decision, trace and validation record for the HR module SRS | Requirements quality reviewer | Inputs used, decisions made, checks run, failures and unassessed items are explicit. |

## Capability and permission boundaries

Read and search are required. Editing is allowed only when the request authorises creation or repair of the named requirements artefact. Never place real employee, pay or case data in a requirement, example or fixture. Publishing, production mutation, spending and certification need explicit authority.

## Degraded mode

Fallback: if a policy manual, statutory source, reviewer or execution capability is unavailable, return the narrowest useful qualified result and mark the affected check `not assessed`; never convert an unassessed check into a pass.

## Decision Rules

| Choice or condition | Action | Failure or risk avoided |
| --- | --- | --- |
| A requirement states a statutory rate or day count | Replace with a parameter requirement citing a VERIFIED row, or mark `NOT_VERIFIED`. | Law presented as fact. |
| A requirement lets one role read pay, disciplinary and medical data | Split into separate permissions with per-role tests. | Broad exposure of sensitive files. |
| A requirement lets a model decide about a person | Require visible inputs, override and a named human decider. | Unreviewable decisions. |
| Inputs and oracles are complete | Continue and record evidence. | Acceptance that cannot be reproduced. |

## Quality Standards

- Preserve stable identifiers and bidirectional traceability from project evidence to requirements and acceptance checks.
- Apply measures only with a named metric, method, threshold, source and reviewer; run the anti-slop gate before release.

## Anti-Patterns

- Requirements that name people instead of positions. Fix: name the position and the role.
- A rate, band or day count written into the requirement text without a source row. Fix: write a parameter requirement and mark status.
- "The system shall be secure" with no per-role, per-field oracle. Fix: add one denied-case test per role and field.
- Treating an unavailable check as passed. Fix: mark it `not assessed` and state the release consequence.
- Claiming statutory or stakeholder approval without evidence. Fix: cite the source and reviewer or qualify the claim.

## References

- [HR module requirements](references/hr-module-requirements.md): subsection template, requirement wording, acceptance criteria.
- [Skill authoring and release standard](../../docs/skill-authoring-standard.md)
- [Document numbering requirements](../references/document-numbering-requirements.md): load for the HR document series.
<!-- dual-compat-end -->
<!-- local-contract-end -->
