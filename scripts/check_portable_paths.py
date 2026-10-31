#!/usr/bin/env python3
"""Keep machine-specific and per-user content out of this public repository.

Two checks run over the files tracked by git:

1. Per-user settings (`*.local.json`) must not be tracked. They hold local usernames, project
   names and command permissions that a cloner would inherit.
2. Machine-specific paths (a Windows drive path under a user or web-server folder, a home
   directory, a WSL mount) must not appear in live content. The historical record under the
   prefixes listed in `tests/portable-paths-baseline.json` is exempt but cannot grow: its line
   count must stay at or below the committed ceiling. Lower the ceiling when history is cleaned.

Exit codes: 0 clean, 1 findings, 2 not assessed (not a git checkout).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "tests" / "portable-paths-baseline.json"
LOCAL_SETTINGS_SUFFIX = ".local.json"
MAX_FILE_BYTES = 2_000_000
MACHINE_PATH = re.compile(
    r"[A-Za-z]:[\\/]+(?:wamp64|Users)[\\/]"
    r"|(?<![A-Za-z0-9_.-])/home/[a-z][a-z0-9_-]*/"
    r"|/Users/[A-Za-z][A-Za-z0-9_-]*/"
    r"|/mnt/[a-z]/"
    r"|[/\\]c[/\\]wamp64"
    r"|/c/(?:Users)/"
)


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


def load_baseline(path: Path = BASELINE) -> dict:
    if not path.is_file():
        return {"history_prefixes": [], "history_line_ceiling": 0}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "history_prefixes": tuple(data.get("history_prefixes", [])),
        "history_line_ceiling": int(data.get("history_line_ceiling", 0)),
    }


def machine_path_lines(root: Path, files: list[str]) -> list[tuple[str, int]]:
    """(file, line number) for every line with a machine-specific path in a readable text file."""
    hits: list[tuple[str, int]] = []
    for rel in files:
        target = root / rel
        try:
            if not target.is_file() or target.stat().st_size > MAX_FILE_BYTES:
                continue
            text = target.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        hits.extend((rel, number) for number, line in enumerate(text.splitlines(), start=1) if MACHINE_PATH.search(line))
    return hits


def check(root: Path, baseline: dict | None = None) -> list[str]:
    baseline = load_baseline() if baseline is None else baseline
    files = tracked_files(root)
    findings = [
        f"tracked-local-settings {path}: per-user settings must not be committed; "
        f"run `git rm --cached {path}` and ignore it"
        for path in tracked_local_settings(files)
    ]
    history = tuple(baseline["history_prefixes"])
    history_lines = 0
    for rel, number in machine_path_lines(root, files):
        if history and rel.startswith(history):
            history_lines += 1
        else:
            findings.append(f"machine-path {rel}:{number}: replace with a portable reference")
    ceiling = baseline["history_line_ceiling"]
    if history_lines > ceiling:
        findings.append(
            f"machine-path-history: {history_lines} lines under the historical prefixes exceed the "
            f"ceiling of {ceiling} in tests/portable-paths-baseline.json"
        )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
