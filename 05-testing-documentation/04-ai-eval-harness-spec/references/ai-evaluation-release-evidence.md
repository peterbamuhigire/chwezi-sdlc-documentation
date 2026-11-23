<!-- Source basis: Designing for AI early release chapters 1-4; XP 2026 AI-augmented engineering and regression-testing papers. -->

# AI Evaluation Release Evidence

The eval harness must test the product system, not only text similarity.

| Dimension | Test evidence |
|---|---|
| Task outcome | Goldens, holdout, edge cases, multilingual/local and low-resource cases |
| Model/system boundary | Versioned model, prompt, retrieval, tools, policy and fallback |
| Human control | Preview, correction, contest, override, undo, escalation, consent/notice |
| Safety and fairness | Abuse, privacy, subgroup, accessibility and harmful-action cases |
| Operations | Cost, latency percentiles, availability, errors, drift and alert response |
| Release decision | Baseline comparison, guardrail result, owner, cohort, duration, rollback |

Refresh the dataset after incidents, user corrections, model changes, data
changes, or policy changes. Never use the same generated data for tuning and
final gating without a leakage check. A failed or unavailable test is retained
as `fail` or `not assessed`, never silently omitted.

## Filled evaluation record for ticket dispatch and maintenance answers

**EVAL-01** evaluates requirement FR-K1-01 on tickets-v1, rules-v1 and candidate-v1. For K2 it evaluates corpus atlas-v2 and the indicated response variant. Use [the frozen casebook](../../../docs/plans/ai-engine-kaizen/casebook.md) to repeat the review. Keep each fixture revision with the resulting decision.

| K1 policy | TP | FP | FN | TN | Flagged | Precision | Recall | Miss and review penalty |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| rules-v1 | 1 | 1 | 2 | 4 | 2 | 1/2 | 1/3 | 11 |
| candidate-v1 | 3 | 2 | 0 | 3 | 5 | 3/5 | 1 | 2 |

The frozen policy CAP-2 allows two alerts. Reject candidate-v1 for that shift. CAP-ALL can accommodate all five, but an adoption decision still needs a confirmed label owner, deadline and representative evidence. The eight frozen labels do not estimate population performance. Report a subgroup's numerator and denominator separately. When a group has no positive predictions, report precision as undefined. Report pending outcomes and abstentions separately from scored cases. A reviewer must be able to trace any declared cost back to its operating policy.

For metrics, name the scorer, unit, direction, dataset revision and denominator. On observed [0,2,4] and predicted [0,2,3], squared residuals sum to 1 and total squared deviation from the mean is 8. MSE is 1/3 in squared outcome units, lower is better. R-squared is 7/8, dimensionless, higher is better. Reject any result labeled MSE that uses the default coefficient of determination.

On atlas-v2, returning P2 revision 2 first is a retrieval hit. The answer “five days” fails support, since P2 says three. When nothing authorized supports the answer, abstain without disclosing the other tenant's title or identifier. Evaluate abstentions on no-answer cases separately from answerable-case ranking. A schema, permission or idempotency failure overrides a subjective pass.

Calibrate a model judge on independently human-labeled groups excluded from tuning and final testing. Include disagreements, ties and unknowns. Present a synthetic identical-content pair in both orders with both item IDs blinded. A judge that always picks the first slot disagrees with the tie label twice and changes the winning ID when reversed. Flag position bias and suspend automated acceptance for that criterion. Record both orders, labels, abstentions and denominators. No general agreement percentage or vendor prestige establishes project acceptance.
