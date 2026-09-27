# Decision log (synthetic fixture)

| ID | Origin | Status | Owner | Decision / unresolved choice |
|---|---|---|---|---|
| D-001 | P11 cross-facility scenario | SYNTHETIC TEST CONDITION | Facility access owner not supplied | Deny access when facility permission is absent. No real role or permission matrix is specified. |
| D-002 | P11 interrupted-intake scenario | SYNTHETIC TEST CONDITION | Identity/privacy owner not supplied | Prevent silent duplicate creation and present the existing draft. Match-key selection, authorized reviewer, merge/retention behavior, and audit obligations remain open. |
| D-003 | P11 unavailable-data scenario | SYNTHETIC TEST CONDITION | Service owner not supplied | Retain pending draft and do not mark complete. Retry policy, data source, and timeout remain open. |
| D-004 | P11 sign-off/billing-handoff scenario | SYNTHETIC TEST CONDITION | Admission and billing owners not supplied | Do not emit handoff without sign-off. Sign-off criteria, role, billing event schema, and reconciliation controls remain open. |
| D-005 | Contradictory draft example | OPEN CONFLICT - NOT APPROVED | Decision owner absent | One draft says “billing handoff only after sign-off”; a contradictory draft says “billing handoff before sign-off”. The conflict is exposed here and excluded from approved fixture requirements. No automated semantic-conflict detector is claimed. |
| D-006 | Missing sign-off example | OPEN - NOT APPROVED | Decision owner absent | No sign-off record is supplied. No approval is inferred; the handoff remains blocked in the fixture. |

All records and wording are synthetic test material; none represents Medic8, a real facility, or a professional decision.
