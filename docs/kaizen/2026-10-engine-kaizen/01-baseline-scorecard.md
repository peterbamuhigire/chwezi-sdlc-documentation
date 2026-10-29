# Frozen baseline scorecard — fresh ten-dimension snapshot

**Frozen:** 2026-10-29 before implementation. **Checkout:** clean `kaizen/2026-10` at `b3b08b5`. **Scope:** baseline only; no engine source edits yet. Each rating is a fresh reviewer judgement against the named evidence below, informed by current validators, task artefacts and primary-source checks. This cycle uses a simple arithmetic mean of the ten dimensions because the Portfolio Kaizen Standard requires ten ratings but supplies no aggregate weights. Scores have judgement uncertainty; they are not measurements of customer satisfaction or release quality.

| Standard dimension | Fresh rating /100 | Evidence and deficiency statement |
|---|---:|---|
| Doctrine | 62 | `AGENTS.md`, phase rules and Kaizen guidance give explicit evidence, safety and handoff boundaries; standards are inconsistently attributed across router, registry and gates, and a clean checkout cannot build DOCX without a separately generated ignored template. |
| Taxonomy and routing | 56.8 | 159 active phase skills validate structurally; routing p@1 is 47/55 (85.5%) and CI smoke has zero lint findings, but 0/159 skills meet the 3-positive/2-owned-negative coverage target and 3 cross-engine negatives remain unassessed. |
| Skill depth | 55 | Latest measured audit records 43 skills without local references and current static check confirms 34 identical generic worked-example paragraphs; strong generic contracts do not close domain-specific workflow gaps. |
| Applied proof | 42 | 4/159 skills have an `examples/` folder; 81 headings include 34 identical boilerplate paragraphs; task prototypes exist only in temp and are not standardized engine proof. |
| Standards currency | 38 | Primary records show current published editions, but six Phase 02 and one Phase 09 registry rows still cite IEEE 830-1998; engine Phase 03 cites withdrawn 42010:2011 and Phase 05 cites withdrawn 29119-3:2013; legal currency is only partial through 2023 for the Act. |
| Output readiness | 52 | Task 1 Phase 01/02 passes and generates an SRS with explicit gaps; Task 3 has static 10/10 design/test links but seven requirements await decision inputs, and Task 2 contradiction handling was manual, not gate evidence. |
| Accessibility and inclusion | 52 | Design guidance and WCAG 2.2 routes exist; generated PDF is tagged but its TOC is empty and no native Word accessibility or font-embedding check was completed. |
| Production and handoff | 43 | `scripts/build-doc.sh` fails in a clean checkout because ignored `templates/reference.docx` is absent; temporary regeneration yields DOCX/PDF, but the blank TOC requires correction and visual/font fidelity is not assessed. |
| Hygiene | 44 | Three dev-engine skill names remain dangling in SRS text; standards references are stale. The previously reported hospitality drive path was not found in that skill. |
| Safety and integrity | 58 | Anti-invention, permission and gate-failure contracts are explicit; current legal status, cross-engine target resolution, archival verification and actual model runtime identity remain partial or unassessed. |

**Raw score:** (62 + 56.8 + 55 + 42 + 38 + 52 + 52 + 43 + 44 + 58) ÷ 10 = **50.28/100**.

**Portfolio Standard published score:** `min(50.28, 65) = 50.28/100` (displayed 50.3). The cap does not bind. **User-initial-cap view:** `min(50.28, 45) = 45/100`. Raw ratings are unchanged; this second value is a reporting cap, not a scoring adjustment.

The 2026-09-29 audit published 54.6 under a different weighted rubric. Neither comparison implies measured regression. The prior score is historical context and is not reused in this frozen calculation.

## Measured inputs

| Measure | Current result | Evidence |
|---|---|---|
| Active skills / templates | 159 / 1 | `validate_skill_engine.txt` |
| Catalogue validator | Exit 0; failure counts `{}`; 5 report-only byte warnings | `validators/validate_skill_engine.txt` |
| Routing p@1 | 47/55 = 85.5%; top-3 55/55 | `validators/routing_smoke_test.txt` |
| Owned negatives | 13 pass, 0 fail, 3 cross-engine `NOT_ASSESSED` | `validators/routing_smoke_test.txt` |
| Fixture inventory/coverage | 71 prompts; 31 positives, 16 negatives, 20 collisions, 2 limited-capability, 2 failure-path; 0/159 at >=3 positives and >=2 owned negatives | `routing-fixtures.json` recount recorded in `00-scope-and-evidence.md` |
| Full test suite | 430 passed, 4 skipped, 96.29% coverage | `validators/pytest.txt`, with explicit counts in `validators/pytest-summary.txt` |
| Kernel validator | Exit 0, `ENGINE CONTRACT: PASS` | `validators/validate_engine.txt` |
| Applied proof | 4 examples directories; 81 worked-example headings; 34 duplicate generic worked-example paragraphs | Static current checkout counts in `00-scope-and-evidence.md` |
| Broken/machine-specific links | Hospitality absolute path: no match in target skill. Full path scan: not run. Three dangling cross-engine names found; target catalogue not freshly verified. | Targeted `rg` probes and noted limits in `00-scope-and-evidence.md` |
| Expired source records | No local source-register files found under `docs/`; expired-record count cannot be computed. | `find docs -iname '*source*register*'` result; currentness coverage is incomplete, not zero expired by assertion. |
| Phase gates / product tasks | Task 1 Phase 01 and 02 pass; all-phase validation of task-limited projects fails on missing lifecycle outputs; Task 3 Phase 05 passes after completion report repair; Phase 09 business-goal links absent. | Individual records in `tasks/task1/` and `tasks/task3/` |
| DOCX pipeline | Normal clean-checkout attempt fails for absent ignored reference template. Temp mirror + generated font-adjusted template builds with Pandoc 3.13; PDF export succeeds; PDF blank TOC visible. | `tasks/task1/docx-build.txt`, `docx-render.txt`, page PNGs |

## Frozen-before-change record

This file is committed before any implementation change. Ratings remain immutable as the baseline; updated ratings appear in the final report. The initial 45 cap is shown alongside, but separate from, the Portfolio Standard cap of 65.

## Currentness and release blockers

- The stale Phase 02, Phase 03 and Phase 05 standards references are currentness defects; full clause remapping is still required.
- The absent `templates/reference.docx` prevents a clean-checkout normal DOCX build. Temporary template generation does not standardise the fix.
- No unsupported legal requirement was put into a sample. Uganda legal status through 2026 remains `NOT_ASSESSED` beyond the evidence window stated in `standards-source-register.md`.
- The SRS task samples are drafts, not approved specifications. Missing project evidence, model runtime identity, archival snapshots and native Word accessibility checks stay visible.
