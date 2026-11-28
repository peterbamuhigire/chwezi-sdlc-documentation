# Experiment log

**Before.** The generator required unconditional reversal while the owning skill explicitly recognises forward-fix-only migrations.

**Intervention.** Make the recovery decision depend on compatibility, acknowledged writes and the last safe reversal point. Produce a deployment guide section from a partially migrated service.

**Keep decision.** An ordinary release retains its rollback path; an incompatible migration preserves acknowledged writes and requires reconciliation before reopening.

The first revision retained unconditional reversal in the acceptance text. Review identified it, and both the operator contract and generator now cover recovery after accepted writes. Worked example below.

﻿# Depot maintenance portal deployment guide

## 5. Rollback procedure

This rehearsal uses a synthetic maintenance portal release. The replacement application is build B and the prior application is build A. The migration creates a normalized category record for each work order and then removes the legacy category field. The test input records work orders WO-101 and WO-102 before migration and WO-103 and WO-104 as accepted afterward. WO-101 and WO-103 share one normalized category, so totals alone cannot detect a lost order.

| Change and trigger | Recovery authority and last safe reversal point | Operator action and verification |
|---|---|---|
| Build B application fails smoke checks before schema contract changes. | Release lead. Deployment history and schema inspection must confirm that build A still supports the active schema. | Redeploy the approved build A artifact through the release workflow. Verify the running artifact identifier, read WO-101, and create and reconcile one synthetic work order through the application. |
| Build B fails after the legacy field was dropped and WO-103 and WO-104 were accepted. | Incident commander authorises stopping intake and queue consumers. The data owner approves the recovery plan. The last safe point for restoring the prior database state was before migration and before the first new accepted write. | Quiesce writers and preserve the active database, intake acknowledgements and work queue at the same recorded cutoff. Keep build A out of service because it needs the removed field. Apply the reviewed forward fix to a retained copy and verify WO-101 through WO-104, their category assignments and exactly one resulting queue outcome per accepted identifier. The data owner confirms reconciliation and the incident commander authorises the production recovery and resumption of writers only after service and data checks pass. |
| Migration tool stops without a reliable completion record. | Data owner decides after inspecting preserved evidence. Last safe reversal point is unknown. | Keep affected writes paused if authorised. Record the migration step and observed schema state, then escalate before replaying or reversing any step. The data owner must reconcile state with the deployment plan before approving further action. |

### Rehearsal stop condition

A missing or duplicate work-order identifier, incorrect category assignment, unknown queue watermark, or failed user-path smoke check keeps writers paused and sends the decision to the incident commander.

## Second-wave recovery replay

At `de04d72`, the example already compared individual writes at a recorded cutoff. The prompt and skill only asked for reconciliation. A checklist that compared the row count and category totals could therefore satisfy their wording while dropping WO-103 and duplicating WO-101.

Compare the expected work-order ID and category pairs through the agreed cutoff with the recovered pairs. Compare the observed queue outcomes by accepted ID against the expected outcomes for the same cutoff. In this rehearsal, each accepted ID must have exactly one outcome. Include service health in the resumption decision.

| Rehearsal input | Expected operator decision |
|---|---|
| Build B fails before contraction. Build A is compatible with the observed schema. | Reverse the application release and run read and write smoke checks. |
| Build B fails after contraction. All four IDs and category assignments match, with one queue outcome per accepted ID and a known cutoff. | Complete the forward-fix checks and obtain authorisation to resume. |
| WO-101 appears twice and WO-103 is missing. Both use the same category. | Hold writers even though row and category counts match. |
| All four IDs and categories match, but WO-104 has a duplicate queue outcome. | Hold writers and reconcile queue effects. |
| All records match, but the queue cutoff is unknown. | Hold writers and escalate the missing evidence. |
| The migration tool stops and observed migration state is unknown. | Escalate before retrying or reversing. |

The contract change carries the existing rehearsal's evidence into the operative prompt and skill. The replay uses synthetic records. Live migration and autonomous generation were outside this trial.
