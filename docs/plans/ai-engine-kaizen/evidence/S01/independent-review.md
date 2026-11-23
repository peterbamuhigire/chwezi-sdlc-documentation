# AC-S01 independent walkthrough

Reviewed the committed PRD at `22421ba7c10d9f9f19ae33b567d99c6f14a7e6a5` against the frozen K1 table. Eight rows produce TP/FP/FN/TN of 1/1/2/4 for the dispatch rule and 3/2/0/3 for the candidate. The penalty falls from 11 to 2, but five candidate alerts exceed the two-review capacity. The example keeps manual triage available and distinguishes dispatch-time inputs from adjudicated evaluation labels.

Removed the decision-deadline and label-owner input lines separately in memory. Each matching named open requirement survived in the omission instructions. The example supplies no approved rollout threshold. Independent review outcome: PASS for AC-S01. Stakeholder approval and live performance remain unassessed.

The native skill-engine baseline validator returned zero failures with six existing size warnings. The original worker's result.md is a historical receipt from before the operator commit.
