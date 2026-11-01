---
name: 01-technical-specification
description: Use when producing or updating implementation-ready technical specification for module contracts, interfaces, data schemas, dependencies, and requirement traceability. Use coding-guidelines for the neighbouring concern; this skill owns the named document contract and its acceptance evidence.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---


# Technical Specification Skill

<!-- dual-compat-start -->
## Use When

- Produce or update implementation-ready technical specification from approved project evidence.
- Resolve decisions about module contracts, interfaces, data schemas, dependencies, and requirement traceability.
- Prepare a reviewable handoff for Implementation team.

## Do Not Use When

- The task is primarily owned by coding-guidelines; route there and use this skill only for its named output.
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
| Implementation-ready Technical Specification | Implementation team | Every in-scope module and interface has a source requirement, deterministic contract, error behaviour, and review owner. |
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
| Evidence is complete and authority is explicit | Choose contract detail from the approved LLD and SRS and produce the full artefact. | Untraceable implementation choices. |
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
- Mixing the neighbouring coding-guidelines concern into this artefact without a boundary. Fix: cross-reference its output and keep ownership explicit.
- Omitting failure, rollback, empty-state, security, tenancy, or escalation behaviour. Fix: specify the trigger, safe action, verification, and owner for each applicable case.
- Mutating a repository, environment, tenant, ledger, or external system while drafting guidance. Fix: remain read-only until the exact mutation and authority are explicit.
- Claiming compliance, certification, readiness, or release from prose alone. Fix: require source-attributed evidence and a named acceptance decision.

## Worked Example

Given an approved project source and a conflicting implementation detail, record both with provenance, stop the affected branch, and obtain the accountable owner's decision. Then update the relevant contract, define a reproducible acceptance check, and retain its observed result. The artefact is accepted only when every in-scope module and interface has a source requirement, deterministic contract, error behaviour, and review owner.

## References

- [Signup Human Validation Requirements](references/signup-human-validation.md) — read when specifying account creation, signup verification, or signup-related resend flows for web and Android clients.

- [logic.prompt](logic.prompt) - load only when its template, logic, or detail is needed.
- [README.md](README.md) - load only when its template, logic, or detail is needed.
<!-- dual-compat-end -->
## Overview

This is the first skill in Phase 04 (Development Artifacts). It transforms the Low-Level Design module decomposition and SRS requirements into an implementation-ready technical specification that defines module contracts, data format schemas, integration specifications, configuration parameters, and dependency matrices. The output serves as the primary reference for developers translating design into code and conforms to IEEE 1016-2009 and IEEE 830-1998.

## When to Use

- After Phase 03 completes and `LLD.md` exists in `projects/<ProjectName>/<phase>/<document>/` with module decomposition and class diagrams.
- When `SRS_Draft.md` is present in `projects/<ProjectName>/<phase>/<document>/` for requirement traceability.
- When `tech_stack.md` is present in `projects/<ProjectName>/_context/` for technology-specific implementation details.

## Quick Reference

| Attribute   | Value |
|-------------|-------|
| **Inputs**  | `projects/<ProjectName>/<phase>/<document>/LLD.md`, `projects/<ProjectName>/<phase>/<document>/SRS_Draft.md`, `projects/<ProjectName>/_context/tech_stack.md` |
| **Output**  | `projects/<ProjectName>/<phase>/<document>/Technical_Specification.md` |
| **Tone**    | Implementation-precise, contract-driven, developer-facing |
| **Standard** | IEEE 1016-2009, ISO/IEC/IEEE 29148:2018 |

## Input Files

| File | Location | Required | Purpose |
|------|----------|----------|---------|
| LLD.md | `projects/<ProjectName>/<phase>/<document>/LLD.md` | Yes | Module decomposition, class diagrams, algorithms to formalize as contracts |
| SRS_Draft.md | `projects/<ProjectName>/<phase>/<document>/SRS_Draft.md` | Yes | Functional requirements for traceability and interface constraints |
| tech_stack.md | `projects/<ProjectName>/_context/tech_stack.md` | Yes | Technology choices, runtime versions, framework-specific implementation details |

## Output Files

| File | Location | Description |
|------|----------|-------------|
| Technical_Specification.md | `projects/<ProjectName>/<phase>/<document>/Technical_Specification.md` | Complete technical specification with module contracts, data formats, and integration specs |

## Core Instructions

Follow these eight steps in order. Halt and notify the user if a required input file is missing.

### Step 1: Read Context Files

Read `LLD.md` and `SRS_Draft.md` from `projects/<ProjectName>/<phase>/<document>/` and `tech_stack.md` from `projects/<ProjectName>/_context/`. Log the absolute path of each file read. If any required file is missing, halt execution and report the gap.

### Step 2: Extract Module Contracts from LLD

For each module defined in LLD.md, extract and formalize the contract:
- **Module Name**: exact identifier from the LLD class diagram
- **Public Interface**: method signatures with typed parameters and return types
- **Preconditions**: input constraints that must hold before invocation
- **Postconditions**: guaranteed state after successful execution
- **Exceptions**: error conditions and corresponding exception types

### Step 3: Define Data Format Specifications

For each data entity exchanged between modules or exposed via APIs, define:
- JSON schema with field names, types, required/optional flags, and constraints
- Database column types with precision (e.g., `DECIMAL(19,4)` for monetary values)
- Enumeration values with definitions for every status or category field

### Step 4: Define Integration Specifications

For each integration point identified in LLD and SRS Section 3.1, define the API contract:
- Endpoint path, HTTP method, and content type
- Request schema with typed parameters and validation rules
- Response schema with status codes and payload structure
- Authentication requirements and rate limits

### Step 5: Define Configuration Parameters

Document every configurable parameter the system requires:
- Parameter name, data type, default value, and valid range
- Environment variable mapping (e.g., `DB_HOST` maps to database connection host)
- Configuration file format and location

### Step 6: Define Dependency Matrix

Produce a module-to-module dependency matrix:
- Source module, target module, dependency type (compile-time, runtime, optional)
- Circular dependency detection: flag any bidirectional dependencies as design issues

### Step 7: Generate Implementation Notes

For each module, provide implementation guidance:
- Recommended design patterns from LLD (e.g., Repository, Strategy, Observer)
- Performance considerations derived from SRS non-functional requirements
- Security considerations derived from SRS Section 3.5

### Step 8: Write Output with Traceability

Write the completed document to `projects/<ProjectName>/<phase>/<document>/Technical_Specification.md`. Include a traceability table mapping every module contract to its LLD module and originating SRS requirement IDs. Log the total count of module contracts, data schemas, and integration specifications.

## Output Format

The generated `Technical_Specification.md` shall contain these sections in order: Document Header (project name, date, version, standards), 1. Introduction and Scope, 2. Module Contracts, 3. Data Format Specifications, 4. Integration Specifications, 5. Configuration Parameters, 6. Dependency Matrix, 7. Implementation Notes, 8. Traceability Matrix, Appendix A: Glossary.

## Common Pitfalls

| Pitfall | Remedy |
|---------|--------|
| Module contracts without preconditions | Every public method shall state input constraints explicitly |
| JSON schemas missing required/optional flags | Every field shall declare whether it is required or optional |
| Integration specs without error responses | Every API contract shall document error status codes and payloads |
| Configuration parameters without defaults | Every parameter shall have a documented default value or be flagged as mandatory |

## Verification Checklist

- [ ] `Technical_Specification.md` exists in `projects/<ProjectName>/<phase>/<document>/` with all eight sections populated.
- [ ] Every LLD module has a corresponding contract with public interface, preconditions, and postconditions.
- [ ] Data format specifications include JSON schemas with typed fields and constraints.
- [ ] Integration specifications document request/response schemas with status codes.
- [ ] Configuration parameters list default values and valid ranges.
- [ ] Dependency matrix flags any circular dependencies.
- [ ] Traceability table maps every module contract to LLD modules and SRS requirement IDs.

## Integration

| Direction | Skill | Relationship |
|-----------|-------|-------------|
| Upstream | Phase 03 (02-low-level-design) | Consumes `LLD.md` module decomposition and class diagrams |
| Upstream | Phase 02 (Requirements Engineering) | Consumes `SRS_Draft.md` for requirement traceability |
| Downstream | 02-coding-guidelines | Informs coding patterns based on module contracts |
| Downstream | Phase 05 (Testing) | Feeds module contracts and integration specs for test derivation |

## Standards

- **IEEE 1016-2009** -- Software Design Descriptions. Governs module contract structure and design viewpoints.
- **ISO/IEC/IEEE 29148:2018** -- Requirements engineering (supersedes IEEE 830-1998). Ensures requirement traceability in the specification.

## Resources

- `logic.prompt` -- Executable prompt containing the step-by-step technical specification generation logic.
- `README.md` -- Quick-start guide for this skill.
