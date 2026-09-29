# Roadmap to world class

Targets are believable scores after each phase, with the current rubric and weighting. The
published score stays capped at 65 until the portfolio craft-standard acceptance evidence exists.
Readiness stays capped at 70 until Tier 3 is executed.

## P0: restore integrity (target: published about 57, Readiness about 60)

| Move | Files | Acceptance evidence |
|---|---|---|
| Fix the red CI. Replace the `C:/wamp64/...` links with engine-identity text resolved through the registry, and add a validator rule that rejects absolute drive or home paths in any tracked `*.md`. | `02-requirements-engineering/hospitality-operating-model-srs/SKILL.md` lines 156–157; `scripts/validate_skill_engine.py` | Remote "Engine" workflow green at HEAD. A negative test proves the new rule fires. |
| Repair the dangling cross-engine skill references. Add a check that resolves `skills/<name>/` references against the dev-engine catalogue, or reports NOT_ASSESSED when that catalogue is absent. | `03-design-documentation/04-database-design/SKILL.md` (points to `backend-databases/mysql-engineering`); `03-design-documentation/03-api-specification/SKILL.md` | 0 unresolved dev-engine skill names. A validator test covers the case. |
| Remap the Phase 02 kernel checks from IEEE 830-1998 to ISO/IEC/IEEE 29148:2018 clauses. Add `edition`, `accessed` and `review` columns to the registry. Verify the 42010, 1058, 26514, 1012 and 730 editions through the Digital Research gate. | `docs/standards-clause-registry.md`; `engine/gates/phase02.py` check metadata; `01-strategic-vision/02-business-case/SKILL.md` | `validate_engine.py` passes. Each row carries a dated source. |
| Make the traceability-matrix skill call `python -m engine sync` and `validate`, and build the RTM from `_registry/`. | `09-governance-compliance/01-traceability-matrix/SKILL.md` | The skill's steps name the commands. A fixture RTM is generated from `engine/tests/fixtures/requirements_traceability`. |
| Correct defects inside skills: the step numbering and double priority scheme in feature decomposition, the business-case ROI formula and manifest, and the API pagination contradiction. | `02/waterfall/05-feature-decomposition/SKILL.md`; `01/02-business-case/SKILL.md`; `03/03-api-specification/SKILL.md` | Reviewed diff. The anti-slop gate passes. |

## P1: applied proof and structure (target: published about 61, Readiness about 61–62)

| Move | Files | Acceptance evidence |
|---|---|---|
| Replace the boilerplate `## Worked Example` paragraph with a real `examples/representative/{inputs,expected-output}` pack for the 12 core output types: PRD, business case, lean canvas, SRS section, HLD, API (with `openapi.yaml`), database, UX journey, test plan (expanded), RTM, user-manual chapter, deployment guide. Link the healthcare fixture where it applies. | The 12 skill folders | 12 of 159 skills with examples, up from 4. Each example validates with the kernel where a check exists. |
| Raise routing fixture coverage. Give at least 40 skills three positives and two owned negatives, beginning with the 12 core skills and the AI incident cluster. | `tests/routing-fixtures.json` | T2_cov ≥ 0.25 and p@1 ≥ 0.90 give Readiness ≈ 30 + 40 × (0.90 + 1 + 0.25 + 1) ÷ 4 = **61.5**. |
| Resolve duplicate prefixes through alias blocks. Split group 02 into fundamentals/waterfall/agile/hybrid/domain. Add an AI-and-agents index skill. Fold the incident sub-skills into one skill with references. | Phase roots; `tests/skill-quality-baseline.json` | Validator rule against duplicate prefixes; within-engine collision below 0.75. |
| Bring the six oversize skills under 20 KB by moving detail into references. | `03/05-ux-specification`, `02/.../02-elicitation-toolkit`, `07-requirements-validation`, `04-requirements-analysis`, `06-infrastructure-design`, `09/28-anti-ai-slop` | 0 skill-bytes warnings. |
| Add the missing skills: data migration plan, threat-model/security requirements specification, accessibility conformance report, DR/BCP plan, administrator/training guide, as-built recovery. | New skills under 02, 03, 06, 08 and 09 | 165 active skills, each with references and an example. |
| Record a typeface decision from the design engine in the reference DOCX, and add a DOCX structure lint (heading order, table header rows, alt-text coverage). | `scripts/create-reference-docx.py`; `scripts/check_docx_diagrams.py` or a sibling | The lint runs in `build-doc.sh`. The typeface is named with its reason. |

## P2: behavioural and delivery proof (target: raw about 66, published capped at 65; Readiness up to about 85 once T3 is executed)

| Move | Files | Acceptance evidence |
|---|---|---|
| Execute the Tier-3 behavioural runs for this engine under a pinned model and CLI version. This needs spend authority from Peter Bamuhigire. | `chwezi-engine-agents/evals/behavioural/results/**/grading.json` | Validated grading files. If T3 passes at 0.8, Readiness reaches ≈ 61.5 + 24 = 85.5. |
| Run one representative project chain end to end: requirement → failed-path test → rendered DOCX → stakeholder decision → handoff. This carries over from the 2026-09-08 backlog, which has not been met. | A synthetic project under `templates/project-examples/` (not client work) | Trace IDs, test results, a human review of the rendered DOCX, and a sign-off ledger entry. |
| Produce the portfolio craft-standard acceptance evidence. | Per `chwezi-engine-agents/docs/operations/portfolio-craft-standard-2026-09-04.md` | Evidence exists. After that the 65 cap no longer binds. |

## Stop rules

- Do not lower `--min-rank1 83` or the coverage gate to make a phase pass.
- Do not count a boilerplate or single-sentence example as applied proof.
- Keep every `NOT_ASSESSED` slot at 0 until executed evidence exists.
