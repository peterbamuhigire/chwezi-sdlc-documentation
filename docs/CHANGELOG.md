# Changelog - Chwezi SDLC Documentation

All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2026-09-29] - Repository renamed to chwezi-sdlc-documentation

- The GitHub repository and local folder `srs-skills` are now `chwezi-sdlc-documentation`
  (https://github.com/peterbamuhigire/chwezi-sdlc-documentation). Engine id, display name,
  README, manifest, installers and cross-engine links follow the new name.
- Claude Code plugin renamed: marketplace `chwezi-srs` is now `chwezi-sdlc-documentation` and
  plugin `srs` is now `sdlc-documentation` (`/plugin install sdlc-documentation@chwezi-sdlc-documentation`).
- The Python validation kernel keeps its `engine` import package; its distribution name is now
  `chwezi-sdlc-documentation-engine`.
- Dated records (audits, Kaizen logs, plans, evidence) keep the old name as written.

## [2026-09-24] - OWASP 2026 re-mapping and follow-up fixes

- AI skills, red-team scenario library, agent security requirements and the ISO 27001 control
  template re-mapped to the OWASP Top 10 for LLM Applications 2026 (published 2026-08-03), with
  2025 IDs kept in brackets; every citation carries its edition year. A mis-cited "LLM06"
  (sensitive information disclosure) corrected to LLM02.
- Router tables updated for the chwezi-dev-engine consolidation (doc-architect and
  skill-engine-audit absorb markdown lint, doc maintenance and the skill safety gate).

## [2026-09-24] - Book-extraction retirement and requirement-quality currentness

### Removed

- `book-extractions/` (15 files), `docs/research/adzic-books-analysis.md` and
  `docs/ux-foundations.md`; knowledge folded into task-oriented skill references
  and all links repointed. See
  `docs/continuous-improvement/book-extraction-retirement-2026-09-24.md`.

### Added

- References: scenario spine and requirement contract (traceability), human
  English and lexical precision (anti-slop), UX requirements foundations (UX
  specification), story splitting patterns, scenario quality rules, and the
  ISO/IEC 25010:2023 NFR coverage map (attribute mapping).
- Part 7 ISO/IEC/IEEE 29148:2018 requirement-quality overlay in the waterfall
  compliance checklist; `08-semantic-auditing` applies it.
- "Never store book extractions" section in `AGENTS.md` and `CLAUDE.md`.
- `scripts/source_ingestion_guardrail.py` fails on extraction folders,
  extraction-named files and links into them; tests in
  `tests/test_source_ingestion_guardrail.py`.

### Changed

- `CLAUDE.md` principles now name ISO/IEC/IEEE 29148:2018 (IEEE 830 kept only as
  section layout), ISO/IEC/IEEE 24765 (successor to IEEE 610.12) and
  ISO/IEC 25010:2023 with IEEE 982-2024 measures (982.1-2005 replaced).
- UX specification: WCAG 2.2 and project-validated list limits replace
  WCAG 2.1 and fixed "7 plus or minus 2" caps.
- `03-api-specification`: generates OpenAPI 3.1.2 (3.2.x optional when the
  toolchain supports it), JSON Schema 2020-12 schemas and RFC 9457 problem
  details; rate-limit headers are a documented project decision (IETF
  RateLimit fields still a draft); RFC 9110 replaces RFC 7231. Heading
  contract of `API_Specification.md` unchanged.
- IEEE 830-1998 no longer cited as a governing standard in skills, templates
  and domain packs; ISO/IEC/IEEE 29148:2018 is named as authoritative.
- "OWASP LLM Top 10 (agentic addendum)" replaced by OWASP Top 10 for LLM
  Applications 2025 and OWASP Top 10 for Agentic Applications 2026; red-team
  scenario library re-mapped from 2023 v1.1 names to LLM01:2025-LLM10:2025.
- `03-vision-statement` filter rewritten as five task-oriented checks.
- `05-conceptual-data-modeling` description covers data contracts,
  dictionaries, catalogs, lineage, and data quality/governance requirements.
- `07-attribute-mapping` description aligned to its body (SRS Sections
  3.3-3.6 quality attributes).

### Added (Kaizen follow-up)

- `09-governance-compliance/15-ai-act-and-regulatory-compliance-doc/references/eu-ai-act-application-timeline.md`
  (AI Act dates as amended by Regulation (EU) 2026/1744).
- `02-requirements-engineering/references/final-requirements-quality-gate.md`,
  linked from `01-prd-generation`, `01-initialize-srs` and `08-semantic-auditing`.
- Routing fixtures `attribute-mapping-positive` and
  `data-quality-governance-positive`.

## [2026-09-19] - Phase 1 Kaizen references

- Added the bounded Phase 1 Kaizen reference slice: requirements problem/goal,
  event-centred trace, and fit-criteria fixtures; governance pause-point,
  dependency-exception, and pilot-evaluation templates; and healthcare
  care-to-cash, denial/compliance, role/credential, and listening/safe-service
  references.
- Added focused contract tests covering normal and failure paths. Current payer,
  credential, privacy, clinical, legal, and accounting claims remain explicit
  project inputs and are not admitted by these references.

## [2026-09-08] - Waiver Integrity and Engine Routing

### Changed

- Hardened waiver loading and CLI writes against malformed YAML, invalid field
  types, duplicate IDs, unsafe scopes, blank approvals, and invalid durations.
- Routed Codex and Claude to the
  [Chwezi Dev Engine](https://github.com/peterbamuhigire/chwezi-dev-engine)
  without embedding a machine-specific checkout path; removed stale
  home-mirror references.
- Added the comprehensive Kaizen evidence record at
  `docs/audits/2026-09-08-comprehensive-kaizen.md`.

### Validation

- 157 active skills and 52/52 routing fixtures pass; the engine contract,
  source-ingestion guard, and 255 tests pass. The configured 90% coverage gate
  passes at 95.93% total coverage.

## [2026-08-09] - Kraal Code Product Identity Migration

### Changed

- Established `Kraal Code` as the canonical product name and `kraalcode.com` as the canonical product website.
- Renamed the SRS workspace to `projects/KraalCode`, converted compact tokens to `KraalCode`, deployment and repository slugs to `kraal-code`, and runtime identifiers to the `KRAAL_CODE` namespace.
- Updated project, cross-project, domain-reference, alignment, build-permission, and engine-inventory references.
- Renamed and regenerated the complete Word delivery set using the `KraalCode_*.docx` convention.

### Validation

- SRS engine, identity-residue, DOCX-package, finance, design, accessibility, render, and anti-slop results are recorded in `projects/KraalCode/DOCUMENTATION-STATUS.md` and the project gate manifests.

## [2026-08-02] - Predecessor Product Identity Migration (Superseded)

### Changed

- Applied the then-current product identity to the SRS workspace, Word deliverables, deployment examples, cross-project references, alignment plans, and build permissions.
- This record is retained for change history; the 9 August 2026 Kraal Code migration supersedes its identity values.

### Validation

- The migration passed the SRS engine, DOCX package, and identity-residue checks recorded at that time.

## [2026-07-06] - Validation Kernel Fixes (glossary code spans, waiver dates, FR ID pattern)

### Fixed

- `engine/checks/glossary_registry.py`: the jargon scanner now strips inline code spans and skips fenced code blocks before extracting acronym/CamelCase candidates. Backticked identifiers (`FtsIndexService`) are code references under the documented monospace convention, not undefined glossary jargon; previously a code-grounded document set produced hundreds of false `missing_term` findings.
- `engine/waivers.py`: waiver `approved_on`/`expires_on` values are coerced to `date` on load. The `engine waive` CLI writes quoted ISO strings, which made `phase09.waivers_have_expiry` crash with a `str - str` TypeError on any project that used its own waiver command.
- `engine/gates/phase05.py`: the exit-evidence FR-reference pattern now accepts module-qualified IDs (`FR-META-006`) in addition to bare `FR-1`, matching the identifier convention the engine's own idscan enforces.

## [2026-04-28] - Project DOCX Export Contract

### Added

- Defined the required per-project DOCX export contract: `projects/<ProjectName>/export/`, `projects/<ProjectName>/export-docs.ps1`, and `projects/<ProjectName>/export-docs.sh`.
- Updated the engine scaffold so every new project receives the export folder and both export scripts, including example-seeded projects.
- Updated setup scripts, root protocols, pathing documentation, and Word-output guidance to require refreshing `export/` after `.docx` generation.

## [2026-04-25] - Standard Skill Repository Layout

### Changed

- Moved the root-level `00-meta-initialization` skill into the standard `skills/00-meta-initialization/SKILL.md` layout.
- Removed the duplicate root-level `professional-word-output` skill; the canonical copy remains at `skills/professional-word-output/SKILL.md`.
- Updated root project documentation to state that portable skills live under `skills/<skill-name>/SKILL.md` and that the repository root is reserved for project documentation plus `docs/`, `skills/`, and `projects/` where relevant.

## [2026-04-14] — Skills Engine Completion Plan — 10-Phase Execution Roadmap

### Added

- **`docs/plans/execute-completion/`** — 10-phase execution plan to complete the canonical [Chwezi Dev Engine](https://github.com/peterbamuhigire/chwezi-dev-engine) library as an SDLC software execution engine for Chwezi Core Systems ICT consultancy.
  - `README.md` — Master index: all 12 new skills, 8 enhancements, 3 stubs, and 4 deprecations in one summary table; priority override directing infrastructure phases first.
  - `phase-01.md` — Client Engagement, Discovery & Strategic Planning: 15 existing skills inventoried; practice workflow and reading list (Nomadic Developer, INSPIRED, Software Requirements).
  - `phase-02.md` — Requirements Engineering & Documentation Engine: full 8-phase SRS workflow, Uganda DPPA compliance annex, professional Word output; already world-class.
  - `phase-03.md` — Architecture, Design & Data Modeling: 2 new skills (`event-driven-architecture`, `graphql-patterns`); content outlines + reading list (Kleppmann, Bellemare, Newman).
  - `phase-04.md` — Web Application Stack: `webapp-gui-design` stub completion (27 → 350+ lines); 15-section content outline covering SaaS UI component architecture.
  - `phase-05.md` — Mobile Application Stack: `android-ai-ml` new skill (ML Kit, TFLite, MediaPipe, Gemini Nano); 4 deprecated android-* skill markers; reading list.
  - `phase-06.md` — AI-Differentiated Product Layer: production RAG enhancement for `ai-rag-patterns` — Advanced RAG, RAGAS evaluation, multi-tenant isolation, cost management.
  - `phase-07.md` — Quality Engineering & Test Automation: 2 new skills (`e2e-testing` with Playwright POM + CI, `pwa-offline-first` with Workbox + Dexie.js + Background Sync).
  - `phase-08.md` — Deployment Pipeline, CI/CD & Infrastructure: 4 new skills (`cloud-architecture`, `kubernetes-platform`, `infrastructure-as-code`, `cicd-pipelines`) + 3 enhancements (Vault/ISO27001/Falco, Linux hardening, FinOps); reading list of 7 books.
  - `phase-09.md` — Production Operations, Observability & SRE: `observability-platform` skill (SigNoz, OTel, SLO/SLI, Sentry, blameless postmortems) + 3 enhancements (database SRE, Nginx/Kong ops, n8n/Temporal orchestration).
  - `phase-10.md` — Revenue Infrastructure, Business Growth & Scale: 4 new skills (`stripe-payments`, `subscription-billing`, `product-led-growth`, `saas-growth-metrics`); `pos-restaurant-ui-standard` + `inventory-management` stubs completed; `web-app-security-audit` network layer enhancement.
- **`docs/plans/2026-04-14-engine-completion-design.md`** — Brainstorming design document recording the approved 10-phase structure and scope decisions.

### Summary

When all 10 phases are executed the skills library will cover the complete SDLC arc — from first client conversation through deployed, monitored, revenue-generating production software — with no critical capability gap remaining. Phase 8 (infrastructure) and Phase 10 (revenue) are flagged as highest-priority and should be executed before the remaining phases.

---

## [2026-04-13] - Workspace Pathing Model Clarification

### Changed

- Defined `projects/<ProjectName>/...` as the canonical runtime workspace model in root repository documentation.
- Added `docs/pathing-model.md` to formalize the relationship between canonical project paths and legacy execution aliases such as `../project_context/` and `../output/`.
- Updated `README.md`, `AGENTS.md`, `CLAUDE.md`, `ARCHITECTURE.md`, `skill_overview.md`, `00-meta-initialization/templates/doc_roadmap.md.template`, and `02-requirements-engineering/waterfall/README.md` to remove the root-level path ambiguity.
- Updated evaluation documents so pathing is no longer described as an unresolved root-architecture inconsistency, but as a remaining skill-level migration task.

## [2026-04-13] - Testing Standards Modernization

### Added

- **Phase 05 deterministic checklist** (`05-testing-documentation/references/29119-deterministic-checks.md`) enumerating the mandatory ISO/IEC/IEEE 29119-3 artifact tree, normative fields, traceability, and gate criteria.
- **Running templates** for incident reports and test completion reports per 29119-3 §§7.5-7.6 (`05-testing-documentation/templates/incident-report.md`, `test-completion-report.md`) so every execution log can cite a structured artifact.

### Changed

- **Phase 05 README** now highlights the 29119-3 alignment and supporting templates.
- **01-Test-Strategy**, **02-Test-Plan**, and **03-Test-Report** SKILLs now reference BS ISO/IEC/IEEE 29119-3, invoke the deterministic checklist before writing artifacts, and document obligation to include normative fields and technique taxonomies.
- **Book-driven gap analysis** and evaluation summaries now cite these testing improvements so standards alignment is seen as actionable, not just declarative.

## [2026-04-07] — AI Module Upgrade Across All Active Projects

### Added

- **Kulima** — AI Farm Advisor module: PRD `FR-AI` business section (5 features: Natural Language Q&A, Photo Pest/Disease Diagnosis, Personalised Farm Plan, Seasonal Planting Advisory, Market Timing Advice); SRS FR-AI-001–006 technical requirements verified and strengthened with measurable thresholds; `Kulima_PRD.docx` and `Kulima_SRS.docx` built.
- **Medic8** — AI Clinical Intelligence module: PRD `FR-AI` business section (5 features: At-Risk Patient EWS, Differential Diagnosis Support, SOAP Note Summarisation, Pharmacy Demand Forecasting, Disease Surveillance); SRS FR-AI-001–005 technical requirements added to `04-functional-requirements.md`; `Medic8_PRD.docx` and `Medic8_SRS.docx` built.
- **KraalCode** — AI Intelligence module: new PRD file `10-ai-intelligence.md` (5 features: Cash Flow Intelligence, GL Anomaly Detection, Demand Forecasting and Reorder, Debtor Default Risk Scoring, Narrative Financial Reports); new SRS Module 15 directory (`15-ai-intelligence/`) with cover, introduction, FR-AI-001–005, NFRs, and traceability; `KraalCode_PRD.docx` rebuilt and `KraalCode_SRS_AIIntelligence.docx` built.
- **Maduuka** — AI Business Intelligence module: PRD section `7A` (4 features: Sales Forecasting, Smart Reorder Advisor, Fraud and Anomaly Alerts, Business Health Advisor) inserted into `01-prd.md`; SRS FR-AI-001–004 appended to `04-functional-requirements.md`; `Maduuka_PRD.docx` and `Maduuka_SRS_Phase1.docx` rebuilt.
- **BIRDC-ERP** — AI Intelligence Phase 7 contract extension: new PRD file `11-ai-module.md` (5 capabilities: Production Yield Prediction, Quality Defect Pattern Detection, Farmer Supply Forecasting, Predictive Equipment Maintenance, Export Demand Intelligence); SRS `08-fr-ai.md` added to Phase 6 (`06-srs-phase6-research-admin/`) with FR-AI-001–005; `PRD_BIRDC_ERP.docx` and `SRS_BIRDC_ERP_Phase6_ResearchAdmin.docx` rebuilt.
- Implementation plan saved to `docs/plans/2026-04-07-ai-module-upgrade-all-projects.md`.

### Changed

- All 5 active projects now have domain-specific AI modules specified at both PRD (business language) and SRS (IEEE 830 stimulus-response) levels, consistent with the AcademiaPro AI module pattern established previously.

---

## [Unreleased] — AcademiaPro Phase 2 Requirements Engineering — 2026-03-29

### Project: AcademiaPro (Chwezi Core Systems)

**Phase 2 — Requirements Engineering completed.** All IEEE 830-compliant SRS sections authored, built to `.docx`, and project documentation updated.

**Deliverables produced:**

- `02-requirements-engineering/AcademiaPro_SRS.docx` — 6-section SRS: Introduction, Overall Description, External Interfaces, 49 Functional Requirements (FR-AUTH/TNT/SIS/ACA/FEE/ATT/EXM/RPT/RBAC/EMIS/AUD), System Constraints, 13 NFRs
- `02-requirements-engineering/AcademiaPro_UserStories.docx` — 20 user stories with Gherkin acceptance criteria
- `02-requirements-engineering/AcademiaPro_RBAC_Stakeholder.docx` — Full RBAC permission matrix (60+ permissions × 8 roles); closes HIGH-005

**Skill alignments explicit in SRS:**

- `multi-tenant-saas-architecture` — three-tier panel architecture, `tenant_id` enforcement, rate limits, audit retention
- `dual-auth-rbac` — session prefix `academia_pro_`, JWT 15 min/30 day, Argon2ID (C-003), 5-level permission resolution
- `mysql-best-practices` — InnoDB/utf8mb4, non-destructive migrations
- PRD 7-day mobile refresh token superseded by skill's 30-day standard (documented in C-002)

**Gap analysis updates:**

- HIGH-005 (RBAC matrix): ✅ Resolved
- HIGH-006 (double-payment, Phase 1 manual scope): ✅ Resolved in FR-FEE-002/003
- HIGH-001, HIGH-002, HIGH-003, HIGH-004, HIGH-007, HIGH-008: Pending (next phase)

**Context gaps flagged for external resolution:**

- `[CONTEXT-GAP: UNEB registration format]` — contact UNEB; blocks FR-EXM-008
- `[CONTEXT-GAP: MoES EMIS data dictionary]` — obtain from MoES; blocks FR-EMIS-001

---

## [3.5.1] - 2026-03-08

### Added

**IEEE 830-1998 Full Compliance Enforcement:**
- **ieee-830-compliance-checklist.md** - Authoritative compliance reference for all waterfall SRS skills
  - Part 1: Eight Quality Attributes (§4.3) with pass/fail criteria and examples
  - Part 2: SRS Structure Checklist (§5.1–§5.4) with checklist IDs (IEEE830-x.x.x)
  - Part 3: Annex A Template Selection Guide (A.1–A.8)
  - Part 4: TBD Protocol (§4.3.3.1) with mandatory fields
  - Part 5: Anti-Patterns and Fixes
  - Part 6: Skill-to-Clause Mapping

### Changed

**Phase 03 (Descriptive Modeling) - IEEE 830 §5.2 compliance:**
- Now generates all eight §5.2.1 sub-items: System/User/Hardware/Software/Communications Interfaces, Memory Constraints, Operations, Site Adaptation
- Added Section 2.6 Apportioning of Requirements (§5.2.6)

**Phase 05 (Feature Decomposition) - IEEE 830 §5.3.2 compliance:**
- Added validity checks on inputs (§5.3.2a)
- Added exact sequence of operations (§5.3.2b)
- Added responses to abnormal situations: overflow, communication failure, error recovery (§5.3.2c)
- Added effect of parameters (§5.3.2d)
- Added input/output relationships and formulas (§5.3.2e)
- Enforced importance ranking on every requirement (§4.3.5)
- Enforced backward traceability reference on every requirement (§4.3.8)

**Phase 07 (Attribute Mapping) - IEEE 830 §5.3.5.1 and §5.3.8:**
- Added Section 3.5.5 Standards Compliance (§5.3.5.1): report formats, data naming, audit tracing
- Added Section 3.6 Other Requirements (§5.3.8): portability, installation, localization
- Output range expanded from Sections 3.3–3.5.4 to Sections 3.3–3.6

**Phase 08 (Semantic Auditing) - Comprehensive IEEE 830 audit:**
- Enhanced to validate all 8 quality attributes with checklist ID references
- Added ranking completeness check (§4.3.5): flags every unranked requirement
- Added TBD protocol enforcement (§4.3.3.1): validates condition, resolution, owner, deadline
- Added modifiability checks (§4.3.7): compound-shall detection, redundancy detection
- Added backward traceability validation (§4.3.8): every requirement must reference source
- Added SRS structure completeness check (§5.1–§5.4): verifies all required sections exist
- Added Annex A template verification (confirms Section 1.5 documents template choice)
- Enhanced Python automation (`semantic_auditing.py`) with 8 new validation functions
- Overall compliance verdict: COMPLIANT / PARTIALLY COMPLIANT / NON-COMPLIANT
- RTM now includes Backward Trace column

## [3.3.0] - 2026-03-01

### Added

**Phase 04: Development Artifacts (4 new skills):**
- **01-technical-specification** - Module-level technical specs with interface contracts, data structures, algorithm details per IEEE 1016/830
- **02-coding-guidelines** - Naming conventions, formatting, patterns, code review criteria per IEEE 730
- **03-dev-environment-setup** - Toolchain installation, build configuration, local development workflow per IEEE 1074
- **04-contribution-guide** - Branching strategy, commit conventions, PR workflow, CI/CD integration per IEEE 1074

**Phase 05: Testing Documentation (3 new skills):**
- **01-test-strategy** - Test levels, types, tools, environments, entry/exit criteria per IEEE 829 Sec 6
- **02-test-plan** - Test cases with requirements traceability, test data, schedule per IEEE 829 Sec 7-8
- **03-test-report** - Execution report template with pass/fail summary, defect analysis, coverage metrics per IEEE 829 Sec 9-10

**Phase 06: Deployment & Operations (4 new skills):**
- **01-deployment-guide** - Step-by-step deployment procedures with rollback and environment configs per IEEE 1062
- **02-runbook** - Incident response, escalation paths, health checks, recovery playbooks per SRE practices
- **03-monitoring-setup** - Metrics definitions, alerting rules, dashboard specs, SLI/SLO targets per ISO/IEC 25010
- **04-infrastructure-docs** - Architecture diagrams (Mermaid), resource inventory, networking topology per IEEE 1016

**Phase 07: Agile Artifacts (4 new skills):**
- **01-sprint-planning** - Sprint goal, capacity calculation, backlog selection, task breakdown per Scrum Guide/IEEE 29148
- **02-definition-of-done** - Multi-level DoD checklist (story, increment, release) per Scrum Guide
- **03-definition-of-ready** - Backlog item readiness criteria with acceptance criteria and sizing per Scrum Guide
- **04-retrospective-template** - Multiple facilitation formats (Start-Stop-Continue, 4Ls, Sailboat) per Scrum Guide

**Phase 08: End-User Documentation (4 new skills):**
- **01-user-manual** - Getting started, feature guides, role-based workflows, troubleshooting per ISO 26514
- **02-installation-guide** - System requirements, installation steps, configuration, verification per ISO 26514
- **03-faq** - Categorized question-answer pairs with cross-references per ISO 26514
- **04-release-notes** - Version tracking, features, bug fixes, breaking changes, migration guide per IEEE 830

**Phase 09: Governance & Compliance (4 new skills):**
- **01-traceability-matrix** - Bidirectional RTM with gap analysis and orphan detection per IEEE 1012-2016
- **02-audit-report** - V&V audit with severity-rated findings and remediation plan per IEEE 1012-2016
- **03-compliance-documentation** - Regulatory mapping (GDPR/HIPAA/SOC2) with gap analysis
- **04-risk-assessment** - ISO 31000 risk framework with probability/impact matrix and risk register per ISO 31000/IEEE 1012

**Infrastructure:**
- Updated skill_overview.md pipeline registry with all 23 new skills
- 6 new phase-level README.md files

### Changed

- All 10 SDLC phases now fully implemented (100% phase coverage)
- Overall engine implementation increased from ~50% to 100% of planned documentation skills
- Total skill count: 46 documentation generation skills across 10 phases

## [3.2.0] - 2026-02-28

### Added

**Phase 01: Strategic Vision (3 new skills):**
- **03-vision-statement** - Formal vision document with elevator pitch, Geoffrey Moore product positioning, SMART success criteria per IEEE 29148 Sec 6.2
- **01-prd-generation** - Product Requirements Document with market context, feature priority matrix (MoSCoW), success metrics per IEEE 29148/1233
- **02-business-case** - Business case with cost-benefit analysis (NPV/LaTeX), ROI projection, risk assessment matrix, go/no-go criteria per IEEE 1058

**Phase 02: Agile Requirements Track Completion (3 new skills):**
- **02-acceptance-criteria** - Gherkin Given-When-Then acceptance criteria with NFR criteria per IEEE 29148 Sec 6.4.5
- **03-story-mapping** - Jeff Patton story maps with backbone activities, walking skeleton, release slices per IEEE 29148
- **04-backlog-prioritization** - MoSCoW classification with WSJF scoring, sprint allocation, release planning per IEEE 29148 Sec 6.4.6

**Phase 03: Design Documentation (4 new skills):**
- **01-high-level-design** - System architecture with Mermaid C4/deployment/data flow diagrams, technology decisions per IEEE 1016-2009 Sec 5
- **02-low-level-design** - Module specs with class/sequence/state diagrams (Mermaid), algorithm formalization (LaTeX) per IEEE 1016-2009 Sec 6
- **03-api-specification** - REST API endpoints with OpenAPI 3.0 YAML artifact, standardized error format per IEEE 29148/RFC 7231
- **04-database-design** - ERD (Mermaid), normalization analysis, data dictionary, migration strategy per IEEE 1016 Sec 6.7 with mandatory mysql-best-practices integration

**Phase 02 Fix:**
- **05-feature-decomposition** - Added missing SKILL.md wrapper for the waterfall feature decomposition skill

**Infrastructure:**
- Setup scripts for new SRS projects (PowerShell + Bash)
- SETUP_GUIDE.md with complete workflow instructions
- Updated skill_overview.md pipeline registry with all new skills

### Changed

- Agile requirements track expanded from 1/4 to 4/4 sub-phases (100% complete)
- Waterfall requirements track now 8/8 sub-phases with all SKILL.md files present
- Overall engine implementation coverage increased from ~23% to ~50%

## [3.1.0] - 2026-02-07

### Added

**AI-Assisted Development Skills:**
- **ai-assisted-development** - Orchestration patterns for coordinating multiple AI agents in software development workflows
  - 5 orchestration strategies (Sequential, Parallel, Conditional, Looping, Retry)
  - 3 AI-specific patterns (Agent Handoff, Fan-Out/Fan-In, Human-in-the-Loop)
  - Real-world examples from MADUUKA and BRIGHTSOMA applications
  - References: orchestration-strategies.md, ai-patterns.md, practical-examples.md

- **orchestration-best-practices** - The 10 Commandments of Orchestration for multi-step workflows
  - Enforces clear step definition, dependency tracking, error handling
  - Complete code examples (good vs bad patterns)
  - Verification checklist for all generated code
  - Anti-patterns guide

- **ai-error-prevention** - Error prevention strategies for AI-assisted development (Trust But Verify)
  - 7 prevention strategies to minimize wasted tokens and catch Claude's mistakes early
  - Common Claude failure modes and prevention techniques
  - App-specific checklists (MADUUKA, MEDIC8, BRIGHTSOMA, DDA, CROWNPOINT)
  - Token savings: 50-75% reduction in wasted tokens
  - References: prevention-strategies.md, failure-modes.md, app-specific-prevention.md

- **ai-error-handling** - 5-layer validation stack for AI-generated code
  - Layer 1: Syntax validation
  - Layer 2: Requirement matching
  - Layer 3: Test validation
  - Layer 4: Security checks
  - Layer 5: Documentation validation
  - Quality scoring system (0-100 with 80% acceptance threshold)

**Reference Guides:**
- **prompting-patterns-reference.md** - 10 essential prompting patterns for better AI instructions
  - Clear Task + Context + Constraints, Chain-of-Thought, Few-Shot Learning, etc.
  - Reduces clarification questions by 50%, improves first-time-right code by 60%

- **orchestration-patterns-reference.md** - Comprehensive orchestration guide for multi-agent workflows
  - 5 orchestration types with real-world examples
  - 4 core patterns (Map-Reduce, Pipeline, Fan-Out/Fan-In, Circuit Breaker)
  - Decision trees and complexity vs performance analysis

- **encoding-patterns-into-skills.md** - Guide for creating pattern-enforcing skills
  - Formula: Rules + Examples + Checklists + Decision Trees
  - Pattern encoding templates
  - Skill effectiveness and iteration strategies

**Documentation Standards:**
- All new skills comply with doc-standards.md (500-line hard limit)
- Two-tier structure (Tier 1 TOC + Tier 2 deep dives)
- Smart subdirectory grouping for maintainability

### Changed

- **skills/CLAUDE.md** - Updated repository structure to include AI development skills
- **skills/ai-assisted-development/SKILL.md** - Refactored from 879 lines to 462 lines (compliant)
  - Split into main SKILL.md + 3 reference files
  - Improved navigability and token efficiency

### Performance

- **Token Efficiency Improvements:**
  - ai-error-prevention saves 50-75% of tokens through early error detection
  - Prompting patterns reduce clarification rounds by 50%
  - Orchestration patterns enable 30-50% faster parallel execution

### Documentation

- Updated to reflect expanded scope beyond SDLC documentation to include AI development assistance
- All skills now enforce automatic pattern following through structured templates

## [3.0.0] - 2026-02-06

### Added

- Multi-methodology support (Waterfall, Agile, Hybrid)
- Expanded from SRS-only to 23 document types across 10 SDLC phases
- Phase 00: Meta-initialization for methodology detection
- Agile track: User story generation with INVEST criteria
- Backward compatibility with v2.x Waterfall SRS pipeline

### Changed

- Renamed from SRS-Skills to SDLC-Docs-Engine
- Reorganized phases: 01-08 → 02-requirements-engineering/waterfall/
- Updated README.md and PROJECT_BRIEF.md

## [1.0.0] - 2026-01-26

### Added

- Core 1-8 Skill Pipeline targeting IEEE 830 and ISO/IEC 25010.
- Submodule-ready architecture with relative pathing to ../project_context.
- High-density seeder templates for Skill 01 with ISO-aligned elicitation questions.
- Skill Registry (skill_overview.md) for architectural transparency.
- V&V Standard Operating Procedure in CLAUDE.md.

### Changed

- (Document future modifications to skill logic.prompt or root-level protocols here, referencing the Engineering Registry when appropriate.)

### Fixed

- (Reserve for bug fixes per semantic versioning.)

### Removed

- (Use this section for retired features or deprecated skill templates.)

### Security

- (Record security-related updates or compliance notes.)
