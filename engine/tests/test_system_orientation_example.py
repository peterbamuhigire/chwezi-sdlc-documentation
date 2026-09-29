"""M10-08-T05 (UA-06): every repository path cited in the orientation example resolves."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "04-development-artifacts" / "03-dev-environment-setup"
EXAMPLE = SKILL / "examples" / "system-orientation-guide-srs-engine.md"
_PATH = re.compile(r"`((?:engine)(?:/[A-Za-z0-9_.\-]+)+/?)`")


def _section(text: str, start: str, end: str) -> str:
    return text[text.index(start):text.index(end)]


def test_reading_path_and_file_map_paths_all_resolve() -> None:
    text = EXAMPLE.read_text(encoding="utf-8")
    reading = _section(text, "## 4. Guided Reading Path", "## 5. File Map")
    file_map = _section(text, "## 5. File Map", "## 6. Complexity Hotspots")
    cited = set(_PATH.findall(reading)) | set(_PATH.findall(file_map))
    assert len(cited) >= 12
    unresolved = sorted(p for p in cited if not (ROOT / p).exists())
    assert unresolved == []


def test_reading_path_has_5_to_15_steps() -> None:
    text = EXAMPLE.read_text(encoding="utf-8")
    reading = _section(text, "## 4. Guided Reading Path", "## 5. File Map")
    steps = re.findall(r"^### Step \d+ ", reading, re.M)
    assert 5 <= len(steps) <= 15


def test_frontmatter_pins_and_referenced_paths_resolve() -> None:
    text = EXAMPLE.read_text(encoding="utf-8")
    assert re.search(r'^generated_from_commit: "[0-9a-f]{40}"$', text, re.M)
    assert re.search(r"^source_repository: ", text, re.M)
    refs = re.findall(r"^  - (engine/\S+)$", text, re.M)
    assert refs and all((ROOT / r).exists() for r in refs)


def test_template_and_reference_are_present_and_linked() -> None:
    assert (SKILL / "templates" / "system-orientation-guide.md").is_file()
    assert (SKILL / "references" / "system-orientation-guide.md").is_file()
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "references/system-orientation-guide.md" in skill
    template = (SKILL / "templates" / "system-orientation-guide.md").read_text(encoding="utf-8")
    for key in ("generated_from_commit", "source_repository", "referenced_paths"):
        assert key in template
