# Frozen SDLC Documentation baseline

Cycle 2026-11-28-four-engine-book-kaizen. Checkout clean before validation at `09b84e76f98189ba4786f6190641226a46a4963a`, on `kaizen/2026-11-28-four-engine-book-kaizen` after integrating owner and upstream changes. Origin is the public SDLC Documentation repository. No concurrent Jidoka or auto-agents writer for this checkout was identified in the Windows process snapshot. The cycle used the account-confirmed GPT-6.2 Sol model and retained pins. Local model-policy check passed. Claude account availability and comparative local quality/cost/latency are NOT_ASSESSED.

| Dimension | Score | Status | Confidence | Revision-bound evidence |
|---|---:|---|---|---|
| Routing | 58 | FAIL | Medium | Documented lexical smoke 67/75 first and 75/75 top three. Four of ten new phrasing trials reached top three and two reached first. Explicit skill routes exist, yet generic SRS and cross-domain phrases surfacing game or AI artefacts reproduce known ambiguity. Live model outcomes NOT_ASSESSED. |
| Skill quality | 60 | FAIL | Medium | `validate_skill_engine.py` reports no structural failures. Phase 06 deploy guide recognizes forward-fix-only migrations but still requires unconditional reversal in its acceptance checklist and generation prompt. Existing examples vary in specificity. |
| Duplication and drift | 49 | FAIL | High | `AGENTS.md` and full Kaizen prompt point to superseded default research routing. Deployment guide and its logic prompt duplicate and contradict recovery rules. Prior scorecard records unresolved repeated example prose. |
| Evidence and currentness | 63 | FAIL | Medium | Source registers and date checks exist. Prior report separates historical draft layout from current standards, but many clause labels retain superseded editions and the main currentness route selects a retired default. Currentness requirement crosses a near-term review boundary. |
| Validators and tests | 68 | FAIL | Medium | Ranking has positive and negative controls. Root and engine suites exercise actual parser and gate paths. Demo positive and sabotage run through real CLI. Outstanding Windows-specific results are in validation record. |
| Token cost | 68 | PASS | High for bytes | Strict token-budget lint exit 0. AGENTS 31,293 B, CLAUDE 44 B, README 52,102 B. Five long skill files produce report-only warnings. Actual runtime tokenizer cost NOT_ASSESSED. |
| Security and safety | 50 | FAIL | Medium | Controlled destructive-hook suite tests refused and allowed operations. Windows fixture failures involve unverified repository configuration. Prior README identifies historical per-user settings file. No credentials were inspected; external efficacy and historical secret audit are NOT_ASSESSED. |
| Install and packaging | 65 | NOT_ASSESSED | Medium | Windows checkout, locally installed Python and Node, maintained package validator. 45 tracked scripts files. Standalone fresh install and installed-host behavior across Windows and Linux are NOT_ASSESSED. |
| Human-facing English | 57 | FAIL | Medium | README's task navigation works by document name. Historical passes, dates, releases and quarterly quality detail exceed a first-time operator's decision needs. Deployment acceptance checklist is short but can mandate an unsafe action. |
| Kaizen system | 68 | FAIL | High | Existing two October evidence packs report cap, kept changes, and review dates. Prior next-cycle evidence lists routing coverage and unresolved authority decisions. Stale currentness route and repeated template contradiction remain visible. |

Unweighted raw score **60.6/100**. Published baseline after the cap of 65 is **60.6/100**. Scores are reviewer judgements on the recorded evidence with one incomplete environment dimension, so they carry no live acceptance or certification claim. Any confirmed unsafe action, disclosure or data-loss boundary stands outside the average.

## Ten routing trials

Lexical proxy from `scripts/routing_smoke_test.py` using `read_catalogue()` and `rank()` over these phrases. The predicted owner is a manually identified skill for the job.

| Phrase | Predicted owner | Observed rank | First place |
|---|---|---:|---|
| Before we start, draft a product requirements document for a school maintenance portal with users, measures and scope. | 01-prd-generation | 18 | 15-game-product-and-production-brief |
| Write out assumptions and dependencies for a new cost-saving internal platform, then explain why we should fund it. | 02-business-case | 2 | 12-ai-cost-runbook |
| Initialize a software requirements specification using stakeholder evidence for a clinic reservation service. | 01-initialize-srs | 4 | 19-game-software-requirements-specification |
| For an approved external interface, document the provider's endpoints, authentication, idempotency and OpenAPI schemas. | 03-api-specification | 1 | 03-api-specification |
| Record why we picked a shared database instead of separate storage per client and what trade-off we accepted. | 05-architecture-decision-records | 86 | 09-sign-off-ledger |
| Turn reporting acceptance criteria and functional requirements into a test plan with boundary cases and recovery checks. | 02-test-plan | 2 | 08-accounting-engine-test-plan |
| Write a release deployment guide with numbered infrastructure and application steps, rollback and migration verification. | 01-deployment-guide | 1 | 01-deployment-guide |
| Write an incident response runbook explaining how a support engineer diagnoses a failed background job. | 02-runbook | 15 | 14-ai-incident-response-runbook |
| Convert signed Waterfall requirements into Scrum work while preserving links to the approved baseline. | hybrid-synchronization | 4 | 11-requirements-reuse |
| Write a printable onboarding guide for staff who need to reset a user password and export a register. | 01-user-manual | 5 | 09-ai-agent-user-disclosure-pack |

## Inventory and local residue

- Git tracks 160 numbered-phase SKILL.md files, including one template, 261 numbered-phase reference files, 45 files under `scripts/`, and 173 files in `tests/` and `engine/tests/`.
- A separate filesystem search counted 30,592 files under `scripts/diagram-render/`, overwhelmingly ignored `node_modules/`. That folder has a local ignore rule. Restore dependencies from the documented renderer install when required.
- Both root egg-info directories and `.coverage` are untracked local outputs. The tracked `.pre-commit-config.yaml` runs a real project-workspace validation hook and serves an active purpose.
- Keep prior authority questions open until resolved. The October record identifies Phase 02 optional source-reconciliation registration, superseded clause labels, Phase 09 missing identifier families, education jurisdiction, standards levels and history treatment.
