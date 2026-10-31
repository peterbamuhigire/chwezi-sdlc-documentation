from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from scripts import check_portable_paths
from scripts.check_portable_paths import (
    MACHINE_PATH,
    NotAssessed,
    check,
    load_baseline,
    tracked_local_settings,
)

# Sample paths are built from parts so this file never holds a literal machine path itself.
WINDOWS_USER_PATH = "C:" + "\\Users\\someone\\Downloads\\tool"
WINDOWS_WEB_ROOT = "C:/" + "wamp64/www/engine"
HOME_PATH = "/ho" + "me/someone/projects"
NO_HISTORY = {"history_prefixes": (), "history_line_ceiling": 0}


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


@pytest.mark.parametrize("sample", [WINDOWS_USER_PATH, WINDOWS_WEB_ROOT, HOME_PATH, "/m" + "nt/c/work", "/c/" + "Users/x"])
def test_machine_path_pattern_matches_each_form(sample: str) -> None:
    assert MACHINE_PATH.search(f"see `{sample}` for details")


@pytest.mark.parametrize("sample", [
    "projects/<ProjectName>/_context/", "https://example.org/home/page", "C:/Program Files/tool",
    "the home directory", "docs/Users-guide.md", "/usr/local/bin",
])
def test_machine_path_pattern_ignores_portable_text(sample: str) -> None:
    assert MACHINE_PATH.search(sample) is None


def test_live_machine_path_is_reported_with_file_and_line(tmp_path: Path) -> None:
    git_repo(tmp_path, {"skill/SKILL.md": f"# s\nuse {WINDOWS_USER_PATH}\n"})
    assert check(tmp_path, NO_HISTORY) == ["machine-path skill/SKILL.md:2: replace with a portable reference"]


def test_history_prefix_is_exempt_up_to_the_ceiling(tmp_path: Path) -> None:
    git_repo(tmp_path, {"docs/audits/old.md": f"{HOME_PATH}\n{WINDOWS_WEB_ROOT}\n"})
    baseline = {"history_prefixes": ("docs/audits/",), "history_line_ceiling": 2}
    assert check(tmp_path, baseline) == []
    baseline["history_line_ceiling"] = 1
    findings = check(tmp_path, baseline)
    assert len(findings) == 1 and findings[0].startswith("machine-path-history: 2 lines")


def test_outside_history_prefix_is_never_exempt(tmp_path: Path) -> None:
    git_repo(tmp_path, {"docs/skill-authoring-standard.md": f"run {WINDOWS_WEB_ROOT}\n"})
    baseline = {"history_prefixes": ("docs/audits/",), "history_line_ceiling": 99}
    assert len(check(tmp_path, baseline)) == 1


def test_unreadable_binary_files_are_skipped(tmp_path: Path) -> None:
    git_repo(tmp_path, {"blob.bin": "x"})
    (tmp_path / "blob.bin").write_bytes(b"\xff\xfe" + HOME_PATH.encode())
    assert check(tmp_path, NO_HISTORY) == []


def test_committed_baseline_is_loadable_and_live_tree_is_clean() -> None:
    baseline = load_baseline()
    assert baseline["history_line_ceiling"] >= 0 and baseline["history_prefixes"]
    try:
        findings = check(Path(__file__).resolve().parents[2])
    except NotAssessed as exc:
        pytest.skip(f"not a git checkout: {exc}")
    assert findings == [], findings
