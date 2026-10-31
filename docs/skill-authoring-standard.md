# Skill authoring and release standard

This repository treats each active `SKILL.md` as a portable procedure for Claude Code and Codex. The active roots are discovered from the numbered phase directories; `templates/skill/SKILL.md` is a template and is not active.

## Required contract

Every active skill must satisfy all of these rules.

1. Frontmatter contains only `name`, `description`, `license`, `allowed-tools`, and `metadata`. `name` matches the directory. `description` is one line, starts with `Use when`, is no longer than 350 characters, and separates the skill from its nearest neighbour.
2. `metadata.portable` is `true` and `metadata.compatible_with` is exactly `claude-code`, then `codex`.
3. The body contains `Use When`, `Do Not Use When`, `Required Inputs`, `Workflow`, `Outputs`, `Evidence Produced`, `Capability and permission boundaries`, `Degraded mode`, `Decision Rules`, `Quality Standards`, `Anti-Patterns`, and `References`.
4. Inputs name the artefact, source or provider, whether it is required, and the response when it is missing. Outputs name the consumer and an observable acceptance condition.
5. The workflow is ordered. It identifies a stop condition and a recovery action. Decision rules name the action and the failure or risk avoided.
6. Review, audit, critique, analysis, and planning skills are read-only by default. Editing, publishing, production mutation, destructive action, spending, and certification claims require explicit authority.
7. Degraded mode reports the narrowest useful qualified result. An unavailable or unassessed check never becomes a pass.
8. Evidence-bearing skills state what evidence is produced and how a reviewer can inspect it.
9. Anti-patterns contain at least five concrete failures, each paired with a correction.
10. Relative links resolve. Referenced `logic.prompt`, templates, examples, and reference files exist. Runner-specific command names stay outside portable skill bodies.
11. `SKILL.md` stays at or below 500 lines. Long catalogues, schemas, case studies, and background move to a directly linked reference whose first section links back to the parent skill.
12. Generated human-facing content passes `09-governance-compliance/28-anti-ai-slop`; reviews also use `09-governance-compliance/29-ai-slop-audit`.

## Authoring sequence

1. Copy `templates/skill/SKILL.md` and choose the nearest neighbouring routes.
2. Write the input and output contracts before the workflow.
3. Add domain decisions, stop conditions, recovery, evidence, and acceptance conditions from real repository context. Do not fill these sections with compatibility boilerplate.
4. Add or update routing fixtures when a trigger or neighbour boundary changes.
5. Run:

```powershell
python -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json
python -X utf8 scripts/routing_smoke_test.py
python -m engine validate-skills
python -X utf8 scripts/validate_engine.py
```

For a changed skill, also run the canonical validator with the directory path:

```powershell
python -X utf8 <dev-engine-root>/skills/sdlc-meta/skill-writing/scripts/quick_validate.py <skill-directory>
```

## Release rule

The machine baseline is a zero-debt assertion, not a waiver. `failure_counts` must remain empty, every routing fixture must place the expected skill in the top three, active and template counts must match the reviewed catalogue, and the repository-specific test suite must pass before release.
