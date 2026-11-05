# Accounting Requirements Gate

Use this reference when an SRS, BRD, architecture, data model, or test plan involves money, accounting, billing, POS, ERP, inventory, payroll, grants, loans, subscriptions, tax, or management reporting.

## Required Requirement Families

| Family | Requirements to elicit and specify |
|---|---|
| Business events | Sales, receipts, purchases, payments, refunds, credit notes, inventory movements, payroll, loans, tax, fixed assets, journals, adjustments |
| Accounting engine | Chart of accounts, posting rules, balanced journals, subledgers, control accounts, fiscal periods, reversals, period close |
| Source documents | Invoice, receipt, bill, PO, GRN, delivery note, stock count, timesheet, payroll run, bank/mobile money statement, tax return evidence |
| Management accounting | Cost centers, profit centers, projects, branches, cost drivers, budgets, variance reports, contribution margin, break-even |
| Controls | Segregation of duties, maker-checker approvals, audit logs, role permissions, document numbering (contiguous per tenant and type; see `02-requirements-engineering/references/document-numbering-requirements.md`), closed periods, exception handling |
| Reconciliations | Bank/mobile money, AR, AP, inventory, payroll, tax, loans, fixed assets, intercompany where relevant |
| Reporting | Trial balance, GL, P&L, balance sheet, cash flow, aging, inventory valuation, tax schedules, management accounts, dashboards |
| Compliance | IFRS/local GAAP basis, VAT/sales tax, payroll taxes, withholding, record retention, privacy, audit evidence |

## Functional Requirement Patterns

- The system shall create balanced journal entries automatically for every posted financial business event.
- The system shall prevent deletion or direct editing of posted entries and shall correct them only through reversals or approved adjustment entries.
- The system shall reconcile each subledger control balance to the general ledger for each fiscal period.
- The system shall prevent transactions from posting into a closed period except through an approved reopening or adjustment workflow.
- The system shall store source-document evidence and link it to the accounting event, posting, approval, and report line.
- The system shall maintain cost center, profit center, project, branch, product, customer, supplier, and tax dimensions where relevant to management reporting.
- The system shall produce period-end financial statements that can be regenerated from the underlying transactions and journals.

## IFRS-Aware Elicitation

Ask whether the system must support:

- Accrual accounting or cash basis.
- Revenue recognition rules by product, service, contract, subscription, milestone, delivery, or usage.
- Inventory costing method and net realizable value review.
- Depreciation, impairment, disposal, and asset custody.
- Leases, loans, interest, effective-rate calculations, provisions, and contingent obligations.
- Foreign currency transactions and remeasurement.
- Consolidated reporting, intercompany transactions, eliminations, and non-controlling interests.
- Fair-value, impairment, revaluation, and write-down workflows for balances that cannot remain at simple historical cost.
- Accounting-policy, estimate-change, and prior-period-error workflows if statutory reporting or audit readiness is required.

## Cost And Control Requirements

- For manufacturing, processing, logistics, and inventory-heavy systems, specify job/process/hybrid costing, bill of materials, yield, scrap, rework, overhead absorption, variance analysis, and production capacity.
- For service businesses, specify project costing, timesheets, utilization, recoverable expenses, WIP, deferred revenue, and milestone billing.
- For branches/franchises, specify transfer pricing, interbranch transfers, responsibility-center reporting, and branch P&L.
- For donor/grant work, specify fund accounting, budget line controls, eligible cost checks, expenditure evidence, and restricted-fund reporting.
- For group or multi-entity systems, specify intercompany invoicing, settlement, elimination, consolidation adjustments, ownership percentages, non-controlling interests, and group reporting packs.
- For loan, lease, or investment modules, specify amortization schedules, effective interest, principal/interest splits, current/non-current classification, covenants, and maturity reporting.

## Acceptance Criteria

- Posting tests prove debit total equals credit total for each event and batch.
- Trial balance, subledger reports, and financial statements reconcile for a sample period.
- Reversal tests prove the audit trail remains intact and balances reverse correctly.
- Role tests prove users cannot approve their own high-risk transactions.
- Period-close tests prove late transactions are blocked or routed to approved adjustments.
- Report tests prove figures trace from source document to journal to ledger to statement.
