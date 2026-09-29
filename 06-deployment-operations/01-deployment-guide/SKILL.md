---
name: 01-deployment-guide
description: Use when producing or updating deployment guide for release prerequisites, migration choreography, verification, rollback, and ownership. Use runbook for the neighbouring concern; this skill owns the named document contract and its acceptance evidence.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---


# Deployment Guide Skill

<!-- dual-compat-start -->
## Use When

- Produce or update deployment guide from approved project evidence.
- Resolve decisions about release prerequisites, migration choreography, verification, rollback, and ownership.
- Prepare a reviewable handoff for Release engineers and operators.

## Do Not Use When

- The task is primarily owned by runbook; route there and use this skill only for its named output.
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
| Deployment Guide | Release engineers and operators | An authorised operator can deploy and roll back using versioned commands, named gates, and observable health checks. |
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
| Evidence is complete and authority is explicit | Choose the release path from environment risk and migration reversibility and produce the full artefact. | An irreversible release without rollback evidence. |
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
- Mixing the neighbouring runbook concern into this artefact without a boundary. Fix: cross-reference its output and keep ownership explicit.
- Omitting failure, rollback, empty-state, security, tenancy, or escalation behaviour. Fix: specify the trigger, safe action, verification, and owner for each applicable case.
- Mutating a repository, environment, tenant, ledger, or external system while drafting guidance. Fix: remain read-only until the exact mutation and authority are explicit.
- Claiming compliance, certification, readiness, or release from prose alone. Fix: require source-attributed evidence and a named acceptance decision.

## Worked Example

Given an approved project source and a conflicting implementation detail, record both with provenance, stop the affected branch, and obtain the accountable owner's decision. Then update the relevant contract, define a reproducible acceptance check, and retain its observed result. The artefact is accepted only when an authorised operator can deploy and roll back using versioned commands, named gates, and observable health checks.

## References

- [logic.prompt](logic.prompt) - load only when its template, logic, or detail is needed.
- [README.md](README.md) - load only when its template, logic, or detail is needed.
- [references/delivery-pipeline-requirements.md](references/delivery-pipeline-requirements.md) - load when the guide or SRS must state verifiable requirements for artifact identity, provenance, pipeline credentials, rollout abort criteria, reversal time, IaC changes, or DORA delivery metrics.
<!-- dual-compat-end -->
## Overview

This is the first skill in Phase 06 (Deployment & Operations). It produces a comprehensive deployment guide that defines pre-deployment checklists, numbered deployment steps with exact commands, database migration procedures, environment-specific configuration, rollback procedures, and post-deployment verification. The output conforms to IEEE 1062 (Software Acquisition) and serves as the authoritative deployment reference for operations teams.

## When to Use

- After Phase 03 completes and `HLD.md` exists in `projects/<ProjectName>/<phase>/<document>/` with system architecture and component topology.
- When `tech_stack.md` is present in `projects/<ProjectName>/_context/` with technology choices and runtime versions.
- Optionally when `Database_Design.md` exists in `projects/<ProjectName>/<phase>/<document>/` for database migration steps.

## Quick Reference

| Attribute   | Value |
|-------------|-------|
| **Inputs**  | `projects/<ProjectName>/<phase>/<document>/HLD.md`, `projects/<ProjectName>/_context/tech_stack.md`, `projects/<ProjectName>/<phase>/<document>/Database_Design.md` (optional) |
| **Output**  | `projects/<ProjectName>/<phase>/<document>/Deployment_Guide.md` |
| **Tone**    | Procedural, precise, operations-facing |
| **Standard** | IEEE 1062 |

## Input Files

| File | Location | Required | Purpose |
|------|----------|----------|---------|
| HLD.md | `projects/<ProjectName>/<phase>/<document>/HLD.md` | Yes | System architecture, component topology, deployment targets |
| tech_stack.md | `projects/<ProjectName>/_context/tech_stack.md` | Yes | Technology choices, runtime versions, package managers |
| Database_Design.md | `projects/<ProjectName>/<phase>/<document>/Database_Design.md` | No | Database schema for migration step generation |

## Output Files

| File | Location | Description |
|------|----------|-------------|
| Deployment_Guide.md | `projects/<ProjectName>/<phase>/<document>/Deployment_Guide.md` | Complete deployment procedure with pre-checks, steps, rollback, and verification |

## Core Instructions

Follow these eight steps in order. Halt and notify the user if a required input file is missing.

### Step 1: Read Context Files

Read `HLD.md` from `projects/<ProjectName>/<phase>/<document>/` and `tech_stack.md` from `projects/<ProjectName>/_context/`. Optionally read `Database_Design.md` from `projects/<ProjectName>/<phase>/<document>/`. Log the absolute path of each file read. Halt if any required file is missing.

### Step 2: Define Pre-Deployment Checklist

Document every action that shall occur before deployment begins:
- Database backup verification (method, location, retention)
- Stakeholder notification (who, channel, timing)
- Maintenance window scheduling (duration estimate, approval)
- Dependency verification (external services, third-party APIs)
- Artifact readiness (build artifacts, container images, checksums)
- For Ugandan government/local-government/public-entity/NGO/donor-funded clients, add procurement and fiscal pre-checks: the contract is signed (and Solicitor-General-cleared where applicable), the Contracts Committee award stands, the funding instrument (warrant/release or signed grant tranche) and uncommitted quarterly balance are confirmed, and the cutover window avoids financial-year close, board-of-survey, and audit blackout periods. A cutover SHALL NOT precede these sign-offs. See `09-governance-compliance/05-formal-review-gates/references/uganda-public-sector-and-ngo-delivery-constraints.md`; the finance engine (`chwezi-accounting-doctrine`) is the authority for the substance, and no statutory threshold is fixed as current.

### Step 3: Define Deployment Steps

Produce numbered deployment steps with exact commands where the tech stack permits:
- Service shutdown or traffic drain sequence
- Artifact deployment (copy, pull, install)
- Service startup sequence with dependency ordering
- Each step shall include expected duration and success criteria
- For DevOps-ready systems, specify whether deployment is rolling, blue-green, canary, dark-launch, or GitOps-driven; state why that pattern fits the release risk.
- For PHP systems, include Composer install mode, environment file handling, PHP-FPM reload/restart, OPcache reset or warm-up, queue worker restart, cache clear/warm, web server reload, and file ownership checks.

### Step 4: Define Database Migration Steps

If `Database_Design.md` is present, define migration steps:
- Migration script execution order
- Data transformation steps
- Schema validation after migration
- If no database design exists, state that this section is not applicable

### Step 5: Define Configuration Changes per Environment

Document configuration differences across environments:
- Dev, Staging, and Production environment variables
- Feature flags and toggles per environment
- External service endpoints per environment (API URLs, credentials references)

### Step 6: Define Rollback Procedure

Provide step-by-step reversal instructions:
- Decision criteria for triggering rollback
- Service rollback sequence (reverse of deployment order)
- Database rollback (restore from backup or reverse migration)
- Configuration rollback
- Verification that rollback restored previous state

### Step 7: Define Post-Deployment Verification

Document verification procedures after deployment completes:
- Health check endpoints and expected responses
- Smoke test scenarios (critical user paths)
- Performance baseline comparison
- Log review checklist (error rates, warnings)
- Release markers in logs, metrics, and traces so incidents can be tied to the deployed version.
- Actionable alert checks for error rate, latency, saturation, queue depth, failed jobs, and business-critical transactions.

### Step 8: Define Environment Matrix and Write Output

Produce an environment matrix summarizing resource differences across dev/staging/prod. Write the completed document to `projects/<ProjectName>/<phase>/<document>/Deployment_Guide.md`. Log the total count of deployment steps and rollback steps.

## Output Format

The generated `Deployment_Guide.md` shall contain these sections in order: Document Header (project name, date, version, standards), 1. Pre-Deployment Checklist, 2. Deployment Steps, 3. Database Migrations, 4. Configuration, 5. Rollback Procedure, 6. Post-Deployment Verification, 7. Environment Matrix.

## Common Pitfalls

| Pitfall | Remedy |
|---------|--------|
| Deployment steps without exact commands | Every step shall include the literal command or action to execute |
| Missing rollback procedure | Every deployment guide shall include a complete reversal procedure |
| No environment differentiation | Configuration shall distinguish dev, staging, and prod explicitly |
| Post-deployment verification omitted | Every guide shall define health checks and smoke tests |
| Rollback ignores data and queues | Classify migrations as reversible, compensating-only, or forward-fix-only; include cache and queue recovery |

## Verification Checklist

- [ ] `Deployment_Guide.md` exists in `projects/<ProjectName>/<phase>/<document>/` with all seven sections populated.
- [ ] Pre-deployment checklist includes backup verification and stakeholder notification.
- [ ] Deployment steps are numbered with exact commands and expected durations.
- [ ] Rollback procedure reverses every deployment step.
- [ ] Post-deployment verification defines health checks and smoke tests.
- [ ] Environment matrix covers dev, staging, and production.
- [ ] Release markers, alert watch list, and observation owner are specified for production changes.

## Integration

| Direction | Skill | Relationship |
|-----------|-------|-------------|
| Upstream | Phase 03 (01-high-level-design) | Consumes `HLD.md` for system architecture and component topology |
| Upstream | Phase 04 (01-technical-specification) | Consumes tech specs for deployment context |
| Downstream | 02-runbook | Informs incident response with deployment context |
| Downstream | 04-infrastructure-docs | Feeds deployment topology into infrastructure documentation |

## Standards

- **IEEE 1062** -- Recommended Practice for Software Acquisition. Governs deployment procedure structure and acceptance criteria.

## Resources

- `logic.prompt` -- Executable prompt containing the step-by-step deployment guide generation logic.
- `README.md` -- Quick-start guide for this skill.
