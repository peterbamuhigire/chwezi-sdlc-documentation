# Review Focus

A Review Focus table records the conditions a requirement set implies but does not state. It is the
last step of validation before a baseline decision. Inspection finds defects in what was written;
Review Focus finds what was left unwritten.

## What qualifies as an implied condition

An implied condition is a situation that the stated requirements make possible, that a stakeholder
would expect the system to handle, and that no requirement, business rule or test case yet covers.
Typical sources:

- **Reversal and failure paths.** A payment, approval or submission that is cancelled, reversed or
  interrupted part-way (for example, reversal of a mobile-money payment made while the device was
  offline).
- **Boundary states.** An actor who holds two roles, a record created before a rule came into force,
  or a period that closes while a transaction is open.
- **Concurrency.** Two users acting on the same record, or a retry arriving after the original has
  succeeded.
- **Data lifecycle.** Retention expiry, archival, correction of a submitted statutory record, or a
  data-subject request under the Data Protection and Privacy Act 2019.
- **Environment.** Loss of connectivity, a failed external service, or a clock that differs between
  device and server.

## How to build the table

1. Read the functional requirements, business rules and test oracles together.
2. For each critical flow, ask what happens when the flow is interrupted, reversed, repeated or
   started from an unexpected state. Keep only conditions with no covering requirement or test.
3. Rank the candidates by consequence (harm to a person, money, statutory standing, then
   operational cost) and keep at most five.
4. Write one row per condition with the columns below.
5. Record the disposition agreed with the owner.

| Column | Content |
| --- | --- |
| No. | `RF-1` to `RF-5` |
| Implied condition | The unstated situation, in one sentence |
| Why it matters | The consequence if the system does not handle it |
| Acceptance criterion | A testable statement of correct behaviour, in the same form as a test oracle |
| Disposition | New requirement (cite the new ID), clarification (cite the amended ID), or accepted risk |
| Owner | The accountable person or role; an accepted risk always names one |

## The cap of five

The cap keeps the review on the conditions with the largest consequence. If more than five
candidates survive step 2, the requirement set is not ready for validation: stop, record the
candidates in the elicitation log, and return to `02-elicitation-toolkit` for another
decision-frontier round. Do not raise the cap to accommodate them.

## Worked rows

| No. | Implied condition | Why it matters | Acceptance criterion | Disposition | Owner |
|---|---|---|---|---|---|
| RF-1 | A cashier's mobile-money payment is reversed by the network operator after the device queued it offline | The ledger shows income that was never received | Given a queued payment later reversed by the operator, when the device synchronises, then the system shall post a reversing entry within 60 seconds and flag the receipt as void | New requirement | Finance Manager |
| RF-2 | A supervisor who is also a cashier approves their own refund | Segregation of duties is defeated | Given a refund raised by user U, when U attempts to approve it, then the system shall refuse the approval and log the attempt | Clarification of the refund-approval rule | Internal Audit |
| RF-3 | A receipt is corrected after it has been reported to the tax authority | The statutory record and the ledger diverge | Given a reported receipt, when a correction is saved, then the system shall issue a credit note linked to the original and shall not alter the original record | Accepted risk until the e-invoicing interface is specified | Tax Accountant |

## Attribution

Ceremony classification, section-scoped approval and Review Focus adapted from Superpowers (MIT,
https://github.com/obra/superpowers, commit 8ca22dba9a94f28898bbce59f2537ff4d87c747d). Paraphrased.
