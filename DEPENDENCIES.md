# Dependency and Runtime Manifest

This document lists what Chwezi SDLC Documentation needs to run its validation kernel, its scripts and its document build. Versions come from `pyproject.toml`, `requirements-ci.txt` and `scripts/diagram-render/package.json`. The measured results of each check are in the "Validation" section of [`README.md`](README.md).

## Engine Stack

- **Language:** Python 3.11 or later (`requires-python` in `pyproject.toml`). The kernel was last run on Python 3.14.8; CI runs Python 3.11.
- **Install:** `python3 -m pip install -c requirements-ci.txt -e ".[dev,docs]"`, in a virtual environment.
- **Python packages:**

  | Package | Pin in `requirements-ci.txt` | Used for |
  |--------|--------|--------|
  | click | 8.3.3 | The `python3 -m engine` command line. |
  | ruamel.yaml | 0.19.1 | Frontmatter and YAML parsing in the kernel; `scripts/validate_skill_engine.py` and `scripts/routing_smoke_test.py`. |
  | jsonschema | 4.26.0 | Identifier registry and change-impact schemas; `scripts/validate_traceability_evidence.py`. |
  | mistune | 3.3.4 | Declared in `pyproject.toml`; no import of it was found in the repository on 2026-10-31. |
  | pytest, pytest-cov | 9.0.3, 7.1.0 | `python3 -m pytest`; the default options enforce a 90% coverage floor. |
  | python-docx | 1.2.0 | The temporary Word style template (`scripts/create-reference-docx.py`) and the clean-template build test. |
  | setuptools | 83.0.0 | Build backend. |
  | pyyaml | Not pinned | `scripts/validate_decision_frontier.py` and `tests/agent-integration/test_srs_agent_contract.py`. Install it separately when you run them. |

- **Nine validators need no package at all** (Python 3 and a Git checkout), all in `scripts/`: `validate_engine.py`, `validate_plugin_packages.py`, `check_portable_paths.py`, `check_cross_engine_refs.py`, `check_standards_currency.py`, `validate_source_register.py`, `validate_sdd_phase_boundaries.py`, `validate_requirements_decision.py` and `source_ingestion_guardrail.py`. All nine were run with the third-party packages above made unimportable and exited 0.
- **No cloud SDK, API key or `.env` file is needed.** The repository's code makes no model call; skills run inside the active coding agent.
- **Environment variables the code reads:**
  - `CHWEZI_DEV_ENGINE_ROOT`: dev-engine checkout for `scripts/check_cross_engine_refs.py` (or pass `--dev-engine-root`).
  - `BUILD_DOC_TEMPLATE`: Word style template for `scripts/build-doc.sh` instead of `templates/reference.docx`.
  - `PYTHON`: interpreter for `scripts/build-doc.sh` (it falls back to `python3` when `python` is absent).
  - `PUPPETEER_EXECUTABLE_PATH`: Chrome or Edge for the Mermaid renderer. `SRS_DIAGRAM_FONT_FILE`: optional font file for diagram rendering.
  - `CHWEZI_GATEGUARD` and `CHWEZI_GATE_EXTRA_PATTERNS`: the destructive-command hook in `hooks/`.
  - `ECC_PLAN_CANVAS_STATE_DIR`: state folder for the Plan Canvas review tool.
- **Local vs. cloud execution:** every script runs locally. Network access is needed only to clone the repository, to install packages (`pip`, `npm ci`) and to read the primary sources when a kaizen cycle re-verifies a currentness claim.

## Document Build Tools

| Tool | Needed for | Not needed for |
|--------|--------|--------|
| Pandoc | `bash scripts/build-doc.sh` and the `.docx` tests. | Any validator. |
| Node.js 18 or later | `install.sh`, the Mermaid renderer, the hook tests and the Plan Canvas tests. | The Python kernel. |
| `@mermaid-js/mermaid-cli` 12.0.0 (`npm ci` in `scripts/diagram-render` with `PUPPETEER_SKIP_DOWNLOAD=1`) and a local Chrome or Edge | Rendering Mermaid blocks to figures inside `scripts/build-doc.sh`. | Documents without Mermaid blocks. |
| PowerShell | `install.ps1`, `scripts/setup-srs-project.ps1`, the generated `export-docs.ps1`. | Every registered check; use the `.sh` equivalents elsewhere. |

LibreOffice and container runtimes are not required by any check in this repository.

## Cross-Platform Compatibility

### Linux and macOS

- Run the shell scripts through `bash`. No script in the repository is tracked with the executable bit, so `./install.sh` and `./scripts/build-doc.sh` fail with `Permission denied`; use `bash install.sh` and `bash scripts/build-doc.sh`.
- Use `python3`. Inside an activated virtual environment `python` is the same interpreter.
- Install Pandoc from your package manager when you need `.docx` output.
- Keep `git` configured to respect LF endings (`core.autocrlf=input`).

### Windows

- `install.ps1` and `scripts/setup-srs-project.ps1` need PowerShell 7 or Windows PowerShell; they have not been run on the Linux workstation that last validated the engine.
- Git Bash runs `install.sh` and `scripts/build-doc.sh` directly; `scripts/build-doc.sh` converts paths with `cygpath` for the native Pandoc program.
- Keep `core.autocrlf` and `.gitattributes` settings consistent before committing to avoid line-ending churn.

## Repository Architecture Constraints

- The engine needs read and write access to the active `projects/<ProjectName>/_context/` folder and the phase output folders for context ingestion and artefact delivery. `projects/` is untracked and gitignored; project data is never committed to this public repository.
- The repository is stateless: no project-specific data belongs under any numbered phase folder, `engine/`, `domains/` or `docs/`. The legacy skill-local paths `../project_context/` and `../output/` are aliases into the active workspace (see [`docs/pathing-model.md`](docs/pathing-model.md)).
- The seeding skill `01-initialize-srs` creates the initial template files but never persists project answers inside this repository.

## Resources

No hardware minimum has been measured. On the Fedora workstation that last validated the engine, `python3 -m pytest` took about 28 seconds, and the checkout including `.git` occupied 83 MB.
