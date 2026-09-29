---
name: 03-compliance-documentation
description: Use when producing a governed compliance document set from verified obligations, controls, owners, evidence, review cadence, and approvals. Use audit-report for independent findings and regulator-overlap-mapping for cross-regime reuse.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Compliance Documentation Skill

<!-- dual-compat-start -->

## Use When

- Use when producing a governed compliance document set from verified obligations, controls, owners, evidence, review cadence, and approvals. Use audit-report for independent findings and regulator-overlap-mapping for cross-regime reuse.

## Do Not Use When

- Do not use when a more specific upstream or downstream skill owns the task, or when the required project context has not been prepared.
- Do not use this skill to fabricate missing project facts, legal conclusions, test results, approvals, or certification claims.

## Required Inputs

| Artefact | Source or provider | Required? | Missing-input behaviour |
|---|---|---:|---|
| Verified obligations and jurisdictions; system scope and data flows; control register; policy owners; evidence sources; review and approval cadence | Legal/privacy advisers and accountable control owners | Yes | Stop dependent work; name the missing item, owner, and decision impact. A review check remains `not assessed`. |
| Scope, audience, baseline/version, and accountable decision owner | Requester or project context | Yes | Ask for or record the gap; do not infer authority or scope. |

## Capability and permission boundaries

Default to read-only. Read and search access to the supplied artefacts are required. Editing is limited to an explicitly authorised requested draft or project files. Execute validation only when authorised; publishing, signature, certification, production mutation, destructive action, spending, and risk acceptance require explicit authority.

## Degraded Mode

When files, tools, network, rendering, fonts, execution, or evidence are unavailable, return the narrowest useful qualified draft or finding set. Name every unavailable check and its consequence; an unassessed check is never a pass. Preserve evidence already gathered and provide the exact next verification step.

## Decision Rules

| Condition | Action | Failure or risk avoided |
|---|---|---|
| A required source, owner, obligation, or acceptance condition is missing | Stop the affected claim and record the gap | Unsupported governance artefact |
| Evidence satisfies the declared acceptance condition | Record the decision and hand off to the named consumer | Ambiguous approval or release |

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
| Compliance Documentation | Accountable reviewer, control owner, auditor, or release authority | Each obligation maps to an owned control, evidence source, review cadence, exception path, and authorised approval state. |
| Gap and decision record | Accountable owner and downstream reviewer | Every gap has status, impact, owner, next action, and no unsupported pass or approval. |

## Evidence Produced

| Evidence | Contents | Acceptance condition |
|---|---|---|
| Compliance Documentation evidence record | Source identifiers, scope/version, decisions, checks, exceptions, and approval state | A reviewer can reproduce each material conclusion from named sources. |
| Validation record | Check, result (`pass`, `fail`, or `not assessed`), evidence location, date, and actor | No required check is omitted or silently treated as passed. |

## Quality Standards

- Keep outputs grounded in source context, traceable to stated standards, and specific enough to review or verify.
- Use deterministic acceptance conditions and preserve traceability from source to decision and output.
- Separate facts, inferences, assumptions, and approvals; never present one as another.
- Apply `28-anti-ai-slop` during authoring and `29-ai-slop-audit` at major checkpoints and release.

## Anti-Patterns

- **Producing Compliance Documentation from assumptions instead of named project sources.** Fix: Cite the source or mark the item unverified.
- **Treating a missing or inaccessible check as passed.** Fix: Mark it `not assessed`, state impact, and block dependent claims.
- **Using vague gates such as `adequate`, `secure`, or `user-friendly`.** Fix: Replace each with an observable criterion, threshold, and evidence source.
- **Copying a generic template without product, control, role, version, or jurisdiction detail.** Fix: Ground every section in the supplied context and remove unused boilerplate.
- **Publishing, signing, certifying, changing production, or accepting risk without authority.** Fix: Prepare a draft and route the decision to the accountable owner.
- **Listing evidence without provenance or an acceptance result.** Fix: Record source, period, integrity check, mapping, and pass/fail/not-assessed status.

## Worked Example

Example: if a required source, owner, obligation, or acceptance condition is missing, stop the affected claim and record the gap. Record the evidence and result in the validation record; this avoids unsupported governance artefact.

## References

- [Generation logic](logic.prompt): load when creating the complete artefact.
- [Skill notes](README.md): consult for local examples and invocation context.
- [Repository operating rules](../../AGENTS.md): apply the engine's routing, evidence, and release gates.
- [Data governance, catalog, and lineage requirements](../../02-requirements-engineering/fundamentals/during/05-conceptual-data-modeling/references/data-governance-catalog-lineage-requirements.md): load when obligations cover data ownership, classification, retention, lineage, or erasure evidence.

<!-- dual-compat-end -->

## Overview

This skill generates regulatory compliance documentation that maps project requirements, data handling practices, and architectural decisions to applicable regulatory frameworks. The skill assesses applicability of GDPR, HIPAA, and SOC2, then produces detailed compliance mappings, gap analyses, and remediation roadmaps for each applicable framework. Only frameworks relevant to the project's domain and data classification are included.

## When to Use This Skill

- When the project handles personal data subject to GDPR
- When the project processes protected health information (PHI) under HIPAA
- When the project requires SOC2 attestation for service organization controls
- When stakeholders or clients require evidence of regulatory compliance posture
- When preparing for regulatory audits or third-party assessments
- When onboarding into regulated industries (healthcare, finance, government)

## Quick Reference

| Attribute | Value |
|-----------|-------|
| **Input** | vision.md, quality_standards.md, SRS_Draft.md, HLD.md |
| **Output** | Compliance_Docs.md |
| **Standard** | GDPR, HIPAA, SOC2 |
| **Estimated Time** | 20-35 minutes |

## Input Files

| File | Purpose | Required? |
|------|---------|-----------|
| `projects/<ProjectName>/_context/vision.md` | Project scope, domain, and data subjects to determine regulatory applicability | Yes |
| `projects/<ProjectName>/_context/domain.md` | Resolves the active domain (`uganda`, `healthcare`, `finance`, `education`, `retail`, `logistics`, `government`, `agriculture`) | Yes |
| `projects/<ProjectName>/_context/quality-standards.md` | Stakeholder-specified security and compliance frameworks (scopes which obligations are in force) | Yes |
| `projects/<ProjectName>/_registry/controls.yaml` | Consultant's control selection (`selected[]` entries with `id`, `applies_because`, optional `owner`, `exemption`) | Yes |
| `projects/<ProjectName>/_registry/identifiers.yaml` | Identifier registry — supplies the verification test case IDs (`TC-*`) per control | Yes |
| `domains/<domain>/controls/control-register.yaml` | Domain control library — source of `title`, `category`, `verification_kinds`, `minimum_evidence`, and `regulatory_anchor` for each selected control | Yes |
| `domains/<domain>/controls/obligations.yaml` | Obligation-to-control map used for the gap analysis | Yes |
| `domains/<domain>/controls/evidence-expectations.yaml` | Per-category artifact patterns — identifies satisfying artifacts for each control | Yes |
| `domains/<domain>/controls/required-reviews.yaml` | Per-category reviewer roles assigned to each control section | Yes |
| `projects/<ProjectName>/<phase>/<document>/SRS_Draft.md` | Requirements referencing data handling, authentication, and access control | No |
| `projects/<ProjectName>/<phase>/<document>/HLD.md` | Architecture decisions affecting data flow, storage, and transmission | No |

To find the anchored control for a requirement, run `python -m engine controls search "<query>" [--domain <d>] [--framework <f>]` (read-only; it abstains when nothing matches well). Cite the returned control ID and registry path; do not paraphrase the control.

## Output Files

| File | Description |
|------|-------------|
| `projects/<ProjectName>/<phase>/<document>/Compliance_Docs.md` | Complete compliance documentation with applicability assessment and gap analysis |

## Stimulus / Process / Response

- **Stimulus:** the consultant requests a compliance annex for a project whose `_registry/controls.yaml` has been populated with the applicable controls selected from the domain control library.
- **Process:** the skill hydrates the control library, joins it with the consultant's selection, gathers satisfying artifacts and verification test case IDs, and emits a deterministic per-control section.
- **Response:** a `Compliance_Docs.md` whose body sections are driven by the selected controls, each tied back to a regulatory anchor and an assigned reviewer; no free-text claims about frameworks that were not enumerated in `_context/quality-standards.md`.

## Core Instructions

1. The skill SHALL read `projects/<ProjectName>/_context/vision.md` to determine the project domain, target users, data subjects, and geographic scope. If the file is missing, halt execution and report the error.

2. The skill SHALL resolve the active domain from `projects/<ProjectName>/_context/domain.md`. If the file does not name one of the eight engine-recognized domains, halt and emit `[CONTEXT-GAP: domain]`.

3. The skill SHALL load `projects/<ProjectName>/_registry/controls.yaml` and extract every entry under `selected[]`. If the file is missing or `selected` is empty, halt and emit `[CONTEXT-GAP: controls.yaml]`. Each entry supplies the control `id`, the `applies_because` justification, and optional `owner` and `exemption` values.

4. The skill SHALL load `domains/<domain>/controls/control-register.yaml` and join each selected `id` to its `title`, `category`, `verification_kinds`, `minimum_evidence`, and `regulatory_anchor`. An `id` present in the selection but absent from the register SHALL be tagged `[V&V-FAIL: unknown_control]` and excluded from the output.

5. The skill SHALL load `domains/<domain>/controls/evidence-expectations.yaml` and, for each control's `category`, enumerate the expected artifact path patterns. The skill SHALL then scan the project workspace for artifacts matching each pattern (`fnmatch` on POSIX-normalized relative paths) and list the matching artifacts as the satisfying evidence. A pattern with no matching artifact SHALL be recorded in the Compliance Gap Analysis.

6. The skill SHALL load `projects/<ProjectName>/_registry/identifiers.yaml` and, for each selected control, extract every test case identifier (`TC-*`) that references the control `id` or is tagged with the control's `category`, and list those identifiers under the control's verification subsection.

7. The skill SHALL load `domains/<domain>/controls/required-reviews.yaml` and, for each control's `category`, record the `reviewer_role` and `cadence`. Controls whose category has no required-review entry SHALL be tagged `[REVIEWER-UNASSIGNED]`.

8. The skill SHALL perform a Regulatory Applicability Assessment grounded in `_context/quality-standards.md`. A framework is "in scope" only if its name appears (case-insensitive substring) in that file. Controls whose `regulatory_anchor.framework` is not in scope SHALL be excluded from the main body and listed in an appendix.

9. The skill SHALL classify all data elements identified in the project into categories: Public, Internal, Confidential, Restricted (or PII, PHI, PCI as applicable).

10. For each selected, in-scope control the skill SHALL emit a section containing (a) control `id` and `title`, (b) the `regulatory_anchor.framework` and `clause`, (c) the `applies_because` justification, (d) the satisfying artifacts listed under step 5, (e) the verification test case IDs listed under step 6, and (f) the assigned reviewer listed under step 7.

11. For each applicable framework, the skill SHALL generate a dedicated compliance section:
   - **GDPR:** Lawful basis for processing, data subject rights implementation, Data Protection Impact Assessment (DPIA) triggers, data retention policies, cross-border transfer mechanisms
   - **HIPAA:** PHI identification, administrative/physical/technical safeguards, Business Associate Agreement (BAA) requirements, minimum necessary standard
   - **SOC2:** Trust Service Criteria mapping (Security, Availability, Processing Integrity, Confidentiality, Privacy)

12. The skill SHALL map security controls from the project architecture to regulatory requirements by loading `domains/<domain>/controls/obligations.yaml` and, for each in-scope obligation, listing the `satisfied_by` control IDs and whether each is present in the project selection.

13. The skill SHALL generate a Compliance Gap Analysis listing (a) obligations whose `framework` is in scope but for which no `satisfied_by` control is selected, (b) selected controls with no satisfying artifact, and (c) selected controls without a registered verification test case identifier.

14. The skill SHALL produce a Remediation Roadmap prioritizing compliance gaps by risk severity and regulatory deadline pressure.

15. The skill SHALL explicitly state when a framework is determined to be not applicable, with justification.

16. The skill SHALL avoid speculative compliance claims -- if insufficient information exists to assess a control, flag it as `[ASSESSMENT-PENDING]` rather than assuming compliance.

## Output Format Specification

The generated `Compliance_Docs.md` SHALL contain the following sections:

```
# Compliance Documentation
## 1. Document Information
## 2. Regulatory Applicability Assessment
## 3. Data Classification
## 4. GDPR Compliance (if applicable)
### 4.1 Lawful Basis for Processing
### 4.2 Data Subject Rights
### 4.3 Data Protection Impact Assessment
### 4.4 Data Retention & Deletion
### 4.5 Cross-Border Transfers
## 5. HIPAA Compliance (if applicable)
### 5.1 PHI Identification
### 5.2 Administrative Safeguards
### 5.3 Physical Safeguards
### 5.4 Technical Safeguards
### 5.5 BAA Requirements
## 6. SOC2 Compliance (if applicable)
### 6.1 Security Criteria
### 6.2 Availability Criteria
### 6.3 Processing Integrity Criteria
### 6.4 Confidentiality Criteria
### 6.5 Privacy Criteria
## 7. Security Controls Mapping
## 8. Compliance Gap Analysis
## 9. Remediation Roadmap
## 10. Revision History
```

## Common Pitfalls

- Assuming all three frameworks apply without performing applicability assessment
- Making definitive compliance claims without sufficient architectural evidence
- Omitting data classification, which is the foundation for all compliance mapping
- Treating compliance as binary (compliant/non-compliant) without recognizing partial compliance states
- Ignoring cross-framework overlaps (e.g., GDPR and HIPAA both require access controls)
- Generating boilerplate compliance text that is not grounded in the actual project context

## Verification Checklist

1. Regulatory applicability is assessed and justified for each framework.
2. Data classification covers all data elements identified in the project.
3. Each applicable framework has a dedicated section with specific, grounded controls.
4. Non-applicable frameworks are explicitly excluded with justification.
5. Security controls are mapped to specific regulatory obligations.
6. Compliance gaps are identified with severity and remediation priority.
7. No speculative compliance claims exist -- uncertain items are tagged `[ASSESSMENT-PENDING]`.
8. The remediation roadmap is prioritized by risk and regulatory urgency.

## Integration

- **Upstream:** Consumes vision and quality standards from project context, and SRS/design artifacts from prior phases. Benefits from 02-audit-report findings.
- **Downstream:** Feeds external regulatory submissions and audit processes. Informs 04-risk-assessment compliance risk category.

## Standards Compliance

| Standard | Governs |
|----------|---------|
| GDPR (EU 2016/679) | Personal data processing, data subject rights, cross-border transfers |
| HIPAA (45 CFR Parts 160, 164) | Protected health information safeguards and BAA requirements |
| SOC2 (AICPA TSC) | Trust Service Criteria for service organizations |

## Resources

- GDPR: Regulation (EU) 2016/679 of the European Parliament
- HIPAA: 45 CFR Parts 160 and 164, HHS Security Rule Guidance
- AICPA: Trust Services Criteria (SOC2)
- CLAUDE.md: Project-level quality and compliance constraints
