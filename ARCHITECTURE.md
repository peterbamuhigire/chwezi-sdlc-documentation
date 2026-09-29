# Architecture Overview

Chwezi SDLC Documentation uses `projects/<ProjectName>/` as the canonical runtime workspace. The project context source of truth is `projects/<ProjectName>/_context/`, while generated artifacts live under the appropriate phase/document directories inside the same project workspace.

For backward compatibility, many existing skill-local instructions still refer to `../project_context/` and `../output/`. Those relative paths are execution aliases into the active project workspace, not a separate architectural model.

The repository is arranged as a phase-oriented catalogue: `00-meta-initialization`
plus SDLC phases `01` through `09`, with Waterfall, Agile, and Hybrid tracks
under Phase 02. The active count is controlled by the
[`skill-quality-baseline.json`](tests/skill-quality-baseline.json) catalogue
control and checked against filesystem truth by
[`validate_skill_engine.py`](scripts/validate_skill_engine.py). Each skill
encapsulates:

1. **Input Context:** Reads specific project context files from the active workspace, canonically `projects/<ProjectName>/_context/*.md` (vision, features, tech stack, quality standards, etc.).
2. **Logic Core:** Executes a Python script (or LLM prompt) designed for a particular IEEE section.
3. **Output Target:** Writes or rewrites generated artifacts in the active project workspace, commonly through skill-local `../output/...` aliases.

The `skills/` directory is the standard skill repository layout: each portable skill lives at `skills/<skill-name>/SKILL.md` with local references and assets beside it. Root-level project documentation remains at the repository root, while `docs/`, `skills/`, and `projects/` hold repository documentation, skill entrypoints, and untracked client workspaces respectively. This architecture enforces separation of concerns (introduction, interfaces, behavior, logic, attributes, and validation) while ensuring each phase consumes only the data projected by previous phases.
