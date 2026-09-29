"""M10-08-T06 (UA-07): commit-pinned staleness check."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from engine.artifact_graph import ArtifactGraph
from engine.checks.generation_staleness import (
    GenerationStalenessGate,
    StalenessError,
    changed_since,
    contained_paths,
    validate_sha,
)
from engine.cli import _default_registry
from engine.findings import FindingCollection, Severity
from engine.workspace import Workspace


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
         "-c", "commit.gpgsign=false", "-C", str(repo), *args],
        capture_output=True, text=True, check=True,
    )
    return proc.stdout.strip()


@pytest.fixture
def source_repo(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "source"
    (repo / "src").mkdir(parents=True)
    (repo / "src" / "alpha.php").write_text("<?php // alpha\n", encoding="utf-8")
    (repo / "src" / "beta.php").write_text("<?php // beta\n", encoding="utf-8")
    (repo / "README.md").write_text("readme\n", encoding="utf-8")
    _git(repo, "init", "-q")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "initial")
    return repo, _git(repo, "rev-parse", "HEAD")


def _project(tmp_path: Path, sha: object, repo_value: str = "../source",
             extra_body: str = "") -> Path:
    project = tmp_path / "project"
    (project / "_context").mkdir(parents=True, exist_ok=True)
    (project / "_context" / "vision.md").write_text("# Vision\n", encoding="utf-8")
    doc = project / "04-development-artifacts" / "orientation.md"
    doc.parent.mkdir(parents=True, exist_ok=True)
    sha_line = f'"{sha}"' if isinstance(sha, str) else str(sha)
    doc.write_text(
        "---\n"
        f"generated_from_commit: {sha_line}\n"
        f"source_repository: {repo_value}\n"
        "referenced_paths:\n  - src/alpha.php\n"
        "---\n"
        "# Orientation\n\nThe entry point is `src/beta.php`; see also `README.md`.\n"
        + extra_body,
        encoding="utf-8",
    )
    return project


def _run(project: Path) -> list:
    findings = FindingCollection()
    GenerationStalenessGate().evaluate(ArtifactGraph.build(Workspace.load(project)), findings)
    return list(findings)


def test_one_changed_referenced_file_is_reported_exactly(tmp_path, source_repo):
    repo, sha = source_repo
    (repo / "src" / "alpha.php").write_text("<?php // alpha v2\n", encoding="utf-8")
    (repo / "README.md").write_text("changed but not referenced by path with a slash\n", encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "change")
    found = _run(_project(tmp_path, sha))
    assert [(f.code, f.evidence["path"]) for f in found] == [
        ("staleness/changed-since-generation", "src/alpha.php")]
    assert found[0].severity == Severity.MEDIUM


def test_backticked_body_path_is_checked(tmp_path, source_repo):
    repo, sha = source_repo
    (repo / "src" / "beta.php").write_text("<?php // beta v2\n", encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "change beta")
    found = _run(_project(tmp_path, sha))
    assert [f.evidence["path"] for f in found] == ["src/beta.php"]


def test_no_change_reports_nothing(tmp_path, source_repo):
    _, sha = source_repo
    assert _run(_project(tmp_path, sha)) == []


def test_absent_repository_is_one_info_not_assessed(tmp_path):
    found = _run(_project(tmp_path, "a" * 40, repo_value="../nowhere"))
    assert len(found) == 1
    assert found[0].severity == Severity.INFO
    assert found[0].message.startswith("NOT_ASSESSED")


def test_directory_that_is_not_a_work_tree_is_not_assessed(tmp_path):
    (tmp_path / "plain").mkdir()
    found = _run(_project(tmp_path, "a" * 40, repo_value="../plain"))
    assert [f.code for f in found] == ["staleness/not-assessed"]


@pytest.mark.parametrize("bad", ["abc123", "A" * 40, "g" * 40, "a" * 39, None, 1234])
def test_malformed_sha_is_rejected(bad):
    with pytest.raises(StalenessError):
        validate_sha(bad)


def test_malformed_sha_in_document_is_a_finding_and_git_is_not_run(tmp_path, source_repo):
    found = _run(_project(tmp_path, "not-a-sha"))
    assert [f.code for f in found] == ["staleness/malformed-commit"]


def test_unquoted_numeric_sha_is_rejected(tmp_path, source_repo):
    found = _run(_project(tmp_path, 1234567890))
    assert [f.code for f in found] == ["staleness/malformed-commit"]


def test_unknown_commit_is_reported(tmp_path, source_repo):
    found = _run(_project(tmp_path, "b" * 40))
    assert [f.code for f in found] == ["staleness/unknown-commit"]


def test_paths_outside_repository_are_rejected(tmp_path, source_repo):
    repo, sha = source_repo
    inside, rejected = contained_paths(repo, ["src/alpha.php", "../escape.txt", "/abs/path"])
    assert inside == ["src/alpha.php"]
    assert rejected == ["../escape.txt", "/abs/path"]
    project = _project(tmp_path, sha, extra_body="\nSee `src/../../escape/file.txt`.\n")
    found = _run(project)
    assert [f.code for f in found] == ["staleness/path-outside-repository"]


def test_changed_since_with_no_paths_makes_no_git_call(tmp_path):
    assert changed_since(tmp_path / "absent", "c" * 40, []) == []


def test_documents_without_a_pin_are_ignored(tmp_path):
    project = tmp_path / "project"
    (project / "_context").mkdir(parents=True)
    (project / "_context" / "vision.md").write_text("# Vision\n\n`src/x.php`\n", encoding="utf-8")
    assert _run(project) == []


def test_gate_is_registered_in_validate_and_never_blocks(tmp_path):
    ids = [g.id for g in _default_registry()]
    assert "kernel.generation_staleness" in ids
    project = _project(tmp_path, "a" * 40, repo_value="../nowhere")
    findings = FindingCollection()
    for gate in _default_registry():
        if gate.id == "kernel.generation_staleness":
            gate.evaluate(ArtifactGraph.build(Workspace.load(project)), findings)
    assert not findings.is_blocking


def test_gate_without_root_does_nothing():
    findings = FindingCollection()
    GenerationStalenessGate().evaluate(ArtifactGraph(artifacts=()), findings)
    assert len(findings) == 0
