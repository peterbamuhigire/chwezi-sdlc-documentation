# Chwezi SDLC documentation engine — preparation record

**As of:** 2026-10-29 (environment date). **Phase:** baseline frozen before implementation. **Repository:** `chwezi-sdlc-documentation`, HEAD `b3b08b5be8066772e0bd29b0ffb9cbda39a95979` at branch point; clean `kaizen/2026-10` branch. Root recorded the pulled checkout in a temporary prep record outside this repository.

## Scope and authority

- Read the complete portfolio prompt; SRS router, currentness rule, common rules and Kaizen skill; portfolio standard; Digital Research currentness gate; source-evaluation, evidence-discipline and source-verification skills; design engine router/doctrine/gate and DOCX/font selection skills.
- Installed only the repository-pinned Python dependencies into a disposable virtual environment, added `python-docx`, and downloaded the official Pandoc 3.13 Linux binary outside the checkout. Its SHA-256 matched the official release asset value. Temporary environment and task artifacts stayed outside the repository.
- Ran the catalogue validators, kernel validator, CI routing arguments, full kernel test suite, three disposable practitioner projects, normal and injected-failure gate paths, and the normal DOCX builder in a temporary mirror with a generated temporary reference template.
- No checkout file was edited. No branch, commit, push, external submission, paid behavioural evaluation or cross-engine edit was made. No current external rule was added to engine doctrine.

## Baseline validator results

The exact command outcomes and counts below are the retained baseline record. The disposable task projects and generated files remain outside the repository.

| Exact command (with disposable environment interpreter) | Exit | Observation |
|---|---:|---|
| `python -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | 0 | 159 active skills; 1 template; failure counts `{}`; 5 report-only `skill-bytes` warnings. |
| `python -X utf8 scripts/routing_smoke_test.py` | 0 | 55/55 fixtures; top-3 precision 1.000; precision@1 47/55 = 85.5%; 16 owned negatives: 13 pass, 0 fail, 3 cross-engine `NOT_ASSESSED`. |
| `python -X utf8 scripts/routing_smoke_test.py --min-rank1 83 --lint-fixtures` | 0 | Same route score; 83% floor met; fixture lint 0 findings across 71 prompts. |
| `python scripts/validate_engine.py` | 0 | `ENGINE CONTRACT: PASS`. |
| `python -X utf8 -m pytest -q -p no:cacheprovider` | 0 | 430 passed, 4 skipped; 96.29% coverage, above the configured 90% floor. |

The system Python used for first-run probing lacked `ruamel.yaml`; this was a host environment issue, resolved by the isolated environment. It is not recorded as a repository validator failure.

## Task 1 — multi-tenant school-fees SRS

Source brief: the prompt's single sentence “Produce an SRS for a multi-tenant school-fees module with mobile-money receipts.” The phrase was given by the task; no named stakeholder, workflow, provider, policy, threshold or domain reference was included.

- Route applied: `02-requirements-engineering/waterfall/01-initialize-srs`, with `fundamentals/during/07-requirements-validation` for review. The route matches “new SRS”; no runtime skill router was invoked.
- Draft SRS and context files were disposable. Actor names and fee/payment workflow are marked as inferences or unresolved inputs; quality targets and legal/current standards claims are not invented.
- Targeted Phase 01 and Phase 02 gates both **PASS** with 0 findings. Full `python -m engine validate` returns exit 1 with findings because this SRS-only exercise does not contain the other lifecycle-phase artefacts. Remaining in-scope traceability gaps are explicit: no approved business-goal mapping, design artefact, test plan/test IDs, or risk record. Do not treat out-of-scope phase findings as product defects.
- Failure path: `python -m engine validate <task1> --break-something` returns exit 1 and emits the synthetic Phase 02 failure marker as intended.
- DOCX path: the first normal builder invocation stopped because the ignored `templates/reference.docx` was absent and the build had no bootstrap step. In a temporary mirror, a generated template allowed Pandoc 3.13 to build the SRS. LibreOffice rendered a tagged two-page PDF. Visual inspection found a blank contents page because the DOCX contained a deferred field rather than entries. The host lacked the selected font binaries, and the DOCX did not embed them; visual font fidelity, Word accessibility checks and embedded-font behaviour remain `NOT_ASSESSED`. This was a build smoke test, not a ship-ready document.
- Typeface selection for that temporary DOCX: Source Serif 4 headings, Public Sans body and JetBrains Mono for any code/IDs, from the Design Engine catalogue record `type-01-source-serif-public-sans-mono`; the pairing is specifically listed for standards/governance/SRS. It fits a formal technical specification. Font embedding and final accessibility review were not completed.

## Task 2 — vague, contradictory brief

- Routed manually to `02-requirements-engineering/fundamentals/during/04-requirements-analysis` and `fundamentals/during/07-requirements-validation`; these fit conflict analysis then independent validation.
- The disposable task-2 source brief yielded six ambiguity records. The report identifies channel conflict, payment-state timing, pre-payment receipt meaning, tenant/central-office visibility, undefined offline scope and a no-personal-data assertion without resolving them.
- The all-phase gate passes no Phase 02 finding because the input is only a raw brief and contains no drafted requirements to validate. This is not evidence the ambiguity engine works; it is a measurable coverage gap. Manual analysis surface was adequate for this synthetic input, but no model-selected route or independent reviewer was available.

## Task 3 — ten-requirement traceability and test plan

- Routed manually to `09-governance-compliance/01-traceability-matrix` and `05-testing-documentation/02-test-plan`.
- The disposable task-3 fixture contains ten distinct requirement IDs, five proposed design elements, ten test cases, a coverage matrix, deterministic-check evidence and a test completion report. Static inspection shows all 10/10 IDs have named design and test links. This is link presence, not implementation or execution coverage.
- Seven requirements are only partly testable or cannot pass now because owner inputs are absent: FR-003 supported currency list; FR-005 callback-auth contract; FR-006 transition table; FR-007 receipt-eligible state table; FR-008 role matrix; NFR-001 threshold and workload profile; NFR-002 auth/exception-role model and test matrix. The sample correctly marks them partial/unassessed rather than treating test cases as executed. Requirement-to-business-goal links were not supplied; the governance gate flags them.
- After completing `test-completion-report.md` with explicit untested status, Phase 05 emitted no finding. Full nine-phase validation still fails on lifecycle artifacts outside this exercise and missing business-goal links. No Phase 09 traceability pass is claimed.

## Rechecked prior audit findings

| Finding | Current observation | Disposition |
|---|---|---|
| Hospitality machine-specific path | The target skill has no match for the path reported in the prior audit after the repository rename. | Prompt finding no longer observed in that skill. Full repository machine-path scan not run. |
| Dangling dev-engine skill refs | `03-design-documentation/04-database-design/SKILL.md` named `skills/mysql-best-practices/`; `03-design-documentation/03-api-specification/SKILL.md` named `skills/api-error-handling/` and `skills/api-pagination/`. | Read-only public `main` files confirmed all three exist as references nested under active skills. SRS now links to those exact reference paths and identifies the parent skill where needed. This resolves the path mismatch, not the technical correctness of the references. Evidence: `standards-source-register.md` claim C-DEV-REFERENCES. |
| IEEE 830 registry inconsistency | `docs/standards-clause-registry.md` maps six Phase 02 checks and one Phase 09 check to IEEE 830-1998. Local search finds 18 skill files citing 830. `AGENTS.md` calls it superseded. IEEE SA confirms superseded by 29148:2011. | Confirmed internal issue; official currentness evidence is in `standards-source-register.md`. No doctrine changed. |
| Stale other standards mappings | Registry/gate source cites ISO/IEC/IEEE 42010:2011 and BS ISO/IEC/IEEE 29119-3:2013. Issuers list 2011 and 2013 as withdrawn, with 42010:2022 and 29119-3:2021 published. | Confirmed, currentness record supplied. Clause-level mapping to new versions remains to be reviewed. |
| Thin proof | 159 Phase 01–09 skills; 4 `examples/` folders; 81 worked-example headings; 34 identical generic worked-example paragraphs (current static counts). | Confirmed; sample products do not fix engine inventory. |
| Routing coverage | 71 fixture prompts; static recount finds 0/159 skills with >=3 positives and >=2 owned negatives. Smoke test confirms 47/55 p@1 and 13 local owned-negative passes. | Confirmed. 3 cross-engine negatives remain `NOT_ASSESSED` by this engine alone. |
| Missing DOCX style file | `templates/reference.docx` is absent and ignored by Git; builder exits 1 until someone generates/supplies it. The current style generator uses Calibri/Calibri Light by default, in conflict with the design engine's document defaults. | New confirmed reproducibility and typography defect; temp build used a temporary font-adjusted copy only. |

## Source and currentness disposition

Primary issuer/source checks and precise support states are in `standards-source-register.md`. Issuer records support the currently published editions of ISO/IEC/IEEE 29148, ISO/IEC 25010, ISO/IEC/IEEE 42010, ISO/IEC/IEEE 29119-3 and ISO/IEC/IEEE 26514. They also show stale 42010:2011 and 29119-3:2013 citations in the engine and IEEE 830 as superseded. Current legal currency beyond the consulted Uganda Act consolidation dated 2023-12-31 is partial/unassessed; the 2021 Regulations PDF is verified as a Gazette item but amendment completeness through 2026 is not established. WCAG 2.2 is supported by W3C’s records. Pandoc 3.13 binary hash was verified. Mermaid CLI is pinned at 12.0.0 while Mermaid 12.2.0 is a later release. No archival snapshots were created.

Model currentness: official OpenAI catalogue/release pages were checked. The policy pin remains Luna/high by authority; no account-specific runtime model catalogue or comparative quality benchmark could be inspected. The official-source claim and exact limitation are recorded in the currentness table; a model-policy replacement is not proposed.

## Integrity limits

`50.3/100` is a fresh unweighted arithmetic mean of the ten ratings in `01-baseline-scorecard.md`, not the 2026-09-29 audit’s weighted 54.6; figures are not directly comparable. Scores are evidence-based reviewer judgements, not automated measurements. Current standards registry mismatch is verified at edition/status level only; no paid standards text was accessed for clause remapping. Archive, runtime model catalogue, actual provider behaviour, stakeholder decisions, real implementation tests and Word’s native accessibility checker remain unassessed.
