"""Figure manifest beside each built ``.docx`` (M10-07-T10, AR-14).

``build-doc.sh`` calls ``python -m engine diagrams manifest`` after the M10-01
render step, Pandoc and the ``.docx`` guard. It writes
``<OutputName>.figures.json`` next to the ``.docx``: for every figure, the
IR path and SHA-256 (and the hash accepted by the last ``diagrams validate``),
the Mermaid SHA-256, the PNG and SVG SHA-256, renderer name and version, font
family, font-substitution result and ``state``; plus an ``artifact_sha256``
map (path -> SHA-256) following the P18 ``render-review-manifest.json``
naming. ``python -m engine diagrams verify-manifest <doc-dir>`` re-hashes every
recorded file and names each figure whose source or output changed after the
build.

Candidate freezing and receipt pattern adapted from Archify (MIT,
https://github.com/tt-a1i/archify, commit
0e4949f910a8e390bd3b4933883a4dcabad571be). Paraphrased; no schema, code or
test text copied.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
from pathlib import Path
from typing import List, Optional, Tuple

from engine.diagram_ir import GENERATED_DIR, read_generated, read_validated, text_sha256
from engine.figures import FIGURES_DIR, MANIFEST_NAME

SUFFIX = ".figures.json"
STATE = "local-review-export"


_TEXT_SUFFIXES = (".json", ".mmd", ".md")


def _sha(path: Path) -> Optional[str]:
    """SHA-256; text sources are hashed with CRLF normalised (as validate does)."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if path.name.endswith(_TEXT_SUFFIXES):
        return text_sha256(data)
    return hashlib.sha256(data).hexdigest()


def _rel(path: Path, base: Path) -> str:
    try:
        return Path(os.path.relpath(path, base)).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _render_entry(doc_dir: Path, name: str) -> Tuple[Optional[dict], Path]:
    figures_dir = doc_dir / FIGURES_DIR
    try:
        data = json.loads((figures_dir / MANIFEST_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None, figures_dir
    entry = (data.get("documents") or {}).get(name)
    return (entry if isinstance(entry, dict) else None), figures_dir


def build_manifest(doc_dir: Path, name: str, docx: Path) -> Optional[dict]:
    """The figures manifest for one build, or None when nothing was rendered."""
    doc_dir, docx = Path(doc_dir).resolve(), Path(docx).resolve()
    entry, figures_dir = _render_entry(doc_dir, name)
    if entry is None:
        return None
    base = docx.parent
    validated = read_validated(doc_dir)
    generated = read_generated(doc_dir)
    renderer = entry.get("renderer", {})
    packages = renderer.get("packages", {})
    font = entry.get("font", {})
    probe = font.get("headless_chrome_probe") or {}
    font_check = "PASS" if probe.get("resolved") is True else "NOT_ASSESSED"
    shas: dict = {}
    if docx.is_file():
        shas[_rel(docx, base)] = _sha(docx)
    figures: List[dict] = []
    for fig in entry.get("figures", []):
        fid = fig.get("ir_figure_id") or f"fig-{fig.get('figure')}"
        png, svg = figures_dir / fig.get("png", ""), figures_dir / fig.get("svg", "")
        rec = {
            "figure_id": fid,
            "figure_number": fig.get("figure"),
            "ir_path": None, "ir_sha256": None, "validated_ir_sha256": None,
            "mermaid_sha256": fig.get("mermaid_sha256"),
            "png_path": _rel(png, base), "png_sha256": fig.get("png_sha256"),
            "svg_path": _rel(svg, base), "svg_sha256": fig.get("svg_sha256"),
            "renderer": "@mermaid-js/mermaid-cli",
            "renderer_version": packages.get("@mermaid-js/mermaid-cli"),
            "font_family": font.get("family"),
            "font_substitution_check": font_check,
            "state": STATE,
        }
        if fig.get("ir_figure_id"):
            ir_path = doc_dir / fig.get("ir_path", "")
            rec["ir_path"] = _rel(ir_path, base)
            rec["ir_sha256"] = fig.get("ir_sha256")
            rec["validated_ir_sha256"] = validated.get(fid, {}).get("ir_sha256")
            shas[rec["ir_path"]] = fig.get("ir_sha256")
            gen = generated.get(fid, {})
            if gen.get("mermaid"):
                shas[_rel(doc_dir / GENERATED_DIR / gen["mermaid"], base)] = gen.get("mermaid_sha256")
        shas[rec["png_path"]] = rec["png_sha256"]
        shas[rec["svg_path"]] = rec["svg_sha256"]
        figures.append(rec)
    return {
        "schema": "srs-figures-manifest/1",
        "attribution": ("Candidate-freezing pattern adapted from Archify (MIT, "
                        "https://github.com/tt-a1i/archify, commit "
                        "0e4949f910a8e390bd3b4933883a4dcabad571be)"),
        "artifact_id": name,
        "built_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "doc_dir": _rel(doc_dir, base),
        "docx": _rel(docx, base),
        "browser": renderer.get("browser"),
        "renderer_packages": packages,
        "font": {k: font.get(k) for k in ("family", "fallback", "file", "file_sha256")},
        "figures": figures,
        "artifact_sha256": dict(sorted(shas.items())),
    }


def write_manifest(doc_dir: Path, name: str, docx: Path) -> Optional[Path]:
    data = build_manifest(doc_dir, name, docx)
    if data is None:
        return None
    out = Path(docx).resolve().parent / f"{name}{SUFFIX}"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def find_manifests(target: Path) -> List[Path]:
    """Manifests for a document directory (or the manifest file itself)."""
    target = Path(target).resolve()
    if target.is_file() and target.name.endswith(SUFFIX):
        return [target]
    out = []
    for cand in sorted(target.parent.glob(f"*{SUFFIX}")):
        try:
            data = json.loads(cand.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if (cand.parent / str(data.get("doc_dir", ""))).resolve() == target:
            out.append(cand)
    return out


def verify(manifest: Path) -> List[str]:
    """Problems found re-hashing one manifest's files (empty list = clean)."""
    data = json.loads(Path(manifest).read_text(encoding="utf-8"))
    base = Path(manifest).parent
    problems: List[str] = []
    owners: dict = {}
    for fig in data.get("figures", []):
        for key in ("ir_path", "png_path", "svg_path"):
            if fig.get(key):
                owners[fig[key]] = fig["figure_id"]
        if fig.get("ir_path") and fig.get("validated_ir_sha256") != fig.get("ir_sha256"):
            problems.append(f"{fig['figure_id']}: built from an IR that was not the validated "
                            "candidate (diagram/candidate-not-validated)")
    for rel, expected in sorted((data.get("artifact_sha256") or {}).items()):
        actual = _sha(base / rel)
        if actual != expected:
            who = owners.get(rel)
            if who is None and rel.endswith(".mmd"):
                who = Path(rel).stem
            state = "missing" if actual is None else "changed since the build"
            problems.append(f"{who or data.get('artifact_id')}: {rel} {state}")
    return problems
