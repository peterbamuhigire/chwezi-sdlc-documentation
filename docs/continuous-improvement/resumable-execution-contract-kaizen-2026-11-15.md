# Resumable execution contract Kaizen — 2026-11-15

## Aim and baseline

Make written plans, acceptance criteria, and specialist handoffs resumable by a
fresh Claude Code or Codex session, including after power loss or a usage-window
reset. The baseline had durable phase handoffs, criterion identifiers, and
general degraded-mode guidance, but no shared procedure tying task scope,
revision-bound evidence, replay decisions, specialist readiness, and compact
resume state together. An ordinary textual inspection of the affected skills
and `rules/common/phase-handoff.md` established this gap; this was not a
quantitative usage study.

## Change and decision

Added `rules/common/resumable-execution-contract.md` and linked it from the
acceptance-criteria, sprint-planning, plan-canvas, multi-agent-coordination,
and phase-handoff routes. The reference gives concrete planning fields, a
worked acceptance item, a small handoff record, external-effect replay
decisions, and capability/readiness/independence evidence rules. It directs
runners to use project-verified commands and environment details; unknown
commands remain `NOT ASSESSED`. It does not impose quotas, require blanket
human review, or alter either runner's model policy.

Decision: retain as a common rule with local links. Do not add a validator or
schema: the existing catalogue and skill formats can express the contract, and
the work adds no structured fields that require machine enforcement.

## Evidence and currentness

The contract is an original operational synthesis informed by Najim, *Systems
Thinking for Agentic AI*; Makino, *Multi-Agent Development with Claude Code*;
Huang, *Claude Code Operating Model*; and McGregor, *Full Stack JavaScript
Strategies* (2025). No book material is reproduced. The ideas are not treated
as evidence of current tool commands or product capabilities.

Digital Research currentness preflight: `NO_TIME_SENSITIVE_CLAIMS`. No standard
edition, law, technology version, platform capability, command, benchmark, or
model-policy assertion was added. Official runner CLI details were outside
this change and are not assessed here.

## Checks and limits

- Reviewed the shared contract against acceptance, sprint-planning,
  phase-handoff, plan-canvas, and multi-agent coordination boundaries.
- Checked that all detailed behavior has one canonical procedure and links
  point to it; the examples explicitly retain unknown project commands as
  `NOT ASSESSED`.
- Automated repository validation and runtime execution are not assessed in
  this workstream. No schema/helper changed, so no tests were added.
- The expected benefit (fewer ambiguous resumptions and unsafe retries) remains
  an inference until project teams exercise the procedure and report evidence.

## Sources

Durable concept inputs: Najim, *Systems Thinking for Agentic AI*; Makino,
*Multi-Agent Development with Claude Code*; Huang, *Claude Code Operating
Model*; McGregor, *Full Stack JavaScript Strategies* (2025). No quotation or
book summary is included.
