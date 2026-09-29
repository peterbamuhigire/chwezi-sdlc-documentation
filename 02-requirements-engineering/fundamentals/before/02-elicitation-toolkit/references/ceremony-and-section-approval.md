# Ceremony Classification and Section-Scoped Approval

Use this reference at the start of every SRS engagement and throughout drafting. It extends the
shared-understanding gate in `decision-frontier-elicitation.md` from the synthesis stage into the
drafting stage. It does not replace decision-frontier elicitation, intent write-back or the
shared-understanding gate; those remain the entry method.

## Ceremony classification

State the classification aloud to the owner at the start of the engagement and record it, with the
date and the owner's confirmation, in `projects/<ProjectName>/_context/methodology.md`.

| Class | Trigger | Required ceremony | Output |
| --- | --- | --- | --- |
| Bounded | A change request against a baselined SRS | Change-impact analysis; elicitation and drafting limited to the affected sections | Revised sections, updated traceability, change-impact record |
| Architectural | A new module or a new system | Full elicitation and the complete IEEE 29148 pipeline | A full SRS or SRS module |
| Spike | A feasibility question whose answer is not yet known | A time-boxed investigation with a named owner and end date | A decision record, not requirements |

Rules:

1. The classification ratchets upwards only. A bounded change that reveals architectural scope is
   reclassified as architectural, and the reason is recorded. A reclassification downwards requires
   the owner's written agreement.
2. A spike never produces `FR-` or `NFR-` identifiers. If the spike concludes that the feature should
   proceed, open a new bounded or architectural engagement and cite the decision record.
3. When the class is uncertain, treat it as the higher class until the owner confirms otherwise.

## Section-scoped drafting approval

Drafting proceeds one numbered IEEE section at a time (for example 3.2, then 3.3). For each section:

1. Present the section on its own, with the decisions and sources it depends on.
2. Ask the owner to approve, correct or reject that section only.
3. Record the outcome in the elicitation log (or, for a formal gate, in
   `_registry/sign-off-ledger.yaml` through `python -m engine signoff`) with the section number,
   date, approver and any conditions.
4. Move to the next section only after the outcome is recorded.

Approval of one section is never approval of another. A later section does not inherit approval
from an earlier one, and a revision to an approved section reopens its approval. Silence, a meeting
that ends without a decision, or a polished draft is not approval.

Bounded engagements approve only the sections they change. Spikes produce no sections, so no
section approval applies; the decision record is approved as a single item.

### Approval log row

| Section | Title | Presented | Outcome | Approver | Date | Conditions |
| --- | --- | --- | --- | --- | --- | --- |
| 3.2 | Functional requirements — Admissions | 2026-09-29 | Approved with conditions | Head of Admissions | 2026-09-30 | Confirm the duplicate-referral rule with Records |

## Relationship to validation

Section approval confirms that the owner accepts what was written. It does not confirm that the
requirement set is complete. Before the set is baselined, `07-requirements-validation` adds a
Review Focus table of conditions the requirements imply but do not state.

## Attribution

Ceremony classification, section-scoped approval and Review Focus adapted from Superpowers (MIT,
https://github.com/obra/superpowers, commit 8ca22dba9a94f28898bbce59f2537ff4d87c747d). Paraphrased.
