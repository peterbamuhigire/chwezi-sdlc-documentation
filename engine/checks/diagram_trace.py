"""DiagramTraceCheck: requirement and closed-world checks on diagram IR.

Runs only when the project holds IR files (``**/diagrams/*.ir.json``), so
workspaces without IR are unaffected. Codes (severity in this first release):

* ``schema/<keyword>``, ``diagram/invalid-json``, ``diagram/duplicate-id``,
  ``diagram/duplicate-figure-id`` — the IR is malformed (HIGH);
* ``diagram/unknown-trace-id`` — a trace id whose prefix is not in
  ``engine.idscan.KIND_PREFIXES`` or that is absent from
  ``_registry/identifiers.yaml`` (HIGH);
* ``diagram/uncovered-requirement`` — an in-scope ``FR-`` registry entry that
  no IR element traces (MEDIUM, report-only; the ratchet to HIGH is an M10-14
  decision);
* ``diagram/unexpected-root`` / ``diagram/unexpected-terminal`` — a node with
  no incoming (outgoing) edge that is not an allowed root (terminal); applies
  to ``state`` and ``dataflow`` figures and to any figure that declares
  ``allowed_roots`` / ``allowed_terminals`` (HIGH);
* ``diagram/required-edge`` / ``diagram/required-path`` — a declared edge is
  absent / no directed path exists (breadth-first search) (HIGH);
* ``diagram/dead-end-state`` — a non-terminal state with no outgoing
  transition (HIGH);
* ``diagram/unmapped-sequence`` — a sequence figure that traces no FR which
  ``stimulus_response.py`` recognises as a stimulus-response requirement
  (MEDIUM);
* ``diagram/unknown-edge-endpoint`` — an edge ``from``/``to`` that is not a
  node of the figure (HIGH).

"In scope": ``_registry/identifiers.yaml`` has no scope or deferral field
(schema checked 29 Sep 2026: ``id``, ``kind``, ``defined_in``, ``title``,
``links``), so every ``FR`` entry is treated as in scope. When the registry
file is absent, the identifiers found in the project's Markdown (outside
``_generated/``) stand in for it and one INFO finding says so.

Limits, stated plainly: the coverage check proves that an FR is drawn
somewhere, not that the drawing is correct; the graph checks prove the
declared structure, not that the structure is the right design. Every fix
offered keeps the requirement and the semantic check (a repair may not delete
what failed).

Pattern adapted from Archify (MIT, https://github.com/tt-a1i/archify, commit
0e4949f910a8e390bd3b4933883a4dcabad571be). Paraphrased; no schema, code or
test text copied.
"""
from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Dict, List, Optional, Set

from engine.artifact_graph import ArtifactGraph
from engine.checks.stimulus_response import _FR as _SR_FR, _SHALL
from engine.diagram_ir import (
    GENERATED_DIR,
    NO_DELETION_GUARD,
    Diagnostic,
    DiagramIR,
    ir_files_by_doc,
    load_doc_irs,
)
from engine.findings import Finding, FindingCollection, Severity
from engine.idscan import KIND_PREFIXES, find_ids, kind_of
from engine.registry.identifiers import IdentifierRegistry

H, M = Severity.HIGH, Severity.MEDIUM


def _diag(ir: DiagramIR, code: str, severity: Severity, message: str, pointer: str,
          identity: str, evidence: dict, fixes: List[str]) -> Diagnostic:
    fixes = [f if NO_DELETION_GUARD in f else f"{f}, {NO_DELETION_GUARD}" for f in fixes]
    return Diagnostic(code=code, severity=severity, message=f"{ir.figure_id}: {message}",
                      subject={"figure_id": ir.figure_id, "path": pointer, "identity": identity},
                      evidence=evidence, supported_fixes=tuple(fixes), path=ir.path)


def _adjacency(ir: DiagramIR, node_ids: Set[str]) -> Dict[str, List[str]]:
    adj: Dict[str, List[str]] = {n: [] for n in node_ids}
    for e in ir.edges:
        if e.get("from") in node_ids and e.get("to") in node_ids:
            adj[e["from"]].append(e["to"])
    return adj


def _reachable(adj: Dict[str, List[str]], start: str, goal: str) -> bool:
    seen, queue = {start}, deque([start])
    while queue:
        cur = queue.popleft()
        if cur == goal:
            return True
        for nxt in adj.get(cur, []):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return False


_DEFAULT_ROOT_ROLES = {"state": {"start"}, "dataflow": {"external_entity", "store"}}
_DEFAULT_TERMINAL_ROLES = {"state": {"terminal"}, "dataflow": {"external_entity", "store"}}


def check_ir(ir: DiagramIR, registry_ids: Set[str], sr_frs: Set[str]) -> List[Diagnostic]:
    """Registry, endpoint, closed-world and sequence checks for one valid IR."""
    out: List[Diagnostic] = []
    nodes = ir.nodes
    node_ids = {n["id"] for n in nodes}
    roles = {n["id"]: n["role"] for n in nodes}

    # Trace ids: known prefix and present in the registry.
    for group, key in ((nodes, "nodes"), (ir.edges, "edges"), (ir.boundaries, "boundaries")):
        for i, el in enumerate(group):
            for j, tid in enumerate(el.get("trace", [])):
                if kind_of(tid) in KIND_PREFIXES and tid in registry_ids:
                    continue
                why = ("prefix not in engine.idscan.KIND_PREFIXES"
                       if kind_of(tid) not in KIND_PREFIXES
                       else "not in _registry/identifiers.yaml")
                out.append(_diag(
                    ir, "diagram/unknown-trace-id", H, f"trace id {tid} on '{el['id']}' is {why}",
                    f"/{key}/{i}/trace/{j}", el["id"], {"trace_id": tid, "reason": why},
                    [f"replace {tid} with the identifier the SRS defines for this element "
                     "(run `python -m engine sync <project>` to refresh the registry)",
                     "if the requirement is new, add it to the SRS and re-sync"]))

    # Edge endpoints.
    for i, e in enumerate(ir.edges):
        for end in ("from", "to"):
            if e.get(end) not in node_ids:
                out.append(_diag(
                    ir, "diagram/unknown-edge-endpoint", H,
                    f"edge '{e['id']}' {end} '{e.get(end)}' is not a node of this figure",
                    f"/edges/{i}/{end}", e["id"], {"endpoint": e.get(end), "side": end},
                    [f"point '{end}' of edge '{e['id']}' at an existing node id",
                     f"or add the missing node '{e.get(end)}'"]))

    adj = _adjacency(ir, node_ids)
    incoming = {n: 0 for n in node_ids}
    for src, dsts in adj.items():
        for d in dsts:
            incoming[d] += 1
    checks = ir.semantic_checks or {}

    # Roots.
    if ir.kind in _DEFAULT_ROOT_ROLES or "allowed_roots" in checks:
        allowed = set(checks.get("allowed_roots", [])) if "allowed_roots" in checks else {
            n for n, r in roles.items() if r in _DEFAULT_ROOT_ROLES.get(ir.kind, set())}
        for idx, n in enumerate(nodes):
            nid = n["id"]
            if incoming[nid] == 0 and nid not in allowed:
                out.append(_diag(
                    ir, "diagram/unexpected-root", H,
                    f"'{nid}' has no incoming edge but is not an allowed root",
                    f"/nodes/{idx}", nid, {"allowed_roots": sorted(allowed)},
                    [f"add the edge that leads into '{nid}'",
                     f"or declare '{nid}' in semantic_checks.allowed_roots if the SRS makes it an entry point"]))

    # Terminals (state figures report non-terminal dead ends separately).
    if ir.kind in _DEFAULT_TERMINAL_ROLES or "allowed_terminals" in checks:
        allowed = set(checks.get("allowed_terminals", [])) if "allowed_terminals" in checks else {
            n for n, r in roles.items() if r in _DEFAULT_TERMINAL_ROLES.get(ir.kind, set())}
        for idx, n in enumerate(nodes):
            nid = n["id"]
            if adj[nid] or nid in allowed:
                continue
            if ir.kind == "state" and roles[nid] != "terminal":
                continue  # reported as dead-end-state below
            out.append(_diag(
                ir, "diagram/unexpected-terminal", H,
                f"'{nid}' has no outgoing edge but is not an allowed terminal",
                f"/nodes/{idx}", nid, {"allowed_terminals": sorted(allowed)},
                [f"add the edge that leaves '{nid}'",
                 f"or declare '{nid}' in semantic_checks.allowed_terminals if the SRS ends the flow there"]))

    if ir.kind == "state":
        for idx, n in enumerate(nodes):
            if n["role"] != "terminal" and not adj[n["id"]]:
                out.append(_diag(
                    ir, "diagram/dead-end-state", H,
                    f"state '{n['id']}' is not terminal and has no outgoing transition",
                    f"/nodes/{idx}", n["id"], {"role": n["role"]},
                    [f"add the transition that leaves '{n['id']}' (from the SRS lifecycle rules)",
                     f"or mark '{n['id']}' as role 'terminal' if the SRS ends the lifecycle there"]))

    edge_pairs = {(e.get("from"), e.get("to")) for e in ir.edges}
    for i, req in enumerate(checks.get("required_edges", [])):
        if (req["from"], req["to"]) not in edge_pairs:
            out.append(_diag(
                ir, "diagram/required-edge", H,
                f"required edge {req['from']} -> {req['to']} is absent",
                f"/semantic_checks/required_edges/{i}", f"{req['from']}->{req['to']}", dict(req),
                [f"add an edge from '{req['from']}' to '{req['to']}'"]))
    for i, req in enumerate(checks.get("required_paths", [])):
        if not (req["from"] in adj and _reachable(adj, req["from"], req["to"])):
            out.append(_diag(
                ir, "diagram/required-path", H,
                f"no directed path from {req['from']} to {req['to']}",
                f"/semantic_checks/required_paths/{i}", f"{req['from']}->{req['to']}", dict(req),
                [f"add the missing step(s) so '{req['to']}' is reachable from '{req['from']}'"]))

    if ir.kind == "sequence":
        traced = {t for _, el in ir.elements() for t in el.get("trace", [])}
        if not traced & sr_frs:
            out.append(_diag(
                ir, "diagram/unmapped-sequence", M,
                "sequence figure traces no stimulus-response FR "
                "(an FR written as '**FR-nnn** ... shall ...')",
                "/meta", ir.figure_id, {"traced": sorted(traced)},
                ["add the FR whose stimulus-response pair this sequence realises to the trace "
                 "of the message that carries the stimulus"]))
    return out


def _is_generated(art) -> bool:
    return GENERATED_DIR in Path(art.path).parts


def registry_universe(root: Path, graph: ArtifactGraph) -> tuple[Set[str], bool]:
    """(known identifiers, True if read from the registry file)."""
    path = root / "_registry" / "identifiers.yaml"
    if path.exists():
        return {e.id for e in IdentifierRegistry.load(path)}, True
    ids: Set[str] = set()
    for art in graph.artifacts:
        if not _is_generated(art):
            ids |= find_ids(art.body)
    return ids, False


def stimulus_response_frs(graph: ArtifactGraph) -> Set[str]:
    """FR ids that StimulusResponseCheck reads as '**FR-nnn** ... shall ...'."""
    out: Set[str] = set()
    for art in graph.artifacts:
        if _is_generated(art):
            continue
        for line in art.body.splitlines():
            m = _SR_FR.search(line)
            if m and _SHALL.search(m.group(2)):
                out.add(m.group(1))
    return out


class DiagramTraceCheck:
    def __init__(self, gate_id: str, project_root: Optional[Path]) -> None:
        self.gate_id = gate_id
        self._root = Path(project_root) if project_root is not None else None

    def diagnostics(self, graph: ArtifactGraph) -> List[Diagnostic]:
        if self._root is None:
            return []
        groups = ir_files_by_doc(self._root)
        if not groups:
            return []
        known, _ = registry_universe(self._root, graph)
        sr_frs = stimulus_response_frs(graph)
        out: List[Diagnostic] = []
        traced: Set[str] = set()
        for doc_dir in sorted(groups):
            irs, diags = load_doc_irs(doc_dir)
            out.extend(diags)
            bad = {d.path for d in diags}
            for ir in irs:
                if ir.path in bad:
                    continue
                traced |= {t for _, el in ir.elements() for t in el.get("trace", [])}
                out.extend(check_ir(ir, known, sr_frs))
        for fr in sorted(i for i in known if kind_of(i) == "FR" and i not in traced):
            out.append(Diagnostic(
                code="diagram/uncovered-requirement", severity=M,
                message=f"{fr} appears on no diagram IR element in this project",
                subject={"figure_id": "", "path": "", "identity": fr},
                evidence={"requirement": fr},
                supported_fixes=(f"add {fr} to the trace of the element that realises it, "
                                 f"{NO_DELETION_GUARD}",),
                path=None))
        return out

    def run(self, graph: ArtifactGraph, findings: FindingCollection) -> None:
        if self._root is None or not ir_files_by_doc(self._root):
            return
        _, from_registry = registry_universe(self._root, graph)
        if not from_registry:
            findings.add(Finding(
                gate_id=self.gate_id, severity=Severity.INFO,
                message=("_registry/identifiers.yaml is absent; diagram trace ids were checked "
                         "against identifiers found in the project's Markdown"),
                location=None, line=None, code="diagram/registry-absent"))
        for d in self.diagnostics(graph):
            findings.add(d.to_finding(self.gate_id, self._root))
