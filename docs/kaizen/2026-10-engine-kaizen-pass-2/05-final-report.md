# Chwezi SDLC Documentation — Kaizen pass 2 final report

**Branch:** `kaizen/2026-10-pass2`, created from `main` at `91b987d`, which is also the branch the checkout started on and is restored when the work ends. The commits are listed by hash below and in `git log main..kaizen/2026-10-pass2`. Nothing pushed, tagged, released or submitted; no paid model call; no other engine edited. The 95/100 target is not reached.

## Scorecard

Ratings are reviewer judgements against the evidence in `01-baseline-scorecard.md`, `03-experiment-log.md` and `04-validation-record.md`, using the same ten dimensions and unweighted mean as the 29 October cycle. They are not measurements of customer outcome and have not had an independent acceptance review.

| Dimension | 29 Oct final | Fresh baseline | Final | What moved and what is still short |
|---|---:|---:|---:|---|
| Doctrine | 62 | 61 | 63 | The router no longer contradicts itself about engine locations, and WCAG doctrine and templates agree. Clause mappings to IEEE 830, 42010:2011 and 29119-3:2013 are unchanged and still stale. |
| Taxonomy and routing | 58.8 | 58.8 | 61.3 | The contradictory-brief task ranks its owning skill first instead of tenth; precision@1 57/65 to 64/72 (88.9%); coverage 4 to 8 of 159 with a CI floor. The literal school-fees prompt still ties with the multi-tenancy skill (9.01 against 9.00) and the spelled-out SRS phrase ranks the game SRS skill first in the proxy. |
| Skill depth | 56 | 56 | 56 | No depth change; five skill files remain above the report-only byte threshold. |
| Applied proof | 43 | 43 | 43 | Unchanged: 4 `examples/` folders; 44 skills share one identical worked-example paragraph. |
| Standards currency | 38 | 38 | 44 | Review dates are now enforced; seven claims re-verified and dated; a ratchet stops stale citations growing. Clause remapping, ISO draft stage and Uganda legal currency remain open or partial. |
| Output readiness | 59 | 56 | 59.5 | Phase 02 and Phase 05 checks give correct answers on the three probes. Unique-definition and NFR traceability checks are still missing, and the `.docx` build was not assessable. |
| Accessibility and inclusion | 52 | 50 | 53 | Six engine templates target WCAG 2.2 AA. Sixteen domain-pack lines still say 2.1 (owner decision); native Word accessibility not assessed. |
| Production and handoff | 53 | 50 | 53 | A missing package now gives a named cause and exit 2; CI runs six more checks. Pandoc and Mermaid builds were not assessable here and the CI file was not run. |
| Hygiene | 54 | 48 | 60 | Live machine-specific paths 43 lines to 0; no tracked per-user settings; 8 dangling references repaired; three guards in CI. The settings file and old paths remain in git history. |
| Safety and integrity | 64 | 61 | 64 | The permissive allowlist and personal data are out of the tree. An absent source register still passes Phase 02 (owner decision), and history still holds the file. |

**Final raw mean:** (63 + 61.3 + 56 + 43 + 44 + 59.5 + 53 + 53 + 60 + 64) ÷ 10 = 556.8 ÷ 10 = **55.68/100**.
**Portfolio cap 65:** `min(55.68, 65) = 55.68/100`. **User initial cap 45:** `min(55.68, 45) = 45/100`.
Comparison: fresh baseline raw 52.18 (capped 52.18); 29 October final raw 53.98 (capped 53.98). The 29 October final was judged on surfaces that cycle inspected; this pass found and fixed defects on surfaces it had not looked at.

## Critical defect

D-01, a developer's local permission file tracked in this public repository (personal and client names, unrestricted shell allowlist), is **fixed in the tree** (`de1efdf`) and verified by a check that fails before and passes after. It is **escalated in part**: the file remains in git history and removing it needs a history rewrite, which this cycle may not do. If any secret or client-identifying detail in that file matters, the owner must decide on a rewrite and force-push.

## Kept changes

| ID | Change | Commit |
|---|---|---|
| K2-01 | Untrack local settings, ignore them, fail on tracked `*.local.json` | `de1efdf` |
| K2-02 | Repair eight dev-engine references; offline reference checker with configurable root | `2ccbf36` |
| K2-03 | Portable wording in 18 live files; machine-path scan with a capped history allowance | `b8f17be` |
| K2-04 | Phase 02 NFR check and Phase 05 trace check corrected, 28 new tests | `08dae96` |
| K2-05 | Routing description for contradictory briefs, 8 fixtures, `--coverage` and `--min-covered` | `17c2179` |
| K2-06 | Six templates to WCAG 2.2 AA; standards-citation ratchet | `87fa205` |
| K2-07 | Source-register review-date validator and re-verified pass-2 register | `4a48a5c` |
| K2-08 | First-run dependency message; six CI steps | `e2e80e1` |
| Docs | Router release gate and changelog | `f15543f` |

**Reverted:** none. Two process slips (a recovered `git stash` and a blocked `rm -rf`) and two measurement corrections are in `03-experiment-log.md`.

**Corrections to the frozen baseline (file not edited):** it records 14 claims in the 29 October register, which has 17; it counts 9 flat-layout matches where the correct figure is 10; it describes five WCAG 2.1 prescriptions where there were six engine-level lines.

## Residual risk

- **Tightened Phase 02 check.** A client NFR that passed with a bare qualifier ("responsive", "at all times") can now fail until a threshold is added. No in-repo project is affected; client projects were not available to test.
- **Source-register check is date-driven.** CI will fail once the earliest review date passes (2026-11-29 for the plugin and marketplace claims) until the claim is re-verified. That is the intended currentness gate.
- **Ratings are judgement-based** and the registered validators, pytest suite, Phase 09 registry checks, `.docx` build, live routing and native Word accessibility were not run on this host.
- **Standards:** IEEE 830, 42010:2011 and 29119-3:2013 clause labels remain; the ISO 29148 third-edition stage and Uganda legal currency through 2026 are `partial` or `NOT_ASSESSED`.

See `06-next-cycle.md` for open findings, the decisions needed, cross-engine mismatches and the next experiment.
