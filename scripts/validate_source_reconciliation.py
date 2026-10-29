#!/usr/bin/env python3
"""Validate a project's source-to-requirement and ambiguity register."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.artifact_graph import ArtifactGraph
from engine.checks.source_reconciliation import SourceReconciliationCheck
from engine.workspace import Workspace, WorkspaceNotFoundError


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="project workspace containing _context/")
    args = parser.parse_args()
    try:
        workspace = Workspace.load(args.project)
    except WorkspaceNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    register = workspace.root / "_registry" / "source-reconciliation.yaml"
    if not register.is_file():
        print(f"ERROR: required source reconciliation register is missing: {register}", file=sys.stderr)
        return 1
    findings = SourceReconciliationCheck().run(ArtifactGraph.build(workspace))
    for finding in findings:
        where = f"{finding.location}:{finding.line}" if finding.line else str(finding.location)
        print(f"{finding.code} {where}: {finding.message}")
    print(f"Source reconciliation: {'PASS' if not findings else 'FAIL'} ({len(findings)} finding(s))")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
