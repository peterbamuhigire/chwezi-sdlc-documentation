"""Diagram intermediate representation (IR): load, validate, canonicalise.

An SRS or SDD figure is authored as a closed, typed JSON document
(``<doc-dir>/diagrams/<name>.ir.json``) validated against
``engine/registry/schemas/diagram-ir.schema.json`` (JSON Schema draft
2020-12). Mermaid text and the trace table are generated from it
(``engine/diagram_render.py``); requirement and semantic checks run on it
(``engine/checks/diagram_trace.py``).

Layout on disk, per document directory (the folder that ``build-doc.sh``
stitches)::

    <doc-dir>/diagrams/*.ir.json         authored IR (one figure per file)
    <doc-dir>/_generated/.validated.json IR hashes accepted by the last
                                         successful ``diagrams validate``
    <doc-dir>/_generated/<FIG-nnn>.mmd   generated Mermaid
    <doc-dir>/_generated/trace-table.md  generated trace table
    <doc-dir>/_generated/.generated.json IR and Mermaid hashes of the last
                                         ``diagrams generate``

A section file embeds a figure with the marker ``<!-- diagram-ir: FIG-001 -->``
and the trace table with ``<!-- diagram-ir: trace-table -->``;
``scripts/render_diagrams.py`` expands the markers at build time and refuses a
figure whose IR is not the validated candidate.

Schema diagnostics carry ``code`` ``schema/<keyword>``, a ``subject``
(``figure_id``, JSON-pointer ``path``, nearest element ``identity``), the
validator ``evidence`` and ``supported_fixes``.

Pattern adapted from Archify (MIT, https://github.com/tt-a1i/archify, commit
0e4949f910a8e390bd3b4933883a4dcabad571be). Paraphrased; no schema, code or
test text copied.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, List, Optional, Tuple

from jsonschema import Draft202012Validator

from engine.findings import Finding, Severity

SCHEMA_PATH = Path(__file__).parent / "registry" / "schemas" / "diagram-ir.schema.json"
IR_SUFFIX = ".ir.json"
DIAGRAMS_DIR = "diagrams"
GENERATED_DIR = "_generated"
VALIDATED_NAME = ".validated.json"
GENERATED_NAME = ".generated.json"
TRACE_TABLE_NAME = "trace-table.md"
_SKIP_PARTS = {"node_modules", GENERATED_DIR, ".git", "_figures"}

MARKER_RE = re.compile(
    r"^[ \t]*<!--\s*diagram-ir:\s*(?P<ref>FIG-[0-9]{3}|trace-table)\s*-->[ \t]*$",
    re.MULTILINE,
)

_SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
_VALIDATOR = Draft202012Validator(_SCHEMA)

# Guard wording required on every fix for a contract failure: a repair must
# not delete the requirement or the semantic check it failed.
NO_DELETION_GUARD = "without removing the requirement or the semantic check"


@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: Severity
    message: str
    subject: dict = field(default_factory=dict)
    evidence: dict = field(default_factory=dict)
    supported_fixes: Tuple[str, ...] = ()
    path: Optional[Path] = None

    def to_finding(self, gate_id: str, root: Optional[Path] = None) -> Finding:
        location = self.path
        if location is not None and root is not None:
            try:
                location = location.resolve().relative_to(root.resolve())
            except ValueError:
                pass
        return Finding(
            gate_id=gate_id,
            severity=self.severity,
            message=f"{self.code}: {self.message}",
            location=location,
            line=None,
            code=self.code,
            subject=dict(self.subject),
            evidence=dict(self.evidence),
            supported_fixes=tuple(self.supported_fixes),
        )


@dataclass(frozen=True)
class DiagramIR:
    path: Path
    data: dict
    sha256: str

    @property
    def figure_id(self) -> str:
        meta = self.data.get("meta") if isinstance(self.data, dict) else None
        fid = meta.get("figure_id") if isinstance(meta, dict) else None
        return fid if isinstance(fid, str) else self.path.name

    @property
    def kind(self) -> str:
        return str(self.data.get("diagram_kind", ""))

    @property
    def meta(self) -> dict:
        return self.data.get("meta", {})

    @property
    def nodes(self) -> List[dict]:
        return list(self.data.get("nodes", []))

    @property
    def edges(self) -> List[dict]:
        return list(self.data.get("edges", []))

    @property
    def boundaries(self) -> List[dict]:
        return list(self.data.get("boundaries", []))

    @property
    def semantic_checks(self) -> Optional[dict]:
        return self.data.get("semantic_checks")

    def elements(self) -> Iterable[Tuple[str, dict]]:
        """(element type, element) in canonical order: nodes, edges, boundaries."""
        for n in sorted(self.nodes, key=lambda x: x.get("id", "")):
            yield "node", n
        for e in sorted(self.edges, key=lambda x: (x.get("order", 0), x.get("id", ""))):
            yield "edge", e
        for b in sorted(self.boundaries, key=lambda x: x.get("id", "")):
            yield "boundary", b


def canonical_json(obj: Any) -> str:
    """Key-sorted, whitespace-free JSON used for element hashing."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def text_sha256(data: bytes) -> str:
    """SHA-256 of text with CRLF normalised to LF.

    IR, Mermaid and trace-table hashes use this so a Git checkout that
    converts line endings (``core.autocrlf``) does not look like an edit;
    any other one-byte change still changes the hash.
    """
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def text_sha256_file(path: Path) -> str:
    return text_sha256(Path(path).read_bytes())


def _pointer(parts: Iterable[Any]) -> str:
    out = []
    for p in parts:
        out.append(str(p).replace("~", "~0").replace("/", "~1"))
    return "/" + "/".join(out) if out else ""


def _identity(data: Any, parts: List[Any]) -> str:
    """Nearest element id (or figure id) on the path to the failing value."""
    found = ""
    cur = data
    if isinstance(data, dict) and isinstance(data.get("meta"), dict):
        fid = data["meta"].get("figure_id")
        found = fid if isinstance(fid, str) else ""
    for p in parts:
        try:
            cur = cur[p]
        except (KeyError, IndexError, TypeError):
            break
        if isinstance(cur, dict) and isinstance(cur.get("id"), str):
            found = cur["id"]
    return found


def _json_safe(value: Any) -> Any:
    try:
        json.dumps(value)
        return value
    except (TypeError, ValueError):
        return repr(value)


def _schema_fixes(error, unknown: List[str]) -> Tuple[str, ...]:
    kw = error.validator
    where = _pointer(error.absolute_path) or "/"
    if kw == "additionalProperties":
        return tuple(f"remove unsupported property '{u}' at {where}" for u in unknown) or (
            f"remove the unsupported property at {where}",)
    if kw == "required":
        return (f"add the missing required property at {where}; do not delete the element "
                "to silence the error",)
    if kw == "pattern":
        return (f"rewrite the value at {where} to match {error.validator_value}",)
    if kw in ("enum", "const"):
        return (f"use one of the allowed values at {where}: {error.validator_value}",)
    if kw in ("minLength", "maxLength", "minItems", "minimum"):
        return (f"change the value at {where} to satisfy {kw}={error.validator_value}",)
    return (f"correct the value at {where} so it satisfies '{kw}'",)


def schema_diagnostics(data: Any, path: Optional[Path] = None) -> List[Diagnostic]:
    """Schema failures as ``schema/<keyword>`` diagnostics, in document order."""
    figure_id = ""
    if isinstance(data, dict) and isinstance(data.get("meta"), dict):
        fid = data["meta"].get("figure_id")
        figure_id = fid if isinstance(fid, str) else ""
    out: List[Diagnostic] = []
    errors = sorted(_VALIDATOR.iter_errors(data),
                    key=lambda e: (_pointer(e.absolute_path), e.validator))
    for err in errors:
        parts = list(err.absolute_path)
        unknown: List[str] = []
        if err.validator == "additionalProperties" and isinstance(err.instance, dict):
            allowed = set((err.schema.get("properties") or {}).keys())
            unknown = sorted(k for k in err.instance if k not in allowed)
        evidence = {"keyword": err.validator,
                    "expected": _json_safe(err.validator_value),
                    "schema_path": _pointer(err.absolute_schema_path)}
        if unknown:
            evidence["unknown_properties"] = unknown
        elif not isinstance(err.instance, (dict, list)):
            evidence["actual"] = _json_safe(err.instance)
        out.append(Diagnostic(
            code=f"schema/{err.validator}",
            severity=Severity.HIGH,
            message=f"{figure_id or (path.name if path else 'IR')} {_pointer(parts) or '/'}: {err.message}",
            subject={"figure_id": figure_id, "path": _pointer(parts),
                     "identity": _identity(data, parts)},
            evidence=evidence,
            supported_fixes=_schema_fixes(err, unknown),
            path=path,
        ))
    return out


def structural_diagnostics(ir: DiagramIR) -> List[Diagnostic]:
    """Rules the schema cannot express: element ids unique within a figure."""
    seen: dict = {}
    out: List[Diagnostic] = []
    for kind, group in (("node", ir.nodes), ("edge", ir.edges), ("boundary", ir.boundaries)):
        for idx, el in enumerate(group):
            eid = el.get("id")
            ptr = f"/{kind}s/{idx}/id" if kind != "boundary" else f"/boundaries/{idx}/id"
            if eid in seen:
                out.append(Diagnostic(
                    code="diagram/duplicate-id", severity=Severity.HIGH,
                    message=f"{ir.figure_id}: element id '{eid}' is used more than once",
                    subject={"figure_id": ir.figure_id, "path": ptr, "identity": eid},
                    evidence={"first": seen[eid], "again": ptr},
                    supported_fixes=(f"rename one of the elements called '{eid}' and update "
                                     "every edge and check that refers to it",),
                    path=ir.path))
            else:
                seen[eid] = ptr
    return out


def load_ir(path: Path) -> Tuple[Optional[DiagramIR], List[Diagnostic]]:
    """Read and validate one IR file. Returns (IR or None, diagnostics)."""
    raw = path.read_bytes()
    try:
        data = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, ValueError) as exc:
        return None, [Diagnostic(
            code="diagram/invalid-json", severity=Severity.HIGH,
            message=f"{path.name} is not valid UTF-8 JSON: {exc}",
            subject={"figure_id": "", "path": "", "identity": path.name},
            evidence={"error": str(exc)},
            supported_fixes=("repair the JSON syntax; keep every element and trace",),
            path=path)]
    diags = schema_diagnostics(data, path)
    ir = DiagramIR(path=path, data=data if isinstance(data, dict) else {}, sha256=text_sha256(raw))
    if isinstance(data, dict) and not diags:
        diags.extend(structural_diagnostics(ir))
    return ir, diags


def is_valid(data: Any) -> bool:
    return not any(True for _ in _VALIDATOR.iter_errors(data))


# -- discovery ------------------------------------------------------------------

def _skipped(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        parts = path.parts
    return any(p in _SKIP_PARTS or p.startswith(".trash-") for p in parts[:-1])


def find_ir_files(root: Path) -> List[Path]:
    """Every ``diagrams/*.ir.json`` under ``root`` (quarantine and output dirs skipped)."""
    root = Path(root)
    out = []
    for p in sorted(root.rglob(f"{DIAGRAMS_DIR}/*{IR_SUFFIX}")):
        if p.is_file() and not _skipped(p, root):
            out.append(p)
    return out


def doc_dir_of(ir_path: Path) -> Path:
    """The document directory that owns an IR file (parent of ``diagrams/``)."""
    return ir_path.parent.parent


def ir_files_by_doc(root: Path) -> dict:
    groups: dict = {}
    for p in find_ir_files(root):
        groups.setdefault(doc_dir_of(p), []).append(p)
    return groups


# -- candidate freezing -----------------------------------------------------------

def _read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def read_validated(doc_dir: Path) -> dict:
    """figure_id -> {ir_path, ir_sha256} accepted by the last ``diagrams validate``."""
    data = _read_json(Path(doc_dir) / GENERATED_DIR / VALIDATED_NAME)
    figs = data.get("figures", {})
    return figs if isinstance(figs, dict) else {}


def write_validated(doc_dir: Path, irs: List[DiagramIR]) -> Path:
    out_dir = Path(doc_dir) / GENERATED_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    figures = {
        ir.figure_id: {"ir_path": ir.path.relative_to(doc_dir).as_posix(),
                       "ir_sha256": ir.sha256}
        for ir in sorted(irs, key=lambda i: i.figure_id)
    }
    path = out_dir / VALIDATED_NAME
    path.write_text(json.dumps({"schema": "srs-diagram-validated/1",
                                "note": "Written by `python -m engine diagrams validate`; "
                                        "do not edit.",
                                "figures": figures}, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8", newline="\n")
    return path


def read_generated(doc_dir: Path) -> dict:
    data = _read_json(Path(doc_dir) / GENERATED_DIR / GENERATED_NAME)
    figs = data.get("figures", {})
    return figs if isinstance(figs, dict) else {}


def candidate_diagnostic(ir: DiagramIR, recorded: Optional[str]) -> Diagnostic:
    return Diagnostic(
        code="diagram/candidate-not-validated", severity=Severity.HIGH,
        message=(f"{ir.figure_id}: IR {ir.path.name} (sha256 {ir.sha256[:12]}…) is not the "
                 f"candidate accepted by the last `diagrams validate` "
                 f"({(recorded or 'none')[:12]}…)"),
        subject={"figure_id": ir.figure_id, "path": "", "identity": ir.path.name},
        evidence={"ir_sha256": ir.sha256, "validated_ir_sha256": recorded},
        supported_fixes=("run `python -m engine diagrams validate <project> --doc <dir>` and fix "
                         "its findings, then generate again",),
        path=ir.path)


def unvalidated(doc_dir: Path, irs: List[DiagramIR]) -> List[Diagnostic]:
    """Candidate freezing: IRs whose current hash differs from the validated one."""
    recorded = read_validated(doc_dir)
    out = []
    for ir in irs:
        rec = recorded.get(ir.figure_id, {})
        if rec.get("ir_sha256") != ir.sha256:
            out.append(candidate_diagnostic(ir, rec.get("ir_sha256")))
    return out


def load_doc_irs(doc_dir: Path) -> Tuple[List[DiagramIR], List[Diagnostic]]:
    irs: List[DiagramIR] = []
    diags: List[Diagnostic] = []
    for p in sorted((Path(doc_dir) / DIAGRAMS_DIR).glob(f"*{IR_SUFFIX}")):
        ir, d = load_ir(p)
        diags.extend(d)
        if ir is not None:
            irs.append(ir)
    seen: dict = {}
    for ir in irs:
        if ir.figure_id in seen:
            diags.append(Diagnostic(
                code="diagram/duplicate-figure-id", severity=Severity.HIGH,
                message=(f"figure id {ir.figure_id} is used by both {seen[ir.figure_id]} and "
                         f"{ir.path.name}"),
                subject={"figure_id": ir.figure_id, "path": "/meta/figure_id",
                         "identity": ir.path.name},
                evidence={"files": [seen[ir.figure_id], ir.path.name]},
                supported_fixes=("give each figure in a document its own FIG-nnn id",),
                path=ir.path))
        else:
            seen[ir.figure_id] = ir.path.name
    return irs, diags


# -- figure provider (engine/figures.py FIGURE_PROVIDERS) --------------------------

def ir_figures(art, root: Optional[Path]):
    """Figures embedded by ``<!-- diagram-ir: FIG-nnn -->`` markers.

    A marker counts as a figure only when the IR exists in the document's
    ``diagrams/`` folder and its current hash is the one recorded by the last
    successful ``diagrams validate`` (valid IR; completes M10-01 AR-03).
    """
    from engine.figures import Figure  # local import: figures imports this module lazily
    if root is None:
        return []
    refs = [m.group("ref") for m in MARKER_RE.finditer(art.body) if m.group("ref") != "trace-table"]
    if not refs:
        return []
    doc_dir = (Path(root) / art.path).parent
    recorded = read_validated(doc_dir)
    by_id: dict = {}
    for p in sorted((doc_dir / DIAGRAMS_DIR).glob(f"*{IR_SUFFIX}")):
        ir, diags = load_ir(p)
        if ir is not None and not diags:
            by_id[ir.figure_id] = ir
    out = []
    for ref in refs:
        ir = by_id.get(ref)
        if ir is None or recorded.get(ref, {}).get("ir_sha256") != ir.sha256:
            continue
        meta = ir.meta
        label = " ".join(str(meta.get(k, "")) for k in ("title", "caption", "alt_text"))
        out.append(Figure(label=label, target=ir.path.relative_to(root).as_posix(),
                          kind="diagram-ir"))
    return out
