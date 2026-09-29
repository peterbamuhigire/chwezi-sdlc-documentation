# SRS engine: M10-14 measured re-audit (29 September 2026)

Engine: `srs-skills` at HEAD `fa85fba`, 159 active skills in nine numbered phase groups.
Auditor: independent (this auditor did not carry out any my-10-kaizen phase).
Method: `chwezi-dev-engine/skills/sdlc-meta/skill-engine-audit` with its scoring rubric, including
the Engine Eval Readiness (measured) section.

## Headline numbers

| Number | Value | Basis |
|---|---:|---|
| Raw overall | **54.6 / 100** (54.63) | Judged dimensions; discovery and routing judged at 60 |
| Measured-constrained overall | **54.6 / 100** (54.58) | Routing replaced by Engine Eval Readiness 58.5 |
| Published overall | **54.6 / 100** | `min(54.58, 65)`; the 65 cap does not bind |
| Engine Eval Readiness | **58.5 / 100** | T1 30.00 + T2 28.54 + T3 0 (NOT_ASSESSED); ceiling 70 while T3 is unexecuted |

Weighting: output readiness 30 %, skill depth and worked examples 25 %, standards currency 15 %,
taxonomy 10 %, doctrine 10 %, hygiene 10 % (hygiene = mean of redundancy, discovery/routing,
safety).

## Verdict

The SRS engine has a real validation kernel (432 passing tests at 96.86 % coverage), a typed
diagram IR, and a DOCX build that renders figures before Pandoc and fails closed. That machinery is
stronger than the skill layer it serves. Only 4 of 159 skills ship an input-and-expected-output
example. 81 skills carry a "Worked Example" section that is a single generic paragraph, and 34 of
those paragraphs are identical. The standards clause registry still maps the Phase 02 gates to IEEE
830-1998, which the engine's own router describes as superseded. Three cross-engine skill
references, one of them marked MANDATORY, point at skills that do not exist, and no validator
detects them. Remote CI has been red since at least 20 September because a skill links to
absolute paths that exist only on this machine. Routing is measured at 58.5, held down by zero
fixture coverage (0/159) and an unexecuted Tier 3. The published score is 54.6. The earlier
figures of 88.8 raw and 65 published (2026-09-08) came from a lenient equal-weight self-review and
cannot be compared directly with this one.

## Files

| File | Contents |
|---|---|
| [`00-executive-summary.md`](00-executive-summary.md) | Verdict, headline findings, strengths, path to the bar |
| [`01-methodology-and-rubric.md`](01-methodology-and-rubric.md) | Method, commands, rubric, weighting, limitations, independence |
| [`02-coverage-and-taxonomy.md`](02-coverage-and-taxonomy.md) | Taxonomy score and named deficiencies |
| [`03-existing-groups-audit.md`](03-existing-groups-audit.md) | Per-group scores and 17 sampled per-skill scores |
| [`05-per-output-type-readiness.md`](05-per-output-type-readiness.md) | 16 output types scored and ranked |
| [`09-master-scorecard.md`](09-master-scorecard.md) | All 11 dimensions, groups, output types, arithmetic |
| [`10-roadmap-to-world-class.md`](10-roadmap-to-world-class.md) | P0/P1/P2 moves with named files and targets |
| [`11-measured-evidence.md`](11-measured-evidence.md) | Commands, exit codes, output lines, Readiness arithmetic, NOT_ASSESSED list |

Not re-run in the M10-14 measured re-audit:

- `04-gap-analysis-new-skills.md`: not re-run. The missing-skill list is summarised in `02`.
- `06-standards-benchmark.md`: not re-run. No fresh external research was done, and currency is judged from the engine's own records.
- `07-hardening-existing-skills.md`: not re-run. Hardening moves are in `10`.
- `08-reading-list.md`: not re-run in the M10-14 measured re-audit.
