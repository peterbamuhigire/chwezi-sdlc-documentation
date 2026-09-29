---
name: 01-initialize-srs
description: "Use when writing a new SRS (software requirements specification) for a business system or module: create the Waterfall SRS workspace, IEEE structure, identifiers and source context; use context-engineering next for boundaries and actors."
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---

> **[MISSING FILE FALLBACK]**
> This skill references auxiliary files (`logic.prompt`, Python scripts) for automated execution.
> **If those files are unavailable in your environment**, Claude can execute this skill directly:
> 1. Read all files in `projects/<ProjectName>/_context/`
> 2. Follow the step-by-step instructions in the **Manual Execution** section below (or ask Claude to generate the relevant SRS section by describing the context inline)
> 3. Write output to `projects/<ProjectName>/02-requirements-engineering/01-srs/<section-file>.md`
>
> _This skill is fully executable without Python or logic.prompt by providing context directly to Claude._

## Royce's 5 Critical Steps (IEEE WESCON 1970)

> Royce's original paper explicitly states the basic sequential waterfall (analysis → design → coding → testing) **"is risky and invites failure."** His real contribution was five corrective steps that all must be present for waterfall to succeed. Consultants must verify all five are planned before proceeding.

| Step | Requirement | Status Check |
|------|-------------|--------------|
| **1. Design First** | Preliminary program design (storage, timing, interfaces) must exist BEFORE analysis begins | `_context/` must include architecture constraints in `tech_stack.md` |
| **2. Document Everything** | Documentation IS the design. "If the documentation does not yet exist there is as yet no design." | All 6 Royce canonical docs must be planned |
| **3. Do It Twice** | Build a pilot/prototype first. Delivered version should be the second version | Pilot plan should exist in `01-strategic-vision/` |
| **4. Plan Testing Early** | Test planning starts at Program Design phase, not at the testing phase | Test Strategy should be initiated during Phase 03 Design |
| **5. Involve the Customer** | Three formal review gates: PSR (after prelim design), CSR (during design), FSAR (after testing) | Review gate dates must be in project schedule |

**Royce's 6 Canonical Documents (all must exist at delivery):**
1. Software Requirements → `SRS_Draft.docx` (this pipeline)
2. Preliminary Design Spec → `HLD.docx` (Phase 03)
3. Interface Design Spec → `APISpec.docx` + `DatabaseDesign.docx` (Phase 03)
4. Final Design Spec (As-Built) → `LLD.docx` updated after coding (Phase 03/04)
5. Test Plan + Test Results → `TestPlan.docx` + `TestReport.docx` (Phase 05)
6. Operating Instructions → `UserManual.docx` + `DeploymentGuide.docx` (Phase 06/08)

# Initialize-SRS Skill Guidance

<!-- local-contract-start -->
<!-- dual-compat-start -->
## Use When

- creating the Waterfall SRS workspace, selecting the specification structure, and establishing identifiers and source context; use context-engineering after initialisation to model boundaries and actors.
- Use this procedure when the required source artefacts are available and `Initialised SRS workspace and manifest` is the next lifecycle deliverable.

## Do Not Use When

- Use `context-engineering` when that neighbouring route owns the decision or deliverable.
- Do not invent missing project evidence, standards clauses, thresholds, or stakeholder decisions.

## Required Inputs

| Artefact | Source or provider | Required? | Behaviour when missing |
| --- | --- | --- | --- |
| Project brief, methodology decision, context files, standards profile, and repository path | Sponsor, project context, and methodology selection | Yes | Stop the affected step, name the missing source, and return only a qualified gap record. |

## Workflow

1. Inspect the required inputs and log the exact sources, versions, and unresolved assumptions.
2. Apply this skill's existing domain workflow and decision rules to produce `Initialised SRS workspace and manifest`.
3. Stop when a required source, accountable decision owner, or deterministic test oracle is absent.
4. Recover by preserving valid work, marking the blocked scope, and returning the narrowest qualified artefact plus the next evidence needed.

## Outputs

| Artefact | Consumer | Acceptance condition |
| --- | --- | --- |
| Initialised SRS workspace and manifest | Context engineering and requirements authors | Required sections are populated, source links resolve, and every material requirement or decision has an observable review or test oracle. |

## Evidence Produced

| Evidence | Reviewer | Acceptance condition |
| --- | --- | --- |
| Source, decision, trace, and validation record for `Initialised SRS workspace and manifest` | Requirements quality reviewer | Inputs used, decisions made, checks run, failures, and unassessed items are explicit. |

## Capability and permission boundaries

Read and search are required. Editing is allowed only when the request authorises creation or repair of the named requirements artefact. Publishing, production mutation, destructive action, spending, and certification require explicit authority.

## Degraded mode

Fallback: if a required file, reviewer, standard source, network check, renderer, or execution capability is unavailable, return the narrowest useful qualified result and mark the affected check `not assessed`; never convert an unassessed check into a pass.

## Decision Rules

| Choice or condition | Action | Failure or risk avoided |
| --- | --- | --- |
| The methodology, project identity, or source-of-truth path is unresolved | Stop initialisation and record the missing decision. | An SRS created in the wrong structure or project. |
| Required inputs and test oracles are complete | Continue through the existing workflow and record evidence. | A deliverable whose acceptance cannot be reproduced. |
| A mandatory source or owner is missing | Stop the affected branch and issue a qualified gap record. | Fabricated context or unauthorised decisions. |

## Quality Standards

- Preserve stable identifiers and bidirectional traceability from project evidence to `Initialised SRS workspace and manifest` and its acceptance checks.
- Apply ISO/IEEE measures only with a named metric, method, threshold, evidence source, and responsible reviewer; run the anti-slop gate before release.

## Anti-Patterns

- Producing `Initialised SRS workspace and manifest` from assumed context. Fix: cite the project source or mark the scope blocked.
- Accepting a material requirement without a deterministic oracle. Fix: add a measurable result, boundary, and verification method.
- Crossing into `context-engineering` without routing the decision. Fix: hand off the named input and preserve trace links.
- Treating an unavailable check as passed. Fix: mark it `not assessed` and state the release consequence.
- Claiming standards, statutory, or stakeholder approval without evidence. Fix: cite the source and reviewer or qualify the claim.

## References

- [Skill authoring and release standard](../../../docs/skill-authoring-standard.md)
- [Final requirements quality gate](../../references/final-requirements-quality-gate.md): the exit gate every SRS started here must pass before review or build.
<!-- dual-compat-end -->
<!-- local-contract-end -->

## Overview
Use this skill to bootstrap the parent project with industrial templates that capture vision, features, technology constraints, business rules, quality standards, and glossary definitions before running any other SRS skills. The skill provides an automation script plus template guidance so Claude can reliably seed `projects/<ProjectName>/_context/` and `projects/<ProjectName>/<phase>/<document>/`.

## Quick Reference
- Initialize or refresh `projects/<ProjectName>/_context/` with six templates (vision, features, tech stack, business rules, quality standards, glossary).
- Ensure `projects/<ProjectName>/<phase>/<document>/` exists before downstream IEEE/ISO skills execute.
- Use Maintenance Mode when existing content must stay untouched; use Clean mode only when a fresh baseline is required.

## Anti-Hallucination Guard

> **CRITICAL:** Do NOT generate, invent, or assume any requirements, stakeholder names, features, or system behaviors that are not explicitly present in the `_context/` files. If a context file is empty or a required field is missing, **halt and prompt the consultant to fill it in** rather than making assumptions. Flag every gap with `[CONTEXT-GAP: <file> is missing <field>]`. This engine is a grounding tool, not a generation tool — all content must trace to stakeholder-provided context. *(Derived from hallucination mitigation guidance: Kodukula & Vinueza, 2024)*

## Core Instructions
1. Run `python init_skill.py` from this directory or call the `logic.prompt` via your skill runner.
2. The automation checks for `projects/<ProjectName>/_context/`. Offer Maintenance Mode (add missing templates) or Clean (delete and reseed). Maintenance Mode must never overwrite user edits.
3. After provisioning, create `projects/<ProjectName>/<phase>/<document>/` if missing so downstream skills always find a writeable folder.
4. Copy templates from `templates/`. Each template embeds Expert Guidance comments, SHALL/MUST phrasing, and aligned Markdown tables. Log every directory action and template copy/skip with explicit paths (e.g., `projects/<ProjectName>/_context/vision.md`).
5. After completion, echo: “The quality of the final SRS depends entirely on the technical density of these files. Avoid vague language; provide specific numbers and models.”

## Resources
- `README.md`: Skill description, ISO/IEC alignment, template list, and references.
- `init_skill.py`: Python automation that handles directory checks, Maintenance/Clean mode, template copying, and logging.
- `logic.prompt`: LLM instructions describing the desired behavior, standards references, and logging needs.
- `templates/`: Six industrial templates (`vision.md`, `features.md`, `tech_stack.md`, `business_rules.md`, `quality_standards.md`, `glossary.md`). Each contains Expert Guidance comments and placeholders for measurable data.

## Common Pitfalls
- Re-running the skill without choosing Maintenance Mode can delete effort; prefer Clean only when templates must reset.
- Skipping template population leaves downstream skills without verifiable inputs; ensure the vision, quality, and business rule files contain measurable targets before proceeding.
- Omitting the role-specific acceptance criteria in `quality_standards.md` or glossary definitions undermines ISO/IEC alignment; keep those sections updated with traceable references.

## Worked example

See [`examples/representative/`](examples/representative/).
