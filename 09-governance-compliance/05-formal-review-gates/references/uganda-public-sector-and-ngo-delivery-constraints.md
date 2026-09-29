# Uganda Public-Sector and NGO Delivery Constraints

Cross-cutting reference for SDLC and software-documentation artefacts produced for Ugandan **government, local-government, public-entity, NGO, and donor-funded** clients. Apply it whenever a delivery plan, review gate, deployment/go-live decision, or risk register is generated for such a client, so the artefact reflects the budgeting, procurement-gating, governance, and audit realities that actually constrain when a system can be funded, authorised, cut over, and operated.

**This reference captures the framework *structure* and *citations*, not current statutory amounts.** Monetary thresholds, percentages, fees, and any amended deadline change by Act, regulation, or circular. Treat every figure below as "framework-as-issued — verify the current instrument before final output." The finance engine at `chwezi-accounting-doctrine` is the authority for the financial substance; this file translates that substance into SDLC delivery gates. Do **not** hardcode any rate or threshold here as current.

## Authority and cross-references

The substance of every constraint below is owned by the finance engine. Consult it as the source of truth and follow its `live-rate-verification-protocol.md` before fixing any figure:

- `chwezi-accounting-doctrine/doctrine/references/uganda-public-sector-pfm.md` — PFM legal hierarchy, budget execution, commitment control, reporting calendar, accounting-officer accountability.
- `chwezi-accounting-doctrine/doctrine/references/uganda-ngo-financial-management-patterns.md` — NGO/donor finance manuals, restricted-fund and reporting cadence patterns.
- `chwezi-accounting-doctrine/skills/12-public-sector-and-ipsas/donor-funded-project-fiscal-compliance/SKILL.md` — donor-funded project fiscal compliance, ineligible-cost exposure.
- `chwezi-accounting-doctrine/skills/12-public-sector-and-ipsas/government-procurement-and-fiscal-controls/SKILL.md` — procurement and fiscal control gating.
- `proposal-skills/skills/profiles-sectors/sectors/ppda-uganda/SKILL.md` — PPDA procurement-process detail (methods, thresholds, timelines).

Primary instruments behind this reference: Local Governments (Financial and Accounting) Regulations 2007 (SI 25/2007) under the Local Governments Act 1997; PFMA 2015 and PFM Regulations 2016; MOFPED Financial Reporting Guide 2024; PPDA Act 2003 (as amended by the PPDA (Amendment) Act 2021) and the PPDA Regulations 2023 (effective 5 February 2024, harmonising central and local government — the former Local Governments (PPDA) Regulations 2006 were revoked); real NGO finance manuals. Verify current statutory thresholds against the PPDA instrument in force at the engagement date.

## How to apply this in SDLC artefacts

1. Treat **funding availability** and **procurement sign-off** as *blocking* delivery gates, not background assumptions. A planned milestone with no released funds or no executed contract behind it is not schedulable.
2. A **system cutover cannot precede** the procurement and fiscal sign-offs that fund and authorise it. Sequence go-live after, never before, those approvals.
3. Align go-live and hypercare windows **away from** financial-year close, board-of-survey, and audit blackout periods.
4. Map each constraint to a concrete artefact: a review gate (PSR/CSR/FSAR), a go-live blocker register row, a deployment pre-check, or a risk-register entry.
5. Never assert a specific threshold or rate as current — cite the instrument and route the figure through the finance engine's verification protocol.

## Budget cycle and funding as a blocking gate

- **Financial year** for central Government of Uganda runs **1 July – 30 June**; appropriations **expire 30 June** and unexpended balances revert to the Consolidated/UCF (donor balances are retained by the Accounting Officer but must be re-voted before use). A deliverable, licence, or payment milestone planned to land across 30 June without re-appropriation is at risk.
- **Quarterly expenditure/commitment limits** govern in-year spend; a quarter's limit caps what can be committed in that quarter. Schedule cost-incurring delivery events (licences, hardware, milestone payments) against the quarter whose limit covers them.
- **Commitment Control System (CCS):** no LPO, contract, or commitment may be raised without an approved commitment requisition and a sufficient uncommitted balance in the quarter's limit. Treat "approved requisition + uncommitted balance confirmed" as a precondition gate on any procurement-dependent delivery step.
- **Vote on account** and **virement** limits constrain reallocation between budget lines; a delivery change that needs funds moved between lines may require Council/Executive approval before it is fundable.
- Delivery-gate rule: **no funding instrument confirmed → no commitment → milestone not schedulable.** Record the funding instrument (warrant, release, signed grant tranche) as evidence at each gate.

## Procurement-approval gates as blocking phase gates

Public procurement under the PPDA framework introduces approval steps that sit *upstream* of any contracted delivery work and cutover:

- **Contracts Committee / evaluation and award:** bid evaluation, Contracts Committee approval, and notice/standstill periods each consume calendar time and can be challenged. Build these timelines into the plan rather than assuming instantaneous award.
- **Contract signature:** no contracted vendor work is authorised until the contract is executed. A go-live that depends on a vendor deliverable cannot precede contract signature.
- **Solicitor General / Attorney-General clearance** is required for public contracts above the prescribed threshold (verify the current threshold and instrument). This clearance is a hard, external dependency with its own queue time.
- **PPDA suspension / administrative-review exposure:** a complaint, administrative review, or provider suspension can halt or reset a procurement. Treat this as a schedule risk on any procurement-gated milestone.
- Delivery-gate rule: **evaluation → Contracts Committee award → (Solicitor General clearance where applicable) → contract signature** must complete *before* the dependent delivery, cutover, or payment step. Sequence the review gates (PSR/CSR/FSAR) and go-live decision after the procurement sign-offs, and record each sign-off as gate evidence.

## Reporting and audit timing — go-live and hypercare windows

- **Statutory reporting deadlines** cluster at and after FY-end (semi-annual, 9-month, and annual financial statements; Accountant General → Auditor General consolidation within the statutory window). Finance and operations staff are heavily loaded in these periods.
- **Board of survey** at FY-end (stock/cash/asset verification) ties up the same staff who would own a cutover or hypercare.
- **Audit blackout:** avoid scheduling go-live, data migration, or cutover during the close and external-audit window, when system stability and staff availability are most constrained and when changes complicate the audit trail.
- Delivery-gate rule: place go-live and hypercare **outside** close, board-of-survey, and audit periods; if unavoidable, treat the overlap as a named blocker with an explicit mitigation and approver. Verify the current statutory deadlines via the finance engine before fixing any date.

## Governance and accountability in delivery roles

- **Accounting Officer responsibility:** the Accounting Officer is personally accountable for the regularity and propriety of expenditure and for the assets under their vote. Change-control sign-off that authorises spend or commits the entity must route to, or be traceable to, the Accounting Officer's authority — not an informal project approver.
- **Internal audit reports to council/board**, independent of management. Internal audit is a legitimate reviewer/stakeholder for delivery governance and evidence, and a route for surfacing control concerns.
- **Surcharge / pecuniary liability (LG Regs 2007; Constitution art. 164):** officers can be held personally (pecuniarily) liable for losses arising from negligence or irregular expenditure. This makes **segregation of duties** in delivery roles a real control, not a formality — requisition, approval, commitment, and verification should not collapse into one person, and change-control approval should preserve that separation.
- Delivery-gate rule: every gate that authorises spend, commitment, or cutover names the accountable approver with the authority to bear that accountability, and preserves segregation between requesting, approving, and verifying roles.

## M&E and reporting cadence as milestone checkpoints (NGO / donor)

- Donor and NGO agreements impose **quarterly programmatic and financial reporting** cycles, typically including **budget-vs-actual / flexed-budget variance** reporting against the approved budget and restricted-fund conditions.
- These reporting dates are natural **milestone checkpoints**: align delivery milestones, evidence capture, and go-live readiness reviews with the reporting cadence so the system can produce the donor-required figures from its first reporting period.
- **Ineligible-cost / recovery exposure:** spend outside the approved budget lines, eligibility rules, or grant period can be disallowed and **recovered** from the entity. Delivery decisions that incur cost (early licences, scope additions) must be checked against eligibility and grant-period limits before commitment.
- Delivery-gate rule: confirm the system can satisfy the donor reporting cadence (quarterly programmatic + financial, variance against flexed budget) as a go-live readiness criterion, and check every cost-incurring delivery decision against eligibility and grant-period limits.

## Sector risk-register additions

Use these as candidate entries when generating a risk assessment for a Ugandan public-sector or donor-funded engagement (score and assign owners per the host risk-assessment skill). They are predominantly **project** and **compliance** category risks:

| Candidate risk | Category | Why it bites delivery |
|---|---|---|
| Budget-release / warrant delays | Project | Released funds lag the plan; commitment cannot be raised; milestones slip into the next quarter or FY. |
| Procurement-process delays | Project | Evaluation, Contracts Committee, Solicitor General clearance, and signature timelines extend the critical path. |
| PPDA suspension / administrative-review exposure | Compliance / Project | A complaint, review, or provider suspension halts or resets a procurement. |
| Donor-audit findings & ineligible-cost recovery | Compliance | Disallowed costs are recovered from the entity; funding and trust erode mid-delivery. |
| Political / electoral-cycle disruption | Project | Elections, reshuffles, and budget re-prioritisation disrupt sponsorship, sign-off, and staff availability. |
| Exchange-rate volatility on USD/EUR donor budgets | Project | UGX movement against the donor currency erodes the local-currency budget for licences/hardware. |
| Staff turnover in procurement / finance units | Operational | Loss of the requisitioning/approving officers stalls commitments and re-starts approval chains. |
| FY-end / audit-blackout overlap | Project | Go-live or migration scheduled into close, board-of-survey, or audit periods raises failure and audit-trail risk. |

Cross-reference the finance engine for the substantive control behind each risk, and verify any threshold cited in a mitigation against the current instrument.
