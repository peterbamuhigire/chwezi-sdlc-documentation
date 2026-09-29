# Chwezi SDLC Documentation Technology Stack

- **Primary Language:** Python 3.11 (scripts under each skill directory). All automation leverages the standard library plus Markdown parsing utilities.
- **Execution Environment:** Skills run inside this unified repository and operate on the active `projects/<ProjectName>/` workspace. No external services or databases are required.
- **Documentation Flow:** Each skill emits Markdown into `../output/SRS_Draft.md`, with `08-semantic-auditing` adding `Audit_Report.md` for traceability.
- **Skills Layout:** Portable skills live under `skills/<skill-name>/SKILL.md`; each skill keeps local references, templates, and helper assets beside its entrypoint.
