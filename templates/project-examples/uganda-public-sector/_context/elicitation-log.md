# Elicitation Log — Section Approvals and Review Focus (sample)

> Sample rows. Replace them with the engagement's own approvals and conditions before any
> deliverable is generated. Method: `02-requirements-engineering/fundamentals/before/02-elicitation-toolkit/references/ceremony-and-section-approval.md`
> and `02-requirements-engineering/fundamentals/during/07-requirements-validation/references/review-focus.md`
> in the SRS engine.

## Ceremony classification

| Engagement | Class | Stated to owner | Confirmed by | Date |
|---|---|---|---|---|
| District trading-licence renewal service | Architectural (new system) | 2026-09-01 | Service owner | 2026-09-01 |

## Section approvals

Approval covers only the section named in the row. Later sections do not inherit it.

| Section | Title | Presented | Outcome | Approver | Date | Conditions |
|---|---|---|---|---|---|---|
| 3.1 | External interfaces | 2026-09-08 | Approved | Service owner | 2026-09-09 | None |
| 3.2 | Functional requirements — licence renewal | 2026-09-15 | Approved with conditions | Service owner | 2026-09-17 | Confirm the late-payment penalty rule with the Finance reviewer |
| 3.3 | Performance and availability | 2026-09-22 | Returned for correction | Accounting Officer | 2026-09-23 | Restate the availability target for the end-of-quarter renewal peak |

## Review Focus

| No. | Implied condition | Why it matters | Acceptance criterion | Disposition | Owner |
|---|---|---|---|---|---|
| RF-1 | A mobile-money renewal fee is reversed by the network operator after the licence has been issued | A licence stays valid although the fee was never received | Given an issued licence whose fee is later reversed, when the reversal is received, then the system shall suspend the licence within one working day and notify the trader by SMS | New requirement | Finance reviewer |
| RF-2 | A trader renews while an enforcement notice is open against the premises | The council issues a licence it is legally obliged to withhold | Given an open enforcement notice on the premises, when a renewal is submitted, then the system shall hold the application for the enforcement officer's decision and shall not issue the licence | Clarification of the renewal eligibility rule | Service owner |
| RF-3 | A citizen asks for their renewal record to be corrected under the Data Protection and Privacy Act 2019 | A correction that overwrites the record destroys the audit trail | Given an approved correction request, when the officer applies it, then the system shall record the corrected value as a new version and retain the original with the request reference | Accepted risk until the records-retention schedule is approved | Accounting Officer |
