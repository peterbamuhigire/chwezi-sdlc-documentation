# Per-output-type readiness

All scores are judged against the top 0.1 % bar. Each output type's scores draw on the skill(s)
that produce it, the kernel gates and checks behind it, and whether it has applied proof.

## Ranked table

| Rank | Output type | Producing skills | Score | Two or three biggest gaps | Lift moves |
|---:|---|---|---:|---|---|
| 1 | Design documents incl. diagrams (HLD/LLD) | 03/01, 03/02, 03/10, 03/11, 03/14 | 62 | Only 3 skills author typed IR. The AI/SaaS architecture specs still hand-write Mermaid. There is no 42010 viewpoint/view model, although the gates cite 42010. | Move 03/10, 03/11 and 03/14 to IR. Add a viewpoint reference. Link the healthcare fixture as the worked example. |
| 2 | PRD | 01/01 | 60 | No worked PRD. Single-file and section-manifest outputs conflict. It relies on the IEEE 1233-1998 standards appendix. | Add `examples/representative/` with a small PRD and its trace. Reconcile the manifest. |
| 2 | API specification | 03/03 | 60 | No example `openapi.yaml`. The pipeline does not validate the specification. There is a pagination contradiction and two dangling dev-engine references. | Ship an example specification and add an OpenAPI lint step to the build or kernel. Fix the references. |
| 2 | Traceability matrix | 09/01, 02/fundamentals/after/09, kernel `sync`/`validate` | 60 | The skill does not call the kernel. The RTM is built by the model while the identifier registry exists. There is no example RTM. | Make `python -m engine sync` and `validate` mandatory steps. Generate the RTM from `_registry/`. |
| 5 | SRS (IEEE 29148 style) | 02/waterfall/01–09, 02/fundamentals/during/07 | 58 | The layout and kernel mapping are still IEEE 830-1998. The 29148 information items are not the template. `05-feature-decomposition` is inconsistent. | Remap `phase02.*` checks to 29148:2018 clauses. Add a 29148 information-item template beside the 830 layout. |
| 5 | Test plans and test design | 05/01, 05/02, 05/04–07 | 58 | The example covers 2 cases. There is no dedicated performance, security or accessibility test design. Tier-3 evidence is absent. | Expand the example to show EP/BVA, state-transition and pairwise technique use. Add a non-functional test-design skill. |
| 5 | Rendered DOCX deliverable | `scripts/build-doc.sh`, `render_diagrams.py`, `check_docx_diagrams.py` | 58 | The reference DOCX uses Calibri/Calibri Light (Word defaults) with no recorded typographic decision from the design engine. There is no automated check of headings, tables, page numbers or document control, and no PDF route. No rendered DOCX was visually reviewed in this audit. | Add a design-engine typeface decision to `create-reference-docx.py`. Add a DOCX structure lint (heading order, table header rows, alt text coverage). |
| 8 | UX specification | 03/05, 03/09 | 57 | 33.7 KB oversize. No example specification. Step 0 depends on an external plugin. | Split into references. Add a one-journey worked specification. |
| 9 | Vision / lean canvas | 01/03, 01/04, 01/05 | 55 | No example canvas. The decision gate hard-codes a USD budget. The vision statement is template-level. | Add an example canvas with a hypothesis board. Parameterise the gate. |
| 9 | Deployment and operations documentation | 06/01–22 | 55 | 15 of 23 skills are AI/SaaS variants with prefix collisions. There is no DR/BCP skill. Worked examples are generic. | Consolidate incident skills. Add a DR/BCP skill with RTO/RPO test oracles. |
| 11 | Database design | 03/04, 02/fundamentals/during/05 | 52 | Dangling MANDATORY reference. No references folder. No PostgreSQL guidance. Dogmatic universals. No DDL example. | Point to `backend-databases/mysql-engineering`. Add platform references and an example schema with its data dictionary. |
| 11 | Governance and compliance packs | 09/03, 09/11–27 | 52 | Regulations are mapped without dated currentness records. 12 skills have no references. The worked examples are single sentences. | Add dated source rows (Digital Research gate) to each control pack. Add one worked control-mapping example. |
| 11 | Agile artefacts | 02/agile/01–04, 07/01–05 | 52 | Generic checklists and no examples. The user-story example is the only exception, as a reference. | Add a worked story map with acceptance criteria and DoR/DoD. |
| 14 | Business case | 01/02 | 50 | Ambiguous ROI formula. No discount-rate or sensitivity procedure. IEEE 1058-1998 cited. No worked financial model. The finance engine is reached only through the AI addendum. | Rewrite the formulae (ROI = (benefits − costs) / costs). Add a sensitivity/tornado step and finance-engine routing for every case. Add a worked three-option example. |
| 14 | User documentation | 08/01–04, 08/09 | 50 | ISO 26514 has no edition. There is no administrator or training guide. 4 of 9 skills have no references. There are no accessibility rules for manuals. | Add an admin-guide skill and an example user-manual chapter. Date the standard. |
| 16 | As-built recovery | 03/01 `references/as-built-recovery.md`, kernel `as_built` fixture | 48 | No skill of its own. Discoverable only through the HLD. | Promote it to a skill with an example recovered-architecture pack. |

**Mean of the 16 output types: 55.4, rounded to 55.** This is the output-readiness dimension.

No output type reaches 70. The highest (design documents, 62) is held back by partial IR adoption
and the missing viewpoint model.
