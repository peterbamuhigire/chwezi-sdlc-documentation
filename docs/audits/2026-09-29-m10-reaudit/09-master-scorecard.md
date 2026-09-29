# Master scorecard

## A. Engine dimensions (the 11 in `audit-dimensions.md`)

| # | Dimension | Label | Score | Evidence (details in 02, 03, 05, 11) |
|---:|---|---|---:|---|
| 1 | Doctrine and philosophy | judged | 64 | Strong points in `AGENTS.md`: grounding without invention, stimulus-response, the IEEE 1012 V&V SOP with fail tags, the Human Review Gate, the anti-slop gate and the currentness gate. Against it: a 500-line router that mixes the Codex setup, a table of dev-engine categories, a duplicated `dpia-generator` bullet, legacy "Skill 05/Skill 08" numbering, and "eight-phase skill flow" against nine phase roots. The router asks for requirements to be judged against 29148 while the SRS layout stays on 830. |
| 2 | Taxonomy and structure | judged | 55 | 7 duplicate prefixes. Group 02 uses four nesting schemes. About 35 AI skills are scattered across all groups. `plan-canvas` is filed as governance. There is one within-engine collision at 0.756. Seven output types are missing (see 02). |
| 3 | Skill depth and rigour | judged | 56 | Core skills have numbered steps, templates and checklists. Against that: the generic contract workflow appears in 28 skills, internal contradictions are present (see 03), 3 cross-engine references dangle, 43/159 skills have no references, and the game skills are stubs. |
| 4 | Worked examples and applied proof | judged (T3 NOT_ASSESSED) | 42 | 4/159 skills have real examples, and 81 "Worked Example" sections are boilerplate. Engine-level proof is strong: 432 tests pass at 96.86 % coverage, with golden reports and project fixtures. No Tier-3 grading exists, so it adds nothing. |
| 5 | Standards currency | judged (from the engine's own currentness records; no fresh external research) | 55 | Current: OpenAPI 3.1.2, RFC 9457, JSON Schema 2020-12, WCAG 2.2, ISO/IEC 25010:2023, ISO 9241-210:2019, 29119-3. Against: `standards-clause-registry.md` maps Phase 02 to IEEE 830-1998, which `AGENTS.md` calls superseded. 18 skills cite 830. 42010:2011 is used in the registry, IEEE 1058-1998 in the business case, and ISO 26514 has no edition. The registry has no access or review dates. The auditor believes the 42010 and 1058 editions have been superseded; to be verified through the Digital Research gate. |
| 6 | Coverage / output-type readiness | judged | 55 | Mean of 16 output types, 55.4 (see 05). |
| 7 | Accessibility and inclusivity | judged | 52 | For: UX uses WCAG 2.2 AA; IR makes `alt_text` mandatory, and `figure-alt.lua` carries it into the DOCX. Against: no ACR/accessibility test-plan skill, no DOCX accessibility lint, and no accessibility or plain-language rules for user manuals beyond the Human-English reference. |
| 8 | Production / handoff / render fidelity | judged plus measured scan | 60 | For: render-first build that fails closed on Mermaid or a missing figure, SHA-256 figure manifest, and a scan of 691 DOCX with 0 Mermaid. Against: reference DOCX in Word-default Calibri with no recorded type decision, no structure lint, no PDF route, and the OpenAPI output is not validated. Rendered output was not visually reviewed. |
| 9 | Redundancy and hygiene | judged | 50 | Remote CI has been red since at least 20 Sep (absolute machine path). There are dangling references, duplicate prefixes, 6 oversize skills, and boilerplate example sections. Superseded audit sets are kept under `docs/evaluation/2026-04-12` and `docs/implementation/review-05-Apr-2026` without a "historical" banner. |
| 10 | Discovery and routing | **measured** | **58.5** | Engine Eval Readiness (see 11). The raw computation uses a judged 60. |
| 11 | Safety and integrity | judged | 62 | For: source-ingestion guardrail with 0 findings, waiver-schema negative tests, capability and permission boundaries in every skill contract, a loopback guard for plan-canvas, and client workspaces gitignored. Against: machine paths leak into a public skill, the skill-safety gate is not recorded per skill, and compliance packs have no dated legal sources. |

No dimension reaches 70, so no extraordinary justification is needed.

## B. Groups

| Group | Score |
|---|---:|
| 03-design-documentation | 60 |
| 02-requirements-engineering | 58 |
| 01-strategic-vision | 56 |
| 05-testing-documentation | 55 |
| 09-governance-compliance | 53 |
| 06-deployment-operations | 52 |
| 04-development-artifacts | 50 |
| 07-agile-artifacts | 50 |
| 08-end-user-documentation | 48 |

## C. Output types

Design documents 62; PRD 60; API specification 60; traceability matrix 60; SRS 58; test
plans/design 58; rendered DOCX 58; UX specification 57; vision/lean canvas 55; deployment and
operations 55; database design 52; governance packs 52; agile artefacts 52; business case 50;
user documentation 50; as-built recovery 48. Mean 55.4.

## D. Overall arithmetic

Weighting: output 30 %, skill depth and worked examples 25 %, standards 15 %, taxonomy 10 %,
doctrine 10 %, hygiene 10 %.

- Skill depth and worked examples = (56 + 42) ÷ 2 = **49**

| Bucket | Weight | Raw | Measured-constrained |
|---|---:|---:|---:|
| Output readiness | 0.30 × 55 | 16.50 | 16.50 |
| Skill depth and worked examples | 0.25 × 49 | 12.25 | 12.25 |
| Standards currency | 0.15 × 55 | 8.25 | 8.25 |
| Taxonomy | 0.10 × 55 | 5.50 | 5.50 |
| Doctrine | 0.10 × 64 | 6.40 | 6.40 |
| Hygiene | 0.10 × H | 5.73 (H = (50 + 60 + 62) ÷ 3 = 57.33) | 5.68 (H = (50 + 58.5 + 62) ÷ 3 = 56.83) |
| **Overall** | | **54.63** | **54.58** |

- **Raw: 54.6 / 100**
- **Measured-constrained: 54.6 / 100**
- **Published: min(54.58, 65) = 54.6 / 100.** The craft-standard acceptance evidence is absent, but
  the cap does not bind.
- **Engine Eval Readiness: 58.5 / 100.** The ceiling is 70 while T3 is unexecuted.

## E. Movement against prior audits

| Audit | Method | Raw | Published |
|---|---|---:|---:|
| 2026-09-06 Kaizen | Narrative; raw and published NOT ASSESSED; cap 65 noted | n/a | n/a (cap 65) |
| 2026-09-08 comprehensive Kaizen | Equal-weight self-review over 10 dimensions, no measured routing | 88.8 | 65 |
| **2026-09-29 M10-14 (this audit)** | Independent, strict rubric, measured routing | **54.6** | **54.6** |

The fall comes mainly from method: strict bands, weighting and an independent auditor. It is not a
regression in the engine. Measured movement since 8 September:

- Active skills rose from 157 to 159.
- Routing fixtures rose from 52 to 55 positives, with 16 owned negatives added.
- Tests rose from 255 to 432 passing, and coverage from 95.93 % to 96.86 %.
- The render pipeline gained the missing-figure guard.
- Remote CI went from unrecorded to red.

The 8 September scorecard gave taxonomy/routing 95 and applied proof 95. This audit does not
support those figures: routing is measured at 58.5, and skill-level worked examples cover 4/159.
