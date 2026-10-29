# October cycle validation record

Validation used the disposable Python environment with the repository requirements and `python-docx`, plus the official Pandoc 3.13 binary in a temporary tools directory. No package, template, PDF, native prompt input, or task project was added to this checkout.

## Registered validators and suite

| Command | Result | Evidence and limits |
|---|---|---|
| `python -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | Exit 0; 159 active skills, 1 template, zero failure counts. Five report-only skill-byte warnings remain. | [Validator](../../../scripts/validate_skill_engine.py), [frozen baseline](../../../tests/skill-quality-baseline.json). The changed requirements-analysis skill was reduced to 20,479 bytes, one byte below the validator's 20,480-byte warning threshold; its pre-cycle size was 20,352 bytes. No new byte warning remains. |
| `python -X utf8 scripts/routing_smoke_test.py` | Exit 0; 65/65 fixtures in top three; rank-one 57/65 (87.7%); top-three 100%; 24 owned negatives: 21 pass, 0 fail, 3 cross-engine `NOT_ASSESSED`. | [Routing fixtures](../../../tests/routing-fixtures.json), [routing checker](../../../scripts/routing_smoke_test.py). |
| `python -X utf8 scripts/routing_smoke_test.py --min-rank1 83 --lint-fixtures` | Exit 0; rank-one floor met; zero lint findings over 89 prompts. Four of 159 active skills (the four touched routes) now meet the three-positive/two-owned-negative target. | Same fixture/checker sources. Three cross-engine negatives cannot be assessed by this repository alone. |
| `python scripts/validate_engine.py` | Exit 0, `ENGINE CONTRACT: PASS`. | [Kernel contract validator](../../../scripts/validate_engine.py). This checks repository contracts, not project semantic correctness. |
| `python -X utf8 -m pytest -q -p no:cacheprovider` | Exit 0; 452 passed, 4 skipped, 96.48% coverage, above the frozen 96.29% and configured 90% floor. 456 tests collected; skipped items remain skipped. | Includes [DOCX tests](../../../engine/tests/test_docx_build.py), [source-reconciliation tests](../../../engine/tests/test_source_reconciliation.py), [package/discovery tests](../../../engine/tests/test_plugin_package_validators.py), [trace-evidence tests](../../../engine/tests/test_traceability_evidence.py), and the existing suite. This test invocation does not assess browser-based rendering or native Word accessibility. |
| `python -m engine validate-skills` | Exit 0, `SKILLS OK: no legacy path references outside alias-blocks.` | Existing compatibility gate. |
| `python scripts/source_ingestion_guardrail.py` | Exit 0, zero findings. | Source ingestion guardrail. |

The suite command uses the temporary interpreter/tool setup described above; command arguments are shown in repository-portable form. The first post-change run exposed one test that required the current routing-fixture count to equal the frozen baseline count. That equality was replaced with a lower-bound assertion, keeping the baseline file unchanged; the final full run passed.

## Independent package-validator acceptance review

An independent review of `f59c82a..8cb2178` reproduced two integrity gaps:
the package gate accepted different plugin `name` values in the Codex and
Claude manifests, and accepted an active `SKILL.md` symlink to a file outside
the package tree. The validator now requires name parity and rejects symlinks
in each declared skill path, including the `SKILL.md` itself. Two focused
regressions cover those refusals; `engine/tests/test_plugin_package_validators.py`
passes 11 tests.

After these acceptance changes, the full suite with the disposable Python
environment and Pandoc 3.13 on `PATH` passed 455 tests, skipped 4, and reported
96.43% coverage, above the frozen 96.29% baseline. Command:
`python -X utf8 -m pytest -q -p no:cacheprovider`. The temporary tool paths are
not part of the repository record. The `459` collected-test count includes the
four skipped cases; native Word/Windows validation remains NOT_ASSESSED.

## Added checks and exercise results

| Check | Result |
|---|---|
| `python scripts/validate_plugin_packages.py` | Exit 0; 159 active skill paths, 1,606 full-checkout file entries and 1,260 package-oriented entries. Both counts are below the fixed 5,000 limit. |
| `python scripts/check_codex_discovery_summary.py <sanitised-summary.json> --expected-paths 159` | Exit 0; sanitized configured native summary: 159 manifest paths, 159 runtime paths, zero missing, `network=none`, zero model calls. The raw prompt input is not retained. |
| `python scripts/validate_traceability_evidence.py engine/tests/fixtures/traceability-evidence.json` | Exit 0; 10 requirement rows, 10 design links, 10 test links, zero business-goal links, 3 executable oracle states, 7 requirements with open owner decisions, zero executed. Fixture asserts these fields remain distinct. |
| `python scripts/validate_source_reconciliation.py <task-2-fixture>` | Expected exit 1; six high-severity unresolved ambiguity findings. The full Phase 02 validation also blocks. This is the intended failure path until an owner resolves the six decisions. |
| `python scripts/build-doc.sh <task-1-SRS-directory> SRS_Final_Cycle` with missing template path | Exit 0. Temporary `reference.docx` generated; Pandoc built a DOCX that opened with python-docx. LibreOffice rendered a tagged two-page PDF and page one visibly contained the linked contents entries. |
| Missing-Pandoc DOCX test | Expected builder failure with an explicit Pandoc requirement; automated failure-path test passes. |
| Temporary native local-installer harness with `chwezi-sdlc-documentation` | At clean commit `a8a1e24`, Codex CLI exit 0 and Claude CLI exit 0; both `network=none`, no model call. This tests local native installation, not public directory submission or account-specific authentication. |

Package tests exercise the exact 5,000/5,001 entry boundary for package-oriented counts and for full-checkout counts. The full-checkout boundary fixture places extra entries beneath its excluded VCS directory, proving the two counts are checked separately. Tests use a small injected limit as an additional fast failure case.

## Rechecked task outputs

- **Task 1:** the disposable SRS still passes the Phase 01 and Phase 02 fixture checks. The rebuilt document now contains a visible contents list. This is a draft based on one short exercise brief; stakeholder validation, approved project decisions, native Word accessibility review and final font fidelity were not assessed.
- **Task 2:** six source ambiguity records remain explicitly unresolved and block the Phase 02 baseline. The validator checks declared records and links; a human analyst/reviewer still owns source completeness and semantic conflict detection.
- **Task 3:** the trace evidence report has 10/10 named design links and 10/10 named test links, zero business-goal links, 3 executable oracle states and 7 open decision rows. No tests were executed against a product. These exercise values are reproduced in the checked-in fixture and are not a claim of implementation coverage.

## `NOT_ASSESSED`

- Full legal currency of the Uganda Act and Regulations through 2026; legal interpretation; normative clause remapping for IEEE 830 / current ISO editions.
- Public portable ZIP validation, directory submission/acceptance, account-specific installation, and any paid behavioural evaluation.
- Semantic discovery of missing or contradictory source statements without human review; source completeness in production projects.
- Three cross-engine routing negatives, because their owners live in other skill engines.
- Word-native accessibility, real target-font installation/embedding and pagination fidelity; archival source snapshots; actual project implementation and execution evidence.
- Automated detection of every cross-engine link or stale standards clause. The known reference paths were checked and corrected in this cycle; standards doctrine was not edited.

## Root acceptance rerun

The root review found that the package counter could silently omit unreadable
subtrees. It now fails closed and has a deterministic negative regression.
Focused package/reconciliation/trace tests pass (21); full pytest with Pandoc
and the temporary Python environment available on PATH passes **453 tests,
4 skipped, 96.47% coverage**, above the frozen 96.29%. An earlier focused run
without `--no-cov` failed the whole-project coverage threshold because it did
not run the whole suite; an earlier full run without Pandoc skipped one extra
build test. Neither incomplete invocation is the final acceptance result.
