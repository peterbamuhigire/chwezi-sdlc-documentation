# SRS and SDLC Documentation Full Kaizen Operation Prompt

Paste this prompt at the root of a PRD, SRS, architecture, test, deployment, operations, governance, or lifecycle-documentation project.

## Configuration

```text
Product/system and document set: [DISCOVER]
Lifecycle method and current phase: [DISCOVER]
Decision owners, stakeholders, and reviewers: [DISCOVER]
Implementation and evidence repositories: [DISCOVER]
Applicable standards, regulation, and assurance level: [DISCOVER]
Known change requests, defects, incidents, or review findings: [NONE OR LIST]
Cycle ID: [YYYY-MM-DD-short-name]
Improvement authority: project-document reversible edits are authorised; approvals and production changes are not
```

## Prompt

Run a full Kaizen operation on this SDLC documentation product. Documentation must improve delivery decisions and traceable evidence; it must not create ceremony or pretend to be executable proof. Freeze a capped baseline, repair root causes through bounded revisions, validate traceability and project evidence, standardise successful learning, and schedule re-measurement.

### Routes and authority

Read project instructions. Resolve Chwezi SDLC Documentation and read its `README.md`, `AGENTS.md`, the skill matching the document/product type, its references, the applicable validation route, and `09-governance-compliance/31-kaizen-engine-and-product-improvement/SKILL.md`. Read the Digital Research portfolio standard and verify current standards, legal, security, platform, and regulatory claims. Route implementation evidence to Skills Web Dev, finance to Chwezi, research to Digital Research, and rendered visual decisions to Design System Skills.

This prompt authorises reversible edits to project documentation, local traceability artefacts, templates, and validation fixtures. It does not authorise requirements approval, risk acceptance, production change, certification, stakeholder sign-off, or canonical engine edits. Stop if the product boundary, decision owner, governing baseline, authority, or rollback copy is missing. Mark absent implementation, user, render, security, standards, or reviewer evidence `NOT ASSESSED`.

### Evidence pack and inventory

Create `docs/kaizen/<cycle-id>/` with `00-scope-and-evidence.md`, `01-baseline-scorecard.md`, `02-improvement-backlog.md`, `03-experiment-log.md`, `04-validation-record.md`, `05-final-report.md`, and `06-next-cycle.md`. Inventory vision/PRD, stakeholder needs, requirements, use cases, data, architecture, interfaces, decisions, risks, controls, test plans/results, deployment, operations, acceptance, change records, approvals, and cross-engine handoffs. Build a trace map from source need to requirement to design element to test/evidence to release decision.

### Capped baseline

Score ten equal dimensions with evidence, confidence, deficiency, and status:

1. Vision, problem, outcomes, scope, assumptions, exclusions, and success measures.
2. Stakeholders, users, context, accessibility/inclusion, roles, and decision rights.
3. Functional requirements: atomicity, clarity, necessity, feasibility, priority, and acceptance criteria.
4. Traceability from source and rationale through design, implementation, verification, and approval.
5. Architecture/design coherence, interfaces, data contracts, decisions, alternatives, and constraints.
6. Non-functional requirements: security, privacy, safety, performance, reliability, usability, accessibility, localisation, and operability.
7. Test strategy, positive/negative/failed paths, environments, data, oracles, coverage, and evidence.
8. Deployment, migration, configuration, monitoring, incident, continuity, rollback, and support readiness.
9. Governance, compliance, risks, changes, versions, reviews, approvals, and method-fit for Agile/Waterfall/Hybrid.
10. Document quality, consistency, navigability, implementation handoff, release bundle, and learning loop.

Show raw scores and publish `min(raw_overall, 65)`. Freeze before editing. An untraceable mandatory requirement, unverifiable acceptance condition, unresolved security/safety/compliance issue, or missing release authority remains a blocker.

### Improve toward 95

Create a P0/P1/P2 backlog. Each action names evidence, root cause, exact requirement/document/template/gate, hypothesis, owner/reviewer, defect/rework/latency measure, guardrails, smallest reversible revision, rollback, stop rule, acceptance proof, target contribution, and re-audit date. Reject process additions that do not reduce defects, rework, ambiguity, risk, or decision latency.

Run one controlled revision at a time. Preserve baseline and identifiers. Repair the source of ambiguity, trace break, contradictory rule, missing failed path, or untestable requirement. Run impacted consistency and trace checks after each change. Where implementation evidence is unavailable, specify the exact executable check and owner without claiming the document proves it.

### Strict anti-AI-slop gate

Apply anti-AI-slop rules while authoring and audit after every major document/iteration and at release. Grade F blocks release. Reject fabricated standards, approvals, stakeholders, constraints, system behaviour, test results, trace links, risks, or compliance; “shall” statements with no observable fit criterion; template sections that do not apply; duplicated requirements; generic personas and use cases; architecture buzzwords without decisions; exhaustive-looking lists with no priority; fake traceability; uniform AI prose; and documents that substitute volume for delivery evidence.

Every requirement must have source/rationale, owner, priority, measurable acceptance, dependencies, failure behaviour, and trace destination as applicable. Every design decision must name alternatives and consequences. Every readiness claim must link to executable, rendered, user, security, operational, or approval evidence. A complete template is not a complete system specification.

### Validate and re-measure

Run applicable structure, schema, link, terminology, requirement-quality, traceability, standards-source, security/privacy, test-evidence, render/accessibility, baseline, pack, and sign-off checks. Sample traces in both directions. Check contradictions, orphan requirements, orphan tests, stale versions, unresolved TBDs, and method-specific artefacts. Record commands, samples, reports, reviewers, failures, and limitations.

Promote accepted learning into the project baseline, trace matrix, decision record, template, checklist, fixture, validator, change-control rule, or handoff. Re-score only from evidence and state the uncapped final result. Write the final report with before/after results, changed artefacts, trace improvements, unavailable execution evidence, release verdict, and next review.

Return the score summary, completed changes, validation record, blockers, evidence-pack path, and re-audit date. Do not claim conformance, completeness, or readiness beyond verified authority and evidence.
