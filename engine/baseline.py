"""Baseline snapshot and diff utilities.

M10-07-T07 (AR-07) adds diagram elements. A snapshot also records, for each
element of each diagram IR in the project, ``<figure-id>#<element-id>`` ->
(element hash, placement hash). The element hash is SHA-256 of the element's
canonical JSON without its placement fields (``boundary``, ``lane`` and a
sequence message's ``order``); the placement hash covers those fields only.
``diff`` then reports diagram elements as ``added``, ``removed``, ``changed``
(same id, different element hash) or ``moved`` (same element hash, different
placement). Entries live under a separate top-level ``diagram_elements`` key,
so snapshots written before this change still load. The delta reports what
changed; it infers no impact, risk or merge safety.

Stable-id delta pattern adapted from Archify (MIT,
https://github.com/tt-a1i/archify, commit
0e4949f910a8e390bd3b4933883a4dcabad571be). Paraphrased; no code copied.
"""
from __future__ import annotations
import hashlib
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Dict, Optional, Tuple
from ruamel.yaml import YAML
from engine.artifact_graph import Artifact, ArtifactGraph
from engine.idscan import find_ids

_yaml = YAML(typ="safe")


@dataclass(frozen=True)
class Snapshot:
    label: str
    created_on: date
    entries: Dict[str, str]  # id -> sha256
    # "<figure-id>#<element-id>" -> (element sha256, placement sha256)
    diagram_elements: Dict[str, Tuple[str, str]] = field(default_factory=dict)


PLACEMENT_FIELDS = ("boundary", "lane", "order")


def element_hashes(element: dict) -> Tuple[str, str]:
    """(element hash, placement hash) of one IR element."""
    from engine.diagram_ir import canonical_json
    core = {k: v for k, v in element.items() if k not in PLACEMENT_FIELDS}
    place = {k: element[k] for k in PLACEMENT_FIELDS if k in element}
    return (hashlib.sha256(canonical_json(core).encode("utf-8")).hexdigest(),
            hashlib.sha256(canonical_json(place).encode("utf-8")).hexdigest())


def diagram_snapshot(root: Optional[Path]) -> Dict[str, Tuple[str, str]]:
    """Element hashes for every valid diagram IR under ``root``."""
    from engine.diagram_ir import find_ir_files, load_ir
    out: Dict[str, Tuple[str, str]] = {}
    if root is None:
        return out
    for path in find_ir_files(root):
        ir, diags = load_ir(path)
        if ir is None or diags:
            continue  # invalid IR is reported by the diagram checks, not baselined
        for _, el in ir.elements():
            out[f"{ir.figure_id}#{el['id']}"] = element_hashes(el)
    return out


def _first_line_mentioning(ident: str, art: Artifact) -> str:
    # Match the id whether or not it is bold (module-prefixed IDs are often
    # unbolded), preferring a bold definition line when one exists.
    bold = f"**{ident}**"
    fallback = ""
    for line in art.body.splitlines():
        if bold in line:
            return line
        if not fallback and ident in line:
            fallback = line
    return fallback


def snapshot(graph: ArtifactGraph, label: str, today: date | None = None) -> Snapshot:
    today = today or date.today()
    entries: Dict[str, str] = {}
    for art in graph.artifacts:
        for ident in find_ids(art.body):
            if ident in entries:
                continue  # first artifact (build order) wins
            line = _first_line_mentioning(ident, art)
            h = hashlib.sha256(line.encode("utf-8")).hexdigest()
            entries[ident] = h
    return Snapshot(label=label, created_on=today, entries=entries,
                    diagram_elements=diagram_snapshot(graph.root))


def save_snapshot(snap: Snapshot, path: Path) -> None:
    data = {
        "label": snap.label,
        "created_on": snap.created_on.isoformat(),
        "entries": [{"id": k, "sha256": v} for k, v in sorted(snap.entries.items())],
    }
    if snap.diagram_elements:
        data["diagram_elements"] = [
            {"id": k, "element_sha256": e, "placement_sha256": p}
            for k, (e, p) in sorted(snap.diagram_elements.items())
        ]
    with path.open("w", encoding="utf-8") as f:
        _yaml.dump(data, f)


def load_snapshot(path: Path) -> Snapshot:
    data = _yaml.load(path.read_text(encoding="utf-8"))
    entries = {e["id"]: e["sha256"] for e in data.get("entries", [])}
    created = data["created_on"]
    if isinstance(created, str):
        created = date.fromisoformat(created)
    diagram = {
        e["id"]: (e["element_sha256"], e["placement_sha256"])
        for e in data.get("diagram_elements", []) or []
    }
    return Snapshot(
        label=data["label"],
        created_on=created,
        entries=entries,
        diagram_elements=diagram,
    )


def diff(old: Snapshot, new: Snapshot) -> dict:
    added = sorted(set(new.entries) - set(old.entries))
    removed = sorted(set(old.entries) - set(new.entries))
    modified = sorted(
        k for k in set(old.entries) & set(new.entries)
        if old.entries[k] != new.entries[k]
    )
    return {"added": added, "removed": removed, "modified": modified,
            "diagram": diagram_diff(old, new)}


def diagram_diff(old: Snapshot, new: Snapshot) -> dict:
    """Diagram elements added, removed, changed or moved between two snapshots."""
    o, n = old.diagram_elements, new.diagram_elements
    both = set(o) & set(n)
    return {
        "added": sorted(set(n) - set(o)),
        "removed": sorted(set(o) - set(n)),
        "changed": sorted(k for k in both if o[k][0] != n[k][0]),
        "moved": sorted(k for k in both if o[k][0] == n[k][0] and o[k][1] != n[k][1]),
    }
