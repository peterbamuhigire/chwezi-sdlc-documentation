# Skill catalogue

This page lists the 160 active skills of Chwezi SDLC Documentation by phase (count taken on 2026-11-10 with `find`, excluding `templates/`). Each name links to its `SKILL.md`, which is the authority: the descriptions here are short summaries, so read the skill's own file before relying on one. Requirements engineering nests `agile/`, `fundamentals/`, `hybrid/` and `waterfall/` subfolders. This page was moved out of the root README on 2026-10-31 with the rows unchanged.

The root [`README.md`](../README.md) holds the phase table and the task-to-skill table.

## Contents

- [Strategic vision](#strategic-vision): 13 skills
- [Requirements engineering](#requirements-engineering): 41 skills
- [Design documentation](#design-documentation): 18 skills
- [Development artefacts](#development-artefacts): 6 skills
- [Testing documentation](#testing-documentation): 10 skills
- [Deployment and operations](#deployment-and-operations): 23 skills
- [Agile artefacts](#agile-artefacts): 5 skills
- [End-user documentation](#end-user-documentation): 9 skills
- [Governance and compliance](#governance-and-compliance): 34 skills

## Strategic vision

Folder `01-strategic-vision`, 13 skills.

| Skill | What it does |
|---|---|
| [`01-prd-generation`](../01-strategic-vision/01-prd-generation/SKILL.md) | Traceable PRD: objectives, prioritised features, success measures and release scope |
| [`02-business-case`](../01-strategic-vision/02-business-case/SKILL.md) | Business case with costs, benefits, ROI, payback, NPV, sensitivity and a go/no-go call |
| [`03-vision-statement`](../01-strategic-vision/03-vision-statement/SKILL.md) | Strategic north star: target users, problem, differentiated value and scope limits |
| [`04-lean-canvas`](../01-strategic-vision/04-lean-canvas/SKILL.md) | Lean Canvas, Impact Map and Hypothesis Board for untested assumptions |
| [`05-system-overview`](../01-strategic-vision/05-system-overview/SKILL.md) | Plain-language system purpose, context, major functions, constraints and actors |
| [`06-ai-economic-value-brief`](../01-strategic-vision/06-ai-economic-value-brief/SKILL.md) | Outcome, data-readiness, cost and risk brief for an AI proposal before PRD work |
| [`07-premium-product-positioning`](../01-strategic-vision/07-premium-product-positioning/SKILL.md) | Case for premium pricing through buyer trust, proof and service quality |
| [`10-saas-mvp-scoping-doc`](../01-strategic-vision/10-saas-mvp-scoping-doc/SKILL.md) | Bounded SaaS v1 with one channel, explicit cuts and a feature-triage log |
| [`11-saas-moat-and-defensibility-plan`](../01-strategic-vision/11-saas-moat-and-defensibility-plan/SKILL.md) | Evidence-based SaaS defensibility plan separating real from false moats |
| [`12-saas-pricing-and-packaging-spec`](../01-strategic-vision/12-saas-pricing-and-packaging-spec/SKILL.md) | SaaS tiers, value metric, feature gates, expansion and price-change policy |
| [`13-ai-feature-strategy-doc`](../01-strategic-vision/13-ai-feature-strategy-doc/SKILL.md) | Choose, tier and sequence AI features; build versus buy and AI moat |
| [`14-ai-agent-strategy-doc`](../01-strategic-vision/14-ai-agent-strategy-doc/SKILL.md) | Agent-versus-workflow decision, autonomy levels and capability sequencing |
| [`15-game-product-and-production-brief`](../01-strategic-vision/15-game-product-and-production-brief/SKILL.md) | Game player promise, platforms, production model and greenlight decision |

## Requirements engineering

Folder `02-requirements-engineering`, 41 skills.

| Skill | What it does |
|---|---|
| [`13-saas-billing-and-metering-spec`](../02-requirements-engineering/13-saas-billing-and-metering-spec/SKILL.md) | SaaS usage events, billing, credits, refunds, dunning and metering controls |
| [`14-ai-feature-prd-spec`](../02-requirements-engineering/14-ai-feature-prd-spec/SKILL.md) | Testable AI feature requirements for quality, latency, cost, citations and consent |
| [`15-ai-data-and-knowledge-base-spec`](../02-requirements-engineering/15-ai-data-and-knowledge-base-spec/SKILL.md) | AI knowledge sources, ingestion, tenant isolation, freshness, retention and lineage |
| [`16-ai-agent-feature-prd-spec`](../02-requirements-engineering/16-ai-agent-feature-prd-spec/SKILL.md) | Agent task scope, autonomy, budgets, intervention and irreversible-action gates |
| [`17-ai-agent-action-catalogue-spec`](../02-requirements-engineering/17-ai-agent-action-catalogue-spec/SKILL.md) | Schema-bound agent tools with side effects, approvals, audit fields and kill switches |
| [`18-embedded-accounting-engine-srs`](../02-requirements-engineering/18-embedded-accounting-engine-srs/SKILL.md) | Requirements for software that touches money, inventory value, payroll, tax or reports |
| [`19-game-software-requirements-specification`](../02-requirements-engineering/19-game-software-requirements-specification/SKILL.md) | Testable game requirements (GREQ): loop, saves, multiplayer, monetisation, certification |
| [`20-hr-module-srs`](../02-requirements-engineering/20-hr-module-srs/SKILL.md) | Requirements and acceptance criteria for an HR module: positions, contract classes, leave, payroll inputs, access, audit |
| [`agile/01-user-story-generation`](../02-requirements-engineering/agile/01-user-story-generation/SKILL.md) | INVEST user stories, epics, story points and initial acceptance criteria |
| [`agile/02-acceptance-criteria`](../02-requirements-engineering/agile/02-acceptance-criteria/SKILL.md) | Deterministic Given-When-Then acceptance criteria for existing stories |
| [`agile/03-story-mapping`](../02-requirements-engineering/agile/03-story-mapping/SKILL.md) | Story map with user activities, walking skeleton and release slices |
| [`agile/04-backlog-prioritization`](../02-requirements-engineering/agile/04-backlog-prioritization/SKILL.md) | MoSCoW and WSJF ranking with release or sprint order |
| [`fundamentals/after/08-requirements-management`](../02-requirements-engineering/fundamentals/after/08-requirements-management/SKILL.md) | Baselines, change control, versions and impact after requirements exist |
| [`fundamentals/after/09-traceability-engineering`](../02-requirements-engineering/fundamentals/after/09-traceability-engineering/SKILL.md) | Forward and backward links from goals to requirements, design, code, tests and evidence |
| [`fundamentals/after/10-requirements-metrics`](../02-requirements-engineering/fundamentals/after/10-requirements-metrics/SKILL.md) | Quantitative quality gates for ambiguity, completeness, traceability and volatility |
| [`fundamentals/after/11-requirements-reuse`](../02-requirements-engineering/fundamentals/after/11-requirements-reuse/SKILL.md) | Curated reusable requirement patterns and product-line variants |
| [`fundamentals/after/12-solution-evaluation-and-transition`](../02-requirements-engineering/fundamentals/after/12-solution-evaluation-and-transition/SKILL.md) | Adoption, transition, go/no-go evidence and post-implementation evaluation |
| [`fundamentals/before/01-stakeholder-analysis`](../02-requirements-engineering/fundamentals/before/01-stakeholder-analysis/SKILL.md) | Stakeholder identification, influence, interests, decision rights and communication |
| [`fundamentals/before/02-elicitation-toolkit`](../02-requirements-engineering/fundamentals/before/02-elicitation-toolkit/SKILL.md) | Select and run interviews, workshops, observation, surveys and prototypes |
| [`fundamentals/before/03-brd-generation`](../02-requirements-engineering/fundamentals/before/03-brd-generation/SKILL.md) | Business Requirements Document bridging strategy and detailed requirements |
| [`fundamentals/before/04-business-analysis-planning`](../02-requirements-engineering/fundamentals/before/04-business-analysis-planning/SKILL.md) | Business-analysis governance, decision rights, cadence and artefact plan |
| [`fundamentals/during/04-requirements-analysis`](../02-requirements-engineering/fundamentals/during/04-requirements-analysis/SKILL.md) | Classify, reconcile, prioritise and test the feasibility of elicited requirements |
| [`fundamentals/during/05-conceptual-data-modeling`](../02-requirements-engineering/fundamentals/during/05-conceptual-data-modeling/SKILL.md) | Conceptual entities, relationships and invariants; data contracts and dictionaries |
| [`fundamentals/during/06-requirements-patterns`](../02-requirements-engineering/fundamentals/during/06-requirements-patterns/SKILL.md) | Decision tables, state transitions, CRUD matrices and requirement patterns |
| [`fundamentals/during/07-requirements-validation`](../02-requirements-engineering/fundamentals/during/07-requirements-validation/SKILL.md) | Independent review for correctness, consistency, feasibility and testability |
| [`fundamentals/during/08-business-process-modeling`](../02-requirements-engineering/fundamentals/during/08-business-process-modeling/SKILL.md) | As-is and to-be workflows, handoffs, controls and exceptions |
| [`fundamentals/during/09-business-rules-analysis`](../02-requirements-engineering/fundamentals/during/09-business-rules-analysis/SKILL.md) | Policies, calculations, eligibility, constraints, ownership and effective dates |
| [`fundamentals/during/10-prototyping-and-solution-discovery`](../02-requirements-engineering/fundamentals/during/10-prototyping-and-solution-discovery/SKILL.md) | Compare solution candidates or prototypes before locking requirements |
| [`fundamentals/during/11-experience-mapping-requirements`](../02-requirements-engineering/fundamentals/during/11-experience-mapping-requirements/SKILL.md) | Turn customer, employee or ecosystem journeys into traceable requirements |
| [`fundamentals/during/12-service-blueprint-requirements`](../02-requirements-engineering/fundamentals/during/12-service-blueprint-requirements/SKILL.md) | Service blueprint to frontstage, backstage, support and recovery requirements |
| [`hospitality-operating-model-srs`](../02-requirements-engineering/hospitality-operating-model-srs/SKILL.md) | Requirements for hotel, lodge, restaurant, bar, catering and venue systems |
| [`hybrid/hybrid-synchronization`](../02-requirements-engineering/hybrid/hybrid-synchronization/SKILL.md) | Keep Water-Scrum-Fall backlog, DoR/DoD and evidence tied to the approved baseline |
| [`retail-operating-model-srs`](../02-requirements-engineering/retail-operating-model-srs/SKILL.md) | Retail, POS, pricing, promotions, fulfilment, returns and store-operations requirements |
| [`waterfall/01-initialize-srs`](../02-requirements-engineering/waterfall/01-initialize-srs/SKILL.md) | Create a Waterfall SRS workspace with IEEE structure, identifiers and source context |
| [`waterfall/02-context-engineering`](../02-requirements-engineering/waterfall/02-context-engineering/SKILL.md) | System boundary, actors, external systems, interfaces and assumptions |
| [`waterfall/03-descriptive-modeling`](../02-requirements-engineering/waterfall/03-descriptive-modeling/SKILL.md) | Scenarios, flows, states, activities and domain views |
| [`waterfall/04-interface-specification`](../02-requirements-engineering/waterfall/04-interface-specification/SKILL.md) | User, software, hardware, communication and external interfaces |
| [`waterfall/05-feature-decomposition`](../02-requirements-engineering/waterfall/05-feature-decomposition/SKILL.md) | Scope to capabilities, features and atomic, traceable requirements |
| [`waterfall/06-logic-modeling`](../02-requirements-engineering/waterfall/06-logic-modeling/SKILL.md) | Decisions, calculations, state transitions, constraints and exception logic |
| [`waterfall/07-attribute-mapping`](../02-requirements-engineering/waterfall/07-attribute-mapping/SKILL.md) | Measurable non-functional requirements (SRS 3.3-3.6) against ISO/IEC 25010 |
| [`waterfall/08-semantic-auditing`](../02-requirements-engineering/waterfall/08-semantic-auditing/SKILL.md) | Read-only audit for ambiguity, contradiction, undefined terms and weak modals |
| [`waterfall/09-use-case-modeling`](../02-requirements-engineering/waterfall/09-use-case-modeling/SKILL.md) | Actor-goal use cases with flows, exceptions, postconditions and trace links |

## Design documentation

Folder `03-design-documentation`, 18 skills.

| Skill | What it does |
|---|---|
| [`01-high-level-design`](../03-design-documentation/01-high-level-design/SKILL.md) | System architecture, critical flows, deployment and ADRs; as-built recovery from code |
| [`02-low-level-design`](../03-design-documentation/02-low-level-design/SKILL.md) | Module, class, sequence, state, algorithm and error contracts from an approved HLD |
| [`03-api-specification`](../03-design-documentation/03-api-specification/SKILL.md) | Versioned API contract with schemas, authentication, errors, idempotency and OpenAPI |
| [`04-database-design`](../03-design-documentation/04-database-design/SKILL.md) | Entity model, normalised schema, keys, indexes, tenancy, retention and migrations |
| [`05-ux-specification`](../03-design-documentation/05-ux-specification/SKILL.md) | Information architecture, interaction states, accessibility and usability evidence |
| [`06-infrastructure-design`](../03-design-documentation/06-infrastructure-design/SKILL.md) | Infrastructure design where availability, scale or recovery exceed the HLD |
| [`07-iot-system-design`](../03-design-documentation/07-iot-system-design/SKILL.md) | Device, gateway and edge design: connectivity, identity, safety and fleet operations |
| [`08-engineering-strategy-brief`](../03-design-documentation/08-engineering-strategy-brief/SKILL.md) | Diagnosis, guiding policies, ADR agenda and sequence for major design work |
| [`09-ux-content-and-form-specification`](../03-design-documentation/09-ux-content-and-form-specification/SKILL.md) | Labels, microcopy, forms, validation, errors and empty states |
| [`10-saas-multi-tenancy-architecture-spec`](../03-design-documentation/10-saas-multi-tenancy-architecture-spec/SKILL.md) | Control and application planes, tenancy patterns, isolation and cost attribution |
| [`11-ai-architecture-spec`](../03-design-documentation/11-ai-architecture-spec/SKILL.md) | Direct call, RAG, fine-tune or agent decisions with gateway, evaluation and security |
| [`12-ai-model-card`](../03-design-documentation/12-ai-model-card/SKILL.md) | Version-specific model card: data, evaluation, limitations, bias and intended use |
| [`13-ai-prompt-and-system-message-spec`](../03-design-documentation/13-ai-prompt-and-system-message-spec/SKILL.md) | Prompt registry, change control, regression evaluation and rollback |
| [`14-ai-agent-architecture-spec`](../03-design-documentation/14-ai-agent-architecture-spec/SKILL.md) | Agent runtime loop, state machine, memory tiers, dispatcher and kill switch |
| [`15-ai-agent-multi-agent-coordination-spec`](../03-design-documentation/15-ai-agent-multi-agent-coordination-spec/SKILL.md) | Multi-agent topology, roles, supervision, message contract and failure handling |
| [`16-accounting-engine-design`](../03-design-documentation/16-accounting-engine-design/SKILL.md) | Append-only journals, posting service, periods, reversals and audit trail |
| [`17-game-system-architecture-specification`](../03-design-documentation/17-game-system-architecture-specification/SKILL.md) | Game client, authoritative state, backend, saves, platforms and live-operations architecture |
| [`18-game-3d-content-and-blender-pipeline-specification`](../03-design-documentation/18-game-3d-content-and-blender-pipeline-specification/SKILL.md) | 3D asset and Blender-to-engine pipeline: rigs, LODs, export and runtime budgets |

## Development artefacts

Folder `04-development-artifacts`, 6 skills.

| Skill | What it does |
|---|---|
| [`01-technical-specification`](../04-development-artifacts/01-technical-specification/SKILL.md) | Module contracts, interfaces, data schemas and requirement traceability |
| [`02-coding-guidelines`](../04-development-artifacts/02-coding-guidelines/SKILL.md) | Language and framework conventions with enforceable checks and exceptions |
| [`03-dev-environment-setup`](../04-development-artifacts/03-dev-environment-setup/SKILL.md) | Repeatable prerequisites, installation, configuration, build and verification |
| [`04-contribution-guide`](../04-development-artifacts/04-contribution-guide/SKILL.md) | Branching, commits, pull requests, review gates and CI expectations |
| [`05-ai-agent-coding-guidelines-addendum`](../04-development-artifacts/05-ai-agent-coding-guidelines-addendum/SKILL.md) | Agent coding rules: tool schemas, reversibility, idempotency, timeouts and HITL gates |
| [`05-game-technical-implementation-specification`](../04-development-artifacts/05-game-technical-implementation-specification/SKILL.md) | Implementable Unity, Godot, Unreal or Apple-native work packages |

## Testing documentation

Folder `05-testing-documentation`, 10 skills.

| Skill | What it does |
|---|---|
| [`01-test-strategy`](../05-testing-documentation/01-test-strategy/SKILL.md) | Risk-based test levels, types, environments, tooling and entry/exit criteria |
| [`02-test-plan`](../05-testing-documentation/02-test-plan/SKILL.md) | Detailed test cases, data, schedule, ownership, traceability and exit evidence |
| [`03-test-report`](../05-testing-documentation/03-test-report/SKILL.md) | Executed results, defects, coverage, residual risk and release recommendation |
| [`04-ai-eval-harness-spec`](../05-testing-documentation/04-ai-eval-harness-spec/SKILL.md) | Reusable AI evaluation harness: datasets, graders, thresholds and regression gates |
| [`05-ai-red-team-test-plan`](../05-testing-documentation/05-ai-red-team-test-plan/SKILL.md) | Red-team plan for prompt injection, unsafe output, privacy, bias and abuse |
| [`06-ai-agent-eval-spec`](../05-testing-documentation/06-ai-agent-eval-spec/SKILL.md) | Agent evaluation for task success, tool selection, budgets and recovery |
| [`07-ai-agent-red-team-test-plan`](../05-testing-documentation/07-ai-agent-red-team-test-plan/SKILL.md) | Agent red-team plan for action abuse, privilege escalation and memory poisoning |
| [`08-accounting-engine-test-plan`](../05-testing-documentation/08-accounting-engine-test-plan/SKILL.md) | Ledger invariants, posting, reversal, period control and reconciliation tests |
| [`09-game-test-and-player-evidence-plan`](../05-testing-documentation/09-game-test-and-player-evidence-plan/SKILL.md) | Game QA, playtesting, balance, performance, accessibility and certification evidence |
| [`10-full-coverage-saas-seeding`](../05-testing-documentation/10-full-coverage-saas-seeding/SKILL.md) | Realistic synthetic SaaS demo data and workflow test coverage |

## Deployment and operations

Folder `06-deployment-operations`, 23 skills.

| Skill | What it does |
|---|---|
| [`01-deployment-guide`](../06-deployment-operations/01-deployment-guide/SKILL.md) | Release prerequisites, migration choreography, verification and rollback |
| [`02-runbook`](../06-deployment-operations/02-runbook/SKILL.md) | Service diagnosis, mitigation, recovery, escalation and verification |
| [`03-monitoring-setup`](../06-deployment-operations/03-monitoring-setup/SKILL.md) | Service indicators, dashboards, alerts, ownership and runbook links |
| [`04-infrastructure-docs`](../06-deployment-operations/04-infrastructure-docs/SKILL.md) | Topology, environments, dependencies, configuration ownership and recovery |
| [`05-go-live-readiness`](../06-deployment-operations/05-go-live-readiness/SKILL.md) | Evidence-based release gates, waivers, rollback readiness and launch decision |
| [`06-customer-adoption-and-support-plan`](../06-deployment-operations/06-customer-adoption-and-support-plan/SKILL.md) | Onboarding, training, support readiness, escalation and adoption measures |
| [`07-saas-tenant-lifecycle-runbook`](../06-deployment-operations/07-saas-tenant-lifecycle-runbook/SKILL.md) | Tenant provisioning, suspension, export, deletion and isolation evidence |
| [`08-saas-slo-and-error-budget-doc`](../06-deployment-operations/08-saas-slo-and-error-budget-doc/SKILL.md) | SaaS SLIs, error budgets, burn alerts and response policy |
| [`09-saas-incident-response-and-postmortem`](../06-deployment-operations/09-saas-incident-response-and-postmortem/SKILL.md) | Incident command, containment, communication and blameless postmortems |
| [`10-ai-hallucination-slo-doc`](../06-deployment-operations/10-ai-hallucination-slo-doc/SKILL.md) | SLO for factuality, citation validity, abstention and release response |
| [`11-ai-feature-rollout-runbook`](../06-deployment-operations/11-ai-feature-rollout-runbook/SKILL.md) | Staged AI feature rollout with evaluation gates and rollback triggers |
| [`12-ai-cost-runbook`](../06-deployment-operations/12-ai-cost-runbook/SKILL.md) | AI cost signals, budgets, attribution, anomaly response and containment |
| [`13-ai-agent-slo-doc`](../06-deployment-operations/13-ai-agent-slo-doc/SKILL.md) | Agent SLOs for task success, safe actions, intervention, budget and latency |
| [`13-ai-incident-severity-matrix`](../06-deployment-operations/13-ai-incident-severity-matrix/SKILL.md) | AI incident severity criteria, escalation, containment and notification |
| [`14-ai-agent-runbook`](../06-deployment-operations/14-ai-agent-runbook/SKILL.md) | Agent health, pauses, retries, replay, tool failures and operator authority |
| [`14-ai-incident-response-runbook`](../06-deployment-operations/14-ai-incident-response-runbook/SKILL.md) | AI incident detection, classification, containment, evidence and recovery |
| [`15-ai-agent-rollout-runbook`](../06-deployment-operations/15-ai-agent-rollout-runbook/SKILL.md) | Shadow to supervised to bounded autonomy with action gates and kill switches |
| [`15-ai-rca-taxonomy-doc`](../06-deployment-operations/15-ai-rca-taxonomy-doc/SKILL.md) | Stable AI failure families, tags, detection links and mitigations |
| [`16-ai-incident-postmortem-template`](../06-deployment-operations/16-ai-incident-postmortem-template/SKILL.md) | Source-attributed AI incident timeline, causes, actions and publication decision |
| [`17-ai-incident-evidence-pack-spec`](../06-deployment-operations/17-ai-incident-evidence-pack-spec/SKILL.md) | AI incident evidence capture, chain of custody, retention and redaction |
| [`20-ai-agent-compliance-runbook`](../06-deployment-operations/20-ai-agent-compliance-runbook/SKILL.md) | Agent control testing, evidence collection, drills and audit-window operations |
| [`21-accounting-operations-runbook`](../06-deployment-operations/21-accounting-operations-runbook/SKILL.md) | Opening balances, close, ledger integrity, reconciliation incidents and rebuilds |
| [`22-game-release-and-live-operations-runbook`](../06-deployment-operations/22-game-release-and-live-operations-runbook/SKILL.md) | Game builds, signing, staged rollout, rollback, live events and economy controls |

## Agile artefacts

Folder `07-agile-artifacts`, 5 skills.

| Skill | What it does |
|---|---|
| [`01-sprint-planning`](../07-agile-artifacts/01-sprint-planning/SKILL.md) | Sprint goal, evidence-based capacity, selected backlog and delivery risks |
| [`02-definition-of-done`](../07-agile-artifacts/02-definition-of-done/SKILL.md) | Observable completion criteria for code, tests, documentation and deployment |
| [`03-definition-of-ready`](../07-agile-artifacts/03-definition-of-ready/SKILL.md) | Evidence a backlog item needs before sprint commitment |
| [`04-retrospective-template`](../07-agile-artifacts/04-retrospective-template/SKILL.md) | Retrospective that turns evidence into owned, time-bound actions |
| [`05-saas-growth-experiment-doc`](../07-agile-artifacts/05-saas-growth-experiment-doc/SKILL.md) | Experiment with hypothesis, primary metric, guardrails, stop rule and decision rule |

## End-user documentation

Folder `08-end-user-documentation`, 9 skills.

| Skill | What it does |
|---|---|
| [`01-user-manual`](../08-end-user-documentation/01-user-manual/SKILL.md) | Role-based, task-oriented operating guidance for an implemented product |
| [`02-installation-guide`](../08-end-user-documentation/02-installation-guide/SKILL.md) | Verified prerequisites, installation, configuration, upgrade and uninstall |
| [`03-faq`](../08-end-user-documentation/03-faq/SKILL.md) | Evidence-backed recurring questions as concise, linked answers |
| [`04-release-notes`](../08-end-user-documentation/04-release-notes/SKILL.md) | Version delta: features, fixes, breaking changes, migration and known issues |
| [`05-saas-customer-success-playbook`](../08-end-user-documentation/05-saas-customer-success-playbook/SKILL.md) | Health scoring, intervention plays, QBRs, renewal and expansion |
| [`06-saas-onboarding-journey-spec`](../08-end-user-documentation/06-saas-onboarding-journey-spec/SKILL.md) | Aha event, activation milestones, segmented paths and drop-off interventions |
| [`07-saas-lifecycle-email-strategy-doc`](../08-end-user-documentation/07-saas-lifecycle-email-strategy-doc/SKILL.md) | Consent-aware lifecycle email campaigns with triggers, suppression and measures |
| [`08-saas-sales-enablement-doc-pack`](../08-end-user-documentation/08-saas-sales-enablement-doc-pack/SKILL.md) | ICP, discovery, demo, qualification, battlecard and closing material |
| [`09-ai-agent-user-disclosure-pack`](../08-end-user-documentation/09-ai-agent-user-disclosure-pack/SKILL.md) | User-facing disclosure of agent capabilities, limits, data use and escalation |

## Governance and compliance

Folder `09-governance-compliance`, 34 skills.

| Skill | What it does |
|---|---|
| [`01-traceability-matrix`](../09-governance-compliance/01-traceability-matrix/SKILL.md) | Requirements mapped to design, tests, evidence, releases and approvals |
| [`02-audit-report`](../09-governance-compliance/02-audit-report/SKILL.md) | Independent read-only findings with severity, scope limits and corrective actions |
| [`03-compliance-documentation`](../09-governance-compliance/03-compliance-documentation/SKILL.md) | Governed compliance set from verified obligations, controls, owners and evidence |
| [`04-risk-assessment`](../09-governance-compliance/04-risk-assessment/SKILL.md) | Risk identification, analysis, treatment and acceptance with evidence |
| [`05-architecture-decision-records`](../09-governance-compliance/05-architecture-decision-records/SKILL.md) | ADR with context, options, rationale, consequences and supersession path |
| [`05-formal-review-gates`](../09-governance-compliance/05-formal-review-gates/SKILL.md) | Evidence-based lifecycle gates, entry criteria, decision rights and outcomes |
| [`06-ccb-charter`](../09-governance-compliance/06-ccb-charter/SKILL.md) | Change Control Board scope, membership, quorum, decision rights and records |
| [`06-change-impact-analysis`](../09-governance-compliance/06-change-impact-analysis/SKILL.md) | Impact of a proposed change on baselines, design, security, tests, schedule and cost |
| [`07-baseline-delta`](../09-governance-compliance/07-baseline-delta/SKILL.md) | Exact approved differences between controlled baselines |
| [`08-waiver-management`](../09-governance-compliance/08-waiver-management/SKILL.md) | Time-bound exceptions to a requirement or control, from approval to closure |
| [`09-sign-off-ledger`](../09-governance-compliance/09-sign-off-ledger/SKILL.md) | Immutable, attributable record of reviews, approvals and conditions |
| [`10-evidence-pack-builder`](../09-governance-compliance/10-evidence-pack-builder/SKILL.md) | Indexed, integrity-checked evidence for a review, audit or release decision |
| [`11-saas-data-isolation-evidence-pack`](../09-governance-compliance/11-saas-data-isolation-evidence-pack/SKILL.md) | Proof of tenant isolation across identity, data, storage, cache and backups |
| [`12-saas-trust-center-document-pack`](../09-governance-compliance/12-saas-trust-center-document-pack/SKILL.md) | Verified customer-facing security, privacy and availability material |
| [`13-saas-dpa-and-privacy-doc-set`](../09-governance-compliance/13-saas-dpa-and-privacy-doc-set/SKILL.md) | Privacy notice, DPA, subprocessor disclosure and data-subject procedures |
| [`14-ai-responsible-ai-declaration`](../09-governance-compliance/14-ai-responsible-ai-declaration/SKILL.md) | Intended use, limits, oversight, evaluation, fairness and accountability of an AI feature |
| [`15-ai-act-and-regulatory-compliance-doc`](../09-governance-compliance/15-ai-act-and-regulatory-compliance-doc/SKILL.md) | AI feature classification against regulatory regimes, obligations and gaps |
| [`16-ai-data-flow-and-dpia`](../09-governance-compliance/16-ai-data-flow-and-dpia/SKILL.md) | AI data flows and privacy impact assessment with residual risk |
| [`17-ai-adr-catalogue`](../09-governance-compliance/17-ai-adr-catalogue/SKILL.md) | Catalogue of AI architecture, model, data, evaluation and provider decisions |
| [`18-ai-agent-responsible-ai-addendum`](../09-governance-compliance/18-ai-agent-responsible-ai-addendum/SKILL.md) | Responsible-AI extension for agent autonomy, approval, memory and kill switch |
| [`19-ai-agent-adr-catalogue`](../09-governance-compliance/19-ai-agent-adr-catalogue/SKILL.md) | Agent decisions on autonomy, planners, tools, approvals and audit logs |
| [`20-ai-agent-soc2-control-pack`](../09-governance-compliance/20-ai-agent-soc2-control-pack/SKILL.md) | AI agent mapped to SOC 2 trust-services controls and evidence |
| [`21-ai-agent-iso27001-control-pack`](../09-governance-compliance/21-ai-agent-iso27001-control-pack/SKILL.md) | AI agent mapped to ISO/IEC 27001:2022 and ISO/IEC 42001 controls |
| [`22-ai-agent-hipaa-control-pack`](../09-governance-compliance/22-ai-agent-hipaa-control-pack/SKILL.md) | PHI-touching agent mapped to HIPAA Security Rule safeguards |
| [`23-ai-agent-compliance-policy-pack`](../09-governance-compliance/23-ai-agent-compliance-policy-pack/SKILL.md) | Signed, auditor-readable policies for agent actions, logs and supervision |
| [`24-ai-agent-attestation-preparation-spec`](../09-governance-compliance/24-ai-agent-attestation-preparation-spec/SKILL.md) | Evidence, remediation and rehearsal plan for SOC 2, ISO 27001 or HIPAA review |
| [`25-ai-agent-evidence-pack-spec`](../09-governance-compliance/25-ai-agent-evidence-pack-spec/SKILL.md) | Agent compliance evidence items, sampling, integrity and auditor access |
| [`26-ai-agent-baa-and-data-processing-language`](../09-governance-compliance/26-ai-agent-baa-and-data-processing-language/SKILL.md) | Legal-review-ready BAA or DPA clauses for AI agents |
| [`27-ai-agent-regulator-overlap-mapping`](../09-governance-compliance/27-ai-agent-regulator-overlap-mapping/SKILL.md) | Crosswalk of agent controls and evidence across several regimes |
| [`28-anti-ai-slop`](../09-governance-compliance/28-anti-ai-slop/SKILL.md) | Writing and design discipline applied to every artefact the engine produces |
| [`29-ai-slop-audit`](../09-governance-compliance/29-ai-slop-audit/SKILL.md) | Independent, evidence-backed AI-slop audit with a grade |
| [`30-game-delivery-evidence-and-greenlight-pack`](../09-governance-compliance/30-game-delivery-evidence-and-greenlight-pack/SKILL.md) | Game greenlight, milestone and release evidence without inflated claims |
| [`31-kaizen-engine-and-product-improvement`](../09-governance-compliance/31-kaizen-engine-and-product-improvement/SKILL.md) | Audit and improve the engine or any document it produces |
| [`plan-canvas`](../09-governance-compliance/plan-canvas/SKILL.md) | Anchored human review of a local artefact with an Approve or Request-changes verdict |
