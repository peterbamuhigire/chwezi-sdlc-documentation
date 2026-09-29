# SDLC-Docs-Engine: New Project Setup Guide

## Prerequisites

| Requirement | Windows | Ubuntu/macOS |
|-------------|---------|--------------|
| Git | [git-scm.com](https://git-scm.com/download/win) | `sudo apt install git` / `brew install git` |
| GitHub CLI (optional) | [cli.github.com](https://cli.github.com/) | `sudo apt install gh` / `brew install gh` |
| Claude Code | [claude.ai/claude-code](https://claude.ai/claude-code) | Same |

## Quick Start (Junior Operator Path)

If you only need to stand up a new project workspace from a shipped
example and validate it, run these five commands:

```bash
git clone https://github.com/peterbamuhigire/chwezi-sdlc-documentation.git
cd chwezi-sdlc-documentation
# Resolve engineering/methodology skills through the Chwezi Dev Engine:
#   https://github.com/peterbamuhigire/chwezi-dev-engine
# Resolve finance/accounting doctrine through the Chwezi Accounting Doctrine:
#   https://github.com/peterbamuhigire/chwezi-accounting-doctrine
pip install -e ".[dev]"
python -m engine doctor
python -m engine new-project Acme --methodology waterfall --domain government --example uganda-public-sector
python -m engine validate projects/Acme
```

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

### Windows (PowerShell)

```powershell
# If script execution is blocked, run this first (one-time):
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Run the setup script:
.\setup-srs-project.ps1 -RepoUrl "https://github.com/user/my-project.git"

# Or specify a target directory:
.\setup-srs-project.ps1 -RepoUrl "https://github.com/user/my-project.git" -TargetDir "C:\projects\my-project"
```

### Ubuntu / macOS / WSL

```bash
# Make executable (one-time):
chmod +x setup-srs-project.sh

# Run the setup script:
./setup-srs-project.sh https://github.com/user/my-project.git

# Or specify a target directory:
./setup-srs-project.sh https://github.com/user/my-project.git ~/projects/my-project
```

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
7. Creates an initial commit and optionally pushes

### Resulting Directory Structure

```
my-project/
├── skills/                    # chwezi-sdlc-documentation engine checkout
│   ├── docs/
│   ├── 02-requirements-engineering/
│   │   ├── waterfall/         # IEEE 830 SRS pipeline (8 phases)
│   │   └── agile/             # INVEST user stories
│   ├── skills/                # skills/<skill-name>/SKILL.md
│   ├── CLAUDE.md
│   ├── README.md
│   └── ...
├── project_context/           # YOUR project data (source of truth)
│   ├── vision.md
│   ├── stakeholders.md
│   └── glossary.md
├── output/                    # Generated SRS documentation
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

### Waterfall Track (IEEE 830 SRS)

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

Then proceed to 02, 03, etc.

### Agile Track

```
Run skill: 02-requirements-engineering/agile/01-user-story-generation
```

Generates INVEST-compliant user stories with acceptance criteria.

## Step 7: Domain Skills (As Needed)

The engine includes reusable skills under `skills/<skill-name>/SKILL.md`. These are invoked automatically when relevant, or you can request them:

| Domain | Skill | When to Use |
|--------|-------|-------------|
| Database | `mysql-best-practices` | **Mandatory** for any database work |
| Security | `vibe-security-skill` | **Mandatory** for web applications |
| Multi-tenant | `multi-tenant-saas-architecture` | SaaS with tenant isolation |
| UI/UX | `webapp-gui-design` | Web application interfaces |
| POS | `pos-sales-ui-design` | Point-of-sale systems |
| Healthcare | `healthcare-ui-design` | Clinical/medical applications |
| Mobile | `android-development` | Android app documentation |
| Mapping | `gis-mapping` | Location-based features |
| Accounting | `saas-accounting-system` | Financial/bookkeeping modules |

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

```bash
chmod +x scripts/setup-srs-project.sh
```

### PowerShell script blocked (Windows)

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Line ending issues (Windows)

```bash
git config --global core.autocrlf true
```
