"""M10-07-T02: IR -> Mermaid and trace table; `diagrams generate`."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from engine.cli import main
from engine.diagram_ir import DiagramIR, load_ir
from engine.diagram_render import DIAGRAM_FONT_STACK, generate, to_mermaid, trace_table

ROOT = Path(__file__).resolve().parents[2]
FIX = Path(__file__).resolve().parent / "fixtures"
PILOT = FIX / "healthcare_admissions"
HLD = PILOT / "03-design-documentation" / "01-high-level-design"
GOLDEN = FIX / "diagram_ir" / "golden" / "healthcare-trace-table.md"


def _pilot_copy(tmp_path: Path) -> Path:
    dst = tmp_path / "ha"
    shutil.copytree(PILOT, dst, ignore=shutil.ignore_patterns("_figures", "*.docx", "*.figures.json"))
    return dst


def _shas(folder: Path) -> dict:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.iterdir()) if p.is_file()}


def test_trace_table_matches_golden_byte_for_byte(tmp_path):
    irs = [load_ir(p)[0] for p in sorted((HLD / "diagrams").glob("*.ir.json"))]
    assert trace_table(irs).encode("utf-8") == GOLDEN.read_bytes().replace(b"\r\n", b"\n")


def test_generate_is_deterministic_and_font_directive_first(tmp_path):
    project = _pilot_copy(tmp_path)
    runner = CliRunner()
    assert runner.invoke(main, ["diagrams", "validate", str(project)]).exit_code == 0
    first = runner.invoke(main, ["diagrams", "generate", str(project)])
    assert first.exit_code == 0, first.output
    out = project / "03-design-documentation" / "01-high-level-design" / "_generated"
    shas1 = _shas(out)
    assert runner.invoke(main, ["diagrams", "generate", str(project)]).exit_code == 0
    assert _shas(out) == shas1
    mmds = sorted(out.glob("*.mmd"))
    assert [m.name for m in mmds] == ["FIG-001.mmd", "FIG-002.mmd", "FIG-003.mmd"]
    for m in mmds:
        first_line = m.read_text(encoding="utf-8").splitlines()[0]
        assert first_line.startswith("%%{init: ") and first_line.endswith("}%%")
        init = json.loads(first_line[len("%%{init: "):-len("}%%")])
        assert init["themeVariables"]["fontFamily"] == DIAGRAM_FONT_STACK
    assert (out / "trace-table.md").read_bytes() == GOLDEN.read_bytes().replace(b"\r\n", b"\n")


def test_font_stack_matches_renderer_config_and_is_unquoted():
    cfg = json.loads((ROOT / "scripts" / "diagram-render" / "render-config.json").read_text("utf-8"))
    assert DIAGRAM_FONT_STACK == f"{cfg['diagram_font_family']}, {cfg['diagram_font_fallback']}"
    assert '"' not in DIAGRAM_FONT_STACK and "'" not in DIAGRAM_FONT_STACK


def _ir(kind: str, nodes, edges, boundaries=None) -> DiagramIR:
    data = {"diagram_kind": kind, "meta": {"figure_id": "FIG-009"}, "nodes": nodes, "edges": edges}
    if boundaries:
        data["boundaries"] = boundaries
    return DiagramIR(path=Path("x.ir.json"), data=data, sha256="0")


def test_mermaid_emitters_escape_and_shape():
    flow = to_mermaid(_ir(
        "component",
        [{"id": "api-gw", "label": 'API; "edge" #1', "role": "component", "boundary": "core"},
         {"id": "db", "label": "Store", "role": "datastore", "boundary": "missing"},
         {"id": "q", "label": "Queue", "role": "queue"}],
        [{"id": "e1", "from": "api-gw", "to": "db", "kind": "async", "label": "a|b"},
         {"id": "e2", "from": "api-gw", "to": "ghost"}],
        [{"id": "core", "label": "Core"}]))
    assert 'subgraph b_core["Core"]' in flow
    assert 'n_api_gw["API#59; #quot;edge#quot; #35;1"]' in flow
    assert 'n_db[("Store")]' in flow and 'n_q>"Queue"]' in flow
    assert 'n_api_gw -.->|"a#124;b"| n_db' in flow
    assert "ghost" not in flow
    erd = to_mermaid(_ir(
        "erd",
        [{"id": "patient", "label": "Patient", "role": "entity",
          "attributes": [{"name": "id", "type": "BIGINT", "key": "pk"},
                         {"name": "ward_id", "type": "INT", "key": "fk"},
                         {"name": "name", "type": "TEXT", "key": "none"}]},
         {"id": "ward", "label": "Ward", "role": "entity"}],
        [{"id": "in", "from": "ward", "to": "patient", "cardinality": "0..1:N", "label": "holds"}]))
    assert "BIGINT id PK" in erd and "INT ward_id FK" in erd and "TEXT name\n" in erd
    assert 'WARD |o--o{ PATIENT : "holds"' in erd
    seq = to_mermaid(_ir("sequence",
                         [{"id": "a", "label": "A", "role": "participant"},
                          {"id": "b", "label": "B", "role": "participant"}],
                         [{"id": "m2", "from": "b", "to": "a", "kind": "async", "order": 2, "label": "later"},
                          {"id": "m1", "from": "a", "to": "b", "kind": "sync", "order": 1, "label": "first"}]))
    assert seq.index("p_a->>p_b: first") < seq.index("p_b-)p_a: later")


def test_mermaid_id_collision_is_refused():
    with pytest.raises(ValueError):
        to_mermaid(_ir("context", [{"id": "a-b", "label": "x", "role": "system"},
                                   {"id": "a_b", "label": "y", "role": "system"}], []))


def test_generate_refuses_invalid_or_unvalidated_ir(tmp_path):
    project = _pilot_copy(tmp_path)
    doc = project / "03-design-documentation" / "01-high-level-design"
    ir_path = doc / "diagrams" / "context.ir.json"
    ir_path.write_bytes(ir_path.read_bytes().replace(b"Billing system", b"Billing systems"))
    result = CliRunner().invoke(main, ["diagrams", "generate", str(project)])
    assert result.exit_code != 0
    assert "diagram/candidate-not-validated" in result.output
    written, diags = generate(doc)
    assert written == {} and [d.code for d in diags] == ["diagram/candidate-not-validated"]
    ir_path.write_text("{}", encoding="utf-8")
    written, diags = generate(doc)
    assert written == {} and diags and all(d.code.startswith("schema/") for d in diags)


def test_cli_reports_missing_ir(tmp_path):
    (tmp_path / "_context").mkdir()
    for cmd in ("validate", "generate"):
        result = CliRunner().invoke(main, ["diagrams", cmd, str(tmp_path)])
        assert result.exit_code == 2 and "No diagram IR" in result.output
