#!/usr/bin/env python3
"""Fail when per-user tool settings are tracked in this public repository.

Per-user settings (for example a local permission allowlist) hold local usernames, project
names and command permissions that a cloner would inherit. They stay on the author's disk and
out of version control. Exit codes: 0 clean, 1 findings, 2 not assessed (not a git checkout).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
LOCAL_SETTINGS_SUFFIX = ".local.json"


class NotAssessed(RuntimeError):
    """Raised when the tracked-file list cannot be read."""


def tracked_files(root: Path) -> list[str]:
    """Return repository-relative POSIX paths from the git index."""
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        raise NotAssessed(f"git is not available: {exc}") from exc
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise NotAssessed(f"{root} is not a readable git checkout: {detail}")
    return [item for item in result.stdout.decode("utf-8").split("\0") if item]


def tracked_local_settings(files: list[str]) -> list[str]:
    """Paths of per-user settings files that are under version control."""
    return sorted(path for path in files if PurePosixPath(path).name.endswith(LOCAL_SETTINGS_SUFFIX))


def check(root: Path) -> list[str]:
    files = tracked_files(root)
    return [
        f"tracked-local-settings {path}: per-user settings must not be committed; "
        f"run `git rm --cached {path}` and ignore it"
        for path in tracked_local_settings(files)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (default: this checkout)")
    args = parser.parse_args()
    try:
        findings = check(args.root)
    except NotAssessed as exc:
        print(f"NOT_ASSESSED: {exc}", file=sys.stderr)
        return 2
    for line in findings:
        print(line)
    print(f"portable-paths: {'FAIL' if findings else 'PASS'} ({len(findings)} finding(s))")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
