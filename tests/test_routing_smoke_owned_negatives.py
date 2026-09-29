"""Owned negatives, precision@1 floor and fixture lint in routing_smoke_test.py (M10-03)."""

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "routing_smoke_test.py"
SPEC = importlib.util.spec_from_file_location("srs_routing_smoke", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
CATALOGUE = MODULE.read_catalogue()


def run(*args):
    return subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), *args], capture_output=True, text=True, cwd=ROOT)


def test_owner_ranking_below_self_fails():
    seeded = {"id": "seeded", "kind": "negative", "prompt": "Write the SRS for the patient billing module.",
              "skill": "01-initialize-srs", "owner": "19-game-software-requirements-specification"}
    status, _detail = MODULE.evaluate_negative(seeded, CATALOGUE)
    assert status == "FAIL"


def test_owner_above_self_passes_and_cross_engine_owner_is_not_assessed():
    good = {"id": "good", "kind": "negative", "prompt": "Write the SRS for the patient billing module.",
            "skill": "19-game-software-requirements-specification", "owner": "01-initialize-srs"}
    assert MODULE.evaluate_negative(good, CATALOGUE)[0] == "PASS"
    cross = dict(good, owner="social-media-skills/meta-social-media-roi-business-case")
    assert MODULE.evaluate_negative(cross, CATALOGUE)[0] == "NOT_ASSESSED"


def test_lint_flags_slug_and_description_copy():
    assert MODULE.lint_prompt("Draft the 02 business case now", "02-business-case", "")
    description = "Use when mapping requirements to designs, tests, evidence, releases, and approvals"
    assert MODULE.lint_prompt("mapping requirements to designs tests evidence releases and approvals", "01-traceability-matrix", description)
    assert MODULE.lint_prompt("Justify the ERP spend to the board", "02-business-case", description) == []


def test_live_fixtures_pass_floor_and_lint_and_seeded_floor_fails():
    assert run("--min-rank1", "83", "--lint-fixtures").returncode == 0
    assert run("--min-rank1", "99").returncode == 1
