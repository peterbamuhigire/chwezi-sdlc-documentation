# Architecture Overview

Chwezi SDLC Documentation uses `projects/<ProjectName>/` as the canonical runtime workspace. The project context source of truth is `projects/<ProjectName>/_context/`, while generated artifacts live under the appropriate phase/document directories inside the same project workspace.

For backward compatibility, many existing skill-local instructions still refer to `../project_context/` and `../output/`. Those relative paths are execution aliases into the active project workspace, not a separate architectural model.

The repository is arranged as a phase-oriented catalogue of nine numbered phase
folders, `01-strategic-vision` to `09-governance-compliance`, with Waterfall,
Agile, Hybrid and fundamentals tracks under `02-requirements-engineering`.
Methodology selection (`00-meta-initialization`) belongs to the Chwezi Dev
Engine, not to this repository. The active count is controlled by the
[`skill-quality-baseline.json`](tests/skill-quality-baseline.json) catalogue
control (159 active skills and 1 template on 2026-10-31) and checked against
filesystem truth by
[`validate_skill_engine.py`](scripts/validate_skill_engine.py). Each skill is a
`SKILL.md` playbook that an agent follows, with local `references/`, templates and
sometimes `examples/` beside it, and it encapsulates:

1. **Input Context:** Reads specific project context files from the active workspace, canonically `projects/<ProjectName>/_context/*.md` (vision, features, tech stack, quality standards, etc.).
2. **Logic Core:** The procedure in `SKILL.md` and its references. 100 skills also ship a `logic.prompt`, and the eight Waterfall skills `01-initialize-srs` to `08-semantic-auditing` keep a Python helper. The validation kernel checks the result deterministically.
3. **Output Target:** Writes or rewrites generated artifacts in the active project workspace, commonly through skill-local `../output/...` aliases.

Around the skills sit `engine/` (the validation kernel: parsers, checks, phase gates, registries, reporters, diagram IR and the `python3 -m engine` command line), `scripts/` (validators, the document build pipeline and the installers), `domains/` (11 domain packs), `templates/`, `references/`, `rules/`, `hooks/`, `tests/` and `docs/`. There is no `skills/` directory in this repository. Root-level project documentation stays at the repository root, and `projects/` holds untracked client workspaces. This architecture enforces separation of concerns (introduction, interfaces, behavior, logic, attributes, and validation) while ensuring each phase consumes only the data projected by previous phases.
