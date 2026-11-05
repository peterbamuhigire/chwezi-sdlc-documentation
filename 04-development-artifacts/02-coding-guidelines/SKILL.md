---
name: 02-coding-guidelines
description: Use when producing or updating project coding guidelines for language and framework conventions, enforceable checks, examples, and exceptions. Use technical-specification for the neighbouring concern; this skill owns the named document contract and its acceptance evidence.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---


# Coding Guidelines Skill

<!-- dual-compat-start -->
## Use When

- Produce or update project coding guidelines from approved project evidence.
- Resolve decisions about language and framework conventions, enforceable checks, examples, and exceptions.
- Prepare a reviewable handoff for Developers and reviewers.

## Do Not Use When

- The task is primarily owned by technical-specification; route there and use this skill only for its named output.
- Required project evidence or decision authority is unavailable and the requester expects a pass, release, certification, or production change.

## Required Inputs

| Artefact | Source/provider | Required? | Behaviour when absent |
|---|---|---|---|
| Project _context/, approved requirements, and relevant architecture | Project owner and upstream phase skills | Required | Stop at a gap register; do not invent scope, thresholds, integrations, or owners. |
| Existing artefact, implementation, configuration, and evidence named below | Repository, delivery team, or service owner | Required when updating or assessing | Mark inaccessible items `not assessed`; do not treat them as passed. |
| Target audience, environment, risk tolerance, and authority | Requester and accountable owner | Required | Produce a read-only outline with explicit assumptions; do not mutate project or production state. |
## Outputs

| Artefact | Consumer | Observable acceptance condition |
|---|---|---|
| Project Coding Guidelines | Developers and reviewers | Every mandatory rule maps to a configured check or an explicit review step, with project-language examples. |
| Decision and gap register | Reviewer and downstream phase owner | Every assumption, rejected option, unresolved dependency, waiver, and owner is explicit. |
| Validation evidence | Release or governance reviewer | Checks identify command or method, date, result, evidence location, and all unassessed items. |

## Evidence Produced

| Evidence | Minimum content | Acceptance |
|---|---|---|
| Traceability record | Source artefact, decision, output section, owner | No mandatory decision is source-free. |
| Quality-gate result | Check, expected result, observed result, evidence path | Failures and unavailable checks cannot appear as passes. |
| Review record | Reviewer, date, disposition, open actions | The consumer can reproduce the acceptance decision. |

## Capability and Permission Boundaries

- Minimum capabilities: read and search the authorised project sources. Execution is optional and limited to non-destructive validation.
- Assessment and planning default to read-only. Create or edit the named project document only when the request explicitly authorises it. Production mutation, publishing, destructive action, spending, external communication, or certification claims require separate explicit authority.
- Treat secrets, tenant data, incident evidence, and financial records as least-privilege inputs; expose only the minimum evidence needed for review.

## Degraded Mode

If files, execution, network, rendering, environment access, fonts, or current evidence are unavailable, return the narrowest useful draft plus a gap register. Label affected checks `not assessed`, retain the intended acceptance oracle, and state who must supply or verify the missing evidence. Never convert an unavailable check into a pass.

## Decision Rules

| Choice | Action | Failure or risk avoided |
|---|---|---|
| Evidence is complete and authority is explicit | Choose rules supported by the declared stack and architecture and produce the full artefact. | Generic rules that cannot be enforced. |
| A required source or approval is missing | Stop the affected branch; record the gap, owner, and unblock condition. | Fabricated requirements or unauthorised action. |
| Evidence conflicts across sources | Preserve both claims, identify the controlling owner, and request a recorded decision. | Silent selection of a convenient but wrong source. |
| A check cannot run in the available environment | Keep its oracle and mark it `not assessed`; require later execution evidence. | False assurance from capability limits. |

## Workflow

1. Confirm the named deliverable, consumer, scope, environment, authority, and neighbouring-skill boundary.
2. Inventory required sources and validate provenance, freshness, internal consistency, and missing inputs. Stop the affected branch on a mandatory gap.
3. Extract traceable requirements, invariants, risks, and measurable acceptance criteria; record conflicts before choosing a design or procedure.
4. Apply the decision rules and the domain workflow below. For a failed branch, preserve evidence, choose the documented recovery path, or escalate to the named owner.
5. Draft the artefact, decision register, and evidence record together. Do not defer failure handling, rollback, security, tenancy, accessibility, or operational ownership.
6. Run available checks, review every result, repair failures, and hand off only when acceptance is observable. If recovery fails or authority is exceeded, stop and escalate without mutation.

## Quality Standards

- Ground every section in a named project source, decision, measured result, or accountable owner.
- Give each requirement or procedure a deterministic oracle that another reviewer can reproduce.
- Keep assumptions, exclusions, degraded checks, residual risks, and waivers visible at handoff.
- Preserve the domain invariants and more specific controls in the existing workflow below; this contract does not replace them.
- Run the repository anti-AI-slop gate: remove filler, verify named standards and dependencies, and retain purposeful domain detail.

## Anti-Patterns

- Copying a generic template without mapping it to project sources. Fix: attach each section to an approved requirement, configuration, risk, or owner.
- Choosing a threshold because it is common practice. Fix: derive it from a requirement, measured baseline, risk decision, or current verified source.
- Reporting an inaccessible or unexecuted check as passed. Fix: mark it `not assessed`, preserve the oracle, and name the verifier.
- Mixing the neighbouring technical-specification concern into this artefact without a boundary. Fix: cross-reference its output and keep ownership explicit.
- Omitting failure, rollback, empty-state, security, tenancy, or escalation behaviour. Fix: specify the trigger, safe action, verification, and owner for each applicable case.
- Mutating a repository, environment, tenant, ledger, or external system while drafting guidance. Fix: remain read-only until the exact mutation and authority are explicit.
- Claiming compliance, certification, readiness, or release from prose alone. Fix: require source-attributed evidence and a named acceptance decision.

## Worked Example

Given an approved project source and a conflicting implementation detail, record both with provenance, stop the affected branch, and obtain the accountable owner's decision. Then update the relevant contract, define a reproducible acceptance check, and retain its observed result. The artefact is accepted only when every mandatory rule maps to a configured check or an explicit review step, with project-language examples.

## References

- [logic.prompt](logic.prompt) - load only when its template, logic, or detail is needed.
- [README.md](README.md) - load only when its template, logic, or detail is needed.
<!-- dual-compat-end -->
> **SaaS mode:** if the project is a multi-tenant SaaS, apply `references/saas-multi-tenant-coding-guidelines-addendum.md` in addition to the generic steps below.


## Overview

This is the second skill in Phase 04 (Development Artifacts). It generates language-specific coding standards that establish naming conventions, code structure patterns, anti-patterns to avoid, error handling conventions, and code quality metrics. The output ensures consistent, maintainable code across the development team and conforms to IEEE 730 (Software Quality Assurance Plans).

## When to Use

- After `tech_stack.md` exists in `projects/<ProjectName>/_context/` with language and framework details.
- Optionally after `HLD.md` exists in `projects/<ProjectName>/<phase>/<document>/` to align coding patterns with architectural decisions.
- Can run in parallel with `03-dev-environment-setup` since they address independent concerns.

## Quick Reference

| Attribute   | Value |
|-------------|-------|
| **Inputs**  | `projects/<ProjectName>/_context/tech_stack.md`; optionally `projects/<ProjectName>/<phase>/<document>/HLD.md` |
| **Output**  | `projects/<ProjectName>/<phase>/<document>/Coding_Guidelines.md` |
| **Tone**    | Prescriptive, example-driven, enforceable |
| **Standard** | IEEE 730 |

## Input Files

| File | Location | Required | Purpose |
|------|----------|----------|---------|
| tech_stack.md | `projects/<ProjectName>/_context/tech_stack.md` | Yes | Languages, frameworks, and tooling to derive conventions from |
| HLD.md | `projects/<ProjectName>/<phase>/<document>/HLD.md` | No | Architectural patterns to align coding conventions with |

## Output Files

| File | Location | Description |
|------|----------|-------------|
| Coding_Guidelines.md | `projects/<ProjectName>/<phase>/<document>/Coding_Guidelines.md` | Complete coding standards document with conventions, patterns, and quality metrics |

## Core Instructions

Follow these seven steps in order. Halt and notify the user if a required input file is missing.

### Step 1: Read Context Files

Read `tech_stack.md` from `projects/<ProjectName>/_context/`. Optionally read `HLD.md` from `projects/<ProjectName>/<phase>/<document>/`. Log the absolute path of each file read. If `tech_stack.md` is missing, halt execution and report the gap.

### Step 2: Define Naming Conventions

For each language and framework detected in `tech_stack.md`, define naming conventions:
- **Files**: naming pattern, casing (kebab-case, PascalCase, snake_case), suffix rules
- **Classes/Components**: casing, prefix/suffix conventions (e.g., `Service`, `Controller`, `Repository`)
- **Functions/Methods**: casing, verb-first naming (e.g., `getUser`, `calculateTotal`)
- **Variables**: casing, descriptive naming rules, abbreviation policy
- **Database Columns**: casing (snake_case), naming patterns for foreign keys, timestamps, and flags
- **Constants**: UPPER_SNAKE_CASE with grouping conventions

### Step 3: Define Code Structure Patterns

Define the project directory layout and module organization:
- Top-level directory structure with purpose annotations
- Module boundary rules (what belongs in each layer)
- File length and function length guidelines with specific thresholds
- Import ordering conventions

### Step 4: Define Anti-Patterns to Avoid

Document specific anti-patterns with explanations:
- Code smells to reject in code review (e.g., God classes, deep nesting, magic numbers)
- Framework-specific anti-patterns (e.g., direct DOM manipulation in React, N+1 queries in ORMs)
- Security anti-patterns (e.g., string concatenation for SQL, hardcoded credentials)

### Step 5: Define Error Handling Conventions

Establish error handling standards:
- Exception hierarchy aligned with the LLD error handling design
- Try-catch scope rules (narrow catches, no empty catch blocks)
- Error message format standards (structured, loggable, user-safe)
- Async error handling patterns (Promise rejection, callback error-first)

### Step 6: Define Logging and Debugging Standards

Establish logging conventions:
- Log levels (DEBUG, INFO, WARN, ERROR, FATAL) with usage criteria
- Structured log format (JSON with timestamp, level, correlation ID, message)
- Sensitive data redaction rules (mask PII, credentials, tokens)
- Debug tooling recommendations aligned with tech stack

### Step 6a (optional): Define AI Assistant Use

If the requester or `tech_stack.md` states that the team uses AI coding assistants, apply `references/ai-assistant-use-section.md`: write section 9 with elements AU-1 to AU-8 and apply its checklist by hand. If it is unknown whether the team uses an assistant, record `[CONTEXT-GAP: assistant use]` and omit section 9. For the coding guidelines of an AI-agent product, route to `05-ai-agent-coding-guidelines-addendum` instead; section 9 governs the team's own use of assistants, not the product.

### Step 7: Write Output

Write the completed document to `projects/<ProjectName>/<phase>/<document>/Coding_Guidelines.md`. The document shall include a Code Review Checklist section that summarizes all conventions as a reviewable checklist. Log the total count of conventions defined.

## Output Format

The generated `Coding_Guidelines.md` shall contain these sections in order: Document Header (project name, date, version, standard), 1. Naming Conventions, 2. Code Structure, 3. Design Patterns to Use, 4. Anti-Patterns to Avoid, 5. Error Handling, 6. Logging, 7. Security Practices, 8. Code Review Checklist. When Step 6a applies, the document also contains 9. AI Assistant Use, after the Code Review Checklist.

## Common Pitfalls

| Pitfall | Remedy |
|---------|--------|
| Generic conventions not tied to tech stack | Every convention shall reference the specific language or framework it applies to |
| No concrete examples | Every naming convention shall include a compliant and non-compliant example |
| Anti-patterns without alternatives | Every anti-pattern shall include the recommended alternative approach |
| Missing security practices | Security conventions shall address injection prevention, authentication handling, and data sanitization |
| Section 9 added to the guidelines of an AI-agent product, or omitted for a team that uses assistants | Route an AI-agent product to `05-ai-agent-coding-guidelines-addendum`; add section 9 only for the team's own use of assistants (`references/ai-assistant-use-section.md`, section 1) |

## Verification Checklist

- [ ] `Coding_Guidelines.md` exists in `projects/<ProjectName>/<phase>/<document>/` with all eight sections populated.
- [ ] Naming conventions cover files, classes, functions, variables, database columns, and constants.
- [ ] Anti-patterns include framework-specific items derived from `tech_stack.md`.
- [ ] Error handling conventions define an exception hierarchy and message format.
- [ ] Logging standards define structured format with redaction rules for sensitive data.
- [ ] Code Review Checklist summarizes all conventions as reviewable items.
- [ ] When section 9 is present, elements AU-1 to AU-8 each pass the hand-applied checklist in `references/ai-assistant-use-section.md`, and the reviewer and date are recorded.

## Integration

| Direction | Skill | Relationship |
|-----------|-------|-------------|
| Upstream | `projects/<ProjectName>/_context/tech_stack.md` | Reads language and framework details |
| Parallel | 03-dev-environment-setup | Independent concern; can run simultaneously |
| Downstream | 04-contribution-guide | Informs code review checklist and PR standards |
| Downstream | Phase 05 (Testing) | Informs test naming and test structure conventions |

## Standards

- **IEEE 730** -- Software Quality Assurance Plans. Governs the definition of coding standards and quality practices.

## Resources

- `logic.prompt` -- Executable prompt containing the step-by-step coding guidelines generation logic.
- `README.md` -- Quick-start guide for this skill.
