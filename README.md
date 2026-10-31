# Chwezi SDLC Documentation

Chwezi SDLC Documentation is a library of 159 skills and a Python validation kernel for software-lifecycle documentation. It covers nine numbered phases, from strategic vision through requirements engineering, design, development, testing, deployment, Agile delivery and end-user documentation to governance and compliance. It produces PRDs, business cases, vision statements, BRDs and IEEE-structured software requirements specifications; high-level and low-level designs, API, database, UX and infrastructure specifications whose diagrams are typed and checked against the requirement registry; test strategies, plans and reports; deployment guides, runbooks and SLO documents; user manuals and release notes; and traceability matrices, ADRs, risk registers, sign-off ledgers and auditor-ready evidence packs. Overlays extend it to SaaS, AI features and agents, embedded accounting, games, hospitality and retail, and eleven domain packs add sector context, among them healthcare, finance, government, agriculture, logistics and Uganda. The kernel checks each project workspace against deterministic phase gates, and a build pipeline renders Mermaid diagrams to captioned figures before Pandoc stitches the Markdown into a styled `.docx`.

The engine follows ISO/IEC/IEEE 29148:2018 for requirements, keeping the IEEE Std 830-1998 layout for SRS structure, and ISO/IEC 25010:2023 for quality attributes. Design work follows ISO/IEC/IEEE 42010 and IEEE Std 1016-2009. Testing and verification follow ISO/IEC/IEEE 29119-3 and IEEE Std 1012-2016, lifecycle processes follow ISO/IEC/IEEE 12207:2017, and user documentation follows ISO/IEC/IEEE 26514. Security and AI governance packs map to ISO/IEC 27001:2022, ISO/IEC 42001, the NIST AI RMF, SOC 2, the HIPAA Security Rule, the EU AI Act and GDPR. API contracts use OpenAPI 3.1 and RFC 9457 problem details, and user interfaces are checked against WCAG 2.2. The engine is for product owners, business analysts, architects, delivery teams, testers, operators and compliance reviewers on waterfall, Agile or hybrid projects. It records missing stakeholder decisions as open questions rather than inventing requirements. It supports engineering, legal and compliance work but does not replace any of them.

## Installation

The GitHub repository is `chwezi-sdlc-documentation`. A checkout made before the rename may still sit in a folder named `srs-skills`. The scripted installer names the installed copy after the checkout folder, so clone into `chwezi-sdlc-documentation`.

Prerequisites:

- Git, and Python 3.11 or later for the validation kernel (`pyproject.toml`). The kernel was last run on Python 3.14.8.
- The pinned Python packages, installed in a virtual environment: `python3 -m pip install -c requirements-ci.txt -e ".[dev,docs]"`. They are `click`, `ruamel.yaml`, `mistune`, `jsonschema`, `pytest`, `pytest-cov` and `python-docx`, at the versions in `requirements-ci.txt`. `scripts/validate_decision_frontier.py` and `tests/agent-integration/test_srs_agent_contract.py` also import `yaml` (`pyyaml`), which that file does not list; install it before running them.
- Node.js 18 or later for the scripted installers (`install.sh`, `install.ps1`) and for the hook and Plan Canvas tests.
- For `.docx` builds: Pandoc, and the `docs` extra for the temporary Word style template. Diagram builds also require a local Chrome or Edge for the pinned Mermaid renderer (`npm ci` in `scripts/diagram-render` with `PUPPETEER_SKIP_DOWNLOAD=1`, and `PUPPETEER_EXECUTABLE_PATH` pointing at the browser). A checked-in or ignored `templates/reference.docx` is optional.

Which checks need which tool:

| Needs | Commands |
|---|---|
| Python 3 and Git only (no third-party package) | `scripts/validate_engine.py`, `scripts/validate_plugin_packages.py`, `scripts/check_portable_paths.py`, `scripts/check_cross_engine_refs.py`, `scripts/check_standards_currency.py`, `scripts/validate_source_register.py`, `scripts/validate_sdd_phase_boundaries.py`, `scripts/validate_requirements_decision.py`, `scripts/source_ingestion_guardrail.py` |
| The pinned packages | `scripts/validate_skill_engine.py` and `scripts/routing_smoke_test.py` (both exit 2 with an install message when `ruamel.yaml` is missing), `scripts/validate_traceability_evidence.py` (`jsonschema`), `scripts/validate_source_reconciliation.py`, every `python3 -m engine` command (`ModuleNotFoundError` when `ruamel.yaml` is missing) and `python3 -m pytest` |
| Node.js 18 or later | `install.sh`, `node hooks/test-destructive-bash-gate.js`, `node hooks/test-plugin-hook-config.js` and the Plan Canvas tests |
| Pandoc | `scripts/build-doc.sh` (exits 1 with "Pandoc is required" when it is missing) and the `.docx` tests, which pytest skips without it |
| Node.js, `npm ci` in `scripts/diagram-render` and a local Chrome or Edge | Mermaid figure rendering inside `scripts/build-doc.sh` |
| PowerShell | `install.ps1`, `scripts/setup-srs-project.ps1` and the `export-docs.ps1` that `new-project` writes into each workspace. No registered check needs it |
| LibreOffice or a container | Nothing in this repository requires either |

Companion engines are resolved through the engine-routing table of the active runner, never through a fixed path. Engineering skills live in `chwezi-dev-engine` (earlier local folder `skills-web-dev`), design and typography in `chwezi-design-engine` (`design-system-skills`), research and currentness in `digital-research-skills` (`chwezi-research-engine`) and finance in `chwezi-accounting-doctrine`. To let `scripts/check_cross_engine_refs.py` resolve category paths, pass `--dev-engine-root <checkout>` or set `CHWEZI_DEV_ENGINE_ROOT`.

**Claude Code plugin.** The repository ships a marketplace manifest (`.claude-plugin/marketplace.json`, marketplace `chwezi-sdlc-documentation`, plugin `sdlc-documentation`):

```text
/plugin marketplace add https://github.com/peterbamuhigire/chwezi-sdlc-documentation
/plugin install sdlc-documentation@chwezi-sdlc-documentation
```

**Codex local marketplace.** From a trusted checkout, add the repo marketplace:

```sh
codex plugin marketplace add .
```

The repo catalogue is `.agents/plugins/marketplace.json`; it points to this
checkout and reuses the Claude-compatible skill manifest. Run
`python3 -X utf8 scripts/validate_plugin_packages.py` to check the local
catalogue, manifest-to-skill parity and package-oriented file count. The check
also reports the full checkout count. It fails if either count is above the
OpenAI ZIP submission ceiling of 5,000 entries, but it does not build
or submit an archive. Public submission and acceptance remain separate steps.

Codex may shorten descriptions or omit skill paths from its initial list when
the installed skills exceed its default context budget. The optional
`skills.max_context_tokens=10000` setting raises the initial-list budget; it
does not load every full skill body. To verify a local runtime, capture only a
sanitised summary of `codex debug prompt-input` and run
`python3 scripts/check_codex_discovery_summary.py --expected-paths 159 <summary.json>`
against it. The summary is a JSON object with `manifest_paths`, `runtime_paths`,
`missing` (an empty list), `network` set to `none`, `model_calls` set to `0` and a
`method` string that contains "offline"; the check exits 1 otherwise. Do not commit the raw
prompt-input dump because it can contain internal instructions. The 10,000-token
budget produced all 159 paths in the offline Codex 0.165.0 check on 2026-10-29;
the default run exposed 108. These are path-discovery counts, not evidence of
correct skill selection or task quality. See
[`docs/kaizen/2026-10-engine-kaizen/04-validation-record.md`](docs/kaizen/2026-10-engine-kaizen/04-validation-record.md).

**Scripted install.** The installers delegate to `scripts/install-engine.js`. User scope (`~/.claude`) is the default, `--scope project` installs into `.claude` under the current directory, and `--dry-run` prints the plan without writing anything. The scripts are tracked without the executable bit, so run them through `bash`; `./install.sh` fails with `Permission denied` on Linux. The installer also takes `uninstall`, `list-installed` and `doctor` (`node scripts/install-engine.js <command>`).

```sh
git clone https://github.com/peterbamuhigire/chwezi-sdlc-documentation
cd chwezi-sdlc-documentation
bash install.sh --scope project --dry-run   # macOS, Linux or Git Bash; drop --dry-run to install
.\install.ps1 --scope project               # Windows PowerShell
```

**Codex.** Codex reads `AGENTS.md` as the router. The Codex-only model policy check lives in `.codex/`. Run `python3 <engine-root>/.codex/ensure_model_policy.py --runtime codex --check`, and run `--apply` only when the check reports drift. The check exits 1 with `DRIFT: Codex config.toml is missing` when no Codex configuration exists. Claude skips this step.

**Manual route.** Clone the repository, read `CLAUDE.md`, which is a thin bridge to `AGENTS.md`, then open the `SKILL.md` for the phase and task in hand. To start a project workspace and validate it:

```sh
python3 -m pip install -c requirements-ci.txt -e ".[dev,docs]"
python3 -m engine doctor
python3 -m engine new-project Acme --methodology waterfall --domain healthcare
python3 -m engine validate projects/Acme
```

`--methodology` accepts `waterfall`, `agile` or `hybrid`. `--example uganda-public-sector` copies the shipped example from `templates/project-examples/`. That example supplies only context and registries, not phase documents.

What these commands print on a clean checkout:

- `doctor` reports `[FAIL] Skills submodule` because it looks for a `skills/` directory in the current folder. That check applies to a project repository that vendors this engine as `skills/` (see [`SETUP_GUIDE.md`](SETUP_GUIDE.md)); it does not apply when you run `doctor` inside the engine checkout. It also reports `[FAIL] Pandoc available` when Pandoc is not on `PATH`. It exits 1 in both cases.
- `validate` on a freshly scaffolded workspace exits 1. A new `healthcare` workspace and a new `uganda-public-sector` workspace each return 22 blocking findings, because the Phase 03 to Phase 09 documents do not exist yet. Exit 0 needs the full document set. To see a passing run, use the seeded demo: `python3 scripts/seed_demo_project.py`, then `python3 -m engine validate projects/_demo-hybrid-regulated` (exit 0).
- When `pip install -e` has not been run, put the checkout first on the import path with `PYTHONPATH=.`. A non-editable copy of `engine` elsewhere in the environment would otherwise be the one that runs.

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

- `python3 -m engine validate projects/<ProjectName>` runs the phase gates for phases 01 to 09 and the hybrid gate. Every check ID maps to a standard and clause in [`docs/standards-clause-registry.md`](docs/standards-clause-registry.md).
- Before Phase 02, copy `02-requirements-engineering/fundamentals/during/04-requirements-analysis/references/source-reconciliation-template.yaml` to `projects/<ProjectName>/_registry/source-reconciliation.yaml`, map each material source statement to a requirement or explicit ambiguity, and run `python3 scripts/validate_source_reconciliation.py projects/<ProjectName>`. The script exits 1 when the register is missing or lists no source statement. The Phase 02 gate in `engine validate` reports unresolved ambiguities as blockers, but a project with no register at all passes that check; whether to require the register is an open owner decision. The check validates the register's links and decisions, not semantic completeness of the source review.
- For a traceability evidence summary, use `references/traceability-evidence.schema.json` and run `python3 scripts/validate_traceability_evidence.py <report.json>`. Goal/design/test links, oracle readiness, owner decisions and executed results are reported separately.
- `python3 -m engine sync`, `baseline snapshot|diff`, `waive`, `signoff` and `pack` maintain the identifier registry, baselines, time-bound waivers and the sign-off ledger, and assemble an evidence-pack ZIP.
- `python3 -m engine diagrams validate|generate|manifest|verify-manifest` checks typed diagram IR (`engine/registry/schemas/diagram-ir.schema.json`) against the requirement registry. It then generates Mermaid from the IR and records figure hashes.
- `bash scripts/build-doc.sh <doc-dir> <output-name>` renders every Mermaid block to a captioned PNG/SVG figure with alt text and a render manifest. It then builds the `.docx` with Pandoc, generating a temporary reference template when `templates/reference.docx` is absent, and refuses a document that still contains raw Mermaid.
- [`docs/hybrid-operating-model.md`](docs/hybrid-operating-model.md) defines the Water-Scrum-Fall contract for projects that baseline requirements formally and deliver in increments.
- [`docs/regulated-evidence-model.md`](docs/regulated-evidence-model.md) defines the minimum evidence chain, from regulation to audit record, for regulated delivery.

## Validation

Run these from the repository root. The results were measured on 31 October 2026 on Python 3.14.8 and Node.js 22, with the packages at the versions in `requirements-ci.txt` except `python-docx`, which was absent. Pandoc, the Mermaid renderer, a browser and PowerShell were also absent. `.github/workflows/engine.yml` runs most of the same commands on Python 3.11 and does not run the Node.js tests. Inside an activated virtual environment `python` and `python3` are the same interpreter.

| Command | Result on 2026-10-31 |
|---|---|
| `python3 -m pytest` | Runs `engine/tests`: 535 passed, 5 skipped, coverage 96.19% against a 90% floor. Four skips need Pandoc, a renderer or a browser; the fifth, in `engine/tests/test_examples_validate.py`, collects no example because it looks in a folder this repository does not contain. |
| `python3 -m pytest tests -o addopts=` | 33 passed. CI runs 19 of them (the routing and Tier-1 lint tests). |
| `python3 -X utf8 scripts/validate_engine.py` | `ENGINE CONTRACT: PASS`. |
| `python3 -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | 159 active skills, 1 template, no failures; 5 report-only size warnings. |
| `python3 -X utf8 scripts/routing_smoke_test.py --min-rank1 83 --lint-fixtures --min-covered 8` | 72 of 72 fixtures in the top three; precision@1 64 of 72 (88.9%); 25 owned negatives, 22 pass and 3 `NOT_ASSESSED` (their owners are in other engines); 8 of 159 skills meet the route-coverage target; fixture lint 0 findings. This is a lexical proxy, not live routing. |
| `python3 -m engine validate-skills` | `SKILLS OK`. |
| `python3 -X utf8 scripts/validate_plugin_packages.py` | 159 active skill paths, `errors: 0`, both file counts under the 5,000 limit. |
| `python3 scripts/check_portable_paths.py` | PASS, 0 findings. |
| `python3 scripts/check_cross_engine_refs.py` | PASS. Category and URL paths are `NOT_ASSESSED` without a dev-engine checkout; with `--dev-engine-root <checkout>` they resolve and the check passes. |
| `python3 scripts/check_standards_currency.py` | PASS: no stale-citation count above its ceiling. |
| `python3 scripts/validate_source_register.py` | PASS: 18 effective records from 2 registers. Date-driven; see the calendar below. |
| `python3 scripts/validate_traceability_evidence.py engine/tests/fixtures/traceability-evidence.json` | Prints the evidence counts and exits 0. |
| `python3 scripts/validate_sdd_phase_boundaries.py --feature-dir engine/tests/fixtures/sdd_feature` | PASS, no boundary findings. |
| `python3 scripts/validate_requirements_decision.py engine/tests/fixtures/requirements_decision/reuse.json` | `"status": "PASS"`. |
| `python3 -X utf8 scripts/source_ingestion_guardrail.py` | `findings: 0`. |
| `python3 scripts/seed_demo_project.py`, then `python3 -m engine validate projects/_demo-hybrid-regulated` | Exit 0. Adding the hidden flag `--break-something` makes the same command exit 1, which CI uses to show the gate can fail. |
| `node hooks/test-destructive-bash-gate.js`, `node hooks/test-plugin-hook-config.js` | 61 of 61 and 7 of 7 passed. |
| `node tests/plan-canvas/markdown.test.js` and the five other files under `tests/plan-canvas`, `tests/hooks` and `tests/scripts` | Plain Node.js scripts: run each with `node <file>`, not `node --test`. 64, 16, 28, 9, 7 and 4 checks pass. |

Not run on that host, so `NOT_ASSESSED`: `bash scripts/build-doc.sh` (Pandoc absent, so it exits 1 with `ERROR: Pandoc is required`), Mermaid figure rendering, the four pytest skips above, `install.ps1` and `scripts/setup-srs-project.ps1` (no PowerShell), and `pip install -e` itself (the environment already held the packages).

## Quality and improvement

The evidence for the October 2026 kaizen cycles is in the repository. [`docs/kaizen/2026-10-engine-kaizen/`](docs/kaizen/2026-10-engine-kaizen/) holds the 29 October cycle and [`docs/kaizen/2026-10-engine-kaizen-pass-2/`](docs/kaizen/2026-10-engine-kaizen-pass-2/) holds the 31 October cycle (pass 2). Each has a scope record, baseline scorecard, backlog, experiment log, validation record, final report, next-cycle notes and a dated source register. Start with `05-final-report.md` and `06-next-cycle.md`. The changes that were kept, with their commits and before-and-after figures, are listed under [What the October 2026 kaizen improved](#what-the-october-2026-kaizen-improved) below. [`docs/README.md`](docs/README.md) indexes the older audits.

**Latest published score:** 55.68 out of 100 raw and 55.68 out of 100 after the portfolio cap of 65, from the pass 2 final report (31 October 2026). The 29 October cycle ended at 53.98. The pass 2 report also states a stricter initial cap of 45, under which the reported value is 45. The score is an unweighted mean of ten reviewer-judged dimensions. It is not a customer outcome and has had no independent acceptance review. The 95 target is not reached.

Open findings that matter when you use the engine:

- A project with no `_registry/source-reconciliation.yaml` still passes the Phase 02 source check, so source-conflict blocking applies only to projects that keep the register.
- Gate clause labels still cite IEEE Std 830-1998 (163 live lines), the 2011 edition of ISO/IEC/IEEE 42010 (13 lines) and the 2013 edition of ISO/IEC/IEEE 29119-3 (11 lines), which their issuers list as superseded or withdrawn. The router treats IEEE 830 as an SRS layout reference only. `scripts/check_standards_currency.py` stops these counts rising; it does not remap clauses.
- Phase 09 does not trace NFR, IR, DR and CON identifiers, and it does not block two definitions of the same identifier.
- Applied proof is thin: 4 of 159 skills have an `examples/` folder, and 44 of the 81 skills with a worked-example section share one of 12 identical paragraphs.
- Routing evidence is lexical. The phrase "software requirements specification" still ranks the game SRS skill first in the proxy, and pass 2 recorded a second near miss for a school-fees prompt. No live-model routing run has been made.
- The education pack is a United States baseline with no school-fees module, and 16 domain-pack lines still target the 2.1 level of the accessibility guidelines, not 2.2, pending a jurisdiction decision.
- The `.docx` build and Mermaid rendering were not assessed on the Linux workstation.
- The per-user settings file `.claude/settings.local.json` is untracked and ignored, but earlier commits on the public history still contain it. Removing it needs a history rewrite, which is a decision for the maintainer.

**Date-triggered gates.** `scripts/validate_source_register.py` fails when a source record has no review date or its review date has passed. Run with `--today YYYY-MM-DD`, it exits as follows:

| Run date | Exit | Findings and the review dates behind them |
|---|---:|---|
| Up to 2026-11-29 | 0 | None. Due-soon notes, which do not fail, start 14 days before a review date, so from 2026-11-15. |
| 2026-11-30 | 1 | 3: OpenAI plugin schema, OpenAI archive limit and Claude marketplace (review 2026-11-29). |
| 2026-12-01 | 1 | 4: adds the Codex skill-list budget (review 2026-11-30). |
| 2027-01-30 | 1 | 8: adds ISO/IEC 25010, Uganda regulations, model catalogue and dev-engine references (review 2027-01-29). |
| 2027-02-01 | 1 | 14: adds ISO/IEC/IEEE 29148, Uganda DPPA, WCAG, Pandoc, Mermaid CLI and dev-engine aliases (review 2027-01-31). |
| 2027-10-30 | 1 | 17: adds ISO/IEC/IEEE 42010, ISO/IEC/IEEE 29119-3 and ISO/IEC/IEEE 26514 (review 2027-10-29). |

To clear a finding, re-verify the claim against its primary source and record it in a newer `docs/kaizen/<cycle>/standards-source-register.md`; a newer record supersedes an older one for the same claim identifier. The pass 2 notes propose the next re-audit for 2026-11-30.

### What the October 2026 kaizen improved

Two kaizen cycles ran on this repository, on 29 October 2026 and on 31 October 2026 (pass 2). This list holds only changes that were kept, and every commit named is on `main`. Neither cycle reverted a change ([pass 2 report](docs/kaizen/2026-10-engine-kaizen-pass-2/05-final-report.md), [29 October report](docs/kaizen/2026-10-engine-kaizen/05-final-report.md)). One test assertion was relaxed on 29 October: a check that required the routing-fixture count to equal the frozen baseline became a lower bound (`4709e28`), and the baseline file was not changed. "Re-measured" means the figure was taken again on 2026-10-31 on a Fedora host from `main` or from the named commit; every other figure is copied from the evidence file named beside it. Ratings are reviewer judgements, not customer outcomes.

**Scores.** The raw score is the unweighted mean of ten reviewer-judged dimensions. The portfolio cap of 65 does not bind at any point, so each raw value equals its capped value. The stricter initial cap of 45 would report 45 at every point.

| Point | Raw | `min(raw, 65)` | Evidence |
|---|---:|---:|---|
| 29 October baseline | 50.28 | 50.28 | [`01-baseline-scorecard.md`](docs/kaizen/2026-10-engine-kaizen/01-baseline-scorecard.md) |
| 29 October final | 53.98 | 53.98 | [`05-final-report.md`](docs/kaizen/2026-10-engine-kaizen/05-final-report.md) |
| Pass 2 fresh baseline | 52.18 | 52.18 | [`01-baseline-scorecard.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/01-baseline-scorecard.md) |
| Pass 2 final | 55.68 | 55.68 | [`05-final-report.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/05-final-report.md) |

The pass 2 baseline is a fresh judgement that looked at surfaces the earlier cycle had not inspected (a tracked local settings file, gate false negatives, template currency), which is why it sits below the 29 October final. The 95 target was not reached.

**Measures.** The three value columns are the tree before the 29 October cycle (`b3b08b5`), the tree after it (`91b987d`) and `main` after pass 2.

| Measure | Before 29 Oct | After 29 Oct | After pass 2 | Basis |
|---|---|---|---|---|
| Active skills | 159 | 159 | 159 | Re-measured: `SKILL.md` files outside `templates/` at each commit. Unchanged. |
| Routing precision@1 (lexical proxy) | 47 of 55 (85.5%) | 57 of 65 (87.7%) | 64 of 72 (88.9%) | Re-measured with the stand-in described below. |
| Skills with three positive and two owned-negative fixtures | 0 of 159 | 4 | 8 | Re-measured with the `--coverage` option of `main` applied to each commit's fixtures. |
| Routing fixture prompts | 71 | 89 | 97 | Re-measured from `tests/routing-fixtures.json`. |
| Files named `check_*.py` or `validate_*.py` in `scripts/` | 6 | 10 | 14 | Re-measured with `git ls-tree`. |
| Python test functions under `engine/tests` and `tests` | 413 | 438 | 493 | Re-measured with `git grep "def test_"`. A static count, not a pass count. |
| Pytest result | 430 passed, 4 skipped, 96.29% coverage | 453 passed, 4 skipped, 96.47% | 535 passed, 5 skipped, 96.19% | Copied from the scorecards and validation records. `pytest` is absent on this host, so none was re-run. The last run had no Pandoc, so it is not like for like. The floor is 90%. |
| Run steps in `.github/workflows/engine.yml` | 12 | 12 | 18 | Re-measured. The workflow itself was never run locally. |
| Live lines naming a machine-specific path | 44 | 44 | 0 | Re-measured with `git grep` and the pattern in `scripts/check_portable_paths.py`, outside `docs/`. The frozen pass 2 baseline recorded 43 lines in 18 files; the difference is one line in `.gitignore` that its script did not count. |
| Tracked per-user settings files | 1 | 1 | 0 | Re-measured with `git ls-tree`. |
| Engine-level lines that prescribe the 2.1 accessibility level | 6 | 6 | 0 | Re-measured with `git grep`, outside `docs/` and `domains/`. |
| Source records whose review date is checked | no register | 17 records, not checked | 18 records, checked | Copied from the scorecards and the pass 2 final report. The count of 18 effective records from 2 registers is the current output of `scripts/validate_source_register.py`. |

The registered catalogue and routing scripts need `ruamel.yaml`, which this host lacks, so they exit 2 here. The re-measured skill counts and routing figures come from running the same scripts against each commit's tree with a throw-away PyYAML stand-in for `ruamel.yaml`, kept outside the repository. The stand-in reproduces the registered results in the Validation section above (64 of 72, 8 of 159).

Two measures did not move: 4 of 159 skills have an `examples/` folder (re-measured), and the live clause-label counts in the open findings above (163, 13 and 11 lines) are unchanged, held by a ceiling.

**Safety and integrity**

- **Tracked settings file** (the one critical defect; K2-01). A per-user permission file, `.claude/settings.local.json`, was tracked in this public repository. It held a broad shell allowlist and local names. It is now untracked and ignored, and `scripts/check_portable_paths.py` fails on any tracked `*.local.json`. The check exited 1 on the old tree and 0 after (pass 2 experiment log); re-measured, the file is tracked at `91b987d` and absent on `main`. Still open: earlier commits hold the file, and removing it needs a history rewrite, which is the maintainer's decision. `de1efdf`
- **Package gate integrity.** The gate accepted a mismatched or symlinked plugin. An independent review on 29 October reproduced two gaps: the Claude and Codex manifests could carry different plugin names, and an active `SKILL.md` could be a symlink to a file outside the tree. A third gap, found by the root review, let the entry counter skip unreadable subtrees without an error. Each now fails, with three regression tests; the 29 October validation record reports the full suite passing with 4 skipped (453 and 455 passed in two recorded reruns). Re-run today: `validate_plugin_packages.py` exits 0 with `errors: 0`. `91b987d`, `8cb2178`

**Correctness fixes**

- **NFR and trace checks** (K2-04). Phase 02 and Phase 05 gave wrong answers. The NFR check passed a requirement that said "quickly" or "at all times" with no threshold, and the test-trace check rejected NFR, IR, DR and CON identifiers and module-qualified forms such as `FR-META-006`. The qualifier list, spelled-out units and identifier forms were widened. Of the 30 new test cases, 21 failed before the change and all 30 passed after; a sweep of 12 project trees and 28 NFR-pattern lines changed no verdict outside the disposable task projects. Re-run today against the old and new patterns: "quickly" and "at all times" pass before and are flagged now; `NFR-001`, `FR-META-006` and `CON-004` are rejected before and accepted now; `BG-001` is still rejected. Behaviour change: a client NFR that passed with a bare qualifier can now fail until it gains a threshold. `08dae96`
- **Clean-checkout `.docx` build** (SDLC-01). A clean checkout could not build a `.docx`, and the contents list was blank. `scripts/build-doc.sh` failed because the ignored `templates/reference.docx` was absent. The builder now generates a temporary Word template and a populated, linked contents list. On 29 October, with Pandoc 3.13, the rebuilt file opened with `python-docx` and a LibreOffice PDF showed the contents entries; a test covers the missing-Pandoc failure. Not re-run today: Pandoc is absent here, so this is `NOT_ASSESSED` on this host. Native Word accessibility and font fidelity were never assessed. `4e5ec34`

**Portability and hygiene**

- **Dev-engine references** (SDLC-06 and K2-02). Skill text pointed at dev-engine skills that do not exist at those paths. Three names were repaired on 29 October and eight more in pass 2 (the retired flat `skills/<name>` layout, or an inactive alias), and the legacy database handoff prompt and README were updated. `scripts/check_cross_engine_refs.py` now detects the class: 8 findings on the old tree and exit 0 after (9 and 0 with a local dev-engine checkout, per the pass 2 log). Re-run today: exit 0. Category-path and URL resolution is `NOT_ASSESSED` without a checkout; the pass 2 record shows it passing against one. `e5698d1`, `2e5149d`, `2a02924`, `2ccbf36`
- **Machine-specific paths** (K2-03). Live files carried a Windows web-server path or a developer's home path. Eighteen files were reworded with the router's line count unchanged, and `check_portable_paths.py` fails on new ones. The historical record under `docs/` is held to a ceiling in `tests/portable-paths-baseline.json` and cannot grow. Re-measured: 44 live lines before, 0 on `main`; the check exits 0. `b8f17be`
- **First-run message and CI** (K2-08). A missing package produced a traceback, and CI skipped the new checks. `validate_skill_engine.py` and `routing_smoke_test.py` now name the package, print the install command and exit 2. The workflow gained six run steps, 12 to 18. Re-run today: both scripts exit 2 with the hint. The kernel CLI and two other scripts still print a traceback (`07-docs-followups.md`, item 6). `e2e80e1`

**New checks and tests**

- **Source ambiguity gate** (SDLC-04). Declared source ambiguities could not block Phase 02. A source-reconciliation register, a validator and a Phase 02 check now report each unresolved ambiguity as a blocker. On the six-ambiguity exercise the result is 6 high-severity findings and exit 1. In the pass 2 paired run the same five requirements fail with five findings when the register is present and pass when it is absent; making the register mandatory is an owner decision. Failure-path tests cover a missing or malformed register, a wrong root shape, bad source rows, identifiers and evidence, and dangling ambiguity links. The check reads declared links, not whether the register is complete. It needs the pinned packages and was not re-run today. `42098e6`, `30aa407`, `293aa0a`
- **Trace evidence states** (SDLC-05). A count of design and test links said nothing about oracles, decisions or execution. A JSON schema and `scripts/validate_traceability_evidence.py` report goal, design and test links, executable oracles, open owner decisions and executed tests as separate figures. On the ten-requirement fixture they read 10 design links, 10 test links, 0 business-goal links, 3 executable oracles, 7 open decisions and 0 executed. That fixture is synthetic and is not product coverage. The validator exited 0 on 29 October and is `NOT_ASSESSED` today (`jsonschema` is absent). `6105f73`
- **Package and discovery checks** (SDLC-02 and SDLC-03). Plugin manifests, the archive ceiling and Codex discovery had no check. A repository-scoped Codex marketplace now sits beside the Claude one. `validate_plugin_packages.py` checks manifest parity for the 159 skill paths and the 5,000-entry ceiling on the full-checkout and package counts, tested at exactly 5,000 and 5,001 entries. `check_codex_discovery_summary.py` validates a sanitised offline summary. The offline Codex 0.165.0 check on 29 October found all 159 paths with `skills.max_context_tokens=10000` against 108 at the default; that counts discovered paths, not selection quality. Re-run today: `validate_plugin_packages.py` exits 0, `errors: 0`. No archive was built or submitted, and the summary check was not run (no summary is held). `a596222`, `1ff245c`, `a51f164`
- **Edition drift** (K2-06). Six engine templates prescribed the 2.1 accessibility level against the engine's own WCAG 2.2 doctrine, and nothing stopped citations of superseded editions spreading. The six lines now say WCAG 2.2 AA, and `scripts/check_standards_currency.py` fails when any of eight counts rises above its committed ceiling. Re-measured: 6 lines before, 0 on `main`; the check exits 0. The ratchet does not remap clause labels, and 16 domain-pack lines wait for a jurisdiction decision. `87fa205`
- **Source review dates** (K2-07). They were prose, so an expired record raised nothing. `scripts/validate_source_register.py` fails on a record with no review date or a passed one. Pass 2 re-verified or added seven claims with source, access date and review date; where an issuer page returned HTTP 403 the record rests on a secondary check and says so. Re-run today: exit 0 as of 2026-10-31, exit 1 with 3 findings as of 2026-11-30 and with 14 as of 2027-02-01, which shows it can fail. `4a48a5c`

**Routing and discoverability**

- **Contradictory-brief routing** (K2-05). The task ranked its owning skill tenth. The description of `04-requirements-analysis` (305 of 350 characters) now names contradictory and ambiguous briefs. In the lexical proxy the task rank went from 10 to 1 (19.0 against 9.0, from the pass 2 log), eight fixtures were added, and `routing_smoke_test.py --coverage` and `--min-covered 8` make the three-positive, two-owned-negative count a repeatable output with a CI floor. The 29 October cycle added fixtures for the four routes it touched (`2e57bc0`, `2a02924`). Precision, coverage and fixture counts are in the measures table. This is a proxy, not live routing: the literal school-fees prompt still ties with the multi-tenancy skill (9.01 against 9.00), and three owned negatives are `NOT_ASSESSED` because their owners sit in other engines. `17c2179`, `2e57bc0`, `2a02924`

**Documentation**

- **Root documents** (documentation wave, 31 October). They described a repository that had changed. `AGENTS.md` no longer claims skills sit under `skills/<name>`; `DEPENDENCIES.md` was rewritten from the measured dependency set; `SETUP_GUIDE.md` and `CONTRIBUTING.md` use the scripts' real locations and the CI step list; the README gained the install, validation and quality sections with each command's measured result; and the architecture, stack, API, database, pathing, project brief and Copilot documents were corrected. The wave ran every documented command once on the Fedora host (no Pandoc, Mermaid renderer, browser or PowerShell) and recorded 13 findings for owners in [`07-docs-followups.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/07-docs-followups.md). It edited documents only. Re-run today: the checks in the Validation table that need no third-party package and the Node.js scripts agree with it. `ce95e9c`, `8cf62b2`, `676dd48`, `f1c17d6`, `908c6c3`, `4946c88`, `44a3eb3`, `29591d9`, `21a2382`, `41615b2`
- **Router release gate** (pass 2). The router named none of the new checks. The release-gate list in `AGENTS.md` now names the portability, reference, standards, source-register and routing checks, and says that category-path resolution is `NOT_ASSESSED` without a dev-engine checkout. The documentation wave later added the packaging check and the rule that a check which cannot run is `NOT_ASSESSED` (`8cf62b2`). `f15543f`

Evidence: [29 October experiment log](docs/kaizen/2026-10-engine-kaizen/03-experiment-log.md), [pass 2 backlog](docs/kaizen/2026-10-engine-kaizen-pass-2/02-improvement-backlog.md), [pass 2 experiment log](docs/kaizen/2026-10-engine-kaizen-pass-2/03-experiment-log.md) and [pass 2 validation record](docs/kaizen/2026-10-engine-kaizen-pass-2/04-validation-record.md).

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
