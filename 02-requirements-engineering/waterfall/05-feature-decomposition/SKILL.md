---
name: 05-feature-decomposition
description: "Use when decomposing approved scope into traceable capabilities, features, subfeatures, and atomic requirements; use user-story-generation for Agile backlog phrasing."
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---

# Feature Decomposition Skill Guidance

<!-- local-contract-start -->
<!-- dual-compat-start -->
## Use When

- decomposing approved scope into traceable capabilities, features, subfeatures, and atomic requirements; use user-story-generation for Agile backlog phrasing.
- Use this procedure when the required source artefacts are available and `Feature hierarchy and atomic requirement set` is the next lifecycle deliverable.

## Do Not Use When

- Use `user-story-generation` when that neighbouring route owns the decision or deliverable.
- Do not invent missing project evidence, standards clauses, thresholds, or stakeholder decisions.

## Required Inputs

| Artefact | Source or provider | Required? | Behaviour when missing |
| --- | --- | --- | --- |
| Vision, PRD or BRD, system context, models, interfaces, and prioritisation rules | Approved upstream product and requirements artefacts | Yes | Stop the affected step, name the missing source, and return only a qualified gap record. |

## Workflow

1. Inspect the required inputs and log the exact sources, versions, and unresolved assumptions.
2. Apply this skill's existing domain workflow and decision rules to produce `Feature hierarchy and atomic requirement set`.
3. Stop when a required source, accountable decision owner, or deterministic test oracle is absent.
4. Recover by preserving valid work, marking the blocked scope, and returning the narrowest qualified artefact plus the next evidence needed.

## Outputs

| Artefact | Consumer | Acceptance condition |
| --- | --- | --- |
| Feature hierarchy and atomic requirement set | SRS assembly, traceability, architecture, and testing | Required sections are populated, source links resolve, and every material requirement or decision has an observable review or test oracle. |

## Evidence Produced

| Evidence | Reviewer | Acceptance condition |
| --- | --- | --- |
| Source, decision, trace, and validation record for `Feature hierarchy and atomic requirement set` | Requirements quality reviewer | Inputs used, decisions made, checks run, failures, and unassessed items are explicit. |

## Capability and permission boundaries

Read and search are required. Editing is allowed only when the request authorises creation or repair of the named requirements artefact. Publishing, production mutation, destructive action, spending, and certification require explicit authority.

## Degraded mode

Fallback: if a required file, reviewer, standard source, network check, renderer, or execution capability is unavailable, return the narrowest useful qualified result and mark the affected check `not assessed`; never convert an unassessed check into a pass.

## Decision Rules

| Choice or condition | Action | Failure or risk avoided |
| --- | --- | --- |
| A feature mixes independent actors, outcomes, or release decisions | Split it while retaining parent and source trace links. | Requirements too broad to design or test. |
| Required inputs and test oracles are complete | Continue through the existing workflow and record evidence. | A deliverable whose acceptance cannot be reproduced. |
| A mandatory source or owner is missing | Stop the affected branch and issue a qualified gap record. | Fabricated context or unauthorised decisions. |

## Quality Standards

- Preserve stable identifiers and bidirectional traceability from project evidence to `Feature hierarchy and atomic requirement set` and its acceptance checks.
- Apply ISO/IEEE measures only with a named metric, method, threshold, evidence source, and responsible reviewer; run the anti-slop gate before release.

## Anti-Patterns

- Producing `Feature hierarchy and atomic requirement set` from assumed context. Fix: cite the project source or mark the scope blocked.
- Accepting a material requirement without a deterministic oracle. Fix: add a measurable result, boundary, and verification method.
- Crossing into `user-story-generation` without routing the decision. Fix: hand off the named input and preserve trace links.
- Treating an unavailable check as passed. Fix: mark it `not assessed` and state the release consequence.
- Claiming standards, statutory, or stakeholder approval without evidence. Fix: cite the source and reviewer or qualify the claim.

## References

- [Skill authoring and release standard](../../../docs/skill-authoring-standard.md)
- [Skill guidance](README.md)
- [Executable generation logic](logic.prompt)
- [Document numbering requirements](../../references/document-numbering-requirements.md): load for every multi-tenant system that issues numbered documents; supplies the Document Numbering feature and its acceptance stubs.
<!-- dual-compat-end -->
<!-- local-contract-end -->

## Overview
Use this skill after Sections 1.0, 2.0, and 3.1 are generated. It transforms the feature set and quality standards into Section 3.2 (Feature Decomposition), ensuring every functional requirement follows a stimulus/response pattern with a single verifiable "shall" per clause per IEEE 830 Clause 5.3.1.

> **WBS Alignment:** The output of this skill forms the **requirements baseline** equivalent to a WBS Work Package layer (per PMBOK Guide, 7th Ed.): it decomposes scope from Features (Epic level) → Subfunctions (Story level) → Verifiable Requirements (task-level acceptance criteria). Project managers familiar with WBS methodology can use this output directly to populate their WBS dictionary for the requirements scope baseline.

## Quick Reference
- Inputs: `projects/<ProjectName>/_context/features.md`, `projects/<ProjectName>/_context/quality_standards.md`
- Output: `projects/<ProjectName>/<phase>/<document>/SRS_Draft.md` (Section 3.2 only)
- Tone: Technical, precise, employing SHALL statements; avoid subjective adjectives and reference ISO/IEC 25010 Functional Suitability.

## Functional Requirement Template

Every SHALL requirement must include an inline GWT (Given-When-Then) acceptance stub immediately after the requirement statement:

```
**FR-[ID]: [Requirement Title]**
The system shall [verb] [object] when [condition].

**Acceptance:**
- **Given** [precondition — system state before the action]
- **When** [trigger action — exactly one]
- **Then** [observable outcome — externally verifiable]

*Priority: [Must/Should/Could/Won't] | Audience: [End User / Admin / Developer] | Precondition: [System state required before this requirement applies, or "None"]*
```

**GWT Rules (Adzic, 2023):**
- Exactly ONE `When` clause per stub. Two Whens = two requirements.
- `Then` must describe an externally observable state change, not an internal variable.
- `Given` uses past tense (preconditions that existed before the action).
- If the expected result requires judgment to determine pass/fail → tag `[VERIFIABILITY-FAIL: expected result is not a test oracle]`.

**Checklist:**
- [ ] Every SHALL requirement has an inline GWT stub with exactly one When clause
- [ ] Every FR has a Precondition clause (even if "None")
- [ ] Every FR has an [AUDIENCE] tag

## Core Instructions
1. Run `python feature_decomposition.py` from this directory or invoke the `logic.prompt` through your skill runner.
2. Parse each feature entry from `features.md`, extract user story triggers, and build a Functional Decomposition Tree with numbered subsections (3.2.x.1 Description/Priority, 3.2.x.2 Stimulus/Response Sequences, 3.2.x.3 Functional Requirements).
3. Write exactly one "shall" per clause; pair every stimulus with a deterministic response. For each feature, include ALL IEEE 830 §5.3.2 sub-items:
   - Validity checks on inputs (data type, range, format)
   - Exact sequence of operations (numbered processing steps)
   - Responses to abnormal situations (overflow, communication failure, error recovery)
   - Effect of parameters (how configuration alters behavior)
   - Input/output relationships and formulas (LaTeX where applicable)
   - Error handling requirements (independently verifiable)
4. Every requirement MUST have an importance ranking (Essential/Conditional/Optional) per IEEE 830 §4.3.5 and a backward traceability reference `[Source: features.md > Feature Name]` per IEEE 830 §4.3.8.
5. Confirm Section 3.2 references ISO/IEC 25010 Functional Suitability and that each requirement is traceable back to a feature in `features.md`.
6. Reference `../ieee-830-compliance-checklist.md` (ID IEEE830-5.3.2) for compliance verification.
7. For a multi-tenant system that issues document numbers, add a cross-cutting feature subsection "Document Numbering" carrying FR-DOCNUM-001 to FR-DOCNUM-047 from `../../references/document-numbering-requirements.md`, one row per document type from the document type register. A missing register is `[CONTEXT-GAP: document type register]`; omitting the feature needs a recorded waiver.
8. Validate that the updated `SRS_Draft.md` retains Sections 1.0, 2.0, and 3.1 content while replacing or appending Section 3.2.

## Final Step: Write `manifest.md`

After generating all section files, create (or overwrite) `manifest.md` in the SRS document directory (`projects/<ProjectName>/<phase>/<document>/01-srs/`) listing the section files in the correct assembly order:

```markdown
# Document Manifest — SRS Feature Decomposition
# Generated by feature-decomposition. Edit to reorder or exclude sections before building.
01-introduction.md
02-overall-description.md
03-functional-requirements.md
04-nfr.md
05-external-interfaces.md
06-constraints.md
```

This ensures `scripts/build-doc.sh` assembles sections in the intended order rather than alphabetical fallback.

## Resources
- `README.md`: Explains the intent and quality expectation for this skill.
- `feature_decomposition.py`: Automation script that performs parsing, decomposition, and writing of Section 3.2.
- `logic.prompt`: Provides meta instructions for Claude to orchestrate the process.
