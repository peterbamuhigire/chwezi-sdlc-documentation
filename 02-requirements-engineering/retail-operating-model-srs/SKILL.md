---
name: retail-operating-model-srs
description: "Use when specifying retail, omnichannel, POS, merchandising, pricing, promotions, fulfilment, returns, shrink, loyalty, vendor funding, or store operations; use embedded-accounting-engine-srs for the shared ledger core."
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---

# Retail Operating Model SRS Skill

<!-- local-contract-start -->
<!-- dual-compat-start -->
## Use When

- specifying retail, omnichannel, POS, merchandising, pricing, promotions, fulfilment, returns, shrink, loyalty, vendor funding, or store operations; use embedded-accounting-engine-srs for the shared ledger core.
- Use this procedure when the required source artefacts are available and `Retail operating-model SRS` is the next lifecycle deliverable.

## Do Not Use When

- Use `embedded-accounting-engine-srs` when that neighbouring route owns the decision or deliverable.
- Do not invent missing project evidence, standards clauses, thresholds, or stakeholder decisions.

## Required Inputs

| Artefact | Source or provider | Required? | Behaviour when missing |
| --- | --- | --- | --- |
| Retail scope, actors, channels, catalogue, inventory, money flows, controls, integrations, and finance doctrine | Retail operators, project context, and finance owner | Yes | Stop the affected step, name the missing source, and return only a qualified gap record. |

## Workflow

1. Inspect the required inputs and log the exact sources, versions, and unresolved assumptions.
2. Apply this skill's existing domain workflow and decision rules to produce `Retail operating-model SRS`.
3. Stop when a required source, accountable decision owner, or deterministic test oracle is absent.
4. Recover by preserving valid work, marking the blocked scope, and returning the narrowest qualified artefact plus the next evidence needed.

## Outputs

| Artefact | Consumer | Acceptance condition |
| --- | --- | --- |
| Retail operating-model SRS | Architecture, implementation, finance, test, and operations teams | Required sections are populated, source links resolve, and every material requirement or decision has an observable review or test oracle. |

## Evidence Produced

| Evidence | Reviewer | Acceptance condition |
| --- | --- | --- |
| Source, decision, trace, and validation record for `Retail operating-model SRS` | Requirements quality reviewer | Inputs used, decisions made, checks run, failures, and unassessed items are explicit. |

## Capability and permission boundaries

Read and search are required. Editing is allowed only when the request authorises creation or repair of the named requirements artefact. Publishing, production mutation, destructive action, spending, and certification require explicit authority.

## Degraded mode

Fallback: if a required file, reviewer, standard source, network check, renderer, or execution capability is unavailable, return the narrowest useful qualified result and mark the affected check `not assessed`; never convert an unassessed check into a pass.

## Decision Rules

| Choice or condition | Action | Failure or risk avoided |
| --- | --- | --- |
| A stock, refund, discount, settlement, shrink, or loyalty event has no accounting and reconciliation path | Block the flow and specify source event, posting, control, evidence, and exception handling. | Operational and financial records diverging. |
| Required inputs and test oracles are complete | Continue through the existing workflow and record evidence. | A deliverable whose acceptance cannot be reproduced. |
| A mandatory source or owner is missing | Stop the affected branch and issue a qualified gap record. | Fabricated context or unauthorised decisions. |

## Quality Standards

- Preserve stable identifiers and bidirectional traceability from project evidence to `Retail operating-model SRS` and its acceptance checks.
- Apply ISO/IEEE measures only with a named metric, method, threshold, evidence source, and responsible reviewer; run the anti-slop gate before release.

## Anti-Patterns

- Producing `Retail operating-model SRS` from assumed context. Fix: cite the project source or mark the scope blocked.
- Accepting a material requirement without a deterministic oracle. Fix: add a measurable result, boundary, and verification method.
- Crossing into `embedded-accounting-engine-srs` without routing the decision. Fix: hand off the named input and preserve trace links.
- Treating an unavailable check as passed. Fix: mark it `not assessed` and state the release consequence.
- Claiming standards, statutory, or stakeholder approval without evidence. Fix: cite the source and reviewer or qualify the claim.

## References

- [Skill authoring and release standard](../../docs/skill-authoring-standard.md)
<!-- dual-compat-end -->
<!-- local-contract-end -->

## Overview

This skill turns retail project context into complete, testable retail software requirements. It uses the retail domain pack as the controlled vocabulary and the finance doctrine engine as the required cross-check whenever money, inventory, refunds, discounts, vendor funding, shrink, POS, or reporting is affected.

## Core Workflow

### Step 1: Classify the Retail Scope

Read `projects/<ProjectName>/_context/` and classify which capability clusters are in scope:

| Cluster | Trigger terms |
|---|---|
| Commercial architecture | assortment, category, merchandising, line review, pricing, promotion, coupon, discount, markdown |
| Customer and digital growth | loyalty, CRM, lifecycle, conversion, product page, search, navigation, faceted filters |
| Omnichannel operations | inventory, fulfilment, available-to-promise, pickup, ship-from-store, returns, reverse logistics |
| Store execution | POS, cashier, store task, SOP, labour, schedule, audit, new store opening |
| Profit protection and supplier economics | shrink, loss prevention, vendor terms, rebate, allowance, trade spend, private label |
| Performance management | dashboard, KPI, weekly business review, planogram, space productivity, action register |

If the brief does not identify the cluster, flag `[CONTEXT-GAP: retail capability scope]`.

### Step 2: Build the Retail Entity Catalogue

For each in-scope cluster, list entities, state transitions, source events, owners, and systems of record. Use `domains/retail/references/retail-operating-model.md` as the minimum entity vocabulary.

Every source event row must include:

- event name;
- source system;
- actor or integration;
- timestamp;
- affected entity;
- prior state;
- new state;
- evidence pointer;
- idempotency key;
- downstream finance/reporting handoff, if any.

### Step 3: Apply Finance and Control Gates

Load `domains/retail/references/finance-control-gates.md`. If any finance trigger is present, route to `chwezi-accounting-doctrine` and record the route in the generated artefact.

Do not write final requirements for these items without a finance/control section:

- inventory valuation, movement, count, write-down, shrink, damage, or disposal;
- sale, payment, refund, exchange, credit note, split tender, cash drawer, card settlement, or mobile money;
- price override, promotion, manual discount, coupon, markdown, vendor funding, rebate, co-op funding, or scanback;
- loyalty points, gift cards, wallet balance, store credit, or customer advance;
- financial KPI, gross margin, markdown rate, return rate, shrink rate, vendor funding recovery, or POS reconciliation.

### Step 4: Write Stimulus-Response Functional Requirements

Use the SRS engine's normal requirement pattern:

```text
When <stimulus> occurs, the system shall <response> so that <controlled outcome> can be verified by <test oracle/evidence>.
```

Each requirement must include:

- actor or source event;
- precondition;
- system response;
- exception path;
- audit evidence;
- measurable acceptance criterion;
- traceability to retail capability and business goal.

### Step 5: Write Retail NFRs

Apply the existing retail defaults plus the added requirements:

- RET-NFR-001 Cardholder Data Protection
- RET-NFR-002 Checkout Performance
- RET-NFR-003 Consumer Data Rights
- RET-NFR-004 Inventory Accuracy
- RET-NFR-005 Peak Sales Availability
- RET-NFR-006 Product Data Quality
- RET-NFR-007 Retail Event Auditability
- RET-NFR-008 Dashboard Freshness and Lineage

Adapt thresholds only when project context provides stronger local targets. Do not weaken security, auditability, or evidence requirements without a documented waiver.

### Step 6: Specify Interfaces

Retail SRS interface coverage should include the relevant systems:

- POS and payment terminal;
- payment gateway, card settlement, mobile money, wallet, cash drawer;
- product information management;
- inventory service, warehouse management system, third-party logistics;
- order management system;
- CRM, email/SMS/push, loyalty platform;
- ERP/general ledger, tax/fiscal device, source-document archive;
- supplier/vendor portal or claims register;
- analytics warehouse and dashboard.

For each interface, define payload, direction, cadence, failure mode, retry/idempotency, reconciliation, and owner.

### Step 7: Produce Acceptance Tests

Create retail acceptance tests for:

- price/promotion/markdown effective-dated rollout;
- offer-stack prevention;
- inventory reservation and release;
- order fulfilment routing;
- return inspection and disposition;
- refund approval and reconciliation;
- manual discount approval;
- stock count variance control;
- vendor funding claim evidence;
- dashboard source lineage and stale-data warning.

## Output Structure

Use this structure for `Retail_Domain_SRS.md`:

1. Retail scope classification
2. Entity and state model
3. Source event catalogue
4. Functional requirements by capability cluster
5. Non-functional requirements
6. Interface requirements
7. Finance and control gates
8. Reporting and dashboard requirements
9. Acceptance tests
10. Traceability matrix

## Quality Gate

Before release, confirm:

- No requirement uses vague retail claims without source context.
- Every finance-triggering workflow has a finance/control gate.
- Every inventory-changing event has an audit trail and reconciliation route.
- Every price/promotion/markdown workflow has effective date, approval, rollback, and exception handling.
- Every dashboard metric has owner, formula, source, refresh cadence, and reconciliation status.
- Every requirement is testable with a deterministic pass/fail oracle.

## Evidence Basis

This skill operationalises the internal research project `umbrex-retail-playbooks-engine-enhancement` from the digital-research-engine. The Umbrex corpus is used as a taxonomy and project-scope evidence base; legal, statutory, accounting, tax, and market-size claims still require the relevant primary authority and reviewer route.
