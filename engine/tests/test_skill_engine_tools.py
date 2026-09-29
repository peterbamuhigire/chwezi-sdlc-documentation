from __future__ import annotations

import importlib.util
import json
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_script(name: str):
    path = ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location(name.removesuffix(".py"), path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_baseline() -> dict:
    return json.loads((ROOT / "tests" / "skill-quality-baseline.json").read_text(encoding="utf-8"))


def test_zero_debt_baseline_and_routing_fixture_contract() -> None:
    baseline = load_baseline()
    fixtures = json.loads((ROOT / "tests" / "routing-fixtures.json").read_text(encoding="utf-8"))

    assert baseline["failure_counts"] == {}
    assert baseline["active_skill_count"] == len(baseline["active_skill_paths"])
    assert baseline["active_skill_paths"] == sorted(set(baseline["active_skill_paths"]))
    assert baseline["template_count"] == 1
    assert len(fixtures["fixtures"]) == baseline["routing"]["fixture_count"]
    assert fixtures["threshold"] == baseline["routing"]["minimum_precision"] == 1.0
    assert {item["kind"] for item in fixtures["fixtures"]} == {
        "positive",
        "collision",
        "limited-capability",
        "failure-path",
        "negative",  # M10-03-T08 owned negatives
    }
    assert len({item["id"] for item in fixtures["fixtures"]}) == len(fixtures["fixtures"])


def test_validator_rejects_an_empty_nonportable_skill(tmp_path: Path) -> None:
    validator = load_script("validate_skill_engine.py")
    skill_dir = tmp_path / "bad-skill"
    skill_dir.mkdir()
    skill = skill_dir / "SKILL.md"
    skill.write_text("---\nname: wrong\ndescription: vague\n---\n\n# Bad\n", encoding="utf-8")

    findings = validator.assess(skill, tmp_path)

    assert "name_mismatch" in findings
    assert "description_contract" in findings
    assert "portable_metadata" in findings
    assert "portable_markers" in findings
    assert "input_contract" in findings
    assert "output_contract" in findings
    assert "degraded_mode" in findings


def test_routing_catalogue_is_unique_and_complete() -> None:
    routing = load_script("routing_smoke_test.py")
    validator = load_script("validate_skill_engine.py")
    baseline = load_baseline()
    catalogue = routing.read_catalogue()
    names = [item["name"] for item in catalogue]
    expected_count = baseline["active_skill_count"]
    active_skill_files = validator.active_skill_files(ROOT)
    active_skill_paths = [skill.relative_to(ROOT).as_posix() for skill in active_skill_files]

    assert len(active_skill_files) == expected_count
    assert active_skill_paths == baseline["active_skill_paths"]
    assert len(catalogue) == expected_count
    assert len(validator.template_files(ROOT)) == baseline["template_count"]
    assert len(names) == len(set(names))


def test_catalogue_control_rejects_unregistered_growth_even_when_count_matches() -> None:
    validator = load_script("validate_skill_engine.py")
    baseline = {
        "active_skill_count": 1,
        "active_skill_paths": ["01-strategic-vision/approved/SKILL.md"],
        "template_count": 0,
        "failure_counts": {},
    }
    measured = {
        "active_skill_count": 1,
        "active_skill_paths": ["01-strategic-vision/unauthorised/SKILL.md"],
        "template_count": 0,
        "failure_counts": {},
    }

    mismatches = validator.baseline_mismatches(measured, baseline)

    assert mismatches
    assert "unexpected=['01-strategic-vision/unauthorised/SKILL.md']" in mismatches[0]
    assert "missing=['01-strategic-vision/approved/SKILL.md']" in mismatches[0]


def test_coverage_policy_is_configured_and_dev_installable() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    addopts = pyproject["tool"]["pytest"]["ini_options"]["addopts"]
    dev_dependencies = pyproject["project"]["optional-dependencies"]["dev"]

    assert "--cov=engine" in addopts
    assert "--cov-fail-under=90" in addopts
    assert any(dependency.startswith("pytest-cov") for dependency in dev_dependencies)
