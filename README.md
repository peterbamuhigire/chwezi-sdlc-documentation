# Chwezi SDLC Documentation

Chwezi SDLC Documentation is a library of 160 skills and a Python validation kernel for software-lifecycle documentation. Each skill tells a coding agent how to write one document, from a product requirements document (PRD) to an auditor-ready evidence pack.

The kernel checks a project's documents against phase gates and builds them into a styled `.docx`. The engine is for product owners, business analysts, architects, delivery teams, testers, operators and compliance reviewers on waterfall, Agile or hybrid projects.

Use it when a project needs requirements, design, test, deployment, user or governance documents that trace to one another. It records missing stakeholder decisions as open questions rather than inventing requirements. It supports engineering, legal and compliance work; it replaces none of them.

## At a glance

- **160 skills in nine numbered phases**, from `01-strategic-vision` to `09-governance-compliance` (counted with `find` on 2026-11-10).
- **Eleven domain packs** under `domains/` add sector context: healthcare, finance, government, agriculture, logistics, Uganda and five more.
- **A validation kernel**, `python3 -m engine`, runs deterministic gates for phases 01 to 09 and a hybrid gate.
- **535 tests passed and 5 skipped** under `engine/tests`, with 96.19% coverage against a 90% floor (pytest, re-run 2026-11-05).
- **Routing proxy:** 73 of 73 fixtures rank the expected skill in the top three, and 65 of 73 rank it first (re-run 2026-11-06). The proxy is lexical, not live routing.
- **Latest published score:** 55.68 out of 100 after pass 2 on 2026-10-31. It is a reviewer judgement, not a customer outcome.

## Start here

1. **Clone and install** (Python 3.11 or later, in a virtual environment):

   ```sh
   git clone https://github.com/peterbamuhigire/chwezi-sdlc-documentation
   cd chwezi-sdlc-documentation
   python3 -m pip install -c requirements-ci.txt -e ".[dev,docs]"
   ```

   To load the skills into Claude Code or Codex without the kernel, see [Installation](#installation).
2. **Check the checkout.** `python3 -X utf8 scripts/validate_engine.py` prints `ENGINE CONTRACT: PASS` and exits 0. It needs only Python and Git.
3. **Create and validate a project workspace:**

   ```sh
   python3 -m engine new-project Acme --methodology waterfall --domain healthcare
   python3 -m engine validate projects/Acme
   ```

   A new workspace exits 1 with 22 blocking findings, because the phase 03 to 09 documents do not exist yet. For a passing run, see [Manual route](#manual-route).

**Contents**

- [Capabilities](#capabilities)
- [Find the right skill](#find-the-right-skill)
- [How it works](#how-it-works)
- [What is inside](#what-is-inside)
- [Standards it follows](#standards-it-follows)
- [Requirements](#requirements)
- [Installation](#installation)
- [Project workspaces, gates and document builds](#project-workspaces-gates-and-document-builds)
- [Validation](#validation)
- [Quality and improvement](#quality-and-improvement)
- [What the October 2026 kaizen improved](#what-the-october-2026-kaizen-improved)
- [References](#references)
- [Contributing and licence](#contributing-and-licence)

## Capabilities

The engine holds 160 skills in nine numbered phases, grouped under [What is inside](#what-is-inside). The [skill catalogue](docs/skill-catalogue.md) lists each one. The table under Find the right skill is the capability map: common tasks and the skill that handles each.

### Find the right skill

Describe the task in plain words and the router (`AGENTS.md`) picks the skill. The tasks below paraphrase the routing test fixtures. Each folder sits at the repository root.

| Task | Skill | Folder |
|---|---|---|
| Set product objectives, users, features and success measures | `01-prd-generation` | `01-strategic-vision` |
| Compare costs and benefits and recommend go or no-go | `02-business-case` | `01-strategic-vision` |
| List stakeholders and build the stakeholder register | `01-stakeholder-analysis` | `02-requirements-engineering/fundamentals/before` |
| Turn a vague or contradictory brief into requirements and surface each ambiguity | `04-requirements-analysis` | `02-requirements-engineering/fundamentals/during` |
| Start a Waterfall software requirements specification (SRS) workspace | `01-initialize-srs` | `02-requirements-engineering/waterfall` |
| Turn features into user stories checked against the INVEST criteria | `01-user-story-generation` | `02-requirements-engineering/agile` |
| Link goals, requirements, design, code, tests and evidence | `09-traceability-engineering` | `02-requirements-engineering/fundamentals/after` |
| Draw the system context, components, key decisions and failure boundaries | `01-high-level-design` | `03-design-documentation` |
| Write an OpenAPI contract with authentication, schemas and an error model | `03-api-specification` | `03-design-documentation` |
| Design entities, constraints, indexes and migrations | `04-database-design` | `03-design-documentation` |
| Define test levels, environments, risk coverage and exit criteria | `01-test-strategy` | `05-testing-documentation` |
| Write production deployment steps with verification and rollback | `01-deployment-guide` | `06-deployment-operations` |

- Games have their own skills, for example `19-game-software-requirements-specification` and `15-game-product-and-production-brief`. In the routing proxy, the bare phrase "software requirements specification" still ranks the game skill first, so name the project type.
- Every other skill is in the [skill catalogue](docs/skill-catalogue.md).

## How it works

- **Skills.** Each skill is a `SKILL.md` file with optional `references/`, `templates/` and a `logic.prompt`. Skills follow the `NN-phase/NN-skill/SKILL.md` layout; the repository has no `skills/` directory. `AGENTS.md` is the router, and `CLAUDE.md` is a thin bridge to it.
- **Workspaces.** Each project lives in `projects/<ProjectName>/`, kept out of version control. Phase output folders sit beside `_context/` and `_registry/`.
- **Gates.** `python3 -m engine validate` checks a workspace against the phase gates. Diagrams are typed and checked against the requirement registry.
- **Build.** `scripts/build-doc.sh` renders Mermaid diagrams to captioned figures. Pandoc then stitches the Markdown into a styled `.docx`.
- **Overlays.** Extra skills extend the core to SaaS, AI features and agents, embedded accounting, games, hospitality and retail.

## What is inside

The 160 active skills sit in nine phase folders. Skills are discovered from the filesystem, not from this table.

| Category (folder) | Skills |
|---|---:|
| Strategic vision (`01-strategic-vision`) | 13 |
| Requirements engineering (`02-requirements-engineering`) | 42 |
| Design documentation (`03-design-documentation`) | 18 |
| Development artefacts (`04-development-artifacts`) | 6 |
| Testing documentation (`05-testing-documentation`) | 10 |
| Deployment and operations (`06-deployment-operations`) | 23 |
| Agile artefacts (`07-agile-artifacts`) | 5 |
| End-user documentation (`08-end-user-documentation`) | 9 |
| Governance and compliance (`09-governance-compliance`) | 34 |
| **Total** | **160** |

Requirements engineering nests `agile/`, `fundamentals/`, `hybrid/` and `waterfall/` subfolders. The skeleton in `templates/skill/` is excluded. The full list, with a one-line description of every skill, is in the [skill catalogue](docs/skill-catalogue.md).

What the skills produce, by phase:

- **Phases 01 and 02:** PRDs, business cases, vision statements, business requirements documents (BRDs) and software requirements specifications.
- **Phase 03:** high-level and low-level designs, and API, database, UX and infrastructure specifications.
- **Phases 04 and 05:** technical specifications and coding guidelines; test strategies, plans and reports.
- **Phase 06:** deployment guides, runbooks, monitoring set-ups and service-level objective documents.
- **Phases 07 and 08:** sprint planning and definition-of-done documents; user manuals, installation guides, FAQs and release notes.
- **Phase 09:** traceability matrices, architecture decision records (ADRs), risk registers, sign-off ledgers and auditor-ready evidence packs.

Eleven domain packs under `domains/` supply sector context: agriculture, automotive, education, finance, government, healthcare, hospitality, logistics, productivity, retail and Uganda. Read a pack's `INDEX.md` when a project belongs to that sector.

## Standards it follows

- **Requirements:** ISO/IEC/IEEE 29148:2018, with the superseded IEEE Std 830-1998 layout kept for SRS structure. Quality attributes follow ISO/IEC 25010:2023.
- **Design:** ISO/IEC/IEEE 42010 and IEEE Std 1016-2009.
- **Testing and verification:** ISO/IEC/IEEE 29119-3 and IEEE Std 1012-2016.
- **Lifecycle and user documentation:** ISO/IEC/IEEE 12207:2017 and ISO/IEC/IEEE 26514.
- **Security and AI governance packs:** ISO/IEC 27001:2022, ISO/IEC 42001, the NIST AI RMF, SOC 2, the HIPAA Security Rule, the EU AI Act and GDPR.
- **Interfaces:** OpenAPI 3.1 and RFC 9457 problem details. User interfaces are checked against WCAG 2.2.

Some gate clause labels still cite superseded editions (see [Quality and improvement](#quality-and-improvement)). The full list is under [Standards and official sources](#standards-and-official-sources).

## Requirements

- Git, and Python 3.11 or later for the validation kernel (`pyproject.toml`). The kernel was last run on Python 3.14.8.
- The pinned Python packages, installed in a virtual environment: `python3 -m pip install -c requirements-ci.txt -e ".[dev,docs]"`. They are `click`, `ruamel.yaml`, `mistune`, `jsonschema`, `pytest`, `pytest-cov` and `python-docx`, at the versions in `requirements-ci.txt`.
- `pyyaml` (`import yaml`), which `requirements-ci.txt` does not list. `scripts/validate_decision_frontier.py` and `tests/agent-integration/test_srs_agent_contract.py` import it, so install it before running them.
- Node.js 18 or later for the scripted installers (`install.sh`, `install.ps1`) and for the hook and Plan Canvas tests.
- For `.docx` builds: Pandoc, and the `docs` extra for the temporary Word style template. A checked-in or ignored `templates/reference.docx` is optional.
- For Mermaid figures: a local Chrome or Edge for the pinned renderer. Run `npm ci` in `scripts/diagram-render` with `PUPPETEER_SKIP_DOWNLOAD=1`, and point `PUPPETEER_EXECUTABLE_PATH` at the browser.

### Which checks need which tool

| Needs | Commands |
|---|---|
| Python 3 and Git only (no third-party package) | `scripts/validate_engine.py`, `scripts/validate_plugin_packages.py`, `scripts/check_portable_paths.py`, `scripts/check_cross_engine_refs.py`, `scripts/check_standards_currency.py` |
| Python 3 and Git only (continued) | `scripts/validate_source_register.py`, `scripts/validate_sdd_phase_boundaries.py`, `scripts/validate_requirements_decision.py`, `scripts/source_ingestion_guardrail.py` |
| The pinned packages | `scripts/validate_skill_engine.py` and `scripts/routing_smoke_test.py` (both exit 2 with an install message when `ruamel.yaml` is missing) |
| The pinned packages (continued) | Every `python3 -m engine` command (`ModuleNotFoundError` when `ruamel.yaml` is missing) and `python3 -m pytest` |
| The pinned packages (continued) | `scripts/validate_traceability_evidence.py` (`jsonschema`) and `scripts/validate_source_reconciliation.py` |
| Node.js 18 or later | `install.sh`, `node hooks/test-destructive-bash-gate.js`, `node hooks/test-plugin-hook-config.js` and the Plan Canvas tests |
| Pandoc | `scripts/build-doc.sh` (exits 1 with "Pandoc is required" when it is missing) and the `.docx` tests, which pytest skips without it |
| Node.js, `npm ci` in `scripts/diagram-render` and a local Chrome or Edge | Mermaid figure rendering inside `scripts/build-doc.sh` |
| PowerShell | `install.ps1`, `scripts/setup-srs-project.ps1` and the `export-docs.ps1` that `new-project` writes into each workspace. No registered check needs it |
| LibreOffice or a container | Nothing in this repository requires either |

## Installation

The GitHub repository is `chwezi-sdlc-documentation`. A checkout made before the rename may still sit in a folder named `srs-skills`. The scripted installer names the installed copy after the checkout folder, so clone into `chwezi-sdlc-documentation`.

### Claude Code plugin

The repository ships a marketplace manifest (`.claude-plugin/marketplace.json`, marketplace `chwezi-sdlc-documentation`, plugin `sdlc-documentation`):

```text
/plugin marketplace add https://github.com/peterbamuhigire/chwezi-sdlc-documentation
/plugin install sdlc-documentation@chwezi-sdlc-documentation
```

### Codex

Codex reads `AGENTS.md` as the router. From a trusted checkout, add the repository marketplace:

```sh
codex plugin marketplace add .
```

The catalogue is `.agents/plugins/marketplace.json`. It points to this checkout and reuses the Claude-compatible skill manifest.

- **Check the package.** `python3 -X utf8 scripts/validate_plugin_packages.py` checks the catalogue, the manifest-to-skill parity and the package-oriented file count. It also reports the full checkout count, and it fails if either count is above the OpenAI ZIP submission ceiling of 5,000 entries.
- **No archive.** The check builds and submits no archive. Public submission and acceptance are separate steps.
- **Skill-list budget.** When the installed skills exceed its default context budget, Codex may shorten descriptions or omit skill paths from the initial list. The optional `skills.max_context_tokens=10000` setting raises that budget. It does not load every full skill body.
- **Verify a local runtime.** Capture only a sanitised summary of `codex debug prompt-input`, then run `python3 scripts/check_codex_discovery_summary.py --expected-paths 159 <summary.json>` against it. Do not commit the raw prompt-input dump, because it can contain internal instructions.
- **Summary format.** A JSON object with `manifest_paths`, `runtime_paths`, `missing` (an empty list), `network` set to `none`, `model_calls` set to `0` and a `method` string that contains "offline". The check exits 1 otherwise.
- **Last result.** The offline Codex 0.165.0 check on 2026-10-29 produced all 159 paths with a 10,000-token budget and 108 by default. These are path-discovery counts, not evidence of correct skill selection or task quality ([record](docs/kaizen/2026-10-engine-kaizen/04-validation-record.md)).
- **Model policy (Codex only).** Run `python3 <engine-root>/.codex/ensure_model_policy.py --runtime codex --check`, and run `--apply` only when the check reports drift. It exits 1 with `DRIFT: Codex config.toml is missing` when no Codex configuration exists. Claude skips this step.

### Scripted install

The installers delegate to `scripts/install-engine.js`. User scope (`~/.claude`) is the default. `--scope project` installs into `.claude` under the current directory, and `--dry-run` prints the plan without writing anything.

The scripts are tracked without the executable bit, so run them through `bash`: `./install.sh` fails with `Permission denied` on Linux. The installer also takes `uninstall`, `list-installed` and `doctor` (`node scripts/install-engine.js <command>`).

```sh
bash install.sh --scope project --dry-run   # macOS, Linux or Git Bash; drop --dry-run to install
.\install.ps1 --scope project               # Windows PowerShell
```

### Manual route

Clone the repository and read `CLAUDE.md`, which is a thin bridge to `AGENTS.md`. Then open the `SKILL.md` for the phase and task in hand. To check the environment, run the kernel's doctor command:

```sh
python3 -m engine doctor
```

What the commands print on a clean checkout:

- `doctor` exits 1. It reports `[FAIL] Skills submodule` because it looks for a `skills/` directory in the current folder. That check applies to a project repository that vendors this engine as `skills/` (see [`SETUP_GUIDE.md`](SETUP_GUIDE.md)), not to the engine checkout.
- `doctor` also reports `[FAIL] Pandoc available` when Pandoc is not on `PATH`.
- `validate` on a new workspace exits 1. A new `healthcare` workspace and a new `uganda-public-sector` workspace each return 22 blocking findings, because the phase 03 to 09 documents do not exist yet. Exit 0 needs the full document set.
- To see a passing run, use the seeded demo: `python3 scripts/seed_demo_project.py`, then `python3 -m engine validate projects/_demo-hybrid-regulated` (exit 0).
- When `pip install -e` has not been run, put the checkout first on the import path with `PYTHONPATH=.`. Otherwise a non-editable copy of `engine` elsewhere in the environment would be the one that runs.

[`SETUP_GUIDE.md`](SETUP_GUIDE.md) covers provisioning a separate project repository.

### Companion engines

Companion engines are resolved through the engine-routing table of the active runner, never through a fixed path.

- Engineering skills: `chwezi-dev-engine` (earlier local folder `skills-web-dev`).
- Design and typography: `chwezi-design-engine` (`design-system-skills`).
- Research and currentness: `digital-research-skills` (`chwezi-research-engine`).
- Finance: `chwezi-accounting-doctrine`.

To let `scripts/check_cross_engine_refs.py` resolve category paths, pass `--dev-engine-root <checkout>` or set `CHWEZI_DEV_ENGINE_ROOT`.

## Project workspaces, gates and document builds

Each project lives in its own workspace at `projects/<ProjectName>/`. Canonical inputs go in `_context/`. Identifiers, baselines, waivers and sign-offs go in `_registry/`. Each phase has its own output folder.

- **Create.** `--methodology` accepts `waterfall`, `agile` or `hybrid`. `--example uganda-public-sector` copies the shipped example from `templates/project-examples/`. That example supplies only context and registries, not phase documents.
- **Validate.** `python3 -m engine validate projects/<ProjectName>` runs the phase gates for phases 01 to 09 and the hybrid gate. Every check ID maps to a standard and clause in [`docs/standards-clause-registry.md`](docs/standards-clause-registry.md).
- **Reconcile sources.** Before Phase 02, copy `02-requirements-engineering/fundamentals/during/04-requirements-analysis/references/source-reconciliation-template.yaml` to `projects/<ProjectName>/_registry/source-reconciliation.yaml`.
- **Check the register.** Map each material source statement to a requirement or an explicit ambiguity, then run `python3 scripts/validate_source_reconciliation.py projects/<ProjectName>`. The script exits 1 when the register is missing or lists no source statement.
- **Register caveat.** The Phase 02 gate in `engine validate` reports unresolved ambiguities as blockers, but a project with no register passes that check. Whether to require the register is an open owner decision. The check validates links and decisions, not the completeness of the source review.
- **Trace evidence.** Use `references/traceability-evidence.schema.json` and run `python3 scripts/validate_traceability_evidence.py <report.json>`. Goal and design links, test links, oracle readiness, owner decisions and executed results are reported separately.
- **Registries and packs.** `python3 -m engine sync`, `baseline snapshot|diff`, `waive`, `signoff` and `pack` maintain the identifier registry, baselines, time-bound waivers and the sign-off ledger, and assemble an evidence-pack ZIP.
- **Diagrams.** `python3 -m engine diagrams validate|generate|manifest|verify-manifest` checks typed diagram IR (`engine/registry/schemas/diagram-ir.schema.json`) against the requirement registry. It then generates Mermaid from the IR and records figure hashes.
- **Build.** `bash scripts/build-doc.sh <doc-dir> <output-name>` renders every Mermaid block to a captioned PNG or SVG figure with alt text and a render manifest. It then builds the `.docx` with Pandoc.
- **Build guards.** The script generates a temporary reference template when `templates/reference.docx` is absent. It refuses a document that still contains raw Mermaid.
- **Hybrid projects.** [`docs/hybrid-operating-model.md`](docs/hybrid-operating-model.md) defines the Water-Scrum-Fall contract for projects that baseline requirements formally and deliver in increments.
- **Regulated projects.** [`docs/regulated-evidence-model.md`](docs/regulated-evidence-model.md) defines the minimum evidence chain, from regulation to audit record, for regulated delivery.

## Validation

Run these from the repository root. The results were measured on 31 October 2026 on Python 3.14.8 and Node.js 22. The packages were at the versions in `requirements-ci.txt`, except `python-docx`, which was absent. Pandoc, the Mermaid renderer, a browser and PowerShell were also absent.

`.github/workflows/engine.yml` runs most of the same commands on Python 3.11. It does not run the Node.js tests. Inside an activated virtual environment, `python` and `python3` are the same interpreter.

On 2026-11-05 the first eleven commands in this table were re-run (Python 3.14.10, pytest 9.2.0, a fresh virtual environment with `PYTHONPATH=.`). They gave the results below, with `validate_plugin_packages.py` reporting 2,196 checkout entries and 1,290 package entries against the 5,000 limit and `validate_source_register.py` reporting 18 effective records as of that date. The six commands after them were not re-run and keep their 2026-10-31 results. Without `PYTHONPATH=.`, `engine/tests/test_agent_brief.py::test_script_writes_beside_the_handoff` fails with `ModuleNotFoundError: No module named 'engine'`.

| Command | Result on 2026-10-31, same on 2026-11-05 where re-run |
|---|---|
| `python3 -m pytest` | Runs `engine/tests`: 535 passed, 5 skipped, coverage 96.19% against a 90% floor. |
| `python3 -m pytest tests -o addopts=` | 33 passed. Continuous integration (CI) runs 19 of them (the routing and Tier-1 lint tests). |
| `python3 -X utf8 scripts/validate_engine.py` | `ENGINE CONTRACT: PASS`. |
| `python3 -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | 160 active skills, 1 template, no failures; 5 report-only size warnings. |
| `python3 -X utf8 scripts/routing_smoke_test.py --min-rank1 83 --lint-fixtures --min-covered 8` | 73 of 73 fixtures in the top three; precision@1 65 of 73 (89.0%); fixture lint 0 findings over 99 prompts. Re-run on 2026-11-06 after two fixtures were added; on 2026-10-31 it was 72 of 72 and 64 of 72 (88.9%). |
| `python3 -m engine validate-skills` | `SKILLS OK`. |
| `python3 -X utf8 scripts/validate_plugin_packages.py` | 160 active skill paths, `errors: 0`, both file counts under the 5,000 limit. |
| `python3 scripts/check_portable_paths.py` | PASS, 0 findings. |
| `python3 scripts/check_cross_engine_refs.py` | PASS. Category and URL paths are `NOT_ASSESSED` without a dev-engine checkout. With `--dev-engine-root <checkout>` they resolve and the check passes. |
| `python3 scripts/check_standards_currency.py` | PASS: no stale-citation count above its ceiling. |
| `python3 scripts/validate_source_register.py` | PASS: 18 effective records from 2 registers. Date-driven; see [Date-triggered gates](#date-triggered-gates). |
| `python3 scripts/validate_traceability_evidence.py engine/tests/fixtures/traceability-evidence.json` | Prints the evidence counts and exits 0. |
| `python3 scripts/validate_sdd_phase_boundaries.py --feature-dir engine/tests/fixtures/sdd_feature` | PASS, no boundary findings. |
| `python3 scripts/validate_requirements_decision.py engine/tests/fixtures/requirements_decision/reuse.json` | `"status": "PASS"`. |
| `python3 -X utf8 scripts/source_ingestion_guardrail.py` | `findings: 0`. |
| `python3 scripts/seed_demo_project.py`, then `python3 -m engine validate projects/_demo-hybrid-regulated` | Exit 0. The hidden flag `--break-something` makes the same command exit 1, which CI uses to show the gate can fail. |
| `node hooks/test-destructive-bash-gate.js`, `node hooks/test-plugin-hook-config.js` | 61 of 61 and 7 of 7 passed. |
| `node tests/plan-canvas/markdown.test.js` and the five other files under `tests/plan-canvas`, `tests/hooks` and `tests/scripts` | Plain Node.js scripts: run each with `node <file>`, not `node --test`. 64, 16, 28, 9, 7 and 4 checks pass. |

Notes on the table:

- **Pytest skips.** Four of the five skips need Pandoc, a renderer or a browser. The fifth, in `engine/tests/test_examples_validate.py`, collects no example because it looks in a folder this repository does not contain.
- **Routing.** The routing result is a lexical proxy, not live routing. The same run reports 26 owned negatives: 23 pass and 3 are `NOT_ASSESSED` because their owners are in other engines (25 and 22 on 2026-10-31). 8 of 159 skills meet the route-coverage target.

Not run on that host, so `NOT_ASSESSED`:

- `bash scripts/build-doc.sh`: Pandoc was absent, so it exits 1 with `ERROR: Pandoc is required`.
- Mermaid figure rendering and the four Pandoc, renderer and browser pytest skips.
- `install.ps1` and `scripts/setup-srs-project.ps1`: no PowerShell.
- `pip install -e` itself: the environment already held the packages.

## Quality and improvement

The evidence for the October 2026 kaizen cycles is in the repository.

- [`docs/kaizen/2026-10-engine-kaizen/`](docs/kaizen/2026-10-engine-kaizen/) holds the 29 October cycle.
- [`docs/kaizen/2026-10-engine-kaizen-pass-2/`](docs/kaizen/2026-10-engine-kaizen-pass-2/) holds the 31 October cycle (pass 2).
- Each folder has a scope record, baseline scorecard, backlog, experiment log, validation record, final report, next-cycle notes and a dated source register. Start with `05-final-report.md` and `06-next-cycle.md`.
- The kept changes, with commits and before-and-after figures, are under [What the October 2026 kaizen improved](#what-the-october-2026-kaizen-improved).
- [`docs/README.md`](docs/README.md) indexes the older audits. The README restructuring of 31 October is recorded in [`docs/kaizen/2026-10-readme-kaizen/readme-kaizen-record.md`](docs/kaizen/2026-10-readme-kaizen/readme-kaizen-record.md).

### Latest published score

The pass 2 final report (31 October 2026) gives 55.68 out of 100 raw and 55.68 out of 100 after the portfolio cap of 65. The 29 October cycle ended at 53.98. The pass 2 report also states a stricter initial cap of 45, under which the reported value is 45.

The score is an unweighted mean of ten reviewer-judged dimensions. It is not a customer outcome and has had no independent acceptance review. The 95 target is not reached.

### Open findings

These findings matter when you use the engine.

- A project with no `_registry/source-reconciliation.yaml` still passes the Phase 02 source check. Source-conflict blocking applies only to projects that keep the register.
- Gate clause labels still cite IEEE Std 830-1998 (163 live lines), the 2011 edition of ISO/IEC/IEEE 42010 (13 lines) and the 2013 edition of ISO/IEC/IEEE 29119-3 (11 lines). Their issuers list these as superseded or withdrawn.
- The router keeps the 1998 standard only as an SRS layout reference. `scripts/check_standards_currency.py` stops these counts rising, but it does not remap clauses.
- Phase 09 does not trace requirement identifiers with the prefixes `NFR`, `IR`, `DR` and `CON`. It also does not block two definitions of the same identifier.
- Applied proof is thin. 4 of 159 skills have an `examples/` folder, and 44 of the 81 skills with a worked-example section share one of 12 identical paragraphs.
- Routing evidence is lexical. The phrase "software requirements specification" still ranks the game SRS skill first in the proxy. Pass 2 recorded a second near miss for a school-fees prompt. No live-model routing run has been made.
- The education pack is a United States baseline with no school-fees module. 16 domain-pack lines still target the 2.1 level of the accessibility guidelines, not 2.2, pending a jurisdiction decision.
- The `.docx` build and Mermaid rendering were not assessed on the Linux workstation.
- The per-user settings file `.claude/settings.local.json` is untracked and ignored, but earlier commits on the public history still contain it. Removing it needs a history rewrite, which is a decision for the maintainer.

### Date-triggered gates

`scripts/validate_source_register.py` fails when a source record has no review date or its review date has passed. Run with `--today YYYY-MM-DD`, it exits as follows:

| Run date | Exit | Findings and the review dates behind them |
|---|---:|---|
| Up to 2026-11-29 | 0 | None. Due-soon notes, which do not fail, start 14 days before a review date, so from 2026-11-15. |
| 2026-11-30 | 1 | 3: OpenAI plugin schema, OpenAI archive limit and Claude marketplace (review 2026-11-29). |
| 2026-12-01 | 1 | 4: adds the Codex skill-list budget (review 2026-11-30). |
| 2027-01-30 | 1 | 8: adds ISO/IEC 25010, Uganda regulations, model catalogue and dev-engine references (review 2027-01-29). |
| 2027-02-01 | 1 | 14: adds ISO/IEC/IEEE 29148, Uganda DPPA, WCAG, Pandoc, Mermaid CLI and dev-engine aliases (review 2027-01-31). |
| 2027-10-30 | 1 | 17: adds ISO/IEC/IEEE 42010, ISO/IEC/IEEE 29119-3 and ISO/IEC/IEEE 26514 (review 2027-10-29). |

To clear a finding, re-verify the claim against its primary source. Record it in a newer `docs/kaizen/<cycle>/standards-source-register.md`; a newer record supersedes an older one for the same claim identifier. The pass 2 notes propose the next re-audit for 2026-11-30.

### Changes after the October kaizen (1 to 7 November 2026)

- **Signup human-validation requirements (1 November, `c8cf4f6`).** The technical-specification skill gained the reference [`signup-human-validation.md`](04-development-artifacts/01-technical-specification/references/signup-human-validation.md).
  - Web signup: Turnstile with mandatory backend verification.
  - Android signup on Google Play: Firebase App Check with Play Integrity, with a Turnstile WebView fallback.
  - Acceptance evidence covers failure and abuse cases such as invalid, expired, replayed and wrong-host tokens, outages and emulators.
  - Provider claims were checked on 1 November 2026. Review them by 1 February 2027. Record: [`docs/updates/2026-11-01-signup-human-validation-standard.md`](docs/updates/2026-11-01-signup-human-validation-standard.md).
- **Document numbering requirements (5 November, `904d9da`).** A new reusable block, [`document-numbering-requirements.md`](02-requirements-engineering/references/document-numbering-requirements.md), states the rule that every user-facing document number in a multi-tenant SaaS system is contiguous per tenant and document type.
  - It holds 28 functional requirements, 7 non-functional requirements, 9 transition requirements, 5 design constraints and 4 controls, each with an ID, a rationale and a verification method. It also holds 20 test cases and a document type register.
  - A multi-tenant SRS now gets a "Document Numbering" feature by default. Leaving it out needs a recorded waiver.
  - It is wired into feature decomposition, attribute mapping, SRS initialisation, the SaaS NFR catalogue, the multi-tenancy architecture spec (new section 10 and a halt rule), database design, API specification, low-level design, the accounting SRS and design, the billing spec, business rules, acceptance criteria, the test plan, the retail and hospitality SRS skills and the finance domain gate.
  - No skill was added, so the count stays 159 skills and 1 template. A step-numbering defect in `05-feature-decomposition` (steps 1 to 6, then 5) was fixed on the way. Record: [`docs/continuous-improvement/document-numbering-kaizen-2026-11-05.md`](docs/continuous-improvement/document-numbering-kaizen-2026-11-05.md).
- **AI assistant use section (6 November, `6d4d158`, `b8febfd`).** The coding-guidelines skill gained an optional section 9 for teams that use AI coding assistants. It follows a 2026 reading of CODE Magazine articles, compared with the engine's own text before any change.
  - The new reference [`ai-assistant-use-section.md`](04-development-artifacts/02-coding-guidelines/references/ai-assistant-use-section.md) sets eight required elements, AU-1 to AU-8: encouraged uses and ownership, uses that need extra review, output that needs human approval, architecture rules the assistant cannot know, testing expectations, security and data rules, disclosure and review of assisted work, and instruction files with an owner and precedence.
  - It has a checklist applied by hand, one worked example that passes and one that fails. No automated document-conformance check exists for coding guidelines.
  - It points to the community development engine for the how and keeps the AI-agent addendum for AI-agent products. Two routing fixtures cover the boundary. No skill was added (159 skills and 1 template). Record: [`docs/continuous-improvement/assistant-use-section-kaizen-2026-11-06.md`](docs/continuous-improvement/assistant-use-section-kaizen-2026-11-06.md).
- **House-style declaration (7 November, SD-KZ-06).** The UX specification skill gained the reference [`house-style-declaration.md`](03-design-documentation/05-ux-specification/references/house-style-declaration.md). A product that follows the Chwezi business-app house style declares it as twelve verifiable requirements (HS-01 to HS-12) with evidence; presentation values stay in the design engine. No skill was added (159 skills and 1 template). Record: [`docs/continuous-improvement/house-style-declaration-kaizen-2026-11-07.md`](docs/continuous-improvement/house-style-declaration-kaizen-2026-11-07.md).
- **Validation re-run (5 November).** The first eleven commands in [Validation](#validation) were re-run on 2026-11-05 and gave the figures already shown. Details are under that table. The routing row was re-run again on 2026-11-06 after the fixtures above.

## What the October 2026 kaizen improved

Two kaizen cycles ran on this repository: 29 October 2026 and 31 October 2026 (pass 2). This section lists only changes that were kept, and every commit named is on `main`. Neither cycle reverted a change (see the final reports linked under Scores).

One test assertion was relaxed on 29 October. A check that required the routing-fixture count to equal the frozen baseline became a lower bound (`4709e28`). The baseline file was not changed.

"Re-measured" means the figure was taken again on 2026-10-31 on a Fedora host, from `main` or from the named commit. Every other figure is copied from the evidence file named beside it. Ratings are reviewer judgements, not customer outcomes.

### Scores

The portfolio cap of 65 does not bind at any point, so each raw value equals its capped value. The stricter initial cap of 45 would report 45 at every point. [Latest published score](#latest-published-score) explains how the raw score is built.

| Point | Raw | `min(raw, 65)` | Evidence |
|---|---:|---:|---|
| 29 October baseline | 50.28 | 50.28 | [`01-baseline-scorecard.md`](docs/kaizen/2026-10-engine-kaizen/01-baseline-scorecard.md) |
| 29 October final | 53.98 | 53.98 | [`05-final-report.md`](docs/kaizen/2026-10-engine-kaizen/05-final-report.md) |
| Pass 2 fresh baseline | 52.18 | 52.18 | [`01-baseline-scorecard.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/01-baseline-scorecard.md) |
| Pass 2 final | 55.68 | 55.68 | [`05-final-report.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/05-final-report.md) |

The pass 2 baseline is a fresh judgement that looked at surfaces the earlier cycle had not inspected: a tracked local settings file, gate false negatives and template currency. That is why it sits below the 29 October final.

### Measures

The three value columns are the tree before the 29 October cycle (`b3b08b5`), the tree after it (`91b987d`) and `main` after pass 2.

| Measure | Before 29 Oct | After 29 Oct | After pass 2 | Basis |
|---|---|---|---|---|
| Active skills | 159 | 159 | 159 | Re-measured: `SKILL.md` files outside `templates/` at each commit. Unchanged. |
| Routing precision@1 (lexical proxy) | 47 of 55 (85.5%) | 57 of 65 (87.7%) | 64 of 72 (88.9%) | Re-measured with the stand-in described below. |
| Skills with three positive and two owned-negative fixtures | 0 of 159 | 4 | 8 | Re-measured with the `--coverage` option of `main` applied to each commit's fixtures. |
| Routing fixture prompts | 71 | 89 | 97 | Re-measured from `tests/routing-fixtures.json`. |
| Files named `check_*.py` or `validate_*.py` in `scripts/` | 6 | 10 | 14 | Re-measured with `git ls-tree`. |
| Python test functions under `engine/tests` and `tests` | 413 | 438 | 493 | Re-measured with `git grep "def test_"`. A static count, not a pass count. |
| Pytest result | 430 passed, 4 skipped, 96.29% coverage | 453 passed, 4 skipped, 96.47% | 535 passed, 5 skipped, 96.19% | Copied from the scorecards and validation records. `pytest` is absent on this host, so none was re-run. The last run had no Pandoc. The floor is 90%. |
| Run steps in `.github/workflows/engine.yml` | 12 | 12 | 18 | Re-measured. The workflow itself was never run locally. |
| Live lines naming a machine-specific path | 44 | 44 | 0 | Re-measured with `git grep` and the pattern in `scripts/check_portable_paths.py`, outside `docs/`. See the notes below. |
| Tracked per-user settings files | 1 | 1 | 0 | Re-measured with `git ls-tree`. |
| Engine-level lines that prescribe the 2.1 accessibility level | 6 | 6 | 0 | Re-measured with `git grep`, outside `docs/` and `domains/`. |
| Source records whose review date is checked | no register | 17 records, not checked | 18 records, checked | Copied from the scorecards and the pass 2 final report. 18 effective records from 2 registers is the current output of `scripts/validate_source_register.py`. |

Notes on the measures:

- The frozen pass 2 baseline recorded 43 machine-specific path lines in 18 files. The difference is one line in `.gitignore` that its script did not count.
- The catalogue and routing scripts need `ruamel.yaml`, which this host lacks, so they exit 2 here.
- The re-measured skill counts and routing figures come from the same scripts run against each commit's tree. They used a throw-away PyYAML stand-in for `ruamel.yaml`, kept outside the repository. The stand-in reproduces the registered results in [Validation](#validation) (64 of 72, 8 of 159).
- Two measures did not move. 4 of 159 skills have an `examples/` folder (re-measured). The live clause-label counts in the open findings (163, 13 and 11 lines) are unchanged, held by a ceiling.

### Kept changes

Each entry ends with its commits. [`docs/kaizen/2026-10-readme-kaizen/kept-changes-detail.md`](docs/kaizen/2026-10-readme-kaizen/kept-changes-detail.md) holds the full text and every re-run result.

**Safety and integrity**

- **Tracked settings file** (K2-01, critical). A per-user permission file, `.claude/settings.local.json`, was tracked in this public repository. It is now untracked and ignored, and `check_portable_paths.py` fails on any tracked `*.local.json`. Earlier commits still hold the file; removing it needs a history rewrite, the maintainer's decision. `de1efdf`
- **Package gate integrity.** The plugin gate accepted mismatched manifests and a `SKILL.md` symlinked outside the tree, and its entry counter skipped unreadable subtrees without an error. Each now fails, with three regression tests. `91b987d`, `8cb2178`

**Correctness fixes**

- **NFR and trace checks** (K2-04). The Phase 02 check for non-functional requirements (NFRs) passed "quickly" with no threshold, and the Phase 05 check rejected the prefixes `NFR`, `IR`, `DR` and `CON`. Of 30 new tests, 21 failed before the change. A client NFR with a bare qualifier can now fail. `08dae96`
- **Clean-checkout `.docx` build** (SDLC-01). A clean checkout could not build a `.docx`, and the contents list was blank. The builder now makes a temporary Word template and a linked contents list. Checked on 29 October with Pandoc 3.13; `NOT_ASSESSED` on this host. `4e5ec34`

**Portability and hygiene**

- **Dev-engine references** (SDLC-06, K2-02). Skill text named dev-engine skills at paths that do not exist. Eleven names were repaired over the two cycles. `check_cross_engine_refs.py` found 8 findings on the old tree and exits 0 now. `e5698d1`, `2e5149d`, `2a02924`, `2ccbf36`
- **Machine-specific paths** (K2-03). Eighteen live files named a Windows web-server path or a home path and were reworded. `check_portable_paths.py` fails on new ones. Re-measured: 44 live lines before, 0 on `main`. `b8f17be`
- **First-run message and CI** (K2-08). A missing package gave a traceback. Two scripts now name the package and exit 2, and CI gained six run steps. The kernel CLI and two other scripts still print a traceback ([`07-docs-followups.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/07-docs-followups.md), item 6). `e2e80e1`

**New checks and tests**

- **Source ambiguity gate** (SDLC-04). A register, a validator and a Phase 02 check now block on each unresolved source ambiguity (6 findings on the six-ambiguity exercise). Making the register mandatory is an owner decision. `42098e6`, `30aa407`, `293aa0a`
- **Trace evidence states** (SDLC-05). `validate_traceability_evidence.py` reports goal, design and test links, executable oracles, open decisions and executed tests separately. The synthetic ten-requirement fixture shows 3 oracles, 7 open decisions and 0 executed. `6105f73`
- **Package and discovery checks** (SDLC-02, SDLC-03). A Codex marketplace now sits beside the Claude one. `validate_plugin_packages.py` checks manifest parity and the 5,000-entry ceiling. The offline Codex check found 159 paths against 108 by default. `a596222`, `1ff245c`, `a51f164`
- **Edition drift** (K2-06). Six templates prescribed the 2.1 accessibility level against the engine's WCAG 2.2 doctrine; they now say WCAG 2.2 AA. `check_standards_currency.py` fails when any of eight counts rises above its ceiling. Re-measured: 6 lines before, 0 now. `87fa205`
- **Source review dates** (K2-07). Review dates were prose, so an expired record raised nothing. `validate_source_register.py` now fails on a missing or passed date. Pass 2 re-verified or added seven claims; where an issuer page returned HTTP 403, the record says it rests on a secondary check. `4a48a5c`

**Routing and discoverability**

- **Contradictory-brief routing** (K2-05). The task ranked its owning skill tenth. The description of `04-requirements-analysis` now names contradictory and ambiguous briefs, and the proxy rank went from 10 to 1 (19.0 against 9.0). Eight fixtures were added. The school-fees prompt still ties with the multi-tenancy skill (9.01 against 9.00). `17c2179`, `2e57bc0`, `2a02924`

**Documentation**

- **Root documents** (documentation wave, 31 October). The root documents described a repository that had changed, and the wave corrected them. `ce95e9c`, `8cf62b2`, `676dd48`, `f1c17d6`, `908c6c3`, `4946c88`, `44a3eb3`, `29591d9`, `21a2382`, `41615b2`
- **Documentation findings.** The wave ran every documented command once on the Fedora host and recorded 13 findings for owners in [`07-docs-followups.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/07-docs-followups.md).
- **Router release gate** (pass 2). The release-gate list in `AGENTS.md` now names the portability, reference, standards, source-register, routing and packaging checks, and the rule that a check which cannot run is `NOT_ASSESSED`. `f15543f`, `8cf62b2`

Evidence:

- [29 October experiment log](docs/kaizen/2026-10-engine-kaizen/03-experiment-log.md) and [pass 2 backlog](docs/kaizen/2026-10-engine-kaizen-pass-2/02-improvement-backlog.md).
- [Pass 2 experiment log](docs/kaizen/2026-10-engine-kaizen-pass-2/03-experiment-log.md) and [pass 2 validation record](docs/kaizen/2026-10-engine-kaizen-pass-2/04-validation-record.md).

## References

Citations only. The engine keeps no book extractions ([retirement record](docs/continuous-improvement/book-extraction-retirement-2026-09-24.md)). Each entry is cited somewhere in this repository, and the detail given is the detail the repository records.

Books, repositories, websites and articles are in [`docs/references.md`](docs/references.md). Two dated reading lists ([2026-04-12](docs/evaluation/2026-04-12/suggested-reading.md), [July 2026](docs/engine-upgrade-july-2026/05-reading-list.md)) name further recommended books. No skill cites them.

### Standards and official sources

- Requirements: ISO/IEC/IEEE 29148:2018; IEEE Std 830-1998 (superseded, kept for SRS layout); IEEE Std 1233-1998; ISO/IEC/IEEE 24765 and IEEE Std 610.12-1990 (vocabulary).
- Quality: ISO/IEC 25010:2023, ISO/IEC 25019:2023, ISO/IEC 25023, ISO/IEC 25012:2008, ISO/IEC 25051, ISO/IEC 25062; IEEE Std 982.1-2005.
- Architecture and lifecycle: ISO/IEC/IEEE 42010:2011; IEEE Std 1016-2009; ISO/IEC/IEEE 12207:2017; ISO/IEC/IEEE 15288; IEEE Std 828-2012; IEEE Std 1062-2015; ISO/IEC 14764:2006; ISO/IEC 15504.
- Testing, verification and reviews: ISO/IEC/IEEE 29119-3:2013 and 29119-4; IEEE Std 1012-2016; IEEE Std 1028-2008; IEEE 829.
- User documentation and usability: IEEE Std 26514-2022 (ISO/IEC/IEEE 26514); ISO 9241; WCAG 2.2 (https://www.w3.org/TR/WCAG22/).
- Security and privacy management (ISO/IEC): ISO/IEC 27001:2022, ISO/IEC 27002:2022, ISO/IEC 27017, ISO/IEC 27018, ISO/IEC 27035, ISO/IEC 27007, ISO/IEC 17021-1.
- AI governance and risk: ISO/IEC 42001:2023; ISO/IEC 23894; ISO 31000:2018; NIST AI RMF (NIST AI 100-1).
- Security guidance (NIST and OWASP): NIST SP 800-53, 800-61, 800-63 (A and B), 800-57, 800-66, 800-137, 800-161, 800-175B and 800-207; OWASP Top 10, OWASP API Security Top 10, OWASP Top 10 for LLM Applications and the OWASP GenAI Security Project.
- Regulation and assurance: GDPR; EU AI Act; HIPAA Security Rule; SOC 2; PCI DSS; IFRS 15; Uganda Data Protection and Privacy Act, 2019; Nigeria NDPC AI advisory (2024).
- Interfaces and formats: OpenAPI 3.1; RFC 9110, RFC 9457 (formerly RFC 7807), RFC 4918, RFC 7519, RFC 5322, RFC 8594 and RFC 9745; JSON Schema draft 2020-12; SARIF 2.1.0; ISO 8601; ISO 4217; Semantic Versioning 2.0.0 (https://semver.org/spec/v2.0.0.html); Bitol Open Data Contract Standard v3.2.0.
- Domain packs: HL7 FHIR R4 (https://hl7.org/fhir/R4/); GLOBALG.A.P. (https://www.globalgap.org/); Rainforest Alliance (https://www.rainforest-alliance.org/); ISO 22000:2018; ISO 28000; ISO 3779, ISO 3780 and ISO 15031.
- Delivery: DORA and SLSA primary documentation; Google Site Reliability Engineering practice; Pandoc manual (https://pandoc.org/MANUAL.html#option--reference-doc).

## Contributing and licence

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before changing a skill. It sets out the authoring steps and the required checks. New skills start from `templates/skill/SKILL.md` and follow [`docs/skill-authoring-standard.md`](docs/skill-authoring-standard.md).

Peter Bamuhigire wrote and maintains the engine for Chwezi. It is released under the MIT licence ([`LICENSE`](LICENSE)). Third-party sources adapted into the skills are listed, with licence and commit where the repository records them, under [Repositories](docs/references.md#repositories).
