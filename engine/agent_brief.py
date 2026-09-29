"""Render a derived agent build brief from an approved SRS workspace (M10-08-T08).

The brief is a short, six-area hand-over for a coding agent: Objective,
Commands, Structure, Conventions, Testing and Boundaries (Always / Ask first /
Never). It is derived, never authored: every entry ends with the SRS section
path or registry identifier it came from, and an area whose source is missing
becomes a ``[CONTEXT-GAP: ...]`` marker, which the kernel's blocking-marker gate
(``engine/checks/markers.py``) reports until the source document is completed.
The brief never replaces or edits the SRS; it is regenerated, not hand-edited,
and is written beside the SDD hand-off record (``engine/sdd_handoff.py``),
following the same repository-relative reference convention.

Six-area brief structure adapted from addyosmani/agent-skills ``/spec`` (MIT,
https://github.com/addyosmani/agent-skills, commit 2686b62). Paraphrased.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

from ruamel.yaml import YAML

from engine.parsers.frontmatter import parse_frontmatter

BRIEF_NAME = "agent-build-brief.md"
BRIEF_DOCUMENT = "agent-build-brief"
TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "templates" / BRIEF_NAME
AREAS = ("objective", "commands", "structure", "conventions", "testing",
         "always", "ask_first", "never")

_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
_ITEM = re.compile(r"^\s*(?:[-*]|\d+\.)\s+(.*\S)\s*$")
_BOLD_ID = re.compile(r"^\*\*(?P<id>(?:FR|BR|CTRL|BG)-[A-Z0-9-]*\d{3,5})\*\*:?\s+(?P<text>.*)$")
_FIG = re.compile(r"<!--\s*diagram-ir:\s*(FIG-\d{3,5})\s*-->")
_TC_TITLE = re.compile(r"^#\s+(TC-\d{3,5})\s+(.*)$", re.MULTILINE)
_DECISION_ROW = re.compile(r"^\|\s*(D-\d{3,5})\s*\|(.*)\|\s*$")
_NEGATION = re.compile(r"\b(do not|does not|must not|shall not|never)\b", re.IGNORECASE)
_TEST_HEAD = re.compile(r"\btest (commands?|execution|runner)\b", re.IGNORECASE)
_CMD_HEAD = re.compile(r"\b(build|run|commands?|operating environment|development environment)\b",
                       re.IGNORECASE)
_STRUCT_HEAD = re.compile(r"\b(software interfaces|external interfaces|repository structure|"
                          r"system structure|components)\b", re.IGNORECASE)
_CONV_HEAD = re.compile(r"\b(conventions?|coding|style|guidelines?)\b", re.IGNORECASE)
_PROHIBITED_HEAD = re.compile(r"\b(prohibited|never)\b", re.IGNORECASE)
_CLOSED_DECISIONS = {"approved", "accepted", "implemented", "rejected", "closed"}


@dataclass(frozen=True)
class Entry:
    area: str
    text: str
    source: str

    @property
    def is_gap(self) -> bool:
        return self.text.startswith("[CONTEXT-GAP:")

    def render(self) -> str:
        return f"- {self.text} ({self.source})"


@dataclass(frozen=True)
class _Doc:
    rel: str
    frontmatter: dict
    body: str

    def sections(self) -> List[Tuple[str, List[str]]]:
        out: List[Tuple[str, List[str]]] = []
        heading, lines = "", []
        for line in self.body.splitlines():
            m = _HEADING.match(line)
            if m:
                out.append((heading, lines))
                heading, lines = m.group(2), []
            else:
                lines.append(line)
        out.append((heading, lines))
        return out


def _gap(area: str, reason: str, expected: str) -> Entry:
    return Entry(area, f"[CONTEXT-GAP: {reason}]", f"expected in {expected}")


def _first_sentence(text: str) -> str:
    text = " ".join(text.split())
    return re.split(r"(?<=\.)\s", text, maxsplit=1)[0]


def _load_docs(project: Path) -> List[_Doc]:
    docs = []
    for path in sorted(project.rglob("*.md")):
        rel = path.relative_to(project).as_posix()
        if "_generated" in path.relative_to(project).parts:
            continue
        fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        if fm.get("document") == BRIEF_DOCUMENT:
            continue
        docs.append(_Doc(rel, fm, body))
    return docs


def _items(lines: Iterable[str]) -> List[str]:
    return [m.group(1) for m in (_ITEM.match(line) for line in lines) if m]


def _section_items(docs: Iterable[_Doc], area: str, match, exclude=None,
                   prefix: str = "") -> List[Entry]:
    out = []
    for doc in docs:
        if not doc.rel.startswith(prefix):
            continue
        for heading, lines in doc.sections():
            if not heading or not match.search(heading):
                continue
            if exclude is not None and exclude.search(heading):
                continue
            out.extend(Entry(area, item, f"{doc.rel} § {heading}") for item in _items(lines))
    return out


def _objective(project: Path, docs: List[_Doc]) -> List[Entry]:
    vision = [d for d in docs if d.rel == "_context/vision.md"]
    out = []
    for doc in vision:
        for item in _items(doc.body.splitlines()):
            m = _BOLD_ID.match(item)
            if m and m.group("id").startswith("BG-"):
                out.append(Entry("objective", m.group("text"), f"{m.group('id')}, {doc.rel}"))
    return out or [_gap("objective", "no business goals (BG-nnn) found in the vision",
                        "_context/vision.md")]


def _structure(docs: List[_Doc]) -> List[Entry]:
    out = _section_items(docs, "structure", _STRUCT_HEAD)
    for doc in docs:
        if not doc.rel.startswith("03-design-documentation/01-high-level-design/"):
            continue
        for heading, lines in doc.sections():
            figs = [m.group(1) for line in lines for m in _FIG.finditer(line)]
            if heading and figs and "traceab" not in heading.lower():
                title = re.sub(r"^\d+(\.\d+)*\.?\s*", "", heading)
                out.append(Entry("structure", f"Design view: {title}, shown in {', '.join(figs)}",
                                 f"{doc.rel} § {heading}"))
    return out or [_gap("structure", "no interface, component or high-level design section found",
                        "SRS interface sections or 03-design-documentation/01-high-level-design/")]


def _testing(docs: List[_Doc]) -> List[Entry]:
    out = []
    for doc in docs:
        if not (doc.frontmatter.get("phase") == "05" or doc.rel.startswith("05-")):
            continue
        m = _TC_TITLE.search(doc.body)
        if not m:
            continue
        trace = doc.frontmatter.get("requirement_trace") or []
        trace = [trace] if isinstance(trace, str) else list(trace)
        expected = doc.frontmatter.get("expected_results") or []
        text = f"{m.group(1)} {m.group(2)} verifies {', '.join(trace) or 'no traced requirement'}"
        if expected:
            text += f"; expected result: {_first_sentence(str(expected[0]))}"
        out.append(Entry("testing", text, f"{m.group(1)}, {doc.rel}"))
    if not out:
        out.append(_gap("testing", "no TC-nnn test cases found", "05-testing-documentation/"))
    commands = _section_items(docs, "testing", _TEST_HEAD)
    return (commands or [_gap("testing", "no test commands are recorded",
                              "a Test commands section of the test plan or SRS environment section")]) + out


def _always(docs: List[_Doc]) -> List[Entry]:
    out = []
    for doc in docs:
        if not (doc.frontmatter.get("phase") == "02" or doc.rel.startswith("02-")):
            continue
        for item in _items(doc.body.splitlines()):
            m = _BOLD_ID.match(item)
            if m and not m.group("id").startswith("BG-"):
                text = re.split(r";\s*traces to\b", m.group("text"), maxsplit=1)[0].rstrip(".")
                out.append(Entry("always", f"{m.group('id')}: {text}", f"{m.group('id')}, {doc.rel}"))
    return out or [_gap("always", "no requirements, business rules or controls found",
                        "02-requirements-engineering/")]


def _decision_rows(docs: List[_Doc]):
    for doc in docs:
        for line in doc.body.splitlines():
            m = _DECISION_ROW.match(line)
            if m:
                cells = [c.strip() for c in m.group(2).split("|")]
                if len(cells) >= 4:
                    yield doc, m.group(1), cells[1], cells[-1]


def _ask_first(project: Path, docs: List[_Doc]) -> List[Entry]:
    out = [Entry("ask_first", "Any change to a baselined requirement or its acceptance criterion",
                 "change control, _registry/change-impact.yaml")]
    for doc, did, status, decision in _decision_rows(docs):
        if "OPEN" in status.upper():
            out.append(Entry("ask_first", f"{did} ({status}): {_first_sentence(decision)}",
                             f"{did}, {doc.rel}"))
    cia = project / "_registry" / "change-impact.yaml"
    if cia.is_file():
        data = YAML(typ="safe").load(cia.read_text(encoding="utf-8")) or {}
        for entry in data.get("entries", []) or []:
            decision = str(entry.get("decision", "")).lower()
            if decision in _CLOSED_DECISIONS:
                continue
            ids = ", ".join(entry.get("affected_baseline_ids", []) or [])
            out.append(Entry("ask_first",
                             f"{entry.get('id')} ({decision or 'undecided'}) affects {ids}: "
                             f"{_first_sentence(str(entry.get('decision_body', '')))}",
                             f"{entry.get('id')}, _registry/change-impact.yaml"))
    return out


def _never(docs: List[_Doc]) -> List[Entry]:
    out = [Entry("never", "Edit the SRS or this brief by hand; change the SRS and regenerate the brief",
                 "templates/agent-build-brief.md")]
    out.extend(_section_items(docs, "never", _PROHIBITED_HEAD))
    for doc, did, status, decision in _decision_rows(docs):
        if "OPEN" in status.upper():
            continue
        for sentence in re.split(r"(?<=\.)\s+", decision):
            if _NEGATION.search(sentence):
                out.append(Entry("never", sentence.rstrip("."), f"{did}, {doc.rel}"))
    for entry in _always(docs):
        if not entry.is_gap and re.search(r"\b(shall|must) not\b", entry.text, re.IGNORECASE):
            out.append(Entry("never", entry.text, entry.source))
    return out


def collect(project: Path) -> List[Entry]:
    """Every brief entry, in area order, traced or marked as a gap."""
    project = Path(project)
    docs = _load_docs(project)
    return (
        _objective(project, docs)
        + (_section_items(docs, "commands", _CMD_HEAD, exclude=_TEST_HEAD)
           or [_gap("commands", "no build or run commands are recorded",
                    "the SRS operating or development environment section")])
        + _structure(docs)
        + (_section_items(docs, "conventions", _CONV_HEAD, prefix="04-development-artifacts/")
           or [_gap("conventions", "no coding conventions are recorded",
                    "04-development-artifacts/ coding guidelines")])
        + _testing(docs)
        + _always(docs)
        + _ask_first(project, docs)
        + _never(docs)
    )


def untraced(entries: Iterable[Entry]) -> List[Entry]:
    """Entries without a source reference (must always be empty)."""
    return [e for e in entries if not e.source.strip()]


def render(project: Path, entries: Optional[List[Entry]] = None,
           template: Path = TEMPLATE_PATH) -> str:
    project = Path(project)
    entries = collect(project) if entries is None else entries
    text = template.read_text(encoding="utf-8").replace("{{project}}", project.name)
    for area in AREAS:
        block = "\n".join(e.render() for e in entries if e.area == area)
        text = text.replace("{{" + area + "}}", block)
    return text


def write_brief(project: Path, out: Optional[Path] = None) -> Path:
    """Render the brief and write it (default: ``<project>/agent-build-brief.md``)."""
    project = Path(project)
    if not project.is_dir():
        raise ValueError(f"project directory not found: {project}")
    output = Path(out) if out is not None else project / BRIEF_NAME
    if output.suffix != ".md":
        raise ValueError("the brief must be written to a .md file")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(project), encoding="utf-8", newline="\n")
    return output
