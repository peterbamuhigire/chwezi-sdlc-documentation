"""Module-aware identifier scanning.

This is the single source of truth for recognizing project identifiers in
artifact text. It deliberately supports **module-prefixed** IDs (``FR-COOP-011``,
``NFR-PLAT-002``, ``CTRL-HC-001``) in addition to the classic single-segment
form (``FR-001``), and it matches IDs whether or not they are wrapped in bold
(``**FR-001**``).

It is intentionally NOT used by ``ArtifactGraph.all_identifiers()`` — that
narrow, bold-only surface still feeds the traceability / design-sufficiency /
phaseNN gates, whose line-level heuristics are calibrated for the classic form.
Broadening those would change validation semantics for every project. Instead,
this scanner powers only the three places that benefit from a content-bearing,
module-aware view: ``sync`` (registry population), the identifier-registry
check, and ``baseline`` snapshotting.

Prefix recognition is an **allowlist**: over-matching would turn tokens like
``AES-256`` / ``SHA-256`` / ``ISO-27001`` into phantom identifiers and break
projects, whereas under-matching is harmless (an unrecognized prefix is simply
left untracked, exactly as before this module existed). To track a new prefix,
add it to ``KIND_PREFIXES``.
"""
from __future__ import annotations
import re
from typing import Iterator, NamedTuple

# Curated allowlist of genuine SDLC / requirements identifier prefixes.
# Derived from the actual prefixes in use across the project corpus; excludes
# crypto/standard/measurement tokens (AES, SHA, ISO, IEC, RFC, ...) on purpose.
KIND_PREFIXES: frozenset[str] = frozenset({
    "FR", "NFR", "BG", "US", "TC", "BR", "DC", "GAP", "SP", "STK",
    "CTRL", "RISK", "ADR", "PBI", "CIA", "WAIVE", "OD", "FT", "MAC",
    "EP", "INC", "REC", "OBJ", "MP", "CR", "DEP", "REM", "MNT",
    "EI",  # external-interface ids (M10-08 hand-off from the M10-07 GarageFlow dry run)
})

# Longest-first so the alternation prefers e.g. NFR over a hypothetical NF.
_PREFIX_ALT = "|".join(sorted(KIND_PREFIXES, key=len, reverse=True))

# (optional bold) PREFIX (optional -SEGMENT...) -SEGMENTNUMBER (optional bold)
# Boundaries reject IDs glued to surrounding word characters or hyphens, so
# `AES-256` inside `AES-256-GCM` cannot masquerade (AES is not allowlisted) and
# `XFR-001` is not read as `FR-001`.
_ID_RE = re.compile(
    r"(?<![A-Za-z0-9-])"
    r"(?P<b1>\*\*)?"
    r"(?P<id>(?:" + _PREFIX_ALT + r")(?:-[A-Z0-9]{1,8})*-\d{3,5})"
    r"(?P<b2>\*\*)?"
    r"(?![A-Za-z0-9-])"
)


class IdHit(NamedTuple):
    id: str
    bold: bool
    trailing: str  # text after the id on the same line (used for titles)


def scan_line(line: str) -> Iterator[IdHit]:
    """Yield every identifier hit on a single line of text."""
    for m in _ID_RE.finditer(line):
        bold = bool(m.group("b1")) and bool(m.group("b2"))
        trailing = line[m.end():].strip()
        yield IdHit(id=m.group("id"), bold=bold, trailing=trailing)


def find_ids(text: str) -> set[str]:
    """All distinct identifiers appearing anywhere in ``text`` (bold or not)."""
    return {m.group("id") for m in _ID_RE.finditer(text)}


def kind_of(ident: str) -> str:
    """The kind/prefix of an identifier (its leading segment)."""
    return ident.split("-", 1)[0]
