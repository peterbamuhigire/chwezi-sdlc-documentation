#!/usr/bin/env bash
# =============================================================================
# SDLC-Docs-Engine: New SRS Project Setup (Linux/macOS/WSL)
# =============================================================================
# Usage:
#   chmod +x setup-srs-project.sh
#   ./setup-srs-project.sh <github-repo-url> [target-directory]
#
# Examples:
#   ./setup-srs-project.sh https://github.com/user/my-project.git
#   ./setup-srs-project.sh https://github.com/user/my-project.git ~/projects/my-project
#   ./setup-srs-project.sh git@github.com:user/my-project.git /opt/projects/my-project
# =============================================================================

set -euo pipefail

# --- Configuration ---
SRS_SKILLS_REPO="https://github.com/peterbamuhigire/chwezi-sdlc-documentation.git"
SUBMODULE_NAME="skills"

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_step() { echo -e "${CYAN}[STEP]${NC} $1"; }
print_ok()   { echo -e "${GREEN}[OK]${NC}   $1"; }
print_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_err()  { echo -e "${RED}[ERR]${NC}  $1"; }

# --- Preflight Checks ---
check_prerequisites() {
    print_step "Checking prerequisites..."

    if ! command -v git &>/dev/null; then
        print_err "git is not installed. Install it first:"
        echo "  Ubuntu/Debian: sudo apt install git"
        echo "  macOS:         brew install git"
        exit 1
    fi
    print_ok "git $(git --version | cut -d' ' -f3)"

    if ! command -v gh &>/dev/null; then
        print_warn "GitHub CLI (gh) not found. Optional but recommended."
        echo "  Install: https://cli.github.com/"
    else
        print_ok "gh $(gh --version | head -1 | cut -d' ' -f3)"
    fi
}

# --- Argument Parsing ---
if [ $# -lt 1 ]; then
    print_err "Missing repository URL."
    echo ""
    echo "Usage: $0 <github-repo-url> [target-directory]"
    echo ""
    echo "Examples:"
    echo "  $0 https://github.com/user/my-project.git"
    echo "  $0 https://github.com/user/my-project.git ~/projects/my-project"
    exit 1
fi

REPO_URL="$1"

# Extract repo name from URL for default directory
REPO_NAME=$(basename "$REPO_URL" .git)

if [ $# -ge 2 ]; then
    TARGET_DIR="$2"
else
    read -rp "Target directory [./$REPO_NAME]: " TARGET_DIR
    TARGET_DIR="${TARGET_DIR:-./$REPO_NAME}"
fi

# Expand ~ to $HOME
TARGET_DIR="${TARGET_DIR/#\~/$HOME}"

# --- Main Script ---
echo ""
echo "============================================="
echo " SDLC-Docs-Engine: Project Setup"
echo "============================================="
echo " Repo:      $REPO_URL"
echo " Target:    $TARGET_DIR"
echo " Skills:    $SRS_SKILLS_REPO"
echo "============================================="
echo ""

check_prerequisites

# Step 1: Clone the project repository
print_step "Cloning project repository..."
if [ -d "$TARGET_DIR" ]; then
    print_err "Directory already exists: $TARGET_DIR"
    read -rp "Remove and re-clone? (y/N): " CONFIRM
    if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
        rm -rf "$TARGET_DIR"
    else
        print_err "Aborted."
        exit 1
    fi
fi

git clone "$REPO_URL" "$TARGET_DIR"
print_ok "Cloned to $TARGET_DIR"

# Step 2: Enter project directory
cd "$TARGET_DIR"
print_ok "Working directory: $(pwd)"

# Step 3: Add chwezi-sdlc-documentation as a submodule
print_step "Adding chwezi-sdlc-documentation as submodule '$SUBMODULE_NAME'..."
if [ -d "$SUBMODULE_NAME" ]; then
    print_warn "Directory '$SUBMODULE_NAME' already exists. Skipping submodule add."
else
    git submodule add "$SRS_SKILLS_REPO" "$SUBMODULE_NAME"
    print_ok "Submodule added: $SUBMODULE_NAME"
fi

# Step 4: Initialize and update submodules (including nested)
print_step "Initializing submodules..."
git submodule update --init --recursive
print_ok "Submodules initialized"

# Step 5: Create project_context directory with starter templates
print_step "Creating project_context directory..."
mkdir -p project_context

if [ ! -f "project_context/vision.md" ]; then
    cat > "project_context/vision.md" << 'VISION_EOF'
# Project Vision

## Project Name
<!-- Replace with your project name -->

## Problem Statement
<!-- What problem does this project solve? -->

## Target Users
<!-- Who are the primary users? -->

## Business Goals
1. <!-- Goal 1 -->
2. <!-- Goal 2 -->
3. <!-- Goal 3 -->

## Success Metrics
<!-- How will success be measured? -->

## Constraints
<!-- Budget, timeline, technology, regulatory -->
VISION_EOF
    print_ok "Created project_context/vision.md"
fi

if [ ! -f "project_context/stakeholders.md" ]; then
    cat > "project_context/stakeholders.md" << 'STAKE_EOF'
# Stakeholders

## Primary Stakeholders
| Role | Name | Responsibilities |
|------|------|-----------------|
| Project Sponsor | <!-- --> | <!-- --> |
| Product Owner | <!-- --> | <!-- --> |
| Lead Developer | <!-- --> | <!-- --> |

## Secondary Stakeholders
| Role | Name | Responsibilities |
|------|------|-----------------|
| End Users | <!-- --> | <!-- --> |
| QA Team | <!-- --> | <!-- --> |
STAKE_EOF
    print_ok "Created project_context/stakeholders.md"
fi

if [ ! -f "project_context/glossary.md" ]; then
    cat > "project_context/glossary.md" << 'GLOSS_EOF'
# Glossary (IEEE Std 610.12-1990)

| Term | Definition | Source |
|------|-----------|--------|
| <!-- --> | <!-- --> | <!-- --> |
GLOSS_EOF
    print_ok "Created project_context/glossary.md"
fi

# Step 6: Create output directory
print_step "Creating output directory..."
mkdir -p output
if [ ! -f "output/.gitkeep" ]; then
    touch output/.gitkeep
    print_ok "Created output directory with .gitkeep"
fi

print_step "Creating DOCX export contract..."
mkdir -p export
if [ ! -f "export/.gitkeep" ]; then
    touch export/.gitkeep
fi
if [ ! -f "export-docs.sh" ]; then
    cat > "export-docs.sh" << 'EXPORT_SH_EOF'
#!/usr/bin/env bash
# export-docs.sh -- Copy all .docx deliverables into export/
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXPORT_DIR="$SCRIPT_DIR/export"
mkdir -p "$EXPORT_DIR"
echo "Project   : $(basename "$SCRIPT_DIR")"
echo "Exporting : $EXPORT_DIR"
echo ""
count=0
while IFS= read -r -d '' f; do
    dest="$EXPORT_DIR/$(basename "$f")"
    if [ -f "$dest" ]; then
        echo "  OVERWRITE: $(basename "$f")"
    else
        echo "  COPY:      $(basename "$f")"
    fi
    cp "$f" "$dest"
    ((count++)) || true
done < <(find "$SCRIPT_DIR" -name "*.docx" -not -path "*/export/*" -print0)
echo ""
echo "Exported $count file(s) to $EXPORT_DIR"
EXPORT_SH_EOF
    chmod +x export-docs.sh
fi
if [ ! -f "export-docs.ps1" ]; then
    cat > "export-docs.ps1" << 'EXPORT_PS1_EOF'
# export-docs.ps1 -- Copy all .docx deliverables into export/
$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$ExportDir  = Join-Path $ScriptDir 'export'
New-Item -ItemType Directory -Force -Path $ExportDir | Out-Null
Write-Host "Project   : $(Split-Path -Leaf $ScriptDir)"
Write-Host "Exporting : $ExportDir"
Write-Host ""
$docxFiles = Get-ChildItem -Path $ScriptDir -Recurse -Filter '*.docx' |
             Where-Object { $_.FullName -notlike "*\export\*" }
$count = 0
foreach ($f in $docxFiles) {
    $dest = Join-Path $ExportDir $f.Name
    if (Test-Path $dest) { Write-Host "  OVERWRITE: $($f.Name)" }
    else                 { Write-Host "  COPY:      $($f.Name)" }
    Copy-Item -Path $f.FullName -Destination $dest -Force
    $count++
}
Write-Host ""
Write-Host "Exported $count file(s) to $ExportDir"
EXPORT_PS1_EOF
fi
print_ok "Created export/, export-docs.sh, and export-docs.ps1"

# Step 7: Create/update .gitignore
print_step "Updating .gitignore..."
GITIGNORE_ENTRIES=(
    "# Environment"
    ".env"
    ".env.local"
    "# IDE"
    ".idea/"
    ".vscode/"
    "*.swp"
    "*.swo"
    "# OS"
    ".DS_Store"
    "Thumbs.db"
    "# Python"
    "__pycache__/"
    "*.pyc"
    ".venv/"
    "venv/"
)

if [ ! -f ".gitignore" ]; then
    printf '%s\n' "${GITIGNORE_ENTRIES[@]}" > .gitignore
    print_ok "Created .gitignore"
else
    print_ok ".gitignore already exists (not modified)"
fi

# Step 8: Initial commit
print_step "Creating initial commit..."
git add .
if git diff --cached --quiet; then
    print_warn "No changes to commit."
else
    git commit -m "Initialize SRS project with SDLC-Docs-Engine submodule

- Added chwezi-sdlc-documentation as 'skills' submodule
- Created project_context/ with starter templates (vision, stakeholders, glossary)
- Created output/ directory for generated documentation
- Created export/ plus export-docs scripts for DOCX delivery copies
- Updated .gitignore"
    print_ok "Initial commit created"
fi

# Step 9: Push to remote
read -rp "Push to remote origin? (Y/n): " PUSH_CONFIRM
if [[ ! "$PUSH_CONFIRM" =~ ^[Nn]$ ]]; then
    git push origin "$(git branch --show-current)"
    print_ok "Pushed to origin"
else
    print_warn "Skipped push. Run 'git push' when ready."
fi

# --- Summary ---
echo ""
echo "============================================="
echo -e " ${GREEN}Setup Complete!${NC}"
echo "============================================="
echo ""
echo " Project:         $TARGET_DIR"
echo " Skills submodule: $TARGET_DIR/$SUBMODULE_NAME"
echo " Project context:  $TARGET_DIR/project_context/"
echo " Output:           $TARGET_DIR/output/"
echo " DOCX export:      $TARGET_DIR/export/"
echo ""
echo " Next Steps:"
echo " 1. Edit project_context/vision.md with your project details"
echo " 2. Open Claude Code in this directory:"
echo "    cd $TARGET_DIR && claude"
echo " 3. Run the shared-understanding step:"
echo "    Paste the kick-off prompt (see SETUP_GUIDE.md)"
echo " 4. Then run meta-initialization:"
echo "    'Run skill: 00-meta-initialization'"
echo ""
echo "============================================="
