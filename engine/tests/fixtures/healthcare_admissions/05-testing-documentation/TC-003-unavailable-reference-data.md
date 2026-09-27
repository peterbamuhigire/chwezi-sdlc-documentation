---
phase: "05"
inputs:
  - Required reference-data service is unavailable.
expected_results:
  - Draft remains retrievable with status PENDING_REFERENCE_DATA and completion is false.
requirement_trace:
  - FR-004
  - FR-005
---
# TC-003 Unavailable reference data

Given required reference data is unavailable, when an intake is submitted, then the draft remains retrievable, status is `PENDING_REFERENCE_DATA`, and the system does not report completion.
