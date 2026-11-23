# AI-Feature PRD Addendum (paste into generic PRD)

Use this addendum to extend the generic `01-prd-generation` output for any AI-powered feature. Append the following sub-sections to the FR block.

## FR-XXX — [Feature name]

### Hallucination tolerance

- Factuality target: >= 0.XX on golden set EVAL-XXX.
- Citation accuracy target: >= 0.XX (RAG features only).
- Abstain rule when below target.

### Latency budget

- P95 target: <= XXXX ms end-to-end.
- Per-stage budget: retrieval XXX ms, model call XXX ms, post-process XXX ms.
- Timeout: XXXX ms with graceful fallback (last good response / cached / error message).

### Cost ceiling

- Per-call ceiling: <= $0.XX.
- Per-tenant daily ceiling: <= $XX (configurable).
- Throttle behaviour on ceiling breach.

### Abstain criteria

- Quantitative: confidence score < X, retrieval count < N, or judge-LLM gate fails.
- Behaviour on abstain: structured non-answer with offer to escalate to human.

### Citation policy

- Every factual claim about ingested content cites a source span (doc id + offset).
- Citation rendering rule in UI.

### Consent and opt-in

- Feature default state per region and per tier.
- Admin override path.
- End-user privacy notice text reference.

### Training-data exclusion

- Provider configuration evidence (no-training endpoint, zero-retention contract clause).
- Quarterly audit reference.

### Acceptance gate

- Eval harness pass threshold (golden set ID + percentage).
- Red-team pass threshold (adversarial set ID + percentage).
- Hallucination SLO target post-launch.

## Filled example — K1 support-ticket triage

This synthetic example uses the frozen inputs in `docs/plans/ai-engine-kaizen/casebook.md`.
Its penalties and predictions are fixture values, not measured operating results.

### Decision and linked requirement

- **AI-FR-K1-01 / parent FR-K1-01:** For each incoming support ticket, present an urgency recommendation and its input ticket ID to the shift lead before dispatch. The classifier may recommend; it does not dispatch or close a ticket.
- **Actor and decision:** The shift lead decides which tickets receive human review. The shift can review two alerts. The candidate flags five of eight fixture tickets, so it exceeds that profile's review capacity.
- **Decision deadline:** Not supplied. The product owner must specify the latest useful decision time relative to dispatch before this requirement can be accepted. Until then, `[OPEN: FR-K1-01 decision deadline]` remains unresolved.
- **Available inputs:** At dispatch, use the incoming ticket ID and text. The frozen urgent/not-urgent labels and predictions in K1 are evaluation inputs only. They must not be supplied as prediction-time features. The prediction table is synthetic; it does not establish production label availability, classifier quality, or live input access.
- **Miss and false-alert consequences:** In this fixture only, one missed urgent case costs five units and one unnecessary review costs one unit. The current rule's fixture cost is 11; the candidate's is 2. These example penalties are not approved operational values.
- **Label ownership and fallback:** The Support Operations Lead is the proposed accountable role for label adjudication and unresolved cases; a named owner and confirmation of that role are not supplied. Until confirmed, `[OPEN: FR-K1-01 label owner]` remains unresolved. The shift lead is the immediate manual fallback for this shift; overflow beyond two reviews needs an owner-approved queue or escalation path before rollout.
- **Non-AI comparators:** (1) deterministic dispatch using the existing rule, with its K1 fixture counts (1 TP, 1 FP, 2 FN, 4 TN); and (2) manual triage by the shift lead. The classifier is a third option and must be compared against both on the same frozen, appropriately labeled cases.

### Distinct behavior and acceptance boundary

The classifier predicts urgency. Deterministic dispatch applies the existing rule to route tickets. Manual triage leaves urgency and routing decisions to the shift lead. Keep these behaviors and their outcomes separately identified in the evaluation record.

For the two-review profile, the K1 candidate is not eligible for rollout as configured: its five alerts exceed capacity even though its fixture penalty is lower. A ranking, threshold, queue, or staffing change is a new evaluated decision. The all-alert review profile may lead to a different decision from the same counts, but the casebook supplies no approved rollout target, threshold, deadline, or production result. Do not inherit or invent one. Record the chosen policy and its owner before making a rollout recommendation.

### Required omission checks

- If the deadline field is removed or left blank, keep `[OPEN: FR-K1-01 decision deadline]` and do not accept the requirement.
- If label ownership is removed or left unconfirmed, keep `[OPEN: FR-K1-01 label owner]` and do not accept the requirement.
- A filled example does not close either stakeholder decision or establish a rollout target.
