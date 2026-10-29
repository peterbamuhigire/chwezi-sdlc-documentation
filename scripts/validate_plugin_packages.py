#!/usr/bin/env python3
"""Validate local plugin marketplace metadata and package file-count budget."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_EXCLUDES = {".git", ".cache", "cache", "__pycache__", "node_modules", ".venv", "venv"}
PACKAGE_LIMIT = 5000


def active_skill_paths(root: Path) -> list[str]:
    paths = []
    for folder in sorted(root.iterdir()):
        if not folder.is_dir() or not (len(folder.name) >= 3 and folder.name[:2].isdigit() and folder.name[2] == "-"):
            continue
        paths.extend(p.relative_to(root).as_posix() for p in folder.rglob("SKILL.md"))
    return sorted(paths)


def entry_counts(root: Path) -> tuple[int, int]:
    """Count files and symlink entries; package count omits VCS/tool caches."""
    def count(exclude: bool) -> int:
        total = 0
        for current, dirs, files in os.walk(root, followlinks=False):
            current_path = Path(current)
            if exclude:
                dirs[:] = [name for name in dirs if name not in PACKAGE_EXCLUDES]
            total += sum(
                1 for name in files
                if (current_path / name).is_file() or (current_path / name).is_symlink()
            )
            # os.walk reports symlinked directories in dirs without traversing them.
            total += sum(1 for name in dirs if (current_path / name).is_symlink())
        return total

    return count(exclude=False), count(exclude=True)


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        data = json.load(stream)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return data


def validate(root: Path, package_limit: int = PACKAGE_LIMIT) -> list[str]:
    errors: list[str] = []
    expected = active_skill_paths(root)
    expected_dirs = sorted(path.removesuffix("SKILL.md") for path in expected)

    claude_path = root / ".claude-plugin" / "plugin.json"
    try:
        claude = read_json(claude_path)
        configured = claude.get("skills")
        if not isinstance(configured, list) or any(not isinstance(item, str) for item in configured):
            errors.append("Claude manifest skills must be an array of relative directory paths")
        else:
            configured_dirs = sorted(item.removeprefix("./") for item in configured)
            if len(configured_dirs) != len(set(configured_dirs)):
                errors.append("Claude manifest contains duplicate skill paths")
            if configured_dirs != expected_dirs:
                missing = sorted(set(expected_dirs) - set(configured_dirs))
                extra = sorted(set(configured_dirs) - set(expected_dirs))
                errors.append(f"Claude skill paths differ from active catalogue (missing={missing}; extra={extra})")
            for item in configured:
                if not (root / item / "SKILL.md").is_file():
                    errors.append(f"Claude skill path has no SKILL.md: {item}")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"Claude manifest cannot be read: {exc}")

    marketplace_path = root / ".agents" / "plugins" / "marketplace.json"
    try:
        marketplace = read_json(marketplace_path)
        if not isinstance(marketplace.get("name"), str) or not marketplace["name"].strip():
            errors.append("Codex marketplace requires a non-empty name")
        plugins = marketplace.get("plugins")
        if not isinstance(plugins, list) or len(plugins) != 1:
            errors.append("Codex marketplace must list exactly this engine's one local plugin")
        else:
            plugin = plugins[0]
            source = plugin.get("source") if isinstance(plugin, dict) else None
            path = source.get("path") if isinstance(source, dict) else None
            if not isinstance(plugin, dict) or not isinstance(source, dict):
                errors.append("Codex plugin source must use the documented local source object")
            elif source.get("source") != "local" or not isinstance(path, str) or not path.startswith("./"):
                errors.append("Codex plugin source must be local and use a ./-prefixed path")
            else:
                resolved = (root / path).resolve()
                if not resolved.is_relative_to(root.resolve()) or not resolved.is_dir():
                    errors.append(f"Codex marketplace source path is missing or escapes repository: {path}")
            policy = plugin.get("policy") if isinstance(plugin, dict) else None
            if not isinstance(policy, dict) or not policy.get("installation") or not policy.get("authentication"):
                errors.append("Codex plugin entry requires installation and authentication policy")
            if not (root / ".claude-plugin" / "plugin.json").is_file():
                errors.append("local Codex-compatible package has no Claude-compatible plugin manifest")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"Codex marketplace cannot be read: {exc}")

    full_count, package_count = entry_counts(root)
    if package_count > package_limit:
        errors.append(f"package-oriented file count {package_count} exceeds hard limit {package_limit}")
    print(f"active skill paths: {len(expected)}")
    print(f"checkout file entries (including .git and caches): {full_count}")
    print(f"package-oriented file entries (excluding {', '.join(sorted(PACKAGE_EXCLUDES))}): {package_count}")
    print(f"package hard limit: {package_limit}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--package-limit", type=int, default=PACKAGE_LIMIT)
    args = parser.parse_args()
    return 1 if validate(args.root.resolve(), args.package_limit) else 0


if __name__ == "__main__":
    raise SystemExit(main())
