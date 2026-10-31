# Pass 2 validation record

**Run:** 2026-10-31, after the last engine edit (`f15543f`), on a Fedora workstation with Python 3.14.8 and Node 22. No package was installed. `ruamel.yaml`, `click`, `jsonschema`, `mistune`, `pytest`, `pytest-cov`, `python-docx`, Pandoc and the Mermaid CLI are all absent, so several registered checks cannot run here. Those are `NOT_ASSESSED`, never passes. Where an indicative run was possible with scratch tools kept outside the repository (a PyYAML-backed stand-in for `ruamel.yaml`, a minimal pytest-compatible function runner, and a driver for the Phase 02 checks that need no `jsonschema`), it is labelled *indicative* and sits beside, not in place of, the registered result.

## Registered validators, as registered

| Command | Exit | Result |
|---|---:|---|
| `python3 -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | 2 | `NOT_ASSESSED`: prints that `ruamel.yaml` is missing and the install command (new in K2-08; the baseline run was a traceback with exit 1). |
| `python3 -X utf8 scripts/routing_smoke_test.py` | 2 | `NOT_ASSESSED`, same message. |
| `python3 scripts/validate_engine.py` | 0 | `ENGINE CONTRACT: PASS` (no third-party package needed). |
| `python3 -m engine validate-skills` | 1 | `NOT_ASSESSED`: `ModuleNotFoundError: No module named 'ruamel'` (the CLI imports `click` and `ruamel.yaml`). |
| `python3 -m pytest` | 1 | `NOT_ASSESSED`: `No module named pytest`. |
| `python3 -X utf8 scripts/source_ingestion_guardrail.py` | 0 | `findings: 0`. |
| `python3 scripts/validate_plugin_packages.py` | 0 | 159 active skill paths; 1,985 checkout entries (includes `.git` growth from this cycle's commits); 1,277 package-oriented entries (1,260 at baseline, the rise is the new files); limit 5,000; `errors: 0`. |

## New checks added this cycle

| Command | Exit | Result |
|---|---:|---|
| `python3 scripts/check_portable_paths.py` | 0 | PASS: no tracked per-user settings; 0 machine-path lines in live content; history lines within the ceiling of 65. |
| `python3 scripts/check_cross_engine_refs.py` | 0 | PASS for flat-layout names; category and URL resolution `NOT_ASSESSED` (no checkout configured). |
| `python3 scripts/check_cross_engine_refs.py --dev-engine-root <local dev-engine checkout>` | 0 | PASS; every category path and URL resolves in that checkout. |
| `python3 scripts/check_standards_currency.py` | 0 | PASS: all eight counts at their ceilings. |
| `python3 scripts/validate_source_register.py --today 2026-10-31` | 0 | PASS: 18 effective records from 2 registers. As of 2027-02-01 it exits 1 with 14 overdue records, proving it can fail. |
| `python3 scripts/validate_traceability_evidence.py engine/tests/fixtures/traceability-evidence.json` | 1 | `NOT_ASSESSED`: the script imports `jsonschema`, which is absent (`ModuleNotFoundError`). CI runs it; the step was added this cycle. |

## Indicative runs (scratch stand-ins, not the registered environment)

| Run | Result |
|---|---|
| Catalogue validator under the YAML stand-in | Exit 0; 159 active skills, 1 template, failure counts `{}`; the same 5 report-only byte warnings as baseline; `04-requirements-analysis` is 19,994 bytes, below the 20,480 warning threshold. |
| `routing_smoke_test.py --min-rank1 83 --lint-fixtures --coverage --min-covered 8` | Exit 0; 72/72 fixtures in the top three; precision@1 64/72 (88.9%), baseline 57/65 (87.7%); 25 owned negatives: 22 pass, 0 fail, 3 cross-engine `NOT_ASSESSED`; route coverage 8 of 159 (7 with cross-engine owners excluded); fixture lint 0 findings over 97 prompts. |
| Function runner over `engine/tests/test_*.py` and `tests/test_*.py` | 302 pass, 8 fail, 1 skip, 26 error. Baseline run: 215 pass, 8 fail, 1 skip, 26 error. The 87 additional passes are the tests added this cycle. The failing and erroring set is identical to baseline by name, and every member traces to an absent package (`jsonschema`, `click`, `ruamel.yaml.error`) or to a CLI subprocess that needs `click`. This is not the 459-test pytest suite and says nothing about its coverage floor. |

## Failing-first and sabotage evidence

| Check | Failing case | Result |
|---|---|---|
| Tracked local settings | The pre-change tree | exit 1 with the file named; exit 0 after untracking |
| Flat-layout references | The pre-change tree | 8 findings (9 with a checkout); 0 after |
| Machine paths | The pre-change tree | 40 findings; 0 after |
| NFR and test-trace checks | 30 new tests | 21 failed before the change, 30 pass after |
| Standards ratchet | The pre-change tree | `wcag-2.1-engine: 6 lines exceed the ceiling of 0`, exit 1; a test injects an extra citation and expects exit 1 |
| Source register | A copy with a past review date, a row with no date, and a date set 2027-02-01 | each reported; rows split by a blank line still parsed |
| Missing dependency | A shadow `ruamel` package on the path | both catalogue scripts exit 2 with the install hint and no traceback |

## Step 1 tasks, re-run after the changes

| Task | Before | After |
|---|---|---|
| 1. School-fees SRS (disposable project) | Phase 01 gate pass; Phase 02 checks 1 finding, of which 1 false positive, 2 vague NFRs missed; route for the literal sentence: `10-saas-multi-tenancy-architecture-spec` 9.01, `01-initialize-srs` 9.00 | Phase 01 pass; Phase 02 checks 2 findings, both correct (`at all times`, `quickly`); false positive gone. The routing tie is unchanged (still a lexical-proxy near miss; next cycle). `.docx` build: `NOT_ASSESSED`, Pandoc absent. |
| 2. Contradictory brief (paired) | Route: `04-requirements-analysis` rank 10. With register: 5 blocking findings. Without: pass with the five contradictions silently resolved. | Route: rank 1 (19.0 against 9.0). With register: 5 blocking findings. Without register: still passes, deliberately unchanged because absence policy needs an owner decision. |
| 3. Ten-requirement trace (disposable) | 7 findings, 2 of them gate defects (NFR and module-qualified trace rejected), NFR with no test or goal silent | 5 findings, all correct (missing goal or test links for `FR-001`, `FR-002`, `FR-003`). The silent NFR gap (D-10) and duplicate-ID gap (D-09) remain open for an owner decision. |

## Independent re-measure

Counts come from the independent script (`git ls-files` plus regular expressions), after correcting its flat-layout pattern.

| Measure | Baseline | Final |
|---|---:|---:|
| Machine-specific path lines outside `docs/` | 43 in 18 files | 0 |
| Machine-path lines in historical `docs/` records | 66 | 65 |
| Tracked per-user settings files | 1 | 0 |
| Flat-layout references that do not resolve | 8 (baseline script counted 7) | 0 (2 remaining matches are upstream citations on the allowlist) |
| Stale-citation lines outside `docs/` (IEEE 830 / 42010:2011 / 29119-3:2013 / 25010:2011 / 29148:2011 / 26514:2008) | 163 / 13 / 11 / 1 / 1 / 0 | 163 / 13 / 11 / 1 / 1 / 0, unchanged (ceilings now enforce it; unfiltered counts are higher only because the new ratchet files hold the patterns as data) |
| Engine-level WCAG 2.1 prescriptions | 6 | 0 |
| Skills at three positives and two owned negatives | 4 of 159 | 8 of 159 (7 excluding cross-engine owners) |
| Fixture prompts | 89 | 97 |
| Worked-example headings / identical-paragraph skills / `examples/` folders | 81 / 44 / 4 | 81 / 44 / 4, unchanged |
| Expired source records as of 2026-10-31 | 0 of 17, unenforced | 0 of 18, enforced |

## `NOT_ASSESSED` in this pass

- The registered catalogue validators, kernel CLI and pytest suite, because required packages are absent (indicative stand-in runs above).
- The Phase 02 gate class and Phase 09 registry checks (need `jsonschema`); only the individual Phase 02 checks that do not need it ran.
- `scripts/validate_traceability_evidence.py` (needs `jsonschema`).
- The `.docx` and diagram build, native Word accessibility, real-font rendering (Pandoc and Mermaid CLI absent).
- Live model routing; the lexical proxy is not live routing. Cross-engine owned negatives (3).
- The CI workflow itself (edited and parsed, not run).
- Model currentness: this is a Claude session; the Codex pins in `AGENTS.md` do not apply and no fresh comparison was run.
- Legal currency of the Uganda Act and Regulations through 2026; the ISO 29148 draft stage; clause-level remapping of IEEE 830, 42010:2011 and 29119-3:2013.
