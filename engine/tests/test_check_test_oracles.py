from pathlib import Path

import pytest

from engine.artifact_graph import ArtifactGraph
from engine.checks.test_oracles import TestOraclesCheck
from engine.findings import FindingCollection
from engine.workspace import Workspace


def _findings(tmp_path: Path, trace: list[str]) -> list:
    (tmp_path / "_context").mkdir()
    folder = tmp_path / "05-testing-documentation"
    folder.mkdir()
    entries = "".join(f"  - {item}\n" for item in trace)
    (folder / "tc.md").write_text(
        "---\nphase: \"05\"\ninputs:\n  - one confirmed payment\nexpected_results:\n  - one receipt issued\n"
        f"requirement_trace:\n{entries}---\n# Test Case TC-001\n",
        encoding="utf-8",
    )
    findings = FindingCollection()
    TestOraclesCheck("phase05.test_oracles").run(ArtifactGraph.build(Workspace.load(tmp_path)), findings)
    return list(findings)


@pytest.mark.parametrize("identifier", [
    "FR-001", "NFR-001", "IR-010", "DR-004", "CON-002", "FR-META-006", "NFR-PLAT-002", "FR-12345",
])
def test_requirement_identifiers_are_valid_trace_targets(tmp_path: Path, identifier: str) -> None:
    assert _findings(tmp_path, [identifier]) == []


@pytest.mark.parametrize("token", ["BG-001", "TC-001", "FR-1", "fr-001", "NFR-", "FR-001-extra", "REQ-001"])
def test_non_requirement_tokens_are_still_rejected(tmp_path: Path, token: str) -> None:
    items = _findings(tmp_path, [token])
    assert len(items) == 1
    assert token in items[0].message
    assert "non-requirement" in items[0].message


def test_one_bad_entry_among_good_ones_is_the_only_one_reported(tmp_path: Path) -> None:
    items = _findings(tmp_path, ["FR-001", "NFR-002", "BG-001"])
    assert len(items) == 1
    assert "BG-001" in items[0].message and "NFR-002" not in items[0].message
