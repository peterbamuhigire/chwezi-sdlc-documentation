from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from scripts import check_portable_paths
from scripts.check_portable_paths import NotAssessed, check, tracked_local_settings


def git_repo(root: Path, files: dict[str, str]) -> None:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    for name, body in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "--", *files], check=True)


def test_tracked_local_settings_is_reported(tmp_path: Path) -> None:
    git_repo(tmp_path, {".claude/settings.local.json": "{}", "README.md": "# ok\n"})
    findings = check(tmp_path)
    assert len(findings) == 1
    assert findings[0].startswith("tracked-local-settings .claude/settings.local.json")


def test_clean_checkout_has_no_findings(tmp_path: Path) -> None:
    git_repo(tmp_path, {".claude/settings.json": "{}", "README.md": "# ok\n"})
    assert check(tmp_path) == []


def test_ignored_local_settings_are_not_tracked(tmp_path: Path) -> None:
    git_repo(tmp_path, {".gitignore": ".claude/settings.local.json\n", "README.md": "# ok\n"})
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "settings.local.json").write_text("{}", encoding="utf-8")
    assert check(tmp_path) == []


def test_name_match_is_on_the_file_name_only() -> None:
    files = ["a/b.local.json", "a/local.json.md", "docs/the.local.jsonl", "x/y/settings.local.json"]
    assert tracked_local_settings(files) == ["a/b.local.json", "x/y/settings.local.json"]


def test_non_git_directory_is_not_assessed(tmp_path: Path) -> None:
    with pytest.raises(NotAssessed):
        check(tmp_path)


def test_main_exit_codes(tmp_path: Path, monkeypatch, capsys) -> None:
    git_repo(tmp_path, {".claude/settings.local.json": "{}"})
    monkeypatch.setattr("sys.argv", ["check_portable_paths.py", "--root", str(tmp_path)])
    assert check_portable_paths.main() == 1
    assert "portable-paths: FAIL (1 finding(s))" in capsys.readouterr().out
