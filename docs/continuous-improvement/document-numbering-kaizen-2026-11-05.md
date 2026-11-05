# Document numbering kaizen record, 2026-11-05

## Trigger

The owner's standing rule of 5 November 2026: in every multi-tenant SaaS system, existing or new,
every user-facing document number (invoice, receipt, credit note, bill, kitchen ticket, order,
purchase order, goods receipt, stock transfer, adjustment, count, expense, deposit, withdrawal,
journal entry, payroll run and the rest) is contiguous per tenant per document type, and the
surrogate key stays separate. The engineering detail comes from the Maduuka reference plan
(`docs/plans/numbering/` in that repository: decisions, architecture, production rollout,
verification and capacity documents).

## Baseline (measured on `main` at `c8cf4f6`)

A search of every skill, reference, template and domain pack for document, invoice, receipt or
sequential numbering found:

- No skill or template required contiguous document numbers or a numbering section.
- `domains/finance/references/accounting-requirements-gate.md` listed "document numbering" as one word
  in its Controls row, with no requirement behind it.
- `03-design-documentation/01-high-level-design/references/as-built-recovery.md` and an engine test
  fixture used invoice sequences only as an as-built example.
- `domains/uganda/references/nfr-defaults.md` covered the EFRIS fiscal document number, a separate
  authority-issued number.
- The SRS chain (`05-feature-decomposition`, `07-attribute-mapping`), the SaaS NFR catalogue, the
  multi-tenancy architecture spec, database design, API specification, LLD, test plan, acceptance
  criteria, business rules, accounting SRS and design, billing spec and the retail and hospitality
  SRS skills said nothing about numbering, idempotent replays of numbered creates, void-not-delete,
  clash handling, capacity or migration of existing numbers.

Gap: a multi-tenant spec produced by this engine could pass every gate with no numbering
requirement at all.

## Change (standardise)

| Slice | Surface | Acceptance condition |
|---|---|---|
| Reusable requirement block | New `02-requirements-engineering/references/document-numbering-requirements.md` | 28 FR, 7 NFR, 9 transition NFR, 5 DC and 4 CTRL items with ID, rationale and verification method; 20 test cases; acceptance criteria; SRS placement map; document type register; design obligations; review checklist. All ten points of the owner rule are covered. |
| SRS default | `05-feature-decomposition` SKILL and `logic.prompt`, `07-attribute-mapping` SKILL and `logic.prompt`, `01-initialize-srs`, SaaS NFR catalogue section 11 | A multi-tenant SRS gets a "Document Numbering" feature in 3.2 and the NFRs in 3.3-3.6; omission needs a recorded waiver |
| Design default | `10-saas-multi-tenancy-architecture-spec` (new spec section 10, checklist row, `logic.prompt` halt), `04-database-design`, `03-api-specification`, `02-low-level-design`, `16-accounting-engine-design` | Each design document names the single allocator and its data, API and algorithm obligations |
| Verification | `05-testing-documentation/02-test-plan`, `agile/02-acceptance-criteria` | Test plans instantiate TC-DOCNUM cases, at minimum contiguity under concurrency, rollback burns no number, replay returns the same number, void keeps its number, draft delete leaves no gap and history untouched after migration |
| Domain routes | `09-business-rules-analysis`, `18-embedded-accounting-engine-srs`, `13-saas-billing-and-metering-spec`, retail and hospitality SRS skills, finance domain gate | Each links to the block where its documents are numbered |

No new skill was added: the rule is a cross-cutting requirement set, which this engine keeps as a
phase reference (like the SaaS NFR catalogue). No skill description changed, so routing fixtures
are unchanged. One pre-existing defect was fixed in passing: the core-instruction list in
`05-feature-decomposition/SKILL.md` ran 1-6 then 5; it now runs 1-8.

## Check

Run on 2026-11-05 after the change:

| Check | Result |
|---|---|
| `scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | 159 active skills, 1 template, failure counts empty |
| `scripts/routing_smoke_test.py` and `--min-rank1 83 --lint-fixtures --min-covered 8` | precision@1 floor met; 0 fixture lint findings; 8 of 159 covered; 3 cross-engine negatives `NOT_ASSESSED` as before |
| `scripts/source_ingestion_guardrail.py` | 0 findings |
| `scripts/check_portable_paths.py` | PASS |
| `scripts/check_cross_engine_refs.py --dev-engine-root <dev engine>` | PASS |
| `scripts/check_standards_currency.py` | PASS |
| `scripts/validate_source_register.py` | PASS, 18 records as of 2026-11-05 |
| `python -m engine validate-skills` | OK |
| Dev-engine `quick_validate.py` on the 15 changed skills | all valid |
| `scripts/validate_plugin_packages.py` | 2 errors (checkout and package file counts over 5,000). Same result with this change stashed; caused by local untracked workspace content, not by this change. |
| `pytest` | Coverage 96.75% (gate 90%); 4 failures, all host conditions unrelated to this change: two DOCX build tests (the WSL `bash` cannot attach its disk) and two portable-path tests (`git add` of a `.claude/` path refused on this host). The portable-path pair fails identically with the change stashed. |

## Currentness

No external standard, law, platform capability or version is admitted. Default thresholds
(50 ms p95 lock wait at 40 parallel issuers, 200 documents per second, 5 ms lookups and a 60 s
incremental gap check at 10 million documents) are the reference plan's lab gates, marked
*default* in the block, and must be replaced by project measurements. The RFC 8259 note on JSON
integer precision is stable protocol text. Fiscal-authority numbering rules stay `NOT_ASSESSED`.
Review date: 2027-05-05.

## Next cycle

- Add a deterministic kernel check that flags a multi-tenant SRS with numbered documents but no
  FR-DOCNUM items and no waiver.
- Add a golden-path example SRS section built from the block.
- Re-measure after the first project SRS uses the block.
