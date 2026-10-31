# Chwezi SDLC Documentation Project Brief

## Current catalogue and phase model (2026-10-31)

The current catalogue contains **159 filesystem-discovered active skills** and
**1 inactive authoring template**, as recorded in the
[`skill-quality-baseline.json`](tests/skill-quality-baseline.json) control and
checked by [`validate_skill_engine.py`](scripts/validate_skill_engine.py); both
counts were also taken with `find` on this date.
The phase model is SDLC phases `01` through `09`; Phase 02 contains the
Waterfall, Agile, Hybrid and requirements-fundamentals tracks. Methodology
selection (`00-meta-initialization`) belongs to the Chwezi Dev Engine and is no
longer in this repository. Release and validation status are in
[`README.md`](README.md); the v3.x labels below are the historical numbering of
the earlier SDLC-Docs-Engine.

## What Is This?

**Chwezi SDLC Documentation** (earlier names: SDLC-Docs-Engine and SRS-Skills) is a standards-driven library of agent skills and a validation kernel for software-lifecycle documentation. Its skills help an agent produce IEEE/ISO-aligned documents across all phases of software development, and the kernel checks the result against deterministic gates.

**Think of it as:** A portable documentation engine whose skill entrypoints (`SKILL.md` files under the numbered phase folders) read your project context and guide the generation of documentation for **Waterfall, Agile, or Hybrid** methodologies.

---

## Historical v3.3 release snapshot

**Complete SDLC Coverage** (March 2026) - 23 new documentation skills across 6 phases, bringing the engine to **100% phase coverage**:

**Phase 04: Development Artifacts** - Technical specs, coding standards, dev setup, contribution guides (IEEE 730, IEEE 1074)

**Phase 05: Testing Documentation** - Test strategy, test plans, test reports (IEEE 829)

**Phase 06: Deployment & Operations** - Deployment guides, runbooks, monitoring, infrastructure docs (IEEE 1062, SRE, ISO 25010)

**Phase 07: Agile Artifacts** - Sprint planning, Definition of Done/Ready, retrospective templates (Scrum Guide, IEEE 29148)

**Phase 08: End-User Documentation** - User manuals, installation guides, FAQs, release notes (ISO 26514, IEEE 830)

**Phase 09: Governance & Compliance** - Traceability matrix, audit reports, compliance docs, risk assessment (IEEE 1012, GDPR/HIPAA/SOC2, ISO 31000)

**Historical v3.3 snapshot: 46 documentation generation skills across all 10
SDLC phases.** The current catalogue is recorded above.

## What Was New in v3.2?

**Documentation Skills Expansion** (February 2026) - 11 new skills across 3 phases:
- **Phase 01: Strategic Vision** - Vision Statement, PRD, Business Case (IEEE 29148, IEEE 1058)
- **Phase 02: Agile Track Complete** - Acceptance Criteria, Story Mapping, Backlog Prioritization (IEEE 29148)
- **Phase 03: Design Documentation** - HLD, LLD, API Specification, Database Design (IEEE 1016, OpenAPI 3.1)
- **Infrastructure:** Setup scripts (PowerShell + Bash) for bootstrapping new SRS projects

## What Was New in v3.1?



**AI-Assisted Development Skills** - Skills that enhance Claude Code's ability to help you develop software:

- **ai-assisted-development**: Orchestrate multiple AI agents (30-75% faster through parallelization)
- **ai-error-prevention**: 7 strategies to catch Claude's mistakes early (saves 50-75% of tokens)
- **orchestration-best-practices**: The 10 Commandments of Orchestration
- **ai-error-handling**: 5-layer validation stack for AI-generated code
- **Reference guides**: Prompting patterns, orchestration patterns, encoding patterns into skills

## What Was New in v3.0?

Previously called **SRS-Skills** (focused only on IEEE 830 SRS generation), v3.0 expanded to support:

- ✅ **Multi-Methodology Support**: Waterfall (IEEE 830 SRS) + Agile (User Stories) + Hybrid
- ✅ **23 Document Types**: PRD, SRS, User Stories, HLD, LLD, API Specs, Test Plans, Runbooks, Manuals, Compliance Docs
- ✅ **10 SDLC Phases**: From strategic vision to governance/compliance
- ✅ **Methodology Detection**: Automatic project analysis and recommendation (Phase 00)
- ✅ **Backward Compatible**: Existing Waterfall SRS pipeline preserved

---

## How It Works

### 1. Install as Unified Repository

```bash
git clone https://github.com/peterbamuhigire/chwezi-sdlc-documentation.git
cd chwezi-sdlc-documentation
```

### 2. Select Methodology

```bash
Run skill: 00-meta-initialization (engineering catalog engine)
```

The engine scans your project and recommends Waterfall, Agile, or Hybrid based on:
- Regulatory requirements (FDA, FAA, HIPAA)
- Project type (startup, enterprise, government)
- Development pace (commit frequency, sprint structure)
- Team structure and size

### 3. Generate Documentation

**For Waterfall:**
```bash
Run: 02-requirements-engineering/waterfall/01-initialize-srs
# ... run phases 02-08 sequentially
Output: SRS_Draft.md (IEEE 830), Traceability_Matrix.md, Audit_Report.md
```

**For Agile:**
```bash
Run: 02-requirements-engineering/agile/01-user-story-generation
Output: user_stories.md, story_map.mmd, backlog_summary.md
```

### 4. Expand to Other Phases

```bash
Run: 03-design-documentation/01-high-level-design
Run: 05-testing-documentation/02-test-plan
Run: 06-deployment-operations/02-runbook
```

---

## What Can It Generate?

### Requirements Documentation
- **Waterfall**: SRS in the IEEE 830 section layout (Waterfall skills 01 to 09)
- **Agile**: INVEST-compliant user stories with acceptance criteria

### Design Documentation
- High-Level Design (HLD) - IEEE 1016
- Low-Level Design (LLD) - IEEE 1016
- API Specifications - OpenAPI 3.1
- Database Design - ERDs, schema docs

### Testing Documentation
- Test Strategy - IEEE 829
- Test Plans & Test Cases
- Test Reports

### Operational Documentation
- Deployment Guides
- Runbooks (SRE best practices)
- Monitoring & IaC Documentation

### Agile Artifacts
- Sprint Planning Documents
- Definition of Done (DoD)
- Definition of Ready (DoR)
- Retrospectives

### End-User Documentation
- User Manuals - ISO 26514
- Installation Guides
- FAQs & Troubleshooting

### Governance & Compliance
- Requirements Traceability Matrix (RTM) - IEEE 1012
- Audit Reports - IEEE 1012 V&V
- Compliance Docs (GDPR, HIPAA, SOC2)

---

## Architecture Overview

```
chwezi-sdlc-documentation/
├── 01-strategic-vision/             # PRD, vision, business case, SaaS and AI strategy
├── 02-requirements-engineering/
│   ├── waterfall/                   # Waterfall SRS skills 01 to 09
│   ├── agile/                       # User stories, acceptance criteria, backlog
│   ├── fundamentals/                # Before, during and after requirements
│   └── hybrid/                      # Water-Scrum-Fall synchronisation
├── 03-design-documentation/         # HLD, LLD, API specs
├── 04-development-artifacts/        # Technical specs, code docs
├── 05-testing-documentation/        # Test strategy, plans, reports
├── 06-deployment-operations/        # Deployment guides, runbooks
├── 07-agile-artifacts/              # Sprint planning, DoD, DoR
├── 08-end-user-documentation/       # User manuals, FAQs
├── 09-governance-compliance/        # Traceability, audits, compliance
├── engine/                          # Validation kernel (python3 -m engine)
├── domains/                         # 11 domain packs
├── scripts/, templates/, references/, rules/, hooks/, tests/, docs/
└── projects/                        # Untracked client workspaces
```

**Stateless Design:**
- Skills live under the numbered phase folders, each at `<NN-phase>/.../<skill-name>/SKILL.md`
- Project data in `projects/<ProjectName>/_context/` (legacy skill-local alias `../project_context/`)
- Generated docs in the same project workspace (legacy alias `../output/`)
- No project-specific data commits to the repository unless explicitly promoted to examples or documentation

---

## Standards Compliance

All documentation aligns with industry standards:

- **IEEE 830-1998**: Software Requirements Specifications
- **IEEE 1233-1998**: System Requirements Development
- **IEEE 1012-2016**: Verification and Validation
- **IEEE 1016-2009**: Software Design Descriptions
- **IEEE 29148-2018**: Requirements Engineering
- **IEEE 829**: Software Test Documentation
- **ISO/IEC 25010**: Software Product Quality
- **ISO 26514**: User Documentation
- **OpenAPI 3.1.x**: API Documentation (3.2.x optional where the toolchain supports it)

IEEE 830-1998 is superseded and is kept only as the SRS section layout. The status of each edition above, with source and review date, is in `docs/kaizen/2026-10-engine-kaizen-pass-2/standards-source-register.md`, and clause mappings that still cite superseded editions are listed as open findings in `README.md`.

---

## Key Features

### Methodology-Agnostic
Choose Waterfall, Agile, or Hybrid based on your project needs.

### Standards-Driven
Every document maps to specific IEEE/ISO standards with clause references. Edition status is dated in the source register (see Standards Compliance below).

### Iterative and Idempotent
Re-run skills when context changes; they update without losing work.

### Verification and Validation
Built-in IEEE 1012 auditing checks correctness, completeness and consistency, and `python3 -m engine validate` runs the phase gates.

### Domain and Cross-Engine Integration
Eleven domain packs live under `domains/`; multi-tenant, security, UI/UX, finance and research skills come from the companion engines named in `README.md`.

### Token-Efficient
Every `SKILL.md` stays at or below 500 lines (`docs/skill-authoring-standard.md`), with longer material moved to linked references.

---

## Use Cases

### Use Case 1: Medical Device SRS (Waterfall)

**Scenario:** FDA-regulated medical device requires IEEE 830 SRS

**Workflow:**
1. Run `00-meta-initialization` (engineering catalog engine) → Detects "FDA", recommends Waterfall
2. Run `02-requirements-engineering/waterfall/01-initialize-srs`
3. Populate context files (`vision.md`, `features.md`, `business_rules.md`)
4. Run phases 02-08 sequentially
5. Output: Complete SRS + Traceability Matrix + Audit Report

**Timeline:** 4-6 weeks

---

### Use Case 2: Startup MVP (Agile)

**Scenario:** E-commerce startup needs rapid iteration with user stories

**Workflow:**
1. Run `00-meta-initialization` (engineering catalog engine) → Detects "MVP", recommends Agile
2. Run `01-strategic-vision/01-prd-generation` → Lightweight PRD
3. Run `02-requirements-engineering/agile/01-user-story-generation`
4. Output: User Stories + Story Map + Sprint-ready backlog

**Timeline:** 1-2 sprints

---

### Use Case 3: Enterprise SaaS (Hybrid)

**Scenario:** SaaS platform with regulated backend + agile frontend

**Workflow:**
1. Run `00-meta-initialization` (engineering catalog engine) → Detects microservices, recommends Hybrid
2. Backend: Run `02-requirements-engineering/waterfall/` → SRS for payment service
3. Frontend: Run `02-requirements-engineering/agile/` → User stories for UI
4. Shared: Run `03-design-documentation/01-high-level-design` → Unified architecture

**Timeline:** 3-4 weeks

---

## Migration from v2.x

Existing SRS-Skills users:

**Old structure:**
```
01-initialize-srs/
02-context-engineering/
... (at root level)
```

**New structure (v3.0):**
```
02-requirements-engineering/waterfall/01-initialize-srs/
02-requirements-engineering/waterfall/02-context-engineering/
... (moved to waterfall subdirectory)
```

**Backward compatible:** Legacy paths still work with deprecation notices.

See `docs/migration/skill-paths-2026-04-16.md` for the recorded path migration.

---

## Quick Reference

| Task | Command | Output |
|------|---------|--------|
| **Select Methodology** | `00-meta-initialization` (engineering catalog engine) | `methodology.md`, `doc_roadmap.md` |
| **Waterfall SRS** | `02-requirements-engineering/waterfall/01-initialize-srs` | SRS in the IEEE 830 section layout |
| **Agile User Stories** | `02-requirements-engineering/agile/01-user-story-generation` | User story backlog |
| **High-Level Design** | `03-design-documentation/01-high-level-design` | HLD with C4 diagrams |
| **Test Plans** | `05-testing-documentation/02-test-plan` | Test plans with cases, data and exit evidence |
| **Traceability** | `09-governance-compliance/01-traceability-matrix` | RTM + audit report |

---

## Roadmap

### v3.3 (Historical - 2026-03-01)
- ✅ 100% phase coverage (all 10 SDLC phases fully implemented)
- ✅ 46 documentation generation skills in the v3.3 snapshot
- ✅ Phases 04-09 complete (Development, Testing, Deployment, Agile, End-User, Governance)

### v3.2 (2026-02-28)
- ✅ Phases 01-03 (Strategic Vision, Agile Track, Design Documentation)
- ✅ Setup scripts for project bootstrapping

### v3.1 (2026-02-07)
- ✅ AI-Assisted Development Skills

### v3.0 (2026-02-06)
- ✅ Multi-methodology support, 10 SDLC phases, methodology detection

---

## Support & Resources

- **GitHub:** https://github.com/peterbamuhigire/chwezi-sdlc-documentation
- **Issues:** https://github.com/peterbamuhigire/chwezi-sdlc-documentation/issues
- **Full Documentation:** See `README.md` in root
- **AI Assistant Guide:** See `CLAUDE.md` for AI-specific protocols

---

**Release:** 1.1.0 (`.claude-plugin/plugin.json`); the validation kernel package is 0.1.0 (`pyproject.toml`).
**Last Updated:** 2026-10-31
**Maintained by:** Peter Bamuhigire
