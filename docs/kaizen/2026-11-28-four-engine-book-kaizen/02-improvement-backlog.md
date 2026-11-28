# Improvement backlog

| Priority | Decision and proof |
|---|---|
| P0 | Prevent data loss from unconditional reversal. Security and licensing exceptions remain outside the score. |
| P1 | `06-deployment-operations/01-deployment-guide/logic.prompt`. The generator required unconditional reversal while the owning skill explicitly recognises forward-fix-only migrations. Make the recovery decision depend on compatibility, acknowledged writes and the last safe reversal point. Produce a deployment guide section from a partially migrated service. |
| P1, second wave | `06-deployment-operations/01-deployment-guide/SKILL.md` and `logic.prompt` require reconciliation but leave the comparison unspecified. Use the existing rehearsal's cutoff and accepted-write identifiers to make the operator's acceptance check explicit. The synthetic test must reject an equal-count recovery with a missing and duplicate write. A compatible application-only rollback must remain available. Revert the paired edits if either case fails. |
| P2 | November 28 register refresh supersedes the four November 29–30 platform deadlines. Keep historical standards mappings and project decisions with their designated owners. |

Owner: repository maintainer. Counter-metric: An ordinary release retains its rollback path; an incompatible migration preserves acknowledged writes and requires reconciliation before reopening. Roll back the owning change and its paired regression together if the ordinary case fails. Retain all failed observations.

Morris (2021), *Infrastructure as Code*, second edition. Split a release into independently recoverable changes. The author lists a later edition; no platform commands or version claims were imported.
