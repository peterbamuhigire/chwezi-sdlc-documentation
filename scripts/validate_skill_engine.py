#!/usr/bin/env python3
"""Validate active skill contracts and compare them with a zero-debt baseline."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from ruamel.yaml import YAML


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
ACTIVE_ROOT_RE = re.compile(r"^0[1-9]-")
FRONTMATTER_RE = re.compile(r"^\ufeff?---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
MOJIBAKE = ("Ãƒ", "Ã‚", "Ã¢â‚¬", "Ã¢â€", "Ã¢Å", "Ã°Å¸", "�")
RUNNER_SNIPPETS = ("Task tool", "apply_patch tool", "functions.exec", "collaboration.spawn_agent")
ENCODING_SUBSTITUTIONS = (
    re.compile(r"[A-Za-z]\?s\b"),
    re.compile(r"\?(?:adequate|secure|user-friendly)\?", re.I),
    re.compile(r"\)\s+\?\s+apply\b", re.I),
    re.compile(r"\]\([^)]+\)\s+\?\s+"),
)
MANDATORY_ENGINE_RESOURCES = (
    "docs/skill-authoring-standard.md",
    "templates/skill/SKILL.md",
    "tests/skill-quality-baseline.json",
    "tests/routing-fixtures.json",
    "scripts/routing_smoke_test.py",
)
REQUIRED_HEADINGS = (
    "Use When",
    "Do Not Use When",
    "Required Inputs",
    "Workflow",
    "Outputs",
    "Evidence Produced",
    "Capability and permission boundaries",
    "Degraded mode",
    "Decision Rules",
    "Quality Standards",
    "Anti-Patterns",
    "References",
)
AUDIT_WORDS = re.compile(r"\b(audit|review|critique|analysis|assessment|planning|evaluation)\b", re.I)


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--max-skill-bytes",
        type=int,
        default=20480,
        help="report-only SKILL.md size warning threshold in bytes (M10-04-T07); never changes the exit status",
    )
    return parser.parse_args()


def active_roots(root: Path) -> list[Path]:
    return sorted(path for path in root.iterdir() if path.is_dir() and ACTIVE_ROOT_RE.match(path.name) and any(path.rglob("SKILL.md")))


def active_skill_files(root: Path) -> list[Path]:
    """Return the filesystem-backed active entrypoints in stable order."""
    return sorted(
        path
        for active_root in active_roots(root)
        for path in active_root.rglob("SKILL.md")
    )


def active_skill_paths(root: Path) -> list[str]:
    """Return active entrypoint paths used by the catalogue control."""
    return [path.relative_to(root).as_posix() for path in active_skill_files(root)]


def template_files(root: Path) -> list[Path]:
    templates = root / "templates"
    return sorted(templates.rglob("SKILL.md")) if templates.exists() else []


def parse_skill(path: Path) -> tuple[dict, str, str | None]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    match = FRONTMATTER_RE.match(raw)
    if not match:
        return {}, raw, "frontmatter"
    yaml = YAML(typ="safe")
    try:
        frontmatter = yaml.load(match.group(1)) or {}
    except Exception:
        return {}, raw[match.end():], "frontmatter_yaml"
    if not isinstance(frontmatter, dict):
        return {}, raw[match.end():], "frontmatter_type"
    return dict(frontmatter), raw[match.end():], None


def section(body: str, heading: str) -> str | None:
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s|\Z)", body, re.M | re.I)
    return match.group(1).strip() if match else None


def markdown_links(text: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def table_header_has(content: str, required: tuple[str, ...]) -> bool:
    lines = [line.strip().lower() for line in content.splitlines() if line.strip().startswith("|")]
    return bool(lines) and all(term.lower() in lines[0] for term in required)


def assess(path: Path, root: Path) -> list[str]:
    fm, body, parse_error = parse_skill(path)
    raw = path.read_text(encoding="utf-8", errors="replace")
    findings: list[str] = []
    if parse_error:
        return [parse_error]
    if set(fm) - ALLOWED_KEYS:
        findings.append("unsupported_frontmatter_keys")
    if fm.get("name") != path.parent.name:
        findings.append("name_mismatch")
    description = fm.get("description")
    if not isinstance(description, str) or not description.startswith("Use when") or "\n" in description or len(description) > 350:
        findings.append("description_contract")
    metadata = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    if metadata.get("portable") is not True or list(metadata.get("compatible_with", [])) != ["claude-code", "codex"]:
        findings.append("portable_metadata")
    if "<!-- dual-compat-start -->" not in body or "<!-- dual-compat-end -->" not in body:
        findings.append("portable_markers")
    sections = {name: section(body, name) for name in REQUIRED_HEADINGS}
    for name, content in sections.items():
        if not content:
            findings.append("missing_or_empty_" + re.sub(r"\W+", "_", name.lower()).strip("_"))
    inputs = sections.get("Required Inputs") or ""
    if not table_header_has(inputs, ("artefact", "source", "required")) or not re.search(r"\|[^\n]*(missing|absent|unavailable)", inputs, re.I):
        findings.append("input_contract")
    outputs = sections.get("Outputs") or ""
    if not table_header_has(outputs, ("artefact", "consumer", "acceptance")):
        findings.append("output_contract")
    evidence = sections.get("Evidence Produced") or ""
    if not table_header_has(evidence, ("evidence", "acceptance")):
        findings.append("evidence_contract")
    workflow = sections.get("Workflow") or ""
    if len(re.findall(r"^\s*\d+\.\s+", workflow, re.M)) < 3 or not re.search(r"\bstop\b", workflow, re.I) or not re.search(r"\brecover", workflow, re.I):
        findings.append("workflow_contract")
    decision = sections.get("Decision Rules") or ""
    if not table_header_has(decision, ("action", "risk")):
        findings.append("decision_contract")
    capability = sections.get("Capability and permission boundaries") or ""
    if not re.search(r"\b(read|search)\b", capability, re.I) or not re.search(r"authori[sz]|authorit", capability, re.I):
        findings.append("capability_contract")
    if AUDIT_WORDS.search(path.parent.name) and "read-only" not in capability.lower():
        findings.append("audit_not_read_only")
    degraded = sections.get("Degraded mode") or ""
    if not re.search(r"not assessed|unassessed", degraded, re.I) or not re.search(r"narrowest|qualified", degraded, re.I):
        findings.append("degraded_mode")
    anti = sections.get("Anti-Patterns") or ""
    anti_lines = re.findall(r"^\s*[-*]\s+(.+)$", anti, re.M)
    if len(anti_lines) < 5 or any(not re.search(r"\bfix\s*:", line, re.I) for line in anti_lines):
        findings.append("anti_patterns")
    if len(raw.splitlines()) > 500:
        findings.append("line_limit")
    if any(marker in raw for marker in MOJIBAKE):
        findings.append("encoding_noise")
    if any(pattern.search(raw) for pattern in ENCODING_SUBSTITUTIONS):
        findings.append("encoding_substitution")
    if any(snippet in body for snippet in RUNNER_SNIPPETS):
        findings.append("runner_specific_body")
    for target in markdown_links(body):
        clean = target.split("#", 1)[0].strip()
        if not clean or "://" in clean or clean.startswith(("mailto:", "/")):
            continue
        if not (path.parent / clean).resolve().exists():
            findings.append("broken_relative_link")
            break
    refs = sections.get("References") or ""
    if not markdown_links(refs):
        findings.append("references_not_directly_linked")
    return sorted(set(findings))


def baseline_mismatches(payload: dict, baseline: dict) -> list[str]:
    """Compare measured engine state with the explicit baseline control."""
    mismatches: list[str] = []
    for key in ("active_skill_count", "template_count", "failure_counts"):
        if payload[key] != baseline.get(key):
            mismatches.append(
                f"{key}: expected {baseline.get(key)!r}, got {payload[key]!r}"
            )

    expected_paths = baseline.get("active_skill_paths")
    if not isinstance(expected_paths, list) or any(
        not isinstance(path, str) for path in expected_paths
    ):
        mismatches.append(
            "active_skill_paths: baseline must contain a list of relative paths"
        )
    elif payload["active_skill_paths"] != expected_paths:
        missing = sorted(set(expected_paths) - set(payload["active_skill_paths"]))
        unexpected = sorted(
            set(payload["active_skill_paths"]) - set(expected_paths)
        )
        mismatches.append(
            "active_skill_paths: catalogue differs from baseline "
            f"(missing={missing!r}, unexpected={unexpected!r})"
        )
    return mismatches


def main() -> int:
    args = arguments()
    root = args.root.resolve()
    files = active_skill_files(root)
    failures: Counter[str] = Counter()
    results: dict[str, list[str]] = {}
    names: dict[str, list[str]] = {}
    for path in files:
        found = assess(path, root)
        rel = path.relative_to(root).as_posix()
        results[rel] = found
        failures.update(found)
        fm, _, _ = parse_skill(path)
        name = fm.get("name")
        if isinstance(name, str):
            names.setdefault(name, []).append(rel)
    duplicates = {name: paths for name, paths in names.items() if len(paths) > 1}
    if duplicates:
        failures["duplicate_names"] = len(duplicates)
        for paths in duplicates.values():
            for rel in paths:
                results[rel] = sorted(set(results[rel] + ["duplicate_name"]))
    descriptions: dict[str, list[str]] = {}
    for path in files:
        fm, _, _ = parse_skill(path)
        description = fm.get("description")
        if isinstance(description, str):
            descriptions.setdefault(description.strip().lower(), []).append(path.relative_to(root).as_posix())
    duplicate_descriptions = {value: paths for value, paths in descriptions.items() if len(paths) > 1}
    if duplicate_descriptions:
        failures["duplicate_descriptions"] = len(duplicate_descriptions)
        for paths in duplicate_descriptions.values():
            for rel in paths:
                results[rel] = sorted(set(results[rel] + ["duplicate_description"]))
    for template in template_files(root):
        found = assess(template, root)
        if found:
            rel = template.relative_to(root).as_posix()
            results[rel] = found
            failures.update("template_" + item for item in found)
    missing_resources = [resource for resource in MANDATORY_ENGINE_RESOURCES if not (root / resource).exists()]
    if missing_resources:
        failures["missing_engine_resources"] = len(missing_resources)
        results["<engine>"] = ["missing:" + resource for resource in missing_resources]
    payload = {
        "active_roots": [path.name for path in active_roots(root)],
        "active_skill_count": len(files),
        "active_skill_paths": [path.relative_to(root).as_posix() for path in files],
        "template_count": len(template_files(root)),
        "failure_counts": dict(sorted(failures.items())),
        "results": {path: found for path, found in results.items() if found},
        # Report-only size warnings beside the 500-line cap (M10-04-T07, Caveman CV-06);
        # they never enter failure_counts, so the baseline and exit status are unchanged.
        "size_warnings": [
            {"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size}
            for path in files
            if path.stat().st_size > args.max_skill_bytes
        ],
    }
    baseline_errors: list[str] = []
    if args.baseline:
        baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
        baseline_errors.extend(baseline_mismatches(payload, baseline))
        if baseline_errors:
            payload["baseline_errors"] = baseline_errors
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"skill-engine: {root}")
        print(f"- active skills: {payload['active_skill_count']}")
        print(f"- templates: {payload['template_count']}")
        print(f"- failure counts: {payload['failure_counts']}")
        for rel, found in payload["results"].items():
            print(f"- {rel}: {', '.join(found)}")
        for error in baseline_errors:
            print(f"- baseline: {error}")
        for item in payload["size_warnings"]:
            print(f"WARN skill-bytes {item['path']}: {item['bytes']} bytes > {args.max_skill_bytes} (report-only)")
    return 1 if failures or baseline_errors else 0


if __name__ == "__main__":
    sys.exit(main())
