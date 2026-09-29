---
name: 15-game-product-and-production-brief
description: "Use when defining a game's player promise, product hypotheses, platform options, production model, vertical-slice evidence, commercial boundaries, or greenlight decision before detailed requirements."
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Game Product and Production Brief
<!-- dual-compat-start -->
## Use When
- A game needs an evidence-bounded concept, prototype plan, platform posture, production scope, or greenlight packet.
## Do Not Use When
- Detailed requirements already exist; use `19-game-software-requirements-specification`.
- Do not call a pitch, editor prototype, or art sample production-ready.
## Required Inputs
| Artefact | Source or provider | Required? | Behaviour when missing |
|---|---|---|---|
| Player evidence, cohorts, concept, platforms, constraints, team and commercial intent | Product, design, research and delivery leads | Yes | Stop greenlight and return a hypothesis/gap register. |
| Learning, wellbeing, rights, fact/fiction, consultation/permission, comparable and technical-risk evidence | Accountable education, culture, rights, research and engineering owners | Conditional | Mark not assessed and prohibit unsupported claims. |
## Workflow
1. Define cohort-specific player promise, repeated action, intended emotion, session and stopping model, differentiation, exclusions and ethical boundaries.
2. Convert creative, learning, technical, visual, commercial, cultural and wellbeing uncertainty into falsifiable hypotheses and prototype thresholds; engagement never proves learning or wellbeing.
3. Compare engine, platform and topology options without inventing current implementation facts.
4. Separate historical/cultural fact, fiction, inspiration, consultation, permission and rights; research does not grant approval.
5. Compare premium, demo/prologue, DLC, subscription, sponsorship, licensing, institutional sales, grants, ethical ads and IAP as hypotheses with assumptions, downside and stop rules. Financial independence is motivation, not a promise.
6. Define gates from paper proof through vertical slice, production, release candidate and sustain, including a non-intrusive-ad gate when ads are contemplated.
7. Specify staffing lines, content-throughput, localisation, rework, support, platform/payment/tax/rights assumptions, dependencies, contingency and greenlight/pivot/narrow/hold/stop triggers.
8. Stop on missing player, learning, rights/culture, device, safety or owner evidence; recover with bounded discovery work.
## Outputs
| Artefact | Consumer | Acceptance condition |
|---|---|---|
| Game product and production brief | Sponsor, product, design and studio leads | Promise, hypotheses, options, gates, risks and evidence are explicit. |
## Evidence Produced
| Evidence | Reviewer | Acceptance condition |
|---|---|---|
| Hypothesis, prototype, risk and decision register | Greenlight reviewer | Each decision has evidence, owner, date, confidence and reversal trigger. |
## Capability and permission boundaries
Read and search are allowed. Creating the brief requires authority; budget, licences, hires or certification require accountable approval.
## Degraded mode
Return the narrowest qualified concept, mark unavailable checks `not assessed`, and never infer a pass.
## Decision Rules
| Choice or condition | Action | Failure or risk avoided |
|---|---|---|
| Core action is not understood or enjoyed | Iterate, pivot or stop. | Scaling an unproven loop. |
| Target-device risk is material | Require a representative spike. | Editor-only feasibility. |
| Rights are unresolved | Substitute, obtain permission or remove scope. | Infringement. |
## Quality Standards
- Separate facts, hypotheses, estimates and decisions; defer game implementation craft to the software engine and visual/interaction craft to `chwezi-design-engine`.
## Anti-Patterns
- Pitch treated as validation. Fix: require player evidence.
- Content before loop proof. Fix: validate repeated play.
- Engine chosen by fashion. Fix: compare constraints.
- Platform without hardware. Fix: identify device envelopes.
- Greenlight without stop criteria. Fix: add thresholds and owner.
- Ads treated as a revenue default. Fix: define placement, child/privacy, trust, no-fill and kill-switch hypotheses before greenlight.
## References
- [Game brief evidence model](references/game-brief-evidence-model.md)
- [PRD learning contract](../../01-strategic-vision/01-prd-generation/references/kaizen-prd-learning-contract.md)
<!-- dual-compat-end -->
