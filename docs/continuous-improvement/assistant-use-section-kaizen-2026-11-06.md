# AI assistant use section kaizen record, 2026-11-06

## Trigger

A 2026 reading of CODE Magazine articles produced six reviewed cards that agree on what a team's guidance for AI coding assistants needs: a short first guide, encouraged uses listed first, the architecture rules an assistant cannot know written down, review expectations for assisted changes, and the guide kept as a reviewed team artefact. The cards were compared with this engine's text on 2026-11-05 and the gap below was found. The owner asked on 2026-11-06 for the action to be carried out. The cards are concept input only; nothing here is copied from the articles.

## Baseline (measured on `main` at `739dcd3`, 2026-11-06)

| Measure | Value |
|---|---|
| Matches for AGENTS.md, CLAUDE.md, copilot, assistant, instruction file, rules file, AI coding, coding assistant in `02-coding-guidelines/SKILL.md` | 0 |
| The same terms in `05-ai-agent-coding-guidelines-addendum/SKILL.md` | 0 |
| `pytest` | 535 passed, 5 skipped, coverage 96.19% |
| `validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | 159 active skills, 1 template, no failures |
| `routing_smoke_test.py --min-rank1 83 --lint-fixtures --min-covered 8` | 72 of 72 in the top three, precision@1 64 of 72 (88.9%), 25 owned negatives (22 pass, 3 not assessed), 8 of 159 skills covered, 0 lint findings over 97 prompts |
| `source_ingestion_guardrail.py`, `check_portable_paths.py`, `validate_plugin_packages.py` | 0 findings, PASS, 0 errors |

The search of the two `SKILL.md` files was the plan's baseline. A wider search of the skills and references found one related file: `02-coding-guidelines/references/ai-coding-guidelines-addendum.md`. It covers code that calls a model, builds prompts or runs agent tools. It does not cover a team's own use of coding assistants, so the gap stands.

## Stop-condition assessment

The action stops if the community development engine already owns a document contract for assistant instructions. It does not. Three skills there are adjacent, and each owns a procedure, not a coding-guidelines requirement:

- `sdlc-meta/doc-architect` generates and maintains layered `AGENTS.md` project guidance.
- `sdlc-meta/ai-assisted-development` holds the AI-generated code review gate.
- `ai/coding-agent-optimization` tunes one device's assistant configuration, context and permissions.

The new section states what the guidelines shall say and points to those three for the how. It does not restate their procedures.

## Change (standardise)

| Surface | Change | Acceptance condition |
|---|---|---|
| `02-coding-guidelines/references/ai-assistant-use-section.md` (new) | When section 9 applies and when it does not; eight required elements AU-1 to AU-8, each with its source and acceptance condition; what the section shall not contain; a hand-applied checklist; one worked example that passes and one that fails; pointers to the community development engine | The contract names the section, its content and a checklist |
| `02-coding-guidelines/SKILL.md` | Optional Step 6a, one Output Format sentence, one Common Pitfalls row, one Verification Checklist item | Section 9 is reachable from the skill and routed away for an AI-agent product |
| `02-coding-guidelines/logic.prompt` | Step 6a and the optional section in the output list | The executable prompt matches the skill |
| `tests/routing-fixtures.json` | One positive and one owned negative | Both fixtures pass; each fails when broken |

No skill was added and no description changed: 159 active skills and 1 template. The reference is 142 lines; `SKILL.md` is 236 lines and 15,786 bytes, under the 500-line limit and the 20,480-byte report-only threshold.

## Check

| Check | Before | After |
|---|---|---|
| `pytest` | 535 passed, 5 skipped, 96.19% | 535 passed, 5 skipped, 96.19% |
| `pytest tests -o addopts=` | 33 passed | 33 passed |
| `validate_skill_engine.py --baseline ...` | 159 skills, 1 template, no failures | 159 skills, 1 template, no failures |
| `routing_smoke_test.py ... --min-covered 8` | 72 of 72; precision@1 64 of 72; 25 owned negatives (22 pass, 3 not assessed); 97 prompts | 73 of 73; precision@1 65 of 73 (89.0%); 26 owned negatives (23 pass, 3 not assessed); 99 prompts; 8 of 159 covered; 0 lint findings |
| `source_ingestion_guardrail.py` | 0 findings | 0 findings |
| `check_portable_paths.py` | PASS | PASS |
| `check_standards_currency.py` | PASS | PASS |
| `check_cross_engine_refs.py --dev-engine-root <checkout>` | PASS, 0 findings | PASS, 0 findings |
| `validate_plugin_packages.py` | errors 0 | errors 0 |
| `python -m engine validate-skills` | SKILLS OK | SKILLS OK |
| `python -X utf8 scripts/validate_engine.py` | ENGINE CONTRACT: PASS | ENGINE CONTRACT: PASS |
| Assistant-term matches in `02-coding-guidelines/SKILL.md` (the baseline search) | 0 | 5 |
| The same search in `05-ai-agent-coding-guidelines-addendum/SKILL.md` | 0 | 0 |

Python 3.14.10 and pytest 9.2.0 in a fresh virtual environment, with `PYTHONPATH` set to the repository root. The ranked fixture count rose by 1 (the positive), and the owned-negative count by 1 (the negative), so 97 prompts became 99.

## Controls (checks shown able to fail)

- Routing, negative fixture: with the owner and skill swapped, `evaluate_negative` returns FAIL ("`05-ai-agent-coding-guidelines-addendum` ranks first (35.006)"). With the real fields it returns PASS (owner rank 1, `02-coding-guidelines` rank 34).
- Routing, positive fixture: with a wrong expected skill the rank is 4, outside the top three, so the positive check would fail. With the real skill the rank is 1 (22.0 against 14.0 for the addendum).
- Cross-engine references: changing `sdlc-meta/doc-architect` to `sdlc-meta/doc-architectx` in the tracked reference made the check exit 1 and name the line (131). Restored, it exits 0 with 0 findings. A first attempt used an untracked file and passed, because the check reads tracked files only; that control was invalid and is not counted.

## Worked examples, applied by hand

The reference holds both. Fictional project: Harbour Tracker, a multi-tenant shipment tracking application.

- Example A (all eight elements present, each with its acceptance condition): AU-1 to AU-8 PASS, 8 of 8. Section 9 is accepted.
- Example B (example A with 9.8 replaced by "Assistants read the repository instructions and follow them."): AU-1 to AU-7 PASS; AU-8 FAIL, because no file name or path, owner role, review step or precedence rule is stated. 7 of 8. Section 9 is returned to its owner.

No automated document-conformance check exists for coding guidelines, so both results are a reader's judgement, applied once by the author of this record. They have had no independent review.

## Not assessed

- Whether a team that uses the section writes better guidelines. No team has used it. The section is a contract with a checklist, and its value is a hypothesis.
- Whether routing reads the section. The lexical ranker scores skill names and descriptions only, so the two fixtures test the neighbour boundary, not the body text.
- Live-model routing, and independent review of the eight elements and the two examples.
- Any claim about what a particular assistant product reads or supports. The section avoids such claims on purpose; they change, and the engine would need a dated primary-source read to state them.

## Judgement calls

- The section lives in a reference, not in `SKILL.md`, to keep the skill within its size budget and to leave its contract block unchanged.
- The description of `02-coding-guidelines` is unchanged, because a description change moves routing for the neighbours and the plan did not ask for one.
- Three pointers into the community development engine are given by skill name; the check that resolves them reads tracked files only and was shown to fail on a wrong name.

## Rollback

Remove the optional section: delete `references/ai-assistant-use-section.md`, revert the four edits in `SKILL.md` and the step in `logic.prompt`, and remove the two fixtures from `tests/routing-fixtures.json`. Counts return to 72 of 72 and 25 owned negatives.
