from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "scripts" / "build-doc.sh"


def build_shell() -> str:
    if os.name == "nt":
        git = shutil.which("git")
        if git:
            git_bash = Path(git).resolve().parents[1] / "bin" / "bash.exe"
            if git_bash.is_file():
                return str(git_bash)
    return "bash"


@pytest.mark.skipif(
    shutil.which("pandoc") is None or importlib.util.find_spec("docx") is None,
    reason="Pandoc and python-docx are required for the clean-template build test",
)
def test_clean_build_writes_actual_contents_and_uses_temporary_template(tmp_path: Path) -> None:
    doc_dir = tmp_path / "document"
    doc_dir.mkdir()
    (doc_dir / "01-srs.md").write_text(
        "# Example SRS\n\n## Purpose\nBody.\n\n## Acceptance\nEvidence.\n",
        encoding="utf-8",
    )
    override = tmp_path / "missing-reference.docx"
    env = os.environ.copy()
    env["BUILD_DOC_TEMPLATE"] = str(override)
    env["PYTHON"] = Path(sys.executable).as_posix()
    result = subprocess.run(
        [build_shell(), BUILD.as_posix(), doc_dir.as_posix(), "Example"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    output = tmp_path / "Example.docx"
    assert output.is_file()
    assert not override.exists()

    from docx import Document

    doc = Document(output)
    text = [paragraph.text for paragraph in doc.paragraphs]
    assert text[:4] == ["Contents", "Example SRS", "Purpose", "Acceptance"]
    assert doc.styles["Normal"].font.name == "Public Sans"
    assert doc.styles["Heading 1"].font.name == "Source Serif 4"

    import zipfile

    with zipfile.ZipFile(output) as archive:
        xml = archive.read("word/document.xml").decode("utf-8")
    assert "TOC" not in xml
    assert xml.count("<w:hyperlink") >= 3


def test_build_failure_names_missing_pandoc(tmp_path: Path) -> None:
    doc_dir = tmp_path / "document"
    doc_dir.mkdir()
    (doc_dir / "01-srs.md").write_text("# Example\n", encoding="utf-8")
    env = os.environ.copy()
    env["BUILD_DOC_TEMPLATE"] = str(tmp_path / "missing-reference.docx")
    env["PYTHON"] = Path(sys.executable).as_posix()
    # Simulate only the missing dependency, regardless of where Pandoc is installed.
    missing_pandoc = (
        'command() { if [[ "$1" == -v && "$2" == pandoc ]]; then return 1; fi; '
        'builtin command "$@"; }; source "$@"'
    )
    result = subprocess.run(
        [build_shell(), "-c", missing_pandoc, "bash", BUILD.as_posix(), doc_dir.as_posix(), "Example"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    assert "Pandoc is required" in result.stderr
