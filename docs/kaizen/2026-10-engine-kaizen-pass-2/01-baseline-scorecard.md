# Frozen baseline scorecard — pass 2

**Frozen:** 2026-10-31, committed before any engine change. **Checkout:** `kaizen/2026-10-pass2` at the same tree as `main` `91b987d`. **Method:** a fresh reviewer judgement on the ten Portfolio Kaizen Standard dimensions, scored against the evidence named below, and the same unweighted arithmetic mean the 29 October cycle used so the two records compare. Ratings are judgements, not measurements of customer outcome. The 29 October final column is shown for comparison only: this pass looked at new surfaces (tracked local settings, gate false negatives, template currency), so a lower fresh rating on a dimension means the earlier cycle did not inspect that surface, not that earlier work regressed. The indicative catalogue and routing numbers equal the 29 October results exactly.

| Dimension | 29 Oct final | Fresh baseline | Evidence and one-line deficiency |
|---|---:|---:|---|
| Doctrine | 62 | 61 | Router states that no engine location is assumed, yet carries 18 drive-letter WAMP path lines (`AGENTS.md`); UX doctrine retires WCAG 2.1 while engine templates keep it. |
| Taxonomy and routing | 58.8 | 58.8 | Indicative precision@1 57/65 (87.7%); 4 of 159 skills meet three positives and two owned negatives; the contradictory-brief task ranks `04-requirements-analysis` tenth; the generic SRS phrase ranks the game SRS skill first. |
| Skill depth | 56 | 56 | 5 skill files above the report-only byte threshold; 12 groups of skills (44 skills) share one identical worked-example paragraph; strong contracts do not close domain workflow gaps. |
| Applied proof | 43 | 43 | 4 of 159 skills have an `examples/` folder; 81 worked-example headings, 44 of them sharing an identical paragraph. |
| Standards currency | 38 | 38 | Issuer records exist for the current editions, but 57 files cite IEEE 830, 4 cite 42010:2011 and 6 cite 29119-3:2013 outside `docs/`; no validator checks source-record review dates; 7 engine-level WCAG 2.1 lines. |
| Output readiness | 59 | 56 | Phase 02 passes metric-less NFRs and flags a valid hour threshold; test cases cannot trace an NFR without a HIGH finding; Phase 09 ignores NFRs; duplicate requirement IDs are undetected. |
| Accessibility and inclusion | 52 | 50 | Engine-level templates prescribe WCAG 2.1 AA (5 lines) against the engine's own WCAG 2.2 doctrine; native Word accessibility and font fidelity not assessed. |
| Production and handoff | 53 | 50 | The `.docx` build cannot run here (no Pandoc, no Mermaid CLI); the catalogue validators fail with a bare traceback when a pinned package is absent; CI omits three October validators. |
| Hygiene | 54 | 48 | 18 live files with machine or personal paths (43 lines); a tracked local settings file; 7 flat-layout dev-engine references that do not resolve; no validator for either class. |
| Safety and integrity | 64 | 61 | The tracked local settings file ships an unrestricted `Bash(bash:*)` allowlist and personal data to every cloner (D-01); declared-ambiguity blocking exists but an absent register passes. |

**Raw mean:** (61 + 58.8 + 56 + 43 + 38 + 56 + 50 + 50 + 48 + 61) ÷ 10 = 521.8 ÷ 10 = **52.18/100**.
**Portfolio cap:** `min(52.18, 65) = 52.18/100`. The cap does not bind. **User initial cap 45:** `min(52.18, 45) = 45/100` (a reporting ceiling, not a rating change).
29 October final for comparison: raw 53.98, capped 53.98.

## Measured inputs

All counts come from an independent script that reads `git ls-files` and the fixture JSON; it does not call the repository's validators.

| Measure | Value |
|---|---|
| Active skills / templates | 159 / 1 (indicative catalogue validator under a PyYAML stand-in; registered run `NOT_ASSESSED`) |
| Routing precision@1 / top three | 57/65 = 87.7% / 65/65 (indicative) |
| Owned negatives | 24: 21 pass, 0 fail, 3 cross-engine `NOT_ASSESSED` (indicative) |
| Fixture prompts | 89 |
| Skills with at least three positives and two owned negatives | **4 of 159** (`03-api-specification`, `04-database-design`, `04-requirements-analysis`, `09-traceability-engineering`); nearest: `01-high-level-design` (2 positives, 2 negatives), `01-initialize-srs` (1, 2), `02-business-case` (1, 3) |
| Worked-example depth | 81 headings; 12 groups of identical paragraphs covering 44 skills; 4 `examples/` directories |
| Machine-specific or personal path lines outside `docs/` | 43 lines in 18 files (`.claude/settings.local.json` 5, `AGENTS.md` 18, `scripts/build-doc.sh` 2, `09-governance-compliance/plan-canvas/SKILL.md` 3, `hooks/plan-canvas-pending.js` 2, 12 other files 1 each). History documents under `docs/` outside the evidence folders: 66 lines in 14 files (historical record, not edited) |
| Tracked local settings files | 1 (`.claude/settings.local.json`) |
| Flat-layout skill references outside `docs/` | 9 matches: 7 dev-engine names that do not resolve (API specification 2 lines, domain checklists 5 names) and 2 upstream citations of an external `skills/plan-canvas/SKILL.md` that are not engine links |
| Stale standard citations outside `docs/` | IEEE 830: 57 files, 163 lines; 42010:2011: 4 files, 13 lines; 29119-3:2013: 6 files, 11 lines; 25010:2011: 1; 29148:2011: 1; 26514:2008: 0 |
| Engine-level WCAG 2.1 lines | 7 (5 prescribe 2.1; 1 is the doctrine sentence retiring it; 1 is a skill overview row). Domain packs: 16 lines, jurisdiction-bound United States baselines left for owner decision |
| Expired source records | 0 of 14 in the 29 October register as of 2026-10-31; earliest review date `2026-11-05` (Codex budget claim). No validator enforces review dates. |
| Dangling cross-engine references | 7 flat-layout names (above); design and accounting engine paths cited in skills resolve (checked for the four named paths) |
| Broken relative links | Not independently counted this pass; the October link checks are unchanged. `NOT_ASSESSED` |
| Phase gates | Phase 01 gate passes on the task 1 project; Phase 02 checks: 1 finding on 4 NFRs, of which 1 is a false positive and 2 are false negatives; Phases 03 to 09 not run on the task projects (project is SRS-only) |
| DOCX pipeline | `NOT_ASSESSED`: Pandoc and Mermaid CLI absent |
| Full test suite | `NOT_ASSESSED` (pytest absent). Indicative runner: 215 pass, 8 fail, 1 skip, 26 error, all failures traced to absent packages |

## Currentness and release blockers

- **Blocker, fixed in this cycle if the backlog item holds:** D-01, a public repository tracking a local permission allowlist with personal and client names.
- Standards clause mappings (IEEE 830, 42010:2011, 29119-3:2013) stay open: remapping needs authoritative clause text and owner approval, and no canonical doctrine changes in this cycle.
- Uganda Data Protection and Privacy Act 2019 and Regulations 2021 currency beyond the 2023 consolidation remains `NOT_ASSESSED` until re-checked in Step 5.
- Live routing, native Word accessibility, real-font rendering, Phase 09 registry checks and the pytest suite are `NOT_ASSESSED` on this host.
