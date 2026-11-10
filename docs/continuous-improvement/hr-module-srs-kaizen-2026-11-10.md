# 2026-11-10: HR module SRS skill (HR-systems kaizen, phase P4)

## Baseline

Search of the engine for HR, payroll, leave, org structure and position management found
no skill for an HR module SRS. Neighbours: `18-embedded-accounting-engine-srs` (payroll as
a money flow), `01-initialize-srs` (generic). Nothing deleted, moved or renamed.

## Changes

- New skill `02-requirements-engineering/20-hr-module-srs` (SKILL.md plus one reference):
  15-subsection HR requirements template, `FR-HR-` wording, acceptance-criteria patterns with
  oracles and synthetic data, parameterised statutory values, contiguous HR document series.
- Registered in `.claude-plugin/plugin.json`, `docs/skill-catalogue.md`,
  `tests/skill-quality-baseline.json`, `tests/routing-fixtures.json` (two fixtures).
- Counts 159 to 160 in the live count surfaces (README, AGENTS, ARCHITECTURE, PROJECT_BRIEF,
  docs/README, catalogue, marketplace description, baseline). Historical records and
  synthetic test summaries left as they were.

## Not done

- No "Find the right skill" README row and no neighbour cross-references (P5).
- Statutory rows are the owner's law notes of 10 Nov 2026, not re-checked against the
  instruments (NOT_ASSESSED). NOT_VERIFIED: Employment (Amendment) Act 2025, DPP
  Regulations numbers, OSH Act, ITA section for 6% WHT, severance, disguised-employment test.
- Live host discovery, golden and pressure cases: NOT_ASSESSED.

## Re-measure (10 Nov 2026, Windows 11)

- `validate_engine.py`: ENGINE CONTRACT PASS.
- `validate_skill_engine.py --baseline`: 160 active skills, no failures (5 report-only size warnings, none for the new skill).
- `routing_smoke_test.py`: 75/75 fixtures, top-3 1.000, precision@1 67/75; 0 owned-negative failures, 3 cross-engine NOT_ASSESSED.
- `pytest engine/tests`: 4 failed, coverage 96.75%. Failures are `test_docx_build.py` (2, pandoc) and `test_portable_paths.py` (2, git in temp repo); environmental, not shown to be caused by this change, not re-run on a clean checkout.
- `validate_plugin_packages.py`: 2 errors, file counts 63,019 and 25,114 against 5,000 (local untracked trees); path count 160. Same class as the dev-engine budget test.
