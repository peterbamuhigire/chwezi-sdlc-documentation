# Data Quality Dimensions as Measurable NFRs

Parent skill: [05-conceptual-data-modeling](../SKILL.md).

Load when a data quality profile (Step 5) must become baselined, testable
non-functional requirements, or when a data contract, regulator, or AI feature
needs quality thresholds it can verify. [data-quality-rules.md](data-quality-rules.md)
defines the six working dimensions and their formulas; this file turns them
into `DQ-*` requirements with measurement windows, measurement points, and
breach responses, and maps them to ISO/IEC 25012 so nothing material is missed.

## Why the Six Dimensions Are Not Enough on Their Own

The six working dimensions (completeness, consistency, conformity, accuracy,
timeliness, uniqueness) describe the data's content. Consumers also depend on
properties the system provides around the data. ISO/IEC 25012 defines 15
characteristics, split into inherent and system-dependent ones; the Open Data
Contract Standard (ODCS) adds *coverage*. Use the crosswalk to check that the
SRS addresses each characteristic or records why it does not apply.

| ISO/IEC 25012 characteristic | Working dimension or NFR home | Typical `DQ-*` or NFR metric |
| --- | --- | --- |
| Accuracy | Accuracy | Sampled records matching the authoritative source, percent |
| Completeness | Completeness | Populated required fields, percent; records present versus source count |
| Consistency | Consistency | Records passing cross-entity rules, percent |
| Credibility | Accuracy (provenance) | Records with a verified source of record, percent |
| Currentness | Timeliness | Age of newest record at read time; p95 latency event-to-availability |
| Accessibility | Usability NFRs | Consumers able to read the interface through their declared channel |
| Compliance | Governance requirements | Fields carrying required classification, percent |
| Confidentiality | Security NFRs | Unauthorised read attempts succeeded: 0 |
| Efficiency | Performance NFRs | Query or export completion time at stated volume |
| Precision | Conformity | Values stored at the declared scale and unit, percent |
| Traceability | Lineage requirements | Records traceable to source and transformation, percent |
| Understandability | Data dictionary | Fields with an approved definition, percent |
| Availability | Service-level NFRs | Interface read success, percent over window |
| Portability | Interoperability NFRs | Successful export and re-import to the declared format |
| Recoverability | Backup and restore NFRs | Recovery point and recovery time achieved in restore test |
| Coverage (ODCS) | Completeness at population level | Real-world instances represented, percent of reference population |

## The `DQ-*` Requirement Pattern

Every data quality requirement shall state all nine elements. A requirement
missing any element is tagged `[VERIFIABILITY-FAIL]`.

| Element | Question it answers | Example |
| --- | --- | --- |
| Subject | Which dataset, entity, and attribute? | Loan Repayment interface, `amount` |
| Dimension | Which characteristic? | Conformity |
| Metric | What is counted, and how? | Records whose amount is a positive whole number, divided by all records |
| Population and exclusions | Which records count? | All records published in the window; test tenants excluded |
| Window | Over what period? | Each business day, 00:00 to 23:59 East Africa Time |
| Measurement point | Where is it measured? | At the published interface, not in the source system |
| Threshold | Pass value, with boundary rule | 100%; boundary at 100% passes |
| Method | Automated check, sampled review, or reconciliation | Automated check each day at 07:00 |
| Breach response | What happens, who acts, how fast | Publication halts for failing records; producing team notified within 15 minutes |

Template sentence:

> **DQ-<ID>** The `<subject>` shall achieve `<metric>` of `<threshold>` over `<window>`, measured at `<measurement point>`, excluding `<exclusions>`; a breach shall trigger `<response>` owned by `<role>`.

## Setting Thresholds Without Inventing Them

1. Start from the consumer decision the data supports and the cost of a wrong
   decision. Record both in the requirement's rationale.
2. Obtain a baseline: measure the current system or a representative sample.
   If no baseline exists, state `[CONTEXT-GAP: baseline for DQ-<ID>]` and set
   the requirement status to *proposed*.
3. Set the threshold at the level the most demanding legitimate consumer needs,
   not the level anyone asked for. Tighter targets cost disproportionately more
   and an unmet target erodes trust in every other target.
4. Separate *prevent* thresholds (records rejected at entry, target 100%) from
   *detect* thresholds (population-level measures reviewed on a schedule).
5. Record who accepted the threshold and on what date in the sign-off ledger.

## Criticality Tiers

Assign each dataset a tier; the tier fixes which elements are mandatory and how
often measurement runs. The client decides the tier, and the SRS records the decision.

| Tier | Typical data | Mandatory `DQ-*` coverage | Measurement cadence |
| --- | --- | --- | --- |
| 1 Regulated or financial | Ledger postings, tax submissions, clinical records, statutory returns | All six working dimensions plus traceability and recoverability | Each load or event, plus scheduled reconciliation |
| 2 Operational | Orders, stock movements, dispatch, bookings | Completeness, conformity, uniqueness, timeliness | Each load or event |
| 3 Analytical | Aggregates, dashboards, model features | Completeness, timeliness, consistency with tier 1 or 2 source | Each refresh |

## Statutory Anchor for Personal Data in Uganda

Section 15 of the Data Protection and Privacy Act, 2019 requires a data
collector, processor, or controller to ensure that personal data is complete,
accurate, up to date, and not misleading, having regard to the purpose of
collection or processing. Section 16 gives the data subject a right to request
correction. For any Uganda-scoped dataset containing personal data:

- Write at least one completeness, one accuracy, and one timeliness `DQ-*`
  requirement per personal-data entity, each justified by the processing purpose.
- Write a functional requirement for the correction request path, with a
  response time taken from the client's legal advice or the domain pack.
- Trace these requirements to the compliance annex produced by
  `dpia-generator` and to `domains/uganda/references/regulations.md`.

## Worked Examples (Illustrative Contexts)

**DQ-FARM-003 Completeness, coffee cooperative intake.** The Produce Intake
record shall have farmer identifier, collection centre, weight in kilograms,
and moisture reading populated for 100% of records accepted in each collection
day, measured at the point of intake submission; records missing any of these
fields shall be rejected at entry with a message naming the missing field.

**DQ-FARM-007 Uniqueness, farmer register.** The Farmer register shall contain
no more than 0.5% suspected duplicate farmers, measured monthly by the
duplicate-detection rule approved in the master data management assessment;
suspected duplicates shall be queued for the data steward, who shall resolve
each within 10 business days.

**DQ-CLINIC-012 Timeliness, outpatient visits.** 98% of outpatient visit
records created at a facility shall be available in the district reporting
dataset within 24 hours of the visit, measured weekly from visit time to
availability time; facilities without connectivity for the whole window are
reported separately, not excluded silently.

The numbers above illustrate structure. Every project sets its own thresholds
under the procedure above.

## Acceptance Checklist

- [ ] Every tier 1 and tier 2 dataset has `DQ-*` requirements for its mandatory dimensions.
- [ ] Every `DQ-*` requirement contains all nine elements.
- [ ] Every threshold has a baseline or a `[CONTEXT-GAP]` flag, and a named acceptor.
- [ ] The ISO/IEC 25012 crosswalk shows each characteristic addressed or marked not applicable with a reason.
- [ ] Uganda-scoped personal data carries section 15 quality requirements and a correction path.
- [ ] Measurement points are stated at the interface consumers read.

## Failure Modes

- "Data shall be of high quality." Fix: rewrite as `DQ-*` requirements with all nine elements.
- A percentage without a window or population. Fix: state both; the same data
  can pass daily and fail monthly.
- Measuring quality in the source system when consumers read a transformed
  copy. Fix: measure where the consumer reads, and optionally at source too.
- Silent exclusions that make a failing feed look healthy. Fix: list exclusions
  and report excluded volume.
- Copying the thresholds from this file. Fix: derive from the client's
  baseline and decisions.

## Evidence/currentness

Access date: 2026-09-24.

- ISO/IEC 25012:2008 is the edition cited by current secondary sources, with
  15 characteristics split into inherent and system-dependent groups. The
  iso.org catalogue page refused automated access, so its current review status
  is `NOT_ASSESSED`; confirm on iso.org before citing a confirmation year.
- ODCS v3.2.0 quality dimensions (`accuracy`, `completeness`, `conformity`,
  `consistency`, `coverage`, `timeliness`, `uniqueness`) checked against
  `schema/odcs-json-schema-v3.2.0.json` (bitol-io/open-data-contract-standard, release 2026-09-08).
- Uganda Data Protection and Privacy Act, 2019 (Act 9 of 2019), sections 15
  and 16, checked against the Laws.Africa/ULII text as at 2019-05-03. A
  consolidated version dated 2023-12-31 is listed; renumbering there is `NOT_ASSESSED`.
- DAMA-DMBOK: DMBOK 3.0 is in active development and not published (dama.org
  DMBOK 3.0 project page; kick-off 2025-06-25). The second edition (DMBOK2)
  remains the published reference; the existence of a 2024 revision is reported
  by secondary sources only and is `NOT_ASSESSED`. Do not cite DMBOK 3.0 as a standard.

Sources: Jones (2023) *Driving Data Quality with Data Contracts*; ISO/IEC 25012:2008;
Bitol project, ODCS v3.2.0 (2026); Uganda Data Protection and Privacy Act, 2019.
