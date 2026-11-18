---
name: 14-ai-agent-architecture-spec
description: Use when an approved tool-using AI agent needs a runtime loop, state machine, memory tiers, planner, dispatcher, durability, kill switch and tenant isolation; use AI architecture for non-agent AI services and multi-agent coordination only when several agents share a task.
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---
# AI Agent Architecture Spec Skill
<!-- dual-compat-start -->
## Use When

- The strategy and feature requirements justify adaptive planning and bounded tool actions.

## Do Not Use When

- Do not use for direct calls, ordinary RAG or deterministic workflows that do not require an agent.

## Required Inputs

| Artefact | Source or provider | Required? | Missing behaviour |
|---|---|---|---|
| Approved agent feature, action catalogue and AI architecture | Phase 01-03 artefacts | Required | Stop if actions, authority or autonomy level are undefined. |
| Durability, tenancy, audit, cost and safety constraints | Platform, security, finance and operations owners | Required | Default to lower autonomy and narrower actions when evidence is incomplete. |

## Workflow

1. Read the named inputs and confirm their approval, version and unresolved decisions.
2. Apply the decision rules below before drafting; stop on a missing authority, unsafe assumption or unresolved scope driver.
3. Produce the AI Agent Architecture Specification and ADR seeds through the existing domain procedure and load only the references needed for the chosen branch.
4. Trace each material statement in the AI Agent Architecture Specification and ADR seeds to an input, decision or explicitly qualified assumption.
5. Verify the observable acceptance conditions, record unassessed checks, and hand the artefacts to their named consumers.
6. If validation fails, recover by correcting the source decision or artefact and rerun the affected check; do not weaken the acceptance condition.

## Outputs

| Artefact | Consumer | Observable acceptance condition |
|---|---|---|
| AI Agent Architecture Specification and ADR seeds | Agent, platform, security, test and operations teams | State is durable; every action passes dispatcher policy and audit; budgets, approval, recovery, kill switch and tenant isolation have deterministic tests. |

## Evidence Produced

| Evidence | Consumer | Acceptance condition |
|---|---|---|
| Source and decision trace | Reviewer and downstream owner | Each material statement cites an approved input, named decision or qualified open issue. |
| Completed verification record | Release or phase gate owner | Every applicable check records pass/fail; unavailable checks remain `not assessed`. |

## Capability and permission boundaries

Read-only is the default for analysis, review, evaluation and planning. Read and search access to authorised project artefacts are required. Editing is limited to an explicitly requested project deliverable. Execution may run document, syntax or validation checks. Network access is used only for facts that require current verification. Do not publish, spend, change production, approve policy, or claim certification without explicit authority.

## Degraded mode

If any required capability is unavailable, return the narrowest useful qualified AI Agent Architecture Specification and ADR seeds draft plus a gap register showing the missing item, affected sections, risk and owner. Never convert an unassessed check into a pass.

## Decision Rules

| Choice | Action | Failure or risk avoided |
|---|---|---|
| Action has material external effect | Require policy check and explicit approval per strategy | Agent cannot exceed delegated authority |
| Run is long-lived or retriable | Persist state and idempotency keys | Resume does not duplicate action |

## Quality Standards

- Preserve repository terminology and trace every material choice to project context.
- Use deterministic acceptance conditions; replace vague quality claims with an observable check, threshold or named approval.
- Cover error, empty, edge, recovery and operational cases relevant to this skill.
- Verify standards, citations, APIs and package names before relying on them; qualify what cannot be checked.
- Stop release for a failed safety, security, legal, financial, accessibility or data-integrity gate.

## Anti-Patterns

- Letting the planner call tools directly. Fix: require dispatcher enforcement and audit.
- Sharing memory namespaces across tenants. Fix: bind every memory operation to verified tenant context.
- Using an in-memory loop for durable work. Fix: persist checkpoints and recovery state.
- Defining a kill switch without a response bound. Fix: specify propagation, cancellation and evidence.
- Allowing unbounded steps or spend. Fix: enforce per-run budgets and escalation.

## References

- [Agent architecture template](references/ai-agent-architecture-spec-template.md)
- [AI Architecture neighbour](../11-ai-architecture-spec/SKILL.md)
- [Multi-agent neighbour](../15-ai-agent-multi-agent-coordination-spec/SKILL.md)
<!-- dual-compat-end -->




## Overview

The agent-distinctive architecture artefact. Sits alongside the AI Architecture Spec and the multi-tenancy spec. Captures the runtime loop, the state machine, the memory tiers, the planner, the dispatcher (the gate that enforces the action catalogue, the audit log, the rate limits, and the kill-switch), the supervisor (for multi-agent topologies), and the per-tenant isolation contract.

## Core Instructions

### Step 1: Read context

Read the AI architecture spec, the agent feature PRD, the action catalogue, the multi-tenancy spec. Identify in-scope agent features, autonomy levels, and the action catalogue scope per feature.

### Step 2: Declare the agent runtime decomposition

The agent runtime sits inside the AI plane and contains:

- **Agent Orchestrator** — the per-run controller that hosts the loop and state machine.
- **Planner** — the LLM call(s) that produce or revise the plan.
- **Tool Dispatcher** — single point of egress for every tool call; consults the action catalogue, enforces rate limits, applies kill-switch, emits the audit-log event, and gates irreversible actions through the HITL hook.
- **Memory Tiers** — scratchpad (per-run, ephemeral), episodic (per-user / per-tenant, time-windowed), long-term (per-tenant, opted-in only).
- **Supervisor** (optional, multi-agent only) — coordinates worker agents.
- **Durable State Store** — agent-run-state at every step for resumability.
- **HITL Hook** — the bridge to the human-approval UI and the inbox of approver-role queues.
- **Audit Log Pipeline** — append-only sink for every tool call event.
- **Kill-switch Controller** — operator surface; flips global, per-tenant, or per-feature switches; propagates to all dispatchers within the SLA.

Diagram in Mermaid; place every service.

### Step 3: Spec the loop and state machine

Standard loop: `observe → plan → act → observe → ...` until terminal state. State machine states: `pending`, `planning`, `awaiting-approval`, `executing-tool`, `awaiting-tool-result`, `intervened`, `aborted`, `completed-success`, `completed-abstain`, `completed-failed`. Define transitions and the durability point at every transition.

### Step 4: Spec memory tiers

For each tier:

- **Scratchpad** — in-process; lifespan = agent run; isolation key = `(tenant_id, agent_run_id)`; never crosses run boundaries.
- **Episodic** — durable; lifespan = TTL (e.g. 30 d); isolation key = `(tenant_id, user_id)`; access requires tenant claim.
- **Long-term** — durable; lifespan = unbounded; isolation key = `(tenant_id)`; access requires both the tenant claim and the per-tenant opt-in flag.

State the encryption posture, key management, and the redaction rule at write time.

### Step 5: Spec the planner

State whether the planner is `ReAct`, `Plan-and-execute`, `Tree-of-thought`, `Function-calling-loop`, or custom. State the prompt template source (prompt registry). State the budget hooks — the planner shall halt when max-step or max-cost is reached. State the abstain payload — the planner emits a structured abstain when no plan satisfies the policy envelope.

### Step 6: Spec the tool dispatcher

The dispatcher is the gate. For every tool call:

1. Look up tool in the action catalogue; refuse if absent.
2. Validate input against the tool schema; refuse on schema failure.
3. Re-validate tenant claim and tier availability.
4. Consult kill-switch state (global, per-tenant, per-feature); refuse with the configured message.
5. Consult rate-limit class; throttle if exhausted.
6. If reversibility=irreversible or above-threshold, invoke the HITL hook and block until approved or timed-out.
7. Execute the underlying API call.
8. Sanitise tool output (strip embedded instructions; truncate; redact PII).
9. Emit the audit-log event.
10. Return the sanitised output to the orchestrator.

### Step 7: Spec the supervisor (multi-agent only)

If multi-agent, cross-link to `15-ai-agent-multi-agent-coordination-spec` and place the supervisor in the diagram. State the supervision policy (review-before-act / review-after-act / sample-review).

### Step 8: Spec durability and resumability

The orchestrator persists state at every transition. After a process crash or planned restart, the orchestrator shall resume in-flight runs from the last durable state. State the storage technology, the serialisation format, and the resume SLA (e.g. < 30 s after restart). State the idempotency contract — every tool call carries an idempotency key derived from `(agent_run_id, step_index)`.

### Step 9: Spec kill-switch wiring

State the kill-switch surface (operator API + ops console UI). State the propagation SLA — global kill-switch shall halt every dispatcher within 5 seconds. State the rehearsal cadence — kill-switch is rehearsed monthly in staging.

### Step 10: Spec per-tenant isolation

State the enforcement points: planner (no cross-tenant retrieval), dispatcher (tenant claim re-validated per call), memory tiers (isolation keys above), audit log (per-tenant partitioning).

### Step 11: Emit ADR seeds

ADR seeds: planner choice per feature, memory store technology, durable state store, supervisor topology, kill-switch propagation SLA, irreversibility-gating policy, tool-call audit log retention.

### Specify how a corrected memory takes effect

For a design that stores summaries, include one worked correction in the Memory Tiers section. Identify the source record, summary, dependent index or cache, the actor allowed to correct it and what a reader sees during propagation. Specify the observable result after correction and after access revocation. A test can warm the cache with a permitted answer, revoke the reader's access, then repeat the same question in the same session and in a fresh one. State which component enforces the decision in each path.

Concept source: Labaschin et al. (2025), *Managing Memory for AI Agents*, chapters 1 and 5, on lossy summaries and versioned collective memory.

### Step 12: Write the spec

`AI_Agent_Architecture_Spec.md` sections: 1) Agent Runtime Diagram, 2) Loop & State Machine, 3) Memory Tiers, 4) Planner, 5) Tool Dispatcher, 6) Supervisor (if applicable), 7) Durability & Resumability, 8) Kill-switch Wiring, 9) Per-Tenant Isolation, 10) ADR Seed Index, 11) Traceability.

## Standards

- OWASP Top 10 for LLM Applications 2026 (published 2026-08-03; LLM01:2026-LLM10:2026 verified 2026-09-24 against the edition PDF at genai.owasp.org/resource/owasp-genai-llm-top-10-2026) and OWASP Top 10 for Agentic Applications 2026. Cite 2026 IDs; add the LLMxx:2025 ID only where an existing control set still uses it (2025-to-2026 map: `05-ai-red-team-test-plan/references/red-team-scenario-library.md`)
- NIST AI RMF MAP / MEASURE / MANAGE
- ISO/IEC 42001 Clause 8
- AWS Well-Architected ML/AI Lens

## Resources

- `logic.prompt`, `README.md`, `references/ai-agent-architecture-spec-template.md`.
