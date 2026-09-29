# Repository Agents Guide

## Codex-only model setup and Kaizen review

Apply this section only when the active runner is Codex. Claude and other
runners must skip it and retain their own models and full engine capabilities.

Before substantive Codex work, resolve this engine's directory and an available
Python 3.11+ interpreter (use its absolute path if absent from PATH), then run
`python <engine-root>/.codex/ensure_model_policy.py --runtime codex --check`.
If it reports configuration drift, Peter authorises the bounded
`--runtime codex --apply` repair, followed by `--check`. The helper backs up
changes and preserves unrelated settings. If Python or configuration access is
unavailable, report the limitation; do not replace the user's config wholesale.
Read `.codex/model-policy.md` for the full contract. Use Luna (`gpt-6-luna`) with high reasoning by
default for orchestration, research, audit, review, and implementation. Use Astra (`gpt-6-astra`) only when
Peter explicitly selects it for the task; never select or fall back to GPT-5.6. Report unavailable required GPT-6
models. A running session may need restarting for root settings to apply.


Every Kaizen cycle MUST check latest official model releases and actual
runtime availability, record dated evidence and a retain/change decision,
and evaluate better candidates before recommending replacement. Preserve the
pins until Peter authorises a verified change. Missing model-currentness
evidence is `NOT_ASSESSED`. This Codex adapter must not change CLAUDE.md,
Claude configuration, domain doctrine, permission settings or skill access.

## Universal agent integration

See `.skills-engine/engine-manifest.yaml` for the declarative contract used by the optional universal coordination package. The router and domain SKILL.md files remain authoritative.

The package may read the router, discover skills, inspect Git, and run only declared checks. Missing evidence is NOT ASSESSED; writes, pulls, publication, submissions, ledger/filing changes, deployment, or control changes require explicit approval.

Project context: if the working project root holds a `PROJECT.md` with `project_schema: 1`, read it before planning. It points to this engine's own context sources and never replaces them.

## Rules

Always-on cross-cutting principles live in `rules/` — see `rules/README.md`.
Load `rules/common/core.md` and `rules/common/phase-handoff.md` alongside the
routed skill for any non-trivial task; they are short and do not replace the
skill, only set the baseline the skill operates within.

## Mandatory Digital Research currentness gate for Kaizen

Every Kaizen audit, skill edit, reference update, validator change, and
standardisation decision MUST begin with the Digital Research Engine at
`C:\wamp64\www\digital-research-engine`. Read its `source-evaluation` and
`source-verification` skills and the currentness gate reference
`docs/continuous-improvement/kaizen-currentness-gate.md` (in the Digital Research
Engine, not this repository).

Before admitting any standard, policy, law, technology, platform capability,
software version, command, security control, benchmark, or lifecycle claim,
record source scope, publication/version date, access date, freshness class,
review date, support status, and uncertainty. Use current authoritative
primary sources; quarantine stale/ambiguous/unsupported claims and mark them
`NOT_ASSESSED`. Books are durable concept inputs only.

Before admitting any standard edition, law, platform capability, version or metric threshold into a
skill or generated requirement, follow the Digital Research Engine currentness gate described in
`AGENTS.md` (source-evaluation, source-verification, dated evidence, `NOT_ASSESSED` when unverified).
Books are durable concept inputs only.

This repository is a dual-compatible skill system for Claude Code and Codex. The portable unit is any directory that contains a `SKILL.md`.

## Purpose

- Preserve the existing Claude Code workflow, now held in this file; [CLAUDE.md](/C:/wamp64/www/srs-skills/CLAUDE.md) is a thin bridge that imports it (portfolio bridge contract, M10-02).
- Expose the same skills to Codex through predictable `SKILL.md` frontmatter, local references, and repo-level routing rules.
- Keep portable skill entrypoints under `skills/<skill-name>/SKILL.md`.

## Skill Families

- Engineering/methodology skills live in the sibling **engineering catalog engine** at `C:\wamp64\www\chwezi-dev-engine` (skills under `skills/<category>/<skill-name>/SKILL.md`). Consult its router, then read the matching SKILL.md directly. Its `<category>` namespace is grouped into 17 categories (verified 2026-09-24); see the "Skill Categories" section below. Methodology-selection skills such as `00-meta-initialization` live at the outer numbered-phase roots (e.g. `01-strategic-vision/`).
- Root directories are reserved for project documentation and repository-level folders such as `docs/` and `projects/`, plus operational folders (`engine/`, `templates/`, `scripts/`, `domains/`) where relevant. Finance/accounting is the standalone cross-cutting **finance engine** at `C:\wamp64\www\chwezi-accounting-doctrine` — consult it whenever finance/IFRS/IAS/tax/bookkeeping arises, in addition to the active work.
- Domain packs live under `domains/`. They are not skills by themselves; use them as context sources when a task is domain-specific.

## Baseline Routing

- New client-documentation or methodology-selection requests: start with `00-meta-initialization` (engineering catalog engine).
- SDLC document generation or review: route to the relevant numbered phase skill first, then load supporting domain references from `domains/<domain>/`.
- General software engineering work: start with `sdlc-meta/world-class-engineering` in the engineering catalog engine (`C:\wamp64\www\chwezi-dev-engine`), then add the narrowest relevant skills.
- Skill authoring or upgrades: use `sdlc-meta/skill-writing` in the engineering catalog engine (`C:\wamp64\www\chwezi-dev-engine`).
- Word or `.docx` output quality work: use `product-business/professional-word-output` in the engineering catalog engine (`C:\wamp64\www\chwezi-dev-engine`).
- BDS programme intake, selection, monitoring, or donor dashboard requirements: use `product-business/bds-intake-and-monitoring-system-spec` in the engineering catalog engine (`C:\wamp64\www\chwezi-dev-engine`).
- E-commerce platform, payment, API, AI, data-protection, or integration audit requirements: use `architecture/ecommerce-platform-audit-requirements` in the engineering catalog engine (`C:\wamp64\www\chwezi-dev-engine`).

## Skill Authoring and Release Gate

The shared agents, commands, hooks, evidence, and handoff contract is mapped
for SRS work in `docs/control-plane-adoption.md` and governed centrally by
`C:\wamp64\www\chwezi-dev-engine\docs\engine-control-plane.md`.

On interruption or a blocked phase, write `sdd-handoff.json` with
`python scripts/create_sdd_handoff.py`; an incomplete phase is never closed
without a resumable owner, next step, blockers, risks, and evidence list.

- The local standard is `docs/skill-authoring-standard.md`; start new skills from `templates/skill/SKILL.md`.
- Active skills are discovered from numbered phase roots. Do not maintain a hand-edited active-skill table as the source of truth.
- Books and other copyrighted sources may inform independently written skills, but raw books, OCR output, chapter reconstructions, and long extracts must never enter this repository. Keep source files outside the repository and retain only the minimum independently expressed facts or framework needed.
- See "Never store book extractions" below; the source-ingestion guardrail enforces it.
- Run `python -X utf8 scripts/source_ingestion_guardrail.py` for every skill or source-reference change; any finding blocks release.
- Before releasing any skill change, run `python -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` and `python -X utf8 scripts/routing_smoke_test.py`.
- The baseline is zero debt, not a waiver. Any structural finding, duplicate name, broken mandatory resource, routing failure, active-count drift, or template-count drift blocks release.
- Update routing fixtures when a trigger or neighbour boundary changes, and run the anti-slop audit on changed human-facing content before release.
- Anti-AI-slop pre-ship gate: run `09-governance-compliance/28-anti-ai-slop` on every generated SRS/spec/doc/code artefact before delivery (MANDATORY).
- Slop analysis/audit: `09-governance-compliance/29-ai-slop-audit` auto-runs whenever the user asks to analyse, review, evaluate, audit, critique, or de-slop any spec, requirement, document, system, or codebase, or asks "does this look AI-generated?".

## Never store book extractions

Book extractions, book summaries, chapter-by-chapter notes and book-by-book
"analysis" digests must never be stored in this repository: no
`book-extractions/`, `extracted-books/`, `book-dumps/`, `raw-books/`,
`source-books/` or `docs/book-study/` folder, and no `*-extraction.md` or
`*-books-analysis.md` files. Keeping them infringes copyright. Knowledge from
purchased books enters only as paraphrased, task-oriented skill content and
`references/` files (procedures, decision rules, checklists, rubrics,
templates, acceptance criteria, original worked examples), organised by task
rather than by the book's chapter order, with a short "Sources" line (Author
(Year) *Title*) and an Evidence/currentness note. Verbatim quotations stay rare
and under 25 words per file. Staging notes live outside the repository and are
never linked from skills or root docs. Plans, audits and change logs may name
books but must not store their content.

`python -X utf8 scripts/source_ingestion_guardrail.py` fails when an
extraction folder or extraction-named file exists, or when a skill, reference,
root document or `docs/` file links to one. The 2026-09-24 retirement is
recorded in `docs/continuous-improvement/book-extraction-retirement-2026-09-24.md`.

## Cross-Engine Handoffs

- Proposal to SRS: consume proposal scope, win themes, assumptions, exclusions, service promises, commercial options, and support commitments as discovery inputs. Convert them into requirements, acceptance criteria, traceability, risks, and evidence obligations before implementation starts.
- Website proposal to SRS: when a premium website includes portal, SaaS, ecommerce, AI, integration, data, compliance, or operational workflow scope, create SRS/PRD artefacts before website delivery commits to build details.
- SRS to implementation: hand off signed PRD/SRS, HLD/LLD, API/database specs, ADRs, UX/content/form specs, RTM, test strategy, deployment guide, go-live readiness, and customer adoption/support plan to the master engineering engine. Include a detail register for critical journeys: actors, states, data transitions, failure recovery, content/motion/accessibility intent, telemetry, and acceptance evidence so implementation and design can refine the same product slice.
- SRS to website delivery: hand off sitemap-affecting requirements, content/form requirements, accessibility and performance constraints, launch criteria, analytics events, and support obligations to the website engine.
- Implementation to maintenance/support: require runbooks, release notes, service levels, escalation rules, known issues, training materials, and feedback loops before closing Phase 06.

## Working Rules

- Treat each `SKILL.md` as the execution entrypoint and its local `references/`, `templates/`, `logic.prompt`, `protocols/`, and helper scripts as supporting assets.
- Prefer the closest local instructions over broad repo-level assumptions.
- Keep changes additive and in place. Preserve existing Claude-facing prompts, terminology, and invocation patterns unless they are actually broken.
- Do not duplicate logic between `SKILL.md` and reference files when a short link is enough.
- When a skill has both concise metadata and a longer body, use metadata for routing and the body for execution detail.

## Pathing Model

- The canonical project workspace model is `projects/<ProjectName>/...`.
- The source of truth for project context is `projects/<ProjectName>/_context/`.
- Every project workspace must include the DOCX export contract: `projects/<ProjectName>/export/`, `projects/<ProjectName>/export-docs.ps1`, and `projects/<ProjectName>/export-docs.sh`. Generated Word deliverables remain in their phase folders, then the export script copies all `.docx` files into `export/` for delivery.
- Existing skill-local references such as `../project_context/` and `../output/` should be treated as execution aliases into the active project workspace, not as a separate architecture.
- Root documentation should prefer the canonical model described in [docs/pathing-model.md](/C:/wamp64/www/srs-skills/docs/pathing-model.md).

## Quality Bar

### SDD phase-boundary control

For SDD-style feature workspaces, use the additive deterministic contract in
`docs/sdd-phase-boundary-contract.md` and run
`python scripts/validate_sdd_phase_boundaries.py --feature-dir <feature-dir>`
at the relevant boundary. Agent explanations and waivers do not replace
validator evidence; persistent waivers require owner, reason, expiry, scope,
and rollback.

- Outputs must be specific, grounded in local context, and appropriate for production or delivery review.
- Do not invent missing requirements or hidden project context.
- Use local standards, checklists, and references before falling back to generic knowledge.
- If a skill points to upstream or downstream skills, respect that sequence unless the user explicitly narrows the task.
- Premium, world-class quality is the default for this engine. SRS, PRD, UX, architecture, and business-case outputs must support premium products and serious clients by default, not commodity or lowest-cost positioning.
- Premium requirements must make value visible through product packaging, simple usable UX, buyer proof, service quality, content/SEO authority where relevant, pricing power, and high-value sales/proposal assets.
- When a project targets cheap, vague, low-trust, or sub-premium work, treat it as a poor-fit engagement. Recommend narrowing scope to a premium deliverable, raising discovery/quality requirements, or declining the work rather than lowering the SRS quality bar.
- Do not generate commodity-grade requirements, vague low-cost specifications, or documents intended to justify weak products.
- Premium requirements are specific, verifiable, outcome-linked, operationally realistic, and designed to support serious buyers and high-trust users.
- For executive, enterprise, affluent, luxury, high-ticket, or premium product contexts, invoke `01-strategic-vision/07-premium-product-positioning` before PRD/SRS finalisation.
- Premium is not marketing language in the SRS; it must appear as measurable quality, trust, onboarding, reporting, support, governance, usability, security, reliability, and service-level requirements.
- Use `01-strategic-vision/07-premium-product-positioning` whenever buyer trust, executive adoption, high-ticket pricing, affluent/elite users, or premium product experience matters.
- No generated artefact ships if it reads as AI slop. Run `09-governance-compliance/28-anti-ai-slop` as the pre-ship gate: every section must carry a concrete `_context/`-grounded element, every quality attribute a defined IEEE-982.1 / ISO 25010 metric, every requirement a deterministic test oracle, and no hallucinated API, package, or citation. Use the banned-vocabulary list and the SRS/spec avoidance block.

## Document and Spreadsheet Tooling

- Before promising `.docx`, `.pdf`, `.xlsx`, application registers, scoring matrices, budgets, monitoring dashboards, reports, or annexes, check whether document and spreadsheet tooling is available.
- Prefer built-in Codex/Claude document and spreadsheet plugins where available. If unavailable, use local Python libraries such as `openpyxl`, `XlsxWriter`, `pandas`, `python-docx`, `docxtpl`, `docxcompose`, `pypandoc`, `markdown`, `PyMuPDF`, `pypdf`, `pdfplumber`, and `reportlab`.
- Check binaries such as `pandoc`, LibreOffice/`soffice`, `wkhtmltopdf`, and `tesseract` when conversion or OCR is needed.
- Run a minimal DOCX/XLSX smoke test on a new machine before production export.
- Never claim a generated Word, PDF, or Excel file exists unless it was actually written and opened or validated.

## Compatibility Notes

- `AGENTS.md` is the single runner-neutral root protocol, routing and doctrine file for Claude Code, Codex and other runners.
- `CLAUDE.md` is a thin bridge (`@AGENTS.md`) under the portfolio bridge contract (`chwezi-engine-agents/docs/operations/claude-bridge-contract.md`); do not add doctrine to it.
- `SKILL.md` files carry a portable metadata contract so both assistants can identify use conditions, inputs, workflow expectations, quality gates, anti-patterns, outputs, and references from the standard `skills/<skill-name>/SKILL.md` layout.


## Project Mission

You are an expert Systems Architect. You are assisting in developing and executing modular, IEEE-compliant skills that reside within this repository to generate high-fidelity Software Requirements Specifications for an active project workspace.

## Directory Logic & Pathing

- **Skills:** Engineering/methodology skills live in the [Chwezi Dev Engine](https://github.com/peterbamuhigire/chwezi-dev-engine) — the engineering-catalog engine, local checkout `C:\wamp64\www\chwezi-dev-engine` (skills under `skills/<category>/<skill-name>/SKILL.md`). Consult its router (`CLAUDE.md`/`AGENTS.md`), then read the matching `SKILL.md` directly. Use these skills for methodology selection, document generation support, and reusable engineering workflows.
- **Finance/Accounting:** Finance/accounting is the standalone cross-cutting [Chwezi Accounting Doctrine](https://github.com/peterbamuhigire/chwezi-accounting-doctrine) engine (local checkout `C:\wamp64\www\chwezi-accounting-doctrine`). Resolve it through the global engine registry and consult it whenever finance, IFRS, IAS, tax, or bookkeeping arises, in addition to the active work.
- **Domain Knowledge:** Located in `/domains/`. Read the relevant domain `INDEX.md` when generating requirements for a domain-specific project.
- **Project Workspace:** Located in `projects/<ProjectName>/` (untracked, gitignored). All client documentation is built here.
- **Output Destination:** Write all generated section files to `projects/<ProjectName>/<phase>/<document>/`. Write final `.docx` files to `projects/<ProjectName>/<phase>/`.
- **Pathing:** Skill files MUST use the canonical `projects/<ProjectName>/_context/` and `projects/<ProjectName>/<phase>/` paths. Legacy `../project_context/` and `../output/` references are only permitted inside `<!-- alias-block start --> ... <!-- alias-block end -->` HTML comments and are enforced by `python -m engine validate-skills`.
- **Templates:** `templates/reference.docx` is the Pandoc Word style reference.
- **Build Script:** `scripts/build-doc.sh` stitches `.md` files into `.docx`.

## New Project Protocol

When the user says "start a new project" or equivalent:
1. Establish shared understanding before scaffolding. Use the decision-frontier method in `02-requirements-engineering/fundamentals/before/02-elicitation-toolkit/references/decision-frontier-elicitation.md`: ask only the questions whose prerequisites are settled, write the stated intent back, and stop until the owner confirms it. State the ceremony classification (bounded, architectural or spike) as set out in `02-requirements-engineering/fundamentals/before/02-elicitation-toolkit/references/ceremony-and-section-approval.md`. `superpowers:brainstorming` may be used as an optional aid where it is installed; it is not required.
2. Ask 5 questions (name, description, methodology, owner, team size) — one at a time
3. After the methodology answer, run the **hybrid-detection heuristic**: if the user answers "Agile" or "Scrum" but also describes formal documentation gates, detailed up-front requirements, or testing at the end — flag this as a potential Water-Scrum-Fall pattern and note it in `_context/vision.md`. Ask: "Does your team have a formal requirements sign-off before development begins?" A "yes" answer confirms the hybrid.
4. Deduce domain automatically from the project description using `domains/INDEX.md` keyword signals. **Uganda domain keyword signals:** `Uganda`, `BIRDC`, `PIBID`, `URA`, `EFRIS`, `PPDA`, `OAG`, `NSSF Uganda`, `NIRA`, `NIN`, `matooke`, `cooperative farmers`, `Kampala`, `Bushenyi`, `MTN MoMo`, `Airtel Money`, `parliamentary budget vote`, `ICPAU`, `DPPA`. If 2 or more Uganda signals are present, select the `uganda` domain automatically.
5. If domain is ambiguous, ask during the shared-understanding step only
6. Scaffold the full directory structure under `projects/<ProjectName>/`
7. Pre-populate `_context/` files with interview answers and guided TODO prompts
8. Copy `domains/<domain>/INDEX.md` into `_context/domain.md`
9. Inject `[DOMAIN-DEFAULT]` blocks from `domains/<domain>/references/nfr-defaults.md` into section stubs
10. Print scaffold summary showing pre-populated files and outstanding TODOs
11. Run `python -m engine new-project <Name> --methodology <m> --domain <d> --example <e>` -- the kernel handles the mechanical scaffolding including copying the chosen golden-path example into `projects/<Name>/`.

## Hybrid Cross-Cutting Trigger

If `projects/<ProjectName>/_context/methodology.md` declares `methodology: hybrid`, the assistant MUST invoke the `hybrid-synchronization` skill after the Phase 02 Waterfall SRS is signed off and before any Phase 07 Agile artifact is generated. The kernel will block Phase 07 outputs until `python -m engine validate <project>` passes the `hybrid` gate.

## Build Document Protocol

When the user says "build the [document]":
1. Resolve the document directory using the mapping in `00-meta-initialization/new-project/SKILL.md` in the engineering catalog engine (`C:\wamp64\www\chwezi-dev-engine\00-meta-initialization\new-project\SKILL.md` — not a path in this repo)
2. Check for `manifest.md` in the document directory — use it if present, otherwise sort all `*.md` files (excluding `manifest.md`) alphabetically
3. Execute: `bash scripts/build-doc.sh <doc-dir> <OutputName>`
4. Run `projects/<ProjectName>/export-docs.ps1` on Windows or `projects/<ProjectName>/export-docs.sh` on bash-capable shells to refresh `projects/<ProjectName>/export/`
5. Report both the phase-local output `.docx` path and the exported copy in `projects/<ProjectName>/export/` to the user

## Domain Injection Protocol

`[DOMAIN-DEFAULT]` tagged blocks are pre-populated at scaffold time. They are:
- Clearly marked with opening `<!-- [DOMAIN-DEFAULT: <domain>] -->` and closing `<!-- [END DOMAIN-DEFAULT] -->` tags
- Sourced from `domains/<domain>/references/nfr-defaults.md`
- Reviewed and either kept, edited, or deleted by the consultant before building
- Never silently removed by the assistant (Claude or any other runner) — only the consultant removes them


## Core Engineering Principles

1. **IEEE/ISO/ASTM Grounding:** Every requirement generated must be mapped to the standards listed in the README. Requirement quality is judged against ISO/IEC/IEEE 29148:2018 (individual and set characteristics; see Part 7 of `02-requirements-engineering/waterfall/ieee-830-compliance-checklist.md`). IEEE 830-1998 is superseded and is kept only as the SRS section layout the build pipeline and gates depend on; IEEE 1233 and ASTM E1340 remain supporting guides.
2. **Strict Grounding:** Never "hallucinate" features. If a detail is missing from `projects/<ProjectName>/_context/`, flag the gap to the user instead of making an assumption.
3. **The "Stimulus-Response" Rule:** Functional requirements (Skill 05) must follow a stimulus-response pattern to ensure they are **Verifiable**.
4. **Terminology:** Use **ISO/IEC/IEEE 24765** definitions (the successor to the superseded IEEE Std 610.12-1990; legacy 610.12 citations remain acceptable only where a client document uses them). Maintain a strict glossary in the parent project to avoid ambiguity.
5. **Technical Precision:** Use LaTeX for any mathematical logic or algorithms: $LateFee = Balance \times Rate$. Use professional, active-voice engineering prose (e.g., "The system shall..." instead of "The system can...").
6. **Minimum-Length Directive:** Output only the content required for verifiability and completeness. Every sentence must earn its length. No padding, no restatements of the obvious, no vague qualifiers. Long sentences are acceptable only when every word is load-bearing. *(Cunningham, 2013)*
7. **Prohibition on Vague Adjectives:** Do not use "fast," "intuitive," "reliable," "robust," "seamless," or similar adjectives without defining a specific metric (ISO/IEC 25010:2023 characteristic plus an ISO/IEC 25023 or IEEE 982 measure; "IEEE-982.1" tags elsewhere in this engine refer to that measure family — IEEE 982.1-2005 was replaced by IEEE 982-2024). Replace with measurable thresholds: "response time ≤ 500 ms at P95 under normal load."

## Skill Execution Workflow

> **PRIME Methodology (Kodukula & Vinueza, 2024):** Every skill execution follows the PRIME cycle — **P**repare (`_context/` files populated with real data), **R**elay (invoke the skill), **I**nspect (review output against context), **M**odify (refine and re-invoke if needed), **E**xecute (run `build-doc.sh`). Never skip Inspect and Modify — the first AI output is a draft, not a deliverable.

1. **Initialization (Skill 01):** Must check for the existence of `projects/<ProjectName>/_context/` and seed it if missing.
2. **Analysis (Prepare):** Read inputs from `projects/<ProjectName>/_context/*.md`. The `_context/` directory is the Project Input Folder (PIF) — the richer the context files, the higher the output quality. Also read `_context/glossary.md` if it exists — every domain-specific term used in generated output must appear there. Flag any term that is used but not defined as `[GLOSSARY-GAP: <term>]` and list all gaps in the Human Review Gate step.
3. **Synthesis (Relay):** Generate the specific SRS section based on the skill's theme.
4. **Human Review Gate (Inspect):** Present the generated output to the consultant before proceeding. Explicitly list all `[CONTEXT-GAP]` flags and all `[V&V-FAIL]` tags. Do NOT run downstream skills until the consultant acknowledges review. *(Etter, 2016 — "AI-generated content must be human-verified; verification is not optional.")*
5. **Validation (Modify):** Apply consultant feedback; re-invoke the skill if context files were updated. Check against the "Correct, Unambiguous, Complete" criteria of IEEE 830.

## Full Skill Suite

Refer to `README.md` and `PROJECT_BRIEF.md` for the new eight-phase skill flow: Initialization, Introduction, Overview, Interfaces, Functional Requirements, Logic Modeling, Attribute Mapping, and Semantic Auditing with verification artifacts.

## Skill Categories

These categories belong to the external engineering-catalog engine (`C:\wamp64\www\chwezi-dev-engine`), NOT to this repository — this repo's own skills follow the `NN-phase/NN-skill/SKILL.md` layout described in `README.md`. The [Chwezi Dev Engine](https://github.com/peterbamuhigire/chwezi-dev-engine) organises its portable skill catalogue into category subdirectories under `skills/<category>/<skill-name>/...`. When routing to an individual skill, always include the category segment in the path.

| Category | Scope |
| --- | --- |
| `ai` | LLM integration, agent runtime, RAG, prompt engineering, AI app architecture, AI ops/eval, AI economics, AI safety/security/UX, openai-agents-sdk. |
| `android` | Android development, UI/UX, data persistence, TDD. |
| `architecture` | API design-first, REST/GraphQL patterns, microservices architecture/communication/orchestration, distributed systems patterns, contract validation, system architecture design. |
| `backend-databases` | MySQL and PostgreSQL engineering/administration/operations/performance, database design, internals and reliability, vector databases. |
| `devops-cloud` | CI/CD (pipeline design, Jenkins, DevSecOps), Docker, Kubernetes (fundamentals/platform/production/SaaS delivery), IaC, cloud architecture, deployment/release, observability, reliability engineering. |
| `finance-accounting` | Accounting engine, finance/controller, chart of accounts, payroll (Uganda), inventory costing/management, demand forecasting, fixed assets/depreciation, multicurrency/FX, chwezi finance engine skeletons. |
| `frontend-ux` | Frontend engineering only: React, Next.js App Router, Tailwind, frontend architecture/performance, Avalonia desktop, POS UI engineering standards, image compression, UX content strategy. Visual design, typography, UI/UX audits, motion, accessibility QA and design systems moved to the `design-system-skills` engine. |
| `execution-plan-scripts` | Converting an approved long-running plan into self-contained execution prompts with dependency order, checkpoints and evidence handoff. |
| `game-development` | Game build engineering: 2D/3D asset pipelines (incl. Blender), audio, AI behaviour, accessibility/localisation, build and platform release. |
| `gis` | GIS mapping, maps integration, PostGIS backend, platform engineering, enterprise GIS domain. |
| `ios` | iOS development, architecture, data persistence, UI/UX, AI/ML, monetization, platform capabilities, quality/release, security/RBAC; macOS AppKit/sandbox/system-integrations/git-libgit2; Swift concurrency; Xcode Cloud/TestFlight, Instruments, project engineering. |
| `languages` | JavaScript modern/patterns, TypeScript (mastery/effective/full-stack/patterns), Node.js, Python (modern, data analytics, data pipelines, ML predictive, SaaS integration), PHP modern/security, language standards. |
| `mobile-cross` | KMP development, PWA offline-first, mobile platform operations, mobile reports. |
| `product-business` | Product strategy/vision, product discovery, product-led growth, premium product positioning/execution, software business models/pricing, growth telemetry, experiment engineering, customer service, content writing, IT proposal writing, Excel spreadsheets, professional Word output. |
| `saas` | SaaS architecture strategy, modular/multi-tenant, control plane, admin/backoffice, lifecycle email, entitlements/plan gating, rate limiting/quotas, SSO/SCIM enterprise auth, tenant onboarding/portability/erasure, deployment models, business metrics, SaaS ERP/accounting design, subscription billing, Stripe payments, seeder, sales organization. |
| `sdlc-meta` | World-class engineering, engineering management/strategy, advanced testing strategy, E2E testing, AI-assisted development, git collaboration workflow, plan implementation, project requirements, SDLC (planning/design/documentation/testing/user-deploy), doc-architect (incl. markdown lint, code tours, doc maintenance), capability matrix, continuous improvement, custom sub-agents, implementation status auditor, skill-writing, skill-engine-audit (incl. skill safety gate), skill composition standards. |
| `security` | Code safety scanner, DPIA generator, dual-auth RBAC, Linux security hardening, network security, Uganda DPPA compliance, vibe security skill, web app security audit. |

To locate a specific skill quickly, resolve the Chwezi Dev Engine through the global engine registry, inspect `skills/<category>/`, then read the matching `<skill-name>/SKILL.md`.

## Compliance Skills (Uganda Domain)

For Uganda-based projects, two additional compliance skills are available and should be invoked as cross-cutting tasks alongside the main SRS skill flow:

- **`uganda-dppa-compliance`** — Generates the DPPA 2019 compliance annex: PII inventory, classification (financial info = special personal data), consent FRs, data subject rights FRs, breach notification procedure (immediate → PDPO), retention/destruction schedule, DPIA trigger assessment, DPO/PDPO registration requirements. Invoke after Skill 05 (Functional Requirements) for any module that collects personal data.
- **`dpia-generator`** — Generates a Regulation 12-compliant DPIA document for any processing operation flagged `[DPIA-REQUIRED]`. Invoke when `uganda-dppa-compliance` raises a DPIA flag.

## Compliance Fail Tags (Uganda)

In addition to the standard V&V fail tags, use these for Uganda DPPA compliance:
- `[DPPA-FAIL: S-tier field not encrypted]` — special personal data field without AES-256-GCM
- `[DPPA-FAIL: no consent mechanism]` — personal data collected without lawful basis or consent FR
- `[DPPA-FAIL: breach notification > immediate]` — breach SLA longer than immediate
- `[DPPA-FAIL: no data subject rights FR]` — module collects personal data but no rights FRs
- `[DPIA-REQUIRED: <reason>]` — processing operation triggers mandatory DPIA

## Documentation & Writing Standards

These rules apply to all generated output — SRS sections, design documents, test plans, and skill template files.

### Three-Emphasis Rule *(Cunningham, 2013; Etter, 2016)*
- `**Bold**` — UI element names, field labels, and requirement identifiers only: "Click **Save**." / "**FR-001**"
- `*Italic*` — critical warnings, caveats, and first introduction of defined terms only
- `` `Monospace` `` — file paths, terminal commands, environment variable names, code, and system identifiers
- Never bold more than 4 consecutive words in body text. Never combine bold and italic on the same element. Underline is prohibited.

### List Formatting Rules
- **Ordered lists are mandatory for all sequential procedures** — every numbered procedure must use `1.`, `2.`, `3.`, never prose paragraphs.
- Bullet items that are complete sentences get a period. Bullet items that are phrases do not.
- All items in a list must follow the same grammatical pattern (parallel structure).
- A lead-in sentence ending with a colon treats the bullet items as continuations of that sentence.

### Heading Standards
- Headings must stand on their own — not just label a category. "Requirements" is weak; "Functional Requirements for the Loan Processing Module" is informative.
- Choose one capitalization style per document and hold it throughout.

### Numbers in Technical Documents
- Always use figures (not words) for: version numbers, section references, page numbers, measurements, performance thresholds, and data values.
- "Section 3.2.1" not "section three point two." "Response time ≤ 2 seconds" not "two seconds."
- Percentages always use the % symbol.

### Markdown Syntax Rules *(Etter, 2016; Cone, 2023)*
- **Unordered lists:** Always use `-` as the bullet character. Never use `*` or `+`.
- **Headings:** Never use `---` or `===` underline-style headings. Always use ATX-style `#` prefixes. The `---` underline syntax conflicts with Pandoc YAML front matter and horizontal rule detection.
- **Table cells:** Never place nested lists, blockquotes, or fenced code blocks inside a Markdown table cell. Use a footnote reference instead.
- **Blank lines:** Always place a blank line before and after: headings, fenced code blocks, blockquotes, and tables. Omitting blank lines causes Pandoc rendering errors.
- **Emphasis syntax:** Always use asterisks (`**bold**`, `*italic*`), never underscores (`__bold__`, `_italic_`). Underscores have inconsistent behaviour inside words.

### Acronyms and Glossary *(M-09)*
- Every IEEE standard, domain acronym, and project-specific term must be defined in `_context/glossary.md`.
- Spell out on first use in the document: "Software Requirements Specification (SRS)" — then "SRS" thereafter.
- Undefined acronym in a delivered SRS = audit anomaly. Flag with `[GLOSSARY-GAP: <term>]`.

## Prohibited Actions

- Do not use subjective adjectives like "fast," "intuitive," or "reliable" without defining the specific IEEE-982.1 metric (see Principle 7 above).

## Anti-AI-Slop Quality Gate (MANDATORY)

Two cross-cutting skills enforce that no generated artefact reads as "AI slop" — low-quality, untestable, hallucination-prone output produced at volume:

- **`09-governance-compliance/28-anti-ai-slop`** — a **MANDATORY gate applied in REAL TIME on every generated SRS, PRD, user story, acceptance criterion, design document, test document, ADR, runbook, and code artefact**. It is a live constraint applied **continuously while generating** — to every requirement, section, criterion, and line of code as it is written, not only as a final pre-ship pass. The moment a banned word, a subjective adjective with no IEEE-982.1 metric, a generic placeholder, an unverified figure, a hallucinated API, or a template default appears, fix it in place. Run its ship-gate checklist after the Phase 09 IEEE 1012 audit and before presenting any draft at the Human Review Gate (PRIME "Inspect" step). Any unticked box promotes to the matching V&V fail tag (`[SMART-FAIL]`, `[V&V-FAIL]`, `[CONTEXT-GAP]`, `[TRACE-GAP]`, `[VERIFIABILITY-FAIL]`). Its banned-vocabulary list incorporates Principle 7: never ship "fast/intuitive/reliable/robust/scalable" without a defined IEEE-982.1 / ISO 25010 metric.
- **`09-governance-compliance/29-ai-slop-audit`** — **RUNS AFTER EACH MAJOR ITERATION (not only on request)**. Run it after each completed unit of work — each drafted SRS section, each completed design or test document, each finished module or feature, each significant revision, each phase or milestone — logging a verdict each time and mapping any blocking finding to its V&V fail tag; a grade **F blocks progression** to the next section or iteration until the blocking findings are fixed. It also **auto-runs whenever the user asks to analyse, review, evaluate, audit, critique, or "de-slop"** any spec, requirement, user story, document, system, or codebase, or asks "does this look AI-generated?", and as the final gate before a `.docx` deliverable ships. It produces a graded slop report (A–F) with per-marker evidence and a concrete fix, and maps each blocking finding to a V&V fail tag.

Both skills preserve verified evidence only: Merriam-Webster 2025 Word of the Year; Kommers et al. (arXiv 2601.06060); Spracklen et al. (USENIX Security 2025 — 19.7% package hallucination); Veracode (45% of AI code flawed, XSS 86%, log-injection 88%); GitClear duplication 8.3% (2020) → 12.3% (2024). Do not add new statistics or sources to these skills without verification.

## Git Commit Protocol for Projects

Project workspaces (`projects/<ProjectName>/`) are **local only** and gitignored — this repository is public and publishes only skills, engine code, and domain packs, not client work. Never `git add -f` a project path. Never commit the Word binary template (`templates/reference.docx`). Commits to this repo contain skill logic, engine code, domains, templates, and documentation only.

## Verification & Validation (V&V) Standard Operating Procedure

### IEEE 1012 Evaluation Framework

- **Correctness:** Confirm the requirement mirrors the stakeholder intent documented in `projects/<ProjectName>/_context/vision.md`, using Anomaly Identification to flag deviations.
- **Consistency:** Ensure terminology and logical structure are uniform across sections (e.g., Section 3.1 aligns with Section 3.2) by referencing the Integrity Level of each artifact.
- **Completeness:** Verify every Edge Case captured in context files has a corresponding functional requirement; mark omissions via Baseline Verification notes.
- **Verifiability:** Confirm that a deterministic test case with a clear pass/fail criterion exists for every requirement, and annotate the test expectation directly beside the requirement.

### Audit Execution Loop (Skill 08)

1. **Traceability:** Verify that every functional requirement in Section 3.2 has a unique identifier and links back to a business goal in Section 1.2. Record unresolved links as Anomaly Identification artifacts.
2. **Logic Scrutiny:** Recalculate every LaTeX formula in Section 3.2.x, ensuring numerical expressions yield consistent Integrity Levels and documenting any deviations.
3. **Conflict Resolution:** Search Section 3.4 for Design Constraints that may render any System Feature in Section 3.2 unimplementable; log each conflict and recommend remediation.

### Filling Context Gaps

When the kernel reports `[CONTEXT-GAP: <topic>]`, consult `00-meta-initialization/new-project/prompts/context-gap-fillers.md` in the engineering catalog engine (`C:\wamp64\www\chwezi-dev-engine\00-meta-initialization\new-project\prompts\context-gap-fillers.md` — not a path in this repo) before authoring from scratch. It contains an opinionated prompt per topic you can paste into a fresh assistant session.

### Failure Protocols

- When a requirement fails any audit criterion, tag it with the appropriate fail tag and append a remediation step naming the missing or conflicting element.
- The failing artifact is returned to the originating skill's owner for correction before any downstream skill runs, preventing anomaly propagation.

**Fail Tags:**
- `[V&V-FAIL: <reason>]` — requirement fails verification/validation (e.g., "Missing data type for input field X"; "Expected result is not a test oracle")
- `[CONTEXT-GAP: <topic>]` — required context is absent from `_context/` files
- `[GLOSSARY-GAP: <term>]` — term used in output is not defined in `_context/glossary.md`
- `[SMART-FAIL: NFR not measurable]` — non-functional requirement lacks a specific, measurable metric
- `[TRACE-GAP: <FR-ID>]` — functional requirement has no traceability to a business goal or test case
- `[VERIFIABILITY-FAIL: <reason>]` — expected result is not a deterministic test oracle (judgment call required)

### Quality Constraints

- The tone remains formal, prescriptive, and objective; do not soften findings with marketing language.
- Document Integrity Level, Baseline Verification, and Anomaly Identification for every V&V action so review artifacts remain auditable under ISO/IEC 15504.
- Treat this SOP as the operating contract for Skill 08; no iteration resumes until the Verification Gateways confirm closure.

### Project Registries

Every project workspace MUST contain `_registry/identifiers.yaml` and `_registry/glossary.yaml`. Generate or refresh them with:

```bash
python -m engine sync projects/<ProjectName>
```

Manual edits to these files are allowed for `links:` and `title:` fields. Identifier `id`, `kind`, and `defined_in` fields are derived from the artifacts and will be overwritten on the next sync.

The validation kernel (`python -m engine validate <project>`) will fail if:

- An artifact references an ID that is not in `identifiers.yaml` (`phase09.id_registry.unknown_id`).
- A registry entry is orphaned — no artifact mentions it (`phase09.id_registry.orphan_id`).
- A domain-specific term is used in artifacts but missing from `glossary.yaml` (`phase09.glossary_registry.missing_term`).
- A glossary term is defined but never referenced (`phase09.glossary_registry.orphan_term`).
- Two NFRs specify contradicting thresholds for the same metric (`phase09.nfr_threshold_dedup.contradiction`).

### Governance Artifacts

- **ADR catalog** — every significant architectural decision is captured as `projects/<ProjectName>/09-governance-compliance/05-adr/NNNN-slug.md` and indexed in `_registry/adr-catalog.yaml`.
- **Change Impact Analysis** — any change to a baselined FR/NFR/CTRL requires a CIA entry in `_registry/change-impact.yaml` with a rollback plan.
- **Baseline snapshots** — run `python -m engine baseline snapshot <project> --label vX.Y` at each phase closure; `python -m engine baseline diff <project> old new` produces a reviewable delta.
- **Waivers** — `python -m engine waive <project> --gate <gate_id> --reason "..." --approver "..." --days N` appends a waiver to `_registry/waivers.yaml`. Max 90 days.
- **Sign-off ledger** — `python -m engine signoff <project> --gate phaseNN --signer "..." --role "..." --artifact path1 --artifact path2`. Required before the next phase begins.
- **Evidence pack** — `python -m engine pack <project> --out <project>/evidence-pack-<date>.zip` assembles an auditor-ready bundle.

## Documentation Maintenance

- Update docs/CHANGELOG.md with every change to skill logic prompts, root protocols, or new standards; cite the Engineering Registry when the change alters input/process/output mappings.
- Keep DEPENDENCIES.md current with runtime and environment requirements so onboarding scripts and the offline workflow remain consistent.
- Reference README.md, AGENTS.md (imported by the CLAUDE.md bridge), and other root docs when describing the documentation flow in change tickets to ensure traceability during audits.


## Finance & Accounting Trigger

Consult the finance engine at `C:\wamp64\www\chwezi-accounting-doctrine` whenever the user's request, the artefact being generated, or the code being edited touches **any** of:

- Money flows: sales, purchases, payments, refunds, credit notes, expenses
- Stock and inventory
- Payroll
- Tax (VAT, PAYE, WHT, NSSF, income tax, customs, excise, EFRIS, eTIMS)
- Grants, donations, donor restrictions
- Banking, mobile money, POS, card settlement, cash drawer
- Fixed assets
- Financial reports, management accounts, statutory returns
- Chart of Accounts, journals, ledger, posting services, period state, audit trail
- Reconciliation, close, migration, opening balances
- Internal controls, audit, evidence packs
- Any IFRS or IFRS for SMEs section

When the trigger fires:

1. Consult the finance engine at `C:\wamp64\www\chwezi-accounting-doctrine` — start from its `README.md` router.
2. Follow the router to the relevant doctrine and reference material in that engine.
3. Read the relevant finance skill `SKILL.md` in that engine.
4. Apply the **finance & accounting quality gate** defined in that engine.
5. Record the gate run in the artefact manifest.

The `finance-module-audit` skill (in the finance engine at `C:\wamp64\www\chwezi-accounting-doctrine`) auto-runs whenever the user asks to analyse, review, audit, build, propose, or replace any software system with even a slight finance element.


<!-- design-system-skills:trigger v2 -->
### Design / typography / UI/UX (cross-cutting — consult IN ADDITION)

Any work touching how an artifact LOOKS — font/typeface choice, type scale, colour, layout/grid,
visual identity, web/desktop/mobile UI screens, or the visual formatting of a DOCX/PPTX/PDF/XLSX
— routes to the **`design-system-skills`** engine, the single home for ALL design/UI/UX skills
and the anti-AI-slop doctrine.

**Resolve its location on THIS device from the active runner's global engine-routing table or
`AGENTS.md`** — never assume an absolute path; it varies per machine. Then read its
`README.md` → `doctrine/design-doctrine.md` → glob `skills/**/SKILL.md` fresh and route by
frontmatter (read SKILL.md directly, not via the Skill tool). Content and structure stay in THIS
engine; presentation comes from design-system-skills. Hard rule: never use a banned AI-slop font
as primary type — hard ban: Inter, Geist, Roboto, Open Sans, Lato, Arial, Fraunces, IBM Plex (all
faces); secondary ban: Space Grotesk, Instrument Serif, Poppins, Montserrat, Nunito, Nunito Sans;
Roboto Mono and IBM Plex Mono are banned as monospace choices; Source Sans 3 only as a paired
body face; no bare system stacks alone. State the chosen typeface and reason before producing
any artifact.
<!-- /design-system-skills:trigger -->

## Human-English editorial standard (2026-08 Kaizen)

Load [`09-governance-compliance/28-anti-ai-slop/references/human-english-and-lexical-precision.md`](09-governance-compliance/28-anti-ai-slop/references/human-english-and-lexical-precision.md) for requirements, UX content, user manuals, FAQs, release notes, runbooks, training, support messages, and other human-facing documentation. Apply it alongside the applicable IEEE/ISO, traceability, accessibility, security, and `28-anti-ai-slop` controls.

Technical prose must remain exact: name actors, states, constraints, terminology, and test oracles. User-facing text must also be calm, respectful, grammatical, and useful in the current state. Never add errors, slang, unexplained humour, or vague adjectives to make text seem human. Record artefact type, reader/task, source traceability, terminology checks, test-oracle review, language/proof status, gaps, reviewer, and date.

The same reference carries the collocation, register, idiom, lexical-precision and calibrated-claim overlay. It strengthens the English layer; it does not override approved product terminology, accessibility rules, requirements traceability, or current Digital Research verification.

## DOMAIN PROMPT GENERATION CONTRACT

For a prompt handoff, read the local [domain prompt contract](docs/ai-prompting/domain-prompt-compilation-contract.md). Generate a ready-to-paste prompt for the named AI tool using actor and decision, supplied context, one primary intent, requirements, structure, hard constraints, risks, output contract, and acceptance checks. For SRS work, include actors, states, traceability, constraints, and deterministic test oracles; distinguish requirements discovery from implementation. Return assumptions and any NOT ASSESSED evidence. **Ready-to-paste prompt:** include the prompt package. **Failure action:** revise the smallest failed requirement or regenerate when the structure is wrong.

## PORTFOLIO CRAFT CONTRACT

Load `C:\wamp64\www\chwezi-engine-agents\docs\operations\portfolio-craft-standard-2026-09-04.md` when available. Every SRS, requirement, architecture note, and governance artefact is built in named slices: frame the actor and decision, select one flow or requirement, inspect existing context, make the smallest useful change, exercise normal and failure states, refine, and record proof before continuing. Requirements must carry concrete actors, states, constraints, and test oracles; do not generate a whole specification as one opaque batch. Apply `Observe -> Baseline -> Select -> Experiment -> Check -> Standardise -> Teach -> Re-measure` to kaizen itself. Missing execution, render, source, reviewer, or stakeholder evidence is `NOT ASSESSED`, never a pass.
