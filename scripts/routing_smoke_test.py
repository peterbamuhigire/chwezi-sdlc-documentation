#!/usr/bin/env python3
"""Rank active skills against representative prompts and enforce top-three routing.

Fixture kinds (tests/routing-fixtures.json):

- positive, collision, failure-path, limited-capability: ``expected`` must rank in the top ``top_k``;
  rank 1 counts towards precision@1 (``--min-rank1`` ratchet, M10-03-T11).
- negative (M10-03-T08): ``skill`` must not rank first with a non-zero score, and ``owner`` must
  rank strictly above ``skill`` with a score above zero. This makes each negative a pairwise test,
  adapted from addyosmani/agent-skills (MIT, https://github.com/addyosmani/agent-skills, commit
  2686b62), paraphrased. An owner written ``<engine-id>/<skill>`` belongs to another engine: it is
  reported NOT_ASSESSED here and evaluated in union mode by chwezi-engine-agents route oracles.

``--coverage`` reports how many active skills have at least three positive prompts and two owned
negatives (a negative that names an owner). The count is also given with cross-engine owners
excluded, because those negatives are `NOT_ASSESSED` here. ``--min-covered N`` fails below N skills.

``--lint-fixtures`` (M10-03-T05) fails a prompt that names its expected skill slug (numeric prefix
stripped, hyphens as spaces) or copies the expected description (word-trigram overlap >= 0.6).

This is a lexical proxy, not live routing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    from ruamel.yaml import YAML
except ModuleNotFoundError:
    sys.stderr.write(
        "ERROR: the Python package 'ruamel.yaml' is not installed, so this check cannot run (NOT_ASSESSED).\n"
        "Install the pinned dependencies: python -m pip install -c requirements-ci.txt -e \".[dev]\"\n"
    )
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "routing-fixtures.json"
TRIGRAM_LIMIT = 0.6
STOP = {
    "a", "an", "and", "are", "as", "at", "be", "before", "by", "do", "for", "from",
    "in", "into", "is", "it", "of", "on", "or", "the", "this", "to", "with", "write",
    "create", "generate", "prepare", "produce", "document", "skill",
}
SYNONYMS = {
    "prioritize": "prioritization", "prioritise": "prioritization", "audit": "auditing",
    "review": "validation", "validate": "validation", "install": "installation",
    "deploy": "deployment", "monitor": "monitoring", "stories": "story",
    "requirements": "requirement", "risks": "risk", "tests": "test",
}
POSITIVE_KINDS = {"positive", "collision", "failure-path", "limited-capability"}
COVERAGE_POSITIVES = 3
COVERAGE_NEGATIVES = 2


def tokens(text: str) -> set[str]:
    found = set(re.findall(r"[a-z0-9]+", text.lower()))
    normal = {SYNONYMS.get(word, word) for word in found if word not in STOP and len(word) > 1}
    return normal


def read_catalogue(root: Path = ROOT) -> list[dict[str, str]]:
    yaml = YAML(typ="safe")
    catalogue: list[dict[str, str]] = []
    for base in sorted(path for path in root.iterdir() if path.is_dir() and re.match(r"^0[1-9]-", path.name)):
        for skill in sorted(base.rglob("SKILL.md")):
            raw = skill.read_text(encoding="utf-8")
            match = re.match(r"^---\n(.*?)\n---", raw, re.S)
            if not match:
                continue
            try:
                fm = yaml.load(match.group(1)) or {}
            except Exception:
                continue
            name = fm.get("name")
            description = fm.get("description")
            if isinstance(name, str) and isinstance(description, str):
                catalogue.append({"name": name, "description": description, "path": skill.parent.relative_to(root).as_posix()})
    return catalogue


def rank(prompt: str, catalogue: list[dict[str, str]]) -> list[tuple[float, str]]:
    prompt_tokens = tokens(prompt)
    ranked: list[tuple[float, str]] = []
    lower = prompt.lower()
    for item in catalogue:
        name_words = tokens(item["name"].replace("-", " "))
        description_words = tokens(item["description"])
        overlap_name = len(prompt_tokens & name_words)
        overlap_description = len(prompt_tokens & description_words)
        phrase = item["name"].replace("-", " ")
        score = overlap_name * 5 + overlap_description * 2 + (8 if phrase in lower else 0)
        specificity = len(name_words) / 1000
        ranked.append((score + specificity, item["name"]))
    return sorted(ranked, key=lambda pair: (-pair[0], pair[1]))


def slug_phrase(slug: str) -> str:
    return re.sub(r"^\d+-", "", slug.lower()).replace("-", " ").strip()


def trigrams(text: str) -> set[tuple[str, ...]]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {tuple(words[i : i + 3]) for i in range(len(words) - 2)}


def lint_prompt(prompt: str, slug: str, description: str) -> list[str]:
    findings: list[str] = []
    normal = " " + re.sub(r"[^a-z0-9]+", " ", prompt.lower()).strip() + " "
    phrase = slug_phrase(slug)
    if phrase and f" {phrase} " in normal:
        findings.append(f"slug-in-prompt '{phrase}'")
    grams = trigrams(prompt)
    if grams:
        overlap = len(grams & trigrams(description)) / len(grams)
        if overlap >= TRIGRAM_LIMIT:
            findings.append(f"description-copy trigram overlap {overlap:.2f}")
    return findings


def evaluate_negative(fixture: dict, catalogue: list[dict[str, str]]) -> tuple[str, str]:
    """Return (status, detail) for one owned negative: PASS, FAIL or NOT_ASSESSED."""
    ranking = rank(fixture["prompt"], catalogue)
    scores = {name: score for score, name in ranking}
    order = [name for _, name in ranking]
    skill = fixture["skill"]
    owner = fixture.get("owner")
    if skill not in scores:
        return "FAIL", f"skill {skill} is not active"
    self_rank = order.index(skill) + 1
    if owner and "/" in owner:
        # The owner lives in another engine, so this catalogue cannot hold the pairwise test.
        return "NOT_ASSESSED", f"cross-engine owner {owner}; evaluated in union mode"
    if self_rank == 1 and scores[skill] >= 1:
        return "FAIL", f"{skill} ranks first ({scores[skill]:.3f})"
    if not owner:
        return "PASS", f"{skill} rank {self_rank}"
    if owner not in scores:
        return "FAIL", f"owner {owner} is not active"
    owner_rank = order.index(owner) + 1
    if scores[owner] < 1 or owner_rank >= self_rank:
        return "FAIL", f"owner {owner} rank {owner_rank} ({scores[owner]:.3f}) does not outrank {skill} rank {self_rank}"
    return "PASS", f"owner {owner} rank {owner_rank} above {skill} rank {self_rank}"


def coverage_report(fixtures: list[dict], active: list[str]) -> dict[str, list[str]]:
    """Skills meeting the fixture target: all owned negatives, and local (same-engine) ones only."""
    names = set(active)
    positives = Counter(f["expected"] for f in fixtures if f.get("kind", "positive") in POSITIVE_KINDS and f.get("expected") in names)
    owned = [f for f in fixtures if f.get("kind") == "negative" and f.get("owner") and f.get("skill") in names]
    any_owner = Counter(f["skill"] for f in owned)
    same_engine = Counter(f["skill"] for f in owned if "/" not in f["owner"])
    return {
        "meeting": sorted(s for s in names if positives[s] >= COVERAGE_POSITIVES and any_owner[s] >= COVERAGE_NEGATIVES),
        "meeting_same_engine": sorted(s for s in names if positives[s] >= COVERAGE_POSITIVES and same_engine[s] >= COVERAGE_NEGATIVES),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=FIXTURES)
    parser.add_argument("--min-rank1", type=float, default=None, help="Fail when precision@1 (percent) falls below this floor.")
    parser.add_argument("--lint-fixtures", action="store_true", help="Fail on prompts that leak the expected slug or copy its description.")
    parser.add_argument("--coverage", action="store_true", help="Report skills with >=3 positives and >=2 owned negatives.")
    parser.add_argument("--min-covered", type=int, default=None, help="Fail when fewer skills than this meet the coverage target (implies --coverage).")
    args = parser.parse_args()
    data = json.loads(args.fixtures.read_text(encoding="utf-8"))
    catalogue = read_catalogue()
    descriptions = {item["name"]: item["description"] for item in catalogue}
    top_k = int(data.get("top_k", 3))
    failures: list[str] = []
    positives = [fixture for fixture in data["fixtures"] if fixture.get("kind", "positive") in POSITIVE_KINDS]
    negatives = [fixture for fixture in data["fixtures"] if fixture.get("kind") == "negative"]
    top1 = 0
    for fixture in positives:
        top = [name for _, name in rank(fixture["prompt"], catalogue)[:top_k]]
        if top and top[0] == fixture["expected"]:
            top1 += 1
        if fixture["expected"] not in top:
            failures.append(f"{fixture['id']}: expected {fixture['expected']}; got {', '.join(top)}")
    negative_status = {"PASS": 0, "FAIL": 0, "NOT_ASSESSED": 0}
    negative_lines: list[str] = []
    for fixture in negatives:
        status, detail = evaluate_negative(fixture, catalogue)
        negative_status[status] += 1
        if status != "PASS":
            negative_lines.append(f"{status} {fixture['id']}: {detail}")
        if status == "FAIL":
            failures.append(f"negative {fixture['id']}: {detail}")
    total = len(positives)
    passed = total - sum(1 for line in failures if not line.startswith("negative "))
    precision = passed / total if total else 0.0
    p_at_1 = 100.0 * top1 / total if total else 0.0
    threshold = float(data["threshold"])
    owned = sum(1 for fixture in negatives if fixture.get("owner"))
    print(
        f"routing-smoke: {passed}/{total} fixtures; top-{top_k} precision={precision:.3f}; threshold={threshold:.3f}; "
        f"precision@1={top1}/{total} ({p_at_1:.1f}%)"
    )
    print(
        f"owned negatives: {owned} (pass={negative_status['PASS']}, fail={negative_status['FAIL']}, "
        f"not_assessed={negative_status['NOT_ASSESSED']} cross-engine)"
    )
    for line in negative_lines:
        print(f"- {line}")
    for failure in failures:
        if not failure.startswith("negative "):
            print(f"- {failure}")
    exit_code = 1 if failures or precision < threshold else 0
    if args.min_rank1 is not None:
        if p_at_1 < args.min_rank1:
            print(f"FAIL precision@1 {p_at_1:.1f}% is below the floor {args.min_rank1:.1f}%")
            exit_code = 1
        else:
            print(f"precision@1 floor {args.min_rank1:.1f}% met")
    if args.coverage or args.min_covered is not None:
        report = coverage_report(data["fixtures"], [item["name"] for item in catalogue])
        print(
            f"route coverage: {len(report['meeting'])} of {len(catalogue)} active skills have "
            f">={COVERAGE_POSITIVES} positives and >={COVERAGE_NEGATIVES} owned negatives "
            f"({len(report['meeting_same_engine'])} with cross-engine owners excluded)"
        )
        if args.min_covered is not None and len(report["meeting"]) < args.min_covered:
            print(f"FAIL route coverage {len(report['meeting'])} is below the floor {args.min_covered}")
            exit_code = 1
    if args.lint_fixtures:
        lint: list[str] = []
        for fixture in positives:
            lint.extend(f"{fixture['id']}: {item}" for item in lint_prompt(fixture["prompt"], fixture["expected"], descriptions.get(fixture["expected"], "")))
        for fixture in negatives:
            owner = fixture.get("owner") or ""
            if owner and "/" not in owner:
                lint.extend(f"{fixture['id']}: {item}" for item in lint_prompt(fixture["prompt"], owner, descriptions.get(owner, "")))
        print(f"fixture lint: {len(lint)} finding(s) over {len(positives) + len(negatives)} prompts")
        for item in lint:
            print(f"LINT {item}")
        if lint:
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
