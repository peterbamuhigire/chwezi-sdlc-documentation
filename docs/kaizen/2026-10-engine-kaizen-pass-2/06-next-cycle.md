# Next cycle — open findings, decisions needed and one bounded experiment

**Proposed re-audit:** 2026-11-30, or earlier if CI reports an overdue source record (the first review dates pass on 2026-11-29). No cross-engine edit is authorised by this record.

## Decisions needed from the owner

| Question | Evidence | Options |
|---|---|---|
| Should a project with no `_registry/source-reconciliation.yaml` fail Phase 02? | Paired run (`00-scope-and-evidence.md`): the same five requirements pass with the register absent and fail with five blocking findings when it is present. The check returns nothing when the file is missing (`engine/checks/source_reconciliation.py:29`). | Keep optional; warn at MEDIUM; or require it for new projects and give existing projects a dated waiver. |
| Retire IEEE 830 from gate clause labels, or keep it as a named layout reference only? | IEEE SA lists it as superseded (register record C-IEEE830). The router already calls it layout-only, while `engine/gates/phase02.py` (lines 11 to 15), `docs/standards-clause-registry.md` and 57 files cite it by clause. | Layout-only wording everywhere with new clause labels from ISO/IEC/IEEE 29148:2018 once the owner supplies clause text; or keep the labels and add a visible "historical layout" note. |
| Should Phase 09 trace NFR, IR, DR and CON identifiers and should duplicate definitions block? | Probe: an NFR with no goal link and no test case raised nothing (`engine/checks/traceability.py:31`); two `**FR-001**` definitions raise nothing and `engine/sync.py:62` always returns an empty error list. Both are blocking rules that could fail existing client projects. | Add as MEDIUM first, measure on the seven focus projects, then promote with a migration note. |
| Should the education domain pack gain a school-fees module and a jurisdiction gate? | `domains/education/INDEX.md` is a United States baseline (FERPA, COPPA, Section 508) with no fee or receipt module, and `scaffold` writes only `domain: education`. | Add a fees and receipts feature module and a jurisdiction note; or add an East Africa pack beside `uganda`. |
| Move the 16 domain-pack WCAG 2.1 lines to 2.2? | `domains/education`, `government` and `retail` pair WCAG 2.1 with Section 508 or ADA references whose adopted level is a legal question. The ceiling in `tests/standards-currency-baseline.json` holds them at 16. | Keep per jurisdiction with a dated legal source, or move to 2.2 where no legal level is cited. |
| Rewrite git history to remove the committed local settings file? | `de1efdf` removed it from the tree; earlier commits still contain it. | Leave (it is a permission list, not a secret); or rewrite and force-push under separate authority. |

## Open findings

| Finding | Exact files and evidence | Next evidence |
|---|---|---|
| Lexical routing near misses | `scripts/routing_smoke_test.py` ranks `10-saas-multi-tenancy-architecture-spec` (9.01) above `01-initialize-srs` (9.00) for the literal school-fees sentence, and ranks `19-game-software-requirements-specification` first (17.0) for the spelled-out "software requirements specification". A fixture for either would fail rank one today. | Live-model routing evidence (not run: no model calls) before changing any description, so the proxy is not gamed. |
| Applied proof is thin | 4 of 159 skills have `examples/`; 12 groups of skills (44 skills) share one worked-example paragraph under their "Worked Example" heading. | Per-skill worked examples grounded in fixtures, starting with the skills at the route-coverage target. A ratchet alone would only freeze the debt. |
| Route coverage | 8 of 159 meet three positives and two owned negatives (7 excluding cross-engine owners). | Add fixtures for the next ten skills named in the three tasks; raise the CI floor each time. |
| Standards clause mappings | 167 live lines cite IEEE 830 (163 excluding the ratchet's own data); 42010:2011 in 4 files; 29119-3:2013 in 6 files (`engine/gates/phase03.py`, `phase05.py`). | Owner decision above, authoritative clause text, then a remap with fixtures. |
| Cross-engine names beyond the dev engine are not machine-checked | Accounting and design engine skill names (for example `finance-ui-pattern-library`, `inventory-costing-and-stock-accounting`) were verified by hand this cycle only. | Extend `check_cross_engine_refs.py` with optional accounting and design roots. |
| Build pipeline not assessable on this host | Pandoc and Mermaid CLI absent; Pandoc 3.13 and Mermaid 12.0.0 pinned (core 12.2.0 exists, compatibility untested). | Run the `.docx` build and a diagram render on a host with both; check the Mermaid 12.2.0 upgrade in a disposable render. |
| Registered validators need the pinned packages | `requirements-ci.txt` set not installed here; the traceability validator lacks the friendly message the catalogue scripts now have. | Run the full registered set in the pinned environment; give `validate_traceability_evidence.py` the same guard. |
| Uganda legal currency | ULII and ISO pages returned HTTP 403 to the fetch tool; ISO 29148 third-edition stage is reported inconsistently by secondary sources. | Read the primary pages from a host that can; consult Gazette and Parliament sources before any legal requirement is drafted. |

## Cross-engine mismatches (recorded only; no other engine was edited)

1. **Dev engine alias targets use a prefix that no longer exists.** `docs/skill-aliases.yml` in the Chwezi Dev Engine (lines 62 to 66, and the matching `ALIAS.md` in `skills/frontend-ux/pos-restaurant-ui-standard/`, `skills/frontend-ux/pos-sales-ui-design/` and `skills/finance-accounting/inventory-management/`) routes to `doctrine/skills/<name>`. The accounting engine now keeps those skills at `skills/16-ux-and-presentation/finance-ui-pattern-library/SKILL.md` and `skills/04-subledgers-and-operations/inventory-costing-and-stock-accounting/SKILL.md`. Line 70 of the same alias file uses `design-system/skills/ai-agent-ux`, while the design engine holds it at `skills/04-web-and-ui-design/ai-agent-ux/`. For the dev-engine cycle.
2. **Dev engine has no `gis-mapping` skill, but its alias file lists it as absorbed.** `docs/skill-aliases.yml` lines 337 to 340 name `gis-mapping` under `gis-platform-engineering`, whose `skills/gis/` directory holds only `gis-enterprise-domain` and `gis-platform-engineering`. The SDLC reference now cites `gis-platform-engineering`. For the dev-engine cycle.
3. **The dev engine's `product-business/experiment-engineering` is an inactive alias** routed to `skills/ai-feature-rollout-and-experimentation`, a skill whose name reads as AI-specific. The SDLC experiment-requirements reference now cites the successor as the alias map directs; the dev-engine owner should confirm it covers non-AI experimentation platforms.
4. **Three owned negatives remain `NOT_ASSESSED` locally**: `neg-business-case-vs-social-roi`, `neg-business-case-vs-proposal-roi`, `neg-business-case-vs-business-plan`. Owners are in the social, proposal and business-plan engines; evaluate them in the portfolio union.
5. **Accounting overlay.** The school-fees exercise touched money flows, mobile-money receipts and settlement but produced no ledger or tax requirement. If a real project carries those, route it through the accounting engine as a cross-cutting review before baselining. This is a scope condition, not a validation of the overlay.

## One small experiment for next time

Take the default NFR blocks that name WCAG 2.1 (`domains/education/references/nfr-defaults.md` and `domains/government/references/nfr-defaults.md`) and, in a disposable copy only, scaffold one project from each with the WCAG line changed to 2.2. Run the Phase 02 checks and the standards ratchet before and after, and ask the owner which jurisdictions must keep 2.1. Success evidence: the paired gate output, the ratchet counts, and a written owner answer per domain. No pack is edited until that answer exists.

## Re-audit entry criteria

- Re-run `scripts/validate_source_register.py` with the real date and re-verify every claim it reports as overdue or due soon.
- Re-run all registered validators and the pytest suite in the pinned environment, and the `.docx` build on a host with Pandoc and Mermaid CLI.
- Confirm the three owner decisions on source-register policy, IEEE 830 labels and NFR tracing before touching any gate policy.
- Record the root reviewer disposition and integrate only after that review; this branch has not been pushed.
