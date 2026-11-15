---
name: 15-ai-agent-multi-agent-coordination-spec
description: Use when two or more agents participate in one user task and need a bounded topology, role inventory, scratchpad isolation, supervision, message contract and failure handling; use agent architecture for the common single-agent runtime.
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---
# AI Agent Multi-Agent Coordination Spec Skill
<!-- dual-compat-start -->
## Use When

- An approved feature requires supervisor-worker, handoff, debate or another multi-agent topology.

## Do Not Use When

- Do not use for a single agent, parallel independent jobs, or to justify extra agents without measured need.

## Required Inputs

| Artefact | Source or provider | Required? | Missing behaviour |
|---|---|---|---|
| Approved agent architecture, feature and action catalogue | Phase 02/03 artefacts | Required | Stop if roles, authority or handoff outcome are undefined. |
| Latency, cost, privacy and failure constraints | Product, security and platform owners | Required | Return a single-agent alternative when multi-agent evidence is weak. |

## Workflow

1. Read the named inputs and confirm their approval, version and unresolved decisions.
2. Apply the decision rules below before drafting; stop on a missing authority, unsafe assumption or unresolved scope driver.
3. Produce the Multi-Agent Coordination Specification through the existing domain procedure and load only the references needed for the chosen branch.
4. Trace each material statement in the Multi-Agent Coordination Specification to an input, decision or explicitly qualified assumption.
5. Verify the observable acceptance conditions, record unassessed checks, and hand the artefacts to their named consumers.
6. If validation fails, recover by correcting the source decision or artefact and rerun the affected check; do not weaken the acceptance condition.

## Outputs

| Artefact | Consumer | Observable acceptance condition |
|---|---|---|
| Multi-Agent Coordination Specification | Agent, platform, security, evaluation and operations teams | Exactly one topology is chosen; every role has bounded actions, message schema, context rule, budget, supervision, timeout and recovery path. |

## Evidence Produced

| Evidence | Consumer | Acceptance condition |
|---|---|---|
| Source and decision trace | Reviewer and downstream owner | Each material statement cites an approved input, named decision or qualified open issue. |
| Completed verification record | Release or phase gate owner | Every applicable check records pass/fail; unavailable checks remain `not assessed`. |

## Capability and permission boundaries

Read-only is the default for analysis, review, evaluation and planning. Read and search access to authorised project artefacts are required. Editing is limited to an explicitly requested project deliverable. Execution may run document, syntax or validation checks. Network access is used only for facts that require current verification. Do not publish, spend, change production, approve policy, or claim certification without explicit authority.

## Degraded mode

If any required capability is unavailable, return the narrowest useful qualified Multi-Agent Coordination Specification draft plus a gap register showing the missing item, affected sections, risk and owner. Never convert an unassessed check into a pass.

## Decision Rules

| Choice | Action | Failure or risk avoided |
|---|---|---|
| Roles need distinct permissions or expertise | Use supervised workers with explicit handoffs | Authority remains bounded |
| One agent can complete the task within limits | Keep one agent | Coordination cost and emergent failure are avoided |

## Quality Standards

- Preserve repository terminology and trace every material choice to project context.
- Use deterministic acceptance conditions; replace vague quality claims with an observable check, threshold or named approval.
- Cover error, empty, edge, recovery and operational cases relevant to this skill.
- Verify standards, citations, APIs and package names before relying on them; qualify what cannot be checked.
- Stop release for a failed safety, security, legal, financial, accessibility or data-integrity gate.

## Anti-Patterns

- Adding agents to appear advanced. Fix: show the measured need and single-agent comparator.
- Sharing all scratchpads. Fix: pass only typed handoff data allowed by policy.
- Allowing workers to spawn workers. Fix: centralise topology authority in the supervisor.
- Running debate without a round cap. Fix: set budget, stop rule and tie-breaker.
- Retrying a failed handoff blindly. Fix: use idempotency, timeout and escalation rules.

## References

- [Resumable execution contract](../../rules/common/resumable-execution-contract.md): specify specialist capability/readiness, independence, evidence verdicts, and interruption-safe replay and reconciliation.

- [Coordination template](references/ai-agent-multi-agent-coordination-spec-template.md)
- [Agent Architecture neighbour](../14-ai-agent-architecture-spec/SKILL.md)
<!-- dual-compat-end -->




## Core Instructions

### Step 1: Declare the topology

Pick exactly one per feature:

| Topology | When | Trade-off |
|----------|------|-----------|
| Single-agent | task fits one role | simplest; least observability cost |
| Supervisor-worker | task decomposes into specialist sub-tasks | strong observability; supervisor is the bottleneck and the source of policy |
| Debate (N-agent) | task benefits from adversarial cross-check | improves factuality; cost scales with N and rounds |
| Handoff chain | sequential phases (retrieve → draft → verify) | clear ownership; brittle to mid-chain failure |

### Step 2: Declare the agent inventory and roles

Per agent role, declare:

- Role name.
- Bounded action-catalogue subset (the role may not call tools outside this subset).
- Memory access (which tiers, which keys).
- Planner template.
- Termination criteria for the role.

### Step 3: Declare the scratchpad isolation rule

Default: each agent role has its own scratchpad keyed by `(tenant_id, agent_run_id, agent_role)`. Cross-role sharing is permitted only via explicit handoff messages on the message bus, not via shared memory.

### Step 4: Declare the supervision policy

For supervisor-worker:

- **Review-before-act** — supervisor approves every worker plan before any tool execution.
- **Review-after-act** — supervisor reviews after each worker step.
- **Sample-review** — supervisor samples N% of worker outputs.

State which policy applies at which autonomy level. Irreversible tools always require review-before-act regardless of overall policy.

### Step 5: Declare the message-bus contract

Inter-agent messages carry: `from_role`, `to_role`, `agent_run_id`, `payload_schema`, `handoff_token`. The supervisor is the sole authority that issues `handoff_token`. Messages without a valid token are refused.

### Step 6: Declare failure-mode handling

| Failure | Handling |
|---------|----------|
| Worker exceeds budget | supervisor aborts the worker; the run continues with reduced scope or terminates |
| Worker emits malformed handoff | supervisor rejects; one retry; then abort |
| Debate fails to converge in N rounds | terminate; emit abstain payload |
| Supervisor crashes | orchestrator re-elects supervisor from the durable state |
| Worker proposes irreversible tool without approval | dispatcher refuses; supervisor reviews; the worker is paused |

### Step 7: Write the spec

`Multi_Agent_Coordination_Spec.md` sections: 1) Topology Verdict, 2) Agent Inventory & Roles, 3) Scratchpad Isolation, 4) Supervision Policy, 5) Message-Bus Contract, 6) Failure-Mode Handling, 7) ADR Seeds, 8) Traceability.

## Standards

- OWASP Top 10 for LLM Applications 2026 (published 2026-08-03; LLM01:2026-LLM10:2026 verified 2026-09-24 against the edition PDF at genai.owasp.org/resource/owasp-genai-llm-top-10-2026) and OWASP Top 10 for Agentic Applications 2026. Cite 2026 IDs; add the LLMxx:2025 ID only where an existing control set still uses it (2025-to-2026 map: `05-ai-red-team-test-plan/references/red-team-scenario-library.md`)
- Anthropic agent-engineering patterns
- AutoGen / CrewAI post-mortems
- ISO/IEC 42001 Clause 8

## Resources

- `logic.prompt`, `README.md`, `references/ai-agent-multi-agent-coordination-spec-template.md`.
