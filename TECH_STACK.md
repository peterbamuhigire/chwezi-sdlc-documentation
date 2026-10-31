# Chwezi SDLC Documentation Technology Stack

- **Primary Language:** Python 3.11 or later for the validation kernel in `engine/` and the scripts in `scripts/`; last run on Python 3.14.8. Node.js 18 or later runs the installer, the hooks and the Plan Canvas review tool. The pinned packages are listed in [`DEPENDENCIES.md`](DEPENDENCIES.md).
- **Skills:** Each skill is a `SKILL.md` playbook under a numbered phase folder, with local references and templates beside it. 100 skills also carry a `logic.prompt`, and eight Waterfall skills keep a Python helper.
- **Execution Environment:** Skills run inside the active coding agent and operate on the active `projects/<ProjectName>/` workspace. The kernel runs locally. No external service or database is required, and no code in this repository calls a model.
- **Documentation Flow:** Skills write Markdown into the active project's phase folders. The Waterfall pipeline emits `SRS_Draft.md`, with `08-semantic-auditing` adding `Audit_Report.md` for traceability. `scripts/build-doc.sh` renders Mermaid blocks to figures and builds the `.docx` with Pandoc.
- **Validation:** `python3 -m engine validate` runs deterministic phase gates; the scripts and tests that guard the catalogue are listed in the "Validation" section of [`README.md`](README.md).
