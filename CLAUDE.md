# AI Assistant Protocol: SRS-Skills

## Project Mission

You are an expert Systems Architect. You are assisting in developing and executing modular, IEEE-compliant skills that reside within this repository to generate high-fidelity Software Requirements Specifications for an active project workspace.

## Directory Logic & Pathing

- **Repository Root:** This directory (where root project documentation and repository-level folders live).
- **Skills:** Engineering/methodology skills live in the [Chwezi Dev Engine](https://github.com/peterbamuhigire/chwezi-dev-engine) — the engineering-catalog engine, local checkout `C:\wamp64\www\chwezi-dev-engine` (skills under `skills/<category>/<skill-name>/SKILL.md`). Consult its router (`CLAUDE.md`/`AGENTS.md`), then read the matching `SKILL.md` directly. Use these skills for methodology selection, document generation support, and reusable engineering workflows.
- **Finance/Accounting:** Finance/accounting is the standalone cross-cutting [Chwezi Accounting Doctrine](https://github.com/peterbamuhigire/chwezi-accounting-doctrine) engine (local checkout `C:\wamp64\www\chwezi-accounting-doctrine`). Resolve it through the global engine registry and consult it whenever finance, IFRS, IAS, tax, or bookkeeping arises, in addition to the active work.
- **Domain Knowledge:** Located in `/domains/`. Read the relevant domain `INDEX.md` when generating requirements for a domain-specific project.
- **Project Workspace:** Located in `projects/<ProjectName>/` (untracked, gitignored). All client documentation is built here.
- **Context Source of Truth:** Read all project-specific data from `projects/<ProjectName>/_context/`.
- **Output Destination:** Write all generated section files to `projects/<ProjectName>/<phase>/<document>/`. Write final `.docx` files to `projects/<ProjectName>/<phase>/`.
- **DOCX Export Contract:** Every project workspace MUST contain `projects/<ProjectName>/export/`, `projects/<ProjectName>/export-docs.ps1`, and `projects/<ProjectName>/export-docs.sh`. After building `.docx` deliverables, run the appropriate export script so `export/` contains a flat delivery copy of every generated Word document.
- **Pathing:** Skill files MUST use the canonical `projects/<ProjectName>/_context/` and `projects/<ProjectName>/<phase>/` paths. Legacy `../project_context/` and `../output/` references are only permitted inside `<!-- alias-block start --> ... <!-- alias-block end -->` HTML comments and are enforced by `python -m engine validate-skills`.
- **Templates:** `templates/reference.docx` is the Pandoc Word style reference.
- **Build Script:** `scripts/build-doc.sh` stitches `.md` files into `.docx`.

## New Project Protocol

When the user says "start a new project" or equivalent:
1. Invoke `superpowers:brainstorming` first — mandatory, no exceptions
2. Ask 5 questions (name, description, methodology, owner, team size) — one at a time
3. After the methodology answer, run the **hybrid-detection heuristic**: if the user answers "Agile" or "Scrum" but also describes formal documentation gates, detailed up-front requirements, or testing at the end — flag this as a potential Water-Scrum-Fall pattern and note it in `_context/vision.md`. Ask: "Does your team have a formal requirements sign-off before development begins?" A "yes" answer confirms the hybrid.
4. Deduce domain automatically from the project description using `domains/INDEX.md` keyword signals. **Uganda domain keyword signals:** `Uganda`, `BIRDC`, `PIBID`, `URA`, `EFRIS`, `PPDA`, `OAG`, `NSSF Uganda`, `NIRA`, `NIN`, `matooke`, `cooperative farmers`, `Kampala`, `Bushenyi`, `MTN MoMo`, `Airtel Money`, `parliamentary budget vote`, `ICPAU`, `DPPA`. If 2 or more Uganda signals are present, select the `uganda` domain automatically.
5. If domain is ambiguous, ask during brainstorming session only
5. Scaffold the full directory structure under `projects/<ProjectName>/`
6. Pre-populate `_context/` files with interview answers and guided TODO prompts
7. Copy `domains/<domain>/INDEX.md` into `_context/domain.md`
8. Inject `[DOMAIN-DEFAULT]` blocks from `domains/<domain>/references/nfr-defaults.md` into section stubs
9. Print scaffold summary showing pre-populated files and outstanding TODOs
10. Run `python -m engine new-project <Name> --methodology <m> --domain <d> --example <e>` -- the kernel handles the mechanical scaffolding including copying the chosen golden-path example into `projects/<Name>/`.

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
- Never silently removed by Claude — only the consultant removes them

## Core Engineering Principles

1. **IEEE/ISO/ASTM Grounding:** Every requirement generated must be mapped to the standards listed in the README. Requirement quality is judged against ISO/IEC/IEEE 29148:2018 (individual and set characteristics; see Part 7 of `02-requirements-engineering/waterfall/ieee-830-compliance-checklist.md`). IEEE 830-1998 is superseded and is kept only as the SRS section layout the build pipeline and gates depend on; IEEE 1233 and ASTM E1340 remain supporting guides.
2. **Strict Grounding:** Never "hallucinate" features. If a detail is missing from `projects/<ProjectName>/_context/`, flag the gap to the user instead of making an assumption.
3. **The "Stimulus-Response" Rule:** Functional requirements (Skill 05) must follow a stimulus-response pattern to ensure they are **Verifiable**.
4. **Terminology:** Use **ISO/IEC/IEEE 24765** definitions (the successor to the superseded IEEE Std 610.12-1990; legacy 610.12 citations remain acceptable only where a client document uses them). Maintain a strict glossary in the parent project to avoid ambiguity.
5. **Technical Precision:** Use LaTeX for any mathematical logic or algorithms: $LateFee = Balance \times Rate$. Use professional, active-voice engineering prose (e.g., "The system shall..." instead of "The system can...").
6. **Minimum-Length Directive:** Output only the content required for verifiability and completeness. Every sentence must earn its length. No padding, no restatements of the obvious, no vague qualifiers. Long sentences are acceptable only when every word is load-bearing. *(Cunningham, 2013)*
7. **Prohibition on Vague Adjectives:** Do not use "fast," "intuitive," "reliable," "robust," "seamless," or similar adjectives without defining a specific metric (ISO/IEC 25010:2023 characteristic plus an ISO/IEC 25023 or IEEE 982 measure; "IEEE-982.1" tags elsewhere in this engine refer to that measure family — IEEE 982.1-2005 was replaced by IEEE 982-2024). Replace with measurable thresholds: "response time ≤ 500 ms at P95 under normal load."

## Premium Default

This SRS engine is for premium, world-class systems work. Do not generate commodity-grade requirements, vague low-cost specifications, or documents intended to justify weak products. If a client or project brief implies sub-premium work, either narrow the scope to a premium deliverable or flag the engagement as poor fit.

Premium requirements must make value visible through product packaging, simple usable UX, buyer proof, service quality, content/SEO authority where relevant, pricing power, and high-value sales/proposal assets.

- Premium requirements are specific, verifiable, outcome-linked, operationally realistic, and designed to support serious buyers and high-trust users.
- For executive, enterprise, affluent, luxury, high-ticket, or premium product contexts, invoke `01-strategic-vision/07-premium-product-positioning` before PRD/SRS finalisation.
- Premium is not marketing language in the SRS; it must appear as measurable quality, trust, onboarding, reporting, support, governance, usability, security, reliability, and service-level requirements.

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

## Skill authoring gate

Use `docs/skill-authoring-standard.md` and `templates/skill/SKILL.md` for every skill change. Release requires both zero-debt checks:

```powershell
python -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json
python -X utf8 scripts/routing_smoke_test.py
```

Do not waive a finding through the baseline. Update routing fixtures when a trigger or neighbour boundary changes, and run the anti-slop audit on changed human-facing content before release.

## Never store book extractions

Book extractions, book summaries, chapter-by-chapter notes and book-by-book analysis digests must
never be stored in this repository (no `book-extractions/`, `extracted-books/` or `docs/book-study/`
folder, no `*-extraction.md` or `*-books-analysis.md` files). Keeping them infringes copyright.
Knowledge from purchased books enters only as paraphrased, task-oriented skill content and
`references/` files (procedures, decision rules, checklists, templates, acceptance criteria,
original worked examples) organised by task, with a short citation (Author (Year) *Title*) and an
Evidence/currentness note. Verbatim quotations stay rare and under 25 words. Staging notes live
outside the repository and are never linked from skills. `scripts/source_ingestion_guardrail.py`
fails if an extraction folder or extraction-named file exists or if a skill, reference, root doc or
`docs/` file links to one; plan and audit documents may name books but not store their content.

## Currentness gate

Before admitting any standard edition, law, platform capability, version or metric threshold into a
skill or generated requirement, follow the Digital Research Engine currentness gate described in
`AGENTS.md` (source-evaluation, source-verification, dated evidence, `NOT_ASSESSED` when unverified).
Books are durable concept inputs only.

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
- Reference README.md, CLAUDE.md, and other root docs when describing the documentation flow in change tickets to ensure traceability during audits.


## Finance & Accounting Trigger

Consult the [Chwezi Accounting Doctrine](https://github.com/peterbamuhigire/chwezi-accounting-doctrine) engine whenever the user's request, the artefact being generated, or the code being edited touches **any** of:

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

1. Resolve the Chwezi Accounting Doctrine through the global engine registry and start from its `README.md` router.
2. Follow the router to the relevant doctrine and reference material in that engine.
3. Read the relevant finance skill `SKILL.md` in that engine.
4. Apply the **finance & accounting quality gate** defined in that engine.
5. Record the gate run in the artefact manifest.

The `finance-module-audit` skill in the Chwezi Accounting Doctrine auto-runs whenever the user asks to analyse, review, audit, build, propose, or replace any software system with even a slight finance element.


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
as primary type — hard ban: Inter, Geist, Roboto, Open Sans, Lato, Arial, Fraunces, IBM Plex (all
faces); secondary ban: Space Grotesk, Instrument Serif, Poppins, Montserrat, Nunito, Nunito Sans;
Roboto Mono and IBM Plex Mono are banned as monospace choices; Source Sans 3 only as a paired
body face; no bare system stacks alone. State the chosen typeface and reason before producing
any artifact.
<!-- /design-system-skills:trigger -->
