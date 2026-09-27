---
phase: "02"
---
# Synthetic admissions requirements

This test-only fixture contains no patient names, identifiers, dates of birth, clinical facts, monetary amounts, jurisdiction claims, or production policy. The behaviors below are synthetic acceptance conditions for testing traceability; they are not client-approved requirements.

- **FR-001** The system shall deny an admissions request when the user lacks permission for its facility; traces to **BG-001**, **TC-001**, and decision **D-001**.

  **AC-001:** Given a user with no admission permission for facility F-B, when the user submits an admission request for F-B, then the system returns `ACCESS_DENIED` and the F-B intake-record count does not change.

- **FR-002** The system shall prevent a second patient record when a retry matches the synthetic identity key of an interrupted draft; traces to **BG-002**, **TC-002**, and decision **D-002**.

  **AC-002:** Given one interrupted draft for fixture key `SYNTH-001`, when a retry is submitted with that same key, then the patient-record count remains one.

- **FR-003** The system shall return the existing draft reference for authorized review when a retry matches an interrupted draft; traces to **BG-002**, **TC-002**, and decision **D-002**.

  **AC-003:** Given one interrupted draft for fixture key `SYNTH-001`, when a retry is submitted with that same key, then the existing draft reference is returned and no merge or identity adjudication occurs automatically.

- **FR-004** The system shall mark an intake `PENDING_REFERENCE_DATA` when a required reference-data lookup is unavailable; traces to **BG-002**, **TC-003**, and decision **D-003**.

  **AC-004:** Given the reference-data service is unavailable, when intake is submitted, then status is `PENDING_REFERENCE_DATA` and the draft remains retrievable.

- **FR-005** The system shall reject admission completion while required reference data is unavailable; traces to **BG-002**, **TC-003**, and decision **D-003**.

  **AC-005:** Given the reference-data service is unavailable, when admission completion is requested, then completion remains false.

- **FR-006** The system shall create a billing-handoff event only after an admission has a recorded sign-off; traces to **BG-003**, **TC-004**, and decision **D-004**.

  **AC-006:** Given an admission with no sign-off, when the billing handoff job runs, then no billing-handoff event is emitted and the admission remains awaiting review.

## Scope limits

These requirements test only the generic P11 flow. The identity-matching rule, authorized-review role, reference-data service contract, sign-off owner, and billing event contract require stakeholder decisions before any client specification. No fees, accounting treatment, insurer/payer rule, tax value, or statutory obligation is defined. Jurisdiction, clinical safety, and legal compliance are NOT_ASSESSED.
