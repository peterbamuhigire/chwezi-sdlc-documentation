# Contributing to Chwezi SDLC Documentation

Active skills live under the numbered phase roots. Discover them from the filesystem; do not use a cached README table as the catalogue authority.

## Change a skill

1. Read `AGENTS.md`, `CLAUDE.md`, and [the local authoring standard](docs/skill-authoring-standard.md).
2. Start new entrypoints from [the skill template](templates/skill/SKILL.md). Keep the directory name and frontmatter `name` identical.
3. Preserve the skill's domain workflow, examples, references, terminology, and project pathing. Add domain decisions and evidence contracts from real context, not generic compatibility text.
4. Update [routing fixtures](tests/routing-fixtures.json) when a description, trigger, exclusion, or neighbour boundary changes.
5. For finance-touching content, run the finance doctrine quality gate. For human-facing content, apply `28-anti-ai-slop` during authoring and `29-ai-slop-audit` before release.

## Required checks

The default pytest configuration enforces the repository coverage policy and
therefore requires the development extra. From a fresh checkout, install the
pinned packages in a virtual environment before running the default suite:

```sh
python3 -m pip install -c requirements-ci.txt -e ".[dev,docs]"
python3 -m pytest -q
```

If `pytest-cov` cannot be installed in the current environment, do not report a
coverage pass. Run structural or logic-only tests with `-o addopts=` and record
coverage as `NOT ASSESSED`.

The default run covers `engine/tests` (535 passed, 5 skipped, coverage 96.19%
against the 90% floor on 2026-10-31). Run the remaining Python tests, the
validators and the whitespace check as well. `README.md` ("Validation") gives
the result each one should produce and the tool it needs.

```sh
python3 -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json
python3 -X utf8 scripts/routing_smoke_test.py --min-rank1 83 --lint-fixtures --min-covered 8
python3 -X utf8 scripts/validate_engine.py
python3 -m engine validate-skills
python3 -X utf8 scripts/validate_plugin_packages.py
python3 scripts/check_portable_paths.py
python3 scripts/check_cross_engine_refs.py --dev-engine-root <chwezi-dev-engine-checkout>
python3 scripts/check_standards_currency.py
python3 scripts/validate_source_register.py
python3 scripts/validate_traceability_evidence.py engine/tests/fixtures/traceability-evidence.json
python3 scripts/validate_sdd_phase_boundaries.py --feature-dir engine/tests/fixtures/sdd_feature
python3 scripts/validate_requirements_decision.py engine/tests/fixtures/requirements_decision/reuse.json
python3 -X utf8 scripts/source_ingestion_guardrail.py
python3 -m pytest -q -o addopts= tests
git diff --check
```

Without a dev-engine checkout, `check_cross_engine_refs.py` still runs but reports
category paths as `NOT_ASSESSED`. `validate_source_register.py` is date-driven: it
starts failing on 2026-11-30 until the overdue source records are re-verified (see
"Quality and improvement" in `README.md`).

Run the canonical quick validator for each changed skill directory:

Resolve the [Chwezi Dev Engine](https://github.com/peterbamuhigire/chwezi-dev-engine)
through the engine-routing table of your runner (or set `CHWEZI_DEV_ENGINE_ROOT`),
then run its canonical validator:

```sh
python3 -X utf8 "$CHWEZI_DEV_ENGINE_ROOT/skills/sdlc-meta/skill-writing/scripts/quick_validate.py" <skill-directory>
```

The baseline must remain empty. Do not add findings to it. A deliberate active-skill or template-count change requires an evidence-backed routing decision, updated fixtures, and an explicit baseline count update in the same change.

## Release procedure

1. Fetch `origin` and confirm local `main` is not behind `origin/main`.
2. Run the full checks above and inspect the complete diff for unrelated files, secrets, caches, and broken references.
3. Stage only intended files and review the staged stat plus representative skill, validator, fixture, and documentation diffs.
4. Commit once with a message that states the release outcome.
5. Push without force. Verify `HEAD` and `origin/main` resolve to the same commit and the worktree is clean.
