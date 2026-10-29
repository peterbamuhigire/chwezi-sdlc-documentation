# Next cycle — open findings and one bounded experiment

**Proposed re-audit:** 2026-11-30, subject to portfolio scheduling. No cross-engine edits are authorised by this record.

## Open findings

| Finding | Current evidence and exact files | Owner / next evidence |
|---|---|---|
| Standards clause registry is stale | `AGENTS.md` describes IEEE 830 as superseded, while `docs/standards-clause-registry.md`, `engine/gates/phase02.py`, and phase 03/05 gates still attach checks to IEEE 830-1998, ISO/IEC/IEEE 42010:2011 or BS ISO/IEC/IEEE 29119-3:2013. The issuer edition/status records are in [`standards-source-register.md`](standards-source-register.md). | Standards/doctrine owner to approve the status of IEEE 830 and provide authoritative clause text or approve a non-normative status-only change. Do not remap clauses by inference. |
| Source completeness remains human-owned | `engine/checks/source_reconciliation.py` validates only statements and ambiguities that the project register declares. It cannot prove omitted source statements were captured or determine semantic conflict. | Requirements analyst and independent reviewer to compare each project register with its source brief; record review evidence with the project baseline. |
| Task 2 owner decisions remain unresolved | Disposable task 2 fixture has six unresolved `AMB-###` records and Phase 02 blocks ([validation record](04-validation-record.md)). | A project owner would need to decide the alternatives; no answer is assumed by the engine. |
| Trace chain lacks business-goal evidence and execution | The disposable task 3 matrix links 10 requirements to design and test IDs, but has zero goal links, seven open owner decisions, and zero executed tests ([validation record](04-validation-record.md)). | A real project must supply approved goals, accountable decisions and product test execution before any acceptance claim. |
| Local route coverage is still sparse | Current fixtures cover four touched skills to the three-positive/two-owned-negative target, but only 4 of 159 skills meet it. Three cross-engine owned negatives are still `NOT_ASSESSED` ([validation record](04-validation-record.md)). | Continue with a small priority set, and validate cross-engine negatives in the portfolio union rather than treating them as local passes. |
| Public package acceptance is unknown | Local Claude/Codex manifests validate and both native CLI installs pass offline. The repository's phase-root skill layout still needs a portable package build; no public ZIP or directory submission was attempted. | Plugin owner to build the documented portable layout, test a clean archive against official constraints, and submit only under separate authority. |
| Current engine handoffs depend on the dev-engine public tree | SRS [API specification](../../../03-design-documentation/03-api-specification/SKILL.md) links to `chwezi-dev-engine/skills/architecture/api-design-first/references/api-error-handling.md` and `api-pagination.md`. SRS [database design](../../../03-design-documentation/04-database-design/SKILL.md) links to `chwezi-dev-engine/skills/backend-databases/mysql-engineering/references/mysql-best-practices.md`. The paths were verified in the public `main` tree and recorded under C-DEV-REFERENCES. The dev-engine content was not edited or semantically reviewed. | Dev-engine owner should retain those paths or notify SRS when references move; local automated validation of sibling repository contents is not yet available. |
| Legal, accessibility, release and archival limits remain | The source register records partial legal-currentness for Uganda, and Word accessibility/font embedding and source archival were not assessed. | Consult current legal sources for a real product; run native accessibility review and archive selected sources when required by the project. |

The design, accounting and proposal engines were not edited. No additional evidence in this SRS-only cycle established a confirmed mismatch in their exact skill inventories. The task 1 school-fees exercise did not supply journal, settlement, tax or ledger requirements; if a future scope includes those decisions, route it through the accounting engine as a cross-cutting review before baselining. This is a scope condition, not a finding that the accounting overlay was validated.

## One small experiment for the next cycle

Create one disposable Phase 02 project pair with identical requirements: one with a completed source register and one with the register absent. Compare the current optional-gate behavior with the intended portfolio requirement, document migration impact for existing projects, and ask the requirements owner whether missing registries should block Phase 02. Do not change gate policy until that decision is recorded. Success evidence is the paired gate output, owner decision, and a migration note; no production project is used.

## Re-audit entry criteria

- Recheck source-register review dates and issuer status pages.
- Verify that the six task 2 ambiguities are still reported as blockers in the fixture.
- Re-run the registered validators and both native offline marketplace tests.
- Review any authority or evidence received for the standards mappings before changing canonical doctrine.
- Record the root reviewer disposition and integrate only after that review; this branch has not been pushed.
