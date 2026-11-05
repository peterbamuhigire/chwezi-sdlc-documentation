---
name: 18-embedded-accounting-engine-srs
description: "Use when specifying software that touches money, inventory value, payroll, tax, grants, payments, assets, or financial reports; use the finance doctrine for accounting policy and current statutory facts."
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---

# Embedded Accounting Engine SRS

<!-- local-contract-start -->
<!-- dual-compat-start -->
## Use When

- specifying software that touches money, inventory value, payroll, tax, grants, payments, assets, or financial reports; use the finance doctrine for accounting policy and current statutory facts.
- Use this procedure when the required source artefacts are available and `Embedded accounting engine SRS` is the next lifecycle deliverable.

## Do Not Use When

- Use `finance-module-audit` when that neighbouring route owns the decision or deliverable.
- Do not invent missing project evidence, standards clauses, thresholds, or stakeholder decisions.

## Required Inputs

| Artefact | Source or provider | Required? | Behaviour when missing |
| --- | --- | --- | --- |
| Money-flow map, reporting framework, jurisdiction, roles, and finance doctrine baseline | Project context, finance owner, and canonical finance doctrine | Yes | Stop the affected step, name the missing source, and return only a qualified gap record. |

## Workflow

1. Inspect the required inputs and log the exact sources, versions, and unresolved assumptions.
2. Apply this skill's existing domain workflow and decision rules to produce `Embedded accounting engine SRS`.
3. Stop when a required source, accountable decision owner, or deterministic test oracle is absent.
4. Recover by preserving valid work, marking the blocked scope, and returning the narrowest qualified artefact plus the next evidence needed.

## Outputs

| Artefact | Consumer | Acceptance condition |
| --- | --- | --- |
| Embedded accounting engine SRS | Architecture, finance, implementation, test, and audit owners | Required sections are populated, source links resolve, and every material requirement or decision has an observable review or test oracle. |

## Evidence Produced

| Evidence | Reviewer | Acceptance condition |
| --- | --- | --- |
| Source, decision, trace, and validation record for `Embedded accounting engine SRS` | Requirements quality reviewer | Inputs used, decisions made, checks run, failures, and unassessed items are explicit. |

## Capability and permission boundaries

Read and search are required. Editing is allowed only when the request authorises creation or repair of the named requirements artefact. Publishing, production mutation, destructive action, spending, and certification require explicit authority.

## Degraded mode

Fallback: if a required file, reviewer, standard source, network check, renderer, or execution capability is unavailable, return the narrowest useful qualified result and mark the affected check `not assessed`; never convert an unassessed check into a pass.

## Decision Rules

| Choice or condition | Action | Failure or risk avoided |
| --- | --- | --- |
| A money flow bypasses the approved posting service or lacks a control-account tie-out | Block release and add ledger, reversal, reconciliation, and evidence requirements. | Broken double entry, misstated reports, or unauditable transactions. |
| Required inputs and test oracles are complete | Continue through the existing workflow and record evidence. | A deliverable whose acceptance cannot be reproduced. |
| A mandatory source or owner is missing | Stop the affected branch and issue a qualified gap record. | Fabricated context or unauthorised decisions. |

## Quality Standards

- Preserve stable identifiers and bidirectional traceability from project evidence to `Embedded accounting engine SRS` and its acceptance checks.
- Apply ISO/IEEE measures only with a named metric, method, threshold, evidence source, and responsible reviewer; run the anti-slop gate before release.

## Anti-Patterns

- Producing `Embedded accounting engine SRS` from assumed context. Fix: cite the project source or mark the scope blocked.
- Accepting a material requirement without a deterministic oracle. Fix: add a measurable result, boundary, and verification method.
- Crossing into `finance-module-audit` without routing the decision. Fix: hand off the named input and preserve trace links.
- Treating an unavailable check as passed. Fix: mark it `not assessed` and state the release consequence.
- Claiming standards, statutory, or stakeholder approval without evidence. Fix: cite the source and reviewer or qualify the claim.

## References

- [Skill authoring and release standard](../../docs/skill-authoring-standard.md)
- [Document numbering requirements](../references/document-numbering-requirements.md): load for subsection 11.
<!-- dual-compat-end -->
<!-- local-contract-end -->

## Use When

- The system records sales, expenses, inventory, payroll, school fees, clinic billing, grants, donations, payments, loans, assets, wallets, or tax.
- The SRS must prove the product can replace routine external bookkeeping software for the operating entity.

## Do Not Use When

- The product only exports data to an external accounting system and never owns the books.
- Accounting treatment depends on a current law, tax rate, or professional judgement not provided in the brief; write a verification requirement instead of inventing the answer.

## Required SRS Subsections

Add these to functional requirements for every money-handling system:

1. Accounting standard and compliance profile: IFRS for SMEs by default, full IFRS where required, or project-specific local GAAP.
2. Chart of accounts: tenant-specific CoA cloned from an industry template, account types, control accounts, status, currency, and report rollups.
3. Mapping layer: product categories, expense categories, payment methods, tax rates, payroll components, asset categories, donor funds, and inventory categories mapped to accounts.
4. Posting engine: one `LedgerPostingService` write path, idempotency key, period validation, account validation, debit-credit validation, and atomic database transaction.
5. Journal model: append-only `journal_entries` and `journal_lines`; no edits or soft deletes; reversing journals only.
6. Subledgers: AR, AP, inventory, fixed assets, payroll, tax, bank/mobile money, grants/funds implemented through tagged journal lines or reconciled registers.
7. Accounting periods: open, closed, locked states; no posting to locked periods except approved reopening workflow.
8. Reports: trial balance, income statement, statement of financial position, cash flow statement, statement of changes in equity/net assets, GL detail, ageing, tax schedules, inventory valuation, payroll liabilities, fixed asset register, donor/fund reports where relevant.
9. Integrity invariants: balanced entries, control-account reconciliation, inventory tie-out, period enforcement, idempotency enforcement, tenant isolation, rebuildable balances.
10. Audit trail: actor, timestamp, source document, posting rule version, mapping changes, CoA changes, reversals, exports, and close approvals.
11. Document numbering: contiguous per tenant and document type for source documents and journals, voided not deleted, with credit notes and platform invoices on their own series ([standard](../references/document-numbering-requirements.md)).

## Requirement Wording Pattern

Use testable requirements:

```text
FR-ACC-001 The system shall post every accounting entry through a single LedgerPostingService.
FR-ACC-002 The system shall reject any journal entry whose total debits do not equal total credits.
FR-ACC-003 The system shall prevent updates, deletes, or soft deletes of posted journal lines.
FR-ACC-004 The system shall correct posted accounting errors only by posting reversing journals linked to the original journal.
FR-ACC-005 The system shall run a nightly per-tenant accounting integrity check and alert operators on failure.
```

## Compliance And Standards Template

```text
Accounting standard: IFRS for SMEs / full IFRS / local GAAP: [fill in]
Functional currency: [fill in]
Presentation currency, if different: [fill in]
Tax regime: [fill in]
VAT/sales tax regime: [fill in]
Payroll statutory regime: [fill in]
External sign-off required: statutory audit / tax filing / donor audit / board approval: [fill in]
Current-rate verification owner: [role/person]
```

## Outputs

- SRS accounting-engine functional requirements.
- Compliance and standards section.
- Requirements traceability entries for accounting invariants.
- Open verification items for current tax/regulatory rates.
