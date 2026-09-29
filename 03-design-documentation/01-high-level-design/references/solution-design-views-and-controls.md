# Solution Design Views and System Controls

Parent skill: [01-high-level-design](../SKILL.md). Load this reference when the HLD must show
that every requirement is realised across the experience, process, data and security views, and
that system controls (input, output, data quality, process, workflow, privacy, security) are
designed rather than assumed. It supplements the component, deployment and data-flow steps of
the parent skill; module internals stay in `02-low-level-design`, schemas in `04-database-design`,
and screen specifications in `05-ux-specification`.

## 1. Design objectives traceable to requirements

State design objectives in the current quality vocabulary so testers and auditors read them the
same way.

| Source | Characteristics to map | Use in the HLD |
|---|---|---|
| ISO/IEC 25010:2023 product quality | Functional suitability, performance efficiency, compatibility, interaction capability (formerly usability; now includes inclusivity, self-descriptiveness, user engagement), reliability (faultlessness replaces maturity), security, maintainability, flexibility (formerly portability), safety | One row per characteristic that a requirement drives, with the design decision and the verification method |
| ISO/IEC 25019:2023 quality in use | Beneficialness, freedom from risk, acceptability | Outcome targets for critical journeys; link to acceptance tests and post-launch measures |

Correction to older sources: effectiveness, efficiency and satisfaction as the quality-in-use set
come from ISO/IEC 25010:2011; do not cite them as ISO/IEC 25019:2023 characteristics.

Decision rule: an objective that no requirement drives ("the system shall be flexible") is removed
or turned into a concrete, testable property (configurable tax rates without redeploy; second
database engine supported behind the persistence interface).

Record constraints in three groups and cite each in the ADR it shapes: project (budget, timescale,
skills), technical (platform, legacy systems, mandated standards), organisational (regulation,
stakeholders, culture, requirement quality).

## 2. The four views and what each must show

| View | Must show | Acceptance condition |
|---|---|---|
| Experience | Inputs and outputs per actor and channel (web, mobile, USSD, SMS, print, API), device and connectivity assumptions, accessibility target | Every functional requirement with a human actor maps to at least one input or output; channel choice justified by actor context |
| Process | Solution-level components and interfaces; per critical use case a sequence of component interactions covering main, alternative and failure paths | Each interface names service, parameters and return type; each use case step lands on exactly one owning component |
| Data | Conceptual-to-logical model, data at rest vs in transit, structured vs unstructured, transactional vs analytical stores, retention | Every entity has an owning component; every cross-component flow names its format and protection |
| Security and control | The control catalogue in section 3, trust boundaries, identity and authorisation model | Every control is traced to a risk or requirement and has a verification method |

Use the POPIT check before closing the HLD: for each major decision ask what changes for People,
Organisation, Processes, Information and Technology. A control that depends on a role or procedure
the client has not agreed to create is a risk, not a control.

## 3. System control catalogue

Specify controls as requirements the design must honour; build detail belongs to engineering.

**Input controls**
- Verification (captured accurately): double entry for critical values, check digits on
  account-style codes, confirmation screens before commit, control totals (record count, hash
  total, financial total) for batch and file imports.
- Validation (plausible and consistent): type, length and format, existence (mandatory and
  reference-data lookup), range, cross-field consistency.
- Hostile input: parameterised queries, output encoding, and prompt-injection containment for any
  field that reaches a language model.
- Localisation trap: name, phone and address rules must accept real local forms. Uganda examples:
  names with apostrophes or multiple parts (Nakato-Ssempijja, O'Kello), +256 numbers entered with
  or without the leading 0, and addresses expressed as village, parish and landmark rather than
  street numbers. Over-strict validation is a defect, not a control.

**Output controls**: format, completeness and accuracy checks before release; recipient
authorisation; encryption in transit; monitoring for anomalous volumes; a route for recipients to
report wrong output.

**Data quality controls**: map to the data-quality dimensions and thresholds already defined in
`02-requirements-engineering/fundamentals/during/05-conceptual-data-modeling/references/data-quality-rules.md`;
add uniqueness (keys and duplicate detection), integrity (referential and business-rule), and
timeliness (maximum data age per use). Tamper evidence uses hashes or signatures where integrity
is contractual.

**Process controls**: business rules shown as guard conditions in activity or sequence models
(for example, "payment retried at most three times, then the order is abandoned").

**Workflow controls**: a state machine per core business object (order, invoice, claim, loan)
listing every state, permitted transition, triggering actor and automatic transition (archive after
one year, purge after the retention period). Each forbidden transition becomes a negative test.

**Privacy controls**: data minimisation, purpose limitation, consent capture and withdrawal,
data-subject request handling, retention and deletion, masking, pseudonymisation and tokenisation.
For Uganda, route to `dpia-generator`; for other jurisdictions cite the
applicable law in force.

**Security controls**: least-privilege role model, strong authentication (MFA for privileged and
financial actions), encryption at rest and in transit including backups, logging and monitoring of
access, backup and restore targets (RPO, RTO), incident response ownership, secure development and
security testing obligations. For AI components add prompt-injection, data-poisoning and
output-handling controls.

## 4. Anti-patterns and corrections

- Controls listed as a generic checklist. Correction: each control names the risk, the component
  that enforces it and the test.
- Happy-path sequence diagrams only. Correction: add alternative and failure paths for every
  critical use case.
- Order or loan status held as free text. Correction: a state machine with permitted transitions.
- "Secure" without a standard. Correction: cite the control framework and version in force.
- Data view drawn once for the database only. Correction: include data in transit and exports.

## 5. Worked example (original)

A Gulu agro-input distributor's order system. Experience view: shop agents order on Android with
intermittent connectivity; farmers confirm by USSD; head office prints delivery notes. Process view:
`OrderService` exposes `createOrder(agentId, lines) -> orderNo`; offline orders queue on the device
and sync with an idempotency key. Workflow control: Draft -> Submitted -> Paid -> Picked ->
Dispatched -> Delivered, with cancellation allowed only before Dispatched. Input control: the
mobile-money reference is checked against the payment provider callback before the order moves to
Paid; nightly settlement import is reconciled with record count and financial total. Privacy
control: farmer phone numbers are masked for agents after delivery.

## Evidence/currentness

Access date 2026-09-24. Verified: ISO/IEC 25010:2023 renamed usability to interaction capability
and portability to flexibility, added safety, and replaced user interface aesthetics and maturity
with user engagement and faultlessness (ISO catalogue preview; arc42 quality-model summary);
ISO/IEC 25019:2023 quality-in-use characteristics are beneficialness, freedom from risk and
acceptability (ISO OBP). Security frameworks to cite at current versions: ISO/IEC 27001:2022, NIST
CSF 2.0 (2024), OWASP Top 10 (confirm the current edition at owasp.org before citing) —
edition currency beyond these was NOT_ASSESSED in this pass.

Sources: Thompson (2025) *Designing Digital Solutions*, BCS; ISO/IEC 25010:2023; ISO/IEC 25019:2023;
DAMA International (2017) *DMBOK*.
