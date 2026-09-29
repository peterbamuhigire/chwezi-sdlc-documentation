---
name: 01-user-manual
description: Use when producing role-based, task-oriented operating guidance for an implemented product. Use installation-guide for setup, FAQ for concise recurring answers, and release-notes for version deltas.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# User Manual Skill

<!-- dual-compat-start -->

## Use When

- Use when producing role-based, task-oriented operating guidance for an implemented product. Use installation-guide for setup, FAQ for concise recurring answers, and release-notes for version deltas.

## Do Not Use When

- Do not use when a more specific upstream or downstream skill owns the task, or when the required project context has not been prepared.
- Do not use this skill to fabricate missing project facts, legal conclusions, test results, approvals, or certification claims.

## Required Inputs

| Artefact | Source or provider | Required? | Missing-input behaviour |
|---|---|---:|---|
| Approved feature inventory; current role and permission matrix; verified UI build or screenshots; workflows; error states; support escalation routes | Product owner, implementation team, and support owner | Yes | Stop dependent work; name the missing item, owner, and decision impact. A review check remains `not assessed`. |
| Scope, audience, baseline/version, and accountable decision owner | Requester or project context | Yes | Ask for or record the gap; do not infer authority or scope. |

## Capability and permission boundaries

Default to read-only. Read and search access to the supplied artefacts are required. Editing is limited to an explicitly authorised requested draft or project files. Execute validation only when authorised; publishing, signature, certification, production mutation, destructive action, spending, and risk acceptance require explicit authority.

## Degraded Mode

When files, tools, network, rendering, fonts, execution, or evidence are unavailable, return the narrowest useful qualified draft or finding set. Name every unavailable check and its consequence; an unassessed check is never a pass. Preserve evidence already gathered and provide the exact next verification step.

## Decision Rules

| Condition | Action | Failure or risk avoided |
|---|---|---|
| A feature, screen, or answer is not confirmed in the product or approved source | Omit or mark it pending verification | Documenting nonexistent behaviour |
| A procedure lacks a success or recovery state | Add both before publication | Users stranded after errors |

## Workflow

1. Confirm the requested artefact, audience, scope, decision owner, and applicable baseline or version. Work read-only by default; source mutation, publication, signature, certification, production change, or risk acceptance requires explicit authority.
2. Inspect every required input and record missing, stale, conflicting, or inaccessible evidence. Stop claims that depend on an unresolved required input.
3. Apply the Decision Rules, then execute the existing Core Instructions below in order; preserve project terminology and trace each material statement to its source.
4. Test the draft against the output acceptance conditions and domain quality standards. If a check cannot run, mark it `not assessed` and never convert it into a pass.
5. On failure, recover by preserving completed evidence, identifying the narrowest corrective action and owner, and rerunning only the affected checks before handoff.
6. Produce the named artefact and evidence record; publish, sign, certify, mutate production, or accept risk only under explicit authority.

## Outputs

| Artefact | Consumer | Observable acceptance condition |
|---|---|---|
| User Manual | Customer, support, success, sales, or implementation owner | Every released feature and role has a tested procedure, expected result, error recovery, and verified navigation reference. |
| Gap and decision record | Accountable owner and downstream reviewer | Every gap has status, impact, owner, next action, and no unsupported pass or approval. |

## Evidence Produced

| Evidence | Contents | Acceptance condition |
|---|---|---|
| User Manual evidence record | Source identifiers, scope/version, decisions, checks, exceptions, and approval state | A reviewer can reproduce each material conclusion from named sources. |
| Validation record | Check, result (`pass`, `fail`, or `not assessed`), evidence location, date, and actor | No required check is omitted or silently treated as passed. |

## Quality Standards

- Keep outputs grounded in source context, traceable to stated standards, and specific enough to review or verify.
- Use deterministic acceptance conditions and preserve traceability from source to decision and output.
- Separate facts, inferences, assumptions, and approvals; never present one as another.
- Apply `28-anti-ai-slop` during authoring and `29-ai-slop-audit` at major checkpoints and release.

## Anti-Patterns

- **Producing User Manual from assumptions instead of named project sources.** Fix: Cite the source or mark the item unverified.
- **Treating a missing or inaccessible check as passed.** Fix: Mark it `not assessed`, state impact, and block dependent claims.
- **Using vague gates such as `adequate`, `secure`, or `user-friendly`.** Fix: Replace each with an observable criterion, threshold, and evidence source.
- **Copying a generic template without product, control, role, version, or jurisdiction detail.** Fix: Ground every section in the supplied context and remove unused boilerplate.
- **Publishing, signing, certifying, changing production, or accepting risk without authority.** Fix: Prepare a draft and route the decision to the accountable owner.
- **Listing evidence without provenance or an acceptance result.** Fix: Record source, period, integrity check, mapping, and pass/fail/not-assessed status.

## Worked Example

Example: if a feature, screen, or answer is not confirmed in the product or approved source, omit or mark it pending verification. Record the evidence and result in the validation record; this avoids documenting nonexistent behaviour.

## References

- [Generation logic](logic.prompt): load when creating the complete artefact.
- [Skill notes](README.md): consult for local examples and invocation context.
- [Repository operating rules](../../AGENTS.md): apply the engine's routing, evidence, and release gates.

<!-- dual-compat-end -->

## Overview

This is the first skill in Phase 08 (End-User Documentation). It produces a comprehensive user manual that guides end users through every feature of the software product with step-by-step procedures, screenshot placeholders, navigation overviews, and role-based workflow instructions. The output conforms to ISO 26514 (User Documentation) and serves as the primary reference for end users adopting the system.

## When to Use This Skill

- After Phase 02 completes and `vision.md` and `features.md` exist in `projects/<ProjectName>/_context/`.
- When end users require a structured guide to learn and operate the software product.
- Optionally after Phase 05 when `user_stories.md` exists in `projects/<ProjectName>/<phase>/<document>/` for richer workflow context.
- Optionally after Phase 02 when `SRS_Draft.md` exists in `projects/<ProjectName>/<phase>/<document>/` for detailed functional reference.

## Quick Reference

| Attribute    | Value |
|--------------|-------|
| **Inputs**   | `projects/<ProjectName>/_context/vision.md`, `projects/<ProjectName>/_context/features.md`, `projects/<ProjectName>/<phase>/<document>/SRS_Draft.md` (optional), `projects/<ProjectName>/<phase>/<document>/user_stories.md` (optional) |
| **Output**   | `projects/<ProjectName>/<phase>/<document>/User_Manual.md` |
| **Tone**     | Instructional, user-facing, task-oriented |
| **Standard** | ISO 26514 |
| **Time**     | 15-25 minutes |

## Input Files

| File | Location | Required | Purpose |
|------|----------|----------|---------|
| vision.md | `projects/<ProjectName>/_context/vision.md` | Yes | Product purpose, target audience, high-level goals |
| features.md | `projects/<ProjectName>/_context/features.md` | Yes | Feature list with descriptions for per-feature guide generation |
| SRS_Draft.md | `projects/<ProjectName>/<phase>/<document>/SRS_Draft.md` | No | Detailed functional requirements for precise procedure steps |
| user_stories.md | `projects/<ProjectName>/<phase>/<document>/user_stories.md` | No | User stories and personas for role-based workflow generation |

## Output Files

| File | Location | Description |
|------|----------|-------------|
| User_Manual.md | `projects/<ProjectName>/<phase>/<document>/User_Manual.md` | Complete user manual with getting started, feature guides, role-based workflows, troubleshooting, and glossary |

## Core Instructions

Follow these eight steps in order. Halt and notify the user if a required input file is missing.

### Step 1: Read Context Files

Read `vision.md` and `features.md` from `projects/<ProjectName>/_context/`. Optionally read `SRS_Draft.md` and `user_stories.md` from `projects/<ProjectName>/<phase>/<document>/`. Log the absolute path of each file read. Halt if any required file is missing.

### Step 2: Define Getting Started Section

Document the onboarding experience for a first-time user:
- System access procedures (login, registration, initial setup)
- First-run configuration or wizard steps
- Orientation to the primary interface layout
- Quick-start task that demonstrates core value within five minutes

### Step 3: Generate Navigation Overview

Produce a navigation map of the application:
- Primary navigation elements (menus, sidebars, toolbars) with screenshot placeholders
- Page-by-page or screen-by-screen summary with purpose description
- Navigation shortcuts and keyboard accelerators if applicable

### Step 4: Generate Feature Guides

For each feature in `features.md`, produce a dedicated section:
- Feature purpose and user benefit (one to two sentences)
- Step-by-step procedure with numbered instructions
- Screenshot placeholders formatted as `[Screenshot: Feature Name - Step N]` until a verified image file is supplied
- Expected results after each critical step
- Edge cases and limitations the user should be aware of

### Step 5: Generate Role-Based Workflows

If `user_stories.md` is present, define workflows per user role:
- Identify distinct user roles from stories or personas
- Map each role to its permitted features and typical task sequences
- Produce end-to-end workflow walkthroughs for each role
- Order each role's walkthrough from foundational screens (sign-in, home, the records the role creates first) to the dependent workflows that use them, and end with administration; keep 5–12 steps per role, and split a longer walkthrough by task.
- If no user stories exist, generate workflows based on features.md feature groupings

### Step 6: Generate Troubleshooting Section

Document common user-facing issues and resolutions:
- Error message catalog with plain-language explanations and resolution steps
- Frequently encountered obstacles during onboarding
- Performance or display issues with recommended actions
- Escalation path for unresolved issues (support contact, ticket system)

### Step 7: Generate Glossary

Compile a glossary of domain-specific and product-specific terms:
- Every acronym and abbreviation used in the manual SHALL be expanded
- Technical terms SHALL include user-friendly definitions
- Terms SHALL be sorted alphabetically

### Step 8: Assemble and Write Output

Assemble all sections into the final document with a table of contents. Write the completed document to `projects/<ProjectName>/<phase>/<document>/User_Manual.md`. Log the total count of feature guides and role-based workflows generated.

## Output Format Specification

The generated `User_Manual.md` SHALL contain these sections in order:

1. **Document Header** -- Product name, version, date, audience, standards reference
2. **Table of Contents** -- Auto-navigable section links
3. **Getting Started** -- First-time user onboarding and quick-start
4. **Navigation Overview** -- Interface map with screenshot placeholders
5. **Feature Guides** -- Per-feature step-by-step procedures
6. **Role-Based Workflows** -- End-to-end task sequences per user role
7. **Troubleshooting** -- Error catalog and resolution steps
8. **Glossary** -- Alphabetical term definitions
9. **Support & Contact** -- Escalation paths and contact information

## Final Step: Write `manifest.md`

After generating all section files, create (or overwrite) `manifest.md` in this document's directory listing the section files in the correct assembly order:

```markdown
# Document Manifest — User Manual
# Generated by user-manual. Edit to reorder or exclude sections before building.
01-getting-started.md
02-navigation-overview.md
03-feature-guides.md
04-role-based-workflows.md
05-troubleshooting.md
06-glossary.md
07-support.md
```

This ensures `scripts/build-doc.sh` assembles sections in the intended order rather than alphabetical fallback.

## Common Pitfalls

- **Jargon without definition:** Every technical term SHALL appear in the glossary with a user-friendly definition.
- **Missing screenshot placeholders:** Every multi-step procedure SHALL include at least one screenshot placeholder per critical step.
- **Role-agnostic instructions:** Workflows SHALL be segmented by user role when multiple roles exist.
- **Assumed prior knowledge:** The Getting Started section SHALL assume zero familiarity with the product.
- **Missing error guidance:** Every known error state SHALL have a documented resolution path.

## Verification Checklist

1. `User_Manual.md` exists in `projects/<ProjectName>/<phase>/<document>/` with all nine sections populated.
2. Getting Started section assumes zero prior knowledge and includes a quick-start task.
3. Every feature in `features.md` has a corresponding feature guide section.
4. Screenshot placeholders follow the `[Screenshot: Name - Step]` format and are replaced only with verified image files.
5. Role-based workflows cover every identified user role, each ordered from foundational screens to dependent workflows to administration, in 5–12 steps.
6. Troubleshooting section includes error messages with resolution steps.
7. Glossary contains every acronym and technical term used in the manual.
8. Table of contents links match actual section headings.

## Integration

| Direction | Skill | Relationship |
|-----------|-------|-------------|
| Upstream | Phase 02 (Requirements Engineering) | Consumes `vision.md` and `features.md` for product scope |
| Upstream | Phase 05 (Testing Documentation) | Consumes `user_stories.md` for role-based workflows |
| Downstream | 03-faq | FAQ generation references the user manual for cross-linking |
| Downstream | Phase 09 (Compliance) | User manual feeds compliance documentation traceability |

## Standards Compliance

- **ISO 26514** -- Systems and Software Engineering -- Requirements for Designers and Developers of User Documentation. Governs structure, completeness, and audience-appropriateness of user-facing documentation.

## Resources

- `logic.prompt` -- Executable prompt containing the step-by-step user manual generation logic.
- `README.md` -- Quick-start guide for this skill.

The walkthrough ordering rule (Step 5) adapts the reading-path ordering in Understand Anything (MIT, https://github.com/Egonex-AI/Understand-Anything, commit b05cc3b20990afca537b4fc0a49b4d7fbdc65bb0). Paraphrased.
