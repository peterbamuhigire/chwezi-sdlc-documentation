"""Read-only lexical search over the domain control registers (M10-08-T10, UX-10).

Searches ``domains/*/controls/control-register.yaml`` so a drafting skill can
find the anchored control for a requirement and cite its ID and registry path
instead of paraphrasing it. Ranking is BM25 (k1 = 1.5, b = 0.75, the standard
values) over the fields ``id``, ``title``, ``category``, ``minimum_evidence``,
``regulatory_anchor.framework``, ``regulatory_anchor.clause`` and the domain
name. When the best score falls below ``ABSTAIN_THRESHOLD`` the search
abstains and returns no results, so a query with no genuine match never
produces a confident-looking control.

The threshold was calibrated on the 12-query fixture in
``engine/tests/fixtures/controls_search_queries.json`` (six positives, six
nonsense queries); see that file for the recorded score margins.

Abstaining lexical retrieval pattern adapted from UI UX Pro Max (MIT,
https://github.com/nextlevelbuilder/ui-ux-pro-max-skill, commit
09170eec67eefd46a7ae85de61b40c194020f997). No data reused. Paraphrased; no
code copied.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from ruamel.yaml import YAML

K1 = 1.5
B = 0.75
# Calibrated on the 12-query fixture: highest nonsense score 4.447
# ("annual football tournament schedule"), lowest positive top score 7.016
# ("cardholder encryption"). 5.5 sits inside that gap. Known limit: a
# single-word query scores roughly 3-5 and may abstain; add a second term.
ABSTAIN_THRESHOLD = 5.5

_TOKEN = re.compile(r"[a-z0-9]+")
_STOP = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is",
    "it", "no", "not", "of", "on", "or", "the", "to", "with", "within", "any",
    "all", "each", "every", "must", "shall", "should", "data", "system",
}
# Small synonym map kept in the module: each query token also searches its
# listed equivalents (a query term never gains weight from its own synonyms).
SYNONYMS: Dict[str, tuple[str, ...]] = {
    "cardholder": ("pan", "card"),
    "pan": ("cardholder", "card"),
    "card": ("cardholder", "pan"),
    "encryption": ("encrypt", "cryptography", "cryptographic", "unreadable"),
    "encrypt": ("encryption", "cryptography", "cryptographic"),
    "crypto": ("cryptography", "cryptographic", "encryption"),
    "health": ("phi", "hipaa"),
    "patient": ("phi",),
    "regulator": ("pdpo",),
    "office": ("pdpo",),
    "protection": ("dppa", "pdpo"),
    "logging": ("audit", "log"),
    "log": ("audit", "logging"),
    "erasure": ("deletion", "delete", "erase"),
    "delete": ("erasure", "deletion"),
    "consent": ("lawful", "basis"),
    "privacy": ("dppa", "gdpr", "personal"),
    "sod": ("segregation", "duties"),
}


def tokenise(text: str) -> List[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in _STOP]


@dataclass(frozen=True)
class Control:
    id: str
    title: str
    domain: str
    framework: str
    clause: str
    registry_path: str
    tokens: tuple[str, ...]


def load_controls(root: Path) -> List[Control]:
    yaml = YAML(typ="safe")
    out: List[Control] = []
    for reg in sorted(root.glob("domains/*/controls/control-register.yaml")):
        data = yaml.load(reg.read_text(encoding="utf-8")) or {}
        domain = str(data.get("domain") or reg.parent.parent.name)
        for c in data.get("controls") or []:
            anchor = c.get("regulatory_anchor") or {}
            fields = [c.get("id", ""), c.get("title", ""), c.get("category", ""),
                      *(c.get("minimum_evidence") or []),
                      anchor.get("framework", ""), str(anchor.get("clause", "")), domain]
            out.append(Control(
                id=str(c.get("id", "")), title=str(c.get("title", "")), domain=domain,
                framework=str(anchor.get("framework", "")), clause=str(anchor.get("clause", "")),
                registry_path=reg.relative_to(root).as_posix(),
                tokens=tuple(tokenise(" ".join(str(f) for f in fields))),
            ))
    return out


def _bm25(query: List[str], docs: List[Control]) -> List[float]:
    n = len(docs)
    avgdl = sum(len(d.tokens) for d in docs) / n if n else 0.0
    df: Dict[str, int] = {}
    for d in docs:
        for t in set(d.tokens):
            df[t] = df.get(t, 0) + 1
    scores = []
    for d in docs:
        tf: Dict[str, int] = {}
        for t in d.tokens:
            tf[t] = tf.get(t, 0) + 1
        score = 0.0
        for q in query:
            # A query term counts once: its best-scoring form among itself and synonyms.
            best = 0.0
            for form in (q, *SYNONYMS.get(q, ())):
                f = tf.get(form, 0)
                if not f:
                    continue
                idf = math.log(1 + (n - df[form] + 0.5) / (df[form] + 0.5))
                best = max(best, idf * f * (K1 + 1) / (f + K1 * (1 - B + B * len(d.tokens) / avgdl)))
            score += best
        scores.append(score)
    return scores


def search(query: str, *, root: Path, domain: Optional[str] = None,
           framework: Optional[str] = None, top: int = 5,
           threshold: float = ABSTAIN_THRESHOLD) -> dict:
    """Rank controls for ``query``. IDF is computed over the whole corpus so
    scores (and the abstention threshold) do not shift with the filters."""
    controls = load_controls(root)
    scores = _bm25(tokenise(query), controls)
    hits = [
        (s, c) for s, c in zip(scores, controls)
        if s > 0
        and (domain is None or c.domain.lower() == domain.lower())
        and (framework is None or framework.lower() in c.framework.lower())
    ]
    hits.sort(key=lambda sc: (-sc[0], sc[1].id))
    best = hits[0][0] if hits else 0.0
    abstained = best < threshold
    results = [] if abstained else [
        {"id": c.id, "title": c.title, "domain": c.domain, "framework": c.framework,
         "clause": c.clause, "score": round(s, 3), "registry_path": c.registry_path}
        for s, c in hits[:top]
    ]
    return {"query": query, "domain": domain, "framework": framework,
            "abstained": abstained, "best_score": round(best, 3),
            "threshold": threshold, "results": results}
