# SDD Phase-Boundary Contract

This contract adds deterministic controls for Spec-Driven Development feature
workspaces. It complements the standards-driven SRS lifecycle; it does not
replace IEEE/ISO requirements validation, traceability, or sign-off gates.

## Boundaries

| Boundary | Required evidence | Blocking failures |
|---|---|---|
| Spec → Plan | P1 requirements, coverage-map rows, implementation files, symbols/APIs | missing requirement coverage, empty file/symbol mapping |
| Plan → Tasks | every P1 requirement tagged, sequential task IDs, valid dependencies | untasked P1 requirement, missing dependency, cycle, oversized task file |
| Tasks → Implement | task state is authoritative; deferred work is explicit | `.completed` while active tasks remain |
| Implement → QC | implementation completion plus QC report with exactly one `overall: PASS` verdict | `.qc-passed` without an explicit current PASS, or with FAIL/NOT ASSESSED/contradictory verdict text |

## Deterministic runner

Run from the engine root:

```powershell
python scripts/validate_sdd_phase_boundaries.py --feature-dir projects/<Project>/feature
```

Use `--stage spec-plan`, `--stage plan-tasks`, `--stage tasks-implement`, or
`--stage implement-qc` to run one boundary. Add `--json` for CI or an evidence
manifest. A missing required artifact is a failure, not an unassessed pass.

## Agent and hook integration

Agents may explain or repair a finding, but they cannot manufacture a PASS. A
QC report must contain exactly one machine-readable line `overall: PASS`; a
bare PASS word, historical PASS, negated PASS, or contradictory overall verdict
does not establish the boundary.
The validator is the preflight/release hook for environments without native
hooks. Native hooks should invoke the same command at plan, task, completion,
and release events. Persist overrides in the project evidence record with an
owner, reason, expiry, scope, and rollback; never record a gate bypass only in
conversation.

Handoff records may carry a requirement baseline hash/version, need and reuse
decision IDs, invariants, fit criteria, evidence status, waiver scope and the
next engineering return link. A `complete` handoff requires
`evidence_status: verified`; older schema-version-1 records remain readable but
unknown fields are not treated as approval.

When the current requirements hash is available, pass it with
`--requirement-hash`; a handoff carrying a different baseline is stale and
blocks the boundary until the handoff and evidence are regenerated.

When work stops or a phase is blocked, pair the validator result with
`python scripts/create_sdd_handoff.py --feature-dir <dir> --stage <stage>
--status blocked --owner <owner> --next-step <step>`. The handoff record is
the resumable stop-hook evidence; it does not replace the phase validator.

Beside the handoff record, `python scripts/create_agent_build_brief.py --project <project-dir> --feature-dir <dir>`
writes `agent-build-brief.md`: a six-area agent brief derived from the approved SRS, every entry traced to its
source, with untraceable areas marked `CONTEXT-GAP` so the kernel blocks them. It never replaces or edits the SRS.
