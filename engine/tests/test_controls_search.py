"""Tests for the read-only controls search (M10-08-T10)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from engine.cli import main
from engine.controls_search import ABSTAIN_THRESHOLD, load_controls, search, tokenise

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = json.loads(
    (Path(__file__).parent / "fixtures" / "controls_search_queries.json").read_text(encoding="utf-8")
)


def test_corpus_holds_all_registered_controls():
    controls = load_controls(ROOT)
    assert len(controls) >= 39
    assert all(c.registry_path.startswith("domains/") for c in controls)


def test_cardholder_encryption_in_finance_returns_fin_001_first():
    r = search("cardholder encryption", root=ROOT, domain="finance")
    assert r["abstained"] is False
    assert r["results"][0]["id"] == "CTRL-FIN-001"
    assert r["results"][0]["registry_path"] == "domains/finance/controls/control-register.yaml"


def test_nonsense_query_abstains_with_no_results():
    r = search("purple elephant tariff", root=ROOT)
    assert r["abstained"] is True
    assert r["results"] == []


def test_framework_filter_limits_results():
    r = search("encryption of health information at rest", root=ROOT, framework="hipaa")
    assert r["results"]
    assert all("hipaa" in h["framework"].lower() for h in r["results"])
    assert r["results"][0]["id"] == "CTRL-HC-002"


def test_domain_filter_is_case_insensitive():
    r = search("cardholder encryption", root=ROOT, domain="Retail")
    assert [h["domain"] for h in r["results"]] == ["retail"] * len(r["results"])


def test_fixture_threshold_matches_module():
    assert FIXTURE["calibration"]["threshold"] == ABSTAIN_THRESHOLD


@pytest.mark.parametrize("case", FIXTURE["positives"], ids=lambda c: c["query"])
def test_calibration_positives_rank_expected_first(case):
    r = search(case["query"], root=ROOT, domain=case.get("domain"))
    assert r["abstained"] is False
    assert r["results"][0]["id"] == case["expected_first"]


@pytest.mark.parametrize("query", FIXTURE["nonsense"])
def test_calibration_nonsense_abstains(query):
    r = search(query, root=ROOT)
    assert r["abstained"] is True and r["results"] == []


def test_tokenise_drops_stopwords_and_lowercases():
    assert tokenise("Encrypt THE Cardholder data") == ["encrypt", "cardholder"]


def test_cli_json_and_text_output():
    runner = CliRunner()
    res = runner.invoke(main, ["controls", "search", "cardholder encryption",
                               "--domain", "finance", "--json"])
    assert res.exit_code == 0
    assert json.loads(res.output)["results"][0]["id"] == "CTRL-FIN-001"
    res = runner.invoke(main, ["controls", "search", "cardholder encryption", "--top", "2"])
    assert res.exit_code == 0 and "domains/" in res.output
    res = runner.invoke(main, ["controls", "search", "purple elephant tariff"])
    assert res.exit_code == 0 and res.output.startswith("ABSTAINED")
