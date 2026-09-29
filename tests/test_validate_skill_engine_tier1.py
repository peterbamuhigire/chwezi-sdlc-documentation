"""Crafted fixtures for the Tier-1 lint refinements in validate_skill_engine.py (M10-03-T12)."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_skill_engine.py"
SPEC = importlib.util.spec_from_file_location("validate_skill_engine", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
TEMPLATE = (ROOT / "templates" / "skill" / "SKILL.md").read_text(encoding="utf-8")
DESCRIPTION = "description: Use when creating the named SDLC artefact; use the nearest phase neighbour when it owns a different decision or deliverable."


def make_skill(tmp_path: Path, text: str) -> Path:
    (tmp_path / "docs").mkdir(exist_ok=True)
    (tmp_path / "docs" / "skill-authoring-standard.md").write_text("standard", encoding="utf-8")
    folder = tmp_path / "group" / "skill"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "SKILL.md"
    path.write_text(text, encoding="utf-8")
    return path


def test_template_is_clean(tmp_path):
    assert MODULE.assess(make_skill(tmp_path, TEMPLATE), tmp_path) == []


def test_heading_inside_a_fence_does_not_satisfy_a_section(tmp_path):
    body = TEMPLATE.replace("## Quality Standards", "```markdown\n## Quality Standards")
    body = body.replace("## Anti-Patterns", "```\n\n## Anti-Patterns")
    assert "missing_or_empty_quality_standards" in MODULE.assess(make_skill(tmp_path, body), tmp_path)


def test_fenced_sample_does_not_break_real_sections(tmp_path):
    body = TEMPLATE.replace("## References", "```text\n## Workflow\n1. sample only\n```\n\n## References")
    assert MODULE.assess(make_skill(tmp_path, body), tmp_path) == []


def test_negated_only_trigger_fails(tmp_path):
    text = TEMPLATE.replace(DESCRIPTION, "description: Use when. Do not use when drafting a PRD or a vision.")
    assert "description_trigger_negated_only" in MODULE.assess(make_skill(tmp_path, text), tmp_path)


def test_positive_trigger_with_negated_clause_passes(tmp_path):
    text = TEMPLATE.replace(DESCRIPTION, "description: Use when writing the release test plan; do not use when setting the programme test strategy.")
    assert MODULE.assess(make_skill(tmp_path, text), tmp_path) == []


def test_host_strict_yaml_subset(tmp_path):
    colon = TEMPLATE.replace(DESCRIPTION, "description: Use when a new ERP needs this: costs and benefits for the board.")
    assert "frontmatter_unquoted_colon" in MODULE.assess(make_skill(tmp_path, colon), tmp_path)
    tab = TEMPLATE.replace("  portable: true", "\tportable: true")
    found = MODULE.assess(make_skill(tmp_path, tab), tmp_path)
    assert "frontmatter_tab" in found or "frontmatter_yaml" in found
    unclosed = TEMPLATE.replace(DESCRIPTION, 'description: "Use when creating the named SDLC artefact for the board')
    found = MODULE.assess(make_skill(tmp_path, unclosed), tmp_path)
    assert "frontmatter_unclosed_quote" in found or "frontmatter_yaml" in found
    quoted = TEMPLATE.replace(DESCRIPTION, 'description: "Use when a new ERP needs this: costs and benefits for the board."')
    assert MODULE.assess(make_skill(tmp_path, quoted), tmp_path) == []


def test_exemptions_live_in_the_validator_not_frontmatter(tmp_path, monkeypatch):
    text = TEMPLATE.replace("metadata:", "lint-exempt: [anti_patterns]\nmetadata:")
    assert "unsupported_frontmatter_keys" in MODULE.assess(make_skill(tmp_path, text), tmp_path)
    broken = TEMPLATE.replace("## Anti-Patterns", "## Anti Patterns Removed")
    path = make_skill(tmp_path, broken)
    assert "missing_or_empty_anti_patterns" in MODULE.assess(path, tmp_path)
    monkeypatch.setattr(MODULE, "EXEMPTIONS", {"group/skill/SKILL.md": {"missing_or_empty_anti_patterns": "crafted test", "anti_patterns": "crafted test"}})
    assert "missing_or_empty_anti_patterns" not in MODULE.assess(path, tmp_path)
    monkeypatch.setattr(MODULE, "EXEMPTIONS", {"gone/SKILL.md": {"anti_patterns": ""}})
    assert len(MODULE.stale_exemptions(tmp_path)) == 2


def test_live_catalogue_has_no_findings():
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT), "--json", "--baseline", str(ROOT / "tests" / "skill-quality-baseline.json")],
        capture_output=True, text=True, cwd=ROOT,
    )
    payload = json.loads(result.stdout)
    assert payload["failure_counts"] == {}
    assert result.returncode == 0


def _with_reference(link: str) -> str:
    anchor = "- [Skill authoring and release standard](../../docs/skill-authoring-standard.md)"
    return TEMPLATE.replace(anchor, anchor + "\n- [Other engine](" + link + ")")


def test_sibling_engine_link_is_broken_even_when_the_sibling_exists(tmp_path):
    repo = tmp_path / "srs-skills"
    repo.mkdir()
    sibling = tmp_path / "chwezi-dev-engine" / "references"
    sibling.mkdir(parents=True)
    (sibling / "standard.md").write_text("sibling", encoding="utf-8")
    body = _with_reference("../../../chwezi-dev-engine/references/standard.md")
    assert "broken_relative_link" in MODULE.assess(make_skill(repo, body), repo)


def test_host_absolute_link_is_broken_even_when_the_target_exists(tmp_path):
    repo = tmp_path / "srs-skills"
    repo.mkdir()
    target = tmp_path / "outside.md"
    target.write_text("outside", encoding="utf-8")
    # On Windows the drive-letter path exists; on a Linux runner it never does. Both must fail.
    link = target.resolve().as_posix() if target.resolve().drive else "C:/wamp64/www/outside.md"
    body = _with_reference(link)
    assert "broken_relative_link" in MODULE.assess(make_skill(repo, body), repo)


def test_github_url_to_another_engine_is_accepted(tmp_path):
    body = _with_reference("https://github.com/peterbamuhigire/chwezi-dev-engine/blob/main/references/standard.md")
    assert MODULE.assess(make_skill(tmp_path, body), tmp_path) == []
