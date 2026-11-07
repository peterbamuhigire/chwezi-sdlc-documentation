# House-Style Declaration Section

Parent skill: [`05-ux-specification`](../SKILL.md).

## Purpose and scope

A product that follows the Chwezi business-app house style shall declare it in its UX
specification (Section 3, Design System) or, where no separate UX specification exists, in the
SRS user-interface section (3.1.1). The declaration turns the style into verifiable requirements
so a reviewer can tell from evidence, not opinion, whether a build conforms.

This reference owns the structure and the acceptance conditions. Presentation decisions (role
values, component shapes, motion curves, icon artwork) belong to the `chwezi-design-engine`
engine; resolve it through the engine-routing table and read:

- `chwezi-design-engine`: `skills/09-design-systems-tokens-and-theming/chwezi-business-app-house-style/SKILL.md`
  (colour roles, type pair, components, motion, guardrail tests).
- `chwezi-design-engine`: `skills/12-data-viz-and-dashboards/money-figures-and-statement-display/SKILL.md`
  (compact amounts, hero figures, statement and summary layouts).
- `chwezi-design-engine`: `docs/kaizen/2026-11-app-house-style/README.md` (the audit record:
  kept patterns K1 to K19, rejected patterns R1 to R11).

Do not restate those skills here or in the specification. Cite them and record the values the
product chose.

## When to load

- The owner states that the product follows the Chwezi house style, or the product is one of the
  owner's business apps (POS, ERP, hotel, pharmacy, school, SaaS administration; Android or web).
- An existing app is being brought onto the house style and its specification is being revised.

Do not load it for a product with its own brand system, or for a marketing website. Use the
design-system foundation in Step 4 of the parent skill instead.

## Task procedure

1. Confirm the owner's decision to adopt the house style and record who made it and when.
   Missing decision: `[CONTEXT-GAP: house-style adoption]`; stop.
2. Read the two design-engine skills above at their current revision. Record the revision date.
3. Obtain the brand primary from the owner or brand file. Measure its contrast with white and on
   the tinted ground before writing HS-01. If either is under 4.5:1, the design engine darkens the
   primary in the same hue; record both values.
4. Fill the template table below, one row per requirement HS-01 to HS-12. A row that does not
   apply (for example, a product with no money figures for HS-05) is marked `N/A` with the reason;
   it is never deleted silently.
5. Write each requirement as a "shall" statement with its acceptance criterion and the evidence
   that proves it. Every acceptance criterion is a deterministic pass/fail oracle.
6. Attach the evidence plan (HS-12). Any check not measured at sign-off is `NOT_ASSESSED`, and a
   `NOT_ASSESSED` row blocks a "conforms to house style" claim.
7. Trace each HS row to the screens it covers in the Traceability Matrix (Section 8).

## Required requirements

Identifiers are local to the declaration; keep them or map them to the project's own scheme.

| ID | Requirement ("shall" statement) | Acceptance criterion | Evidence |
|---|---|---|---|
| **HS-01** | The brand primary shall have a contrast ratio of at least 4.5:1 with white text and with text on the tinted ground. | Both ratios recomputed from the token values are >= 4.5:1. | Contrast table (HS-12) with hex values and ratios. |
| **HS-02** | Pages shall use a pale, brand-tinted ground with near-white cards (large radius, hairline border, no more than one card level). | No screen in the screenshot set shows a card inside a card or a card without the border token. | Screenshot set; component inventory. |
| **HS-03** | Each screen shall carry at most one warm next-step accent, and a screen with no single next step shall carry none. | Guardrail test "one accent per screen part" passes; reviewer count per screen <= 1. | Test report; screenshot review log. |
| **HS-04** | Interface text shall use the declared body face and figure face; all amounts, including amounts inside sentences, shall use tabular figures; neither face shall be on the design engine's banned-font list. | Font files in the build match the declared pair; banned-font check passes; a column of 5 amounts aligns on the decimal point. | Typeface record (name, licence, reason); banned-font check result; screenshot. |
| **HS-05** | Tiles, rows and summaries shall show amounts in compact form (K, M, B, two decimals); documents, closing balances and input fields shall show the full amount; assistive technology shall read the full amount; a non-zero value shall never display as 0% (use "less than 1%"). | Unit tests on the formatter cover each case; screen-reader label of a compact figure equals the full amount; a fixture of 0.4% displays "less than 1%". | Formatter test report; screen-reader transcript or semantics test. |
| **HS-06** | All dates on screen shall use one declared format (long form and one short form). | A search of the interface strings and the screenshot set finds no second format. | Format declaration; string search result. |
| **HS-07** | No raw identifier (database id, run id, wire status code, UUID) shall appear on screen. | The raw-identifier guardrail count is 0, or at or below its recorded baseline for an existing app. | Guardrail test report. |
| **HS-08** | Reveal, count-up and grow-in motion shall play at most once per screen visit, only on summary screens, and shall not play when the system requests reduced motion. | With reduced motion on, a recorded visit shows no motion; a second visit in the same session shows none. | Reduced-motion test; screen recording. |
| **HS-09** | Each illustrated menu icon shall have a recorded source and licence before release. | The icon register has a source and licence for 100% of shipped illustrated icons. | Icon register. |
| **HS-10** | Interactive targets shall be at least 24 by 24 CSS px (web) and meet the platform target (48 dp Android, 44 pt iOS) on mobile; boundaries of controls and meaningful graphics shall reach 3:1 against adjacent colours. | Rendered measurement of targets; non-text contrast ratios >= 3:1. | Measurement log; contrast table. |
| **HS-11** | The guardrail tests (raw colour outside the theme = 0; one accent per screen part; spacing, shape and raw-identifier ratchets that only go down) shall run as release gates. | CI fails a build that adds a raw colour, a second accent or raises a ratchet; the baseline file shows no increase between releases. | CI configuration; one recorded failing control run. |
| **HS-12** | The declaration shall carry evidence: screenshots at default and 200% text, light and dark theme, phone and tablet; and a contrast table of every text and control pair. | Every cell of the evidence matrix holds a file or `NOT_ASSESSED`. | Evidence matrix. |

Notes on scope:

- HS-03 counts the warm accent only. Filled primary, tonal and outlined buttons are not limited.
- HS-05 applies only where the product shows money or other large figures; otherwise `N/A`.
- HS-08 treats operational screens (selling, cashier, kitchen, dispensing) as state transitions
  only; they get no reveal or count-up at all.
- HS-11 for a new app starts every ratchet at 0. For an existing app, measure first and record the
  baseline with its date.

## Standards basis

The thresholds above rely on these WCAG 2.2 success criteria. Source: W3C, *Web Content
Accessibility Guidelines (WCAG) 2.2*, W3C Recommendation 12 December 2024,
<https://www.w3.org/TR/WCAG22/>, and for 2.5.8 the W3C Understanding page
<https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html>. Accessed and verified on
2026-11-07; record in `docs/kaizen/2026-11-house-style-declaration/standards-source-register.md`.

| Criterion | Level | Threshold used | Used by |
|---|---|---|---|
| 1.4.3 Contrast (Minimum) | AA | Text >= 4.5:1; large text >= 3:1 | HS-01, HS-12 |
| 1.4.11 Non-text Contrast | AA | UI components and graphics >= 3:1 against adjacent colours | HS-10, HS-12 |
| 2.5.8 Target Size (Minimum) | AA | Pointer targets >= 24 by 24 CSS px, or the spacing exception | HS-10 |
| 2.3.3 Animation from Interactions | AAA | Motion triggered by interaction can be disabled unless essential | HS-08 |

2.3.3 is Level AAA, so HS-08 exceeds an AA conformance target by the owner's choice; state that in
the specification rather than citing AA for it. The 48 dp and 44 pt platform targets are platform
guidance, not WCAG, and are `NOT_ASSESSED` in this reference until a dated platform source is
recorded for them. Whether WCAG applies to a project by law is a separate question and is not
established here.

## Fill-in template

Copy into the UX specification, Section 3, as subsection "3.x House-Style Declaration".

```markdown
### 3.x House-Style Declaration

This product follows the Chwezi business-app house style, adopted by <owner> on <date>.
Design-engine revision read: <date>. Money-figure rules apply: <yes / no, reason>.

| Item | Declared value | Measured result | Evidence file | Status |
|---|---|---|---|---|
| HS-01 Brand primary | <hex> | <ratio> on white; <ratio> on ground <hex> | <path> | PASS / FAIL / NOT_ASSESSED |
| HS-02 Ground and card | ground <hex>; card <hex>; radius <token> | <finding> | <path> | |
| HS-03 Warm accent | <hex> with ink <hex>; screens: <list of next steps> | <max per screen> | <path> | |
| HS-04 Type pair | body <face, licence>; figures <face, licence>; tabular <yes> | banned-font check <result> | <path> | |
| HS-05 Compact amounts | ladder K/M/B, 2 decimals; full-amount surfaces: <list> | formatter tests <n passed> | <path> | |
| HS-06 Date format | long <example>; short <example> | second format found: <yes/no> | <path> | |
| HS-07 Raw identifiers | baseline <n> on <date> | current <n> | <path> | |
| HS-08 Motion | summary screens: <list> | reduced-motion run <result> | <path> | |
| HS-09 Illustrated icons | register: <path> | <n of n> with source and licence | <path> | |
| HS-10 Targets and non-text contrast | <platform targets> | smallest <size>; lowest <ratio> | <path> | |
| HS-11 Guardrail gates | tests: <names> | failing control run on <date> | <path> | |
| HS-12 Evidence matrix | default and 200% text x light and dark x phone and tablet | <cells filled / 8> | <path> | |
```

## Worked example (fictional)

Kisima Water Billing is a fictional web and Android app for a small water utility: meter readings,
bills, payments and customer statements. It is not a Maduuka product, and the values are for
illustration only.

| Item | Declared value | Measured result | Status |
|---|---|---|---|
| HS-01 | Owner's green `#2E8B57` measured 4.25:1 on white, so it was darkened to `#23704A` | 6.02:1 on white; 5.43:1 on ground `#EEF5F0` | PASS |
| HS-02 | Ground `#EEF5F0`; card near-white with hairline border | No nested cards in 24 screenshots | PASS |
| HS-03 | Amber `#F8B020` with ink `#1B1B1B` (9.20:1); next steps: Record reading, Take payment, Issue bill | Max 1 per screen | PASS |
| HS-04 | Pair taken from the design engine's role table, with licence records | Banned-font check passed | PASS |
| HS-05 | Tiles and statement rows compact; bill document, closing balance and payment input full | 18 formatter tests passed; "less than 1%" fixture passed | PASS |
| HS-06 | "6 Nov 2026"; short "Fri 6 Nov" | No second format | PASS |
| HS-07 | New app, baseline 0 | 0 | PASS |
| HS-08 | Monthly summary only | Reduced-motion run on Android passed; web not run | NOT_ASSESSED (web) |
| HS-09 | 9 hub icons | 9 of 9 recorded | PASS |
| HS-10 | 48 dp Android, 24 CSS px web | Smallest 48 dp; lowest non-text ratio 3.4:1 | PASS |
| HS-11 | Raw colour, one accent, spacing, shape, raw-identifier tests | A deliberate second accent failed CI on the control run | PASS |
| HS-12 | 8 cells | 6 of 8; tablet dark at 200% not captured | NOT_ASSESSED |

Result: the specification may not claim conformance yet, because HS-08 (web) and HS-12 are
`NOT_ASSESSED`. The two gaps go to the release owner with a due date.

A sample requirement as it would appear in the SRS:

> **FR-UI-014:** The system shall display the customer's closing balance on the statement screen
> as the full amount with two decimals (for example "1,284,500.00"), and each statement row amount
> in compact form (for example "1.28M"), with the full amount as its accessibility label.
> Verification: formatter unit tests and a screen-reader semantics test on the statement screen.

## Review checklist

- [ ] The adoption decision names the owner and the date.
- [ ] HS-01 to HS-12 each have a value, a measured result, an evidence file and a status, or `N/A`
      with a reason.
- [ ] The contrast table is recomputed from the token values, not copied from another app.
- [ ] No presentation value is invented here; each comes from the design-engine skills.
- [ ] `NOT_ASSESSED` rows are listed in the gap register with an owner and a due date.
- [ ] Each HS row traces to the screens it covers.
