---
document: agent-build-brief
derived_from: approved-srs
source_project: "healthcare_admissions"
---
# Agent build brief: healthcare_admissions

> Generated from the approved SRS; regenerate, never hand-edit. This brief is an
> internal agent artefact. It does not replace or amend the SRS: where the two
> differ, the SRS governs. Every entry ends with its source in parentheses; an
> entry that could not be traced carries a `CONTEXT-GAP` marker, which the
> kernel's blocking-marker gate reports until the source document is completed.
>
> Six-area brief structure adapted from addyosmani/agent-skills `/spec` (MIT,
> https://github.com/addyosmani/agent-skills, commit 2686b62). Paraphrased.
>
> Regenerate with `python scripts/create_agent_build_brief.py --project <project-dir>`.

## 1. Objective

- Enforce admissions access at the facility assigned to the user. (BG-001, _context/vision.md)
- Avoid creating duplicate patient records when intake is interrupted. (BG-002, _context/vision.md)
- Preserve completed admission review before a billing handoff is emitted. (BG-003, _context/vision.md)

## 2. Commands

- [CONTEXT-GAP: no build or run commands are recorded] (expected in the SRS operating or development environment section)

## 3. Structure

- Design view: System context, shown in FIG-001 (03-design-documentation/01-high-level-design/hld.md § 1. System context)
- Design view: Interrupted intake retry, shown in FIG-002 (03-design-documentation/01-high-level-design/hld.md § 2. Interrupted intake retry)
- Design view: Intake lifecycle, shown in FIG-003 (03-design-documentation/01-high-level-design/hld.md § 3. Intake lifecycle)

## 4. Conventions

- [CONTEXT-GAP: no coding conventions are recorded] (expected in 04-development-artifacts/ coding guidelines)

## 5. Testing

- [CONTEXT-GAP: no test commands are recorded] (expected in a Test commands section of the test plan or SRS environment section)
- TC-001 Facility-scope denial verifies FR-001; expected result: ACCESS_DENIED is returned and F-B intake-record count is unchanged. (TC-001, 05-testing-documentation/TC-001-facility-denial.md)
- TC-002 Interrupted intake duplicate verifies FR-002, FR-003; expected result: Existing draft reference is returned and the patient-record count remains one. (TC-002, 05-testing-documentation/TC-002-interrupted-duplicate.md)
- TC-003 Unavailable reference data verifies FR-004, FR-005; expected result: Draft remains retrievable with status PENDING_REFERENCE_DATA and completion is false. (TC-003, 05-testing-documentation/TC-003-unavailable-reference-data.md)
- TC-004 Missing sign-off blocks handoff verifies FR-006; expected result: No billing-handoff event is emitted and admission remains awaiting review. (TC-004, 05-testing-documentation/TC-004-missing-signoff.md)

## 6. Boundaries

### Always

- FR-001: The system shall deny an admissions request when the user lacks permission for its facility (FR-001, 02-requirements-engineering/requirements.md)
- FR-002: The system shall prevent a second patient record when a retry matches the synthetic identity key of an interrupted draft (FR-002, 02-requirements-engineering/requirements.md)
- FR-003: The system shall return the existing draft reference for authorized review when a retry matches an interrupted draft (FR-003, 02-requirements-engineering/requirements.md)
- FR-004: The system shall mark an intake `PENDING_REFERENCE_DATA` when a required reference-data lookup is unavailable (FR-004, 02-requirements-engineering/requirements.md)
- FR-005: The system shall reject admission completion while required reference data is unavailable (FR-005, 02-requirements-engineering/requirements.md)
- FR-006: The system shall create a billing-handoff event only after an admission has a recorded sign-off (FR-006, 02-requirements-engineering/requirements.md)

### Ask first

- Any change to a baselined requirement or its acceptance criterion (change control, _registry/change-impact.yaml)
- D-005 (OPEN CONFLICT - NOT APPROVED): One draft says “billing handoff only after sign-off”; a contradictory draft says “billing handoff before sign-off”. (D-005, 03-design-documentation/decision-log.md)
- D-006 (OPEN - NOT APPROVED): No sign-off record is supplied. (D-006, 03-design-documentation/decision-log.md)
- CIA-001 (deferred) affects FR-001: A proposed change from facility-specific permission to shared admissions access changes the authorization boundary. (CIA-001, _registry/change-impact.yaml)

### Never

- Edit the SRS or this brief by hand; change the SRS and regenerate the brief (templates/agent-build-brief.md)
- Retain pending draft and do not mark complete (D-003, 03-design-documentation/decision-log.md)
- Do not emit handoff without sign-off (D-004, 03-design-documentation/decision-log.md)
