"""A catalogue script run without its pinned YAML package names the cause and exits 2 (NOT_ASSESSED)."""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("script", ["scripts/validate_skill_engine.py", "scripts/routing_smoke_test.py"])
def test_missing_ruamel_is_a_clear_not_assessed_exit(tmp_path: Path, script: str) -> None:
    # An empty `ruamel` package placed first on the path shadows any installed copy and has no `yaml` module.
    (tmp_path / "ruamel").mkdir()
    (tmp_path / "ruamel" / "__init__.py").write_text("", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(ROOT / script)],
        capture_output=True, text=True, cwd=ROOT, env={"PYTHONPATH": str(tmp_path), "PATH": ""},
    )
    assert result.returncode == 2
    assert "ruamel.yaml" in result.stderr and "requirements-ci.txt" in result.stderr
    assert "Traceback" not in result.stderr
