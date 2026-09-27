---
phase: "05"
inputs:
  - User has no admission permission for F-B.
expected_results:
  - ACCESS_DENIED is returned and F-B intake-record count is unchanged.
requirement_trace:
  - FR-001
---
# TC-001 Facility-scope denial

Given a synthetic user has no admission permission for facility F-B, when that user submits an admission request for F-B, then the response is `ACCESS_DENIED` and no F-B intake record is created.
