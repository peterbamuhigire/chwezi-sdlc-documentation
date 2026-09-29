"""M10-07-T10/T11: figure manifest, candidate freezing in the renderer, IR figure
provider and the healthcare admissions pilot."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

from engine import figures
from engine.artifact_graph import ArtifactGraph
from engine.cli import main
from engine.diagram_ir import read_validated
from engine.diagram_manifest import build_manifest, find_manifests, verify, write_manifest
from engine.findings import FindingCollection, Severity
from engine.gates.phase03 import Phase03Gate
from engine.tests.test_diagram_figures import ROOT, _renderer_available, load_script
from engine.workspace import Workspace

PILOT = Path(__file__).resolve().parent / "fixtures" / "healthcare_admissions"
REL = Path("03-design-documentation") / "01-high-level-design"


def _pilot(tmp_path: Path) -> Path:
    dst = tmp_path / "ha"
    shutil.copytree(PILOT, dst, ignore=shutil.ignore_patterns("_figures", "*.docx", "*.figures.json"))
    return dst


def _bump(path: Path, old: bytes = b"Billing system", new: bytes = b"Billing systemz") -> None:
    path.write_bytes(path.read_bytes().replace(old, new, 1))


# -- pilot (T11) ------------------------------------------------------------------

def test_pilot_ir_validates_and_committed_record_is_current(tmp_path):
    result = CliRunner().invoke(main, ["diagrams", "validate", str(_pilot(tmp_path))])
    assert result.exit_code == 0, result.output
    assert "DIAGRAMS: PASS (3 figure(s) validated)" in result.output
    committed = read_validated(PILOT / REL)
    assert committed == read_validated(tmp_path / "ha" / REL)
    assert sorted(committed) == ["FIG-001", "FIG-002", "FIG-003"]


def test_pilot_phase03_sees_ir_figures_and_trace_evidence():
    graph = ArtifactGraph.build(Workspace.load(PILOT))
    findings = FindingCollection()
    Phase03Gate().evaluate(graph, findings)
    ids = {f.gate_id for f in findings}
    assert "phase03.design_docs_have_figures" not in ids
    assert "phase03.requirements_have_design_evidence" not in ids  # the generated trace table
    diagram = findings.for_gate("phase03.diagram_trace")
    assert [(f.code, f.severity) for f in diagram] == [("diagram/registry-absent", Severity.INFO)]


def test_ir_figure_provider_requires_the_validated_candidate(tmp_path):
    project = _pilot(tmp_path)
    graph = ArtifactGraph.build(Workspace.load(project))
    hld = next(a for a in graph.artifacts if a.path.name == "hld.md")
    figs = [f for f in figures.figures_in(hld, project) if f.kind == "diagram-ir"]
    assert len(figs) == 3 and "Admissions system context" in figs[0].label
    _bump(project / REL / "diagrams" / "context.ir.json")
    figs = [f for f in figures.figures_in(hld, project) if f.kind == "diagram-ir"]
    assert len(figs) == 2
    assert figures.figures_in(hld, None) == []


# -- renderer expansion (no browser needed) -----------------------------------------

def test_expand_markers_inserts_validated_figure_and_trace_table(tmp_path):
    rd = load_script("render_diagrams.py")
    project = _pilot(tmp_path)
    hld = project / REL / "hld.md"
    info: dict = {}
    out = rd.expand_ir_markers(hld, hld.read_text(encoding="utf-8"), info)
    assert out.count("```mermaid") == 3 and "%% ir: FIG-002" in out
    assert "%% alt: Sequence diagram: the clerk retries" in out
    assert "%%{init" not in out  # the renderer adds its own directive from the same config
    assert "| Figure | Element | Kind | Requirement IDs | SRS section |" in out
    assert sorted(info) == ["FIG-001", "FIG-002", "FIG-003"]
    blocks = rd.extract_blocks([(hld, out)], warn=lambda m: None)
    assert [b.ir_figure for b in blocks] == ["FIG-001", "FIG-002", "FIG-003"]
    assert blocks[0].caption == "System context of the synthetic admissions service"
    assert "* { filter: none !important; }" in rd.theme_css(rd.load_config())


@pytest.mark.parametrize("mutate, code", [
    ("ir", "diagram/candidate-not-validated"),
    ("mmd", "diagram/stale-generated"),
    ("table", "diagram/stale-generated"),
    ("marker", "diagram/unknown-figure"),
])
def test_expand_markers_refuses_stale_or_unvalidated(tmp_path, mutate, code):
    rd = load_script("render_diagrams.py")
    project = _pilot(tmp_path)
    doc = project / REL
    hld = doc / "hld.md"
    if mutate == "ir":
        _bump(doc / "diagrams" / "context.ir.json")
    elif mutate == "mmd":
        _bump(doc / "_generated" / "FIG-002.mmd", b"Draft store", b"Draft stores")
    elif mutate == "table":
        _bump(doc / "_generated" / "trace-table.md", b"FIG-001", b"FIG-009")
    else:
        hld.write_text(hld.read_text(encoding="utf-8").replace("FIG-003", "FIG-004"),
                       encoding="utf-8")
    with pytest.raises(rd.RenderError, match=code):
        rd.expand_ir_markers(hld, hld.read_text(encoding="utf-8"), {})
    assert rd.build([hld], doc, "X", tmp_path / "out.md") == 1


def test_expand_is_a_no_op_without_markers(tmp_path):
    rd = load_script("render_diagrams.py")
    p = tmp_path / "a.md"
    p.write_text("# A\n", encoding="utf-8")
    assert rd.expand_ir_markers(p, "# A\n", {}) == "# A\n"


# -- manifest (T10) --------------------------------------------------------------------

def _fake_build(project: Path, name: str = "PilotHLD") -> Path:
    """A render manifest as scripts/render_diagrams.py writes it, without a browser."""
    doc = project / REL
    figs = doc / "_figures"
    figs.mkdir()
    rd = load_script("render_diagrams.py")
    gen = json.loads((doc / "_generated" / ".generated.json").read_text(encoding="utf-8"))
    entries = []
    for n, fid in enumerate(sorted(gen["figures"]), start=1):
        (figs / f"{name}-{n}.png").write_bytes(b"\x89PNG fake " + fid.encode())
        (figs / f"{name}-{n}.svg").write_text(f"<svg>{fid}</svg>", encoding="utf-8")
        rec = gen["figures"][fid]
        entries.append({"figure": n, "png": f"{name}-{n}.png", "svg": f"{name}-{n}.svg",
                        "png_sha256": rd.sha256_file(figs / f"{name}-{n}.png"),
                        "svg_sha256": rd.sha256_file(figs / f"{name}-{n}.svg"),
                        "ir_figure_id": fid, "ir_path": rec["ir_path"],
                        "ir_sha256": rec["ir_sha256"], "mermaid_sha256": rec["mermaid_sha256"]})
    entries.append({"figure": 4, "png": f"{name}-4.png", "svg": f"{name}-4.svg",
                    "png_sha256": None, "svg_sha256": None})
    (figs / f"{name}-4.png").write_bytes(b"plain")
    (figs / f"{name}-4.svg").write_bytes(b"plain")
    entries[-1]["png_sha256"] = rd.sha256_file(figs / f"{name}-4.png")
    entries[-1]["svg_sha256"] = rd.sha256_file(figs / f"{name}-4.svg")
    (figs / "render-manifest.json").write_text(json.dumps({"documents": {name: {
        "renderer": {"packages": {"@mermaid-js/mermaid-cli": "12.0.0"}, "browser": "chrome"},
        "font": {"family": "Public Sans", "headless_chrome_probe": {"resolved": True}},
        "figures": entries}}}), encoding="utf-8")
    docx = doc.parent / f"{name}.docx"
    docx.write_bytes(b"PK fake docx")
    return docx


def test_manifest_records_hashes_and_verifies_clean(tmp_path):
    project = _pilot(tmp_path)
    docx = _fake_build(project)
    out = write_manifest(project / REL, "PilotHLD", docx)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert out.name == "PilotHLD.figures.json" and out.parent == docx.parent
    fig = data["figures"][0]
    assert fig["figure_id"] == "FIG-001" and fig["ir_sha256"] == fig["validated_ir_sha256"]
    assert fig["font_substitution_check"] == "PASS" and fig["state"] == "local-review-export"
    assert data["figures"][3]["figure_id"] == "fig-4" and data["figures"][3]["ir_path"] is None
    assert "PilotHLD.docx" in data["artifact_sha256"]
    assert any(k.endswith("context.ir.json") for k in data["artifact_sha256"])
    assert verify(out) == []
    result = CliRunner().invoke(main, ["diagrams", "verify-manifest", str(project / REL)])
    assert result.exit_code == 0 and "VERIFY-MANIFEST: PASS" in result.output


@pytest.mark.parametrize("target, figure", [
    (REL / "diagrams" / "context.ir.json", "FIG-001"),
    (REL / "_figures" / "PilotHLD-3.png", "FIG-003"),
    (REL / "_generated" / "FIG-002.mmd", "FIG-002"),
])
def test_one_byte_change_after_build_names_the_figure(tmp_path, target, figure):
    project = _pilot(tmp_path)
    docx = _fake_build(project)
    write_manifest(project / REL, "PilotHLD", docx)
    path = project / target
    raw = bytearray(path.read_bytes())
    raw[-2] = (raw[-2] + 1) % 256
    path.write_bytes(bytes(raw))
    result = CliRunner().invoke(main, ["diagrams", "verify-manifest", str(project / REL)])
    assert result.exit_code == 1
    assert f"{figure}: " in result.output and "VERIFY-MANIFEST: FAIL" in result.output


def test_manifest_edge_cases(tmp_path):
    project = _pilot(tmp_path)
    doc = project / REL
    assert build_manifest(doc, "Nothing", doc.parent / "x.docx") is None
    assert CliRunner().invoke(main, ["diagrams", "manifest", "--doc-dir", str(doc), "--name",
                                     "Nothing", "--docx", str(doc.parent / "x.docx")]).exit_code == 0
    assert CliRunner().invoke(main, ["diagrams", "verify-manifest", str(doc)]).exit_code == 2
    docx = _fake_build(project)
    out = write_manifest(doc, "PilotHLD", docx)
    assert find_manifests(out) == [out]
    data = json.loads(out.read_text(encoding="utf-8"))
    data["figures"][0]["validated_ir_sha256"] = "0" * 64
    out.write_text(json.dumps(data), encoding="utf-8")
    assert any("not the validated candidate" in p for p in verify(out))
    docx.unlink()
    assert any("PilotHLD.docx missing" in p for p in verify(out))


# -- end-to-end through build-doc.sh (skipped where the renderer is absent) ---------------

@pytest.mark.skipif(not _renderer_available(),
                    reason="local renderer, browser, font, pandoc or reference.docx absent")
def test_build_doc_pilot_end_to_end(tmp_path):
    project = _pilot(tmp_path)
    doc = project / REL
    bash = shutil.which("bash")

    def build():
        return subprocess.run([bash, "scripts/build-doc.sh", str(doc).replace("\\", "/"),
                               "PilotHLD"], capture_output=True, text=True,
                              env=dict(os.environ), cwd=ROOT)
    ok = build()
    assert ok.returncode == 0, ok.stderr
    runner = CliRunner()
    assert runner.invoke(main, ["diagrams", "verify-manifest", str(doc)]).exit_code == 0
    assert build().returncode == 0  # untouched rebuild verifies clean
    assert runner.invoke(main, ["diagrams", "verify-manifest", str(doc)]).exit_code == 0
    _bump(doc / "diagrams" / "context.ir.json")
    result = runner.invoke(main, ["diagrams", "verify-manifest", str(doc)])
    assert result.exit_code == 1 and "FIG-001" in result.output
    bad = build()
    assert bad.returncode != 0 and "diagram/candidate-not-validated" in bad.stderr
