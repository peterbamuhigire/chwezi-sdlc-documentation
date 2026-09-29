# =============================================================================
# SDLC-Docs-Engine: New SRS Project Setup (Windows PowerShell)
# =============================================================================
# Usage:
#   .\setup-srs-project.ps1 -RepoUrl <github-repo-url> [-TargetDir <path>]
#
# Examples:
#   .\setup-srs-project.ps1 -RepoUrl "https://github.com/user/my-project.git"
#   .\setup-srs-project.ps1 -RepoUrl "https://github.com/user/my-project.git" -TargetDir "C:\projects\my-project"
#   .\setup-srs-project.ps1 -RepoUrl "git@github.com:user/my-project.git" -TargetDir "D:\work\my-project"
#
# Note: Run PowerShell as Administrator if you encounter permission issues.
#       If script execution is blocked, run: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
# =============================================================================

param(
    [Parameter(Mandatory = $true, HelpMessage = "GitHub repository URL to clone")]
    [string]$RepoUrl,

    [Parameter(Mandatory = $false, HelpMessage = "Target directory (default: ./<repo-name>)")]
    [string]$TargetDir
)

# --- Configuration ---
$SRS_SKILLS_REPO = "https://github.com/peterbamuhigire/srs-skills.git"
$SUBMODULE_NAME = "skills"

# --- Helper Functions ---
function Write-Step  { param([string]$msg) Write-Host "[STEP] $msg" -ForegroundColor Cyan }
function Write-Ok    { param([string]$msg) Write-Host "[OK]   $msg" -ForegroundColor Green }
function Write-Warn  { param([string]$msg) Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err   { param([string]$msg) Write-Host "[ERR]  $msg" -ForegroundColor Red }

# --- Preflight Checks ---
function Test-Prerequisites {
    Write-Step "Checking prerequisites..."

    try {
        $gitVersion = git --version 2>&1
        Write-Ok "git $($gitVersion -replace 'git version ','')"
    }
    catch {
        Write-Err "git is not installed. Install from: https://git-scm.com/download/win"
        exit 1
    }

    try {
        $ghVersion = gh --version 2>&1 | Select-Object -First 1
        Write-Ok "gh $($ghVersion -replace 'gh version ','' -replace ' .*','')"
    }
    catch {
        Write-Warn "GitHub CLI (gh) not found. Optional but recommended."
        Write-Host "  Install: https://cli.github.com/" -ForegroundColor Gray
    }
}

# --- Extract repo name from URL ---
$RepoName = [System.IO.Path]::GetFileNameWithoutExtension($RepoUrl.TrimEnd('/'))
if ($RepoName.EndsWith('.git')) {
    $RepoName = $RepoName.Substring(0, $RepoName.Length - 4)
}
# Handle URLs like https://github.com/user/repo.git
if ($RepoUrl -match '/([^/]+?)(\.git)?$') {
    $RepoName = $Matches[1]
}

if (-not $TargetDir) {
    $defaultDir = Join-Path (Get-Location) $RepoName
    $TargetDir = Read-Host "Target directory [$defaultDir]"
    if ([string]::IsNullOrWhiteSpace($TargetDir)) {
        $TargetDir = $defaultDir
    }
}

# Resolve to absolute path
$TargetDir = [System.IO.Path]::GetFullPath($TargetDir)

# --- Main Script ---
Write-Host ""
Write-Host "=============================================" -ForegroundColor White
Write-Host " SDLC-Docs-Engine: Project Setup" -ForegroundColor White
Write-Host "=============================================" -ForegroundColor White
Write-Host " Repo:      $RepoUrl"
Write-Host " Target:    $TargetDir"
Write-Host " Skills:    $SRS_SKILLS_REPO"
Write-Host "=============================================" -ForegroundColor White
Write-Host ""

Test-Prerequisites

# Step 1: Clone the project repository
Write-Step "Cloning project repository..."
if (Test-Path $TargetDir) {
    Write-Err "Directory already exists: $TargetDir"
    $confirm = Read-Host "Remove and re-clone? (y/N)"
    if ($confirm -match '^[Yy]$') {
        Remove-Item -Recurse -Force $TargetDir
    }
    else {
        Write-Err "Aborted."
        exit 1
    }
}

git clone $RepoUrl $TargetDir
if ($LASTEXITCODE -ne 0) { Write-Err "Clone failed."; exit 1 }
Write-Ok "Cloned to $TargetDir"

# Step 2: Enter project directory
Set-Location $TargetDir
Write-Ok "Working directory: $(Get-Location)"

# Step 3: Add srs-skills as a submodule
Write-Step "Adding srs-skills as submodule '$SUBMODULE_NAME'..."
if (Test-Path $SUBMODULE_NAME) {
    Write-Warn "Directory '$SUBMODULE_NAME' already exists. Skipping submodule add."
}
else {
    git submodule add $SRS_SKILLS_REPO $SUBMODULE_NAME
    if ($LASTEXITCODE -ne 0) { Write-Err "Submodule add failed."; exit 1 }
    Write-Ok "Submodule added: $SUBMODULE_NAME"
}

# Step 4: Initialize and update submodules (including nested)
Write-Step "Initializing submodules..."
git submodule update --init --recursive
Write-Ok "Submodules initialized"

# Step 5: Create project_context directory with starter templates
Write-Step "Creating project_context directory..."
$contextDir = Join-Path $TargetDir "project_context"
if (-not (Test-Path $contextDir)) {
    New-Item -ItemType Directory -Path $contextDir -Force | Out-Null
}

$visionFile = Join-Path $contextDir "vision.md"
if (-not (Test-Path $visionFile)) {
    @"
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
"@ | Set-Content -Path $visionFile -Encoding UTF8
    Write-Ok "Created project_context/vision.md"
}

$stakeholdersFile = Join-Path $contextDir "stakeholders.md"
if (-not (Test-Path $stakeholdersFile)) {
    @"
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
"@ | Set-Content -Path $stakeholdersFile -Encoding UTF8
    Write-Ok "Created project_context/stakeholders.md"
}

$glossaryFile = Join-Path $contextDir "glossary.md"
if (-not (Test-Path $glossaryFile)) {
    @"
# Glossary (IEEE Std 610.12-1990)

| Term | Definition | Source |
|------|-----------|--------|
| <!-- --> | <!-- --> | <!-- --> |
"@ | Set-Content -Path $glossaryFile -Encoding UTF8
    Write-Ok "Created project_context/glossary.md"
}

# Step 6: Create output directory
Write-Step "Creating output directory..."
$outputDir = Join-Path $TargetDir "output"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}
$gitkeep = Join-Path $outputDir ".gitkeep"
if (-not (Test-Path $gitkeep)) {
    New-Item -ItemType File -Path $gitkeep -Force | Out-Null
    Write-Ok "Created output directory with .gitkeep"
}

Write-Step "Creating DOCX export contract..."
$exportDir = Join-Path $TargetDir "export"
if (-not (Test-Path $exportDir)) {
    New-Item -ItemType Directory -Path $exportDir -Force | Out-Null
}
$exportGitkeep = Join-Path $exportDir ".gitkeep"
if (-not (Test-Path $exportGitkeep)) {
    New-Item -ItemType File -Path $exportGitkeep -Force | Out-Null
}
$exportSh = Join-Path $TargetDir "export-docs.sh"
if (-not (Test-Path $exportSh)) {
    @'
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
'@ | Set-Content -Path $exportSh -Encoding UTF8
}
$exportPs1 = Join-Path $TargetDir "export-docs.ps1"
if (-not (Test-Path $exportPs1)) {
    @'
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
'@ | Set-Content -Path $exportPs1 -Encoding UTF8
}
Write-Ok "Created export/, export-docs.sh, and export-docs.ps1"

# Step 7: Create/update .gitignore
Write-Step "Updating .gitignore..."
$gitignorePath = Join-Path $TargetDir ".gitignore"
if (-not (Test-Path $gitignorePath)) {
    @"
# Environment
.env
.env.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Python
__pycache__/
*.pyc
.venv/
venv/
"@ | Set-Content -Path $gitignorePath -Encoding UTF8
    Write-Ok "Created .gitignore"
}
else {
    Write-Ok ".gitignore already exists (not modified)"
}

# Step 8: Initial commit
Write-Step "Creating initial commit..."
git add .
$hasChanges = git diff --cached --quiet 2>&1; $exitCode = $LASTEXITCODE
if ($exitCode -eq 0) {
    Write-Warn "No changes to commit."
}
else {
    git commit -m @"
Initialize SRS project with SDLC-Docs-Engine submodule

- Added srs-skills as 'skills' submodule
- Created project_context/ with starter templates (vision, stakeholders, glossary)
- Created output/ directory for generated documentation
- Created export/ plus export-docs scripts for DOCX delivery copies
- Updated .gitignore
"@
    Write-Ok "Initial commit created"
}

# Step 9: Push to remote
$pushConfirm = Read-Host "Push to remote origin? (Y/n)"
if ($pushConfirm -notmatch '^[Nn]$') {
    $currentBranch = git branch --show-current
    git push origin $currentBranch
    Write-Ok "Pushed to origin"
}
else {
    Write-Warn "Skipped push. Run 'git push' when ready."
}

# --- Summary ---
Write-Host ""
Write-Host "=============================================" -ForegroundColor White
Write-Host " Setup Complete!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor White
Write-Host ""
Write-Host " Project:          $TargetDir"
Write-Host " Skills submodule: $TargetDir\$SUBMODULE_NAME"
Write-Host " Project context:  $TargetDir\project_context\"
Write-Host " Output:           $TargetDir\output\"
Write-Host " DOCX export:      $TargetDir\export\"
Write-Host ""
Write-Host " Next Steps:" -ForegroundColor Yellow
Write-Host " 1. Edit project_context\vision.md with your project details"
Write-Host " 2. Open Claude Code in this directory:"
Write-Host "    cd $TargetDir; claude" -ForegroundColor Gray
Write-Host " 3. Run the shared-understanding step:"
Write-Host "    Paste the kick-off prompt (see SETUP_GUIDE.md)" -ForegroundColor Gray
Write-Host " 4. Then run meta-initialization:"
Write-Host "    'Run skill: 00-meta-initialization'" -ForegroundColor Gray
Write-Host ""
Write-Host "=============================================" -ForegroundColor White
