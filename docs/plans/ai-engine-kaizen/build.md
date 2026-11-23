# srs-skills · AI capability implementation

**Accountable owner** Peter. **Execution role** SDLC specification author. **Observed starting revision** `0fe8d74bbad170cfa9d0efca510af9ef5c7f6924`. Recheck the revision on staging. Apply ordinary commits to the isolated JAD branch. Link a receipt for each criterion. All tasks begin pending.

**User journey** requirement → dataset contract → evaluation → rollout decision. Use the four existing AI specification families. Preserve their other templates, evidence states and routing semantics.

**Entry condition** Build packet K1/K2 and K3, then hand the exact specification IDs to both engineering owners.

**Inputs** Use [casebook.md](casebook.md) for the fixture data and expected outcomes and [sources.json](sources.json) for external evidence. B1 Joel Grus, B2 Thomas Nield, B3 Albrecht/Ramachandran/Winkler, B4 Parikh/Johri, B5 Neroda/Escaravage/Peters, B6 David Foster, B7 Sanseviero/Cuenca/Passos/Whitaker, B8 Brousseau/Sharp. R IDs refer to primary sources in the register. Use the latest verified source for any new API, model version, security or vendor-specific claim. Close the capability through its normal route.

## Ordered tasks

### S01 · Turn the AI request into a measurable user decision

**Depends on** Entry condition only. **Owned surfaces** `02-requirements-engineering/14-ai-feature-prd-spec`. **Basis** B1 B2 B5 R11.

Name the actor, decision deadline, available inputs, cost of a missed urgent case, false alert workload, fallback owner and non-AI comparator. Extend the existing PRD with a filled example for ticket triage and a linked requirement ID.

**AC-S01.** An evaluator can distinguish the proposed classifier, deterministic dispatch and manual triage. Removing the deadline or label owner leaves a specific open requirement. A rollout cannot inherit an invented target.

**Evidence.** Commit the artifact and independent result, including failed cases, under `docs/plans/ai-engine-kaizen/evidence/S01/`. Record the exact tested source revision, validator or review procedure, fixture digest, output path, result and limitations. Update only the progress and evidence fields of the sidecar.

### S02 · Specify corpus ownership and leakage controls

**Depends on** S01. **Owned surfaces** `02-requirements-engineering/15-ai-data-and-knowledge-base-spec`. **Basis** B1 B3 B4 R01 R03 R04.

Add a data contract with source version, intended use, access class, grouping key, effective time, target availability, deduplication, withdraw/reindex behavior and train-only transformations. Work through the K1 collision and K2 withdrawn document.

**AC-S02.** A reviewer can reproduce partition membership and isolate held-out or withdrawn records. With future labels or unknown rights, the affected use stays unresolved and the unaffected case remains testable.

**Evidence.** Commit the artifact and independent result, including failed cases, under `docs/plans/ai-engine-kaizen/evidence/S02/`. Record the exact tested source revision, validator or review procedure, fixture digest, output path, result and limitations. Update only the progress and evidence fields of the sidecar.

### S03 · Join evaluation evidence to a release decision

**Depends on** S01, S02. **Owned surfaces** `05-testing-documentation/04-ai-eval-harness-spec`, `03-design-documentation/12-ai-model-card`. **Basis** B1 B2 B3 B7 B8 R02 R05 R06.

Extend the existing harness and model card as a pair. Capture a revision tuple, baseline, confusion counts, subgroup denominators, unknown labels, disjoint calibration set, retrieval versus answer errors, abstention and responsible sign-off.

When an evaluator proposes a model judge, define a human-labeled calibration set independent of the developer, include ties and abstentions, swap answer order, and review disagreements. Treat any historical fixed agreement percentage as an example until the project justifies it.

**AC-S03.** On K1 recompute both classifiers’ results. A release recommendation cites its exact policy. On K2 a correct document with an unsupported answer fails the answer criterion while retrieval retains its own result. A judge favoring first position on identical-content pairs produces a calibration finding. No fixed vendor or judge rank can clear a failed deterministic product criterion. The K1 regression fixture rejects a mislabeled scorer and distinguishes MSE of 1/3 from R-squared of 7/8.

**Evidence.** Commit the artifact and independent result, including failed cases, under `docs/plans/ai-engine-kaizen/evidence/S03/`. Record the exact tested source revision, validator or review procedure, fixture digest, output path, result and limitations. Update only the progress and evidence fields of the sidecar.

### S04 · Specify a supervised build and operator recovery

**Depends on** S01, S03. **Owned surfaces** `04-development-artifacts/05-ai-agent-coding-guidelines-addendum`, `06-deployment-operations/11-ai-feature-rollout-runbook`. **Basis** B4 B5 B8 R09 R10 R12.

Give an assisted coding task its contextual files, expected behavior, allowed surfaces, independent regression, owner and recovery. Connect model/prompt/index rollback, user correction and operations ownership to the original requirement.

**AC-S04.** Using the filled K3 specification, a reviewer identifies the public entry point, independent oracle owner, expected failing behavior, correct retry behavior, the plausible wrong fix and the legacy-data invariant. The document assigns execution and actual revision receipts to D07/E05 and their reconciliation to C04. For K4 it names the operator, compatible artifact tuple and expected rollback outcome. A walkthrough can reject a specification that omits replay or legacy behavior before engineering begins.

**Evidence.** Commit the artifact and independent result, including failed cases, under `docs/plans/ai-engine-kaizen/evidence/S04/`. Record the exact tested source revision, validator or review procedure, fixture digest, output path, result and limitations. Update only the progress and evidence fields of the sidecar.

### S05 · Prove the documentation handoff is usable

**Depends on** S02, S03, S04. **Owned surfaces** `05-testing-documentation/04-ai-eval-harness-spec`, `tests`. **Basis** B1 B5 R01 R02 R09.

Assemble the small filled synthetic packet with linked requirement, dataset manifest, acceptance, operating decision and rollback sections. Add the narrowest test that guards broken references or incompatible revision IDs. Preserve existing reusable templates.

**AC-S05.** Hand the packet to a fresh reader. The reader finds the same case ID and scoped decision for each valid case. A mismatched dataset revision and a missing outcome each prevent acceptance. Record the files and handoff revision.

**Evidence.** Commit the artifact and independent result, including failed cases, under `docs/plans/ai-engine-kaizen/evidence/S05/`. Record the exact tested source revision, validator or review procedure, fixture digest, output path, result and limitations. Update only the progress and evidence fields of the sidecar.

## Verification, replay and handoff

Preserve the repository's configured slice and final checks. Run the narrow check for the changed behavior as well. Exercise a negative control by removing a required input or introducing the named defect. Record which assertion fails. Repeat on the repaired revision. Existing tests cover only their actual scope. A documentation example may be validated by an independent walkthrough with observed outputs. A trained-model, hosted or production claim requires that environment's evidence.

Keep an independent test oracle and the frozen synthetic case IDs. Use original product-safe work in public repositories. The book files and window receipts stay outside all engines. Link any additional task-specific code, catalogue, generated projections and test fixtures to the ownership decision in the evidence record. Avoid unrelated edits.

For interruption, inspect JAD status, branch, plan and the verification receipt. A matching digest can identify an existing artifact. Reconcile partial effects by their operation ID. Resume the existing lane after confirming the saved intent. Never reissue an uncertain external action. A gate failure retains its log and remains failed until repaired and rerun. Continue independent tasks. Enter a blocked result only if no permitted work remains.

**Handoff.** Accepted tasks: S01, S02. Next ready task: S03. See the task-level receipts in evidence/.
