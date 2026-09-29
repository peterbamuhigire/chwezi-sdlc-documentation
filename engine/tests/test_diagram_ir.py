"""M10-07-T01: diagram IR schema, loader and canonical form."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine import diagram_ir
from engine.diagram_ir import (
    canonical_json,
    find_ir_files,
    load_doc_irs,
    load_ir,
    read_validated,
    text_sha256,
    unvalidated,
    write_validated,
)
from engine.findings import Severity

FIX = Path(__file__).resolve().parent / "fixtures" / "diagram_ir"


@pytest.mark.parametrize("name", ["context", "sequence", "state"])
def test_valid_fixtures_validate(name):
    ir, diags = load_ir(FIX / "valid" / f"{name}.ir.json")
    assert diags == []
    assert ir is not None and ir.kind == name
    assert ir.figure_id.startswith("FIG-")


@pytest.mark.parametrize("name, code, pointer", [
    ("unknown-property", "schema/additionalProperties", "/nodes/1"),
    ("invalid-element-id", "schema/pattern", "/nodes/1/id"),
    ("malformed-trace-id", "schema/pattern", "/nodes/1/trace/0"),
    ("missing-alt-text", "schema/required", "/meta"),
])
def test_invalid_fixtures_fail_with_schema_code_and_pointer(name, code, pointer):
    _, diags = load_ir(FIX / "invalid" / f"{name}.ir.json")
    assert [d.code for d in diags] == [code]
    d = diags[0]
    assert d.severity == Severity.HIGH
    assert d.subject["path"] == pointer
    assert d.subject["figure_id"] == "FIG-003"
    assert d.supported_fixes
    finding = d.to_finding("phase03.diagram_trace")
    assert finding.code == code and finding.subject["path"] == pointer


def test_unknown_property_names_the_property():
    _, diags = load_ir(FIX / "invalid" / "unknown-property.ir.json")
    assert diags[0].evidence["unknown_properties"] == ["colour"]
    assert diags[0].subject["identity"] == "pending-reference-data"
    assert "remove unsupported property 'colour'" in diags[0].supported_fixes[0]


def _write(tmp_path: Path, data, name="x.ir.json") -> Path:
    p = tmp_path / "doc" / "diagrams" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")
    return p


def _state() -> dict:
    return json.loads((FIX / "valid" / "state.ir.json").read_text(encoding="utf-8"))


def test_invalid_json_and_duplicate_ids(tmp_path):
    ir, diags = load_ir(_write(tmp_path, "{not json"))
    assert ir is None and diags[0].code == "diagram/invalid-json"
    data = _state()
    data["edges"][0]["id"] = "draft"  # collides with a node id
    _, diags = load_ir(_write(tmp_path, data, "dup.ir.json"))
    assert [d.code for d in diags] == ["diagram/duplicate-id"]


def test_role_is_checked_per_kind_and_attributes_only_on_erd(tmp_path):
    data = _state()
    data["nodes"][0]["role"] = "person"
    data["nodes"][1]["attributes"] = [{"name": "id", "type": "INT", "key": "pk"}]
    _, diags = load_ir(_write(tmp_path, data))
    assert {d.code for d in diags} == {"schema/enum", "schema/not"}


@pytest.mark.parametrize("bad", ["../x.md", "/abs/x.md", "C:/x.md", "a\\b.md"])
def test_owner_document_must_be_portable(tmp_path, bad):
    data = _state()
    data["meta"]["owner_document"] = bad
    _, diags = load_ir(_write(tmp_path, data))
    assert diags and all(d.code == "schema/not" for d in diags)


def test_sequence_messages_need_order_and_kind(tmp_path):
    data = json.loads((FIX / "valid" / "sequence.ir.json").read_text(encoding="utf-8"))
    del data["edges"][0]["order"]
    _, diags = load_ir(_write(tmp_path, data))
    assert [d.code for d in diags] == ["schema/required"]


def test_canonical_json_and_crlf_insensitive_hash():
    assert canonical_json({"b": 1, "a": [2]}) == '{"a":[2],"b":1}'
    assert text_sha256(b"a\r\nb\n") == text_sha256(b"a\nb\n")
    assert text_sha256(b"a\nb\n") != text_sha256(b"a\nc\n")


def test_discovery_skips_generated_and_quarantine(tmp_path):
    good = _write(tmp_path, _state())
    for skip in ("_generated", ".trash-1", "node_modules"):
        q = tmp_path / skip / "diagrams" / "q.ir.json"
        q.parent.mkdir(parents=True)
        q.write_text("{}", encoding="utf-8")
    assert find_ir_files(tmp_path) == [good]
    assert diagram_ir.doc_dir_of(good) == tmp_path / "doc"


def test_candidate_freezing_round_trip(tmp_path):
    path = _write(tmp_path, _state())
    doc = tmp_path / "doc"
    irs, diags = load_doc_irs(doc)
    assert diags == []
    assert [d.code for d in unvalidated(doc, irs)] == ["diagram/candidate-not-validated"]
    write_validated(doc, irs)
    assert read_validated(doc)["FIG-003"]["ir_path"] == "diagrams/x.ir.json"
    assert unvalidated(doc, irs) == []
    path.write_bytes(path.read_bytes().replace(b"Draft", b"Drafts"))
    irs, _ = load_doc_irs(doc)
    assert [d.code for d in unvalidated(doc, irs)] == ["diagram/candidate-not-validated"]


def test_duplicate_figure_ids_in_one_document(tmp_path):
    _write(tmp_path, _state(), "a.ir.json")
    _write(tmp_path, _state(), "b.ir.json")
    _, diags = load_doc_irs(tmp_path / "doc")
    assert [d.code for d in diags] == ["diagram/duplicate-figure-id"]


def test_attribution_present():
    schema = json.loads(diagram_ir.SCHEMA_PATH.read_text(encoding="utf-8"))
    assert "0e4949f910a8e390bd3b4933883a4dcabad571be" in schema["$comment"]
    assert "0e4949f910a8e390bd3b4933883a4dcabad571be" in diagram_ir.__doc__
