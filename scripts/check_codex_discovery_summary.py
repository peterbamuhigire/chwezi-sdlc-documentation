#!/usr/bin/env python3
"""Check a sanitized offline Codex prompt-input discovery summary.

This reads only a summary JSON. Never pass or retain the raw prompt-input dump;
it can contain private or internal instruction text.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def validate_summary(summary: dict[str, Any], expected_paths: int) -> list[str]:
    errors: list[str] = []
    manifest = summary.get("manifest_paths")
    runtime = summary.get("runtime_paths")
    missing = summary.get("missing")
    if manifest != expected_paths:
        errors.append(f"manifest_paths={manifest!r}; expected {expected_paths}")
    if runtime != expected_paths:
        errors.append(f"runtime_paths={runtime!r}; expected {expected_paths}")
    if missing != []:
        errors.append("missing must be an empty list")
    if summary.get("network") != "none":
        errors.append("discovery run must record network='none'")
    if summary.get("model_calls") != 0:
        errors.append("discovery run must record model_calls=0")
    method = summary.get("method")
    if not isinstance(method, str) or "offline" not in method.lower():
        errors.append("method must identify an offline discovery run")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary", type=Path, help="sanitized summary JSON, never raw prompt input")
    parser.add_argument("--expected-paths", type=int, required=True)
    args = parser.parse_args()
    try:
        summary = json.loads(args.summary.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read sanitized summary: {exc}", file=sys.stderr)
        return 1
    if not isinstance(summary, dict):
        print("ERROR: summary must be a JSON object", file=sys.stderr)
        return 1
    errors = validate_summary(summary, args.expected_paths)
    print(f"expected paths: {args.expected_paths}")
    print(f"manifest paths: {summary.get('manifest_paths')}")
    print(f"runtime paths: {summary.get('runtime_paths')}")
    print(f"missing paths: {len(summary.get('missing', [])) if isinstance(summary.get('missing'), list) else 'invalid'}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
