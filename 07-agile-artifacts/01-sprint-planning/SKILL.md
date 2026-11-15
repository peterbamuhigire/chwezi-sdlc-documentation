---
name: 01-sprint-planning
description: Use when preparing a sprint goal, evidence-based team capacity, selected backlog, task breakdown, and delivery risks. Use definition-of-ready to admit individual items and definition-of-done to judge completed increments.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Sprint Planning Skill

<!-- dual-compat-start -->

## Use When

- Use when preparing a sprint goal, evidence-based team capacity, selected backlog, task breakdown, and delivery risks. Use definition-of-ready to admit individual items and definition-of-done to judge completed increments.

## Do Not Use When

- Do not use when a more specific upstream or downstream skill owns the task, or when the required project context has not been prepared.
- Do not use this skill to fabricate missing project facts, legal conclusions, test results, approvals, or certification claims.

## Required Inputs

| Artefact | Source or provider | Required? | Missing-input behaviour |
|---|---|---:|---|
| Prioritised product backlog; sprint goal candidate; team availability and recent velocity; Definition of Ready results; dependency and leave calendar | Product owner, delivery team, and approved delivery metrics | Yes | Stop dependent work; name the missing item, owner, and decision impact. A review check remains `not assessed`. |
| Scope, audience, baseline/version, and accountable decision owner | Requester or project context | Yes | Ask for or record the gap; do not infer authority or scope. |

## Capability and permission boundaries

Default to read-only. Read and search access to the supplied artefacts are required. Editing is limited to an explicitly authorised requested draft or project files. Execute validation only when authorised; publishing, signature, certification, production mutation, destructive action, spending, and risk acceptance require explicit authority.

## Degraded Mode

When files, tools, network, rendering, fonts, execution, or evidence are unavailable, return the narrowest useful qualified draft or finding set. Name every unavailable check and its consequence; an unassessed check is never a pass. Preserve evidence already gathered and provide the exact next verification step.

## Decision Rules

| Condition | Action | Failure or risk avoided |
|---|---|---|
| Capacity or dependency evidence is missing | Do not commit the affected item; record the gap and owner | A sprint plan based on fictional capacity |
| Goal and selected items fit measured capacity | Commit the bounded sprint scope | Overcommitment and hidden spillover |

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
| Sprint Planning | Product owner and delivery team | Sprint goal is singular; selected items pass readiness; capacity arithmetic is reproducible; every dependency and risk has an owner. |
| Gap and decision record | Accountable owner and downstream reviewer | Every gap has status, impact, owner, next action, and no unsupported pass or approval. |

## Evidence Produced

| Evidence | Contents | Acceptance condition |
|---|---|---|
| Sprint Planning evidence record | Source identifiers, scope/version, decisions, checks, exceptions, and approval state | A reviewer can reproduce each material conclusion from named sources. |
| Validation record | Check, result (`pass`, `fail`, or `not assessed`), evidence location, date, and actor | No required check is omitted or silently treated as passed. |

## Quality Standards

- Keep outputs grounded in source context, traceable to stated standards, and specific enough to review or verify.
- Use deterministic acceptance conditions and preserve traceability from source to decision and output.
- Separate facts, inferences, assumptions, and approvals; never present one as another.
- Apply `28-anti-ai-slop` during authoring and `29-ai-slop-audit` at major checkpoints and release.

## Anti-Patterns

- **Producing Sprint Planning from assumptions instead of named project sources.** Fix: Cite the source or mark the item unverified.
- **Treating a missing or inaccessible check as passed.** Fix: Mark it `not assessed`, state impact, and block dependent claims.
- **Using vague gates such as `adequate`, `secure`, or `user-friendly`.** Fix: Replace each with an observable criterion, threshold, and evidence source.
- **Copying a generic template without product, control, role, version, or jurisdiction detail.** Fix: Ground every section in the supplied context and remove unused boilerplate.
- **Publishing, signing, certifying, changing production, or accepting risk without authority.** Fix: Prepare a draft and route the decision to the accountable owner.
- **Listing evidence without provenance or an acceptance result.** Fix: Record source, period, integrity check, mapping, and pass/fail/not-assessed status.

## Worked Example

Example: if capacity or dependency evidence is missing, do not commit the affected item; record the gap and owner. Record the evidence and result in the validation record; this avoids a sprint plan based on fictional capacity.

## References

- [Resumable execution contract](../../rules/common/resumable-execution-contract.md): use when breaking selected work into executable, dependency-ordered slices and preparing a resumable handoff.

- [Generation logic](logic.prompt): load when creating the complete artefact.
- [Skill notes](README.md): consult for local examples and invocation context.
- [Repository operating rules](../../AGENTS.md): apply the engine's routing, evidence, and release gates.

<!-- dual-compat-end -->

## Overview

This skill produces a reusable sprint planning template that structures the sprint planning ceremony. It defines the sprint goal, team capacity calculation, backlog item selection criteria, task breakdown format, risk and dependency tracking, and a definition of done reference. The output conforms to the Scrum Guide and IEEE 29148 for requirements traceability.

## When to Use This Skill

- After Phase 02 completes and `prioritized_backlog.md` exists in `projects/<ProjectName>/<phase>/<document>/` with ranked work items.
- When `user_stories.md` is present in `projects/<ProjectName>/<phase>/<document>/` with acceptance criteria for candidate stories.
- When `vision.md` is present in `projects/<ProjectName>/_context/` with project goals to derive sprint goals from.
- At the start of each sprint cycle to produce a fresh planning artifact.

## Quick Reference

| Attribute   | Value |
|-------------|-------|
| **Inputs**  | `projects/<ProjectName>/_context/vision.md`, `projects/<ProjectName>/<phase>/<document>/prioritized_backlog.md`, `projects/<ProjectName>/<phase>/<document>/user_stories.md` |
| **Output**  | `projects/<ProjectName>/<phase>/<document>/Sprint_Planning_Template.md` |
| **Standard** | Scrum Guide, IEEE 29148 |
| **Time**    | 10-15 minutes |

## Input Files

| File | Location | Required | Purpose |
|------|----------|----------|---------|
| vision.md | `projects/<ProjectName>/_context/vision.md` | Yes | Project goals and strategic objectives for sprint goal derivation |
| prioritized_backlog.md | `projects/<ProjectName>/<phase>/<document>/prioritized_backlog.md` | Yes | Ranked backlog items with priority and estimated effort |
| user_stories.md | `projects/<ProjectName>/<phase>/<document>/user_stories.md` | No | User stories with acceptance criteria for task breakdown |

## Output Files

| File | Location | Description |
|------|----------|-------------|
| Sprint_Planning_Template.md | `projects/<ProjectName>/<phase>/<document>/Sprint_Planning_Template.md` | Complete sprint planning template with all ceremony sections |

## Core Instructions

Follow these seven steps in order. Halt and notify the user if a required input file is missing.

### Step 1: Read Context Files

Read `vision.md` from `projects/<ProjectName>/_context/` and `prioritized_backlog.md` from `projects/<ProjectName>/<phase>/<document>/`. Optionally read `user_stories.md` from `projects/<ProjectName>/<phase>/<document>/`. Log the absolute path of each file read. Halt if any required file is missing.

### Step 2: Define Sprint Goal Section

Generate a sprint goal template that SHALL:
- Derive the goal from project vision objectives in `vision.md`.
- State the goal as a single sentence describing the increment value.
- Include a "Goal Rationale" field linking the goal to a business objective.
- Provide a "Success Criteria" checklist for goal completion.

### Step 3: Define Team Capacity Section

Generate a capacity calculation template that SHALL:
- List each team member with available days in the sprint.
- Account for planned time off, ceremonies, and non-sprint overhead.
- Calculate total available story points or hours.
- Include a capacity formula: $Capacity = AvailableDays \times FocusFactor \times HoursPerDay$.

### Step 4: Define Selected Backlog Items Section

Generate a backlog selection table that SHALL:
- Pull candidate items from `prioritized_backlog.md` by priority order.
- Include columns for ID, title, priority, estimate, and acceptance criteria reference.
- Track cumulative effort against team capacity.
- Flag items that exceed remaining capacity.

### Step 5: Define Task Breakdown Section

Generate a task breakdown template that SHALL:
- Decompose each selected backlog item into implementation tasks.
- Assign each task an estimated duration in hours.
- Identify task dependencies within and across stories.
- Include columns for task ID, description, assignee, estimate, and status.

### Step 6: Define Sprint Risks and Dependencies Section

Generate a risk and dependency tracking section that SHALL:
- List known risks with probability, impact, and mitigation strategy.
- Identify external dependencies with owner and expected resolution date.
- Include a blocked-items tracker for impediments surfaced during planning.

### Step 7: Assemble and Write Output

Assemble all sections into the final template. Include a Definition of Done reference section that points to `Definition_of_Done.md`. Include a Sprint Commitment section for the team to record their commitment. Write the completed document to `projects/<ProjectName>/<phase>/<document>/Sprint_Planning_Template.md`. Log completion.

## Output Format Specification

The generated `Sprint_Planning_Template.md` SHALL contain these sections in order:

1. **Document Header** -- project name, sprint number, date range, standards reference
2. **Sprint Goal** -- goal statement, rationale, success criteria
3. **Team Capacity** -- member availability, capacity calculation, total capacity
4. **Selected Backlog Items** -- prioritized items table with cumulative effort
5. **Task Breakdown** -- decomposed tasks per backlog item
6. **Sprint Risks & Dependencies** -- risk register and dependency tracker
7. **Definition of Done Reference** -- pointer to DoD artifact
8. **Sprint Commitment** -- team sign-off section

## Common Pitfalls

- Sprint goal stated as a task list instead of a value statement -- the goal SHALL describe the increment value, not the work performed.
- Capacity calculated without accounting for ceremonies and overhead -- the template SHALL deduct non-coding time from available hours.
- Backlog items selected beyond capacity -- the template SHALL flag items that exceed remaining capacity.
- Task breakdown missing dependency identification -- every task SHALL note upstream dependencies.
- No risk tracking -- every sprint plan SHALL include at least a risk placeholder section.

## Verification Checklist

1. `Sprint_Planning_Template.md` exists in `projects/<ProjectName>/<phase>/<document>/` with all eight sections populated.
2. Sprint goal is a single value statement with rationale linked to a business objective.
3. Capacity calculation includes the formula and accounts for non-sprint overhead.
4. Selected backlog items table includes cumulative effort tracking.
5. Task breakdown decomposes each selected item into estimated tasks.
6. Risk and dependency section includes probability, impact, and mitigation fields.
7. Definition of Done reference points to `Definition_of_Done.md`.
8. Sprint commitment section provides a team sign-off area.

## Integration

| Direction | Skill | Relationship |
|-----------|-------|-------------|
| Upstream | Phase 02 (backlog, user stories) | Consumes `prioritized_backlog.md` and `user_stories.md` |
| Downstream | 02-definition-of-done | Sprint plan references the DoD artifact |
| Downstream | Phase 05 (test planning) | Sprint scope informs test plan scope |
| Downstream | Phase 09 (governance) | Sprint artifacts feed governance audit trail |

## Standards Compliance

- **Scrum Guide** -- Governs sprint planning ceremony structure, sprint goal definition, and team commitment.
- **IEEE 29148** -- Governs requirements traceability from backlog items through task decomposition.

## Resources

- `logic.prompt` -- Executable prompt containing the step-by-step sprint planning generation logic.
- `README.md` -- Quick-start guide for this skill.
