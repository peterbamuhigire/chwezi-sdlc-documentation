from __future__ import annotations

import json
from pathlib import Path

from scripts.check_codex_discovery_summary import validate_summary
from scripts import validate_plugin_packages
from scripts.validate_plugin_packages import entry_counts, validate


def make_package(root: Path) -> None:
    skill = root / "01-example" / "one"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: one\ndescription: Example skill.\n---\n", encoding="utf-8")
    claude = root / ".claude-plugin"
    claude.mkdir()
    (claude / "plugin.json").write_text(json.dumps({"name": "example", "skills": ["./01-example/one/"]}), encoding="utf-8")
    codex = root / ".agents" / "plugins"
    codex.mkdir(parents=True)
    (codex / "marketplace.json").write_text(json.dumps({
        "name": "local-example",
        "plugins": [{
            "name": "example",
            "source": {"source": "local", "path": "./"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        }],
    }), encoding="utf-8")


def test_plugin_marketplace_paths_match_active_catalogue(tmp_path: Path, capsys) -> None:
    make_package(tmp_path)
    assert validate(tmp_path) == []
    assert "active skill paths: 1" in capsys.readouterr().out


def test_plugin_validator_rejects_missing_skill_path_and_package_limit(tmp_path: Path, monkeypatch) -> None:
    make_package(tmp_path)
    monkeypatch.setattr(validate_plugin_packages, "PACKAGE_LIMIT", 1)
    manifest_path = tmp_path / ".claude-plugin" / "plugin.json"
    manifest_path.write_text(json.dumps({"skills": ["./01-example/missing/"]}), encoding="utf-8")
    errors = validate(tmp_path)
    assert any("differ from active catalogue" in error for error in errors)
    assert any("exceeds hard limit 1" in error for error in errors)


def test_plugin_validator_rejects_codex_claude_identity_mismatch(tmp_path: Path) -> None:
    make_package(tmp_path)
    marketplace_path = tmp_path / ".agents" / "plugins" / "marketplace.json"
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    marketplace["plugins"][0]["name"] = "different-plugin"
    marketplace_path.write_text(json.dumps(marketplace), encoding="utf-8")
    assert "Codex plugin name differs from Claude plugin manifest" in validate(tmp_path)


def test_plugin_validator_rejects_symlinked_skill_file(tmp_path: Path) -> None:
    make_package(tmp_path)
    skill = tmp_path / "01-example" / "one" / "SKILL.md"
    external = tmp_path.parent / f"{tmp_path.name}-external-skill.md"
    external.write_text("external fixture", encoding="utf-8")
    try:
        skill.unlink()
        skill.symlink_to(external)
    except OSError as error:
        external.unlink(missing_ok=True)
        import pytest
        pytest.skip(f"symlink creation unavailable: {error}")
    try:
        assert any("Claude skill path contains a symlink" in error for error in validate(tmp_path))
    finally:
        external.unlink(missing_ok=True)


def test_package_limit_accepts_5000_entries_and_rejects_5001(tmp_path: Path) -> None:
    make_package(tmp_path)
    _, package_entries = entry_counts(tmp_path)
    extra = tmp_path / "assets"
    extra.mkdir()
    for index in range(5000 - package_entries):
        (extra / f"item-{index:04d}.txt").touch()
    assert not any("exceeds hard limit" in error for error in validate(tmp_path))
    (extra / "item-over-limit.txt").touch()
    assert any("exceeds hard limit 5000" in error for error in validate(tmp_path))


def test_file_counts_separate_checkout_and_package_entries(tmp_path: Path) -> None:
    (tmp_path / ".git" / "objects").mkdir(parents=True)
    (tmp_path / ".git" / "objects" / "pack").write_text("x", encoding="utf-8")
    (tmp_path / "source.txt").write_text("x", encoding="utf-8")
    assert entry_counts(tmp_path) == (2, 1)


def test_full_checkout_count_also_obeys_hard_limit(tmp_path: Path, monkeypatch) -> None:
    make_package(tmp_path)
    monkeypatch.setattr(validate_plugin_packages, "PACKAGE_LIMIT", 3)
    (tmp_path / ".git" / "objects").mkdir(parents=True)
    (tmp_path / ".git" / "objects" / "large-entry").touch()
    errors = validate(tmp_path)
    assert any("full checkout file count" in error for error in errors)


def test_full_checkout_limit_accepts_5000_and_rejects_5001(tmp_path: Path) -> None:
    make_package(tmp_path)
    full_entries, _ = entry_counts(tmp_path)
    vcs_objects = tmp_path / ".git" / "objects"
    vcs_objects.mkdir(parents=True)
    for index in range(5000 - full_entries):
        (vcs_objects / f"entry-{index:04d}.bin").touch()
    assert entry_counts(tmp_path)[0] == 5000
    assert not any("full checkout file count" in error for error in validate(tmp_path))
    (vcs_objects / "entry-over-limit.bin").touch()
    assert any("full checkout file count 5001 exceeds hard limit 5000" == error for error in validate(tmp_path))


def test_codex_summary_accepts_complete_offline_inventory() -> None:
    summary = {
        "manifest_paths": 159,
        "runtime_paths": 159,
        "missing": [],
        "network": "none",
        "model_calls": 0,
        "method": "native offline debug prompt-input",
    }
    assert validate_summary(summary, expected_paths=159) == []


def test_codex_summary_rejects_omissions_network_or_model_calls() -> None:
    summary = {
        "manifest_paths": 159,
        "runtime_paths": 108,
        "missing": ["omitted/SKILL.md"],
        "network": "used",
        "model_calls": 1,
        "method": "online prompt-input",
    }
    errors = validate_summary(summary, expected_paths=159)
    assert len(errors) == 5


def test_unreadable_inventory_fails_closed(tmp_path: Path, monkeypatch) -> None:
    make_package(tmp_path)
    def denied_walk(*args, **kwargs):
        kwargs["onerror"](PermissionError("fixture directory cannot be read"))
        return iter(())
    monkeypatch.setattr(validate_plugin_packages.os, "walk", denied_walk)
    assert any("inventory incomplete" in error for error in validate(tmp_path))
