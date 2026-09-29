"""Figure evidence shared by the phase gates.

A diagram counts as a figure only when a reader of the delivered document
would see a picture:

* a Markdown image reference whose target file exists, or
* a fenced ``mermaid`` block whose rendering is recorded in a
  ``_figures/render-manifest.json`` written by ``scripts/render_diagrams.py``
  (same source-block SHA-256, and the rendered PNG still exists).

A Mermaid code block on its own is source, not a figure.

Extension point: ``FIGURE_PROVIDERS`` holds extra callables with the
signature ``provider(artifact, root) -> list[Figure]``. M10-07 (AR-03
completion) registers the diagram-IR sidecar provider here, so a valid IR
sidecar can satisfy the same gates without changing them.

The render-receipt idea is adapted from tt-a1i/archify (MIT,
https://github.com/tt-a1i/archify, commit
0e4949f910a8e390bd3b4933883a4dcabad571be), paraphrased.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

MANIFEST_NAME = "render-manifest.json"
FIGURES_DIR = "_figures"

# ```mermaid or ~~~mermaid (optionally {.mermaid}) ... closing fence
MERMAID_BLOCK_RE = re.compile(
    r"^(?P<indent>[ ]{0,3})(?P<fence>`{3,}|~{3,})[ \t]*\{?\.?mermaid\}?[ \t]*\n"
    r"(?P<code>.*?)"
    r"^(?P=indent)(?P=fence)[ \t]*$",
    re.MULTILINE | re.DOTALL,
)
IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<target>[^)\s]+)(?:\s+\"[^\"]*\")?\)")


@dataclass(frozen=True)
class Figure:
    label: str          # alt text / caption / block text used for topic matching
    target: str         # image path or rendered PNG path
    kind: str           # "image" | "rendered-mermaid" | provider-defined


def block_sha256(code: str) -> str:
    """Stable hash of a Mermaid block body (line endings normalised)."""
    norm = code.replace("\r\n", "\n").strip("\n")
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


def mermaid_blocks(body: str) -> List[str]:
    return [m.group("code") for m in MERMAID_BLOCK_RE.finditer(body)]


def _is_remote(target: str) -> bool:
    return bool(re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE)) and not re.match(
        r"^[a-z]:[\\/]", target, re.IGNORECASE
    )


def image_figures(art, root: Optional[Path]) -> List[Figure]:
    """Image references in ``art`` whose target exists on disk."""
    if root is None:
        return []
    out: List[Figure] = []
    base = (root / art.path).parent
    for m in IMAGE_RE.finditer(art.body):
        target = m.group("target").split("#", 1)[0]
        if not target or _is_remote(target):
            continue
        candidate = Path(target)
        paths = [candidate] if candidate.is_absolute() else [base / candidate, root / candidate]
        if any(p.is_file() for p in paths):
            out.append(Figure(label=f"{m.group('alt')} {target}", target=target, kind="image"))
    return out


ManifestIndex = Dict[str, List[Tuple[Path, dict]]]


def load_manifest_index(root: Path) -> Dict[str, List[Tuple[Path, dict]]]:
    """Map source-file absolute path -> [(manifest dir, figure entry)]."""
    index: Dict[str, List[Tuple[Path, dict]]] = {}
    for manifest in sorted(root.rglob(f"{FIGURES_DIR}/{MANIFEST_NAME}")):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        documents = data.get("documents", {}) if isinstance(data, dict) else {}
        for doc in documents.values():
            for fig in doc.get("figures", []) if isinstance(doc, dict) else []:
                src = fig.get("source")
                if not isinstance(src, str):
                    continue
                key = str((manifest.parent / src).resolve())
                index.setdefault(key, []).append((manifest.parent, fig))
    return index


def rendered_figures(art, root: Optional[Path],
                     index: Optional[ManifestIndex] = None) -> List[Figure]:
    """Mermaid blocks in ``art`` with a recorded, still-present rendering."""
    if root is None:
        return []
    blocks = mermaid_blocks(art.body)
    if not blocks:
        return []
    if index is None:
        index = load_manifest_index(root)
    entries = index.get(str((root / art.path).resolve()), [])
    if not entries:
        return []
    out: List[Figure] = []
    for code in blocks:
        sha = block_sha256(code)
        for fig_dir, fig in entries:
            if fig.get("source_sha256") != sha:
                continue
            png = fig.get("png")
            if isinstance(png, str) and (fig_dir / png).is_file():
                label = " ".join(str(fig.get(k, "")) for k in ("caption", "alt"))
                out.append(Figure(label=f"{label} {code}", target=png, kind="rendered-mermaid"))
                break
    return out


FigureProvider = Callable[[object, Optional[Path]], List[Figure]]


def _diagram_ir_figures(art, root: Optional[Path]) -> List[Figure]:
    """Validated diagram-IR figures (M10-07, AR-03 completion); see engine/diagram_ir.py."""
    from engine.diagram_ir import ir_figures
    return ir_figures(art, root)


# M10-07 registers the diagram-IR provider: a ``<!-- diagram-ir: FIG-nnn -->``
# marker whose IR is the validated candidate counts as a figure.
FIGURE_PROVIDERS: List[FigureProvider] = [_diagram_ir_figures]


def figures_in(art, root: Optional[Path],
               index: Optional[ManifestIndex] = None) -> List[Figure]:
    """Every figure a reader would see for ``art`` (see module docstring)."""
    figs = image_figures(art, root) + rendered_figures(art, root, index)
    for provider in FIGURE_PROVIDERS:
        figs.extend(provider(art, root))
    return figs
