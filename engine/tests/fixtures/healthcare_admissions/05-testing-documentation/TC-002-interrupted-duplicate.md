---
phase: "05"
inputs:
  - One interrupted draft exists for synthetic fixture key SYNTH-001.
expected_results:
  - Existing draft reference is returned and the patient-record count remains one.
requirement_trace:
  - FR-002
  - FR-003
---
# TC-002 Interrupted intake duplicate

Given one interrupted draft exists for synthetic fixture key `SYNTH-001`, when a retry uses the same key, then the existing draft reference is returned and no second patient record is created. Automatic merge or identity adjudication is out of scope.
