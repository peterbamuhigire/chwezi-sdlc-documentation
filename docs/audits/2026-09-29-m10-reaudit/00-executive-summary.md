# Executive summary

## Verdict

**Published 54.6 / 100. Engine Eval Readiness 58.5 / 100.** The engine sits in the 40–59 band
("competent; major gaps"). The kernel and render pipeline sit at the upper end of that band. The
skill layer and applied proof pull the overall score down. No dimension, group or output type
scores 70 or above.

## Headline findings

1. **Applied proof is thin at skill level.** 4 of 159 skills ship an `examples/` folder with
   inputs and expected output: `waterfall/01-initialize-srs`, `05-architecture-decision-records`,
   `05-testing-documentation/02-test-plan` and `04-development-artifacts/03-dev-environment-setup`.
   The test-plan example has two test cases. 81 SKILL.md files contain a `## Worked Example`
   heading, but the body is one generic paragraph. 34 of those paragraphs are the identical
   sentence beginning "Given an approved project source and a conflicting implementation detail".
   These sections count as boilerplate, not proof.
2. **CI is red, caused by an absolute machine path.** The remote "Engine" workflow fails at HEAD
   (run 36520102250) with `broken_relative_link` in
   `02-requirements-engineering/hospitality-operating-model-srs/SKILL.md`. Lines 156–157 link to
   `C:/wamp64/www/...`. The link resolves on this host and nowhere else. It also breaks the
   router's own rule that engine locations are resolved per device and never hard-coded.
3. **Cross-engine skill references are dangling, and nothing detects them.**
   `03-design-documentation/04-database-design/SKILL.md` makes `skills/mysql-best-practices/`
   **MANDATORY** for MySQL/MariaDB (lines 138, 245, 254). `03-api-specification/SKILL.md` cites
   `skills/api-error-handling/` and `skills/api-pagination/`. None of these exist in
   chwezi-dev-engine. The nearest real skill is `backend-databases/mysql-engineering`. The M10-12
   commit "canonical dev skill names" missed them, and all four validators pass anyway.
4. **Standards currency is internally inconsistent.** `AGENTS.md` records IEEE 830-1998 as
   superseded by ISO/IEC/IEEE 29148:2018. Even so, `docs/standards-clause-registry.md` maps all
   six Phase 02 kernel checks to IEEE 830-1998 clauses, and 18 skills still cite IEEE 830. The
   registry maps Phase 03 to ISO/IEC/IEEE 42010:2011. The business case cites IEEE 1058-1998 as
   its governing standard. The registry records no access, verification or review dates. This
   dimension is judged from the engine's own currentness records; no fresh external research was
   done.
5. **Routing is measured at 58.5, and fixture coverage is zero.** Precision@1 is 47/55 (85.5 %).
   All 13 locally owned negatives pass, and 3 are mirrored in union mode. Collisions are clean.
   However, no skill has three positives and two owned negatives (0/159), and Tier 3 is
   NOT_ASSESSED. The rank-1 floor of 83 % leaves 2.5 points of headroom.
6. **The taxonomy has structural debt.** There are seven duplicate numeric prefixes (for example
   `06-deployment-operations/13-ai-agent-slo-doc` and `13-ai-incident-severity-matrix`). Group
   02 holds 41 skills under four different nesting schemes. An AI/agent sub-catalogue of about 35
   skills is spread across all nine groups. The union scan reports a within-engine collision
   between `09-saas-incident-response-and-postmortem` and `14-ai-incident-response-runbook`
   (cosine 0.756).

## What is strong

- The validation kernel (`python -m engine`) covers validate, sync, baseline, waive, signoff,
  pack, diagrams and controls. It has 432 passing tests, 2 skipped, and 96.86 % coverage against
  a 90 % gate. Waiver integrity has negative tests.
- The typed diagram IR (`engine/diagram_ir.py`) produces generated Mermaid and a generated trace
  table. The build (`scripts/build-doc.sh`) renders figures first and fails closed if any Mermaid
  survives or a figure is missing. It also writes a SHA-256 figure manifest. The read-only scan
  found 691 DOCX files with 0 containing Mermaid. It correctly flagged the two GarageFlow
  placeholder screenshots.
- Core design skills are current: OpenAPI 3.1.2 (with a 3.2 decision rule), JSON Schema 2020-12,
  RFC 9457, WCAG 2.2 AA, ISO/IEC 25010:2023 and ISO 9241-210:2019.
- Governance doctrine is explicit: fail tags, the IEEE 1012 V&V SOP, the Human Review Gate,
  grounding without invention, the source-ingestion guardrail (0 findings), and client workspaces
  kept out of git.

## Path to the bar

P0 fixes CI, the dangling references and the Phase 02 standards mapping, and adds validator rules
so none of these can recur. Target: published about 57, Readiness about 60. P1 replaces boilerplate
worked examples with real input/output examples for the 12 core output types and raises fixture
coverage. Target: about 61. P2 needs spend and stakeholder authority: Tier-3 behavioural runs, a
representative end-to-end project chain with rendered-DOCX review, and portfolio craft-standard
acceptance evidence. Target: raw about 66, published capped at 65 until that evidence exists. See
`10-roadmap-to-world-class.md`.
