#!/usr/bin/env python3
"""Render a traced agent build brief from an approved SRS workspace.

The brief is written beside the SDD hand-off record: in ``--feature-dir`` when
given, otherwise in the project directory, unless ``--out`` names a file.
It never edits the SRS; regenerate it whenever the SRS changes.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from engine.agent_brief import BRIEF_NAME, collect, untraced, write_brief


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True,
                        help="Project workspace holding the approved SRS")
    parser.add_argument("--feature-dir", type=Path, default=None,
                        help="Feature directory holding sdd-handoff.json")
    parser.add_argument("--out", type=Path, default=None, help="Explicit output file")
    args = parser.parse_args()
    out = args.out or ((args.feature_dir / BRIEF_NAME) if args.feature_dir else None)
    output = write_brief(args.project, out)
    entries = collect(args.project)
    gaps = sum(1 for e in entries if e.is_gap)
    print(f"Created agent build brief: {output}")
    print(f"entries={len(entries)} untraced={len(untraced(entries))} context_gaps={gaps}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
