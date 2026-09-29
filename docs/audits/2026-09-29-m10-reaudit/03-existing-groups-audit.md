# Existing groups audit

All scores are judged. They draw on the machine inventory (every skill) and on 17 sampled
SKILL.md files, which were read in full or in their operational body.

## Cross-cutting observations (all 159 skills)

- **Two-layer SKILL.md.** Each file opens with a `dual-compat` contract block: Use When, Inputs,
  Workflow, Outputs, Evidence, Capability boundaries, Degraded mode, Decision rules, Quality,
  Anti-patterns. The older operational body follows. In 28 skills (12 in group 01, 16 in group 03)
  the contract Workflow is the same six generic steps ("Apply the decision rules below before
  drafting; stop on a missing authority..."). The contract layer adds governance, but it
  duplicates and sometimes contradicts the body.
- **Boilerplate "Worked Example".** 81 skills have a `## Worked Example` heading. 34 carry the same
  paragraph, and the rest carry one-sentence variants. None shows an artefact.
- **Real examples.** There are 4: `02/waterfall/01-initialize-srs`,
  `09/05-architecture-decision-records`, `05/02-test-plan` and `04/03-dev-environment-setup`.
  Kernel fixtures (`engine/tests/fixtures/healthcare_admissions`, `tiny_project`,
  `requirements_traceability`, `diagram_*`) and `templates/project-examples/uganda-public-sector`
  give engine-level proof, but no skill links to them as its example. The one exception is the
  HLD, which cites the healthcare fixture.
- **Oversize.** 6 skills exceed the 20 KB report-only limit. The largest is
  `03/05-ux-specification` at 33.7 KB.

## Per-group scores

| Group | Score | Justification |
|---|---:|---|
| 01-strategic-vision (13) | 56 | The PRD and lean canvas are deep, and the PRD adds opportunity-risk and outcome-roadmap references. The business case is weaker: its formula is ambiguous, it cites IEEE 1058-1998, and the sensitivity step named in its description is missing from the body. There are no examples. SaaS/AI briefs 10–14 depend on addenda. The game brief is a stub. |
| 02-requirements-engineering (41) | 58 | Strongest content: elicitation, analysis, validation (Wiegers plus inspection), traceability, patterns, and the kernel-backed stimulus-response and SMART-NFR gates. Weaknesses: the waterfall chain is still built on the IEEE 830 layout, `05-feature-decomposition` has step-numbering and priority-scheme conflicts, the structure is a grab-bag (see 02), and 13 skills have no own references. |
| 03-design-documentation (18) | 60 | HLD, LLD and DB are the only skills using typed diagram IR with validate/generate and a generated trace table. The API spec is current. UX is rich (WCAG 2.2, 10 references) but oversized. DB design has no references and a dangling MANDATORY reference. The AI/SaaS architecture specs still use free-hand Mermaid. |
| 04-development-artifacts (6) | 50 | Coding guidelines and technical specification are generic templates. They cite IEEE 730, which is not version-checked. Two skills share prefix 05. Only dev-environment-setup has an example. |
| 05-testing-documentation (10) | 55 | The test plan uses ISO/IEC/IEEE 29119-3 fields, test-design techniques and a pairwise reference. Its example is two test cases. The AI eval and red-team plans are specialised, but no example exists. Security, performance and accessibility test design lack their own skills. |
| 06-deployment-operations (23) | 52 | The deployment guide has rollback, migration choreography and a pipeline reference. 15 of 23 skills are AI/SaaS runbooks or SLO documents, with prefix collisions and an internal overlap. Worked examples are generic. There is no DR/BCP skill. |
| 07-agile-artifacts (5) | 50 | Definition of Done and Definition of Ready are generic checklists with SaaS/AI addenda. Two of five skills have no references. There are no examples. |
| 08-end-user-documentation (9) | 48 | The user manual cites ISO 26514 without an edition and uses screenshot placeholders. 4 of 9 skills have no references. Four skills are SaaS go-to-market packs, not end-user documentation. There is no administrator or training guide. |
| 09-governance-compliance (34) | 53 | The RTM, waiver, sign-off, baseline and evidence-pack skills have real kernel commands behind them. The traceability-matrix SKILL.md does not invoke `python -m engine sync/validate`. 12 of 34 skills have no references. The ten AI-agent control packs map regulations without dated currentness records. The anti-slop pair is doctrine-heavy (22 KB). |

## Sampled skills (17)

| Skill | Score | Refs | Example | Justification |
|---|---:|---:|---|---|
| 01/01-prd-generation | 62 | 6 | No | Nine-step body with SMART objectives, a MoSCoW matrix, KPI baselines and opportunity/product-risk gates. Its manifest lists five section files while Step 9 writes a single `PRD.md`. The standards appendix relies on IEEE 1233-1998. |
| 01/02-business-case | 52 | 2 | No | NPV, ROI and payback in LaTeX, plus go/no-go thresholds. The ROI formula subtracts total costs from "net benefits", which is ambiguous and risks double-counting. There is no discount-rate guidance and no sensitivity procedure, although the description promises sensitivity. IEEE 1058-1998 is cited as the governing standard. The manifest names five files against a nine-section template. |
| 01/04-lean-canvas | 57 | 3 | No | Has a scored decision gate, nine blocks, impact map and hypothesis board. The gate hard-codes "budget < $100K", which conflicts with the engine's premium doctrine and is not currency-neutral. |
| 02/waterfall/05-feature-decomposition | 52 | 0 | No | GWT stubs and IEEE 830 §5.3.2 sub-items. Core Instructions are numbered 1–6 and then 5 again. It asks for both IEEE 830 Essential/Conditional/Optional ranking and MoSCoW priority. It depends on `feature_decomposition.py` without a usage contract. |
| 02/fundamentals/during/07-requirements-validation | 60 | 5 | No | Wiegers attributes, an IEEE 830 criteria check, structured inspection, cross-artifact checks and an SDD boundary companion. It is oversize at 23 KB, and its criteria remain keyed to 830, not the 29148 characteristics. |
| 03/01-high-level-design | 64 | 9 | Fixture | The best sampled skill. Its figures are IR-authored and validated, the trace table is generated, and it cites a complete fixture. It still leans on ByteByteGo and Royce for authority. There is no ISO/IEC/IEEE 42010 viewpoint model, although the gates are mapped to 42010. |
| 03/03-api-specification | 62 | 4 | No | Current on OpenAPI 3.1.2 (with a 3.2 rule), RFC 9457, JSON Schema 2020-12 and RFC 9110. Pagination says "cursor-based or offset-based" and then mandates `page`/`per_page`/`total`. It references two non-existent dev-engine skills. There is no example `openapi.yaml`, and the pipeline does not validate the specification. |
| 03/04-database-design | 50 | 0 | No | ERD by IR, 1NF–3NF, a data dictionary and a migration step. The MANDATORY `skills/mysql-best-practices/` does not exist. There is no PostgreSQL guidance. It imposes dogmatic universals (`DECIMAL(19,4)` for all money, `created_at`/`updated_at` on every table). There is no DDL example. |
| 03/05-ux-specification | 58 | 10 | No | WCAG 2.2 AA, ISO 9241-210:2019, usability protocol and handoff. At 33.7 KB it is 65 % over the size limit. Step 0 depends on an external frontend-design plugin. There is no example specification. |
| 05/02-test-plan | 58 | 1 | Yes (minimal) | Uses the nine normative 29119-3 test-case fields and names design techniques. The example has 2 test cases and does not show boundary or state-transition technique use. |
| 06/01-deployment-guide | 54 | 1 | No | Covers rollback, migration and environment matrix. It cites IEEE 1062, a software-acquisition standard, as the deployment standard, which is a doubtful fit. Its worked example is the generic paragraph. |
| 06/13-ai-agent-slo-doc | 55 | 1 | No | SLIs, multi-burn-rate alerts and freeze rules. It cites NIST AI RMF and ISO/IEC 42001 without dates. It shares prefix 13 with another skill. |
| 08/01-user-manual | 50 | 0 | No | Task-oriented structure with troubleshooting and glossary. ISO 26514 is cited without an edition. It has no accessibility or localisation rules for the manual itself. The screenshot placeholder convention is handled well by the missing-figure guard. |
| 09/01-traceability-matrix | 55 | 0 | No | Forward and backward tables, orphan detection and coverage metrics. It does not call the kernel's `sync`/`validate` commands, which enforce IDs, so the RTM is built by the language model. It cites IEEE 1012-2016 without a currency check. |
| 09/22-ai-agent-hipaa-control-pack | 54 | 1 | No | Walks §164.308/310/312/316, minimum necessary, BAA duties and breach notification. There is no dated currentness record for the Security Rule text, and the example is a single sentence. |
| 07/02-definition-of-done | 52 | 3 | No | Tiered DoD with SaaS/AI addenda. Generic, and the example is one sentence. |
| 04/02-coding-guidelines | 50 | 2 | No | A generic naming, structure and error-handling template. It defers to language-specific dev-engine skills without naming them. IEEE 730 is not version-checked. |

Mean of the sampled skills: 55.6.
