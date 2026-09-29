# SRS Skills Engine

The SRS Skills Engine is a library of 159 skills and a Python validation kernel for software-lifecycle documentation. It covers nine numbered phases, from strategic vision through requirements engineering, design, development, testing, deployment, Agile delivery and end-user documentation to governance and compliance. It produces PRDs, business cases, vision statements, BRDs and IEEE-structured software requirements specifications; high-level and low-level designs, API, database, UX and infrastructure specifications whose diagrams are typed and checked against the requirement registry; test strategies, plans and reports; deployment guides, runbooks and SLO documents; user manuals and release notes; and traceability matrices, ADRs, risk registers, sign-off ledgers and auditor-ready evidence packs. Overlays extend it to SaaS, AI features and agents, embedded accounting, games, hospitality and retail, and eleven domain packs add sector context, among them healthcare, finance, government, agriculture, logistics and Uganda. The kernel checks each project workspace against deterministic phase gates, and a build pipeline renders Mermaid diagrams to captioned figures before Pandoc stitches the Markdown into a styled `.docx`.

The engine follows ISO/IEC/IEEE 29148:2018 for requirements, keeping the IEEE Std 830-1998 layout for SRS structure, and ISO/IEC 25010:2023 for quality attributes. Design work follows ISO/IEC/IEEE 42010 and IEEE Std 1016-2009. Testing and verification follow ISO/IEC/IEEE 29119-3 and IEEE Std 1012-2016, lifecycle processes follow ISO/IEC/IEEE 12207:2017, and user documentation follows ISO/IEC/IEEE 26514. Security and AI governance packs map to ISO/IEC 27001:2022, ISO/IEC 42001, the NIST AI RMF, SOC 2, the HIPAA Security Rule, the EU AI Act and GDPR. API contracts use OpenAPI 3.1 and RFC 9457 problem details, and user interfaces are checked against WCAG 2.2. The engine is for product owners, business analysts, architects, delivery teams, testers, operators and compliance reviewers on waterfall, Agile or hybrid projects. It records missing stakeholder decisions as open questions rather than inventing requirements. It supports engineering, legal and compliance work but does not replace any of them.

## Installation

Prerequisites:

- Git, and Python 3.11 or later for the validation kernel (`pyproject.toml`).
- Node.js 18 or later for the scripted installers (`install.sh`, `install.ps1`).
- For `.docx` builds: Pandoc, plus a local Chrome or Edge for the pinned Mermaid renderer in `scripts/diagram-render` (install it once with `npm ci` and `PUPPETEER_SKIP_DOWNLOAD=1`).

**Claude Code plugin.** The repository ships a marketplace manifest (`.claude-plugin/marketplace.json`, marketplace `chwezi-srs`, plugin `srs`):

```text
/plugin marketplace add https://github.com/peterbamuhigire/srs-skills
/plugin install srs@chwezi-srs
```

**Scripted install.** The installers delegate to `scripts/install-engine.js`. User scope (`~/.claude`) is the default, `--scope project` installs into `.claude` under the current directory, and `--dry-run` prints the plan without writing anything:

```sh
git clone https://github.com/peterbamuhigire/srs-skills
cd srs-skills
./install.sh --scope project       # macOS, Linux or Git Bash
.\install.ps1 --scope project      # Windows PowerShell
```

**Codex.** Codex reads `AGENTS.md` as the router. The Codex-only model policy check lives in `.codex/`. Run `python <engine-root>/.codex/ensure_model_policy.py --runtime codex --check`, and run `--apply` only when the check reports drift. Claude skips this step.

**Manual route.** Clone the repository, read `CLAUDE.md`, which is a thin bridge to `AGENTS.md`, then open the `SKILL.md` for the phase and task in hand. To start a project workspace and validate it:

```sh
pip install -e ".[dev]"
python -m engine doctor
python -m engine new-project Acme --methodology waterfall --domain healthcare
python -m engine validate projects/Acme
```

`--methodology` accepts `waterfall`, `agile` or `hybrid`. `--example uganda-public-sector` copies the shipped example from `templates/project-examples/`.

[`SETUP_GUIDE.md`](SETUP_GUIDE.md) covers provisioning a separate project repository.

## Capabilities

Generated from the `SKILL.md` frontmatter on disk. Skill paths are relative to the category folder. Requirements engineering nests `agile/`, `fundamentals/`, `hybrid/` and `waterfall/` subfolders. The skeleton in `templates/skill/` is excluded.

| Category (folder) | Skills |
|---|---:|
| Strategic vision (`01-strategic-vision`) | 13 |
| Requirements engineering (`02-requirements-engineering`) | 41 |
| Design documentation (`03-design-documentation`) | 18 |
| Development artefacts (`04-development-artifacts`) | 6 |
| Testing documentation (`05-testing-documentation`) | 10 |
| Deployment and operations (`06-deployment-operations`) | 23 |
| Agile artefacts (`07-agile-artifacts`) | 5 |
| End-user documentation (`08-end-user-documentation`) | 9 |
| Governance and compliance (`09-governance-compliance`) | 34 |
| **Total** | **159** |

| Category | Skill | What it does |
|---|---|---|
| Strategic vision | `01-prd-generation` | Traceable PRD: objectives, prioritised features, success measures and release scope |
| Strategic vision | `02-business-case` | Business case with costs, benefits, ROI, payback, NPV, sensitivity and a go/no-go call |
| Strategic vision | `03-vision-statement` | Strategic north star: target users, problem, differentiated value and scope limits |
| Strategic vision | `04-lean-canvas` | Lean Canvas, Impact Map and Hypothesis Board for untested assumptions |
| Strategic vision | `05-system-overview` | Plain-language system purpose, context, major functions, constraints and actors |
| Strategic vision | `06-ai-economic-value-brief` | Outcome, data-readiness, cost and risk brief for an AI proposal before PRD work |
| Strategic vision | `07-premium-product-positioning` | Case for premium pricing through buyer trust, proof and service quality |
| Strategic vision | `10-saas-mvp-scoping-doc` | Bounded SaaS v1 with one channel, explicit cuts and a feature-triage log |
| Strategic vision | `11-saas-moat-and-defensibility-plan` | Evidence-based SaaS defensibility plan separating real from false moats |
| Strategic vision | `12-saas-pricing-and-packaging-spec` | SaaS tiers, value metric, feature gates, expansion and price-change policy |
| Strategic vision | `13-ai-feature-strategy-doc` | Choose, tier and sequence AI features; build versus buy and AI moat |
| Strategic vision | `14-ai-agent-strategy-doc` | Agent-versus-workflow decision, autonomy levels and capability sequencing |
| Strategic vision | `15-game-product-and-production-brief` | Game player promise, platforms, production model and greenlight decision |
| Requirements engineering | `13-saas-billing-and-metering-spec` | SaaS usage events, billing, credits, refunds, dunning and metering controls |
| Requirements engineering | `14-ai-feature-prd-spec` | Testable AI feature requirements for quality, latency, cost, citations and consent |
| Requirements engineering | `15-ai-data-and-knowledge-base-spec` | AI knowledge sources, ingestion, tenant isolation, freshness, retention and lineage |
| Requirements engineering | `16-ai-agent-feature-prd-spec` | Agent task scope, autonomy, budgets, intervention and irreversible-action gates |
| Requirements engineering | `17-ai-agent-action-catalogue-spec` | Schema-bound agent tools with side effects, approvals, audit fields and kill switches |
| Requirements engineering | `18-embedded-accounting-engine-srs` | Requirements for software that touches money, inventory value, payroll, tax or reports |
| Requirements engineering | `19-game-software-requirements-specification` | Testable game requirements (GREQ): loop, saves, multiplayer, monetisation, certification |
| Requirements engineering | `agile/01-user-story-generation` | INVEST user stories, epics, story points and initial acceptance criteria |
| Requirements engineering | `agile/02-acceptance-criteria` | Deterministic Given-When-Then acceptance criteria for existing stories |
| Requirements engineering | `agile/03-story-mapping` | Story map with user activities, walking skeleton and release slices |
| Requirements engineering | `agile/04-backlog-prioritization` | MoSCoW and WSJF ranking with release or sprint order |
| Requirements engineering | `fundamentals/after/08-requirements-management` | Baselines, change control, versions and impact after requirements exist |
| Requirements engineering | `fundamentals/after/09-traceability-engineering` | Forward and backward links from goals to requirements, design, code, tests and evidence |
| Requirements engineering | `fundamentals/after/10-requirements-metrics` | Quantitative quality gates for ambiguity, completeness, traceability and volatility |
| Requirements engineering | `fundamentals/after/11-requirements-reuse` | Curated reusable requirement patterns and product-line variants |
| Requirements engineering | `fundamentals/after/12-solution-evaluation-and-transition` | Adoption, transition, go/no-go evidence and post-implementation evaluation |
| Requirements engineering | `fundamentals/before/01-stakeholder-analysis` | Stakeholder identification, influence, interests, decision rights and communication |
| Requirements engineering | `fundamentals/before/02-elicitation-toolkit` | Select and run interviews, workshops, observation, surveys and prototypes |
| Requirements engineering | `fundamentals/before/03-brd-generation` | Business Requirements Document bridging strategy and detailed requirements |
| Requirements engineering | `fundamentals/before/04-business-analysis-planning` | Business-analysis governance, decision rights, cadence and artefact plan |
| Requirements engineering | `fundamentals/during/04-requirements-analysis` | Classify, reconcile, prioritise and test the feasibility of elicited requirements |
| Requirements engineering | `fundamentals/during/05-conceptual-data-modeling` | Conceptual entities, relationships and invariants; data contracts and dictionaries |
| Requirements engineering | `fundamentals/during/06-requirements-patterns` | Decision tables, state transitions, CRUD matrices and requirement patterns |
| Requirements engineering | `fundamentals/during/07-requirements-validation` | Independent review for correctness, consistency, feasibility and testability |
| Requirements engineering | `fundamentals/during/08-business-process-modeling` | As-is and to-be workflows, handoffs, controls and exceptions |
| Requirements engineering | `fundamentals/during/09-business-rules-analysis` | Policies, calculations, eligibility, constraints, ownership and effective dates |
| Requirements engineering | `fundamentals/during/10-prototyping-and-solution-discovery` | Compare solution candidates or prototypes before locking requirements |
| Requirements engineering | `fundamentals/during/11-experience-mapping-requirements` | Turn customer, employee or ecosystem journeys into traceable requirements |
| Requirements engineering | `fundamentals/during/12-service-blueprint-requirements` | Service blueprint to frontstage, backstage, support and recovery requirements |
| Requirements engineering | `hospitality-operating-model-srs` | Requirements for hotel, lodge, restaurant, bar, catering and venue systems |
| Requirements engineering | `hybrid/hybrid-synchronization` | Keep Water-Scrum-Fall backlog, DoR/DoD and evidence tied to the approved baseline |
| Requirements engineering | `retail-operating-model-srs` | Retail, POS, pricing, promotions, fulfilment, returns and store-operations requirements |
| Requirements engineering | `waterfall/01-initialize-srs` | Create a Waterfall SRS workspace with IEEE structure, identifiers and source context |
| Requirements engineering | `waterfall/02-context-engineering` | System boundary, actors, external systems, interfaces and assumptions |
| Requirements engineering | `waterfall/03-descriptive-modeling` | Scenarios, flows, states, activities and domain views |
| Requirements engineering | `waterfall/04-interface-specification` | User, software, hardware, communication and external interfaces |
| Requirements engineering | `waterfall/05-feature-decomposition` | Scope to capabilities, features and atomic, traceable requirements |
| Requirements engineering | `waterfall/06-logic-modeling` | Decisions, calculations, state transitions, constraints and exception logic |
| Requirements engineering | `waterfall/07-attribute-mapping` | Measurable non-functional requirements (SRS 3.3-3.6) against ISO/IEC 25010 |
| Requirements engineering | `waterfall/08-semantic-auditing` | Read-only audit for ambiguity, contradiction, undefined terms and weak modals |
| Requirements engineering | `waterfall/09-use-case-modeling` | Actor-goal use cases with flows, exceptions, postconditions and trace links |
| Design documentation | `01-high-level-design` | System architecture, critical flows, deployment and ADRs; as-built recovery from code |
| Design documentation | `02-low-level-design` | Module, class, sequence, state, algorithm and error contracts from an approved HLD |
| Design documentation | `03-api-specification` | Versioned API contract with schemas, authentication, errors, idempotency and OpenAPI |
| Design documentation | `04-database-design` | Entity model, normalised schema, keys, indexes, tenancy, retention and migrations |
| Design documentation | `05-ux-specification` | Information architecture, interaction states, accessibility and usability evidence |
| Design documentation | `06-infrastructure-design` | Infrastructure design where availability, scale or recovery exceed the HLD |
| Design documentation | `07-iot-system-design` | Device, gateway and edge design: connectivity, identity, safety and fleet operations |
| Design documentation | `08-engineering-strategy-brief` | Diagnosis, guiding policies, ADR agenda and sequence for major design work |
| Design documentation | `09-ux-content-and-form-specification` | Labels, microcopy, forms, validation, errors and empty states |
| Design documentation | `10-saas-multi-tenancy-architecture-spec` | Control and application planes, tenancy patterns, isolation and cost attribution |
| Design documentation | `11-ai-architecture-spec` | Direct call, RAG, fine-tune or agent decisions with gateway, evaluation and security |
| Design documentation | `12-ai-model-card` | Version-specific model card: data, evaluation, limitations, bias and intended use |
| Design documentation | `13-ai-prompt-and-system-message-spec` | Prompt registry, change control, regression evaluation and rollback |
| Design documentation | `14-ai-agent-architecture-spec` | Agent runtime loop, state machine, memory tiers, dispatcher and kill switch |
| Design documentation | `15-ai-agent-multi-agent-coordination-spec` | Multi-agent topology, roles, supervision, message contract and failure handling |
| Design documentation | `16-accounting-engine-design` | Append-only journals, posting service, periods, reversals and audit trail |
| Design documentation | `17-game-system-architecture-specification` | Game client, authoritative state, backend, saves, platforms and live-operations architecture |
| Design documentation | `18-game-3d-content-and-blender-pipeline-specification` | 3D asset and Blender-to-engine pipeline: rigs, LODs, export and runtime budgets |
| Development artefacts | `01-technical-specification` | Module contracts, interfaces, data schemas and requirement traceability |
| Development artefacts | `02-coding-guidelines` | Language and framework conventions with enforceable checks and exceptions |
| Development artefacts | `03-dev-environment-setup` | Repeatable prerequisites, installation, configuration, build and verification |
| Development artefacts | `04-contribution-guide` | Branching, commits, pull requests, review gates and CI expectations |
| Development artefacts | `05-ai-agent-coding-guidelines-addendum` | Agent coding rules: tool schemas, reversibility, idempotency, timeouts and HITL gates |
| Development artefacts | `05-game-technical-implementation-specification` | Implementable Unity, Godot, Unreal or Apple-native work packages |
| Testing documentation | `01-test-strategy` | Risk-based test levels, types, environments, tooling and entry/exit criteria |
| Testing documentation | `02-test-plan` | Detailed test cases, data, schedule, ownership, traceability and exit evidence |
| Testing documentation | `03-test-report` | Executed results, defects, coverage, residual risk and release recommendation |
| Testing documentation | `04-ai-eval-harness-spec` | Reusable AI evaluation harness: datasets, graders, thresholds and regression gates |
| Testing documentation | `05-ai-red-team-test-plan` | Red-team plan for prompt injection, unsafe output, privacy, bias and abuse |
| Testing documentation | `06-ai-agent-eval-spec` | Agent evaluation for task success, tool selection, budgets and recovery |
| Testing documentation | `07-ai-agent-red-team-test-plan` | Agent red-team plan for action abuse, privilege escalation and memory poisoning |
| Testing documentation | `08-accounting-engine-test-plan` | Ledger invariants, posting, reversal, period control and reconciliation tests |
| Testing documentation | `09-game-test-and-player-evidence-plan` | Game QA, playtesting, balance, performance, accessibility and certification evidence |
| Testing documentation | `10-full-coverage-saas-seeding` | Realistic synthetic SaaS demo data and workflow test coverage |
| Deployment and operations | `01-deployment-guide` | Release prerequisites, migration choreography, verification and rollback |
| Deployment and operations | `02-runbook` | Service diagnosis, mitigation, recovery, escalation and verification |
| Deployment and operations | `03-monitoring-setup` | Service indicators, dashboards, alerts, ownership and runbook links |
| Deployment and operations | `04-infrastructure-docs` | Topology, environments, dependencies, configuration ownership and recovery |
| Deployment and operations | `05-go-live-readiness` | Evidence-based release gates, waivers, rollback readiness and launch decision |
| Deployment and operations | `06-customer-adoption-and-support-plan` | Onboarding, training, support readiness, escalation and adoption measures |
| Deployment and operations | `07-saas-tenant-lifecycle-runbook` | Tenant provisioning, suspension, export, deletion and isolation evidence |
| Deployment and operations | `08-saas-slo-and-error-budget-doc` | SaaS SLIs, error budgets, burn alerts and response policy |
| Deployment and operations | `09-saas-incident-response-and-postmortem` | Incident command, containment, communication and blameless postmortems |
| Deployment and operations | `10-ai-hallucination-slo-doc` | SLO for factuality, citation validity, abstention and release response |
| Deployment and operations | `11-ai-feature-rollout-runbook` | Staged AI feature rollout with evaluation gates and rollback triggers |
| Deployment and operations | `12-ai-cost-runbook` | AI cost signals, budgets, attribution, anomaly response and containment |
| Deployment and operations | `13-ai-agent-slo-doc` | Agent SLOs for task success, safe actions, intervention, budget and latency |
| Deployment and operations | `13-ai-incident-severity-matrix` | AI incident severity criteria, escalation, containment and notification |
| Deployment and operations | `14-ai-agent-runbook` | Agent health, pauses, retries, replay, tool failures and operator authority |
| Deployment and operations | `14-ai-incident-response-runbook` | AI incident detection, classification, containment, evidence and recovery |
| Deployment and operations | `15-ai-agent-rollout-runbook` | Shadow to supervised to bounded autonomy with action gates and kill switches |
| Deployment and operations | `15-ai-rca-taxonomy-doc` | Stable AI failure families, tags, detection links and mitigations |
| Deployment and operations | `16-ai-incident-postmortem-template` | Source-attributed AI incident timeline, causes, actions and publication decision |
| Deployment and operations | `17-ai-incident-evidence-pack-spec` | AI incident evidence capture, chain of custody, retention and redaction |
| Deployment and operations | `20-ai-agent-compliance-runbook` | Agent control testing, evidence collection, drills and audit-window operations |
| Deployment and operations | `21-accounting-operations-runbook` | Opening balances, close, ledger integrity, reconciliation incidents and rebuilds |
| Deployment and operations | `22-game-release-and-live-operations-runbook` | Game builds, signing, staged rollout, rollback, live events and economy controls |
| Agile artefacts | `01-sprint-planning` | Sprint goal, evidence-based capacity, selected backlog and delivery risks |
| Agile artefacts | `02-definition-of-done` | Observable completion criteria for code, tests, documentation and deployment |
| Agile artefacts | `03-definition-of-ready` | Evidence a backlog item needs before sprint commitment |
| Agile artefacts | `04-retrospective-template` | Retrospective that turns evidence into owned, time-bound actions |
| Agile artefacts | `05-saas-growth-experiment-doc` | Experiment with hypothesis, primary metric, guardrails, stop rule and decision rule |
| End-user documentation | `01-user-manual` | Role-based, task-oriented operating guidance for an implemented product |
| End-user documentation | `02-installation-guide` | Verified prerequisites, installation, configuration, upgrade and uninstall |
| End-user documentation | `03-faq` | Evidence-backed recurring questions as concise, linked answers |
| End-user documentation | `04-release-notes` | Version delta: features, fixes, breaking changes, migration and known issues |
| End-user documentation | `05-saas-customer-success-playbook` | Health scoring, intervention plays, QBRs, renewal and expansion |
| End-user documentation | `06-saas-onboarding-journey-spec` | Aha event, activation milestones, segmented paths and drop-off interventions |
| End-user documentation | `07-saas-lifecycle-email-strategy-doc` | Consent-aware lifecycle email campaigns with triggers, suppression and measures |
| End-user documentation | `08-saas-sales-enablement-doc-pack` | ICP, discovery, demo, qualification, battlecard and closing material |
| End-user documentation | `09-ai-agent-user-disclosure-pack` | User-facing disclosure of agent capabilities, limits, data use and escalation |
| Governance and compliance | `01-traceability-matrix` | Requirements mapped to design, tests, evidence, releases and approvals |
| Governance and compliance | `02-audit-report` | Independent read-only findings with severity, scope limits and corrective actions |
| Governance and compliance | `03-compliance-documentation` | Governed compliance set from verified obligations, controls, owners and evidence |
| Governance and compliance | `04-risk-assessment` | Risk identification, analysis, treatment and acceptance with evidence |
| Governance and compliance | `05-architecture-decision-records` | ADR with context, options, rationale, consequences and supersession path |
| Governance and compliance | `05-formal-review-gates` | Evidence-based lifecycle gates, entry criteria, decision rights and outcomes |
| Governance and compliance | `06-ccb-charter` | Change Control Board scope, membership, quorum, decision rights and records |
| Governance and compliance | `06-change-impact-analysis` | Impact of a proposed change on baselines, design, security, tests, schedule and cost |
| Governance and compliance | `07-baseline-delta` | Exact approved differences between controlled baselines |
| Governance and compliance | `08-waiver-management` | Time-bound exceptions to a requirement or control, from approval to closure |
| Governance and compliance | `09-sign-off-ledger` | Immutable, attributable record of reviews, approvals and conditions |
| Governance and compliance | `10-evidence-pack-builder` | Indexed, integrity-checked evidence for a review, audit or release decision |
| Governance and compliance | `11-saas-data-isolation-evidence-pack` | Proof of tenant isolation across identity, data, storage, cache and backups |
| Governance and compliance | `12-saas-trust-center-document-pack` | Verified customer-facing security, privacy and availability material |
| Governance and compliance | `13-saas-dpa-and-privacy-doc-set` | Privacy notice, DPA, subprocessor disclosure and data-subject procedures |
| Governance and compliance | `14-ai-responsible-ai-declaration` | Intended use, limits, oversight, evaluation, fairness and accountability of an AI feature |
| Governance and compliance | `15-ai-act-and-regulatory-compliance-doc` | AI feature classification against regulatory regimes, obligations and gaps |
| Governance and compliance | `16-ai-data-flow-and-dpia` | AI data flows and privacy impact assessment with residual risk |
| Governance and compliance | `17-ai-adr-catalogue` | Catalogue of AI architecture, model, data, evaluation and provider decisions |
| Governance and compliance | `18-ai-agent-responsible-ai-addendum` | Responsible-AI extension for agent autonomy, approval, memory and kill switch |
| Governance and compliance | `19-ai-agent-adr-catalogue` | Agent decisions on autonomy, planners, tools, approvals and audit logs |
| Governance and compliance | `20-ai-agent-soc2-control-pack` | AI agent mapped to SOC 2 trust-services controls and evidence |
| Governance and compliance | `21-ai-agent-iso27001-control-pack` | AI agent mapped to ISO/IEC 27001:2022 and ISO/IEC 42001 controls |
| Governance and compliance | `22-ai-agent-hipaa-control-pack` | PHI-touching agent mapped to HIPAA Security Rule safeguards |
| Governance and compliance | `23-ai-agent-compliance-policy-pack` | Signed, auditor-readable policies for agent actions, logs and supervision |
| Governance and compliance | `24-ai-agent-attestation-preparation-spec` | Evidence, remediation and rehearsal plan for SOC 2, ISO 27001 or HIPAA review |
| Governance and compliance | `25-ai-agent-evidence-pack-spec` | Agent compliance evidence items, sampling, integrity and auditor access |
| Governance and compliance | `26-ai-agent-baa-and-data-processing-language` | Legal-review-ready BAA or DPA clauses for AI agents |
| Governance and compliance | `27-ai-agent-regulator-overlap-mapping` | Crosswalk of agent controls and evidence across several regimes |
| Governance and compliance | `28-anti-ai-slop` | Writing and design discipline applied to every artefact the engine produces |
| Governance and compliance | `29-ai-slop-audit` | Independent, evidence-backed AI-slop audit with a grade |
| Governance and compliance | `30-game-delivery-evidence-and-greenlight-pack` | Game greenlight, milestone and release evidence without inflated claims |
| Governance and compliance | `31-kaizen-engine-and-product-improvement` | Audit and improve the engine or any document it produces |
| Governance and compliance | `plan-canvas` | Anchored human review of a local artefact with an Approve or Request-changes verdict |

## Project workspaces, gates and document builds

Each project lives in its own workspace at `projects/<ProjectName>/`. Canonical inputs go in `_context/`, identifiers, baselines, waivers and sign-offs go in `_registry/`, and each phase has its own output folder.

- `python -m engine validate projects/<ProjectName>` runs the phase gates for phases 01 to 09 and the hybrid gate. Every check ID maps to a standard and clause in [`docs/standards-clause-registry.md`](docs/standards-clause-registry.md).
- `python -m engine sync`, `baseline snapshot|diff`, `waive`, `signoff` and `pack` maintain the identifier registry, baselines, time-bound waivers and the sign-off ledger, and assemble an evidence-pack ZIP.
- `python -m engine diagrams validate|generate|manifest|verify-manifest` checks typed diagram IR (`engine/registry/schemas/diagram-ir.schema.json`) against the requirement registry. It then generates Mermaid from the IR and records figure hashes.
- `scripts/build-doc.sh <doc-dir> <output-name>` renders every Mermaid block to a captioned PNG/SVG figure with alt text and a render manifest. It then builds the `.docx` with Pandoc against `templates/reference.docx` and refuses a document that still contains raw Mermaid.
- [`docs/hybrid-operating-model.md`](docs/hybrid-operating-model.md) defines the Water-Scrum-Fall contract for projects that baseline requirements formally and deliver in increments.
- [`docs/regulated-evidence-model.md`](docs/regulated-evidence-model.md) defines the minimum evidence chain, from regulation to audit record, for regulated delivery.

Repository checks: `python -X utf8 scripts/validate_engine.py` (engine contract), `python -m engine validate-skills` (legacy paths) and `python -m pytest` (kernel tests, 90 per cent coverage floor).

## References

Citations only. The engine keeps no book extractions ([retirement record](docs/continuous-improvement/book-extraction-retirement-2026-09-24.md)). Each entry below is cited somewhere in this repository, and the detail given is the detail the repository records.

### Books

- Adzic, Gojko (2012) *Impact Mapping*.
- Adzic, Gojko and Evans *Fifty Quick Ideas to Improve Your User Stories*.
- Adzic, Gojko and Evans *Fifty Quick Ideas to Improve Your Tests*.
- Beyer and Holtzblatt (1997) *Contextual Design*.
- Borges, D. and Campbell, D. (2026, early release) *AI Security Engineering*.
- Branson: UX/UI design guidance (personas, cognitive affordance after Hartson and Pyla); the repository gives no title.
- Brikman (2025) *Fundamentals of DevOps and Software Delivery*.
- ByteByteGo (2024) *System Design – The Big Archive*.
- Cagan, M. (2008) *Inspired: How to Create Products Customers Love*.
- Cassani, Alexio *Code Revealed*.
- Clements and Northrop (2001) *Software Product Lines: Practices and Patterns*.
- Cockburn: actor classification for use cases; the repository gives no title.
- Cohn, Mike (2004) *User Stories Applied*.
- Cotton (2020) *How to Run a SaaS Business*.
- DAMA International (2017) *DMBOK*.
- Day (2024, early release) *Hands-On APIs for AI and Data Science*.
- Deacon: UX and UI strategy (three levels of UX scope); the repository gives no title.
- Diamond, Stephanie *Claude For Dummies*.
- Dynowski and Dulak (2025) *Learning API Styles*.
- Garbugli (2017) *SaaS Email Marketing Playbook*.
- Geewax, JJ (2021) *API Design Patterns*, Manning.
- Golding, Tod (2024) *Building Multi-Tenant SaaS Architectures*, O'Reilly.
- Gujral, Rana *The AI Instinct*.
- Hodjat, B. and Blondeau, A. (2026, early release) *The Agentic Enterprise*.
- Holt *Modern Data Systems*.
- Hoskins *The Product-Minded Engineer*.
- Johnson (2025) *Practical JSON Design and Usage*.
- Jones (2023) *Driving Data Quality with Data Contracts*.
- Kang et al. (1990) *Feature-Oriented Domain Analysis (FODA)*.
- Khan, A. (2026, early release) *AI Product Management*.
- Kohavi, Tang and Xu (2020) *Trustworthy Online Controlled Experiments*.
- Krone, Megan *Navigating the Dissertation Writing Process*.
- Laplante *Requirements Engineering for Software and Systems*.
- Leffingwell *Agile Software Requirements*.
- Levy (2021) *UX Strategy*, 2nd ed.
- Marchiotto, A. (2025) *Adopting AI for Business Transformation*.
- Maurya, Ash *Running Lean*.
- Mersch (2023) *Hacking SaaS*.
- Mohan, Sanjeev *Designing the AI-Driven Data Foundations*.
- Moore, Geoffrey: product positioning template; the repository gives no title.
- Nassery (2025) *Next-Level A/B Testing*.
- Nordic APIs *Identity and APIs*.
- Olesen-Bagneux (2023) *The Enterprise Data Catalog*, and the second edition (early release).
- Osterwalder and Pigneur *Business Model Generation*.
- Patton, Jeff (2014) *Story Mapping*.
- PMI *Business Analysis for Practitioners* (PMI Business Analysis Practice Guide).
- Pohl, Bockle and van der Linden (2005) *Software Product Line Engineering: Foundations, Principles, and Techniques*.
- Ries, Eric *The Lean Startup*.
- Robertson, Suzanne and Robertson, James *Mastering the Requirements Process* (Volere).
- Rubinelli, Sara *Institutional Health Communication in the Information Age*.
- Shneiderman and Plaisant (2016) *Designing the User Interface: Strategies for Effective Human-Computer Interaction*, 6th ed.
- *Software Requirements Essentials*, cited as "Wiegers & Beatty (RE Essentials)" and as numbered Wiegers practices 1 to 20.
- Thompson (2025) *Designing Digital Solutions*, BCS.
- Walling (2022) *SaaS Playbook*.
- Whitten and Bentley (2007) *Systems Analysis and Design Methods*.
- Wiegers, Karl and Beatty, Joy *Software Requirements*, 3rd ed.
- Winning by Design *SaaS Sales Method Fundamentals* and *SaaS Sales Method for Account Executives*.
- Wu and Liang (eds.) (2026) *Human-AI Interaction and Collaboration*, Cambridge University Press.
- Ximenes, F. (2024) *Strategic Software Engineering: Software Engineering Beyond the Code*.

The dated reading lists ([2026-04-12](docs/evaluation/2026-04-12/suggested-reading.md), [July 2026](docs/engine-upgrade-july-2026/05-reading-list.md)) also name the following. They are recommendations; no skill cites them: Stellman and Greene, *Writing Software Requirements Specifications*; Gottesdiener, *The Software Requirements Memory Jogger*; Myers et al., *The Art of Software Testing*; Erder, Pureur and Woods, *Continuous Architecture in Practice*; Bass, Clements and Kazman, *Software Architecture in Practice*; Nygard, *Release It!*; Forsgren, Humble and Kim, *Accelerate*; Adzic, *Specification by Example*; Gentle, *Docs Like Code*; Fowler, *Patterns of Enterprise Application Architecture*.

### Repositories

- Archify — https://github.com/tt-a1i/archify — MIT — commit `0e4949f910a8e390bd3b4933883a4dcabad571be`. Adapted the pattern for typed diagram IR, closed-world trace checks, candidate freezing, render receipts, the `.docx` build guard, finding diagnostics and the stable-ID baseline delta. Rebuilt in Python and paraphrased (my-10-kaizen M10-07, M10-01).
- Graphify — https://github.com/Graphify-Labs/graphify — Apache-2.0 — commit `d6eaa8aae8df155874ebb1044302c055c286342a`. Adapted the EXTRACTED/INFERRED/AMBIGUOUS provenance tags for as-built design recovery. Not a dependency (M10-08).
- Understand Anything — https://github.com/Egonex-AI/Understand-Anything — MIT — commit `b05cc3b20990afca537b4fc0a49b4d7fbdc65bb0`. Adapted the system orientation outline, walkthrough ordering and the commit-pinned generation-staleness gate (M10-08).
- Superpowers — https://github.com/obra/superpowers — MIT — commit `8ca22dba9a94f28898bbce59f2537ff4d87c747d`. Adapted ceremony classification, section-scoped approval and Review Focus. Superpowers is no longer a mandatory step (M10-08).
- Addy Osmani agent-skills — https://github.com/addyosmani/agent-skills — MIT — commit `2686b62`. Adapted the six-area agent build brief and the owned-negative pairwise routing tests (M10-03, M10-08).
- UI UX Pro Max — https://github.com/nextlevelbuilder/ui-ux-pro-max-skill — MIT — commit `09170eec67eefd46a7ae85de61b40c194020f997`. Adapted abstaining lexical retrieval for `engine controls search`. None of its data was reused (M10-08).
- Impeccable — https://github.com/pbakaus/impeccable — Apache-2.0. Source of the AS1–AS7 anti-slop overlay applied in `28-anti-ai-slop` and `29-ai-slop-audit`.
- pypict-claude-skill — https://github.com/omkamal/pypict-claude-skill — MIT — commit `fbda212bca79dfa7611be12527b102c89cc8faeb`. Pairwise combinatorial test design method (test plan reference).
- Microsoft PICT — https://github.com/microsoft/pict — MIT — commit `ab76c2548f551fcb46314e58653a1bd1172f3a72`. Pairwise combinatorial test design method.
- Matt Pocock skills — `mattpocock/skills` at commit `3cca18b` (the repository records no licence). Adapted the persistent domain-context and decision-frontier mechanisms.
- ECC — https://github.com/affaan-m/ECC (the repository records no licence). Plan Canvas review tool, the Git Bash path fix in `install.sh`, the acceptance-criteria "Must not" field, requirement provenance tagging, ADR decision-moment capture and the agent runtime safety guides.
- codex-astra-luna-orchestrator — https://github.com/donvito/codex-astra-luna-orchestrator — commit `21f4561656a1b8f2813828520357e3cd1785d50f`. Concept reference for the Codex model policy. Implemented independently.
- Companion Chwezi engines, routed to rather than copied: https://github.com/peterbamuhigire/chwezi-dev-engine, https://github.com/peterbamuhigire/chwezi-accounting-doctrine and https://github.com/peterbamuhigire/digital-research-skills.

The my-10-kaizen study also covered Ponytail, Caveman and Awesome Claude Skills. This engine adopted nothing from them.

### Standards and official sources

- Requirements: ISO/IEC/IEEE 29148:2018; IEEE Std 830-1998 (superseded, kept for SRS layout); IEEE Std 1233-1998; ISO/IEC/IEEE 24765 and IEEE Std 610.12-1990 (vocabulary).
- Quality: ISO/IEC 25010:2023, ISO/IEC 25019:2023, ISO/IEC 25023, ISO/IEC 25012:2008, ISO/IEC 25051, ISO/IEC 25062; IEEE Std 982.1-2005.
- Architecture and lifecycle: ISO/IEC/IEEE 42010:2011; IEEE Std 1016-2009; ISO/IEC/IEEE 12207:2017; ISO/IEC/IEEE 15288; IEEE Std 828-2012; IEEE Std 1062-2015; ISO/IEC 14764:2006; ISO/IEC 15504.
- Testing, verification and reviews: ISO/IEC/IEEE 29119-3:2013 and 29119-4; IEEE Std 1012-2016; IEEE Std 1028-2008; IEEE 829.
- User documentation and usability: IEEE Std 26514-2022 (ISO/IEC/IEEE 26514); ISO 9241; WCAG 2.2 (https://www.w3.org/TR/WCAG22/).
- Security, privacy and AI governance: ISO/IEC 27001:2022, ISO/IEC 27002:2022, ISO/IEC 27017, ISO/IEC 27018, ISO/IEC 27035, ISO/IEC 27007, ISO/IEC 17021-1; ISO/IEC 42001:2023; ISO/IEC 23894; ISO 31000:2018; NIST AI RMF (NIST AI 100-1); NIST SP 800-53, 800-61, 800-63 (A and B), 800-57, 800-66, 800-137, 800-161, 800-175B and 800-207; OWASP Top 10, OWASP API Security Top 10, OWASP Top 10 for LLM Applications and the OWASP GenAI Security Project.
- Regulation and assurance: GDPR; EU AI Act; HIPAA Security Rule; SOC 2; PCI DSS; IFRS 15; Uganda Data Protection and Privacy Act, 2019; Nigeria NDPC AI advisory (2024).
- Interfaces and formats: OpenAPI 3.1; RFC 9110, RFC 9457 (formerly RFC 7807), RFC 4918, RFC 7519, RFC 5322, RFC 8594 and RFC 9745; JSON Schema draft 2020-12; SARIF 2.1.0; ISO 8601; ISO 4217; Semantic Versioning 2.0.0 (https://semver.org/spec/v2.0.0.html); Bitol Open Data Contract Standard v3.2.0.
- Domain packs: HL7 FHIR R4 (https://hl7.org/fhir/R4/); GLOBALG.A.P. (https://www.globalgap.org/); Rainforest Alliance (https://www.rainforest-alliance.org/); ISO 22000:2018; ISO 28000; ISO 3779, ISO 3780 and ISO 15031.
- Delivery: DORA and SLSA primary documentation; Google Site Reliability Engineering practice; Pandoc manual (https://pandoc.org/MANUAL.html#option--reference-doc).

### Websites and articles

- Amershi et al. (2019) "Guidelines for Human-AI Interaction", CHI.
- Fabijan et al. (2019) sample ratio mismatch taxonomy, KDD; Microsoft Research, "Diagnosing Sample Ratio Mismatch in A/B Testing".
- Wake, Bill (2003) "INVEST in Good Stories, and SMART Tasks".
- Google PAIR (2021) *People + AI Guidebook*.
- Nielsen Norman Group: usability testing sample-size guidance.
- Eleken: https://www.eleken.co/blog-posts/mobile-app-onboarding-best-practices, https://www.eleken.co/blog-posts/dashboard-design-examples-that-catch-the-eye, https://www.eleken.co/blog-posts/ai-design-workflow, https://www.eleken.co/blog-posts/ux-improvements, https://www.eleken.co/blog-posts/making-it-like-stripe and https://www.eleken.co/blog-posts/how-to-validate-product-ideas.
- Design Studio UI/UX: https://www.designstudiouiux.com/blog/web-app-ui-design-patterns/, https://www.designstudiouiux.com/blog/saas-ux-design-cost/, https://www.designstudiouiux.com/blog/how-to-design-and-build-saas-product/, https://www.designstudiouiux.com/blog/mobile-navigation-ux/, https://www.designstudiouiux.com/blog/mobile-app-onboarding-best-practices/, https://www.designstudiouiux.com/blog/dashboard-ui-design-guide/ and https://www.designstudiouiux.com/blog/mobile-app-design-examples/.
- GOV.UK Service Manual, "Making prototypes": https://www.gov.uk/service-manual/design/making-prototypes.
- Apple Human Interface Guidelines, "Onboarding": https://developer.apple.com/design/human-interface-guidelines/onboarding.
- ECC guides: https://raw.githubusercontent.com/affaan-m/ECC/main/the-shortform-guide.md, https://raw.githubusercontent.com/affaan-m/ECC/main/the-longform-guide.md and https://raw.githubusercontent.com/affaan-m/ECC/main/the-security-guide.md.
- Agent Skills: https://agentskills.io/.
- OpenAI model and image guides used in the model-currentness and prompt-compilation records: https://developers.openai.com/api/docs/models/gpt-6-astra, https://developers.openai.com/api/docs/models/gpt-5.6-sol, https://developers.openai.com/api/docs/models/gpt-5.6-terra, https://developers.openai.com/api/docs/models/gpt-5.6-luna, https://developers.openai.com/api/docs/guides/image-prompting and https://developers.openai.com/api/docs/guides/image-generation.
