# Methodology and rubric

## Auditor independence

This audit was carried out by an auditor who did not execute any my-10-kaizen phase. The engine
was graded as committed at HEAD `fa85fba` on 29 September 2026. No git state was changed: no
commit, checkout, stash or reset. Nothing outside this audit folder was written. The auditor
opened only file names under `projects/`; the DOCX scan is the engine's own read-only script. No
paid API, `claude -p` call or model-executed evaluation was run (zero-spend rule).

## Method

1. **Harness first (SKILL.md step 0).** The auditor ran the validators listed in the brief, plus
   `source_ingestion_guardrail.py` and `validate_engine.py`, from the engine root with
   `PYTHONDONTWRITEBYTECODE=1`. Exit codes and output are in `11-measured-evidence.md`. Remote CI
   was inspected with read-only `gh run list` and `gh run view --log-failed`.
2. **Scope.** The auditor read `CLAUDE.md` (a thin `@AGENTS.md` bridge), `AGENTS.md` (500 lines),
   `README.md`, `rules/common/`, `docs/standards-clause-registry.md`, `scripts/build-doc.sh` and
   `scripts/create-reference-docx.py`. A machine inventory of all 159 skills recorded bytes,
   reference-file count, `examples/` presence and the presence of boilerplate workflow text.
3. **Sample read.** The auditor read 17 SKILL.md files from all nine groups, listed in
   `03-existing-groups-audit.md`. Targeted greps across all 159 checked standards citations,
   diagram-IR adoption, cross-engine skill references and "Worked Example" bodies.
4. **Readiness.** The auditor recomputed the Engine Eval Readiness score from the stored inputs in
   `chwezi-engine-agents/docs/operations/m10-kaizen-evidence/M10-14/` and checked T1 and T2_p1
   against the local runs.
5. **Prior audits.** The auditor compared this audit with `docs/audits/2026-09-08-comprehensive-kaizen.md`
   and `2026-09-06-kaizen.md`. Their scores were not copied.

**Documented limitation: no parallel fleet.** The skill prescribes a fleet of six independent
agents. In this audit a single auditor worked through each concern in turn: standards, existing
skills, taxonomy, output types, hardening and reading. The per-concern scores are therefore less
independent than the method intends.

## Rubric

The bar is the top 0.1 % of requirements and software-lifecycle documentation practice. Bands:
90–100 rivals the best; 75–89 excellent; 60–74 solid but visibly short; 40–59 competent with major
gaps; below 40 skeletal. Default range 45–65. Any score of 70+ needs an "Extraordinary
justification" paragraph. **No score in this audit reached 70.**

Each dimension carries one of three labels:

- **measured**: comes from command output, cited in `11`.
- **judged**: the auditor's judgement against named evidence.
- **NOT_ASSESSED**: scores 0 wherever it feeds a formula.

## Weighting

| Bucket | Weight | Source dimension(s) |
|---|---:|---|
| Output-type readiness and coverage | 30 % | Output readiness dimension, which is the mean of 16 output types rounded to 55 |
| Skill depth and worked examples | 25 % | Mean of skill depth (56) and worked examples (42) = 49 |
| Standards currency | 15 % | Standards currency (55) |
| Taxonomy and structure | 10 % | Taxonomy (55) |
| Doctrine and philosophy | 10 % | Doctrine (64) |
| Hygiene | 10 % | Mean of redundancy (50), discovery/routing (judged 60 raw, or Readiness 58.5 measured) and safety (62) |

Accessibility (52) and production/handoff (60) are scored and reported. They feed the overall
score only through the output-type scores, as in the rubric's suggested weighting.

## Three published numbers

- **Raw**: the weighted overall with routing judged.
- **Measured-constrained**: routing replaced by Readiness (AO-14 rule 3).
- **Published**: `min(measured-constrained, 65)`, because the portfolio craft-standard acceptance
  evidence is absent.

## Limitations

- No fresh external research was done. Standards currency is judged from the engine's own
  currentness records. Any edition or supersession the auditor states from general knowledge is
  marked "to be verified through the Digital Research gate".
- Lexical T2 figures are a drift guard, not proof of live routing.
- Tier 3 has not run. Rendered-DOCX visual quality was not inspected, because client DOCX files
  were not opened.
- Fan-in (`skill_fanin.py`) was not run: NOT_ASSESSED.
