# Chwezi SDLC Documentation: New Project Setup Guide

## Prerequisites

| Requirement | Windows | Ubuntu/macOS |
|-------------|---------|--------------|
| Git | [git-scm.com](https://git-scm.com/download/win) | `sudo apt install git` / `brew install git` |
| GitHub CLI (optional) | [cli.github.com](https://cli.github.com/) | `sudo apt install gh` / `brew install gh` |
| Claude Code | [claude.ai/claude-code](https://claude.ai/claude-code) | Same |
| Python 3.11 or later, and the pinned packages | Install from python.org, then `python3 -m pip install -c requirements-ci.txt -e ".[dev,docs]"` | Your package manager, then the same `pip` command in a virtual environment |
| Node.js 18 or later (installer and hook tests) | [nodejs.org](https://nodejs.org/) | Your package manager |
| Pandoc (only for `.docx` output) | [pandoc.org/installing](https://pandoc.org/installing.html) | Your package manager |

[`DEPENDENCIES.md`](DEPENDENCIES.md) lists every package, pin and optional tool.

## Quick Start (Junior Operator Path)

If you only need to stand up a new project workspace from a shipped
example and run the validation gates, run these commands:

```bash
git clone https://github.com/peterbamuhigire/chwezi-sdlc-documentation.git
cd chwezi-sdlc-documentation
# Resolve engineering/methodology skills through the Chwezi Dev Engine:
#   https://github.com/peterbamuhigire/chwezi-dev-engine
# Resolve finance/accounting doctrine through the Chwezi Accounting Doctrine:
#   https://github.com/peterbamuhigire/chwezi-accounting-doctrine
python3 -m pip install -c requirements-ci.txt -e ".[dev,docs]"
python3 -m engine doctor
python3 -m engine new-project Acme --methodology waterfall --domain government --example uganda-public-sector
python3 -m engine validate projects/Acme
```

Expect two things on a clean checkout. `doctor` reports `[FAIL] Skills submodule`,
because that check looks for a `skills/` folder and applies to a project
repository that vendors this engine (Step 2 below), and it reports
`[FAIL] Pandoc available` when Pandoc is absent. The shipped example supplies
context and registries only, so `validate` exits 1 with 22 findings until the
Phase 03 to Phase 09 documents exist. To see a workspace that passes, run
`python3 scripts/seed_demo_project.py` and then
`python3 -m engine validate projects/_demo-hybrid-regulated`.

The remaining sections below cover the full provisioning flow when you
also need to create an empty GitHub repo, run the setup script, and
wire the unified SRS engine into that project workspace.

## Step 1: Create an Empty Repo on GitHub

Create a new repository on GitHub (empty, no README). Copy the clone URL.

**Via GitHub CLI:**

```bash
gh repo create my-srs-project --public --clone=false
```

**Via browser:** github.com > New Repository > Create (no initialization files).

## Step 2: Run the Setup Script

Both scripts live in `scripts/` of this repository. Run them from a checkout of
this engine; the first argument is the empty repository you created in Step 1.

### Windows (PowerShell)

```powershell
# If script execution is blocked, run this first (one-time):
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Run the setup script:
.\scripts\setup-srs-project.ps1 -RepoUrl "https://github.com/user/my-project.git"

# Or specify a target directory:
.\scripts\setup-srs-project.ps1 -RepoUrl "https://github.com/user/my-project.git" -TargetDir "..\my-project"
```

### Linux / macOS / WSL

```bash
# Run the setup script through bash (the repository does not track the executable bit):
bash scripts/setup-srs-project.sh https://github.com/user/my-project.git

# Or specify a target directory:
bash scripts/setup-srs-project.sh https://github.com/user/my-project.git ~/projects/my-project
```

Neither setup script was run while this guide was last checked (it needs a
GitHub repository to clone), so the steps below describe what the scripts do,
read from their source.

### What the Script Does

1. Clones your empty repo to the target directory
2. Adds or links the unified `chwezi-sdlc-documentation` engine under `skills/` for the target project workflow
3. Verifies the engine checkout is available
4. Creates `project_context/` with starter templates:
   - `vision.md` - Project vision and business goals
   - `stakeholders.md` - Stakeholder registry
   - `glossary.md` - IEEE 610.12 terminology
5. Creates `output/` directory for generated documentation
6. Sets up `.gitignore`
7. Creates `export/` and the `export-docs.sh` and `export-docs.ps1` delivery scripts
8. Creates an initial commit and optionally pushes

### Resulting Directory Structure

```
my-project/
├── skills/                    # chwezi-sdlc-documentation engine checkout (git submodule)
│   ├── 01-strategic-vision/ ... 09-governance-compliance/   # the numbered phase skills
│   │   └── 02-requirements-engineering/
│   │       ├── waterfall/     # Waterfall SRS skills (01 to 09)
│   │       └── agile/         # INVEST user stories
│   ├── engine/                # validation kernel
│   ├── domains/               # domain packs
│   ├── docs/
│   ├── AGENTS.md              # router; CLAUDE.md imports it
│   ├── README.md
│   └── ...
├── project_context/           # YOUR project data (source of truth)
│   ├── vision.md
│   ├── stakeholders.md
│   └── glossary.md
├── output/                    # Generated SRS documentation
├── export/                    # Delivery copies of generated .docx files
├── export-docs.sh, export-docs.ps1
├── .gitignore
└── .gitmodules
```

## Step 3: Fill In Project Context

Before running any skills, populate your project context files:

```
project_context/vision.md       # Required - project name, problem, goals
project_context/stakeholders.md # Required - who is involved
project_context/glossary.md     # Recommended - domain terminology
```

## Step 4: Open Claude Code and Establish Shared Understanding

Open Claude Code in your new project directory:

```bash
cd my-project
claude
```

### Kick-off Prompt

Paste this prompt to open the shared-understanding session. Replace the placeholders with your actual project details:

```
I'm starting a new SRS documentation project. Here's what I need to document:

**Project:** [Your project name]
**Domain:** [e.g., Healthcare SaaS, Restaurant POS, E-commerce Platform]
**Description:** [2-3 sentences about what the system does]
**Target Users:** [Who will use this system?]
**Key Features:** [List 3-5 major features]
**Technology Stack:** [e.g., PHP/Laravel, Android/Kotlin, React/Node.js]
**Constraints:** [Regulatory, budget, timeline, existing systems]

Please help me:
1. Refine the project vision and identify missing context
2. Determine the best methodology (Waterfall/Agile/Hybrid)
3. Create a documentation roadmap
4. Identify which domain skills from skills/<skill-name>/SKILL.md are relevant

Start by reading my project_context/ files, then establish shared
understanding with the decision-frontier method before we begin generating
documentation.
```

Claude will use the engine's decision-frontier elicitation method (`02-requirements-engineering/fundamentals/before/02-elicitation-toolkit/references/decision-frontier-elicitation.md`) to confirm your intent before any documentation is generated. The `superpowers:brainstorming` skill may be used as an optional aid where it is installed; it is not required.

## Step 5: Run Meta-Initialization

After the shared-understanding step, run the entry-point skill:

```
Run skill: 00-meta-initialization (engineering catalog engine)
```

This will:
- Scan your project directory and context files
- Detect project characteristics
- Recommend the appropriate methodology
- Generate a documentation roadmap
- Seed any missing template files in `project_context/`

## Step 6: Execute the Documentation Pipeline

Based on the recommended methodology:

### Waterfall Track (SRS in the IEEE 830 section layout)

Execute phases sequentially. Each phase builds on the previous:

| Phase | Skill | Output |
|-------|-------|--------|
| 1 | `02-requirements-engineering/waterfall/01-initialize-srs` | SRS scaffold, Section 1 |
| 2 | `02-requirements-engineering/waterfall/02-context-engineering` | Section 2 (Overall Description) |
| 3 | `02-requirements-engineering/waterfall/03-descriptive-modeling` | Data models, entity relationships |
| 4 | `02-requirements-engineering/waterfall/04-interface-specification` | Section 3.1 (External Interfaces) |
| 5 | `02-requirements-engineering/waterfall/05-feature-decomposition` | Section 3.2 (System Features) |
| 6 | `02-requirements-engineering/waterfall/06-logic-modeling` | Business rules, algorithms |
| 7 | `02-requirements-engineering/waterfall/07-attribute-mapping` | NFRs, quality attributes |
| 8 | `02-requirements-engineering/waterfall/08-semantic-auditing` | V&V audit, traceability matrix |

**Prompt pattern:**

```
Run skill: 02-requirements-engineering/waterfall/01-initialize-srs
```

Then proceed to 02, 03, etc. `02-requirements-engineering/waterfall/09-use-case-modeling`
adds actor-goal use cases when the engagement needs them.

### Agile Track

```
Run skill: 02-requirements-engineering/agile/01-user-story-generation
```

Generates INVEST-compliant user stories with acceptance criteria.

## Step 7: Domain Skills (As Needed)

These skills live in sibling engines, not in this repository. Your agent resolves each engine through its engine-routing table; ask for a skill by name:

| Domain | Skill | Engine | When to Use |
|--------|-------|--------|-------------|
| Database | `mysql-engineering` (absorbs the retired `mysql-best-practices`) | `chwezi-dev-engine` | **Mandatory** for any MySQL work |
| Security | `vibe-security-skill` | `chwezi-dev-engine` | **Mandatory** for web applications |
| Multi-tenant | `multi-tenant-saas-architecture` | `chwezi-dev-engine` | SaaS with tenant isolation |
| UI/UX | `webapp-gui-design` | `chwezi-design-engine` | Web application interfaces |
| POS | `pos-and-retail-operations` | `chwezi-design-engine` | Point-of-sale interfaces (replaces the inactive `pos-sales-ui-design` alias) |
| POS and finance screens | `finance-ui-pattern-library` | `chwezi-accounting-doctrine` | Cash-drawer, receipt and ledger screens |
| Healthcare | `healthcare-ui-design` | `chwezi-design-engine` | Clinical/medical applications |
| Mobile | `android-development` | `chwezi-dev-engine` | Android app documentation |
| Mapping | `gis-platform-engineering` (absorbs the retired `gis-mapping`) | `chwezi-dev-engine` | Location-based features |
| Accounting | `saas-accounting-system` | `chwezi-dev-engine` | Financial/bookkeeping modules |

Earlier local folder names, once: `chwezi-dev-engine` was `skills-web-dev` and `chwezi-design-engine` was `design-system-skills`.

## Updating the SRS Engine Checkout

To pull the latest version of the documentation engine when working directly in this repository:

```bash
cd chwezi-sdlc-documentation
git pull origin main
```

## Troubleshooting

### Skills directory is missing after clone

```bash
git status
git pull origin main
```

### Permission denied on script (Linux/macOS)

The repository does not track the executable bit on any script. Run it through
`bash` (`bash scripts/setup-srs-project.sh ...`), or set the bit yourself with
`chmod +x scripts/setup-srs-project.sh`.

### PowerShell script blocked (Windows)

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Line ending issues (Windows)

```bash
git config --global core.autocrlf true
```
