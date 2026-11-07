# 05 - UX Specification

## Objective

Generate a comprehensive UX specification document covering information architecture, wireframing standards, design system documentation, usability testing protocols, and design handoff specs per ISO 9241-210 and ISO 25010. The output provides a single source of truth for designers and developers to align on user experience implementation.

## When to Use

- After `HLD.md` exists in `projects/<ProjectName>/<phase>/<document>/` and identifies user-facing components.
- When SRS or user stories define user interactions and interface expectations.
- When the project requires formal UX documentation for design-development handoff.
- Before front-end development begins, to establish design tokens and component standards.

## Inputs

| File | Location | Required |
|------|----------|----------|
| SRS_Draft.md | `projects/<ProjectName>/<phase>/<document>/` | Preferred |
| user_stories.md | `projects/<ProjectName>/_context/` | Alternate (if no SRS) |
| HLD.md | `projects/<ProjectName>/<phase>/<document>/` | Yes |
| vision.md | `projects/<ProjectName>/_context/` | Yes |
| features.md | `projects/<ProjectName>/_context/` | Recommended |
| stakeholder_register.md | `projects/<ProjectName>/_context/` | Recommended |

## Outputs

| File | Location |
|------|----------|
| UX_Specification.md | `projects/<ProjectName>/<phase>/<document>/` |

## Quick Start

1. Verify that `HLD.md` and `vision.md` exist.
2. Invoke this skill: the system shall read context files, generate information architecture, define wireframe standards, produce design system tokens, specify interactions and accessibility requirements, create usability testing protocols, and generate the design handoff checklist.
3. Review `projects/<ProjectName>/<phase>/<document>/UX_Specification.md` for completeness against the verification checklist in `SKILL.md`.

## Execution Steps

1. **Read Context** -- Load SRS/stories, HLD, vision, features, and stakeholder register. Halt if required files are missing.
2. **Information Architecture** -- Generate site map (Mermaid flowchart), content inventory, navigation model, card sorting template.
3. **Wireframe Standards** -- Define low/mid/high fidelity levels with annotation requirements and responsive breakpoints (mobile, tablet, desktop).
4. **Design System** -- Document design tokens (color, typography, spacing, elevation), component catalog, and pattern library.
5. **Interaction Specs** -- Define micro-interactions, transitions, loading states, and error states with timing and easing.
6. **Accessibility** -- Specify WCAG 2.2 AA requirements with verification methods.
7. **Usability Testing** -- Create task scenarios, success metrics (completion rate, time, errors, SUS), observation format, findings-to-requirements loop.
8. **Design Handoff** -- Generate annotation standards (token-based), asset delivery checklist, implementation acceptance criteria.

## Resources

- `SKILL.md` -- Full skill specification with core instructions and verification checklist.
- `references/information-architecture.md` -- Site map construction and navigation models.
- `references/wireframing-standards.md` -- Fidelity levels and common wireframe patterns.
- `references/design-system-guide.md` -- Token taxonomy and component documentation template.
- `references/usability-testing.md` -- Test planning, SUS scoring, and observation format.
- `references/design-handoff.md` -- Annotation standards and developer acceptance criteria.
- `references/house-style-declaration.md` -- Required house-style declaration (HS-01 to HS-12) for products that follow the Chwezi business-app house style.
