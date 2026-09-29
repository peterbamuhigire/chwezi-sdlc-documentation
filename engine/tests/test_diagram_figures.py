"""M10-01-T09/T10/T12: rendered-figure evidence, the .docx guard, the render
step and the phase03/phase06 figure gates."""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

from engine import figures
from engine.artifact_graph import ArtifactGraph
from engine.findings import FindingCollection
from engine.gates.phase03 import Phase03Gate
from engine.gates.phase06 import Phase06Gate
from engine.workspace import Workspace

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "diagram_render"
PNG = b"\x89PNG\r\n\x1a\n"


def load_script(name: str):
    path = ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location(name.removesuffix(".py"), path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses need the module registered
    spec.loader.exec_module(module)
    return module


def _ws(tmp_path, files):
    for rel, body in files.items():
        full = tmp_path / rel
        full.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(body, bytes):
            full.write_bytes(body)
        else:
            full.write_text(body, encoding="utf-8")
    return ArtifactGraph.build(Workspace.load(tmp_path))


IR_BLOCK = (
    "flowchart TD\n"
    "  A[Alert] --> B[Page on-call]\n"
    "  B --> C[Escalate to incident lead]\n"
)
INFRA_MERMAID_ONLY = (
    "# Infrastructure\n\n## Incident response flow\n\n"
    f"```mermaid\n{IR_BLOCK}```\n"
)
OPS_BASE = {
    "_context/vision.md": "# Vision",
    "06-deployment-operations/deployment-guide.md": "# Deployment\nRollback via tag.",
    "06-deployment-operations/runbook.md": "# Runbook\nEscalation: on-call.",
    "06-deployment-operations/monitoring.md": "# Monitoring\nSLO 99.9%.",
}


def _manifest(fig_dir: Path, source_rel: str, code: str, png: str = "doc-1.png",
              caption: str = "Incident response flow") -> None:
    fig_dir.mkdir(parents=True, exist_ok=True)
    (fig_dir / figures.MANIFEST_NAME).write_text(json.dumps({
        "documents": {"Doc": {"figures": [{
            "figure": 1, "source": source_rel, "block_index": 1,
            "source_sha256": figures.block_sha256(code), "png": png,
            "caption": caption, "alt": caption,
        }]}}
    }), encoding="utf-8")


def _ir_findings(graph):
    findings = FindingCollection()
    Phase06Gate().evaluate(graph, findings)
    return [f.message for f in findings if f.gate_id == "phase06.infra_has_ir_diagram"]


# -- phase06: incident-response figure ------------------------------------

def test_phase06_mermaid_block_alone_fails(tmp_path):
    graph = _ws(tmp_path, {**OPS_BASE,
                           "06-deployment-operations/infrastructure.md": INFRA_MERMAID_ONLY})
    msgs = _ir_findings(graph)
    assert msgs and "a code block alone is not a figure" in msgs[0]


def test_phase06_word_mermaid_in_prose_fails(tmp_path):
    graph = _ws(tmp_path, {**OPS_BASE, "06-deployment-operations/infrastructure.md":
                           "# Infrastructure\nIncident response: see the mermaid diagram."})
    assert _ir_findings(graph)


def test_phase06_recorded_rendering_passes(tmp_path):
    ops = tmp_path / "06-deployment-operations"
    _ws(tmp_path, {**OPS_BASE, "06-deployment-operations/infrastructure.md": INFRA_MERMAID_ONLY})
    _manifest(ops / "_figures", "../infrastructure.md", IR_BLOCK)
    (ops / "_figures" / "doc-1.png").write_bytes(PNG)
    graph = ArtifactGraph.build(Workspace.load(tmp_path))
    assert _ir_findings(graph) == []


def test_phase06_stale_rendering_fails(tmp_path):
    ops = tmp_path / "06-deployment-operations"
    _ws(tmp_path, {**OPS_BASE, "06-deployment-operations/infrastructure.md": INFRA_MERMAID_ONLY})
    _manifest(ops / "_figures", "../infrastructure.md", IR_BLOCK + "  C --> D[Close]\n")
    (ops / "_figures" / "doc-1.png").write_bytes(PNG)
    graph = ArtifactGraph.build(Workspace.load(tmp_path))
    assert _ir_findings(graph)


def test_phase06_recorded_rendering_with_missing_png_fails(tmp_path):
    ops = tmp_path / "06-deployment-operations"
    _ws(tmp_path, {**OPS_BASE, "06-deployment-operations/infrastructure.md": INFRA_MERMAID_ONLY})
    _manifest(ops / "_figures", "../infrastructure.md", IR_BLOCK)
    graph = ArtifactGraph.build(Workspace.load(tmp_path))
    assert _ir_findings(graph)


def test_phase06_dangling_or_remote_image_fails(tmp_path):
    graph = _ws(tmp_path, {**OPS_BASE, "06-deployment-operations/infrastructure.md": (
        "# Infrastructure\nIncident response flow:\n"
        "![IR flow](missing/ir.png)\n![IR flow](https://example.org/ir.png)\n")})
    assert _ir_findings(graph)


def test_phase06_existing_image_without_ir_label_fails(tmp_path):
    graph = _ws(tmp_path, {**OPS_BASE,
                           "06-deployment-operations/infrastructure.md": (
                               "# Infrastructure\nIncident response is covered below.\n"
                               "![Network layout](net.png)\n"),
                           "06-deployment-operations/net.png": PNG})
    assert _ir_findings(graph)


def test_phase06_root_relative_image_passes(tmp_path):
    graph = _ws(tmp_path, {**OPS_BASE,
                           "06-deployment-operations/infrastructure.md": (
                               "# Infrastructure\n![Incident response flow]"
                               "(assets/ir-flow.png \"IR\")\n"),
                           "assets/ir-flow.png": PNG})
    assert _ir_findings(graph) == []


def test_figure_provider_extension_point(tmp_path, monkeypatch):
    graph = _ws(tmp_path, {**OPS_BASE,
                           "06-deployment-operations/infrastructure.md": INFRA_MERMAID_ONLY})

    def sidecar(art, root):
        return [figures.Figure(label="incident response IR sidecar",
                               target="ir.json", kind="ir-sidecar")]

    monkeypatch.setattr(figures, "FIGURE_PROVIDERS", [sidecar])
    assert _ir_findings(graph) == []


def test_figures_helpers_without_root_and_bad_manifest(tmp_path):
    graph = _ws(tmp_path, {**OPS_BASE,
                           "06-deployment-operations/infrastructure.md": INFRA_MERMAID_ONLY,
                           "06-deployment-operations/_figures/render-manifest.json": "{not json",
                           "x/_figures/render-manifest.json": json.dumps(
                               {"documents": {"D": {"figures": [{"source": 3}]}}})})
    art = next(a for a in graph.artifacts if a.path.name == "infrastructure.md")
    assert figures.figures_in(art, None) == []
    assert figures.rendered_figures(art, tmp_path) == []
    assert figures.load_manifest_index(tmp_path) == {}
    no_block = next(a for a in graph.artifacts if a.path.name == "runbook.md")
    assert figures.rendered_figures(no_block, tmp_path) == []
    assert _ir_findings(ArtifactGraph(artifacts=graph.artifacts, root=None))


def test_block_sha_normalises_line_endings():
    assert figures.block_sha256("a\r\nb\n") == figures.block_sha256("\na\nb")


# -- phase03: HLD/LLD design figures ---------------------------------------

def _design_findings(graph):
    findings = FindingCollection()
    Phase03Gate().evaluate(graph, findings)
    return [f.message for f in findings if f.gate_id == "phase03.design_docs_have_figures"]


HLD_MERMAID = "# HLD\n\n## Context\n\n```mermaid\nflowchart LR\n  A --> B\n```\n"


def test_phase03_hld_with_mermaid_only_fails(tmp_path):
    graph = _ws(tmp_path, {"_context/vision.md": "# Vision",
                           "03-design-documentation/01-high-level-design/01-context.md": HLD_MERMAID,
                           "03-design-documentation/02-lld/lld.md": "# LLD\nNo figures."})
    msgs = _design_findings(graph)
    assert len(msgs) == 2
    assert "01-high-level-design" in msgs[0] and "02-lld" in msgs[1]


def test_phase03_hld_with_rendered_figure_passes(tmp_path):
    hld = tmp_path / "03-design-documentation" / "01-high-level-design"
    _ws(tmp_path, {"_context/vision.md": "# Vision",
                   "03-design-documentation/01-high-level-design/01-context.md": HLD_MERMAID,
                   "03-design-documentation/01-high-level-design/02-more.md": "# More"})
    _manifest(hld / "_figures", "../01-context.md", "flowchart LR\n  A --> B\n")
    (hld / "_figures" / "doc-1.png").write_bytes(PNG)
    graph = ArtifactGraph.build(Workspace.load(tmp_path))
    assert _design_findings(graph) == []


def test_phase03_lld_file_with_image_passes_and_no_design_doc_is_silent(tmp_path):
    graph = _ws(tmp_path, {"_context/vision.md": "# Vision",
                           "03-design-documentation/Kulima_LLD.md": "# LLD\n![Classes](c.png)",
                           "03-design-documentation/c.png": PNG})
    assert _design_findings(graph) == []
    graph = _ws(tmp_path / "other", {"_context/vision.md": "# Vision",
                                     "03-design-documentation/threat-model.md": "# Threat model"})
    assert _design_findings(graph) == []


# -- check_docx_diagrams.py --------------------------------------------------

def _docx(path: Path, text: str, media: bool = False) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(f"<w:p><w:r><w:t>{line}</w:t></w:r></w:p>" for line in text.split("\n"))
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("word/document.xml", f"<w:document><w:body>{body}</w:body></w:document>")
        if media:
            zf.writestr("word/media/image1.png", PNG)
    return path


def test_check_docx_clean_and_dirty(tmp_path, capsys):
    guard = load_script("check_docx_diagrams.py")
    clean = _docx(tmp_path / "clean.docx", "A flowchart shows the flow.\nFigure 1", media=True)
    dirty = _docx(tmp_path / "dirty.docx", "sequenceDiagram\nA->>B: hi\nerDiagram")
    assert guard.main([str(clean)]) == 0
    assert guard.main([str(dirty)]) == 1
    out = capsys.readouterr().out
    assert "MERMAID-SOURCE" in out and "erDiagram" in out and "sequenceDiagram" in out


def test_check_docx_scan_excludes_and_reports(tmp_path, capsys):
    guard = load_script("check_docx_diagrams.py")
    _docx(tmp_path / "p" / "A.docx", "graph TD\nA-->B")
    _docx(tmp_path / "p" / "_kaizen" / "B.docx", "flowchart LR\nA-->B")
    _docx(tmp_path / "p" / ".trash-20260929" / "C.docx", "classDiagram")
    _docx(tmp_path / "p" / "~$lock.docx", "stateDiagram-v2")
    report = tmp_path / "r.json"
    assert guard.main(["--scan", str(tmp_path / "p"), "--exclude", "_kaizen",
                       "--json", str(report)]) == 1
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["scanned"] == 1 and len(data["dirty"]) == 1
    assert "Scanned 1 .docx" in capsys.readouterr().out


def test_check_docx_usage_and_read_errors(tmp_path):
    guard = load_script("check_docx_diagrams.py")
    assert guard.main([]) == 2
    assert guard.main(["--scan", str(tmp_path / "absent")]) == 2
    bad = tmp_path / "bad.docx"
    bad.write_bytes(b"not a zip")
    assert guard.main([str(bad)]) == 2


# -- render_diagrams.py (pure parts) -------------------------------------------

def test_render_block_extraction_alt_caption_and_directive(tmp_path):
    rd = load_script("render_diagrams.py")
    cfg = rd.load_config()
    warnings = []
    text_a = "# Doc\n\n## 2.1 Context view\n\n```mermaid\n%% alt: Alt A\n%% caption: Cap A\nflowchart LR\n  A-->B\n```\n"
    text_b = "Intro without heading.\n\n~~~mermaid\n---\ntitle: T\n---\nsequenceDiagram\n  A->>B: x\n~~~\n"
    blocks = rd.extract_blocks([(tmp_path / "a.md", text_a), (tmp_path / "b.md", text_b)],
                               warn=warnings.append)
    assert [b.figure for b in blocks] == [1, 2]
    assert (blocks[0].alt, blocks[0].caption, blocks[0].alt_source) == ("Alt A", "Cap A", "block-comment")
    assert blocks[1].alt == "Diagram: Context view" and blocks[1].alt_source == "nearest-heading"
    assert warnings and "no '%% alt:'" in warnings[0]
    d0 = rd.prepared_definition(blocks[0].code, cfg)
    assert d0.startswith("%%{init: ") and "Public Sans, sans-serif" in d0 and "%% alt" not in d0
    d1 = rd.prepared_definition(blocks[1].code, cfg).split("\n")
    assert d1[0] == "---" and d1[3].startswith("%%{init")
    md = rd.figure_markdown(blocks[0], "_figures/doc-1.png", 6.25)
    assert md == ('![Figure 1 — Cap A](_figures/doc-1.png){width=6.25in fig-alt="Alt A"}')
    assert rd.slug("My Doc v1.0") == "My-Doc-v1.0"
    assert rd.extract_blocks([(tmp_path / "c.md", "```mermaid\nA\n```\n")], warn=warnings.append)[0].alt == "Diagram"


def test_render_font_policy(tmp_path):
    rd = load_script("render_diagrams.py")
    cfg = rd.load_config()
    assert cfg["diagram_font_family"] == "Public Sans"
    rd.check_font_policy(cfg)
    for bad in ("Arial", "Trebuchet MS", "IBM Plex Sans Arabic", "sans-serif", "Inter"):
        with pytest.raises(rd.SetupError):
            rd.check_font_policy({**cfg, "diagram_font_family": bad})
    good_svg = ("<svg><style>#s *{font-family:'Public Sans', sans-serif !important;}"
                "#s{font-family:&quot;Public Sans&quot;,sans-serif}</style></svg>")
    assert rd.svg_font_violations(good_svg, "Public Sans") == []
    bad_svg = '<svg><style>#s{font-family:"trebuchet ms",verdana,arial}</style></svg>'
    found = rd.svg_font_violations(bad_svg, "Public Sans")
    assert "trebuchet ms" in found and any("missing universal" in f for f in found)
    names, prefixes, _ = rd.banned_families({})
    assert rd.is_banned("IBM Plex Mono", names, prefixes) and not rd.is_banned("Public Sans", names, prefixes)


def test_render_without_blocks_stitches_only(tmp_path):
    rd = load_script("render_diagrams.py")
    (tmp_path / "a.md").write_text("# A\n", encoding="utf-8")
    (tmp_path / "b.md").write_text("# B\n", encoding="utf-8")
    out = tmp_path / "out" / "s.md"
    assert rd.main([str(tmp_path / "a.md"), str(tmp_path / "b.md"), "--doc-dir", str(tmp_path),
                    "--name", "S", "--out", str(out)]) == 0
    assert out.read_text(encoding="utf-8") == "# A\n\n\n# B\n"
    assert rd.main([str(tmp_path / "zz.md"), "--doc-dir", str(tmp_path), "--name", "S",
                    "--out", str(out)]) == 2


def test_render_manifest_merges_documents(tmp_path):
    rd = load_script("render_diagrams.py")
    rd.write_manifest(tmp_path, "A", {"figures": []})
    rd.write_manifest(tmp_path, "B", {"figures": []})
    data = json.loads((tmp_path / figures.MANIFEST_NAME).read_text(encoding="utf-8"))
    assert set(data["documents"]) == {"A", "B"} and "archify" in data["attribution"]


def _renderer_available() -> bool:
    rd = load_script("render_diagrams.py")
    if not (rd.RENDER_DIR / "node_modules" / "@mermaid-js" / "mermaid-cli").is_dir():
        return False
    bash = shutil.which("bash")
    if not shutil.which("node") or not shutil.which("pandoc") or not bash:
        return False
    if "system32" in bash.lower():  # WSL bash cannot run the Windows toolchain
        return False
    try:
        rd.resolve_browser(rd.load_config())
        rd.resolve_font_file(rd.load_config())
    except rd.SetupError:
        return False
    return (ROOT / "templates" / "reference.docx").is_file()


@pytest.mark.skipif(not _renderer_available(),
                    reason="local renderer, browser, font, pandoc or reference.docx absent")
def test_build_doc_renders_fixture_and_rejects_malformed(tmp_path):
    for case in ("valid", "malformed"):
        shutil.copytree(FIXTURES / case / "design", tmp_path / case / "design")
    env = dict(os.environ)
    ok = subprocess.run([shutil.which("bash"), "scripts/build-doc.sh",
                         str(tmp_path / "valid" / "design").replace("\\", "/"), "FixtureDesign"],
                        capture_output=True, text=True, env=env, cwd=ROOT)
    assert ok.returncode == 0, ok.stderr
    figs = tmp_path / "valid" / "design" / "_figures"
    assert len(list(figs.glob("*.png"))) == 2 and len(list(figs.glob("*.svg"))) == 2
    with zipfile.ZipFile(tmp_path / "valid" / "FixtureDesign.docx") as zf:
        assert len([n for n in zf.namelist() if n.startswith("word/media/")]) >= 2
    manifest = json.loads((figs / figures.MANIFEST_NAME).read_text(encoding="utf-8"))
    entry = manifest["documents"]["FixtureDesign"]
    assert all(f["ppi"] >= 300 for f in entry["figures"])
    assert entry["font"]["family"] == "Public Sans"
    bad = subprocess.run([shutil.which("bash"), "scripts/build-doc.sh",
                          str(tmp_path / "malformed" / "design").replace("\\", "/"), "Bad"],
                         capture_output=True, text=True, env=env, cwd=ROOT)
    assert bad.returncode != 0
    assert not (tmp_path / "malformed" / "Bad.docx").exists()
