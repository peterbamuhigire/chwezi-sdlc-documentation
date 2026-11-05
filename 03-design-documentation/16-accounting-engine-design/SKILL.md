---
name: 16-accounting-engine-design
description: Use when approved money-flow requirements need SDS/HLD/LLD for an embedded accounting engine with append-only journals, posting service, periods, reversals, idempotency, subledgers, rebuilds and audit trail; consult the finance doctrine and use database-design for general persistence.
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---
# Accounting Engine Design
<!-- dual-compat-start -->
## Use When

- An approved SRS contains sales, payments, inventory, payroll, tax, assets or reporting that must post to a ledger.

## Do Not Use When

- Do not use to invent accounting policy, tax treatment, chart mappings or IFRS conclusions; obtain finance-doctrine and authorised accountant evidence.

## Required Inputs

| Artefact | Source or provider | Required? | Missing behaviour |
|---|---|---|---|
| Approved finance requirements and finance-doctrine decisions | SRS and canonical finance engine | Required | Stop if posting rules, reporting basis or statutory treatment are unresolved. |
| HLD, source events, tenancy and period controls | Architecture, domain and finance owners | Required | Return a design-gap register when event or control ownership is missing. |

## Workflow

1. Read the named inputs and confirm their approval, version and unresolved decisions.
2. Apply the decision rules below before drafting; stop on a missing authority, unsafe assumption or unresolved scope driver.
3. Produce the Accounting Engine Design and finance quality-gate evidence through the existing domain procedure and load only the references needed for the chosen branch.
4. Trace each material statement in the Accounting Engine Design and finance quality-gate evidence to an input, decision or explicitly qualified assumption.
5. Verify the observable acceptance conditions, record unassessed checks, and hand the artefacts to their named consumers.
6. If validation fails, recover by correcting the source decision or artefact and rerun the affected check; do not weaken the acceptance condition.

## Outputs

| Artefact | Consumer | Observable acceptance condition |
|---|---|---|
| Accounting Engine Design and finance quality-gate evidence | Finance, backend, data, audit, test and operations teams | Every source event maps through one posting service to balanced immutable journals; idempotency, reversal, period, rebuild, tenancy and audit tests are specified. |

## Evidence Produced

| Evidence | Consumer | Acceptance condition |
|---|---|---|
| Source and decision trace | Reviewer and downstream owner | Each material statement cites an approved input, named decision or qualified open issue. |
| Completed verification record | Release or phase gate owner | Every applicable check records pass/fail; unavailable checks remain `not assessed`. |

## Capability and permission boundaries

Read-only is the default for analysis, review, evaluation and planning. Read and search access to authorised project artefacts are required. Editing is limited to an explicitly requested project deliverable. Execution may run document, syntax or validation checks. Network access is used only for facts that require current verification. Do not publish, spend, change production, approve policy, or claim certification without explicit authority.

## Degraded mode

If any required capability is unavailable, return the narrowest useful qualified Accounting Engine Design and finance quality-gate evidence draft plus a gap register showing the missing item, affected sections, risk and owner. Never convert an unassessed check into a pass.

## Decision Rules

| Choice | Action | Failure or risk avoided |
|---|---|---|
| Financial event is approved and postable | Create balanced journal through LedgerPostingService | Subledgers cannot bypass controls |
| Period is closed or event is duplicate | Reject or route authorised reversal/adjustment | Ledger history remains immutable |

## Quality Standards

- Preserve repository terminology and trace every material choice to project context.
- Use deterministic acceptance conditions; replace vague quality claims with an observable check, threshold or named approval.
- Cover error, empty, edge, recovery and operational cases relevant to this skill.
- Verify standards, citations, APIs and package names before relying on them; qualify what cannot be checked.
- Stop release for a failed safety, security, legal, financial, accessibility or data-integrity gate.

## Anti-Patterns

- Writing directly from sales tables to ledger tables. Fix: use the posting service and mapping rules.
- Updating a posted journal. Fix: create an authorised reversal and replacement.
- Storing a balance with no rebuild path. Fix: derive and reconcile it from journal lines.
- Omitting idempotency on event consumption. Fix: enforce a source-event key.
- Inventing debit/credit mappings. Fix: require finance-doctrine approval and traceable configuration.

## References

- [Database Design neighbour](../04-database-design/SKILL.md)
- [Finance engine router](../../AGENTS.md#finance--accounting-trigger)
- [Document numbering requirements](../../02-requirements-engineering/references/document-numbering-requirements.md)
<!-- dual-compat-end -->




## Use When

- The approved SRS includes money-handling or embedded accounting requirements.
- A design document must specify the accounting write path, schema, services, reports, and invariants.

## Hard Rules

- NEVER design a direct write path from sales, inventory, payroll, payments, or assets into ledger tables.
- NEVER design mutable posted journals.
- MUST show how materialized balances rebuild from journal lines.
- MUST include `tenant_id` on accounting tables unless explicitly single-tenant.
- MUST number journals and source documents from the single document-number allocator, inside the posting transaction, contiguous per tenant and type.

## Canonical Data Model

Required tables:

- `chart_of_accounts`
- `account_mappings`
- `posting_rule_versions`
- `journal_entries`
- `journal_lines`
- `accounting_periods`
- `accounting_integrity_runs`
- `accounting_audit_log`

Recommended supporting tables:

- `tax_rates`
- `exchange_rates`
- `inventory_cost_layers`
- `fixed_assets`
- `payroll_runs`
- `bank_accounts`
- `funds` for NGOs and donor-funded projects

## LedgerPostingService Interface

```php
interface LedgerPostingService
{
    public function post(JournalEntry $entry): PostedJournal;
}
```

The design shall document validations for debit-credit equality, tenant scope, open period, active accounts, idempotency key, source document state, mapping completeness, currency policy, and database transaction boundaries.

## Design Sections To Produce

1. Accounting context and standard profile.
2. Service boundaries and event producers.
3. Account resolver and mapping tables.
4. Posting service contract.
5. Database schema and constraints.
6. Reversal and correction workflow.
7. Period close and lock workflow.
8. Subledger and control-account reconciliation.
9. Report projection and cache rebuild strategy.
10. Audit trail and tamper-evidence strategy.
11. Operational jobs: nightly integrity, report rebuild, FX revaluation, depreciation, payroll remittance checks.

## Outputs

- SDS/HLD/LLD accounting-engine section.
- ERD/table specification.
- Service interface and sequence diagram text.
- Reconciliation and report rebuild design.
