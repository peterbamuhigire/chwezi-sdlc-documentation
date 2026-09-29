---
name: hospitality-operating-model-srs
description: Use when writing or auditing requirements for hotel, resort, lodge, inn, guest-house, restaurant, bar, catering, or event-venue systems.
metadata:
  portable: true
  compatible_with: [claude-code, codex]
---

# Hospitality Operating Model SRS
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Requirements concern hotel, resort, accommodation, restaurant, bar, catering or event-venue operations.

## Do Not Use When

- The deliverable is only a finance posting design; route the finance-owned decision to the accounting engine.

## Required Inputs

| Artefact | Source/provider | Required? | If absent |
|---|---|---:|---|
| Format, actors, workflows, states, scope boundaries and source events | Product owner, operators and project context | Yes | Stop and issue a bounded context-gap record. |
| Integrations, controls, evidence and accountable owners | Engineering, finance, security and operations | Conditional | Return a qualified requirement and mark the missing oracle `NOT_ASSESSED`. |

## Workflow

1. Classify hotel, restaurant and shared contracts.
2. Define actors, entities, states, rules, exceptions and source events.
3. Write traceable requirements and measurable acceptance oracles.
4. Inject NFR, security, privacy, finance, food-safety and recovery gates.
5. Validate traceability, conflicts, evidence and human review before handoff; stop on a missing oracle and recover by issuing a qualified gap record.

## Outputs

| Artefact | Consumer | Acceptance condition |
|---|---|---|
| Hospitality operating-model SRS, glossary, traceability matrix, interface contracts and test seeds | Product, architecture, engineering, QA, finance and operations | Requirements are scoped, traceable, testable and owner-approved or explicitly unresolved. |

## Evidence Produced

| Evidence | Consumer | Acceptance condition |
|---|---|---|
| Requirement-to-source/oracle trace, review decisions, test evidence and gap register | Requirements reviewer and delivery team | Evidence is reproducible; missing or unavailable checks remain `NOT_ASSESSED`. |

## Capability and Permission Boundaries

Read/search and authorised requirements editing are required. Production changes,
data mutation, certification and statutory decisions require separate approval.

## Degraded Mode

Return the narrowest qualified question/gap register when project context,
owner, source or test oracle is missing; do not fill gaps with generic
assumptions. Mark the affected requirement not assessed until evidence is
available.

## Decision Rules

| Condition | Action | Risk avoided |
|---|---|---|
| A requirement affects money, stock or tax | Add finance and reconciliation route | Divergent records |
| A requirement affects safety or privacy | Add control, role, evidence and escalation | Hidden harm |
| An acceptance oracle is absent | Block release of the requirement | Untestable scope |

## Quality Standards

Requirements are actor-, state-, scope-, failure-, control- and oracle-complete,
with bidirectional traceability and named owners.
<!-- dual-compat-end -->

This domain skill turns hospitality work into traceable actors, states, controls,
interfaces, acceptance oracles and evidence. It supports a lean product scope;
it does not decide local law, tax, food-safety certification or accounting
treatment without the relevant authority and reviewer.

## Requirement method

For every requirement record: ID, actor, trigger, preconditions, main flow,
alternate/failure flows, state transition, data, permission, tenant/property
scope, integration, audit/control, acceptance oracle, evidence artifact,
priority, dependency, owner and status. Use `Must`, `Should`, `Nice to have` and
`No need` as product decisions; do not confuse them with implementation status.

## Hotel core scenarios

- configure property, room types, rooms, amenities, capacities, rates and
  business date;
- search availability and protect against overlapping reservations, stale
  inventory, group blocks, cancellation, no-show and deposit errors;
- check in a reservation or walk-in, capture only justified identity data with
  retention/consent rules, open a stay and folio;
- post room, F&B, laundry, minibar, meeting and adjustment charges; split,
  transfer, settle, refund and check out with immutable history;
- assign/inspect housekeeping, place/remove out-of-order, create maintenance
  work orders and prevent sale of unavailable rooms;
- run night audit, close/reopen by policy, reconcile folio/payment/ledger totals,
  and produce occupancy, ADR, RevPAR, room-revenue, source and exception views;
- manage groups, corporate/city ledger, events, transport, wake-up and service
  requests only when the operating model requires them.

## Restaurant core scenarios

- configure outlet, areas, tables, reservations, waitlist and server assignment;
- publish menu, modifiers, allergens/dietary notes, price/tax/availability and
  recipe/BOM/yield with effective dating;
- open table/tab/order, record seat/course/notes, route KOT to stations, display
  KDS state/timers, handle partial failure, reprint, void and approval;
- bill with service charge/tips/discounts, split/transfer, room charge,
  payment/refund, receipt, shift open/close, cash count and day close;
- receive and issue stock, record waste/spoilage/yield, warn on shortfall,
  reconcile actual/theoretical usage and report menu contribution;
- support delivery, advance orders, catering/events and food-safety logs only
  when capacity, controls and ownership are defined.

## Non-functional baseline

Inject requirements for tenant isolation, least privilege, immutable event
history, privacy/retention, payment boundary, idempotency, offline behaviour,
recovery/restore, observability, accessibility, low-bandwidth usability,
responsive performance, data lineage and reconciliation. Define targets from
measured property scale; do not copy arbitrary latency or uptime numbers.

## Prioritisation and audit

Must have = safety, legal/control, core revenue, operational continuity or
critical data integrity. Should have = material efficiency, management control
or competitive readiness. Nice to have = valuable but deferrable differentiation.
No need = speculative, duplicative, unsafe, ungoverned or unsupported scope.

Audit each item with code/docs/schema evidence, executable test, failure path,
security/tenant test, reconciliation and owner sign-off. A documented or
observed surface is not a pass; absent evidence is `NOT_ASSESSED`.

## Anti-patterns

- “The system shall manage hotels” with no actor, state or oracle. Fix: decompose it.
- Calling a documented or observed surface complete. Fix: require executable proof.
- Mixing room, restaurant and finance behaviour in one vague requirement. Fix: define the interface and reconciliation owner.
- Making arbitrary latency or uptime targets. Fix: derive targets from measured scale.
- Hiding privacy, safety, approval or recovery paths in non-functional prose. Fix: make them testable requirements.

## Worked example

`HTL-RES-004`: reservations agent searches a property for a room type and date
range; the system rejects an overlapping booking atomically, records the actor,
property, source and reason, returns refreshed availability, and produces a
replayable test with two concurrent requests. The requirement remains
`NOT_ASSESSED` until that evidence exists.

## References

- [Hospitality domain pack](../../domains/hospitality/INDEX.md)
- [Chwezi Accounting Doctrine](https://github.com/peterbamuhigire/chwezi-accounting-doctrine/blob/main/README.md)
- [Hospitality engineering system skill](https://github.com/peterbamuhigire/chwezi-dev-engine/blob/main/skills/product-business/hospitality-hotel-restaurant-systems/SKILL.md)
