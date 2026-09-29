---
name: 03-dev-environment-setup
description: Use when producing or updating development environment setup guide for repeatable prerequisites, installation, configuration, build, and verification steps. Use deployment-guide for the neighbouring concern; this skill owns the named document contract and its acceptance evidence.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---


# Dev Environment Setup Skill

<!-- dual-compat-start -->
## Use When

- Produce or update development environment setup guide from approved project evidence.
- Resolve decisions about repeatable prerequisites, installation, configuration, build, and verification steps.
- Prepare a reviewable handoff for Developers and support engineers.

## Do Not Use When

- The task is primarily owned by deployment-guide; route there and use this skill only for its named output.
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
| Development Environment Setup Guide | Developers and support engineers | A clean workstation can follow the guide to reach a named passing verification command without undocumented secrets. |
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
- Inspection is read-only by default. Create or edit the named project document only when explicitly authorised. Production mutation, publishing, destructive action, spending, external communication, or certification claims require separate explicit authority.
- Treat secrets, tenant data, incident evidence, and financial records as least-privilege inputs; expose only the minimum evidence needed for review.

## Degraded Mode

If files, execution, network, rendering, environment access, fonts, or current evidence are unavailable, return the narrowest useful draft plus a gap register. Label affected checks `not assessed`, retain the intended acceptance oracle, and state who must supply or verify the missing evidence. Never convert an unavailable check into a pass.

## Decision Rules

| Choice | Action | Failure or risk avoided |
|---|---|---|
| Evidence is complete and authority is explicit | Choose setup paths from supported host platforms and pinned toolchain versions and produce the full artefact. | Non-reproducible local environments. |
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
- Mixing the neighbouring deployment-guide concern into this artefact without a boundary. Fix: cross-reference its output and keep ownership explicit.
- Omitting failure, rollback, empty-state, security, tenancy, or escalation behaviour. Fix: specify the trigger, safe action, verification, and owner for each applicable case.
- Mutating a repository, environment, tenant, ledger, or external system while drafting guidance. Fix: remain read-only until the exact mutation and authority are explicit.
- Claiming compliance, certification, readiness, or release from prose alone. Fix: require source-attributed evidence and a named acceptance decision.

## Worked Example

Given an approved project source and a conflicting implementation detail, record both with provenance, stop the affected branch, and obtain the accountable owner's decision. Then update the relevant contract, define a reproducible acceptance check, and retain its observed result. The artefact is accepted only when a clean workstation can follow the guide to reach a named passing verification command without undocumented secrets.

## References

- [logic.prompt](logic.prompt) - load only when its template, logic, or detail is needed.
- [README.md](README.md) - load only when its template, logic, or detail is needed.
- [System orientation guide](references/system-orientation-guide.md) - load when a new developer needs a reading route into an existing codebase; template in `templates/system-orientation-guide.md`, worked example in `examples/system-orientation-guide-srs-engine.md`.
<!-- dual-compat-end -->
## Overview

This is the third skill in Phase 04 (Development Artifacts). It generates comprehensive development environment setup documentation that enables any developer to establish a working local environment from scratch. The output covers prerequisites, dependency installation, local configuration, build commands, IDE setup, and verification steps, conforming to IEEE 1074 (Software Life Cycle Processes).

## When to Use

- After `tech_stack.md` exists in `projects/<ProjectName>/_context/` with toolchain and runtime details.
- Optionally after `HLD.md` exists in `projects/<ProjectName>/<phase>/<document>/` to derive infrastructure dependencies (databases, caches, message queues).
- Can run in parallel with `02-coding-guidelines` since they address independent concerns.

## Quick Reference

| Attribute   | Value |
|-------------|-------|
| **Inputs**  | `projects/<ProjectName>/_context/tech_stack.md`; optionally `projects/<ProjectName>/<phase>/<document>/HLD.md` |
| **Output**  | `projects/<ProjectName>/<phase>/<document>/Dev_Environment_Setup.md` |
| **Tone**    | Instructional, step-by-step, platform-aware |
| **Standard** | IEEE 1074 |

## Input Files

| File | Location | Required | Purpose |
|------|----------|----------|---------|
| tech_stack.md | `projects/<ProjectName>/_context/tech_stack.md` | Yes | Runtimes, package managers, databases, and infrastructure tools |
| HLD.md | `projects/<ProjectName>/<phase>/<document>/HLD.md` | No | Deployment topology to derive local infrastructure dependencies |

## Output Files

| File | Location | Description |
|------|----------|-------------|
| Dev_Environment_Setup.md | `projects/<ProjectName>/<phase>/<document>/Dev_Environment_Setup.md` | Complete environment setup guide with numbered steps and verification commands |

## Core Instructions

Follow these seven steps in order. Halt and notify the user if a required input file is missing.

### Step 1: Read Context Files

Read `tech_stack.md` from `projects/<ProjectName>/_context/`. Optionally read `HLD.md` from `projects/<ProjectName>/<phase>/<document>/` for infrastructure context. Log the absolute path of each file read. If `tech_stack.md` is missing, halt execution and report the gap.

### Step 2: Define Prerequisites

Document all prerequisites the developer must have before starting:
- Operating system requirements (supported OS versions)
- Runtime versions with exact version numbers (e.g., Node.js 20.x, Python 3.12, Java 21)
- Package managers with minimum versions (e.g., npm 10.x, pip 24.x)
- System-level dependencies (e.g., Git, Docker, Docker Compose)

### Step 3: Define Dependency Installation Steps

Provide numbered, copy-paste-ready installation commands:
- Platform-specific commands (macOS/Homebrew, Windows/winget, Linux/apt)
- Runtime installation via version managers (nvm, pyenv, sdkman)
- Project dependency installation (npm install, pip install -r, mvn install)
- Infrastructure dependencies (database, cache, message queue via Docker Compose)

### Step 4: Define Local Configuration

Document all local configuration required:
- Environment variables with descriptions and example values
- Configuration file templates (`.env.example`, `config.local.yaml`)
- Database setup commands (create database, run migrations, seed data)
- SSL/TLS certificates for local development if applicable

### Step 5: Define Build and Run Commands

Document the complete build and execution workflow:
- Build commands (compile, transpile, bundle)
- Run commands for development mode with hot-reload
- Run commands for production-like mode
- Database migration commands
- Common task runner commands (lint, format, type-check)

### Step 6: Define IDE Setup Recommendations

Provide IDE configuration guidance:
- Recommended IDE or editor with version
- Required extensions or plugins (linter, formatter, debugger)
- Workspace settings (tab size, line endings, encoding)
- Debug configuration templates (launch.json, run configurations)

### Step 7: Write Output with Verification Steps

Write the completed document to `projects/<ProjectName>/<phase>/<document>/Dev_Environment_Setup.md`. Include a Verification Checklist section with commands that confirm each component is correctly installed and configured. Include a Troubleshooting section addressing common setup failures. Log the total count of installation steps and verification checks.

## Output Format

The generated `Dev_Environment_Setup.md` shall contain these sections in order: Document Header (project name, date, version, standard), 1. Prerequisites, 2. Installation Steps (numbered, platform-specific), 3. Configuration, 4. Build and Run, 5. IDE Setup, 6. Verification Checklist, 7. Troubleshooting.

## Common Pitfalls

| Pitfall | Remedy |
|---------|--------|
| Missing exact version numbers | Every runtime and tool shall specify an exact or minimum version number |
| Platform-specific commands without labels | Every command block shall state which OS it targets |
| Environment variables without examples | Every env var shall include an example value and description |
| No verification steps | Every major installation step shall have a verification command |

## Verification Checklist

- [ ] `Dev_Environment_Setup.md` exists in `projects/<ProjectName>/<phase>/<document>/` with all seven sections populated.
- [ ] Prerequisites list exact version numbers for all runtimes and tools.
- [ ] Installation steps provide platform-specific commands for at least two operating systems.
- [ ] Configuration section documents all environment variables with example values.
- [ ] Build and Run section covers development mode, production-like mode, and common tasks.
- [ ] Verification Checklist provides runnable commands to confirm correct setup.
- [ ] Troubleshooting section addresses at least three common setup failures.

## Integration

| Direction | Skill | Relationship |
|-----------|-------|-------------|
| Upstream | `projects/<ProjectName>/_context/tech_stack.md` | Reads toolchain and infrastructure details |
| Parallel | 02-coding-guidelines | Independent concern; can run simultaneously |
| Downstream | 04-contribution-guide | Informs the "Getting Started" section of the contribution guide |
| Downstream | Development teams | Primary onboarding reference for new developers |
| Companion | `references/system-orientation-guide.md` | Explains what the code is and in which order to read it, once this guide has it running |

## Standards

- **IEEE 1074** -- Software Life Cycle Processes. Governs the documentation of development environment and toolchain requirements.

## Resources

- `logic.prompt` -- Executable prompt containing the step-by-step environment setup generation logic.
- `README.md` -- Quick-start guide for this skill.
