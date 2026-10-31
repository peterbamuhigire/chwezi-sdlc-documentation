# Kaizen pass 2 — scope, preconditions and observation record

**Date:** 2026-10-31. **Engine:** Chwezi SDLC Documentation (this repository). **Branch:** `kaizen/2026-10-pass2`, created from `main` at `91b987db305f8ba9a49fd98ba8afa467aa9bb1e7`. The earlier branch `kaizen/2026-10` (29 October cycle) is an ancestor of `main`, so its work is already in the starting point. This is a continuation, not a first cycle: the 29 October evidence in `docs/kaizen/2026-10-engine-kaizen/` is the backlog input, and its open items were each re-confirmed below before use.

## Step 0 — preconditions

| Item | Result |
|---|---|
| `git status --porcelain` at start | Empty (0 lines). No uncommitted third-party files to preserve. |
| Starting branch / HEAD | `main` / `91b987db305f8ba9a49fd98ba8afa467aa9bb1e7` |
| Rules read | Portfolio Kaizen Standard, currentness gate, `AGENTS.md`, `31-kaizen-engine-and-product-improvement`, the 29 October final report, next-cycle record, frozen baseline, backlog, experiment log, validation record and source register. |
| Push, tag, pull request, paid model call, other-engine edit | None. |

## Host constraints (recorded because they decide what could be assessed)

This is a Fedora workstation with Python 3.14.8 and Node 22. Packages may not be installed, and none were.

| Dependency the repository pins | State on this host | Consequence |
|---|---|---|
| `ruamel.yaml`, `click`, `jsonschema`, `mistune`, `pytest`, `pytest-cov`, `python-docx` | Not importable (`python3 -c "import ruamel.yaml"` raises `ModuleNotFoundError`); `pip` is not installed | The kernel CLI (`python -m engine ...`), `validate_skill_engine.py`, `routing_smoke_test.py` and the pytest suite cannot run as registered. Each is `NOT_ASSESSED` as a registered check. |
| `pandoc`, `mmdc` (Mermaid CLI) | Not on `PATH` (`command -v pandoc mmdc` prints nothing) | The `.docx` build is `NOT_ASSESSED`. `scripts/build-doc.sh` exits 1 with `ERROR: Pandoc is required for DOCX builds but was not found on PATH.` |

To keep regressions visible without installing anything, three scratch tools were written **outside the repository** and are described in `04-validation-record.md`: a PyYAML-backed `ruamel.yaml` stand-in, a minimal pytest-compatible function runner, and a driver for the Phase 02 checks that do not need `jsonschema`. Results from them are labelled *indicative*. They never replace a registered result and are never reported as a pass of the registered command.

## Registered validators, run once before any change

| Exact command | Exit | Observation |
|---|---:|---|
| `python3 -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | 1 | `ModuleNotFoundError: No module named 'ruamel'`. **NOT_ASSESSED** as registered. Indicative run under the stand-in: exit 0; 159 active skills, 1 template, failure counts `{}`, 5 report-only `skill-bytes` warnings. |
| `python3 -X utf8 scripts/routing_smoke_test.py` | 1 | Same missing module. **NOT_ASSESSED** as registered. Indicative: 65/65 fixtures in top three; precision@1 57/65 (87.7%); 24 owned negatives (21 pass, 0 fail, 3 cross-engine `NOT_ASSESSED`). |
| `python3 -X utf8 scripts/routing_smoke_test.py --min-rank1 83 --lint-fixtures` | 1 | Same missing module. Indicative: floor met; fixture lint 0 findings over 89 prompts. |
| `python3 scripts/validate_engine.py` | 0 | `ENGINE CONTRACT: PASS` (this script needs no third-party package). |
| `python3 -X utf8 scripts/source_ingestion_guardrail.py` | 0 | `findings: 0`. |
| `python3 scripts/validate_plugin_packages.py` | 0 | 159 active skill paths; 1,707 checkout entries; 1,260 package-oriented entries; limit 5,000; `errors: 0`. |
| `python3 -m engine validate-skills` | 1 | `ModuleNotFoundError: No module named 'ruamel'`. **NOT_ASSESSED.** |
| `python3 -m pytest` | 1 | `No module named pytest`. **NOT_ASSESSED.** Indicative function runner: 215 pass, 8 fail, 1 skip, 26 import-or-fixture errors; every failure or error inspected traced to a missing package (`jsonschema`, `click`, `ruamel.yaml.error`). |

These indicative numbers equal the 29 October final results exactly (57/65, 24 owned negatives, 159 skills), so no regression since that cycle is visible at catalogue level.

## Step 1 — three practitioner tasks

All three ran in a disposable mirror of `HEAD` kept under the session scratch area. No project files were created in this repository.

### Task 1 — multi-tenant school-fees SRS with mobile-money receipts

- **Brief used (written for this exercise):** several private schools share one fee-collection system; each school sets its own fee items per term and class; bursars record what each pupil owes; parents pay by mobile money and receive a receipt straight after paying; head teachers see arrears; no school may see another school's pupils or money.
- **Route chosen:** `AGENTS.md` sends a new client document to `00-meta-initialization` (dev engine), then the numbered phase skill: `02-requirements-engineering/waterfall/01-initialize-srs`, with `fundamentals/during/07-requirements-validation` for review. The finance trigger in `AGENTS.md` fires (money flows, mobile money, receipts), so the accounting engine is a cross-cutting consult; it was out of scope for this SRS-only exercise.
- **Was the route right?** The route is right, but the lexical proxy in `scripts/routing_smoke_test.py` does not agree. The literal task sentence ranks `10-saas-multi-tenancy-architecture-spec` first (9.01) and `01-initialize-srs` second (9.00). A longer phrasing ("software requirements specification ...") ranks `19-game-software-requirements-specification` first (17.00) and does not place `01-initialize-srs` in the top four, because the proxy weights name tokens heavily. Live routing was not assessed (no model calls).
- **Scaffold:** `engine.scaffold.scaffold(..., "waterfall", "education", None)` ran. It wrote `_context/domain.md` containing only `domain: education`. The education pack (`domains/education/INDEX.md`) is a United States baseline (FERPA, COPPA, Section 508, WCAG 2.1) with feature modules for student records, learning management, gradebook and attendance. It has no fee, billing or receipt module.
- **Gates:** Phase 01 gate loaded and passed with 0 findings. The Phase 02 gate class could not be imported (it pulls in `jsonschema`), so its four checks that do not need that package were run directly. Four requirements were written to the NFR file. Results are in the defect table (D-05, D-06).
- **DOCX:** `bash scripts/build-doc.sh <srs-dir> SchoolFees_SRS` exited 1 with the clear Pandoc message. **NOT_ASSESSED.**

### Task 2 — vague, contradictory stakeholder brief

- **Brief used:** six raw statements with five contradictions: payment through the app only versus cash entered by the bursar; receipt immediately versus after settlement; one fee for all pupils versus half fee for scholarship pupils; offline operation versus real-time balances; tenant isolation versus district-wide visibility.
- **Route:** `fundamentals/during/04-requirements-analysis`, then `07-requirements-validation`. For the literal task sentence the proxy ranks `04-requirements-analysis` tenth, behind `11-experience-mapping-requirements`, `16-accounting-engine-design` and `10-requirements-metrics`; the skill's description does not mention contradictory or ambiguous source statements (D-07).
- **Paired experiment from the 29 October next-cycle record** (same five requirements, with and without `_registry/source-reconciliation.yaml`):

  | Variant | Phase 02 checks | Standalone `validate_source_reconciliation.py` |
  |---|---|---|
  | With register (five declared ambiguities) | FAIL, five HIGH `unresolved-ambiguity` findings | FAIL, five findings |
  | Register absent (the five contradictions silently resolved in the requirement text) | **PASS, 0 findings** | exit 1, "required source reconciliation register is missing" |

  The Phase 02 gate treats an absent register as a pass (`engine/checks/source_reconciliation.py:29`). Whether absence should block is an owner policy decision; no gate policy was changed (see `06-next-cycle.md`).

### Task 3 — ten-requirement traceability and test plan

Five functional and two non-functional requirements and three test cases were written, then `TestOraclesCheck` and `TraceabilityCheck` were run directly. Outcome: seven findings. Two of them are gate defects (D-08, D-09), one is a coverage gap (D-10), and the remaining three are correct (`FR-001` and `FR-003` without goal or test links).

## Defects found (critical, major, minor) with file and line

| ID | Severity | Defect | Evidence (file:line) |
|---|---|---|---|
| D-01 | **Critical** (privacy and safety, release-affecting) | A developer's local Claude Code permission file is tracked in this public repository. It names local usernames and client project names, and allows `Bash(bash:*)`, so a cloner who trusts the folder inherits an unrestricted shell allowlist. History cannot be rewritten in this cycle. | `.claude/settings.local.json` (tracked since an earlier commit; `.gitignore` has no entry for it) |
| D-02 | Major | Machine-specific and personal paths in 17 further live files outside `docs/` (43 lines across 18 files with D-01). A personal Windows downloads folder is cited as provenance in 14 skill, rule, hook, script and test files. `AGENTS.md` carries 18 lines with drive-letter WAMP paths, which contradicts its own rule that no engine location is assumed. `scripts/build-doc.sh` has 2 comment lines using such a path as an MSYS example, and one unit test uses one as sample data. `docs/skill-authoring-standard.md:40` carries one more. | Counted by the baseline measurement script; per-file counts in `01-baseline-scorecard.md`; router lines in `AGENTS.md` (47, 74-75, 82-86, 92, 200-201, 272, 440, 457, 463, 500 and others) |
| D-03 | Major | Seven dev-engine skill names still use the retired flat `skills/<name>` layout and do not resolve (the 29 October cycle repaired only the three the audit named). `skills/gis-mapping` has no counterpart in the dev engine at all (`gis` holds `gis-enterprise-domain` and `gis-platform-engineering`). No validator detects the class. | `03-design-documentation/03-api-specification/SKILL.md:144,260`; `02-requirements-engineering/fundamentals/before/02-elicitation-toolkit/references/domain-checklists.md:44,65,86` |
| D-04 | Major | The engine's own UX doctrine says WCAG 2.1 AA "is superseded here" (WCAG 2.2 AA), yet engine-level templates still prescribe 2.1. | `03-design-documentation/05-ux-specification/README.md:44`; `.../references/design-handoff.md:177`; `02-requirements-engineering/fundamentals/after/11-requirements-reuse/SKILL.md:163`; `.../02-elicitation-toolkit/references/domain-checklists.md:113`; `scripts/seed_demo_project.py:298` |
| D-05 | Major | `SmartNfrCheck` flags only a requirement that has a vague adjective **and** no metric. An NFR with no metric at all passes: "shall be available at all times" and "shall respond quickly" both returned no finding. | `engine/checks/nfr_smart.py:7,24` |
| D-06 | Minor | The same check's unit list omits hours, days, seconds and minutes spelled out, so a valid threshold ("restore service within ≤ 4 hours") is a false positive when the sentence also contains "reliable". | `engine/checks/nfr_smart.py:8` |
| D-07 | Major | `04-requirements-analysis` is not discoverable for the contradictory-brief task (rank 10 for the task sentence): its description omits contradictory and ambiguous source statements. | `02-requirements-engineering/fundamentals/during/04-requirements-analysis/SKILL.md` frontmatter `description` |
| D-08 | Major | `TestOraclesCheck` rejects `NFR-###` and module-qualified `FR-META-006` in a test's `requirement_trace` as "non-FR entries", although Phase 05's own pattern accepts module-qualified IDs. A correct performance test that traces its NFR is a HIGH finding. | `engine/checks/test_oracles.py:8,60` against `engine/gates/phase05.py` (`_FR_ID`) |
| D-09 | Major | No check enforces unique definition of a requirement identifier. Two `**FR-001**` statements in different files raise nothing, and `sync` always returns an empty error list. Task 3 requires "uniquely identified". | `engine/sync.py:62`; no `duplicate` handling in `engine/checks/` |
| D-10 | Major | Phase 09 traceability covers only `FR-` identifiers. `NFR-002` with no goal link and no test case produced no finding. | `engine/checks/traceability.py:31` |
| D-11 | Minor | `domains/education` is a US-only baseline with no fee or receipt module, so a school-fees SRS scaffolded with `--domain education` receives FERPA and COPPA defaults and nothing about fees. | `domains/education/INDEX.md:5-9,19-23` |
| D-12 | Minor | First-run experience: the catalogue validators die with a Python traceback when `ruamel.yaml` is absent, with no instruction. | `scripts/validate_skill_engine.py:13`; `scripts/routing_smoke_test.py:28` |
| D-13 | Minor | CI does not run the October validators directly (`validate_plugin_packages.py`, `validate_traceability_evidence.py`, `check_codex_discovery_summary.py`); they are covered only through their pytest files. | `.github/workflows/engine.yml` |

## Prior open items re-confirmed

| 29 October item | Status now |
|---|---|
| Standards clause registry stale (IEEE 830, 42010:2011, 29119-3:2013) | **Open and unchanged.** 57 files and 163 lines outside `docs/` still cite IEEE 830; 4 files cite 42010:2011; 6 files cite 29119-3:2013 (measurement script). Clause remapping needs authoritative text and owner approval; not attempted. |
| Source completeness is human-owned | Open by design; the paired experiment above adds evidence (absent register passes). |
| Task 2 owner decisions unresolved | Open; the fresh task-2 fixture reproduces the blocking behaviour. |
| Trace chain lacks goal links and execution | Open; the checked-in fixture still reports zero goal links and zero executed tests. |
| Route coverage sparse (4 of 159) | Open: independent recount gives 4 of 159 skills with at least three positives and two owned negatives. |
| Public package acceptance unknown | Open and out of scope (no submission authority). |
| Dev-engine handoff paths | Partly closed in October; D-03 shows the same class still open elsewhere. |
| Hospitality absolute path (September audit) | Not present in `02-requirements-engineering/hospitality-operating-model-srs/SKILL.md`; confirmed again. |

## Integrity limits

Scores in `01-baseline-scorecard.md` are reviewer judgements against named evidence, not measurements of customer outcomes. Live LLM routing, native Word accessibility, real-font rendering, Phase 09 registry checks (need `jsonschema`) and the full pytest suite are `NOT_ASSESSED` on this host.
