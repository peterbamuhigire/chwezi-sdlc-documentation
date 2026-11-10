# Repository Agents Guide

<!-- MODEL-ROUTING-BLOCK v2 2026-11-10 -->
## Model classes and token discipline (Claude Code, Codex and any runner; mandatory)
Name a class here, never a model version. The owner's routing file maps classes to current models (Knowledge Bank, Development, Anthropic Models: `model-routing.json`; handoff AM-01), so a model upgrade needs no edit in this repository.
- **Classes:** **M Mundane** (fastest and cheapest; mechanical work with a clear right answer); **N Normal** (default; executes an approved plan); **X Expert** (strongest standard class; plans, judges, hard debugging, final review); **S Special occasion** (premium class above X; rare; only through the seven-test gate, AM-01 s5, including approved billing). A new model is classified by relative price and vendor positioning (AM-01 s1.1). With no S class available, X is the ceiling.
- **Escalate one class, on a trigger only:** two failed acceptance checks; an undecidable choice; unreviewed money, tenant, security or legal work. Drop back after the hard step.
- **Tokens, both runners:** start-up files at most 8,000 tokens and `AGENTS.md` at most 32 KiB (Codex stops at its byte cap); one task per session, clear or new thread between tasks, compact near 80%; plan to a file, execute in a fresh session (resume a plan from its small `RESUME.md` only); read the router section then one `SKILL.md`, search instead of loading; consult only the engine whose domain matches the task; subagents and tools return summaries, cap tool output (`tool_output_token_limit`), disable unused MCP tools; stable prefix first, no instruction edits mid-session; parallel agents only with a written budget; non-interactive runs for bulk (Batch API only with an approved API budget); effort medium by default, high needs a reason, the maximum needs approval.
- **Class S case for this repository (E-06, AM-02):** a whole-specification consistency and traceability audit before a large baseline is signed off; read-only, N fixes the text. Everything else: X plans, N executes, M for mechanical work.
- **Monthly Kaizen, first step:** Anthropic currency check (AM-01 s8) and the token-budget lint; record `Anthropic currency check YYYY-MM-DD: no change|changed`.
<!-- /MODEL-ROUTING-BLOCK -->


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
Read `.codex/model-policy.md` for the full contract. Use Luna (`gpt-6-luna`) with medium reasoning by
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
standardisation decision MUST begin with the Digital Research Engine (resolve
its checkout through the engine-routing table). Read its `source-evaluation` and
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

- Preserve the existing Claude Code workflow, now held in this file; [CLAUDE.md](CLAUDE.md) is a thin bridge that imports it (portfolio bridge contract, M10-02).
- Expose the same skills to Codex through predictable `SKILL.md` frontmatter, local references, and repo-level routing rules.
- Keep each portable skill entrypoint at `<NN-phase>/.../<skill-name>/SKILL.md` under the numbered phase roots (`01-strategic-vision` to `09-governance-compliance`). This repository has no `skills/` directory.

## Reference sections (read on demand)

These sections were moved verbatim to `docs/agents-reference.md`. Open the one that applies to the task; do not load the whole file.

- Skill Families (`docs/agents-reference.md#skill-families`)
- Skill Authoring and Release Gate (`docs/agents-reference.md#skill-authoring-and-release-gate`)
- Quality Bar (`docs/agents-reference.md#quality-bar`)
- Directory Logic & Pathing (`docs/agents-reference.md#directory-logic-pathing`)
- New Project Protocol (`docs/agents-reference.md#new-project-protocol`)
- Core Engineering Principles (`docs/agents-reference.md#core-engineering-principles`)
- Skill Execution Workflow (`docs/agents-reference.md#skill-execution-workflow`)
- Compliance Skills (Uganda Domain) (`docs/agents-reference.md#compliance-skills-uganda-domain`)
- Documentation & Writing Standards (`docs/agents-reference.md#documentation-writing-standards`)
- Verification & Validation (V&V) Standard Operating Procedure (`docs/agents-reference.md#verification-validation-v-v-standard-operating-procedure`)
- Human-English editorial standard (2026-08 Kaizen) (`docs/agents-reference.md#human-english-editorial-standard-2026-08-kaizen`)

## Baseline Routing

- New client-documentation or methodology-selection requests: start with `00-meta-initialization` (engineering catalog engine).
- SDLC document generation or review: route to the relevant numbered phase skill first, then load supporting domain references from `domains/<domain>/`.
- General software engineering work: start with `sdlc-meta/world-class-engineering` in the engineering catalog engine, then add the narrowest relevant skills.
- Skill authoring or upgrades: use `sdlc-meta/skill-writing` in the engineering catalog engine.
- Word or `.docx` output quality work: use `product-business/professional-word-output` in the engineering catalog engine.
- BDS programme intake, selection, monitoring, or donor dashboard requirements: use `product-business/bds-intake-and-monitoring-system-spec` in the engineering catalog engine.
- E-commerce platform, payment, API, AI, data-protection, or integration audit requirements: use `architecture/ecommerce-platform-audit-requirements` in the engineering catalog engine.

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
- Root documentation should prefer the canonical model described in [docs/pathing-model.md](docs/pathing-model.md).

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

## Hybrid Cross-Cutting Trigger

If `projects/<ProjectName>/_context/methodology.md` declares `methodology: hybrid`, the assistant MUST invoke the `hybrid-synchronization` skill after the Phase 02 Waterfall SRS is signed off and before any Phase 07 Agile artifact is generated. The kernel will block Phase 07 outputs until `python -m engine validate <project>` passes the `hybrid` gate.

## Build Document Protocol

When the user says "build the [document]":
1. Resolve the document directory using the mapping in `00-meta-initialization/new-project/SKILL.md` in the engineering catalog engine (`00-meta-initialization/new-project/SKILL.md` there — not a path in this repo)
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


## Full Skill Suite

Refer to `README.md` for the phase table (159 active skills in nine numbered phases on 2026-10-31), to `docs/skill-catalogue.md` for the skill-by-skill list and to `PROJECT_BRIEF.md` for the engine's history. The Waterfall SRS skills run under `02-requirements-engineering/waterfall/`, from `01-initialize-srs` through `08-semantic-auditing`, with `09-use-case-modeling` alongside them.

## Skill Categories

These categories belong to the external engineering-catalog engine, NOT to this repository — this repo's own skills follow the `NN-phase/NN-skill/SKILL.md` layout described in `README.md`. The [Chwezi Dev Engine](https://github.com/peterbamuhigire/chwezi-dev-engine) organises its portable skill catalogue into category subdirectories under `skills/<category>/<skill-name>/...`. When routing to an individual skill, always include the category segment in the path.

| Category | Scope |
| --- | --- |
| `ai` | LLM integration, agent runtime, RAG, prompt engineering, AI app architecture, AI ops/eval, AI economics, AI safety/security/UX, openai-agents-sdk. |
| `android` | Android development, UI/UX, data persistence, TDD. |
| `architecture` | API design-first, REST/GraphQL patterns, microservices architecture/communication/orchestration, distributed systems patterns, contract validation, system architecture design. |
| `backend-databases` | MySQL and PostgreSQL engineering/administration/operations/performance, database design, internals and reliability, vector databases. |
| `devops-cloud` | CI/CD (pipeline design, Jenkins, DevSecOps), Docker, Kubernetes (fundamentals/platform/production/SaaS delivery), IaC, cloud architecture, deployment/release, observability, reliability engineering. |
| `finance-accounting` | Accounting engine, finance/controller, chart of accounts, payroll (Uganda), inventory costing/management, demand forecasting, fixed assets/depreciation, multicurrency/FX, chwezi finance engine skeletons. |
| `frontend-ux` | Frontend engineering only: React, Next.js App Router, Tailwind, frontend architecture/performance, Avalonia desktop, POS UI engineering standards, image compression, UX content strategy. Visual design, typography, UI/UX audits, motion, accessibility QA and design systems moved to the `chwezi-design-engine` engine. |
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

## Compliance Fail Tags (Uganda)

In addition to the standard V&V fail tags, use these for Uganda DPPA compliance:
- `[DPPA-FAIL: S-tier field not encrypted]` — special personal data field without AES-256-GCM
- `[DPPA-FAIL: no consent mechanism]` — personal data collected without lawful basis or consent FR
- `[DPPA-FAIL: breach notification > immediate]` — breach SLA longer than immediate
- `[DPPA-FAIL: no data subject rights FR]` — module collects personal data but no rights FRs
- `[DPIA-REQUIRED: <reason>]` — processing operation triggers mandatory DPIA

## Prohibited Actions

- Do not use subjective adjectives like "fast," "intuitive," or "reliable" without defining the specific IEEE-982.1 metric (see Principle 7 above).

## Anti-AI-Slop Quality Gate (MANDATORY)

Two cross-cutting skills enforce that no generated artefact reads as "AI slop" — low-quality, untestable, hallucination-prone output produced at volume:

- **`09-governance-compliance/28-anti-ai-slop`** — a **MANDATORY gate applied in REAL TIME on every generated SRS, PRD, user story, acceptance criterion, design document, test document, ADR, runbook, and code artefact**. It is a live constraint applied **continuously while generating** — to every requirement, section, criterion, and line of code as it is written, not only as a final pre-ship pass. The moment a banned word, a subjective adjective with no IEEE-982.1 metric, a generic placeholder, an unverified figure, a hallucinated API, or a template default appears, fix it in place. Run its ship-gate checklist after the Phase 09 IEEE 1012 audit and before presenting any draft at the Human Review Gate (PRIME "Inspect" step). Any unticked box promotes to the matching V&V fail tag (`[SMART-FAIL]`, `[V&V-FAIL]`, `[CONTEXT-GAP]`, `[TRACE-GAP]`, `[VERIFIABILITY-FAIL]`). Its banned-vocabulary list incorporates Principle 7: never ship "fast/intuitive/reliable/robust/scalable" without a defined IEEE-982.1 / ISO 25010 metric.
- **`09-governance-compliance/29-ai-slop-audit`** — **RUNS AFTER EACH MAJOR ITERATION (not only on request)**. Run it after each completed unit of work — each drafted SRS section, each completed design or test document, each finished module or feature, each significant revision, each phase or milestone — logging a verdict each time and mapping any blocking finding to its V&V fail tag; a grade **F blocks progression** to the next section or iteration until the blocking findings are fixed. It also **auto-runs whenever the user asks to analyse, review, evaluate, audit, critique, or "de-slop"** any spec, requirement, user story, document, system, or codebase, or asks "does this look AI-generated?", and as the final gate before a `.docx` deliverable ships. It produces a graded slop report (A–F) with per-marker evidence and a concrete fix, and maps each blocking finding to a V&V fail tag.

Both skills preserve verified evidence only: Merriam-Webster 2025 Word of the Year; Kommers et al. (arXiv 2601.06060); Spracklen et al. (USENIX Security 2025 — 19.7% package hallucination); Veracode (45% of AI code flawed, XSS 86%, log-injection 88%); GitClear duplication 8.3% (2020) → 12.3% (2024). Do not add new statistics or sources to these skills without verification.

## Git Commit Protocol for Projects

Project workspaces (`projects/<ProjectName>/`) are **local only** and gitignored — this repository is public and publishes only skills, engine code, and domain packs, not client work. Never `git add -f` a project path. Never commit the Word binary template (`templates/reference.docx`). Commits to this repo contain skill logic, engine code, domains, templates, and documentation only.

## Documentation Maintenance

- Update docs/CHANGELOG.md with every change to skill logic prompts, root protocols, or new standards; cite the Engineering Registry when the change alters input/process/output mappings.
- Keep DEPENDENCIES.md current with runtime and environment requirements so onboarding scripts and the offline workflow remain consistent.
- Quote a skill count, test count or validator result in a document only after measuring it (`find` for skills, the validator's own output for the rest), and give the date.
- Reference README.md, AGENTS.md (imported by the CLAUDE.md bridge), and other root docs when describing the documentation flow in change tickets to ensure traceability during audits.


## Finance & Accounting Trigger

Consult the finance engine (resolve its checkout through the engine-routing table) whenever the user's request, the artefact being generated, or the code being edited touches **any** of:

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

1. Consult the finance engine — start from its `README.md` router.
2. Follow the router to the relevant doctrine and reference material in that engine.
3. Read the relevant finance skill `SKILL.md` in that engine.
4. Apply the **finance & accounting quality gate** defined in that engine.
5. Record the gate run in the artefact manifest.

The `finance-module-audit` skill (in the finance engine) auto-runs whenever the user asks to analyse, review, audit, build, propose, or replace any software system with even a slight finance element.


<!-- chwezi-design-engine:trigger v4 -->
### Design / typography / UI/UX (cross-cutting — consult IN ADDITION)

Any work touching how an artifact LOOKS — font/typeface choice, type scale, colour, layout/grid,
visual identity, web/desktop/mobile UI screens, or the visual formatting of a DOCX/PPTX/PDF/XLSX
— routes to the **`chwezi-design-engine`** engine, the single home for ALL design/UI/UX skills
and the anti-AI-slop doctrine.

**Resolve its location on THIS device from the active runner's global engine-routing table or
`AGENTS.md`** — never assume an absolute path; it varies per machine. Then read its
`README.md` → `doctrine/design-doctrine.md` → glob `skills/**/SKILL.md` fresh and route by
frontmatter (read SKILL.md directly, not via the Skill tool). Content and structure stay in THIS
engine; presentation comes from chwezi-design-engine. Hard rule: never use a banned AI-slop font
as primary type — hard ban: Inter, Geist, Roboto, Open Sans, Lato, Arial, Fraunces, IBM Plex (all
faces); secondary ban: Space Grotesk, Instrument Serif, Instrument Sans, Poppins, Montserrat, Nunito, Nunito Sans, Newsreader, Cormorant (all cuts), Crimson Pro, Plus Jakarta Sans, DM Sans, Outfit, Playfair Display, Lora, Space Mono;
Roboto Mono and IBM Plex Mono are banned as monospace choices; Source Sans 3 only as a paired
body face; no bare system stacks alone. State the chosen typeface and reason before producing
any artifact.
<!-- /chwezi-design-engine:trigger -->

## DOMAIN PROMPT GENERATION CONTRACT

For a prompt handoff, read the local [domain prompt contract](docs/ai-prompting/domain-prompt-compilation-contract.md). Generate a ready-to-paste prompt for the named AI tool using actor and decision, supplied context, one primary intent, requirements, structure, hard constraints, risks, output contract, and acceptance checks. For SRS work, include actors, states, traceability, constraints, and deterministic test oracles; distinguish requirements discovery from implementation. Return assumptions and any NOT ASSESSED evidence. **Ready-to-paste prompt:** include the prompt package. **Failure action:** revise the smallest failed requirement or regenerate when the structure is wrong.

## PORTFOLIO CRAFT CONTRACT

Load `docs/operations/portfolio-craft-standard-2026-09-04.md` from `chwezi-engine-agents` (resolve it through the engine-routing table) when available. Every SRS, requirement, architecture note, and governance artefact is built in named slices: frame the actor and decision, select one flow or requirement, inspect existing context, make the smallest useful change, exercise normal and failure states, refine, and record proof before continuing. Requirements must carry concrete actors, states, constraints, and test oracles; do not generate a whole specification as one opaque batch. Apply `Observe -> Baseline -> Select -> Experiment -> Check -> Standardise -> Teach -> Re-measure` to kaizen itself. Missing execution, render, source, reviewer, or stakeholder evidence is `NOT ASSESSED`, never a pass.
