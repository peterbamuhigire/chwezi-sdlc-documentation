# HR module requirements

Client-neutral. Use synthetic people in every example. Requirement identifiers use the
prefix `FR-HR-`. Statutory values appear only as parameters (see subsection 6).

## Subsection template

1. **Organisation and positions.** Units, cost centres, job families, levels, titles, grades, positions with status (planned, approved, vacant, filled, frozen, closed), reporting lines between positions.
2. **Employee master.** One person record; no title, unit or pay on it; assignments link person to position with dates and FTE share.
3. **Effective dating.** Dated rows, overlap and gap rules, corrections that preserve the superseded row, `as_of` reports.
4. **Contract classes.** Employee, part-time or fixed-term, consultant; class parameters; configurable consecutive-contract limit and break; human review prompt for disguised employment.
5. **Leave and time.** Dated policy, accrual, balance check at approval, cut-off.
6. **Statutory parameter register.** Fields `code, value, unit, valid_from, valid_to, instrument, section, checked_on, checked_by, status`; status `VERIFIED`, `NOT_VERIFIED` or `EXPIRED`; payroll blocks on any unset, unverified or expired row.
7. **Payroll inputs and run.** Input snapshot at cut-off, single payroll service, approval, payslips, payment file, finance posting; closed periods immutable.
8. **Workflows.** Recruitment, onboarding, leave, appraisal cycles, disciplinary, exit; states, transitions, who may act, named decider, reason on adverse steps.
9. **Access.** Role and field permissions; manager sees own reports only; medical data stored apart; staff view and request correction of own record.
10. **Personal data.** Purpose, lawful basis, retention, recipients per category; data protection officer; breach path; erasure or restriction path.
11. **Audit trail.** Append-only; change and sensitive-read records; HR administrators cannot edit.
12. **Document numbering.** Contracts, offer letters, payroll runs, cases, appraisal forms: contiguous per tenant and type, allocated at issue, voided not deleted.
13. **Reporting.** KPI card per report: question, formula, source, target, action, owner, backup.
14. **Go-live.** Payroll first, parallel run, reconciliation, then leave and time, then recruitment and appraisal; benefit review within 18 months.
15. **Machine output.** Advisory only: inputs shown, override allowed, human decider recorded.

## Requirement wording

```text
FR-HR-001 The system shall hold title, unit and grade on position and assignment rows and not on the person row.
FR-HR-002 The system shall reject an assignment whose date range overlaps another for the same person unless FTE shares total at most 100%.
FR-HR-003 The system shall read every statutory value from the parameter register and shall refuse a payroll run that touches an unset, NOT_VERIFIED or EXPIRED row, naming the parameter.
FR-HR-004 The system shall allow only the payroll service to write payroll result tables.
FR-HR-005 The system shall flag a fixed-term contract that would exceed the tenant's configured consecutive-contract limit and require a recorded decision by a named role.
FR-HR-006 The system shall allocate contract and payroll-run numbers contiguously per tenant and type inside the issuing transaction and shall void, never delete.
FR-HR-007 The system shall write an audit row for every change and every read of pay, disciplinary, medical and talent records.
FR-HR-008 The system shall show the inputs behind any machine shortlist or score and record the human who accepted or overrode it.
```

## Acceptance criteria patterns

| Criterion | Oracle | Test data |
| --- | --- | --- |
| Vacancy exists without a person | A position with status vacant appears in headcount and not in payroll | Synthetic unit, three positions, two staff |
| Title change keeps history | `as_of` a past date returns the old title and the old payslip reproduces | One synthetic promotion |
| Overlap rejected | Inserting an overlapping assignment fails with a named constraint | Two synthetic assignments |
| Unverified rate blocks payroll | Run with a `NOT_VERIFIED` row is refused naming the code | Synthetic parameter row |
| Cut-off respected | Leave approved after cut-off appears in the next period | Two synthetic requests |
| Closed period immutable | Update to a closed-period line fails; reopening needs a named approver and reason | Synthetic closed period |
| Single writer | Database grants show only the payroll service can write payroll tables | Grant listing |
| Access matrix | Each denied case returns refusal from the API, not only the screen | One synthetic user per role |
| Medical isolation | An HR administrator cannot read the medical store | Synthetic record |
| Audit completeness | A sensitive read produces an audit row with actor, role, record, time | Log extract |
| Numbering | 100 concurrent issues give a gap-free sequence; a voided number is retained | Concurrency test |
| Parallel run | Per-employee, per-component variance report with each variance explained and signed by the payroll owner | Old and new run on synthetic staff |
| Human decision | A shortlist cannot advance without a recorded human decider | Synthetic candidates |

## Statutory content

Only rows the owner marked VERIFIED on 10 Nov 2026 may be cited, and they were not
re-checked against the instruments: NSSF contributions (NSSF Act ss.11-12), Employment
Act ss.53, 55, 56, 57(3) and 65, Data Protection and Privacy Act ss.6 and 23, Tax
Procedures Code s.15. Everything else is `NOT_VERIFIED`: Employment (Amendment) Act
2025, Data Protection and Privacy Regulations numbers, Occupational Safety and Health
Act, the basis for withholding tax on part-time pay, severance, any disguised-employment
test. This reference does not certify compliance.
