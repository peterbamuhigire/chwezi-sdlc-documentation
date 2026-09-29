"""M10-08-T09: the pairwise worked example covers every allowed 2-way pair.

Parses the ``pairwise-model`` block and the "Pairwise test set" table from the
test-plan reference and checks the coverage claim mechanically.
"""
from __future__ import annotations

import itertools
import re
from pathlib import Path

REF = (Path(__file__).resolve().parents[2] / "05-testing-documentation" / "02-test-plan"
       / "references" / "pairwise-combinatorial-test-design.md")


def _model(text: str):
    block = re.search(r"```pairwise-model\n(.*?)```", text, re.S).group(1)
    params: dict[str, list[str]] = {}
    constraints = []
    for line in block.splitlines():
        line = line.strip()
        if line.startswith("param "):
            name, values = line[len("param "):].split(":", 1)
            params[name.strip()] = [v.strip() for v in values.split("|")]
        elif line.startswith("constraint:"):
            cond, then = line[len("constraint:"):].split("->")
            a, av = (s.strip() for s in cond.split("="))
            b, bv = (s.strip() for s in then.split("="))
            constraints.append((a, av, b, bv))
    return params, constraints


def _table(text: str, names: list[str]) -> list[dict[str, str]]:
    section = text.split("### Pairwise test set", 1)[1]
    rows = [ln for ln in section.splitlines() if ln.startswith("| PW-")]
    out = []
    for ln in rows:
        cells = [c.strip() for c in ln.strip("|").split("|")]
        out.append(dict(zip(names, cells[1:])))
    return out


def _allowed(row: dict[str, str], constraints) -> bool:
    return all(row.get(a) != av or row.get(b) == bv for a, av, b, bv in constraints)


def test_pairwise_example_covers_all_allowed_pairs():
    text = REF.read_text(encoding="utf-8")
    params, constraints = _model(text)
    names = list(params)
    assert len(names) >= 4
    assert len(constraints) >= 1
    rows = _table(text, names)
    full_product = 1
    for values in params.values():
        full_product *= len(values)
    assert full_product == 36
    for row in rows:
        assert set(row) == set(names)
        for n in names:
            assert row[n] in params[n], (n, row[n])
        assert _allowed(row, constraints), row

    covered = {((a, row[a]), (b, row[b]))
               for row in rows for a, b in itertools.combinations(names, 2)}
    missing = []
    for a, b in itertools.combinations(names, 2):
        for av in params[a]:
            for bv in params[b]:
                # A pair is allowed if some full combination containing it satisfies the constraints.
                others = [n for n in names if n not in (a, b)]
                feasible = any(
                    _allowed({a: av, b: bv, **dict(zip(others, combo))}, constraints)
                    for combo in itertools.product(*(params[o] for o in others)))
                if feasible and ((a, av), (b, bv)) not in covered:
                    missing.append((a, av, b, bv))
    assert missing == []
    assert len(rows) < full_product
    assert len(rows) == 9  # recorded case count against the full product of 36
