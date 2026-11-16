# Resumable execution contract

Use this contract when a plan, acceptance catalogue, specialist assignment, or
phase handoff will be executed by Claude Code, Codex, or another capable
runner. It is model-neutral. Claude and Codex keep their own model selection,
tools, permissions, and runtime policies.

## Write an executable slice

Give each independently verifiable work item a stable ID that survives
reordering and revision. Record its prerequisite IDs, owned outcome, explicit
in-scope and excluded files or surfaces, and the person or role accountable for
acceptance. Name a file or bounded discovery task for every target. Discovery
must end with a concrete path list and a stop condition before edits expand.

State acceptance as an observable result with its evidence location. For each
work item, provide the exact validation command, working directory, required
environment or fixture, and expected exit/result when those are known from the
project's own instructions or verified environment. Preserve commands
verbatim. If any part is unavailable, mark that check `NOT ASSESSED` and state
the missing fact; do not fill it with a likely command.

Acceptance criteria follow the user journey and its meaningful states, not a
quota. Cover the normal result and applicable empty, invalid/error, denied,
boundary, and interrupted/recovery states. State observable outcomes and
prohibited side effects where those matter. A criterion that has no applicable
state may omit it with a short rationale rather than add filler.

## Preserve evidence and resume safely

Keep approved intent separate from execution state. The executor may update task
status and evidence, but a change to scope, dependency, acceptance criterion or
test oracle returns to the accountable requirement owner. Record the reason,
decision, changed baseline and affected downstream tests and release commitments.
Preserve prior evidence as historical; reassess claims whose inputs changed.
Passing a weakened test does not satisfy the original requirement.

For product work, connect each material slice to the observed user problem and
the decision it serves. Distinguish users, buyers, decision makers and operators;
record whose evidence supports the need and whose acceptance is required. An
agent's proposed feature or invented persona is not stakeholder validation.
After a pilot or operational observation, route new evidence back to the owner
for a baseline decision rather than silently expanding the implementation plan.

Bind evidence to the input revision or baseline, work-item ID, command and
environment, timestamp, result, and durable evidence path. When relevant input
changes, mark dependent evidence stale and rerun only those checks. Distinguish
completed outcomes from activity: a command was attempted is not a pass; files
were edited is not acceptance; a phase is complete only when its stated exit
conditions and evidence are satisfied.

Persist the plan, completed IDs, decisions, evidence pointers, open blockers,
and next action in files in the project workspace. On interruption, reread
that state, verify the current revision and external effects, and continue
automatically through all already-authorised, unblocked phases in dependency
order. Do not wait for a repeated "continue". Pause dependent work only for a
missing decision, explicit approval, genuine blocker, or governing instruction;
continue independent authorised work. A checkpoint reports progress; it does
not close the task.

For each operation that can create an external effect, state its replay policy
before execution: safe to repeat, idempotency key or equivalent deduplication,
read-before-retry reconciliation, or manual recovery required. After a power
cut, context-window end, or usage-window reset, inspect durable records and
the external system for whether the effect committed before retrying. Never
assume a timeout means no effect. If the outcome cannot be reconciled, stop
that operation, preserve evidence, and report the exact unresolved effect and
owner. Do not replay irreversible or non-idempotent work blindly.

## Assign specialists by capability

For every specialist assignment, name the bounded question or deliverable,
required access and tools, permitted writes or actions, source materials,
independence needed, acceptance oracle, evidence format, and failure/return
condition. Check readiness before dispatch: the role has the required
capability and access, its task does not conflict with another writer's owned
files, and its evidence can answer the question. A label, seniority, or
persona is not proof of competence.

Keep independent verification separate from the producer when the claim is
fault-sensitive; give the reviewer the evidence and oracle, not only the
producer's conclusion. Record each result as `PASS`, `FAIL`, or `NOT ASSESSED`,
with source revision, method, evidence location, limitation, and reviewer.
Reconcile specialist outputs against the parent acceptance criteria before
integrating them. Reject unsupported findings; do not turn missing evidence
into agreement.

## Compact handoff record

Keep the resumable handoff short and link to detailed artefacts:

```markdown
## Handoff — <plan or phase ID> — <baseline/revision>
- Status: <complete | in progress | blocked>
- Completed IDs: <IDs and evidence links>
- Next ready IDs: <IDs, in dependency order>
- Decisions/blockers: <owner, impact, exact next action, or none>
- Checks: <command/env/result/evidence, or NOT ASSESSED and why>
- External effects: <reconciled state and replay policy, or none>
- Open risks/assumptions: <bounded items, or none>
```

Do not duplicate the plan in the handoff. A new runner must be able to resume
from the linked files without relying on conversation memory.

## Worked item

```markdown
### PLAN-014 — Verify denied export leaves no file
- Depends on: PLAN-009 (export permission contract)
- Owns: `tests/export/denied-export.*` (confirm exact path before editing)
- Excludes: production data and unrelated export flows
- Acceptance: with a user lacking export permission and one visible row,
  requesting export returns the documented denial; no download is created and
  no export record is added. Evidence: test result and captured response.
- Check: `<copy verified project command>` from `<verified repository root>`;
  expected: `<project-defined result>`. Until populated from project evidence:
  NOT ASSESSED; do not execute a guessed command.
- Replay: local test is safe to repeat; verify the fixture reset before rerun.
```

## Evidence and sources

This is an original operational synthesis informed by Najim, *Systems Thinking
for Agentic AI*; Makino, *Multi-Agent Development with Claude Code*; Huang,
*Claude Code Operating Model*; and McGregor, *Full Stack JavaScript
Strategies* (2025). These works inform durable workflow concepts only; they do
not establish current tool commands, runtime features, or model behaviour.
Currentness preflight: `NO_TIME_SENSITIVE_CLAIMS` (2026-11-15). No platform,
version, command, standard edition, or model-policy claim is introduced here.
