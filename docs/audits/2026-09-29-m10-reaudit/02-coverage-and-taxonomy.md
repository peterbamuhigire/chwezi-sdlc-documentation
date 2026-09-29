# Coverage and taxonomy

**Taxonomy and structure: 55 / 100 (judged).**

## Inventory (measured by `validate_skill_engine.py` and a git-tracked inventory)

| Group | Skills | Mean SKILL.md size | Skills with no `references/` | Skills with `examples/` |
|---|---:|---:|---:|---:|
| 01-strategic-vision | 13 | 10.4 KB | 2 | 0 |
| 02-requirements-engineering | 41 | 11.6 KB | 13 | 1 |
| 03-design-documentation | 18 | 12.3 KB | 3 | 0 |
| 04-development-artifacts | 6 | 12.3 KB | 2 | 1 |
| 05-testing-documentation | 10 | 12.4 KB | 2 | 1 |
| 06-deployment-operations | 23 | 12.0 KB | 3 | 0 |
| 07-agile-artifacts | 5 | 12.8 KB | 2 | 0 |
| 08-end-user-documentation | 9 | 11.6 KB | 4 | 0 |
| 09-governance-compliance | 34 | 11.5 KB | 12 | 1 |
| **Total** | **159** | | **43** | **4** |

Group 02 has six shared reference files under `02-requirements-engineering/references/`, so
some of its 13 skills without their own references do reach shared material.

## What is sound

- The nine groups follow the software life cycle and are easy to explain. The phase-order doctrine
  (vision → requirements → design → development → test → deployment → agile → user docs →
  governance) matches the deterministic gate files `docs/deterministic-gate-phase01..09.md`.
- Routing is discovered from the file tree, not from a hand-kept index (`AGENTS.md` line 99).
  Structure validation reports zero findings.
- Domain packs (`domains/`, 11 domains) are kept apart from skills, which is correct.

## Named deficiencies

1. **Duplicate numeric prefixes (7).** `09/05-architecture-decision-records` and
   `09/05-formal-review-gates`. `09/06-ccb-charter` and `09/06-change-impact-analysis`.
   `06/13-ai-agent-slo-doc` and `06/13-ai-incident-severity-matrix`. `06/14-ai-agent-runbook` and
   `06/14-ai-incident-response-runbook`. `06/15-ai-agent-rollout-runbook` and
   `06/15-ai-rca-taxonomy-doc`. `04/05-ai-agent-coding-guidelines-addendum` and
   `04/05-game-technical-implementation-specification`. `02/fundamentals/before/04-...` and
   `during/04-...`. The numbers no longer mean order or identity.
2. **Group 02 is a grab-bag.** Its 41 skills sit under four schemes:
   `fundamentals/{before,during,after}/NN`, `waterfall/NN`, `agile/NN` and `hybrid/`. Beside
   these are flat `13`–`19` (SaaS billing, AI PRD, accounting SRS, game SRS) and two unnumbered
   domain SRS skills (`hospitality-operating-model-srs`, `retail-operating-model-srs`).
3. **The AI/agent cluster cuts across every group.** About 35 skills carry `ai-` in their name:
   strategy, PRD, architecture, model card, prompt spec, evals, red team, six operations
   runbooks and SLO documents, and ten agent compliance packs (SOC 2, ISO 27001, HIPAA, BAA,
   attestation and others) in group 09. This is a product line inside the engine, with no index
   or entry skill.
4. **The game cluster is seven thin skills.** The seven smallest SKILL.md files in the engine
   (3.7–6.0 KB) are the game series. Each has one or two references and no example.
5. **Tools are filed as governance artefacts.** `09-governance-compliance/plan-canvas` is an
   interactive canvas tool with a Node server, not a governance deliverable.
6. **Overlap inside the engine.** The union scan reports `09-saas-incident-response-and-postmortem`
   and `14-ai-incident-response-runbook` at cosine 0.756. Other pairs overlap by design, including
   `13-ai-incident-severity-matrix`, `15-ai-rca-taxonomy-doc` and
   `16-ai-incident-postmortem-template`, which could be references of a single incident skill.
7. **Small groups.** `07-agile-artifacts` (5) and `04-development-artifacts` (6) are thin, while
   02 (41) and 09 (34) are heavy.

## Coverage gaps (missing output types for an SRS/lifecycle engine)

These are judged against the output types the engine claims to cover:

- Data migration and conversion plan. `04-database-design` step 10 covers schema migrations only.
- Security requirements and threat-model specification. Phase 03 gates on
  `security_threat_model_present`, but no skill produces the threat model outside the AI red-team
  plans.
- Accessibility conformance report (ACR/VPAT-style) and an accessibility test plan.
- Disaster recovery / business continuity plan with RTO/RPO tests.
- Administrator guide and training materials. Group 08 has user manual, installation, FAQ,
  release notes and SaaS go-to-market documents.
- An as-built recovery skill. As-built recovery exists only as
  `03-design-documentation/01-high-level-design/references/as-built-recovery.md` and a kernel
  test fixture.
- Performance and load test design as its own skill. It is currently a step inside `02-test-plan`.

## Proposed structure (P1, non-breaking)

- Keep the nine phase roots. Resolve duplicate prefixes by renumbering with alias blocks, and
  add a validator rule that rejects duplicate prefixes within a folder.
- Split group 02 into `02-requirements-engineering/{fundamentals,waterfall,agile,hybrid,domain}`.
  Move 13–19 and the two operating-model SRS skills under `domain/`.
- Add an `ai-and-agents` entry skill, or index reference, that routes the ~35 AI skills by
  life-cycle stage. Fold the incident sub-skills into one incident skill with references.
- Move `plan-canvas` to `scripts/` or a tooling folder.
