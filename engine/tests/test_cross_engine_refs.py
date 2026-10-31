from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from scripts import check_cross_engine_refs as refs
from scripts.check_cross_engine_refs import check_text, load_allowlist, resolve_dev_root, scan
from scripts.check_portable_paths import NotAssessed


def dev_engine(root: Path) -> Path:
    live = root / "skills" / "security" / "vibe-security-skill"
    live.mkdir(parents=True)
    (live / "SKILL.md").write_text("---\nname: vibe-security-skill\n---\n", encoding="utf-8")
    alias = root / "skills" / "security" / "dual-auth-rbac"
    alias.mkdir(parents=True)
    (alias / "ALIAS.md").write_text(
        "> Inactive alias. Route to `skills/vibe-security-skill` through `docs/skill-aliases.yml`.\n",
        encoding="utf-8",
    )
    (root / "references").mkdir()
    (root / "references" / "standard.md").write_text("# standard\n", encoding="utf-8")
    return root


def git_repo(root: Path, files: dict[str, str]) -> None:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    for name, body in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "--", *files], check=True)


def test_flat_layout_name_is_reported_without_a_sibling_checkout() -> None:
    findings = check_text("a.md", "Use `skills/dual-auth-rbac/` for sessions.", None, set())
    assert [f.code for f in findings] == ["flat-layout"]
    assert findings[0].reference == "skills/dual-auth-rbac"


def test_category_design_group_and_placeholder_forms_are_not_flat_layout_errors() -> None:
    text = (
        "Category `skills/security/vibe-security-skill`, design `skills/04-web-and-ui-design/ai-agent-ux`, "
        "accounting `skills/10-controls-governance-and-fraud/internal-controls-library`, "
        "placeholder `skills/<skill-name>/SKILL.md`, bare `skills/` folder, URL "
        "https://example.org/skills/plan-canvas and a prefix projects/x/skills/y."
    )
    assert check_text("a.md", text, None, set()) == []


def test_category_path_resolves_against_checkout(tmp_path: Path) -> None:
    dev = dev_engine(tmp_path)
    assert check_text("a.md", "See `skills/security/vibe-security-skill`.", dev, set()) == []
    assert check_text("a.md", "See `security/vibe-security-skill/references/x.md`.", dev, set()) == []


def test_missing_category_path_is_dangling(tmp_path: Path) -> None:
    dev = dev_engine(tmp_path)
    findings = check_text("a.md", "See `skills/security/no-such-skill`.", dev, set())
    assert [f.code for f in findings] == ["dangling"]


def test_inactive_alias_names_its_successor(tmp_path: Path) -> None:
    dev = dev_engine(tmp_path)
    findings = check_text("a.md", "See `skills/security/dual-auth-rbac`.", dev, set())
    assert [f.code for f in findings] == ["inactive-alias"]
    assert "skills/vibe-security-skill" in findings[0].message


def test_engine_url_paths_resolve_against_checkout(tmp_path: Path) -> None:
    dev = dev_engine(tmp_path)
    ok = "[x](https://github.com/o/chwezi-dev-engine/blob/main/references/standard.md)"
    bad = "[x](https://github.com/o/chwezi-dev-engine/blob/main/references/missing.md)"
    assert check_text("a.md", ok, dev, set()) == []
    assert [f.code for f in check_text("a.md", bad, dev, set())] == ["dangling"]


def test_category_forms_are_skipped_not_passed_without_a_checkout() -> None:
    assert check_text("a.md", "See `skills/security/no-such-skill`.", None, set()) == []


def test_allowlist_entry_suppresses_only_its_file_and_reference() -> None:
    allowed = {("a.md", "skills/plan-canvas")}
    assert check_text("a.md", "`skills/plan-canvas/SKILL.md`", None, allowed) == []
    assert len(check_text("b.md", "`skills/plan-canvas/SKILL.md`", None, allowed)) == 1


def test_allowlist_entry_without_reason_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "allow.json"
    path.write_text(json.dumps([{"path": "a.md", "reference": "skills/x", "reason": " "}]), encoding="utf-8")
    with pytest.raises(ValueError):
        load_allowlist(path)


def test_scan_skips_history_under_docs_and_non_markdown(tmp_path: Path) -> None:
    git_repo(tmp_path, {
        "docs/audit.md": "old `skills/dual-auth-rbac`\n",
        "notes.txt": "old `skills/dual-auth-rbac`\n",
        "skill/SKILL.md": "live `skills/dual-auth-rbac`\n",
    })
    findings = scan(tmp_path, None, set())
    assert [f.path for f in findings] == ["skill/SKILL.md"]


def test_resolve_dev_root_validates_the_directory(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv(refs.ENV_ROOT, raising=False)
    assert resolve_dev_root(None) is None
    with pytest.raises(ValueError):
        resolve_dev_root(tmp_path)
    dev = dev_engine(tmp_path / "dev")
    monkeypatch.setenv(refs.ENV_ROOT, str(dev))
    assert resolve_dev_root(None) == dev


def test_main_exit_codes(tmp_path: Path, monkeypatch, capsys) -> None:
    git_repo(tmp_path, {"skill/SKILL.md": "live `skills/dual-auth-rbac`\n"})
    monkeypatch.delenv(refs.ENV_ROOT, raising=False)
    monkeypatch.setattr("sys.argv", ["check_cross_engine_refs.py", "--root", str(tmp_path)])
    assert refs.main() == 1
    assert "category and URL path resolution NOT_ASSESSED" in capsys.readouterr().out
    monkeypatch.setattr("sys.argv", ["check_cross_engine_refs.py", "--root", str(tmp_path), "--require-root"])
    assert refs.main() == 2


def test_live_repository_has_no_flat_layout_references() -> None:
    try:
        findings = scan(refs.ROOT, None)
    except NotAssessed as exc:
        pytest.skip(f"not a git checkout: {exc}")
    assert findings == [], [finding.render() for finding in findings]
