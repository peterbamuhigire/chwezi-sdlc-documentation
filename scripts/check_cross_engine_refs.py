#!/usr/bin/env python3
"""Check that skill references into the Chwezi Dev Engine resolve.

Two classes of reference are checked in tracked Markdown outside `docs/` (the history under
`docs/` records old names on purpose):

1. Flat-layout names such as `skills/<name>`. The dev engine groups skills by category, so a
   bare `skills/<name>` cannot resolve. This class needs no sibling checkout and always runs.
2. Category paths (`skills/<category>/<name>`, a backticked `<category>/<name>`, and GitHub
   `chwezi-dev-engine/(blob|tree)/main/<path>` links). These are resolved against a dev-engine
   checkout given by `--dev-engine-root` or the `CHWEZI_DEV_ENGINE_ROOT` environment variable.
   An inactive alias (a directory holding `ALIAS.md` but no `SKILL.md`) is reported with its
   successor. With no checkout, this class is reported NOT_ASSESSED and never counted as a pass.

Exit codes: 0 no findings, 1 findings, 2 usage error or `--require-root` without a checkout.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_portable_paths import NotAssessed, tracked_files  # noqa: E402

ENV_ROOT = "CHWEZI_DEV_ENGINE_ROOT"
ALLOWLIST = ROOT / "tests" / "cross-engine-ref-allowlist.json"
CATEGORIES = (
    "ai", "android", "architecture", "backend-databases", "devops-cloud", "execution-plan-scripts",
    "finance-accounting", "frontend-ux", "game-development", "gis", "ios", "languages", "mobile-cross",
    "product-business", "saas", "sdlc-meta", "security",
)
_CAT = "|".join(CATEGORIES)
_BEFORE = r"(?<![A-Za-z0-9_./-])"
FLAT = re.compile(_BEFORE + r"skills/([a-z0-9][a-z0-9_-]*)(?=[/\s`'\")\].,;:]|$)")
CATEGORY_PATH = re.compile(_BEFORE + rf"skills/({_CAT})/([a-z0-9][a-z0-9-]*)")
CATEGORY_TICKED = re.compile(rf"`({_CAT})/([a-z0-9][a-z0-9-]*)(?:/[^`]*)?`")
ENGINE_URL = re.compile(r"chwezi-dev-engine/(?:blob|tree)/main/([A-Za-z0-9_./-]+)")
ALIAS_SUCCESSOR = re.compile(r"Route to `([^`]+)`")


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    code: str
    reference: str
    message: str

    def render(self) -> str:
        return f"{self.code} {self.path}:{self.line}: {self.message}"


def load_allowlist(path: Path = ALLOWLIST) -> set[tuple[str, str]]:
    """Reviewed exceptions as (file, reference) pairs; every entry must carry a reason."""
    if not path.is_file():
        return set()
    entries = json.loads(path.read_text(encoding="utf-8"))
    allowed = set()
    for entry in entries:
        if not str(entry.get("reason", "")).strip():
            raise ValueError(f"allowlist entry without a reason: {entry}")
        allowed.add((entry["path"], entry["reference"]))
    return allowed


def alias_successor(directory: Path) -> str:
    try:
        text = (directory / "ALIAS.md").read_text(encoding="utf-8")
    except OSError:
        return "its canonical successor"
    match = ALIAS_SUCCESSOR.search(text)
    return f"`{match.group(1)}`" if match else "its canonical successor"


def check_text(rel: str, text: str, dev_root: Path | None, allowed: set[tuple[str, str]]) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[tuple[int, str]] = set()

    def add(line: int, code: str, reference: str, message: str) -> None:
        if (rel, reference) in allowed or (line, reference) in seen:
            return
        seen.add((line, reference))
        findings.append(Finding(rel, line, code, reference, message))

    for number, line in enumerate(text.splitlines(), start=1):
        for match in FLAT.finditer(line):
            name = match.group(1)
            if name in CATEGORIES or re.match(r"\d\d-", name):
                continue
            ref = f"skills/{name}"
            add(number, "flat-layout", ref,
                f"`{ref}` is not a category path; use `skills/<category>/{name}` after checking the dev engine")
        if dev_root is None:
            continue
        for pattern in (CATEGORY_PATH, CATEGORY_TICKED):
            for match in pattern.finditer(line):
                category, name = match.group(1), match.group(2)
                directory = dev_root / "skills" / category / name
                ref = f"{category}/{name}"
                if (directory / "SKILL.md").is_file():
                    continue
                if (directory / "ALIAS.md").is_file():
                    add(number, "inactive-alias", ref,
                        f"`{ref}` is an inactive alias; cite {alias_successor(directory)}")
                else:
                    add(number, "dangling", ref, f"`{ref}` does not exist in the dev engine checkout")
        for match in ENGINE_URL.finditer(line):
            target = match.group(1).rstrip(".")
            if not (dev_root / target).exists():
                add(number, "dangling", target, f"`{target}` does not exist in the dev engine checkout")
    return findings


def scan(root: Path, dev_root: Path | None, allowed: set[tuple[str, str]] | None = None) -> list[Finding]:
    allowed = load_allowlist() if allowed is None else allowed
    findings: list[Finding] = []
    for rel in tracked_files(root):
        if not rel.endswith(".md") or rel.startswith("docs/"):
            continue
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        findings.extend(check_text(rel, text, dev_root, allowed))
    return findings


def resolve_dev_root(argument: Path | None) -> Path | None:
    value = argument if argument is not None else (Path(os.environ[ENV_ROOT]) if os.environ.get(ENV_ROOT) else None)
    if value is None:
        return None
    if not (value / "skills").is_dir():
        raise ValueError(f"dev engine root has no skills/ directory: {value}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (default: this checkout)")
    parser.add_argument("--dev-engine-root", type=Path, default=None, help=f"dev engine checkout (or set {ENV_ROOT})")
    parser.add_argument("--require-root", action="store_true", help="exit 2 when no dev engine checkout is available")
    args = parser.parse_args()
    try:
        dev_root = resolve_dev_root(args.dev_engine_root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if dev_root is None and args.require_root:
        print(f"ERROR: --require-root needs --dev-engine-root or {ENV_ROOT}", file=sys.stderr)
        return 2
    try:
        findings = scan(args.root, dev_root)
    except NotAssessed as exc:
        print(f"NOT_ASSESSED: {exc}", file=sys.stderr)
        return 2
    for finding in findings:
        print(finding.render())
    resolution = "category and URL paths resolved against the dev engine checkout" if dev_root else (
        "category and URL path resolution NOT_ASSESSED (no dev engine checkout configured)")
    print(f"cross-engine-refs: {'FAIL' if findings else 'PASS'} ({len(findings)} finding(s)); {resolution}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
