# Reference sections moved out of AGENTS.md

Moved verbatim on 2026-11-10 to keep the always-loaded file small (token economy; Codex reads at most 32 KiB of AGENTS.md). Open the section you need.

## Skill Families

- Engineering/methodology skills live in the sibling **engineering catalog engine** (resolve its checkout through the engine-routing table; skills under `skills/<category>/<skill-name>/SKILL.md`). Consult its router, then read the matching SKILL.md directly. Its `<category>` namespace is grouped into 17 categories (re-verified 2026-10-31 with `ls skills` in that checkout); see the "Skill Categories" section below. Methodology selection (`00-meta-initialization`) sits at the root of that engine, outside its `skills/` tree; this repository's own skills sit under its numbered phase roots.
- Root directories are reserved for project documentation and repository-level folders such as `docs/` and `projects/`, plus operational folders (`engine/`, `templates/`, `scripts/`, `domains/`) where relevant. Finance/accounting is the standalone cross-cutting **finance engine** (resolve its checkout through the engine-routing table) — consult it whenever finance/IFRS/IAS/tax/bookkeeping arises, in addition to the active work.
- Domain packs live under `domains/`. They are not skills by themselves; use them as context sources when a task is domain-specific.

## Skill Authoring and Release Gate

The shared agents, commands, hooks, evidence, and handoff contract is mapped
for SRS work in `docs/control-plane-adoption.md` and governed centrally by
`docs/engine-control-plane.md` in the Chwezi Dev Engine.

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
- Before releasing, also run `python scripts/check_portable_paths.py`, `python scripts/check_cross_engine_refs.py` (add `--dev-engine-root <checkout>` or set `CHWEZI_DEV_ENGINE_ROOT` to resolve category paths; without one that part is `NOT_ASSESSED`), `python scripts/check_standards_currency.py`, `python scripts/validate_source_register.py`, `python scripts/validate_plugin_packages.py` and `python scripts/routing_smoke_test.py --min-rank1 83 --lint-fixtures --min-covered 8`. The October 2026 pass-2 evidence is in `docs/kaizen/2026-10-engine-kaizen-pass-2/`.
- These checks need the pinned packages (`python3 -m pip install -c requirements-ci.txt -e ".[dev,docs]"`). `README.md` ("Which checks need which tool" and "Validation") lists what each one needs and the results measured on 2026-10-31. A check that cannot run on the current host is `NOT_ASSESSED`, never a pass. `scripts/validate_source_register.py` is date-driven and starts failing on 2026-11-30 unless the overdue source records are re-verified.
- Update routing fixtures when a trigger or neighbour boundary changes, and run the anti-slop audit on changed human-facing content before release.
- Anti-AI-slop pre-ship gate: run `09-governance-compliance/28-anti-ai-slop` on every generated SRS/spec/doc/code artefact before delivery (MANDATORY).
- Slop analysis/audit: `09-governance-compliance/29-ai-slop-audit` auto-runs whenever the user asks to analyse, review, evaluate, audit, critique, or de-slop any spec, requirement, document, system, or codebase, or asks "does this look AI-generated?".

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

## Directory Logic & Pathing

- **Skills:** Engineering/methodology skills live in the [Chwezi Dev Engine](https://github.com/peterbamuhigire/chwezi-dev-engine) — the engineering-catalog engine (resolve its local checkout through the engine-routing table; skills under `skills/<category>/<skill-name>/SKILL.md`). Consult its router (`CLAUDE.md`/`AGENTS.md`), then read the matching `SKILL.md` directly. Use these skills for methodology selection, document generation support, and reusable engineering workflows.
- **Finance/Accounting:** Finance/accounting is the standalone cross-cutting [Chwezi Accounting Doctrine](https://github.com/peterbamuhigire/chwezi-accounting-doctrine) engine (resolve its local checkout). Resolve it through the global engine registry and consult it whenever finance, IFRS, IAS, tax, or bookkeeping arises, in addition to the active work.
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

## Compliance Skills (Uganda Domain)

For Uganda-based projects, two compliance outputs are available, both routed to the `dpia-generator` skill, and should be invoked as cross-cutting tasks alongside the main SRS skill flow:

- **`dpia-generator`** (chwezi-dev-engine; the retired `uganda-dppa-compliance` skill is an inactive alias of it) — Generates the DPPA 2019 compliance annex: PII inventory, classification (financial info = special personal data), consent FRs, data subject rights FRs, breach notification procedure (immediate → PDPO), retention/destruction schedule, DPIA trigger assessment, DPO/PDPO registration requirements. Invoke after Skill 05 (Functional Requirements) for any module that collects personal data.
- **`dpia-generator`** — Generates a Regulation 12-compliant DPIA document for any processing operation flagged `[DPIA-REQUIRED]`. Invoke when the DPPA compliance annex raises a DPIA flag.

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

When the kernel reports `[CONTEXT-GAP: <topic>]`, consult `00-meta-initialization/new-project/prompts/context-gap-fillers.md` in the engineering catalog engine (that file lives in the dev engine, not in this repo) before authoring from scratch. It contains an opinionated prompt per topic you can paste into a fresh assistant session.

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

## Human-English editorial standard (2026-08 Kaizen)

Load [`09-governance-compliance/28-anti-ai-slop/references/human-english-and-lexical-precision.md`](09-governance-compliance/28-anti-ai-slop/references/human-english-and-lexical-precision.md) for requirements, UX content, user manuals, FAQs, release notes, runbooks, training, support messages, and other human-facing documentation. Apply it alongside the applicable IEEE/ISO, traceability, accessibility, security, and `28-anti-ai-slop` controls.

Technical prose must remain exact: name actors, states, constraints, terminology, and test oracles. User-facing text must also be calm, respectful, grammatical, and useful in the current state. Never add errors, slang, unexplained humour, or vague adjectives to make text seem human. Record artefact type, reader/task, source traceability, terminology checks, test-oracle review, language/proof status, gaps, reviewer, and date.

The same reference carries the collocation, register, idiom, lexical-precision and calibrated-claim overlay. It strengthens the English layer; it does not override approved product terminology, accessibility rules, requirements traceability, or current Digital Research verification.

