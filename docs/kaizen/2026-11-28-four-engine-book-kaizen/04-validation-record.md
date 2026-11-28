# SDLC baseline validation at 09b84e7

Observed on Windows 2026-11-28 with Python 3.13.7 and Node 24.8.0. The Python callable was the available Windows interpreter. PYTHONPATH was set to the checkout for Python suites, per README. Coverage output and demo workspace were isolated outside the repository.

| Documented check | Exit | Observed result |
|---|---:|---|
| `scripts/validate_engine.py` | 0 | Engine contract passes. |
| `scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | 0 | 160 active, 1 template, no failures and five pre-existing report-only size warnings. |
| `scripts/routing_smoke_test.py --min-rank1 83 --lint-fixtures --min-covered 8` | 0 | 75/75 in top three, 67/75 first, 23/26 owned negatives pass, three cross-engine owners NOT_ASSESSED, zero fixture-lint findings. |
| `python -m engine validate-skills` | 0 | No legacy path references outside alias declarations. |
| `scripts/validate_plugin_packages.py` in the populated checkout | 1 | 58,095 checkout entries and 25,173 package-oriented entries exceed both 5,000 limits. |
| Same package checker on an isolated baseline checkout after synthetic seed | 0 | 1,697 checkout entries and 1,411 package-oriented entries. Use an isolated checkout when assessing package size. |
| `scripts/check_portable_paths.py` | 1 | Four current managed-runtime machine-path hits in `auto-agents/CHANGES.md`, `README.md`, `driver.py`, and `tests/test_driver.py`, plus historical prefix lines 66 against 65 allowed. The cycle cannot hand-edit or propagate the runtime. |
| `scripts/check_cross_engine_refs.py`, with and without `--dev-engine-root` | 0 / 0 | Pairwise dev checkout links resolve when present. Default entry point reports links NOT_ASSESSED without a checkout. |
| `scripts/check_standards_currency.py` | 0 | No stale-citation count exceeds the current ceiling. |
| `scripts/validate_source_register.py`, actual date and explicit Nov 28 | 0 / 0 | 22 effective records, with OpenAI plugin, zip limit and Claude marketplace due Nov 29, and Codex discovery budget due Nov 30. |
| `scripts/validate_traceability_evidence.py engine/tests/fixtures/traceability-evidence.json` | 0 | Ten requirements and tests reported, seven owner decisions open, zero executions. |
| `scripts/validate_sdd_phase_boundaries.py --feature-dir engine/tests/fixtures/sdd_feature` | 0 | No boundary findings. |
| `scripts/validate_requirements_decision.py engine/tests/fixtures/requirements_decision/reuse.json` | 0 | PASS with no open issues. |
| `scripts/seed_demo_project.py` and `python -m engine validate projects/_demo-hybrid-regulated` in disposable clone | 0 / 0 | Synthetic demo validates. |
| Same demo CLI with `--break-something` | 1 | Expected deliberate failure. The flag belongs to `engine validate`. An earlier seed-script invocation ignored it and was rerun with corrected placement. |
| `node hooks/test-destructive-bash-gate.js` | 1 | 54/61. Seven normal-push fixture cases failed closed in the Windows Git configuration probe. |
| `node hooks/test-plugin-hook-config.js` and all six other documented Node test files | 0 each | 7, 7, 4, 9, 64, 16, 28 passed in hook-config, pending, sessions-hook, e2e, markdown, sessions, and plan-canvas order. |
| `bash scripts/build-doc.sh <doc-dir> <output-name>` in disposable clone | 0 | Git Bash and Pandoc built a short synthetic deployment section. No Mermaid blocks or client data. First invocation used an absent sample folder and returned 1 before the isolated test setup. |
| Portfolio token-budget lint `--strict` | 0 | 31,293-byte AGENTS and 44-byte CLAUDE. Actual token count NOT_ASSESSED. |
| `.codex/ensure_model_policy.py --runtime codex --check` | 0 | Existing user configuration conforms. |

The production host installer, project bootstrap, real client workspaces, and Linux runtime are NOT_ASSESSED. No installed hooks, permissions or user maps were changed.

## Python and final remeasurement

The baseline `python -m pytest` exited 1 with 530 passed, 5 failed and 5 skipped, at 96% reported coverage. Four failures are sync-ID extraction tests in `engine/tests/test_cli_sync.py`; the fifth is the test mirroring the managed-runtime portability finding. `python -m pytest tests -o addopts=` exited 0 with 47 passes.

The one checked SDLC document section builds with Git Bash and Pandoc, and its DOCX archive and table contents validate. Final ranking agreed for all ten phrases. The final Node suite reproduced baseline behavior, including 54/61 passing destructive-hook cases and exit 1 for that file alone. Demo, local package, source guard, and final full Python output are recorded independently in the corresponding harness logs.

The final kernel rerun exited 1 with exactly the same five named failures, 530 passes and five skips. The final root suite exited 0 with 47 passes. Full hook and project-gate outcomes were unchanged. Final populated package validator exited 1 at 58,098 checkout entries and 25,175 package-oriented entries. Its isolated final-content run exited 0 at 1,583 and 1,353 entries. The final source-ingestion guardrail exited 0 with zero findings in both the populated and isolated content runs. Strict final token lint exited 0 at 30,597 B for AGENTS and 44 B for CLAUDE on the installed checkout. Final Codex config check exited 0. `git diff --check 09b84e7` exited 0.

The baseline source register check with `--today 2026-12-01` exited 1 with four overdue records. The proposed successor dated register was verified against the published primary sources and copied into an isolated final-content checkout. Validation exits 0 for both 2026-11-28 and 2026-12-01 and resolves 22 effective records from four registers. The first scratch register trial exited 1 when the first header read "ID" rather than the required "Claim ID". Correcting the format left the underlying claims and dates intact.


﻿# Independent review of SDLC deployment and routing changes

Reviewed the six product files against integrated baseline `09b84e7`. Checked the owning skill, generation prompt, skill README and its linked pipeline reference together. The change replaces a mandatory reverse-order plan with an explicit compatibility and data-recovery decision. The community runtime ownership and host-configured research routing are discoverable from the root guide. No new protocol, threshold, command, package, release or standards edition was added.

## Findings from first review

1. `06-deployment-operations/01-deployment-guide/SKILL.md` retained an unconditional “step-by-step reversal instructions” lead-in at line 183 and unconditional rollback language in the output contract and example at lines 37 and 97. Those lines could reinstate the retired requirement. Requested a recovery-plan framing that preserves reversal for documented reversible cases.
2. `06-deployment-operations/01-deployment-guide/logic.prompt` line 8 did not require explicit reconciliation verification and authorisation to restart writers. Requested both before accepting a recovery draft.
3. The project README linked recovery from Validation. Requested placement alongside task routing. Requested the cited book at the owning skill's evidence boundary.

## Paired document trial

The synthetic depot maintenance scenario has two accepted writes after a destructive schema contraction and tests a separate application-only rollback before the contraction. At the baseline, generation prompt step 6 and the skill’s checklist demand reversing every step. That instruction can restore a prior snapshot and omit accepted writes. The updated decisions instead verify application/schema compatibility, preserve acknowledged identifiers and queued work, distinguish forward fix from reversible service rollback, and stop at an unknown migration state. The generated section includes evidence and named action owners. It lives outside the source tree at `sample-final/05-rollback-procedure.md`. The section is an independently authored tabletop rehearsal. Production migration and live agent judgment remain NOT_ASSESSED.

## Acceptance evidence

The ten new routing phrases are unchanged. Lexical ranking reached rank 1 for two and top three for four on baseline. The final case compare is in the validation log. Document behavior grading is based on the paired instructions and one reviewed section rather than expecting lexical-score movement. Kept findings from the pre-existing Windows hook and managed-runtime portability suites retain their original severity. No credentials, client projects, runtime configuration, installation permissions or Git release pins were accessed or modified during review.

## Disposition after revisions

The author corrected the three review findings. The owning skill defines service-compatible reversal, last safe data reversal point, verification and escalation. The generation prompt verifies health and accepted-write reconciliation before the named owner authorises resumption. Both README routes point to the same operation class. The book citation identifies Morris's second edition, 2021 revision. The edition's initial 2020 release and January 2021 revision are both recorded in the source front matter.

The synthetic section used Git Bash and Pandoc to build a DOCX. Build exit 0, ZIP verification exit 0, and an independent read via python-docx confirmed all three decision rows, expected work-order ID ranges and recovery-owner resumption text. An initial assertion queried the wrong table cell and was corrected to inspect the trigger and action cells individually. The source documents and generated DOCX remain in scratch. A live rollout, user acceptance and visual page rendering are NOT_ASSESSED.


After integration the actual checkout also passed the December 1 register simulation (22 effective records). The second wave corrected the owning Kaizen skill to follow the same research route as the top-level instructions.
