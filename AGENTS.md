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

This repository is a dual-compatible skill system for Claude Code and Codex. The portable unit is any directory that contains a `SKILL.md`.

## Purpose

- Preserve the existing Claude Code workflow defined in [CLAUDE.md](/C:/wamp64/www/srs-skills/CLAUDE.md).
- Expose the same skills to Codex through predictable `SKILL.md` frontmatter, local references, and repo-level routing rules.
- Keep portable skill entrypoints under `skills/<skill-name>/SKILL.md`.

## Skill Families

- Engineering/methodology skills live in the sibling **engineering catalog engine** at `C:\wamp64\www\chwezi-dev-engine` (skills under `skills/<category>/<skill-name>/SKILL.md`). Consult its router, then read the matching SKILL.md directly. Its `<category>` namespace is grouped into 17 categories (verified 2026-09-24); see the "Skill Categories" section in `CLAUDE.md`. Methodology-selection skills such as `00-meta-initialization` live at the outer numbered-phase roots (e.g. `01-strategic-vision/`).
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
- Use `01-strategic-vision/07-premium-product-positioning` whenever buyer trust, executive adoption, high-ticket pricing, affluent/elite users, or premium product experience matters.
- No generated artefact ships if it reads as AI slop. Run `09-governance-compliance/28-anti-ai-slop` as the pre-ship gate: every section must carry a concrete `_context/`-grounded element, every quality attribute a defined IEEE-982.1 / ISO 25010 metric, every requirement a deterministic test oracle, and no hallucinated API, package, or citation. Use the banned-vocabulary list and the SRS/spec avoidance block.

## Document and Spreadsheet Tooling

- Before promising `.docx`, `.pdf`, `.xlsx`, application registers, scoring matrices, budgets, monitoring dashboards, reports, or annexes, check whether document and spreadsheet tooling is available.
- Prefer built-in Codex/Claude document and spreadsheet plugins where available. If unavailable, use local Python libraries such as `openpyxl`, `XlsxWriter`, `pandas`, `python-docx`, `docxtpl`, `docxcompose`, `pypandoc`, `markdown`, `PyMuPDF`, `pypdf`, `pdfplumber`, and `reportlab`.
- Check binaries such as `pandoc`, LibreOffice/`soffice`, `wkhtmltopdf`, and `tesseract` when conversion or OCR is needed.
- Run a minimal DOCX/XLSX smoke test on a new machine before production export.
- Never claim a generated Word, PDF, or Excel file exists unless it was actually written and opened or validated.

## Compatibility Notes

- `CLAUDE.md` remains the Claude-specific root protocol and should not be replaced by this file.
- `AGENTS.md` provides Codex-facing baseline behavior and repository routing.
- `SKILL.md` files carry a portable metadata contract so both assistants can identify use conditions, inputs, workflow expectations, quality gates, anti-patterns, outputs, and references from the standard `skills/<skill-name>/SKILL.md` layout.


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


<!-- design-system-skills:trigger v1 -->
### Design / typography / UI/UX (cross-cutting — consult IN ADDITION)

Any work touching how an artifact LOOKS — font/typeface choice, type scale, colour, layout/grid,
visual identity, web/desktop/mobile UI screens, or the visual formatting of a DOCX/PPTX/PDF/XLSX
— routes to the **`design-system-skills`** engine, the single home for ALL design/UI/UX skills
and the anti-AI-slop doctrine.

**Resolve its location on THIS device from your global engine-routing table** (`~/.claude/CLAUDE.md`,
or `AGENTS.md` for Codex) — never assume an absolute path; it varies per machine. Then read its
`README.md` → `doctrine/design-doctrine.md` → glob `skills/**/SKILL.md` fresh and route by
frontmatter (read SKILL.md directly, not via the Skill tool). Content and structure stay in THIS
engine; presentation comes from design-system-skills. Hard rule: never use a banned AI-slop font
(Inter, Geist, Roboto, Arial, Open Sans, Lato, Space Grotesk, bare system stacks) as primary
type — state the chosen typeface and reason before producing any artifact.
<!-- /design-system-skills:trigger -->

## Human-English editorial standard (2026-08 Kaizen)

Load [`09-governance-compliance/28-anti-ai-slop/references/human-english-and-lexical-precision.md`](09-governance-compliance/28-anti-ai-slop/references/human-english-and-lexical-precision.md) for requirements, UX content, user manuals, FAQs, release notes, runbooks, training, support messages, and other human-facing documentation. Apply it alongside the applicable IEEE/ISO, traceability, accessibility, security, and `28-anti-ai-slop` controls.

Technical prose must remain exact: name actors, states, constraints, terminology, and test oracles. User-facing text must also be calm, respectful, grammatical, and useful in the current state. Never add errors, slang, unexplained humour, or vague adjectives to make text seem human. Record artefact type, reader/task, source traceability, terminology checks, test-oracle review, language/proof status, gaps, reviewer, and date.

The same reference carries the collocation, register, idiom, lexical-precision and calibrated-claim overlay. It strengthens the English layer; it does not override approved product terminology, accessibility rules, requirements traceability, or current Digital Research verification.

## DOMAIN PROMPT GENERATION CONTRACT

For a prompt handoff, read the local [domain prompt contract](docs/ai-prompting/domain-prompt-compilation-contract.md). Generate a ready-to-paste prompt for the named AI tool using actor and decision, supplied context, one primary intent, requirements, structure, hard constraints, risks, output contract, and acceptance checks. For SRS work, include actors, states, traceability, constraints, and deterministic test oracles; distinguish requirements discovery from implementation. Return assumptions and any NOT ASSESSED evidence. **Ready-to-paste prompt:** include the prompt package. **Failure action:** revise the smallest failed requirement or regenerate when the structure is wrong.

## PORTFOLIO CRAFT CONTRACT

Load `C:\wamp64\www\chwezi-engine-agents\docs\operations\portfolio-craft-standard-2026-09-04.md` when available. Every SRS, requirement, architecture note, and governance artefact is built in named slices: frame the actor and decision, select one flow or requirement, inspect existing context, make the smallest useful change, exercise normal and failure states, refine, and record proof before continuing. Requirements must carry concrete actors, states, constraints, and test oracles; do not generate a whole specification as one opaque batch. Apply `Observe -> Baseline -> Select -> Experiment -> Check -> Standardise -> Teach -> Re-measure` to kaizen itself. Missing execution, render, source, reviewer, or stakeholder evidence is `NOT ASSESSED`, never a pass.
