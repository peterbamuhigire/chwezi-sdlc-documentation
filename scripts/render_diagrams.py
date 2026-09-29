#!/usr/bin/env python3
"""Render fenced Mermaid blocks to figures before Pandoc builds a .docx.

Stitches the given Markdown files (in order), renders every fenced
``mermaid`` block to a PNG (>= 300 ppi at the printed width) and an SVG under
``<figures-dir>`` using the pinned local renderer in ``scripts/diagram-render``
(``@mermaid-js/mermaid-cli`` driving the machine's Chrome or Edge; no hosted
renderer, no browser download), and replaces each block with a captioned
figure that carries alt text:

    ![Figure N — <caption>](_figures/<doc>-<n>.png){width=6.25in fig-alt="<alt>"}

A section may also embed a figure authored as diagram IR (M10-07) with the
marker ``<!-- diagram-ir: FIG-nnn -->`` and the generated trace table with
``<!-- diagram-ir: trace-table -->``. The marker is expanded from
``<doc-dir>/_generated/`` only when the IR is the candidate accepted by the
last ``python -m engine diagrams validate`` and the generated Mermaid is
current; otherwise the build stops with ``diagram/candidate-not-validated``
(candidate freezing). The IR's ``alt_text`` and ``caption`` become the
figure's alt text and caption, and the manifest records the IR hashes.

Alt text comes from a ``%% alt: ...`` comment in the block, otherwise from
the nearest heading (with a warning). The caption comes from
``%% caption: ...``, otherwise from the alt text. The diagram typeface comes
from one config value (``diagram_font_family`` in
``scripts/diagram-render/render-config.json``), is checked against the design
engine's banned-font list, is injected as a Mermaid ``%%{init}%%`` directive,
and is loaded from a local font file with ``@font-face``; it is never silently
substituted. Every figure is recorded with source and output SHA-256 in
``<figures-dir>/render-manifest.json`` (P18 render-evidence convention).

The render-receipt and build-guard ideas are adapted from tt-a1i/archify
(MIT, https://github.com/tt-a1i/archify, commit
0e4949f910a8e390bd3b4933883a4dcabad571be), paraphrased; no Archify code is
copied.

Usage:
    python -X utf8 scripts/render_diagrams.py --doc-dir DIR --name NAME \
        --out STITCHED.md [--figures-dir DIR] FILE.md [FILE.md ...]

Exit codes: 0 success; 1 a block failed to render or a figure failed the
font check; 2 usage error; 3 renderer, browser or font not available.
"""
from __future__ import annotations

import argparse
import base64
import datetime as _dt
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RENDER_DIR = ROOT / "scripts" / "diagram-render"
CONFIG_PATH = RENDER_DIR / "render-config.json"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.figures import (  # noqa: E402  (path set above)
    FIGURES_DIR,
    MANIFEST_NAME,
    MERMAID_BLOCK_RE,
    block_sha256,
)
from engine import diagram_ir  # noqa: E402

ATTRIBUTION = (
    "Render-receipt pattern adapted from tt-a1i/archify (MIT, "
    "https://github.com/tt-a1i/archify, commit "
    "0e4949f910a8e390bd3b4933883a4dcabad571be)"
)
# Mermaid's own default faces; they must never reach a figure.
MERMAID_DEFAULT_FACES = ("trebuchet ms", "verdana", "arial", "recursive variable")
BUILTIN_BANNED = (
    "Inter", "Geist", "Roboto", "Open Sans", "Lato", "Arial", "Fraunces",
    "IBM Plex", "Space Grotesk", "Instrument Serif", "Poppins", "Montserrat",
    "Nunito", "Trebuchet MS", "Verdana",
)
GENERIC_FAMILIES = {
    "serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui",
    "inherit", "initial", "unset",
}
ALT_RE = re.compile(r"^\s*%%\s*alt\s*:\s*(.+?)\s*$", re.MULTILINE | re.IGNORECASE)
CAPTION_RE = re.compile(r"^\s*%%\s*caption\s*:\s*(.+?)\s*$", re.MULTILINE | re.IGNORECASE)
IR_REF_RE = re.compile(r"^\s*%%\s*ir\s*:\s*(FIG-[0-9]{3})\s*$", re.MULTILINE)
INIT_LINE_RE = re.compile(r"^\s*%%\{init:.*\}%%\s*$")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
FONT_DECL_RE = re.compile(r"font-family\s*[:=]\s*\"?([^;\"}>]+)", re.IGNORECASE)


class RenderError(Exception):
    """A block failed to render or a figure failed a check."""


class SetupError(Exception):
    """Renderer, browser or font not available."""


@dataclass
class Block:
    figure: int
    source: Path
    index_in_file: int
    code: str
    alt: str
    alt_source: str
    caption: str
    start: int = 0
    end: int = 0
    result: dict = field(default_factory=dict)
    ir_figure: str = ""


# -- config and font policy -------------------------------------------------

def load_config(path: Path = CONFIG_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _first_existing(candidates, base: Path) -> Path | None:
    for c in candidates:
        p = Path(c)
        p = p if p.is_absolute() else (base / p)
        if p.is_file():
            return p.resolve()
    return None


def banned_families(config: dict) -> tuple[set[str], set[str], str]:
    """Return (banned exact names, banned prefixes, source description)."""
    sidecar = _first_existing(config.get("banned_fonts_json_candidates", []), ROOT)
    names = {n.lower() for n in BUILTIN_BANNED}
    prefixes: set[str] = {"ibm plex"}
    source = "built-in list (design sidecar not found)"
    if sidecar:
        data = json.loads(sidecar.read_text(encoding="utf-8"))
        for key in ("hardBan", "secondaryBan", "monospaceBanned"):
            names |= {e["family"].lower() for e in data.get(key, []) if "family" in e}
        prefixes |= {e["prefix"].lower() for e in data.get("hardBanFamilyPrefixes", [])}
        source = str(sidecar)
    names |= set(MERMAID_DEFAULT_FACES)
    return names, prefixes, source


def is_banned(family: str, names: set[str], prefixes: set[str]) -> bool:
    fam = family.strip().strip("'\"").lower()
    return fam in names or any(fam.startswith(p) for p in prefixes)


def check_font_policy(config: dict) -> str:
    family = config["diagram_font_family"]
    names, prefixes, source = banned_families(config)
    if family.strip().lower() in GENERIC_FAMILIES:
        raise SetupError(f"diagram_font_family '{family}' is a bare generic family")
    if is_banned(family, names, prefixes):
        raise SetupError(f"diagram_font_family '{family}' is banned ({source})")
    return source


def svg_font_violations(svg_text: str, family: str) -> list[str]:
    """Primary faces in the SVG other than the approved face or a generic."""
    bad = []
    for decl in FONT_DECL_RE.findall(html.unescape(svg_text)):
        first = decl.split(",")[0].strip().strip("'\"").strip()
        low = first.lower()
        if not first or low == family.lower() or low in GENERIC_FAMILIES:
            continue
        if low.startswith("var(") or "awesome" in low or low.startswith("katex"):
            continue
        bad.append(first)  # banned, a Mermaid default, or simply not approved
    # Mermaid 12 HTML labels inherit no face unless the universal rule from
    # theme_css() is present; without it the browser serif is used silently.
    compact = re.sub(r"\s+", "", html.unescape(svg_text))
    if f'*{{font-family:"{family}"'.replace(" ", "") not in compact.replace("'", '"'):
        bad.append("<missing universal font rule: labels would fall back>")
    return sorted(set(bad))


# -- Markdown handling --------------------------------------------------------

def _nearest_heading(text_before: str) -> str | None:
    heads = HEADING_RE.findall(text_before)
    if not heads:
        return None
    # Drop section numbering such as "2." or "3.4.1" from the heading text.
    return re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", heads[-1].strip()) or heads[-1].strip()


def _one_line(value: str) -> str:
    return " ".join(str(value).split())


def expand_ir_markers(path: Path, text: str, ir_info: dict) -> str:
    """Replace diagram-IR markers with the generated, validated figure source.

    Raises RenderError (every problem listed) when a marker names an unknown
    or invalid IR, when the IR is not the validated candidate, or when the
    generated Mermaid or trace table is missing or stale.
    """
    if not diagram_ir.MARKER_RE.search(text):
        return text
    doc_dir = path.parent
    irs, diags = diagram_ir.load_doc_irs(doc_dir)
    errors = [f"{path.name}: {d.code}: {d.message}" for d in diags]
    by_id = {ir.figure_id: ir for ir in irs}
    validated = diagram_ir.read_validated(doc_dir)
    gen_dir = doc_dir / diagram_ir.GENERATED_DIR
    try:
        gen_all = json.loads((gen_dir / diagram_ir.GENERATED_NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        gen_all = {}
    generated = gen_all.get("figures", {}) if isinstance(gen_all, dict) else {}

    def replace(m: re.Match) -> str:
        ref = m.group("ref")
        if ref == "trace-table":
            table = gen_dir / diagram_ir.TRACE_TABLE_NAME
            if not table.is_file() or diagram_ir.text_sha256_file(table) != gen_all.get("trace_table_sha256"):
                errors.append(f"{path.name}: diagram/stale-generated: trace table missing or "
                              "edited; run `python -m engine diagrams generate`")
                return m.group(0)
            return table.read_text(encoding="utf-8").rstrip("\n")
        ir = by_id.get(ref)
        if ir is None:
            errors.append(f"{path.name}: diagram/unknown-figure: {ref} has no IR in "
                          f"{doc_dir.name}/{diagram_ir.DIAGRAMS_DIR}/")
            return m.group(0)
        if validated.get(ref, {}).get("ir_sha256") != ir.sha256:
            errors.append(f"{path.name}: {diagram_ir.candidate_diagnostic(ir, validated.get(ref, {}).get('ir_sha256')).code}: "
                          f"{ref} ({ir.path.name}) changed after the last `diagrams validate`")
            return m.group(0)
        gen = generated.get(ref, {})
        mmd = gen_dir / str(gen.get("mermaid", f"{ref}.mmd"))
        if gen.get("ir_sha256") != ir.sha256 or not mmd.is_file() or diagram_ir.text_sha256_file(mmd) != gen.get("mermaid_sha256"):
            errors.append(f"{path.name}: diagram/stale-generated: {ref} Mermaid is missing or "
                          "out of date; run `python -m engine diagrams generate`")
            return m.group(0)
        body = [ln for ln in mmd.read_text(encoding="utf-8").splitlines()
                if not INIT_LINE_RE.match(ln)]
        ir_info[ref] = {"ir_path": ir.path.relative_to(doc_dir).as_posix(),
                        "ir_abs": ir.path, "ir_sha256": ir.sha256,
                        "mermaid_sha256": gen.get("mermaid_sha256")}
        meta = ir.meta
        return "\n".join(["```mermaid", f"%% ir: {ref}",
                          f"%% alt: {_one_line(meta['alt_text'])}",
                          f"%% caption: {_one_line(meta['caption'])}", *body, "```"])

    out = diagram_ir.MARKER_RE.sub(replace, text)
    if errors:
        raise RenderError("; ".join(errors))
    return out


def extract_blocks(sources: list[tuple[Path, str]], warn=print) -> list[Block]:
    blocks: list[Block] = []
    context = ""
    for path, text in sources:
        for i, m in enumerate(MERMAID_BLOCK_RE.finditer(text), start=1):
            code = m.group("code")
            alt_m, cap_m = ALT_RE.search(code), CAPTION_RE.search(code)
            heading = _nearest_heading(context + text[: m.start()])
            if alt_m:
                alt, alt_source = alt_m.group(1), "block-comment"
            else:
                alt = f"Diagram: {heading}" if heading else "Diagram"
                alt_source = "nearest-heading" if heading else "generic"
                warn(f"WARNING: {path.name} block {i}: no '%% alt:' comment; "
                     f"alt text taken from {alt_source}: {alt!r}")
            caption = cap_m.group(1) if cap_m else (heading or alt)
            ir_m = IR_REF_RE.search(code)
            blocks.append(Block(len(blocks) + 1, path, i, code, alt, alt_source,
                                caption, m.start(), m.end(),
                                ir_figure=ir_m.group(1) if ir_m else ""))
        context += text + "\n\n"
    return blocks


def font_stack(config: dict) -> str:
    """CSS family list for Mermaid, e.g. ``Public Sans, sans-serif``.

    Unquoted on purpose: Mermaid drops a themeVariables value that contains
    quote characters, which would let its default face (Trebuchet MS) through.
    A multi-word family name is valid unquoted CSS.
    """
    return f"{config['diagram_font_family']}, {config.get('diagram_font_fallback', 'sans-serif')}"


def theme_css(config: dict) -> str:
    """CSS that applies the approved face to every element of the figure."""
    fam = config["diagram_font_family"]
    fallback = config.get("diagram_font_fallback", "sans-serif")
    # Second rule (M10-07, diagram-visual-standards.md): no drop shadows; the
    # neutral theme otherwise adds a drop-shadow filter to every node.
    return (f"* {{ font-family: '{fam}', {fallback} !important; }} "
            "* { filter: none !important; }")


def init_directive(config: dict) -> str:
    """The ``%%{init}%%`` directive that pins theme and typeface for a block."""
    return json.dumps({"theme": config.get("mermaid_theme", "neutral"),
                       "themeVariables": {"fontFamily": font_stack(config)}}).join(
        ("%%{init: ", "}%%"))


def prepared_definition(code: str, config: dict) -> str:
    lines = [line for line in code.replace("\r\n", "\n").strip("\n").split("\n")
             if not ALT_RE.match(line) and not CAPTION_RE.match(line)]
    # A YAML front-matter config block must stay first; put the directive after it.
    stripped = [x.strip() for x in lines]
    if stripped and stripped[0] == "---" and "---" in stripped[1:]:
        close = 1 + stripped[1:].index("---")
        lines = lines[: close + 1] + [init_directive(config)] + lines[close + 1:]
    else:
        lines = [init_directive(config)] + lines
    return "\n".join(lines) + "\n"


def _md_attr(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def figure_markdown(block: Block, rel_png: str, width_in: float) -> str:
    caption = block.caption.replace("]", ")").replace("[", "(")
    return (f"![Figure {block.figure} — {caption}]({rel_png})"
            f"{{width={width_in:.2f}in fig-alt=\"{_md_attr(block.alt)}\"}}")


def slug(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-") or "doc"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# -- renderer -------------------------------------------------------------------

def resolve_browser(config: dict) -> Path:
    env = os.environ.get("PUPPETEER_EXECUTABLE_PATH")
    if env and Path(env).is_file():
        return Path(env)
    found = _first_existing(config.get("browser_candidates", []), ROOT)
    if not found:
        raise SetupError("no local Chrome/Edge found; set PUPPETEER_EXECUTABLE_PATH")
    return found


def resolve_font_file(config: dict) -> Path:
    env = os.environ.get("SRS_DIAGRAM_FONT_FILE")
    if env and Path(env).is_file():
        return Path(env).resolve()
    found = _first_existing(config.get("font_file_candidates", []), ROOT)
    if not found:
        raise SetupError(
            f"font file for '{config['diagram_font_family']}' not found; set "
            "SRS_DIAGRAM_FONT_FILE (the face is never silently substituted)")
    return found


def run_renderer(blocks: list[Block], figures_dir: Path, doc_slug: str,
                 config: dict) -> dict:
    mmdc_pkg = RENDER_DIR / "node_modules" / "@mermaid-js" / "mermaid-cli"
    if not mmdc_pkg.is_dir():
        raise SetupError("renderer not installed: run `npm ci` in scripts/diagram-render "
                         "with PUPPETEER_SKIP_DOWNLOAD=1")
    node = shutil.which("node")
    if not node:
        raise SetupError("node is not on PATH")
    browser = resolve_browser(config)
    font_file = resolve_font_file(config)
    family = config["diagram_font_family"]
    figures_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="srs-render-") as tmp:
        tmpd = Path(tmp)
        # Inline the face as a data: URI; the renderer's file interceptor does
        # not serve .ttf files, and inlining keeps the render fully offline.
        font_b64 = base64.b64encode(font_file.read_bytes()).decode("ascii")
        (tmpd / "diagram-font.css").write_text(
            "@font-face {\n"
            f"  font-family: \"{family}\";\n"
            f"  src: url(data:font/ttf;base64,{font_b64}) format(\"truetype\");\n"
            "  font-weight: 100 900;\n  font-style: normal;\n}\n",
            encoding="utf-8")
        jobs = []
        for b in blocks:
            stem = f"{doc_slug}-{b.figure}"
            jobs.append({"id": stem, "definition": prepared_definition(b.code, config),
                         "svg": str(figures_dir / f"{stem}.svg"),
                         "png": str(figures_dir / f"{stem}.png")})
        job_file = tmpd / "job.json"
        job_file.write_text(json.dumps({
            "fontCss": str(tmpd / "diagram-font.css"),
            "fontFamily": family,
            "mermaidConfig": {"theme": config.get("mermaid_theme", "neutral"),
                              "fontFamily": font_stack(config),
                              "themeVariables": {"fontFamily": font_stack(config)},
                              # Mermaid 12 sets the face only through a CSS
                              # variable scoped to a selector that matches
                              # nothing, so HTML labels fell back to the
                              # browser serif. Pin it on every element.
                              "themeCSS": theme_css(config)},
            "bodyMeasureIn": config["body_measure_in"],
            "maxHeightIn": config["max_figure_height_in"],
            "minPpi": config["min_ppi"],
            "jobs": jobs,
        }), encoding="utf-8")
        env = dict(os.environ, PUPPETEER_EXECUTABLE_PATH=str(browser),
                   PUPPETEER_SKIP_DOWNLOAD="1")
        proc = subprocess.run([node, str(RENDER_DIR / "render.mjs"), str(job_file)],
                              cwd=RENDER_DIR, env=env, capture_output=True, text=True)
        result_file = tmpd / "job.result.json"
        if not result_file.is_file():
            raise SetupError(f"renderer crashed (exit {proc.returncode}): "
                             f"{proc.stderr.strip()[-2000:]}")
        payload = json.loads(result_file.read_text("utf-8"))
        results = {r["id"]: r for r in payload["results"]}
        for r in results.values():
            if r.get("ok"):
                embed_font(Path(figures_dir / f"{r['id']}.svg"), family, font_b64)
    return {"results": results, "browser": str(browser), "font_file": font_file,
            "font_probe": payload.get("fontProbe"),
            "exit": proc.returncode}


def embed_font(svg_path: Path, family: str, font_b64: str) -> None:
    """Embed the approved face in the SVG so it renders the same anywhere."""
    text = svg_path.read_text(encoding="utf-8")
    style = (f'<style>@font-face{{font-family:"{family}";'
             f'src:url(data:font/ttf;base64,{font_b64}) format("truetype");'
             'font-weight:100 900;font-style:normal;}</style>')
    end = text.find(">", text.find("<svg")) + 1
    svg_path.write_text(text[:end] + style + text[end:], encoding="utf-8")


def renderer_versions() -> dict:
    out = {}
    for pkg in ("@mermaid-js/mermaid-cli", "mermaid", "puppeteer"):
        pj = RENDER_DIR / "node_modules" / pkg / "package.json"
        if pj.is_file():
            out[pkg] = json.loads(pj.read_text(encoding="utf-8")).get("version")
    return out


# -- main -------------------------------------------------------------------------

def write_manifest(figures_dir: Path, name: str, entry: dict) -> Path:
    path = figures_dir / MANIFEST_NAME
    data = {"schema": "srs-render-manifest/1", "attribution": ATTRIBUTION, "documents": {}}
    if path.is_file():
        try:
            old = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(old.get("documents"), dict):
                data["documents"] = old["documents"]
        except ValueError:
            pass
    data["documents"][name] = entry
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def _rel(path: Path, base: Path) -> str:
    try:
        return Path(os.path.relpath(path, base)).as_posix()
    except ValueError:  # different drive
        return path.resolve().as_posix()


def build(files: list[Path], doc_dir: Path, name: str, out: Path,
          figures_dir: Path | None = None, config: dict | None = None) -> int:
    config = config or load_config()
    figures_dir = (figures_dir or doc_dir / FIGURES_DIR).resolve()
    sources = [(f.resolve(), f.read_text(encoding="utf-8-sig")) for f in files]  # drop BOMs: stitching would leave them mid-document
    ir_info: dict = {}
    try:
        sources = [(p, expand_ir_markers(p, t, ir_info)) for p, t in sources]
    except RenderError as exc:
        for msg in str(exc).split("; "):
            print(f"ERROR: {msg}", file=sys.stderr)
        return 1
    blocks = extract_blocks(sources, warn=lambda m: print(m, file=sys.stderr))
    out.parent.mkdir(parents=True, exist_ok=True)
    if not blocks:
        out.write_text("\n\n".join(t for _, t in sources), encoding="utf-8")
        print(f"render_diagrams: no Mermaid blocks in {len(files)} file(s)")
        return 0
    banned_source = check_font_policy(config)
    doc_slug = slug(name)
    run = run_renderer(blocks, figures_dir, doc_slug, config)
    family = config["diagram_font_family"]
    failures = []
    for b in blocks:
        r = run["results"].get(f"{doc_slug}-{b.figure}", {"ok": False, "error": "no result"})
        if not r.get("ok"):
            failures.append(f"{b.source.name} block {b.index_in_file} (figure {b.figure}): "
                            f"{' | '.join(r.get('error', 'failed').splitlines()[:4])}")
            continue
        svg = figures_dir / f"{doc_slug}-{b.figure}.svg"
        bad = svg_font_violations(svg.read_text(encoding="utf-8"), family)
        if bad:
            failures.append(f"{b.source.name} block {b.index_in_file}: figure uses "
                            f"non-approved face(s) {bad}")
        if r["ppi"] < config["min_ppi"]:
            failures.append(f"{b.source.name} block {b.index_in_file}: {r['ppi']} ppi "
                            f"< {config['min_ppi']}")
        b.result = r
    if failures:
        for f in failures:
            print(f"ERROR: {f}", file=sys.stderr)
        return 1
    # Replace blocks, file by file, from the end so offsets stay valid.
    by_file: dict[Path, list[Block]] = {}
    for b in blocks:
        by_file.setdefault(b.source, []).append(b)
    stitched = []
    for path, text in sources:
        for b in reversed(by_file.get(path, [])):
            png = figures_dir / f"{doc_slug}-{b.figure}.png"
            md = figure_markdown(b, _rel(png, doc_dir), b.result["printedWidthIn"])
            text = text[: b.start] + md + "\n" + text[b.end:]
        stitched.append(text)
    out.write_text("\n\n".join(stitched), encoding="utf-8")
    font_file = run["font_file"]
    entry = {
        "generated": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "renderer": {"packages": renderer_versions(), "browser": run["browser"],
                     "hosted_renderer": False},
        "font": {"family": family, "fallback": config.get("diagram_font_fallback"),
                 "file": font_file.name, "file_sha256": sha256_file(font_file),
                 "loaded_via": "@font-face data URI from the local file; embedded in each SVG",
                 "headless_chrome_probe": run.get("font_probe"),
                 "banned_list": banned_source},
        "figures": [],
    }
    for b in blocks:
        png = figures_dir / f"{doc_slug}-{b.figure}.png"
        svg = figures_dir / f"{doc_slug}-{b.figure}.svg"
        entry["figures"].append({
            "figure": b.figure, "source": _rel(b.source, figures_dir),
            "block_index": b.index_in_file, "source_sha256": block_sha256(b.code),
            "png": png.name, "svg": svg.name,
            "png_sha256": sha256_file(png), "svg_sha256": sha256_file(svg),
            "png_px": [b.result["pngWidthPx"], b.result["pngHeightPx"]],
            "printed_width_in": round(b.result["printedWidthIn"], 3),
            "ppi": b.result["ppi"], "caption": b.caption, "alt": b.alt,
            "alt_source": b.alt_source,
        })
        info = ir_info.get(b.ir_figure)
        if info:
            entry["figures"][-1].update({
                "ir_figure_id": b.ir_figure, "ir_path": _rel(info["ir_abs"], doc_dir),
                "ir_sha256": info["ir_sha256"], "mermaid_sha256": info["mermaid_sha256"]})
    manifest = write_manifest(figures_dir, name, entry)
    print(f"render_diagrams: {len(blocks)} figure(s) rendered; manifest {manifest}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--doc-dir", type=Path, required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--figures-dir", type=Path)
    args = ap.parse_args(argv)
    missing = [f for f in args.files if not f.is_file()]
    if missing:
        print(f"ERROR: missing source file(s): {missing}", file=sys.stderr)
        return 2
    try:
        return build(args.files, args.doc_dir, args.name, args.out, args.figures_dir)
    except SetupError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
