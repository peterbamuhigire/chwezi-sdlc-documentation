---
name: 13-saas-billing-and-metering-spec
description: "Use when specifying SaaS usage events, billing, credits, refunds, dunning, finance handoff, and testable metering controls; use pricing-and-packaging for commercial tier design."
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---

# SaaS Billing & Metering Spec Skill

<!-- local-contract-start -->
<!-- dual-compat-start -->
## Use When

- specifying SaaS usage events, billing, credits, refunds, dunning, finance handoff, and testable metering controls; use pricing-and-packaging for commercial tier design.
- Use this procedure when the required source artefacts are available and `SaaS billing and metering specification` is the next lifecycle deliverable.

## Do Not Use When

- Use `pricing-and-packaging` when that neighbouring route owns the decision or deliverable.
- Do not invent missing project evidence, standards clauses, thresholds, or stakeholder decisions.

## Required Inputs

| Artefact | Source or provider | Required? | Behaviour when missing |
| --- | --- | --- | --- |
| Approved pricing, entitlement, finance, and tenant context | Product owner and finance doctrine | Yes | Stop the affected step, name the missing source, and return only a qualified gap record. |

## Workflow

1. Inspect the required inputs and log the exact sources, versions, and unresolved assumptions.
2. Apply this skill's existing domain workflow and decision rules to produce `SaaS billing and metering specification`.
3. Stop when a required source, accountable decision owner, or deterministic test oracle is absent.
4. Recover by preserving valid work, marking the blocked scope, and returning the narrowest qualified artefact plus the next evidence needed.

## Outputs

| Artefact | Consumer | Acceptance condition |
| --- | --- | --- |
| SaaS billing and metering specification | Architecture, finance, API, and test owners | Required sections are populated, source links resolve, and every material requirement or decision has an observable review or test oracle. |

## Evidence Produced

| Evidence | Reviewer | Acceptance condition |
| --- | --- | --- |
| Source, decision, trace, and validation record for `SaaS billing and metering specification` | Requirements quality reviewer | Inputs used, decisions made, checks run, failures, and unassessed items are explicit. |

## Capability and permission boundaries

Read and search are required. Editing is allowed only when the request authorises creation or repair of the named requirements artefact. Publishing, production mutation, destructive action, spending, and certification require explicit authority.

## Degraded mode

Fallback: if a required file, reviewer, standard source, network check, renderer, or execution capability is unavailable, return the narrowest useful qualified result and mark the affected check `not assessed`; never convert an unassessed check into a pass.

## Decision Rules

| Choice or condition | Action | Failure or risk avoided |
| --- | --- | --- |
| A chargeable event cannot be tied to tenant, source, quantity, and idempotency key | Reject the event contract and close the lineage gap. | Unbillable usage, duplicate charges, or unauditable revenue. |
| Required inputs and test oracles are complete | Continue through the existing workflow and record evidence. | A deliverable whose acceptance cannot be reproduced. |
| A mandatory source or owner is missing | Stop the affected branch and issue a qualified gap record. | Fabricated context or unauthorised decisions. |

## Quality Standards

- Preserve stable identifiers and bidirectional traceability from project evidence to `SaaS billing and metering specification` and its acceptance checks.
- Apply ISO/IEEE measures only with a named metric, method, threshold, evidence source, and responsible reviewer; run the anti-slop gate before release.

## Anti-Patterns

- Producing `SaaS billing and metering specification` from assumed context. Fix: cite the project source or mark the scope blocked.
- Accepting a material requirement without a deterministic oracle. Fix: add a measurable result, boundary, and verification method.
- Crossing into `pricing-and-packaging` without routing the decision. Fix: hand off the named input and preserve trace links.
- Treating an unavailable check as passed. Fix: mark it `not assessed` and state the release consequence.
- Claiming standards, statutory, or stakeholder approval without evidence. Fix: cite the source and reviewer or qualify the claim.

## References

- [Skill authoring and release standard](../../docs/skill-authoring-standard.md)
- [Skill guidance](README.md)
- [Executable generation logic](logic.prompt)
- [Ai Usage Events](references/ai-usage-events.md)
- [Saas Billing And Metering Srs Template](references/saas-billing-and-metering-srs-template.md)
- [Saas Revenue Recognition Spec Template](references/saas-revenue-recognition-spec-template.md)
<!-- dual-compat-end -->
<!-- local-contract-end -->

## Overview

Generates the requirements specification for the SaaS billing-and-metering pipeline. Sourced from Mersch (financial-metrics rigor) and Golding (control-plane responsibilities).

## Core Instructions

### Step 1: Inventory metered events

For every billable or quota-limited action, produce a row:

| Event name | Schema | Granularity | Source service | Sink | Retention raw / aggregate | Used for | Tenant fields |
|------------|--------|-------------|----------------|------|---------------------------|----------|---------------|
| `api.request.completed` | {tenant_id, endpoint, ts, status, bytes_in, bytes_out, duration_ms} | per request | Gateway | metering bus | 13 mo / 7 y | rate limit + per-call pricing + analytics | tenant_id, tier |
| `storage.snapshot` | {tenant_id, bytes_used, ts} | hourly | Storage service | metering bus | 13 mo / 7 y | GB-hour pricing | tenant_id, tier |
| `seat.assigned` | {tenant_id, user_id, ts, role} | per change | Identity | metering bus | 13 mo / 7 y | per-seat pricing | tenant_id |
| `feature.used` | {tenant_id, feature_id, ts} | per use | App services | metering bus | 13 mo / 7 y | tier enforcement + analytics | tenant_id, tier |

### Step 2: Tenant-context propagation rules

Every event MUST include `tenant_id`. Every billable event MUST also include `tier`, `region`, and source `trace_id`. Events missing `tenant_id` MUST be rejected at the bus ingress and logged.

### Step 3: Transport, ordering, retention

- Transport: append-only event bus (Kafka / Kinesis / SQS-FIFO).
- Ordering: per-tenant partition key.
- Delivery: at-least-once with idempotency keys.
- Retention raw: 13 months (audit-able billing dispute window).
- Retention aggregates: 7 years (SOX / financial-records).

### Step 4: Aggregation & pricing engine

- Rollups: minute → hour → day → month per tenant per meter.
- Pricing engine: consumes aggregates + tier price book + contract overrides → produces invoice line items.
- Tier price book is versioned; price changes require a versioned price book and an ADR.

### Step 5: Revenue-recognition rules (ASC 606 / IFRS 15)

- Identify the contract.
- Identify performance obligations (subscription, professional services, usage overages).
- Determine transaction price.
- Allocate to performance obligations.
- Recognise revenue as obligations satisfied (typically subscription ratable, services on milestone, usage on consumption).

Document for each price-list line: revenue-recognition pattern (ratable / point-in-time / milestone / usage).

### Step 6: Dunning, refunds, credits

- Dunning sequence: D+0 reminder, D+3 first warning, D+7 second warning + read-only flag, D+14 suspension, D+45 offboarding.
- Refunds: who can issue, dollar thresholds, audit, ERP entry.
- Credits (service-credit from SLA breach): how applied, expiration, ERP entry.

### Step 7: Audit & reconciliation

- Daily reconciliation: metering aggregate vs gateway raw count vs charged amount.
- Discrepancy alarm threshold: 0.1%.
- Annual external audit (for series-B+ companies).
- Platform invoices and credit notes to tenants use platform-wide contiguous series that never consume a tenant's own series (FR-DOCNUM-030 in [document numbering requirements](../references/document-numbering-requirements.md)).

### Step 8: ERP / finance handoff

- Export cadence (daily journals).
- Format (CSV / API / Avro).
- Mapping: meter → GL account → cost centre.
- Period-end close cutoff rules.

### Step 9: Write the spec

`Billing_And_Metering_Spec.md` with sections: 1) Metered Event Catalogue, 2) Tenant Context Rules, 3) Transport / Retention / Ordering, 4) Aggregation & Pricing Engine, 5) Revenue Recognition (ASC 606 / IFRS 15), 6) Dunning / Refunds / Credits, 7) Audit & Reconciliation, 8) ERP Handoff, 9) Traceability to PRD pricing and SRS NFRs.

## Standards

- ASC 606 / IFRS 15 — Revenue recognition.
- SOX (for public-co targets) — internal controls over financial reporting.
- ISO/IEC 25010 — quality (correctness as an SLI).

## Resources

- `logic.prompt`, `README.md`, `references/saas-billing-and-metering-srs-template.md`, `references/saas-revenue-recognition-spec-template.md`.
