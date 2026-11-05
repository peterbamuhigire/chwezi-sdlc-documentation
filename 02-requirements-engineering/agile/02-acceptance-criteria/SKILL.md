---
name: 02-acceptance-criteria
description: "Use when formalising deterministic Given-When-Then acceptance criteria for existing user stories; use user-story-generation when the backlog or personas have not yet been defined."
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---

# Acceptance Criteria Skill Guidance

<!-- local-contract-start -->
<!-- dual-compat-start -->
## Use When

- formalising deterministic Given-When-Then acceptance criteria for existing user stories; use user-story-generation when the backlog or personas have not yet been defined.
- Use this procedure when the required source artefacts are available and `Acceptance-criteria catalogue` is the next lifecycle deliverable.

## Do Not Use When

- Use `user-story-generation` when that neighbouring route owns the decision or deliverable.
- Do not invent missing project evidence, standards clauses, thresholds, or stakeholder decisions.

## Required Inputs

| Artefact | Source or provider | Required? | Behaviour when missing |
| --- | --- | --- | --- |
| Approved user stories, business rules, quality thresholds, and error cases | Product owner, requirements baseline, and domain references | Yes | Stop the affected step, name the missing source, and return only a qualified gap record. |

## Workflow

1. Inspect the required inputs and log the exact sources, versions, and unresolved assumptions.
2. Apply this skill's existing domain workflow and decision rules to produce `Acceptance-criteria catalogue`.
3. Stop when a required source, accountable decision owner, or deterministic test oracle is absent.
4. Recover by preserving valid work, marking the blocked scope, and returning the narrowest qualified artefact plus the next evidence needed.

## Outputs

| Artefact | Consumer | Acceptance condition |
| --- | --- | --- |
| Acceptance-criteria catalogue | Developers, testers, product owner, and traceability owners | Required sections are populated, source links resolve, and every material requirement or decision has an observable review or test oracle. |

## Evidence Produced

| Evidence | Reviewer | Acceptance condition |
| --- | --- | --- |
| Source, decision, trace, and validation record for `Acceptance-criteria catalogue` | Requirements quality reviewer | Inputs used, decisions made, checks run, failures, and unassessed items are explicit. |

## Capability and permission boundaries

Read and search are required. Editing is allowed only when the request authorises creation or repair of the named requirements artefact. Publishing, production mutation, destructive action, spending, and certification require explicit authority.

## Degraded mode

Fallback: if a required file, reviewer, standard source, network check, renderer, or execution capability is unavailable, return the narrowest useful qualified result and mark the affected check `not assessed`; never convert an unassessed check into a pass.

## Decision Rules

| Choice or condition | Action | Failure or risk avoided |
| --- | --- | --- |
| A criterion uses subjective language or lacks an observable result | Rewrite it with explicit precondition, stimulus, result, and boundary. | Disputes caused by non-deterministic acceptance. |
| Required inputs and test oracles are complete | Continue through the existing workflow and record evidence. | A deliverable whose acceptance cannot be reproduced. |
| A mandatory source or owner is missing | Stop the affected branch and issue a qualified gap record. | Fabricated context or unauthorised decisions. |

## Quality Standards

- Preserve stable identifiers and bidirectional traceability from project evidence to `Acceptance-criteria catalogue` and its acceptance checks.
- Apply ISO/IEEE measures only with a named metric, method, threshold, evidence source, and responsible reviewer; run the anti-slop gate before release.

## Anti-Patterns

- Producing `Acceptance-criteria catalogue` from assumed context. Fix: cite the project source or mark the scope blocked.
- Accepting a material requirement without a deterministic oracle. Fix: add a measurable result, boundary, and verification method.
- Crossing into `user-story-generation` without routing the decision. Fix: hand off the named input and preserve trace links.
- Treating an unavailable check as passed. Fix: mark it `not assessed` and state the release consequence.
- Claiming standards, statutory, or stakeholder approval without evidence. Fix: cite the source and reviewer or qualify the claim.

## References

- [Skill authoring and release standard](../../../docs/skill-authoring-standard.md)
- [Skill guidance](README.md)
- [Executable generation logic](logic.prompt)
- [Scenario quality rules](references/scenario-quality-rules.md): load when writing or reviewing Given-When-Then criteria, NFR ranges, or post-delivery scenario filing.
- [Document numbering requirements](../../references/document-numbering-requirements.md): load for stories that issue, void or replay numbered documents; reuse its section 9 criteria.
<!-- dual-compat-end -->
<!-- local-contract-end -->

## Overview

Run this skill after user stories are generated. It transforms each user story produced by `01-user-story-generation` into formal acceptance criteria using the Gherkin (Given-When-Then) format. Every criterion shall be deterministic and independently verifiable, ensuring that test engineers can derive binary pass/fail outcomes without ambiguity. The skill enforces IEEE 29148-2018 Section 6.4.5 traceability between stakeholder intent and testable conditions.

## When to Use

Execute this skill after `01-user-story-generation` has produced `projects/<ProjectName>/<phase>/<document>/user_stories.md`. Each user story in that file shall already follow the "As a / I want / So that" format. This skill shall not run until the upstream file exists and contains at least one valid story identifier (US-XXX).

## Quick Reference

- **Inputs:** `projects/<ProjectName>/<phase>/<document>/user_stories.md` (required), `projects/<ProjectName>/_context/quality_standards.md` (optional, for NFR criteria)
- **Output:** `projects/<ProjectName>/<phase>/<document>/acceptance_criteria.md`
- **Tone:** Precise, testable, deterministic -- no subjective adjectives

## Input Files

| File | Source | Purpose | Required? |
|------|--------|---------|-----------|
| `user_stories.md` | `projects/<ProjectName>/<phase>/<document>/` | User stories with "As a / I want / So that" triads | Yes |
| `quality_standards.md` | `projects/<ProjectName>/_context/` | NFR targets for performance, security, and reliability thresholds | No |

## Output Files

| File | Destination | Contents |
|------|-------------|----------|
| `acceptance_criteria.md` | `projects/<ProjectName>/<phase>/<document>/` | Gherkin-format acceptance criteria cross-referenced to story IDs |

## Core Instructions

1. **Read upstream output.** Open `projects/<ProjectName>/<phase>/<document>/user_stories.md` and log the file path to confirm the read succeeded.
2. **Extract story triads.** For each user story identified by US-XXX, parse the "As a [role]", "I want to [action]", and "So that [value]" triad. Record the story ID, title, and epic association.
3. **Generate Gherkin criteria.** Produce 3--5 acceptance criteria per story using the format: `Given [precondition], When [action], Then [expected result]`. Criteria shall cover:
   - The happy-path scenario (normal successful flow)
   - At least one error or edge-case scenario
   - At least one boundary-condition scenario
   - A **Must not** line where a prohibited side effect exists (see "Must not" field, below)

### Must not — the prohibited-side-effect field

> Source: ECC's `intent-driven-development` skill
> (upstream repository github.com/affaan-m/ECC),
> AC format.

Add a **Must not** field alongside Given/When/Then wherever a criterion has
an observable prohibited side effect — most security and data-isolation
requirements live in this field and have nowhere else to go in a plain
Given/When/Then template. State it as an assertion of absence, not a vague
warning:

```
AC-001: Export generates file with correct headers
- Given: authenticated user, at least one data row visible
- When: user clicks "Export CSV"
- Then: browser downloads file with columns [id, name, created_at]
- Must not: expose internal fields or rows belonging to other users
- Verification: automated integration test + manual schema spot-check
```

Omit the **Must not** line only when a criterion genuinely has no side
effect worth constraining (e.g., a pure read with no cross-tenant or
cross-record exposure risk) — do not pad every criterion with a boilerplate
"must not fail" line. When in doubt whether a side effect is worth naming,
name it; an unnecessary **Must not** line costs nothing, a missing one
hides a security requirement inside a generic template with no slot for it.
4. **Append NFR criteria.** If `projects/<ProjectName>/_context/quality_standards.md` exists, read it and append non-functional acceptance criteria with measurable thresholds (response time, throughput, encryption standard, etc.) to each relevant story.
5. **Flag untestable stories.** If a story cannot yield deterministic, binary pass/fail criteria, tag it with `[AC-FAIL]` and append a remediation note identifying the missing or ambiguous element.
6. **Write output.** Write `projects/<ProjectName>/<phase>/<document>/acceptance_criteria.md` with each story's criteria grouped under its US-XXX identifier, including cross-references back to the originating story and epic.

## Output Format Specification

The generated `acceptance_criteria.md` shall follow this structure:

```markdown
# Acceptance Criteria: [Project Name]

**Generated:** [Date]
**Source:** user_stories.md
**Standard:** IEEE 29148-2018 Sec 6.4.5, Gherkin/BDD Format

---

## US-001: [Story Title]

**Epic:** [Epic Name]
**Story:** As a [role], I want to [action], So that [value]

### Functional Criteria

- [ ] **AC-001.1:** Given [precondition], When [action], Then [expected result]
  - Must not: [prohibited side effect, when applicable]
- [ ] **AC-001.2:** Given [error condition], When [action], Then [error handling result]
  - Must not: [prohibited side effect, when applicable]
- [ ] **AC-001.3:** Given [boundary condition], When [action], Then [boundary result]
  - Must not: [prohibited side effect, when applicable]

### NFR Criteria (if applicable)

- [ ] **AC-001.NFR-1:** Given [load condition], When [action], Then [measurable threshold]

---

## US-002: [Story Title]

[... repeat per story ...]

---

## Summary

| Metric | Value |
|--------|-------|
| Stories Processed | N |
| Total Criteria Generated | N |
| NFR Criteria | N |
| Failures Flagged ([AC-FAIL]) | N |
```

## Common Pitfalls

- **Vague criteria:** Avoid language such as "the system handles it correctly." Each criterion shall state a concrete, observable outcome.
- **Missing negative cases:** Every story shall include at least one error-path criterion. Omitting negative cases leaves validation gaps.
- **Subjective language:** Words like "fast," "intuitive," or "user-friendly" violate IEEE 29148 verifiability. Replace with measurable thresholds.
- **Orphaned criteria:** Every criterion shall trace back to exactly one US-XXX identifier. Criteria without story references shall be flagged.
- **Missing "Must not" on a security- or data-isolation-relevant criterion:** if a criterion touches cross-user data, permissions, exported fields, or financial state and has no **Must not** line, the criterion is incomplete even if Given/When/Then reads cleanly.

## Verification Checklist

Before finalizing the output:

- [ ] Every user story in `user_stories.md` has a corresponding criteria section in `acceptance_criteria.md`
- [ ] Each story has 3--5 acceptance criteria in Gherkin format
- [ ] At least one error/edge-case criterion exists per story
- [ ] At least one boundary-condition criterion exists per story
- [ ] All NFR criteria include measurable, numeric thresholds
- [ ] Stories that lack testable criteria are tagged with `[AC-FAIL]` and include remediation notes
- [ ] Every criterion touching cross-user data, permissions, exported fields, or financial state has a **Must not** line

## Integration

- **Upstream:** `01-user-story-generation` -- provides `user_stories.md`
- **Downstream:** `05-testing-documentation/` -- acceptance criteria become test cases; `03-story-mapping` -- maps criteria coverage across the backlog

## Standards Compliance

This skill implements:

- **IEEE Std 29148-2018** Section 6.4.5: Requirements specification and verifiability
- **Gherkin/BDD Format:** Given-When-Then structure for behavioral specifications
- **IEEE Std 610.12-1990:** Terminology alignment via project glossary

## Resources

- `logic.prompt` -- Direct AI execution instructions for this skill
- `README.md` -- Objective summary and quick-start guide

---

**Last Updated:** 2026-02-28
**Skill Version:** 1.0.0
