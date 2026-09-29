# Measured evidence

Host: Windows 11, Python 3.13.7, Git Bash. Engine root `C:\wamp64\www\srs-skills`, HEAD `fa85fba`,
working tree clean before and after the runs. Environment: `PYTHONDONTWRITEBYTECODE=1`. Date:
29 September 2026.

## Validators run by the auditor

| # | Command | Exit | Key output |
|---:|---|---:|---|
| 1 | `python -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | 0 | `active skills: 159`; `templates: 1`; `failure counts: {}`; 6 report-only `WARN skill-bytes` (largest `03-design-documentation/05-ux-specification/SKILL.md: 33701 bytes > 20480`) |
| 2 | `python -X utf8 scripts/routing_smoke_test.py --min-rank1 83 --lint-fixtures` | 0 | `routing-smoke: 55/55 fixtures; top-3 precision=1.000; threshold=1.000; precision@1=47/55 (85.5%)`; `owned negatives: 16 (pass=13, fail=0, not_assessed=3 cross-engine)`; `precision@1 floor 83.0% met`; `fixture lint: 0 finding(s) over 71 prompts` |
| 3 | `python -m engine validate-skills` | 0 | `SKILLS OK: no legacy path references outside alias-blocks.` |
| 4 | `python -X utf8 -m pytest -q -p no:cacheprovider` (full suite, 2 min 56 s) | 0 | 434 collected: 432 passed, 2 skipped. `Required test coverage of 90% reached. Total coverage: 96.86%` |
| 5 | `python -X utf8 scripts/check_docx_diagrams.py --scan projects --exclude _kaizen,render-runs` (read-only) | 1 | `Scanned 691 .docx file(s); 0 contain Mermaid source.` `Figure check: 18 .docx file(s) matched a render manifest; 2 missing rendered figures.` Both are `FIGURE-PLACEHOLDER` entries for `GarageFlow_UserDocs_v1.0.docx` (phase folder and `export/`), caption "Garage Manager App home screen — screenshot pending first build". The screenshot is the client owner's to supply. Exit 1 is the guard working correctly, not an engine defect. |
| 6 | `python -X utf8 scripts/source_ingestion_guardrail.py` (additional) | 0 | `findings: 0` |
| 7 | `python -X utf8 scripts/validate_engine.py` (additional) | 0 | `ENGINE CONTRACT: PASS` |

The declared catalogue validators (`chwezi-engine-agents/catalog/engines.yaml`) are #1 and
`routing_smoke_test.py`. Both pass locally, so T1 = 2/2.

## Remote CI (read-only `gh`)

`gh run list -L 5` at HEAD: `source-ingestion-guardrail` success, and **`Engine` failure** (run
36520102250, commit `fa85fba`). The two previous commits also failed `Engine`.
`gh run view 36520102250 --log-failed`:

```text
- failure counts: {'broken_relative_link': 1}
- 02-requirements-engineering/hospitality-operating-model-srs/SKILL.md: broken_relative_link
- baseline: failure_counts: expected {}, got {'broken_relative_link': 1}
##[error]Process completed with exit code 1.
```

Cause: lines 156–157 of that SKILL.md link to `C:/wamp64/www/chwezi-accounting-doctrine/README.md`
and `C:/wamp64/www/chwezi-dev-engine/skills/product-business/hospitality-hotel-restaurant-systems/SKILL.md`.
These resolve on this host and not on the CI runner, which is why validator #1 passes locally and
fails in CI.

## Engine Eval Readiness arithmetic

Inputs are from `chwezi-engine-agents/docs/operations/m10-kaizen-evidence/M10-14/eval-readiness.json`,
`readiness/tier1-results.json`, `readiness/coverage.json` and `readiness/collision-scan.json`. T1
and T2_p1 were cross-checked against runs #1 and #2 above.

| Slot | Input | Fraction |
|---|---|---:|
| T1 | 2 of 2 declared validators pass (exit 0 locally; the evidence file records the same at `fa85fba`) | 1.0000 |
| T2_p1 | 47 / 55 | 0.8545 |
| T2_neg | 13 local passes + 3 cross-engine mirrors passing in the union oracles = 16 / 16 | 1.0000 |
| T2_cov | Skills with ≥ 3 positives and ≥ 2 owned negatives: 0 / 159 (46 skills have a positive; 12 have an owned negative) | 0.0000 |
| T2_clean | 1 cross-engine pair ≥ 0.75 involving srs (`digital-research-skills/ai-slop-audit` ↔ `srs-skills/29-ai-slop-audit`, 0.7895), declared `canonical_owner`; 0 undeclared | 1.0000 |
| T3 | 0 grading files; every planned run NOT_ASSESSED (zero-spend rule) | 0 |

- T1 points = 30 × 1.0000 = **30.00**
- T2 mean = (0.8545 + 1.0000 + 0.0000 + 1.0000) ÷ 4 = 2.8545 ÷ 4 = 0.71364. T2 points = 40 × 0.71364 = **28.55**. The evidence file rounds this to 28.54, and the difference is rounding only.
- T3 points = 30 × 0 = **0.00**
- **Readiness = 58.5 / 100.** The auditor **agrees** with the executor's figure.

Lexical T2 figures are a drift guard, not proof of live routing.

Note on T2_clean: the union scan reports the undeclared pair
`proposal-skills/hospitality-hotel-restaurant` ↔ `srs-skills/hospitality-operating-model-srs` at
0.7411. It sits just below the 0.75 gate, so it does not count, but it is one wording change away
from failing.

## Other measured facts used in scoring

- Real `examples/` folders: 4/159 skills (`git ls-files` inventory).
- `## Worked Example` headings: 81 SKILL.md files. The identical "Given an approved project source
  and a conflicting implementation detail..." paragraph appears in 34.
- Generic contract workflow ("Apply the decision rules below before drafting; stop on a missing
  authority"): 28 SKILL.md files.
- Skills with no own `references/` files: 43/159.
- Skills citing IEEE 830: 18; citing 29148: 38; authoring typed diagram IR: 3; mentioning Mermaid: 16.
- Unresolved dev-engine skill names: `mysql-best-practices` (4 mentions), `api-error-handling` (2),
  `api-pagination` (2). Checked against `C:\wamp64\www\chwezi-dev-engine\skills\*\*`.

## NOT_ASSESSED list

| Item | Cause | Effect |
|---|---|---|
| Tier 3 behavioural runs | Zero-spend rule; 0 `grading.json` files | 30 points of Readiness lost; ceiling 70 |
| Live (model-executed) routing | Zero-spend rule; only lexical T2 available | T2 is treated as a drift guard |
| Rendered-DOCX visual quality | Client DOCX not opened, by instruction | Render dimension judged from pipeline code and scan only |
| Fan-in per skill (`skill_fanin.py`) | Not run in this audit | Not used in scoring |
| Standards editions (42010, 1058, 1012, 730, 26514, 1233) | No fresh external research | Standards currency judged from the engine's own records |
| Portfolio craft-standard acceptance evidence | Absent for every engine in this Kaizen | Published cap of 65 applies (does not bind here) |
| Stakeholder approval, production execution | Outside repository evidence | Not scored |
