# Decision-Frontier Elicitation

Use this method when requirements depend on several linked human decisions. It prevents repetitive
linear interviews and prevents downstream choices from being asked before their prerequisites are
understood.

## Build the decision graph

| Field | Meaning |
| --- | --- |
| Decision ID | Stable identifier |
| Question | Choice the accountable person must make |
| Owner | Person or role with decision rights |
| Prerequisites | Facts or earlier decisions needed first |
| Options | Real alternatives and consequences |
| Evidence | Project or verified external facts that inform the choice |
| State | blocked, frontier, proposed, confirmed, or superseded |
| Downstream | Requirements, terms, flows, tests, or decisions affected |

Facts are researched or extracted from available evidence. Decisions stay with the accountable
human. Do not ask a stakeholder for repository facts the analyst can inspect, and do not silently
convert a recommendation into a confirmed decision.

## Run frontier rounds

1. Mark a decision `frontier` only when every prerequisite is confirmed or explicitly waived by its owner.
2. Ask independent frontier questions together when that reduces interruption without hiding trade-offs.
3. Explain why each question is ready, the options, and the downstream consequence.
4. Record the answer verbatim or as an attributed paraphrase, confidence, dissent, and effective date.
5. Recompute the frontier. New dependencies return to `blocked`; newly ready decisions advance.
6. End only when the required scope is confirmed or every unresolved branch has an owner and next event.

## Shared-understanding gate

Before synthesis, present the confirmed goal, actors, scope/non-scope, critical flows, terms, quality
constraints, unresolved decisions, and conflicts. The owner confirms or corrects that summary. A
silent meeting end, question count, or polished draft is not confirmation.

The gate continues into drafting: classify the engagement and approve one numbered section at a
time, as set out in `ceremony-and-section-approval.md`.

## Counter-cases

- If two decisions conflict, keep both attributed and route resolution to the named authority.
- If an answer is partial, preserve the answered field and ask only for the missing delta.
- If a decision is asynchronous, issue a questionnaire with context, options, consequences,
  partial-answer support, deadline, and return path.
- If no owner exists, stop the dependent branch and record governance risk.

Start from `templates/decision-frontier.yml` at the repository root and validate the current states
before each round:

```powershell
python -X utf8 scripts\validate_decision_frontier.py <decision-graph.yml>
```

This reference adapts the design-tree and frontier mechanism studied in Matt Pocock's
`mattpocock/skills` repository at commit `3cca18b`; SRS traceability and decision rights remain authoritative.
