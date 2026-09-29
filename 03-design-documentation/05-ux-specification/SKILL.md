---
name: 05-ux-specification
description: Use when approved user journeys need testable information architecture, interaction patterns, states, accessibility, design-system rules, usability evidence and handoff specifications; use UX content and form specification for copy and validation detail.
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---
# UX Specification Skill
<!-- dual-compat-start -->
## Use When

- User-facing behaviour must be specified across web, mobile or responsive states before build handoff.

## Do Not Use When

- Do not use to choose product scope, write production code, or invent a visual identity without design-system authority.

## Required Inputs

| Artefact | Source or provider | Required? | Missing behaviour |
|---|---|---|---|
| Approved users, journeys and functional requirements | PRD/SRS and research | Required | Stop where a critical journey or user need lacks evidence. |
| Brand/design system, device and accessibility constraints | Design owner and project context | Required | Use an explicit provisional system if authorised; otherwise qualify visual decisions. |

## Workflow

1. Read the named inputs and confirm their approval, version and unresolved decisions.
2. Apply the decision rules below before drafting; stop on a missing authority, unsafe assumption or unresolved scope driver.
3. Produce the UX Specification and handoff evidence through the existing domain procedure and load only the references needed for the chosen branch.
4. Trace each material statement in the UX Specification and handoff evidence to an input, decision or explicitly qualified assumption.
5. Verify the observable acceptance conditions, record unassessed checks, and hand the artefacts to their named consumers.
6. If validation fails, recover by correcting the source decision or artefact and rerun the affected check; do not weaken the acceptance condition.

## Outputs

| Artefact | Consumer | Observable acceptance condition |
|---|---|---|
| UX Specification and handoff evidence | Designers, developers, testers and product owner | Every critical journey includes normal, loading, empty, error, disabled and recovery states; accessibility and usability criteria have observable tests. |

## Evidence Produced

| Evidence | Consumer | Acceptance condition |
|---|---|---|
| Source and decision trace | Reviewer and downstream owner | Each material statement cites an approved input, named decision or qualified open issue. |
| Completed verification record | Release or phase gate owner | Every applicable check records pass/fail; unavailable checks remain `not assessed`. |

## Capability and permission boundaries

Read-only is the default for analysis, review, evaluation and planning. Read and search access to authorised project artefacts are required. Editing is limited to an explicitly requested project deliverable. Execution may run document, syntax or validation checks. Network access is used only for facts that require current verification. Do not publish, spend, change production, approve policy, or claim certification without explicit authority.

## Degraded mode

If any required capability is unavailable, return the narrowest useful qualified UX Specification and handoff evidence draft plus a gap register showing the missing item, affected sections, risk and owner. Never convert an unassessed check into a pass.

## Decision Rules

| Choice | Action | Failure or risk avoided |
|---|---|---|
| Interaction pattern already exists in the design system | Reuse and document variation | Product remains coherent |
| User evidence requires a new pattern | Prototype and test before standardising | Novelty does not create avoidable usability risk |

## Quality Standards

- Preserve repository terminology and trace every material choice to project context.
- Use deterministic acceptance conditions; replace vague quality claims with an observable check, threshold or named approval.
- Cover error, empty, edge, recovery and operational cases relevant to this skill.
- Verify standards, citations, APIs and package names before relying on them; qualify what cannot be checked.
- Stop release for a failed safety, security, legal, financial, accessibility or data-integrity gate.

## Anti-Patterns

- Specifying only the happy path. Fix: cover all operational states and recovery.
- Using lorem ipsum in handoff. Fix: use approved content or labelled realistic samples.
- Naming a font or colour without design-system evidence. Fix: cite the authorised token source.
- Calling a screen accessible without a test. Fix: define keyboard, focus, contrast and assistive-technology checks.
- Hiding responsive behaviour in mock-ups. Fix: specify breakpoint and reflow rules.

## References

- [Design handoff](references/design-handoff.md)
- [Usability testing](references/usability-testing.md)
- [Premium UX specification](references/premium-ui-ux-specification.md)
- [UX content neighbour](../09-ux-content-and-form-specification/SKILL.md)
- Presentation handoff: typeface, colour, layout, motion and visual QA are owned by the `chwezi-design-engine` engine (resolve via the global engine table); this skill states what the experience must achieve and how it is verified.
<!-- dual-compat-end -->

## Overview

Produces a complete UX specification document that bridges user research insights and engineering implementation. The output includes information architecture diagrams (Mermaid flowcharts), wireframing standards across three fidelity levels, design system token definitions, usability testing protocols with quantitative metrics, and developer-ready design handoff specifications. This skill draws on ISO 9241-210 (Human-centred design for interactive systems), ISO/IEC 25010:2023 (Systems and software quality models), and principles from "The Effective Product Designer" and "Design for How People Think" (John Whalen).

The UX specification must treat the design system as a maintained product, not a style appendix. Token layers, component contracts, source-of-truth expectations, and governance responsibilities are part of the specification.

For premium, revenue-critical, executive-facing, dashboard-heavy, Android, or iOS products, the UX specification must also apply the `premium-ui-ux-design` skill and `references/premium-ui-ux-specification.md` so beauty, pleasantness, commercial credibility, platform fit, data quality, and production polish become testable requirements.

## When to Use

- After `HLD.md` exists in `projects/<ProjectName>/<phase>/<document>/` and identifies user-facing components.
- SRS or user stories define user interactions and interface expectations.
- `vision.md` and `features.md` in `projects/<ProjectName>/_context/` provide product scope and feature inventory.
- `stakeholder_register.md` in `projects/<ProjectName>/_context/` identifies user personas and audience segments.

## Quick Reference

| Attribute   | Value |
|-------------|-------|
| **Inputs**  | `projects/<ProjectName>/<phase>/<document>/SRS_Draft.md` or `projects/<ProjectName>/_context/user_stories.md`, `projects/<ProjectName>/<phase>/<document>/HLD.md`, `projects/<ProjectName>/_context/vision.md`, `projects/<ProjectName>/_context/features.md`, `projects/<ProjectName>/_context/stakeholder_register.md` |
| **Outputs** | `projects/<ProjectName>/<phase>/<document>/UX_Specification.md` |
| **Tone**    | Precise, user-centred, standards-grounded |
| **Standard** | ISO 9241-210:2019, ISO/IEC 25010:2023, WCAG 2.2 AA |

## Input Files

| File | Location | Required | Purpose |
|------|----------|----------|---------|
| SRS_Draft.md | `projects/<ProjectName>/<phase>/<document>/SRS_Draft.md` | Preferred | Functional requirements, user interaction flows, data objects |
| user_stories.md | `projects/<ProjectName>/_context/user_stories.md` | Alternate | User stories when SRS is not yet available |
| HLD.md | `projects/<ProjectName>/<phase>/<document>/HLD.md` | Yes | Architectural context, component hierarchy, data flow paths |
| vision.md | `projects/<ProjectName>/_context/vision.md` | Yes | Product scope, target audience, business goals |
| features.md | `projects/<ProjectName>/_context/features.md` | Recommended | Feature inventory for information architecture mapping |
| stakeholder_register.md | `projects/<ProjectName>/_context/stakeholder_register.md` | Recommended | User personas, audience segments, accessibility needs |

## Output Files

| File | Location | Description |
|------|----------|-------------|
| UX_Specification.md | `projects/<ProjectName>/<phase>/<document>/UX_Specification.md` | Complete UX specification with all sections |

## Core Instructions

Follow these eight steps in order. Halt and notify the user if a required input file is missing.

### Step 0: Invoke Frontend Design Plugin

Before executing this skill, invoke the `frontend-design` plugin to analyze the project requirements and determine the most ideal UI/UX approach for this specific project:

```
Use the frontend-design skill to study the project requirements from `_context/` and recommend the optimal UI/UX approach before we generate the formal UX Specification.
```

The frontend-design plugin will analyze:
- Target user segments (from `stakeholder_register.md` or `personas.md`)
- Platform context (web, mobile, desktop — from `tech_stack.md`)
- Domain-specific UI patterns (e.g., clinical dashboards, retail POS, enterprise admin panels)
- Recommended design framework (Bootstrap, Material Design, Tabler, etc.)

Capture the plugin's UI/UX recommendation and incorporate it into all subsequent steps of this skill — especially Step 2 (IA), Step 3 (Wireframe Standards), and Step 4 (Design System).

If the product is premium, revenue-critical, dashboard-heavy, Android, or iOS, also load `premium-ui-ux-design` and include its requirements in the UX specification from the start rather than as a final polish pass.

If the product is SaaS, dashboard-heavy, multi-role, subscription-based, or AI-enabled,
load `references/saas-ux-scope-costing.md` and
`references/web-app-ui-pattern-selection.md` so UX scope, cost drivers, onboarding,
time-to-value, and pattern choices become traceable requirements.

If the product has mobile screens, onboarding, or decision dashboards, also load
`references/mobile-dashboard-ux-requirements.md` so mobile navigation, first-run value,
permission timing, dashboard ownership, metric context, and verification methods are
specified.

### Step 1: Read Context Files

Read `SRS_Draft.md` and `HLD.md` from `projects/<ProjectName>/<phase>/<document>/`. Read `vision.md`, `features.md`, `stakeholder_register.md`, and `user_stories.md` from `projects/<ProjectName>/_context/`. Log the absolute path of each file read. If `SRS_Draft.md` is missing, fall back to `user_stories.md`. If both are missing, halt execution and report the gap. If `HLD.md` or `vision.md` is missing, halt execution and report the gap. If `features.md` or `stakeholder_register.md` is missing, log a warning and proceed with available data.

If an existing product or prior UI exists, document a lightweight UI audit before defining the new system: duplicated components, inconsistent states, token drift, and known design debt.

### Step 2: Generate Information Architecture

The system shall produce the following information architecture artifacts:

1. **Site Map** -- Generate a Mermaid flowchart (`graph TD`) representing the full page/screen hierarchy. Each node shall represent a distinct screen or content group. Use top-down decomposition: start from the application shell, then primary navigation targets, then secondary views.

2. **Content Inventory Table** -- Enumerate every content element:

   | Page/Screen | Content Type | Owner | Status | Priority |
   |-------------|-------------|-------|--------|----------|

3. **Navigation Model** -- Define navigation types present in the application:
   - **Global Navigation:** Persistent across all screens (e.g., top bar, sidebar).
   - **Local Navigation:** Context-specific within a section.
   - **Contextual Navigation:** In-content links and related items.
   - **Utility Navigation:** Account, settings, help, logout.
   - **Breadcrumb Navigation:** Hierarchical path indicator.

4. **Card Sorting Results Template** -- Provide a template for recording card sorting sessions (open or closed) with columns for Card Label, User-Assigned Category, Frequency, and Confidence Score.

See `references/information-architecture.md` for construction techniques and methodology.

### Step 3: Define Wireframe Standards

The system shall define three fidelity levels with explicit scope boundaries:

| Level | Purpose | Content | Tools |
|-------|---------|---------|-------|
| **Low Fidelity** | Structure and layout exploration | Boxes, labels, placeholder text, no color | Paper, whiteboard, Balsamiq |
| **Mid Fidelity** | Layout validation and content placement | Actual content, grayscale, basic interactions | Figma (wireframe mode), Axure |
| **High Fidelity** | Visual design and interaction validation | Full color, real assets, micro-interactions | Figma (design mode), Sketch |

**Required Annotations per Level:**
- Low: Screen name, primary user flow, content blocks, navigation targets.
- Mid: All low-fidelity annotations plus spacing values, content hierarchy, interaction triggers, form field types.
- High: All mid-fidelity annotations plus color tokens, typography tokens, exact spacing (in design tokens), animation timing, accessibility notes.

**Responsive Breakpoints:**
- Mobile: 320px -- 767px (single column, stacked layout, touch targets >= 44px).
- Tablet: 768px -- 1023px (adaptive columns, collapsible navigation).
- Desktop: 1024px+ (multi-column, expanded navigation, hover states).

See `references/wireframing-standards.md` for patterns and examples.

### Step 4: Generate Design System Foundation

The system shall produce design system documentation with three layers:

**4.1 Design Tokens**

- **Color Tokens:** Primitives (palette values) -> Semantic (e.g., `color-action-primary`, `color-feedback-error`) -> Component-level (e.g., `button-primary-bg`).
- **Typography Scale:** Font families, size scale (using a modular scale ratio), line heights, font weights, and letter spacing per usage context (heading, body, caption, code).
- **Spacing Scale:** Base unit of 4px. Scale: 4, 8, 12, 16, 24, 32, 48, 64, 96px. Each value shall have a named token (e.g., `space-xs`, `space-sm`, `space-md`).
- **Elevation/Shadow Levels:** Define shadow levels (0-5) with CSS box-shadow values and usage context (e.g., level-1 for cards, level-3 for modals).

**4.2 Component Library Catalog**

For each UI component, document:

| Property | Description |
|----------|-------------|
| Name | Component identifier (PascalCase) |
| Description | One-sentence purpose statement |
| Variants | Visual/behavioral variations (e.g., primary, secondary, destructive) |
| States | Interactive states (default, hover, focus, active, disabled, loading, error) |
| Props | Configurable properties with types and defaults |
| Usage Guidelines | When to use and when not to use |
| Accessibility | ARIA roles, keyboard behavior, screen reader announcements |
| Ownership | Which team or role approves changes |
| Source of Truth | Where the canonical implementation/documentation lives |

**4.3 Pattern Library**

- **Layout Patterns:** Dashboard, list-detail, master-detail, split view, full-screen modal.
- **Form Patterns:** Single-page form, multi-step wizard, inline editing, search with filters.
- **Navigation Patterns:** Sidebar, top bar, tab bar, breadcrumb, mega menu.
- **Data Display Patterns:** Data table, card grid, timeline, tree view, chart dashboard.

**4.4 Governance And Source Of Truth**

The specification shall define:

- where the canonical design-system truth lives
- how design files, code, and documentation stay aligned
- who can add or change a component
- the review path for new variants or states
- how deprecated components are retired

See `references/design-system-guide.md` for token taxonomy and documentation templates.

**4.5 Premium Experience Foundation**

For premium products, the system shall add:

- Visual voice and rationale tied to the target user, domain, and business model.
- Dominant/subordinate/accent color logic, dark mode expectations, and chart palette rules.
- Typography roles for headings, body, metadata, numbers, captions, labels, and data tables.
- Image, icon, motion, chart, and proof-presentation rules.
- Component state matrix covering default, hover, focus, pressed, selected, disabled, loading, empty, error, success, offline, and permission-denied states.
- Platform-specific criteria for web, Android, and iOS where applicable.

See `references/premium-ui-ux-specification.md` for the premium addendum.

### Step 5: Define Interaction Specifications

The system shall define interaction behaviors for:

1. **Micro-interactions:** Button press feedback, toggle animations, form field focus transitions, notification entry/exit.
2. **Page Transitions:** Navigation transitions (slide, fade, none), modal open/close, drawer expand/collapse.
3. **Loading States:** Skeleton screens (preferred over spinners for content areas), progress indicators (determinate for uploads, indeterminate for fetches), optimistic UI updates.
4. **Error States:** Inline field validation (on blur), form-level error summary, toast notifications (auto-dismiss after 5s for info, persist for errors), empty states with actionable guidance, offline/connectivity loss handling.

Each interaction shall specify: trigger, animation duration (in ms), easing function, and fallback for reduced-motion preferences per `prefers-reduced-motion` media query.

### Step 6: Define Accessibility Requirements

The system shall enforce WCAG 2.2 Level AA compliance (W3C Recommendation, 12 December 2024 edition; verified 2026-09-24):

| Criterion | Requirement | Verification Method |
|-----------|-------------|---------------------|
| Color Contrast | Text contrast ratio >= 4.5:1 (normal text), >= 3:1 (large text) | Automated contrast checker |
| Keyboard Navigation | All interactive elements shall be reachable via Tab, operable via Enter/Space, dismissible via Escape | Manual keyboard walkthrough |
| Screen Reader | All images shall have alt text, all form fields shall have associated labels, dynamic content shall use ARIA live regions | Screen reader testing (NVDA, VoiceOver) |
| Focus Management | Visible focus indicator on all interactive elements, logical tab order, focus trap in modals | Manual inspection |
| Touch Targets | WCAG 2.2 SC 2.5.8 minimum 24x24 CSS px (or spacing exception); premium mobile target 44x44 pt (iOS) / 48x48 dp (Android) | Design review and rendered measurement |
| WCAG 2.2 additions | Focus not obscured by sticky UI (SC 2.4.11); single-pointer alternative to every drag (2.5.7); no memory or transcription test at login without paste, password manager or passkey (3.3.8); help in consistent order (3.2.6); no redundant re-entry within a process (3.3.7) | Keyboard, login and journey walkthroughs at each breakpoint |
| Motion | The system shall respect `prefers-reduced-motion` and provide static alternatives | CSS media query audit |

### Step 7: Create Usability Testing Protocol

The system shall define a usability testing framework:

**7.1 Test Planning Template**
- Objectives: What hypotheses does this test validate?
- Participants: Minimum 5 per user segment (per Nielsen Norman Group recommendation).
- Environment: Moderated remote, unmoderated remote, or in-person lab.

**7.2 Task Scenario Template**
- Task scenarios shall be realistic, goal-oriented, and free of leading language.
- Format: "You are [context]. You want to [goal]. Using the application, [action]."

**7.3 Success Metrics**

| Metric | Target | Measurement |
|--------|--------|-------------|
| Task Completion Rate | >= 85% | Binary pass/fail per task per participant |
| Time on Task | Varies by complexity | Stopwatch from task start to completion |
| Error Rate | <= 2 errors per task | Count of incorrect actions or missteps |
| Time to Learn | First-time task completion within [N] minutes | Measured in orientation session; user completes target task unassisted |
| User Memory Retention | [X]% recall of core workflows after 2-week gap | Measured in follow-up session without training refresher |
| SUS Score | >= 68 (above average) | Post-test System Usability Scale questionnaire |

**7.4 Observation Recording Format**

| Task | Participant | Time (s) | Errors | Path Taken | Quotes | Severity |
|------|-------------|----------|--------|------------|--------|----------|

**7.5 Findings-to-Requirements Feedback Loop**
- Each finding shall be classified by severity (Critical, Major, Minor, Cosmetic).
- Critical and Major findings shall generate new or revised requirements traceable to SRS Section 3.2.
- The system shall maintain a findings register mapping each observation to a requirement ID.

**7.6 Heuristic Evaluation — Eight Golden Rules**

Before conducting participant usability tests, perform a heuristic evaluation of the design against Shneiderman & Plaisant's Eight Golden Rules of Interface Design (Designing the User Interface, 7th Ed., 2016):

| Rule | Principle | Evaluation Question |
|------|-----------|---------------------|
| 1. Strive for Consistency | Identical terminology, layout, and color across similar situations | Are menus, labels, and button styles consistent across all screens? |
| 2. Seek Universal Usability | Design for diverse user abilities; provide novice and expert paths | Does the interface work for both first-time and power users? |
| 3. Offer Informative Feedback | Every user action receives an interface response | Does every action (button click, form submit) give visible feedback? |
| 4. Design Dialogs to Yield Closure | Actions have a beginning, middle, and end | Do multi-step processes (wizards, checkout flows) have clear completion states? |
| 5. Prevent Errors | Interface design minimizes serious user errors | Are irreversible actions (delete, submit) protected with confirmations? |
| 6. Permit Easy Reversal | Actions should be reversible to reduce anxiety | Can users undo or go back at every stage? |
| 7. Keep Users in Control | Experienced users feel in charge; no unexpected behavior | Can users customize their workflow? Are surprises avoided? |
| 8. Reduce Short-term Memory Load | Avoid requiring users to remember information across screens | Is context information visible in-view when needed (not hidden behind tabs)? |

Rate each rule: **Pass** / **Partial** / **Fail**. Each **Fail** generates a design issue logged in the findings register per §7.5.

**Standard:** Shneiderman & Plaisant (2016), *Designing the User Interface: Strategies for Effective Human-Computer Interaction*, 6th Ed.

See `references/usability-testing.md` for the SUS questionnaire and scoring methodology.

### Step 8: Generate Design Handoff Checklist

The system shall produce developer-ready handoff specifications:

**8.1 Annotation Standards**
- Spacing values shall reference design tokens, not raw pixel values.
- Colors shall reference semantic tokens (e.g., `color-action-primary`), not hex codes.
- Interaction states shall be documented for every interactive component (default, hover, focus, active, disabled).
- Responsive behavior shall specify layout changes at each breakpoint.

**8.2 Asset Delivery Checklist**

| Asset Type | Format | Naming Convention | Resolution |
|------------|--------|-------------------|------------|
| Icons | SVG | `icon-{name}-{size}.svg` | Vector |
| Illustrations | SVG + PNG fallback | `illustration-{name}.svg` | 1x, 2x |
| Photos | WebP + JPEG fallback | `photo-{context}-{id}.webp` | 1x, 2x, 3x |
| Logos | SVG | `logo-{variant}.svg` | Vector |

**8.3 Implementation Acceptance Criteria**
- The implemented component shall match the design specification within 2px tolerance.
- All design tokens shall be consumed from the shared token system, not hard-coded.
- Responsive layouts shall function correctly at all three breakpoint ranges.
- All WCAG 2.2 AA criteria defined in Step 6 shall pass automated and manual testing.
- Interaction timing shall match specification within 50ms tolerance.
- Premium products shall include a premium UI/UX gate score with every category at 8/10 or better before design sign-off.

## Premium experience and originality addendum
Apply `09-governance-compliance/31-kaizen-engine-and-product-improvement/references/ux-friction-and-premium-experience-requirements.md` for client-facing, dashboard, onboarding, data-entry, or high-stakes UX; it requires client context, a purpose-fit thesis, authored decisions, decision-surface logic, critical states, measures, handoff proof, and `NOT ASSESSED` for missing render or user evidence.

## Output Format

The generated `UX_Specification.md` shall use this section structure with a Document Header (Date, Version, Authors, Standard), followed by eight sections:

1. **Information Architecture** -- Site map (Mermaid flowchart), content inventory, navigation model, card sorting template
2. **Wireframe Standards** -- Fidelity levels, annotation requirements, responsive breakpoints
3. **Design System** -- Design tokens (color, typography, spacing, elevation), component catalog, pattern library
4. **Interaction Specifications** -- Micro-interactions, transitions, loading states, error states
5. **Accessibility Requirements** -- WCAG 2.2 AA criteria with verification methods
6. **Usability Testing Protocol** -- Task scenarios, success metrics, observation format, feedback loop
7. **Design Handoff** -- Annotation standards, asset delivery, acceptance criteria
8. **Traceability Matrix** -- Screen/Component mapped to SRS Section/Requirement IDs

For premium products, add **Premium Experience Strategy** and **Premium Gate** subsections inside Sections 3, 6, 7, and 8 rather than appending generic polish notes.

For forms, critical microcopy, onboarding, checkout, applications, error-heavy workflows, or public-sector submissions, add a companion output from `03-design-documentation/09-ux-content-and-form-specification` so labels, help text, validation, error states, completion metrics, and content governance are testable.

## Cross-References

For cognitive evaluation of designs (mental models, attention patterns, emotional response, memory load), reference `cognitive-ux-framework`.

For premium visual quality, platform fit, data quality, and production gates, reference `premium-ui-ux-design`.

## Common Pitfalls

| Pitfall | Remedy |
|---------|--------|
| Using raw pixel values instead of tokens | The system shall reference named design tokens for all spacing, color, and typography values |
| Missing accessibility annotations | Every interactive component shall include ARIA roles, keyboard behavior, and contrast verification |
| Wireframes without responsive variants | Each wireframe shall show mobile, tablet, and desktop adaptations |
| Usability test tasks with leading language | Task scenarios shall describe goals without hinting at the solution path |
| Design handoff without interaction states | Every component shall document default, hover, focus, active, and disabled states |
| No feedback loop from testing to requirements | Usability findings rated Critical or Major shall generate traceable requirement updates |

## Verification Checklist

- [ ] `UX_Specification.md` exists in `projects/<ProjectName>/<phase>/<document>/`.
- [ ] Site map renders correctly in Mermaid flowchart syntax.
- [ ] All three wireframe fidelity levels are defined with annotation requirements.
- [ ] Design tokens cover color, typography, spacing, and elevation.
- [ ] Component catalog entries include all required properties (name, variants, states, props, accessibility).
- [ ] WCAG 2.2 AA criteria are specified with verification methods.
- [ ] Usability testing protocol defines quantitative success metrics.
- [ ] Design handoff uses token references, not raw values.
- [ ] Traceability matrix links every screen/component to SRS requirements.
- [ ] Premium products include the premium UI/UX addendum and gate score.

## Integration

| Direction | Skill | Relationship |
|-----------|-------|-------------|
| Upstream | 01-high-level-design | Consumes `HLD.md` for component hierarchy and data flow |
| Upstream | Phase 02 (Requirements) | Consumes SRS or user stories for functional context |
| Downstream | Phase 04 (Development) | Provides component specs, tokens, and acceptance criteria for front-end implementation |
| Downstream | Phase 05 (Testing) | Provides usability test protocols and accessibility verification criteria |
| Cross-Ref | `cognitive-ux-framework` | Cognitive evaluation methodology for design decisions |
| Cross-Ref | `premium-ui-ux-design` | Premium UI/UX requirements, platform fit, data quality, and visual production gate |
| Cross-Ref | `03-design-documentation/09-ux-content-and-form-specification` | Detailed UX content, form, validation, and error-state requirements |

## Standards

- **ISO 9241-210:2019** -- Human-centred design for interactive systems: iterative design process, user research, usability evaluation
- **ISO/IEC 25010:2023** -- Systems and software quality models: interaction capability (formerly usability), including appropriateness recognisability, learnability, operability, user error protection, user engagement (replaces user interface aesthetics), inclusivity, user assistance and self-descriptiveness
- **WCAG 2.2 Level AA** -- Web Content Accessibility Guidelines: perceivable, operable, understandable, robust
- **ISO/IEC/IEEE 29148:2018** (supersedes IEEE 830-1998) -- Requirement traceability for UX-to-requirement mapping

## Resources

- `references/information-architecture.md` -- Site map construction and navigation model reference.
- `references/wireframing-standards.md` -- Fidelity levels, annotation rules, and common patterns.
- `references/design-system-guide.md` -- Token taxonomy, component documentation template, pattern library.
- `references/usability-testing.md` -- Test planning, SUS questionnaire, observation format.
- `references/design-handoff.md` -- Annotation standards, asset delivery, acceptance criteria.
- `references/premium-ui-ux-specification.md` -- Premium UI/UX addendum for visual quality, platform fit, dashboard quality, and premium gate scoring.
- `03-design-documentation/09-ux-content-and-form-specification` -- companion skill for UX text, form quality gates, validation timing, and error recovery requirements.
- `README.md` -- Quick-start guide for this skill.

## UX foundations integration (added 2026-05-04 from Branson + Synechron + Deacon)

Canonical reference: [UX requirements foundations](references/ux-requirements-foundations.md) (engine-local, 7 sections).

This skill consumes the broadest portion of the foundations doc. Required reading before producing a UX specification:

- **Section 2 (persona and actor discipline)** — every UX spec's persona section must declare one primary persona and evidence its role, tasks, goals, context, pain points and constraints
- **Section 4 (UX outcome launch gate and maturity)** — every UX spec must declare which maturity level (Level 3 minimum for premium) and document the 5 outcomes as launch criteria
- **Sections 5 and 6 (cognitive load and affordance review)** — used as NFR templates and design-review heuristics
- **Section 1 (experience scope)** — every UX spec declares which scope level it targets

### Required NFR templates (drawn from Section 5)

The UX spec's non-functional-requirements section must include, where applicable:

- **List-length limit** — set a project-specific limit for primary navigation and primary action lists and validate it in usability testing; the "7 plus or minus 2" figure is not a design rule (see the reference's currentness note). Chunk longer sets into labelled groups.
- **Form-step scope** — one decision theme per step; longer forms split into multi-step flows with explicit progress and saved state.
- **Cognitive-load minimization** — plot working-memory load across the primary user task; identify task-closure points; redesign if load never reaches zero across the flow.
- **Stacking-safe interruption recovery** — every multi-step flow auto-saves state; every page that can be interrupted has a "back to where you were" affordance.

### Required affordance audit (drawn from Section 6)

For every primary CTA listed in the UX spec, document Yes/No on each of:
- **Presence** — does the affordance exist?
- **Visibility/Perceivability** — can it be seen at first glance?
- **Recognizability** — can it be detected without searching?
- **Intelligibility** — is the meaning clear once read?

Any No = redesign required before launch.

### Required scope declaration (drawn from Section 1)

The UX spec opens with one sentence: "This specification targets [Single Interaction / Journey / Relationship] level UX scope."

### Required maturity declaration (drawn from Section 4)

The UX spec opens with one sentence: "This specification operates at UX Maturity Level [3 / 4]. Premium-pricing claims require Level 3 minimum."

### Existing references unchanged

This section augments — does not replace — the existing references in `references/`: `design-handoff.md`, `design-system-guide.md`, `information-architecture.md`, `premium-ui-ux-specification.md`, `usability-testing.md`, `wireframing-standards.md`. Use them as before; the new section adds upstream discipline.
