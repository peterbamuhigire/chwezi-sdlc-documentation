# House-style declaration kaizen record, 2026-11-07 (SD-KZ-06)

## Trigger

On 2026-11-07 Peter Bamuhigire asked for the interface style of the Maduuka Android app to become the house style for all his apps. The audit and the canonical standard live in the `chwezi-design-engine` engine (`docs/kaizen/2026-11-app-house-style/README.md`, kept patterns K1 to K19, rejected R1 to R11). That record names one gap for this engine: the UX specification skill did not ask a specification to declare its house style.

## Baseline (measured on `main` at `a097f02`, 2026-11-07)

| Measure | Value |
|---|---|
| Matches for "house style" in `03-design-documentation/05-ux-specification/` | 0 |
| `05-ux-specification/SKILL.md` | 498 lines (limit 500) |
| Active skills | 159 and 1 template (unchanged by this change) |

## Change (standardise)

| Surface | Change | Acceptance condition |
|---|---|---|
| `05-ux-specification/references/house-style-declaration.md` (new, 166 lines) | Task procedure; twelve requirements HS-01 to HS-12 as "shall" statements with acceptance criteria and evidence; WCAG 2.2 basis (1.4.3, 1.4.11, 2.5.8, 2.3.3); fill-in template; worked example for a fictional water-billing app; review checklist | Each HS row has a deterministic oracle and an evidence item; unmeasured checks are `NOT_ASSESSED` |
| `05-ux-specification/SKILL.md` | One References bullet; one sentence added to the Step 4.4 "See" line | 499 lines, under the 500-line limit |
| `05-ux-specification/README.md` | One Resources bullet | The reference is listed with the skill |
| `docs/kaizen/2026-11-house-style-declaration/standards-source-register.md` (new) | Four WCAG 2.2 claim records, accessed 2026-11-07, review by 2027-05-07 | `validate_source_register.py` passes |

Presentation values are not restated. The reference points to the design-engine skills `chwezi-business-app-house-style` and `money-figures-and-statement-display` by engine identifier and relative path. No skill was added and no description changed, so routing fixtures were not changed.

## Check

Command results are in the commit message of this change and in the report to the owner.

## Not assessed

- Whether a specification that uses the declaration produces a more consistent app. No project has used it yet.
- Platform touch-target guidance (48 dp, 44 pt) was not re-read against a dated platform source.
- `money-figures-and-statement-display` was being written in parallel in the design engine and did not exist in the checkout when this record was written; the reference names its intended path.
- The worked example was applied by its author only; no independent review.

## Rollback

Delete the new reference and the source register folder, revert the two lines in `SKILL.md` and the one in `README.md` of the skill, and remove the CHANGELOG and root README entries.
