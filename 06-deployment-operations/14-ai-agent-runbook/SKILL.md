---
name: 14-ai-agent-runbook
description: Use when producing or updating AI-agent operations runbook for agent health, pauses, retries, replay, tool failures, containment, and operator authority. Use incident-response-runbook for the neighbouring concern; this skill owns the named document contract and its acceptance evidence.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---


# AI Agent Runbook Skill

<!-- dual-compat-start -->
## Use When

- Produce or update AI-agent operations runbook from approved project evidence.
- Resolve decisions about agent health, pauses, retries, replay, tool failures, containment, and operator authority.
- Prepare a reviewable handoff for AI operations and SRE.

## Do Not Use When

- The task is primarily owned by incident-response-runbook; route there and use this skill only for its named output.
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
| AI-agent Operations Runbook | AI operations and SRE | Every operator action has an authority check, observable precondition, safe execution step, verification, and audit evidence. |
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
| Evidence is complete and authority is explicit | Choose operation from run state, tool reversibility, and incident severity and produce the full artefact. | Duplicate, unauthorised, or unreplayable actions. |
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
- Mixing the neighbouring incident-response-runbook concern into this artefact without a boundary. Fix: cross-reference its output and keep ownership explicit.
- Omitting failure, rollback, empty-state, security, tenancy, or escalation behaviour. Fix: specify the trigger, safe action, verification, and owner for each applicable case.
- Mutating a repository, environment, tenant, ledger, or external system while drafting guidance. Fix: remain read-only until the exact mutation and authority are explicit.
- Claiming compliance, certification, readiness, or release from prose alone. Fix: require source-attributed evidence and a named acceptance decision.

## Worked Example

Given an approved project source and a conflicting implementation detail, record both with provenance, stop the affected branch, and obtain the accountable owner's decision. Then update the relevant contract, define a reproducible acceptance check, and retain its observed result. The artefact is accepted only when every operator action has an authority check, observable precondition, safe execution step, verification, and audit evidence.

## References

- [logic.prompt](logic.prompt) - load only when its template, logic, or detail is needed.
- [README.md](README.md) - load only when its template, logic, or detail is needed.
<!-- dual-compat-end -->
## Core Instructions

### Step 1: Kill-switch operations

Document three switches with operator-only access:

- **Global kill-switch** — refuses every tool with `kill_switch.global = refuse` across every tenant. Two-person rule. Used for upstream provider compromise, mass irreversible-incident, or red-team-confirmed catastrophic vulnerability.
- **Per-tenant kill-switch** — refuses tools for one tenant. Used for tenant-scoped incident, contractual obligation, or customer request.
- **Per-feature kill-switch** — refuses tools for one agent feature globally. Used for feature-scoped regression or SEV1 from the SLO doc.

State the propagation SLA (default 5 s), the rehearsal cadence (monthly in staging), and the operator surface (ops console + API + on-call paging integration).

### Step 2: Force-pause and force-resume

- **Force-pause an agent run** — orchestrator marks the run `intervened`; in-flight tool calls complete or time-out; no further steps.
- **Force-pause all runs for a tenant** — soft kill-switch; existing runs paused; new starts refused.
- **Force-resume** — orchestrator resumes from last durable state with reasoning logged; available only after a SEV closure review.

### Step 3: Replay a run

Operator can replay any historical run against the current planner + catalogue in the eval environment. Used for postmortems and for "would the fix have caught this?" verification.

### Step 4: Agent-task quarantine

When a run is suspected harmful but not actioned, quarantine the run:

- Mark the run `quarantined`.
- All tool calls refused.
- Run preserved with full state for forensic review.
- Notify the tenant admin within 24 h.

### Step 5: Audit-log review cadence

- Daily: irreversible-action audit log reviewed by an on-call operator; any anomaly creates a ticket.
- Weekly: per-feature audit summary reviewed by the AI lead.
- Quarterly: tenant-facing audit export offered to Enterprise tenants.

### Step 6: Agent-incident playbooks

Define playbooks for:

1. Mass irreversible-action incident.
2. Cross-tenant tool-routing attempt detected.
3. Indirect prompt injection succeeded in production.
4. Budget-runaway event (single tenant > 200% envelope for > 1 h).
5. Agent unresponsive / orchestrator crashed.
6. Tool provider compromise (external write tool with confirmed breach).
7. Disclosure of agent action (regulatory or customer).

Each playbook follows: detection → declare SEV → kill-switch decision → contain → investigate → notify → postmortem.

### Step 7: On-call rotation

Operators on call for agent incidents shall have:

- Kill-switch console access.
- Read-only access to per-tenant audit log.
- Paging from SLO burn-rate alerts and irreversible-incident triggers.
- Documented escalation path: AI Lead → Architect → CTO → CEO.

### Step 8: Write the runbook

`AI_Agent_Runbook.md` sections: 1) Kill-switch Operations, 2) Force-Pause & Resume, 3) Replay, 4) Agent-Task Quarantine, 5) Audit-Log Review, 6) Incident Playbooks, 7) On-call Rotation, 8) Rehearsal Cadence.

## Standards

- Google SRE incident response
- ISO/IEC 27035 (incident management)
- NIST AI RMF MANAGE
- ISO/IEC 42001 Clause 10 (improvement)

## Compliance drill evidence capture

Every drill produces evidence consumed by the SOC 2 / ISO / HIPAA control packs. Capture format and cadence are defined in `09-governance-compliance/25-ai-agent-evidence-pack-spec/references/ai-agent-evidence-frequency-table.md` (rows 15, 16, 17):

| Drill | Evidence | Cadence | Controls |
|-------|----------|---------|----------|
| Kill-switch (global / per-tenant / per-feature) | drill report; audit-log entry; propagation timing | quarterly staging; annual production | SOC2 CC7.4, A1.3; ISO A.5.30, A.8.2; HIPAA 164.308.a.7 |
| Replay-a-run | drill report | quarterly | SOC2 A1.3; ISO A.5.30 |
| Force-pause + force-resume | drill report | quarterly | SOC2 A1.3; ISO A.5.30 |
| Agent-task quarantine | drill report; tenant-admin notification log | annual | SOC2 CC7.3; ISO A.5.25 |

The compliance runbook (`06-deployment-operations/20-ai-agent-compliance-runbook`) sets the calendar.

## Resources

- `logic.prompt`, `README.md`, `references/ai-agent-runbook-template.md`.

## Unattended execution handoff

For an owner-authorised unattended development plan, use the project-local `auto-agents/README.md` and `auto-agents/config.json`. Keep the plan and authority explicit, provide project-specific verification commands, and preserve a durable handoff. Publishing, remote, branch, runner and limits are configured per project. Treat the worktree as checkout isolation, not a sandbox; preserve host permissions and security controls. Failed or unavailable checks are never passes. Verify the actual driver version and runtime before relying on it.
