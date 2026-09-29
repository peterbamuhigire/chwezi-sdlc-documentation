#!/usr/bin/env python3
"""Post-build guard: fail when Mermaid source survives or a figure is missing in a .docx.

A delivered Word document must carry rendered figures, never diagram code.
This guard opens each .docx and runs three checks:

1. Mermaid source. ``word/document.xml`` is searched for Mermaid diagram
   headers in the visible text. Any match is a build failure.
2. Missing figure. When a render manifest lists figures for the document
   (``<doc-dir>/_figures/render-manifest.json``, key = the .docx stem, or a
   ``<stem>.figures.json`` beside the .docx), every listed PNG must be
   embedded in ``word/media/`` byte for byte (SHA-256). A figure Pandoc
   could not fetch is otherwise replaced by its description and the build
   looks clean (M10-13 finding).
3. Figure placeholder. A figure caption paragraph (``ImageCaption``) whose
   figure paragraph holds no image means Pandoc substituted text for the
   picture. This check needs no manifest.

The build-guard idea is adapted from tt-a1i/archify (MIT,
https://github.com/tt-a1i/archify, commit
0e4949f910a8e390bd3b4933883a4dcabad571be), paraphrased; no Archify code is
copied.

Usage:
    python -X utf8 scripts/check_docx_diagrams.py <file.docx> [<file.docx> ...]
        [--render-manifest <doc-dir>/_figures/render-manifest.json]
    python -X utf8 scripts/check_docx_diagrams.py --scan projects \
        --exclude _kaizen,render-runs [--json report.json]

Without ``--render-manifest`` the manifest is discovered: ``<stem>.figures.json``
beside the .docx, then ``render-manifest.json`` files in ``_figures/`` folders
at or below the .docx folder (and, in ``--scan``, anywhere in the same
top-level project folder) whose documents include the .docx stem. A .docx
passes the figure check when at least one discovered manifest is fully
embedded.

Exit codes: 0 clean, 1 Mermaid source found or a figure missing, 2 usage or
read error.
"""
from __future__ import annotations

import argparse
import hashlib
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
_PARA_RE = re.compile(r"<w:p(?:\s[^>]*)?>.*?</w:p>", re.DOTALL)
_STYLE_RE = re.compile(r'<w:pStyle\s+w:val="([^"]+)"')
_IMAGE_RE = re.compile(r"<w:drawing\b|<w:pict\b|<w:object\b")
CAPTION_STYLES = {"ImageCaption"}
RENDER_MANIFEST = "render-manifest.json"
FIGURES_DIR = "_figures"


def _visible(xml: str) -> str:
    xml = _PARA_END_RE.sub("\n", xml)
    xml = xml.replace("<w:br/>", "\n").replace("<w:tab/>", " ")
    return _TAG_RE.sub("", xml)


def read_docx(path: Path) -> tuple[str, dict[str, str]]:
    """Return (word/document.xml, {media name: SHA-256})."""
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml").decode("utf-8", errors="replace")
        media = {n: hashlib.sha256(zf.read(n)).hexdigest()
                 for n in zf.namelist() if n.startswith("word/media/")}
    return xml, media


def docx_text(path: Path) -> tuple[str, int]:
    """Return (visible text of word/document.xml, count of word/media entries)."""
    xml, media = read_docx(path)
    return _visible(xml), len(media)


def figure_placeholders(xml: str) -> list[str]:
    """Captions of figures whose picture paragraph holds no image."""
    found: list[str] = []
    paras = _PARA_RE.findall(xml)
    for i, para in enumerate(paras):
        style = _STYLE_RE.search(para)
        if not style or style.group(1) not in CAPTION_STYLES:
            continue
        if i == 0 or not _IMAGE_RE.search(paras[i - 1]):
            found.append(_visible(para).strip())
    return found


# -- manifest discovery -------------------------------------------------------

def manifest_figures(path: Path, name: str) -> list[dict] | None:
    """Figures a manifest lists for document ``name``; None when not listed.

    Accepts a render manifest (``srs-render-manifest/1``: documents keyed by
    name, figures with ``png`` and ``png_sha256``) or a figures manifest
    (``srs-figures-manifest/1``: figures with ``png_path`` and ``png_sha256``).
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    if isinstance(data.get("documents"), dict):
        doc = data["documents"].get(name)
        figs = doc.get("figures") if isinstance(doc, dict) else None
    elif data.get("artifact_id") == name:
        figs = data.get("figures")
    else:
        return None
    if not isinstance(figs, list):
        return None
    out = []
    for f in figs:
        if isinstance(f, dict):
            out.append({"figure": f.get("figure", f.get("figure_number")),
                        "png": f.get("png") or f.get("png_path"),
                        "png_sha256": f.get("png_sha256")})
    return out


def discover_manifests(docx: Path, project_root: Path | None = None) -> list[Path]:
    """Candidate manifests for ``docx`` (see module docstring)."""
    found: list[Path] = []
    side = docx.with_name(docx.stem + ".figures.json")
    if side.is_file():
        found.append(side)
    roots = [docx.parent]
    if project_root is not None and project_root != docx.parent:
        roots.append(project_root)
    for root in roots:
        for m in _render_manifests_under(root):
            if m not in found:
                found.append(m)
    return found


_MANIFEST_CACHE: dict[Path, list[Path]] = {}


def _render_manifests_under(root: Path) -> list[Path]:
    if root not in _MANIFEST_CACHE:
        _MANIFEST_CACHE[root] = sorted(root.rglob(f"{FIGURES_DIR}/{RENDER_MANIFEST}"))
    return _MANIFEST_CACHE[root]


def missing_figures(media: dict[str, str], figs: list[dict]) -> list[dict]:
    """Figures from one manifest that are not embedded in word/media/."""
    embedded = set(media.values())
    missing = []
    for f in figs:
        sha = f.get("png_sha256")
        if not sha or sha not in embedded:
            missing.append(f)
    if not any(f.get("png_sha256") for f in figs) and len(media) >= len(figs):
        return []  # manifest without hashes: fall back to a count check
    return missing


def figure_check(docx: Path, media: dict[str, str], manifests: list[Path]) -> dict:
    """Pass when one manifest listing this document is fully embedded."""
    listed = []
    for m in manifests:
        figs = manifest_figures(m, docx.stem)
        if figs:
            listed.append((m, figs, missing_figures(media, figs)))
    if not listed:
        return {"manifest": None, "expected": 0, "missing": []}
    for m, figs, miss in listed:
        if not miss:
            return {"manifest": str(m), "expected": len(figs), "missing": []}
    m, figs, miss = min(listed, key=lambda t: len(t[2]))
    return {"manifest": str(m), "expected": len(figs),
            "missing": [{"figure": f["figure"], "png": f["png"]} for f in miss]}


def inspect(path: Path, manifests: list[Path] | None = None) -> dict:
    xml, media = read_docx(path)
    text = _visible(xml)
    hits = [m.group(1).split()[0] for m in MERMAID_HEADER_RE.finditer(text)]
    figs = figure_check(path, media, manifests or [])
    return {"path": str(path), "headers": hits, "media": len(media),
            "placeholders": figure_placeholders(xml), **{
                "manifest": figs["manifest"], "expected_figures": figs["expected"],
                "missing_figures": figs["missing"]}}


def iter_docx(root: Path, excludes: Iterable[str]) -> Iterable[Path]:
    ex = {e for e in excludes if e}
    for p in sorted(root.rglob("*.docx")):
        if p.name.startswith("~$"):
            continue
        parts = set(p.relative_to(root).parts)
        if parts & ex or any(part.startswith(".trash-") for part in parts):
            continue
        yield p


def _project_root(path: Path, scan_root: Path) -> Path:
    rel = path.relative_to(scan_root)
    return scan_root / rel.parts[0] if len(rel.parts) > 1 else scan_root


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--scan", type=Path, help="scan every .docx under this root")
    ap.add_argument("--exclude", default="",
                    help="comma-separated directory names to skip in --scan")
    ap.add_argument("--render-manifest", type=Path, action="append", default=[],
                    help="render manifest listing the figures the .docx must embed "
                         "(repeatable; replaces discovery for the named files)")
    ap.add_argument("--json", type=Path, help="write the full report as JSON")
    args = ap.parse_args(argv)

    if not args.files and not args.scan:
        ap.print_usage(sys.stderr)
        return 2
    targets: list[tuple[Path, Path | None]] = [(f, None) for f in args.files]
    if args.scan:
        if not args.scan.is_dir():
            print(f"ERROR: scan root not found: {args.scan}", file=sys.stderr)
            return 2
        targets.extend((p, _project_root(p, args.scan))
                       for p in iter_docx(args.scan, args.exclude.split(",")))

    report, errors = [], 0
    for path, project in targets:
        if args.render_manifest and project is None:
            manifests = list(args.render_manifest)
        else:
            manifests = discover_manifests(path, project)
        try:
            report.append(inspect(path, manifests))
        except (OSError, KeyError, zipfile.BadZipFile) as exc:
            print(f"ERROR: cannot read {path}: {exc}", file=sys.stderr)
            errors += 1
    dirty = [r for r in report if r["headers"]]
    for r in dirty:
        print(f"MERMAID-SOURCE {r['path']} headers={len(r['headers'])} "
              f"media={r['media']} ({', '.join(sorted(set(r['headers'])))})")
    missing = [r for r in report if r["missing_figures"] or r["placeholders"]]
    for r in missing:
        for f in r["missing_figures"]:
            print(f"MISSING-FIGURE {r['path']} figure={f['figure']} png={f['png']} "
                  f"(manifest {r['manifest']}; media={r['media']})")
        for cap in r["placeholders"]:
            print(f"FIGURE-PLACEHOLDER {r['path']} caption={cap!r} (no image above the caption)")
    checked = sum(1 for r in report if r["manifest"])
    print(f"Scanned {len(report)} .docx file(s); {len(dirty)} contain Mermaid source.")
    print(f"Figure check: {checked} .docx file(s) matched a render manifest; "
          f"{len(missing)} missing rendered figures.")
    if args.json:
        args.json.write_text(json.dumps(
            {"scanned": len(report), "dirty": dirty, "manifest_checked": checked,
             "missing": missing}, indent=2), encoding="utf-8")
    if dirty or missing:
        return 1
    return 2 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
