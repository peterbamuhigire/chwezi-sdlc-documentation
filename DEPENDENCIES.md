# Dependency & Runtime Manifest

This document enumerates the installation and runtime prerequisites for the Chwezi SDLC Documentation engine so it can operate reliably within the IEEE/ISO-aligned workflow and the resource constraints often encountered in Ugandan environments (e.g., intermittent power, mixed local/cloud execution).

## Engine Stack

- **Language:** Python 3.10+ (required for advanced type hints, dataclasses, and modern async patterns used by the skill orchestrator).
- **Required Modules & Libraries:**

  | Module | Purpose |
  |--------|---------|
  | jinja2 | Templating for SRS sections, tables, and reusable snippets. |
  | regex (via `import re`) | Semantic auditing, token scanning, and anomaly detection heuristics. |
  | openai / anthropic / vertexai (as configured) | Optional LLM SDKs used when the parent project opts for cloud inference; configure only the providers in use. |
  | python-dotenv | Load `.env` credentials securely for AI SDK keys and database endpoints. |
  | pyyaml | Configuration parsing when skills interact with structured context metadata. |

- **Environment Variables:**
  - Store provider-specific keys (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `VERTEXAI_KEY`) in a `.env` file at the parent root; use `.env.example` to document the required names.
  - `SKILLS_LOG_LEVEL` controls verbosity (default `INFO`).
  - `PROJECT_CONTEXT_PATH` / `OUTPUT_PATH` may be overriden if the parent repo uses custom directories, but defaults must remain `../project_context/` and `../output/`.
- **Local vs. Cloud Execution:**
  - Local: All templating, file IO, Markdown generation, LaTeX rendering, and regression logic is executed within this repository and Python runtime.
  - Cloud: LLM calls happen through the configured provider SDKs; ensure offline-friendly fallbacks (brief local prompts or caching) when connectivity is limited.

## Cross-Platform Compatibility

### Linux / Unix (Ubuntu, Debian, etc.)

- Bash 4.0+ is required for shell scripts (XDG path handling, arrays).
- Install system packages: `pandoc` (for optional PDF exports), `build-essential`, and `python3.10-venv`.
- Use `pip install -r requirements.txt` within a virtual environment (e.g., `venv` or `pipx`).
- Ensure `git` is configured to respect LF endings (`core.autocrlf=input`).

### Windows

- Prefer PowerShell 7.x or WSL2 to avoid legacy PowerShell/Command limitations.
- For WSL2, map the repository directory with consistent permissions and run scripts via `bash` or `pwsh` to maintain path parity.
- Warning: keep `core.autocrlf` and `.gitattributes` settings consistent before committing to avoid line-ending churn.
- If using local CMD shells, install `python3.10` from the Windows store or an official installer and add it to `%PATH%`.

## Repository Architecture Constraints

- The engine **must** have read/write access to the active `projects/<ProjectName>/_context/` and output folders for context ingestion and artefact delivery. Document this during onboarding so project workspaces use the canonical SRS pathing model.
- The repository is stateless: **no project-specific data** should ever be written under `skills/` or any part of `chwezi-sdlc-documentation`—all outputs belong to `../output/`, and inputs live in `../project_context/`.
- The seeder skill (`01-initialize-srs`) creates the initial template files but never persists project answers inside this repo.

## Recommended Baseline Hardware

- **Memory:** 16 GB RAM enables concurrent prompt handling, LaTeX rendering, and background audits without swapping. Lower RAM configurations risk slowing down Skills 06/07 during data-heavy analysis.
- **CPU:** Multi-core CPU such as Intel Xeon E5 (e.g., HP Z440 workstation) or modern Ryzen/EPYC equivalent to maintain parallel Python workers and I/O throughput.
- **Storage:** SSD with at least 10 GB free to store intermediate drafts, log data, and cached AI responses; configure logs to rotate via environment settings if disk space is constrained.
- **Network:** When using cloud LLMs, allow outbound TLS traffic on ports 443/80; for offline runs on the HP Z440, rely on local smaller LLMs and disable cloud API keys in `.env` to avoid accidental calls.

By codifying these prerequisites you ensure the engine keeps operating through local resilience measures and remains auditable for ISO/IEC 15504 process assessments.
