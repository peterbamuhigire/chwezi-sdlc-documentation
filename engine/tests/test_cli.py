from pathlib import Path
from click.testing import CliRunner
from engine.cli import main


def _seed_clean_project(tmp_path: Path) -> None:
    """Seed a project workspace that passes every gate in _default_registry()."""
    # --- _context (Phase 01) ---
    (tmp_path / "_context").mkdir()
    (tmp_path / "_context/vision.md").write_text(
        "# Vision\nClean.\n", encoding="utf-8"
    )
    (tmp_path / "_context/stakeholders.md").write_text(
        "# Stakeholders\n- Provider Office.", encoding="utf-8"
    )
    (tmp_path / "_context/features.md").write_text(
        "# Features\n- F-1 Submit Claim -- driven by Provider Office",
        encoding="utf-8",
    )
    (tmp_path / "_context/glossary.md").write_text(
        "# Glossary\n- **Claim:** a request for payment.",
        encoding="utf-8",
    )

    # --- Phase 03: design documentation ---
    design = tmp_path / "03-design-documentation"
    (design / "adr").mkdir(parents=True)
    (design / "adr/ADR-001-use-postgres.md").write_text(
        "# ADR-001 Use Postgres\nContext, decision, consequences.",
        encoding="utf-8",
    )
    (design / "03-api-specification").mkdir(parents=True)
    (design / "03-api-specification/claims-api.md").write_text(
        "# Claims API\n- `POST /claims` returns 201.",
        encoding="utf-8",
    )
    (design / "04-database-design").mkdir(parents=True)
    (design / "04-database-design/schema.md").write_text(
        "# Schema\nTable `claims` has PRIMARY KEY `id`.",
        encoding="utf-8",
    )
    (design / "threat-model.md").write_text(
        "# Threat Model\nSTRIDE analysis.", encoding="utf-8"
    )

    # --- Phase 04: development ---
    dev = tmp_path / "04-development"
    dev.mkdir()
    (dev / "coding-standards.md").write_text(
        "# Coding Standards\nUse Black.", encoding="utf-8"
    )
    (dev / "env-setup.md").write_text(
        "# Env Setup\nPrerequisites: Python 3.11. Install: pip install -r "
        "requirements.txt. Verify: pytest.",
        encoding="utf-8",
    )
    # tech-spec is optional (check does not fire without a tech-spec file).
    # Contribution guide at repo root style:
    (tmp_path / "CONTRIBUTING.md").write_text(
        "# Contributing\nPR process.", encoding="utf-8"
    )

    # --- Phase 05: testing ---
    testing = tmp_path / "05-testing-documentation"
    testing.mkdir()
    (testing / "29119-deterministic-checks.md").write_text(
        "# 29119 Deterministic Checks\nApplied.",
        encoding="utf-8",
    )
    (testing / "test-completion-report.md").write_text(
        "# Test Completion\nTested FR-001 with result PASS.",
        encoding="utf-8",
    )
    # Test-plan artifact with frontmatter keys so normative_test_structure
    # passes. Coverage matrix satisfies coverage_measurable.
    (testing / "test-plan").mkdir()
    (testing / "test-plan/tc.md").write_text(
        "---\n"
        "phase: '05'\n"
        "inputs: ['valid claim payload']\n"
        "expected_results: ['claim stored successfully']\n"
        "requirement_trace: ['FR-001']\n"
        "---\n"
        "- **TC-001** covers FR-001",
        encoding="utf-8",
    )
    (testing / "coverage-matrix.md").write_text(
        "# Coverage Matrix\n| FR | TC |\n|---|---|\n| FR-001 | TC-001 |",
        encoding="utf-8",
    )

    # --- Phase 06: deployment & operations ---
    ops = tmp_path / "06-deployment-operations"
    ops.mkdir()
    (ops / "deployment-guide.md").write_text(
        "# Deployment Guide\nSteps... Rollback: revert release tag. "
        "Change window: Saturday 22:00-02:00.",
        encoding="utf-8",
    )
    (ops / "runbook.md").write_text(
        "# Runbook\nEscalation: page on-call via PagerDuty.",
        encoding="utf-8",
    )
    (ops / "monitoring.md").write_text(
        "# Monitoring\nSLO: 99.9% availability; SLI: error rate; "
        "SLA: 99% uptime.",
        encoding="utf-8",
    )
    (ops / "infrastructure.md").write_text(
        "# Infrastructure\nSee IR diagram: "
        "![incident response flow](./ir.png)",
        encoding="utf-8",
    )
    # The phase06 gate requires the figure file to exist (M10-01-T12).
    (ops / "ir.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (ops / "go-live-readiness.md").write_text(
        "# Go-Live Readiness\n- [x] Backups configured\n"
        "- [x] Runbook complete\n- [x] Monitoring live",
        encoding="utf-8",
    )

    # --- Phase 07: agile artifacts ---
    agile = tmp_path / "07-agile-artifacts"
    agile.mkdir()
    (agile / "definition-of-ready.md").write_text(
        "# DoR\nItems ready when scope clear and BG-001 linked.",
        encoding="utf-8",
    )
    (agile / "definition-of-done.md").write_text(
        "# DoD\nDone when security review complete and compliance checked.",
        encoding="utf-8",
    )
    (agile / "sprint-plan.md").write_text(
        "# Sprint Plan\n- **US-001** Login flow (owner: peter)",
        encoding="utf-8",
    )
    (agile / "retrospective.md").write_text(
        "# Retro\n- **A-001** Automate release pipeline "
        "owner: peter due: 2026-06-01",
        encoding="utf-8",
    )
    (agile / "velocity.md").write_text(
        "# Velocity\nsprint-01 delivered 23 points; "
        "sprint-02 delivered 29 points.",
        encoding="utf-8",
    )

    # --- Phase 08: end-user documentation ---
    users = tmp_path / "08-end-user-documentation"
    users.mkdir()
    (users / "user-manual.md").write_text(
        "# User Manual\nHow to submit a claim: "
        "![submit screen](./submit.png)",
        encoding="utf-8",
    )
    (users / "release-notes.md").write_text(
        "# Release Notes v1.0\n- FR-001 implemented.",
        encoding="utf-8",
    )
    (users / "faq.md").write_text(
        "# FAQ\n"
        "## How do I sign up?\nA.\n"
        "## How do I log in?\nA.\n"
        "## How do I reset my password?\nA.\n"
        "## How do I export data?\nA.\n"
        "## How do I contact support?\nA.",
        encoding="utf-8",
    )

    # --- Phase 09: governance ---
    gov = tmp_path / "09-governance-compliance"
    gov.mkdir()
    (gov / "audit-report.md").write_text(
        "# Audit Report\nphase01: PASS. phase03: PASS. phase05: PASS.",
        encoding="utf-8",
    )
    (gov / "risk-register.md").write_text(
        "# Risk Register\n- **R-001** Dependency on third-party API "
        "-- linked to FR-001.",
        encoding="utf-8",
    )
    # No _registry/waivers.yaml -> silent pass for phase09.waivers_have_expiry.


def test_validate_passes_clean_project(tmp_path: Path):
    _seed_clean_project(tmp_path)
    result = CliRunner().invoke(main, ["validate", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "ENGINE CONTRACT: PASS" in result.output


def test_validate_fails_on_unresolved_marker(tmp_path: Path):
    (tmp_path / "_context").mkdir()
    (tmp_path / "_context/vision.md").write_text(
        "# Vision\n[V&V-FAIL: missing oracle]\n"
    )
    result = CliRunner().invoke(main, ["validate", str(tmp_path)])
    assert result.exit_code == 1
    assert "kernel.no_unresolved_fail_markers" in result.output


def test_validate_emits_junit_when_requested(tmp_path: Path):
    _seed_clean_project(tmp_path)
    out_path = tmp_path / "report.xml"
    result = CliRunner().invoke(
        main, ["validate", str(tmp_path), "--junit", str(out_path)]
    )
    assert result.exit_code == 0
    assert out_path.exists()
    assert out_path.read_text().startswith("<testsuite")
