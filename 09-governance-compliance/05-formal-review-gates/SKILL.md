---
name: 05-formal-review-gates
description: Use when defining or operating evidence-based lifecycle review gates, entry criteria, decision rights, outcomes, and remediation. Use sign-off-ledger to record approvals and waiver-management for time-bound exceptions.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Skill: Formal Review Gates (PSR / CSR / FSAR)

<!-- dual-compat-start -->

## Use When

- Use when defining or operating evidence-based lifecycle review gates, entry criteria, decision rights, outcomes, and remediation. Use sign-off-ledger to record approvals and waiver-management for time-bound exceptions.

## Do Not Use When

- Do not use when a more specific upstream or downstream skill owns the task, or when the required project context has not been prepared.
- Do not use this skill to fabricate missing project facts, legal conclusions, test results, approvals, or certification claims.

## Required Inputs

| Artefact | Source or provider | Required? | Missing-input behaviour |
|---|---|---:|---|
| Lifecycle and baseline plan; gate entry and exit criteria; mandatory evidence; decision rights; remediation SLA; waiver and escalation rules | Delivery governance owner and named gate authorities | Yes | Stop dependent work; name the missing item, owner, and decision impact. A review check remains `not assessed`. |
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
| Skill: Formal Review Gates (PSR / CSR / FSAR) | Accountable reviewer, control owner, auditor, or release authority | Each gate has deterministic criteria, evidence locations, authorised outcomes, conditions, remediation ownership, and an auditable decision record. |
| Gap and decision record | Accountable owner and downstream reviewer | Every gap has status, impact, owner, next action, and no unsupported pass or approval. |

## Evidence Produced

| Evidence | Contents | Acceptance condition |
|---|---|---|
| Skill: Formal Review Gates (PSR / CSR / FSAR) evidence record | Source identifiers, scope/version, decisions, checks, exceptions, and approval state | A reviewer can reproduce each material conclusion from named sources. |
| Validation record | Check, result (`pass`, `fail`, or `not assessed`), evidence location, date, and actor | No required check is omitted or silently treated as passed. |

## Quality Standards

- Keep outputs grounded in source context, traceable to stated standards, and specific enough to review or verify.
- Use deterministic acceptance conditions and preserve traceability from source to decision and output.
- Separate facts, inferences, assumptions, and approvals; never present one as another.
- Apply `28-anti-ai-slop` during authoring and `29-ai-slop-audit` at major checkpoints and release.

## Anti-Patterns

- **Producing Skill: Formal Review Gates (PSR / CSR / FSAR) from assumptions instead of named project sources.** Fix: Cite the source or mark the item unverified.
- **Treating a missing or inaccessible check as passed.** Fix: Mark it `not assessed`, state impact, and block dependent claims.
- **Using vague gates such as `adequate`, `secure`, or `user-friendly`.** Fix: Replace each with an observable criterion, threshold, and evidence source.
- **Copying a generic template without product, control, role, version, or jurisdiction detail.** Fix: Ground every section in the supplied context and remove unused boilerplate.
- **Publishing, signing, certifying, changing production, or accepting risk without authority.** Fix: Prepare a draft and route the decision to the accountable owner.
- **Listing evidence without provenance or an acceptance result.** Fix: Record source, period, integrity check, mapping, and pass/fail/not-assessed status.

## Worked Example

Example: if required evidence is missing or inaccessible, mark the check not assessed, state impact, and stop any pass decision. Record the evidence and result in the validation record; this avoids false assurance from an incomplete review.

## References

- [Repository operating rules](../../AGENTS.md): apply the engine's routing, evidence, and release gates.

<!-- dual-compat-end -->

## Source
Royce, W.W. (1970). Managing the Development of Large Software Systems. IEEE WESCON, p. 335-337. Step 5: Involve the Customer.

## Purpose
Generate formal customer review gate documentation for three mandatory review points in the waterfall lifecycle. These reviews commit the customer at earlier points, preventing the "contractor free rein" failure mode Royce identified.

## Trigger
User says: "generate review gates", "create PSR document", "generate CSR", "prepare FSAR", "customer review documentation"

## Three Review Gates

### PSR — Preliminary Software Review
**Timing:** After Preliminary Program Design (Phase 03 HLD complete)
**Purpose:** Customer commits to the architecture before detailed design begins
**Attendees:** Customer representative, project manager, lead architect, systems analyst
**Outputs:** PSR minutes, action items, customer sign-off on HLD

**PSR Document Template:**
Generate to: `projects/<ProjectName>/09-governance-compliance/05-formal-review-gates/PSR.md`

```markdown
# Preliminary Software Review (PSR)

**Project:** <ProjectName>
**Date:** <date>
**Location/Platform:** <location>
**Royce Reference:** IEEE WESCON 1970, Step 5

## Attendees
| Name | Role | Organization |
|------|------|-------------|

## Review Scope
- Software Requirements (Doc 1): ☐ Reviewed ☐ Approved ☐ Conditional ☐ Rejected
- Preliminary Design Spec (Doc 2): ☐ Reviewed ☐ Approved ☐ Conditional ☐ Rejected

## Architecture Decisions Confirmed
[List each major architectural decision agreed at this review]

## Open Items / Action Items
| ID | Item | Owner | Due Date |
|----|------|-------|----------|

## Customer Commitment
By attending this PSR and not formally objecting in writing within 5 business days, the customer commits to the Preliminary Design as the basis for detailed design.

**Customer Representative Signature:** _________________ Date: _________
**Project Manager Signature:** _________________ Date: _________
```

---

### CSR — Critical Software Review
**Timing:** During/after Program Design (Phase 03 complete, multiple rounds permitted)
**Purpose:** Customer reviews detailed design decisions before coding begins; catches requirement misinterpretations
**Attendees:** Customer representative, full design team
**Outputs:** CSR minutes, design issue log, customer approval to proceed to coding

**CSR Document Template:**
Generate to: `projects/<ProjectName>/09-governance-compliance/05-formal-review-gates/CSR-<n>.md`
(Multiple CSRs permitted — number them CSR-1, CSR-2, etc.)

Key sections: Design compliance matrix (each requirement → design element), open design issues, customer approval statement.

---

### FSAR — Final Software Acceptance Review
**Timing:** After testing complete, before operations handover
**Purpose:** Final customer acceptance; commits customer to operational deployment
**Attendees:** Customer, project manager, test lead, operations lead
**Outputs:** FSAR report, acceptance certificate, known issues register

**FSAR Document Template:**
Generate to: `projects/<ProjectName>/09-governance-compliance/05-formal-review-gates/FSAR.md`

Key sections: Test results summary, all-requirements coverage statement, known defects with severity/disposition, formal acceptance statement, operations readiness confirmation.

---

## Execution Instructions

When generating any review gate document:
1. Read `projects/<ProjectName>/_context/vision.md` for project context
2. Read `projects/<ProjectName>/_context/stakeholders.md` for attendee roles
3. Read the relevant completed documents (HLD for PSR, LLD/API spec for CSR, Test Report for FSAR)
4. Generate the document with all sections populated from available context
5. Flag with `<!-- TODO: CUSTOMER SIGNATURE REQUIRED -->` any field requiring physical signature

## Ugandan Public-Sector / NGO Delivery Constraints

For Ugandan government, local-government, public-entity, NGO, or donor-funded clients, treat funding availability and procurement sign-off as *blocking* gates. Sequence each review gate (and especially the FSAR-to-deployment handover) **after** the procurement and fiscal sign-offs that fund and authorise the work, and record the warrant/release and Contracts Committee/contract-signature/Solicitor-General evidence at the gate. Schedule the gate away from financial-year close, board-of-survey, and audit blackout periods. See `references/uganda-public-sector-and-ngo-delivery-constraints.md`; the finance engine (`chwezi-accounting-doctrine`) is the authority for the substance, and no statutory threshold is fixed here as current.

## Standards References
- IEEE 1028-2008: Software Reviews and Audits
- IEEE 15288-2015: System Life Cycle Processes (Section 6.4.7 Verification Process)
- Royce (1970): Step 5, Figure 9, p.337
