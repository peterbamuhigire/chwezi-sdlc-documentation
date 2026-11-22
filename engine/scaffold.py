"""engine new-project scaffolding."""
from __future__ import annotations
import shutil
from pathlib import Path
from typing import Optional


EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "templates" / "project-examples"

EXPORT_DOCS_SH = """#!/usr/bin/env bash
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
done < <(find "$SCRIPT_DIR" -name "*.docx" -not -path "*/export/*" -not -path "*/references/*" -print0)
echo ""
echo "Exported $count file(s) to $EXPORT_DIR"
"""

EXPORT_DOCS_PS1 = """# export-docs.ps1 -- Copy all .docx deliverables into export/
$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$ExportDir  = Join-Path $ScriptDir 'export'
New-Item -ItemType Directory -Force -Path $ExportDir | Out-Null
Write-Host "Project   : $(Split-Path -Leaf $ScriptDir)"
Write-Host "Exporting : $ExportDir"
Write-Host ""
$docxFiles = Get-ChildItem -Path $ScriptDir -Recurse -Filter '*.docx' |
             Where-Object { $_.FullName -notlike "*\\export\\*" -and $_.FullName -notlike "*\\references\\*" }
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
"""


def _ensure_export_contract(project_root: Path) -> None:
    """Create the standard per-project DOCX export folder and scripts."""
    export_dir = project_root / "export"
    export_dir.mkdir(exist_ok=True)
    gitkeep = export_dir / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")

    sh_path = project_root / "export-docs.sh"
    if not sh_path.exists():
        sh_path.write_text(EXPORT_DOCS_SH, encoding="utf-8", newline="\n")
        sh_path.chmod(0o755)

    ps1_path = project_root / "export-docs.ps1"
    if not ps1_path.exists():
        ps1_path.write_text(EXPORT_DOCS_PS1, encoding="utf-8", newline="\n")


def scaffold(project_root: Path, methodology: str, domain: str, example: Optional[str]) -> None:
    """Create project_root, optionally seeded from an example.

    Post-processes _context/methodology.md to set `methodology: <methodology>`.
    """
    project_root = Path(project_root).resolve()
    if project_root.exists():
        raise FileExistsError(f"{project_root} already exists")
    project_root.mkdir(parents=True)
    if example:
        src = EXAMPLES_DIR / example
        if not src.is_dir():
            raise FileNotFoundError(f"Example '{example}' not found in {EXAMPLES_DIR}")
        for item in src.iterdir():
            if item.name == "README.md":
                continue  # don't copy the example readme
            if item.is_dir():
                shutil.copytree(item, project_root / item.name)
            else:
                shutil.copy2(item, project_root / item.name)
    else:
        (project_root / "_context").mkdir()
        (project_root / "_context" / "vision.md").write_text("# Vision\n", encoding="utf-8")
        (project_root / "_context" / "stakeholders.md").write_text("# Stakeholders\n", encoding="utf-8")
        (project_root / "_context" / "features.md").write_text("# Features\n", encoding="utf-8")
        (project_root / "_context" / "glossary.md").write_text("# Glossary\n", encoding="utf-8")
    # Always (re)write methodology.md with the chosen methodology
    methodology_path = project_root / "_context" / "methodology.md"
    methodology_path.parent.mkdir(exist_ok=True)
    methodology_path.write_text(
        f"---\nmethodology: {methodology}\ndomain: {domain}\nproduct_market_strategy: required\n---\n# Methodology\n",
        encoding="utf-8",
    )
    # Seed _registry/ if not present; for hybrid, seed baseline-trace.yaml; for all, seed controls.yaml.
    reg = project_root / "_registry"
    reg.mkdir(exist_ok=True)
    controls_path = reg / "controls.yaml"
    if not controls_path.exists():
        controls_path.write_text(
            "# Populate from domains/{}/controls/control-register.yaml\nselected: []\n".format(domain),
            encoding="utf-8",
        )
    if methodology == "hybrid":
        bt = reg / "baseline-trace.yaml"
        if not bt.exists():
            bt.write_text("baseline: []\nstories: []\n", encoding="utf-8")
    # Domain.md for ControlsCheck
    domain_path = project_root / "_context" / "domain.md"
    if not domain_path.exists():
        domain_path.write_text(f"# Domain\ndomain: {domain}\n", encoding="utf-8")

    # Examples can already own an equivalent strategy at a different location.
    from engine.artifact_graph import ArtifactGraph
    from engine.workspace import Workspace

    graph = ArtifactGraph.build(Workspace.load(project_root))
    if not any(a.document == "product-market-strategy" for a in graph.artifacts):
        strategy_dir = project_root / "01-strategic-vision"
        strategy_dir.mkdir(exist_ok=True)
        target = strategy_dir / "digital-marketing-social-media-and-website-strategy.md"
        if not target.exists():
            shutil.copyfile(Path(__file__).parent / "templates" / "product-market-strategy.md", target)
    _ensure_export_contract(project_root)
