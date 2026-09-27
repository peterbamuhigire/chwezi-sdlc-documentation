---
phase: "05"
inputs:
  - Admission has no sign-off record.
expected_results:
  - No billing-handoff event is emitted and admission remains awaiting review.
requirement_trace:
  - FR-006
---
# TC-004 Missing sign-off blocks handoff

Given an admission has no sign-off record, when the billing handoff job runs, then no handoff event is emitted and the admission remains awaiting review.
