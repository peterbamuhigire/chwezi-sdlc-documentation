#!/usr/bin/env python3
"""Post-build guard: fail when raw Mermaid source survives inside a .docx.

A delivered Word document must carry rendered figures, never diagram code.
This guard opens each .docx, reads ``word/document.xml`` and searches the
visible text for Mermaid diagram headers. Any match is a build failure.

The build-guard idea is adapted from tt-a1i/archify (MIT,
https://github.com/tt-a1i/archify, commit
0e4949f910a8e390bd3b4933883a4dcabad571be), paraphrased; no Archify code is
copied.

Usage:
    python -X utf8 scripts/check_docx_diagrams.py <file.docx> [<file.docx> ...]
    python -X utf8 scripts/check_docx_diagrams.py --scan projects \
        --exclude _kaizen,render-runs [--json report.json]

Exit codes: 0 clean, 1 Mermaid source found, 2 usage or read error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Iterable

# Diagram headers that only appear in Mermaid source, never in prose.
MERMAID_HEADER_RE = re.compile(
    r"(?<![A-Za-z])("
    r"sequenceDiagram|flowchart\s+(?:TD|TB|BT|LR|RL)|graph\s+(?:TD|TB|BT|LR|RL)|"
    r"erDiagram|C4Context|C4Container|C4Component|C4Deployment|classDiagram|"
    r"stateDiagram(?:-v2)?"
    r")(?![A-Za-z])"
)
_TAG_RE = re.compile(r"<[^>]+>")
_PARA_END_RE = re.compile(r"</w:p>")


def docx_text(path: Path) -> tuple[str, int]:
    """Return (visible text of word/document.xml, count of word/media entries)."""
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml").decode("utf-8", errors="replace")
        media = sum(1 for n in zf.namelist() if n.startswith("word/media/"))
    xml = _PARA_END_RE.sub("\n", xml)
    xml = xml.replace("<w:br/>", "\n").replace("<w:tab/>", " ")
    return _TAG_RE.sub("", xml), media


def inspect(path: Path) -> dict:
    text, media = docx_text(path)
    hits = [m.group(1).split()[0] for m in MERMAID_HEADER_RE.finditer(text)]
    return {"path": str(path), "headers": hits, "media": media}


def iter_docx(root: Path, excludes: Iterable[str]) -> Iterable[Path]:
    ex = {e for e in excludes if e}
    for p in sorted(root.rglob("*.docx")):
        if p.name.startswith("~$"):
            continue
        parts = set(p.relative_to(root).parts)
        if parts & ex or any(part.startswith(".trash-") for part in parts):
            continue
        yield p


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--scan", type=Path, help="scan every .docx under this root")
    ap.add_argument("--exclude", default="",
                    help="comma-separated directory names to skip in --scan")
    ap.add_argument("--json", type=Path, help="write the full report as JSON")
    args = ap.parse_args(argv)

    if not args.files and not args.scan:
        ap.print_usage(sys.stderr)
        return 2
    targets: list[Path] = list(args.files)
    if args.scan:
        if not args.scan.is_dir():
            print(f"ERROR: scan root not found: {args.scan}", file=sys.stderr)
            return 2
        targets.extend(iter_docx(args.scan, args.exclude.split(",")))

    report, errors = [], 0
    for path in targets:
        try:
            report.append(inspect(path))
        except (OSError, KeyError, zipfile.BadZipFile) as exc:
            print(f"ERROR: cannot read {path}: {exc}", file=sys.stderr)
            errors += 1
    dirty = [r for r in report if r["headers"]]
    for r in dirty:
        print(f"MERMAID-SOURCE {r['path']} headers={len(r['headers'])} "
              f"media={r['media']} ({', '.join(sorted(set(r['headers'])))})")
    print(f"Scanned {len(report)} .docx file(s); {len(dirty)} contain Mermaid source.")
    if args.json:
        args.json.write_text(json.dumps(
            {"scanned": len(report), "dirty": dirty}, indent=2), encoding="utf-8")
    if dirty:
        return 1
    return 2 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
