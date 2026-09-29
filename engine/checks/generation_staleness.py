"""Commit-pinned staleness check for generated or recovered documents (M10-08-T06, UA-07).

A document that describes a codebase (an as-built design, a system orientation
guide) may pin itself to the code it was written from with two frontmatter
keys::

    generated_from_commit: "<40-character lower-case SHA>"
    source_repository: ../path/to/repository     # relative to the project root, or absolute
    referenced_paths:                            # optional; repository-relative
      - app/Services/InvoiceService.php

For each such document this check runs one read-only
``git --no-replace-objects -C <repo> diff --name-only <sha> HEAD -- <paths>``
and reports every referenced path that has changed since the pinned commit as
``staleness/changed-since-generation`` (MEDIUM, report-only). Referenced paths
are the ``referenced_paths`` list plus backticked repository-relative paths in
the body (a token containing ``/`` and no spaces).

Safety: the SHA must match ``^[0-9a-f]{40}$``; Git runs through
``subprocess.run`` with an argument list (no shell); a referenced path that
resolves outside the repository root is rejected and never passed to Git.
When the repository is absent or not a Git work tree, one INFO finding states
``NOT_ASSESSED`` and nothing else is inferred.

Orientation outline, reading-path ordering and commit-pinned staleness adapted
from Understand Anything (MIT, https://github.com/Egonex-AI/Understand-Anything,
commit b05cc3b20990afca537b4fc0a49b4d7fbdc65bb0). Paraphrased.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Iterable, List, Optional, Sequence

from engine.artifact_graph import Artifact, ArtifactGraph
from engine.findings import Finding, FindingCollection, Severity
from engine.gates.base import Gate

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_BACKTICK_PATH = re.compile(r"`([A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)+/?)`")
_GIT_TIMEOUT_SECONDS = 30


class StalenessError(ValueError):
    """Raised for a malformed pin or an unsafe referenced path."""


def validate_sha(value: object) -> str:
    """Return the SHA if it is a quoted 40-character lower-case hex string."""
    if not isinstance(value, str) or not SHA_RE.match(value):
        raise StalenessError(
            "generated_from_commit must be a quoted 40-character lower-case hexadecimal SHA"
        )
    return value


def referenced_paths(artifact: Artifact) -> List[str]:
    """Frontmatter ``referenced_paths`` plus backticked repository-relative body paths."""
    out: List[str] = []
    listed = artifact.frontmatter.get("referenced_paths") or []
    if isinstance(listed, str):
        listed = [listed]
    for item in listed:
        if isinstance(item, str) and item.strip():
            out.append(item.strip())
    out.extend(m.group(1) for m in _BACKTICK_PATH.finditer(artifact.body))
    seen: set[str] = set()
    return [p for p in out if not (p in seen or seen.add(p))]


def contained_paths(repo: Path, paths: Iterable[str]) -> tuple[List[str], List[str]]:
    """Split paths into (inside the repository, rejected)."""
    root = repo.resolve()
    inside: List[str] = []
    rejected: List[str] = []
    for raw in paths:
        candidate = Path(raw)
        if candidate.is_absolute():
            rejected.append(raw)
            continue
        resolved = (root / candidate).resolve()
        if resolved == root or root in resolved.parents:
            inside.append(candidate.as_posix())
        else:
            rejected.append(raw)
    return inside, rejected


def is_git_work_tree(repo: Path) -> bool:
    if not repo.is_dir():
        return False
    proc = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True, timeout=_GIT_TIMEOUT_SECONDS, check=False,
    )
    return proc.returncode == 0 and proc.stdout.strip() == "true"


def changed_since(repo: Path, sha: str, paths: Sequence[str]) -> List[str]:
    """Paths (of ``paths``) changed between ``sha`` and HEAD. One git call."""
    validate_sha(sha)
    if not paths:
        return []
    proc = subprocess.run(
        ["git", "--no-replace-objects", "-C", str(repo), "diff", "--name-only",
         sha, "HEAD", "--", *paths],
        capture_output=True, text=True, timeout=_GIT_TIMEOUT_SECONDS, check=False,
    )
    if proc.returncode != 0:
        raise StalenessError(f"git diff failed: {proc.stderr.strip() or 'unknown error'}")
    return sorted({line.strip() for line in proc.stdout.splitlines() if line.strip()})


class GenerationStalenessGate(Gate):
    id = "kernel.generation_staleness"
    title = "Commit-pinned documents are not stale against their source repository"
    severity = Severity.MEDIUM

    def __init__(self, project_root: Optional[Path] = None) -> None:
        self._root = Path(project_root) if project_root is not None else None

    def _finding(self, art: Artifact, severity: Severity, code: str, message: str,
                 evidence: Optional[dict] = None, fixes: Sequence[str] = ()) -> Finding:
        return Finding(
            gate_id=self.id, severity=severity, message=message,
            location=art.path, line=None, code=code,
            subject={"document": art.path.as_posix()},
            evidence=evidence, supported_fixes=tuple(fixes),
        )

    def evaluate(self, graph: ArtifactGraph, findings: FindingCollection) -> None:
        root = self._root or graph.root
        if root is None:
            return
        for art in graph.artifacts:
            fm = art.frontmatter
            if "generated_from_commit" not in fm or "source_repository" not in fm:
                continue
            self._check(root, art, findings)

    def _check(self, root: Path, art: Artifact, findings: FindingCollection) -> None:
        fm = art.frontmatter
        try:
            sha = validate_sha(fm.get("generated_from_commit"))
        except StalenessError as exc:
            findings.add(self._finding(art, Severity.MEDIUM, "staleness/malformed-commit", str(exc),
                                       fixes=("quote the full 40-character SHA from `git rev-parse HEAD`",)))
            return
        repo_value = fm.get("source_repository")
        repo = Path(str(repo_value)) if isinstance(repo_value, str) and repo_value.strip() else None
        if repo is not None and not repo.is_absolute():
            repo = (root / repo).resolve()
        if repo is None or not is_git_work_tree(repo):
            findings.add(self._finding(
                art, Severity.INFO, "staleness/not-assessed",
                "NOT_ASSESSED: source repository unavailable",
                evidence={"source_repository": repo_value}))
            return
        inside, rejected = contained_paths(repo, referenced_paths(art))
        for raw in rejected:
            findings.add(self._finding(
                art, Severity.MEDIUM, "staleness/path-outside-repository",
                f"referenced path {raw!r} resolves outside the source repository; not checked",
                evidence={"path": raw}))
        try:
            changed = changed_since(repo, sha, inside)
        except StalenessError as exc:
            findings.add(self._finding(art, Severity.MEDIUM, "staleness/unknown-commit", str(exc),
                                       evidence={"generated_from_commit": sha}))
            return
        for path in changed:
            findings.add(self._finding(
                art, Severity.MEDIUM, "staleness/changed-since-generation",
                f"{path} changed since {sha[:12]}; re-check the sections that cite it",
                evidence={"path": path, "generated_from_commit": sha},
                fixes=("re-read the changed file, revise the affected sections and move the pin forward",)))
