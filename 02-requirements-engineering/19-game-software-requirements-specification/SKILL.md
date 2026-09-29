---
name: 19-game-software-requirements-specification
description: "Use when a video game needs testable GREQ requirements for the game loop, levels, player progression, saves, multiplayer, monetisation, platform certification, content budgets, accessibility, telemetry, builds or live operations; use 01-initialize-srs for a non-game system SRS."
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Game Software Requirements Specification
<!-- dual-compat-start -->
## Use When
- A game needs a controlled SRS across client, server, content and operations.
## Do Not Use When
- The concept is unbounded; use the game product brief first.
- Do not prescribe engine or service APIs without a pinned decision.
## Required Inputs
| Artefact | Source or provider | Required? | Behaviour when missing |
|---|---|---|---|
| Approved brief, journeys, target matrix, rules and risks | Product, design, engineering and production | Yes | Stop affected requirements and issue a gap record. |
| Online, economy/ads, learning, wellbeing, data, safety, culture/rights, visual and platform obligations | Specialist owners | Conditional | Exclude or mark the feature blocked. |
## Workflow
1. Establish boundaries across client, authoritative services, platform services, content/build pipeline and operations.
2. Assign `GREQ-*` and specify action, precondition, authoritative transition, feedback, failure and oracle.
3. Specify saves, time/randomness, input, content, gameplay accessibility, localisation, age treatment, learning evidence limits, wellbeing/stopping, and fact/fiction/consultation/permission controls.
4. For online play specify authority, sessions, replication intent, reconnect, version skew and abuse cases.
5. Add conditioned device performance, memory, loading, thermal, network and storage measures.
6. Specify telemetry purpose, economy integrity, privacy by SDK, build provenance, rollback and ethical commercial behaviour. If ads are in scope, require clear identification, a predictable genuine break after the requested action, neutral decline/close, cap/pace, no-fill/offline/error and kill switch; prohibit interruption of play, learning, narrative, saving, recovery, stopping and exit.
7. Specify visual-direction and UI acceptance as observable game outcomes and evidence while deferring craft to the five game skills in `design-system-skills`.
8. Stop on an ownerless transition, unresolved child/cultural/right boundary or unverifiable threshold; recover with a decision request.
## Outputs
| Artefact | Consumer | Acceptance condition |
|---|---|---|
| Game SRS and register | Architecture, implementation, QA and operations | Every behaviour has owner, boundary, condition, oracle and trace. |
## Evidence Produced
| Evidence | Reviewer | Acceptance condition |
|---|---|---|
| Requirement-source-oracle trace | Requirements reviewer | No requirement rests only on assumption or editor behaviour. |
## Capability and permission boundaries
Read and search are allowed. Editing baselines requires authority; paid services, policy or certification require approval.
## Degraded mode
Return the narrowest qualified subsystem, mark unavailable evidence `not assessed`, and block dependent claims.
## Decision Rules
| Choice or condition | Action | Failure or risk avoided |
|---|---|---|
| Mutable field has no authority | Block and assign ownership. | Desynchronisation or exploit. |
| NFR lacks conditions | Replace or mark provisional. | Decorative requirements. |
| Trust/money boundary exists | Add validation, idempotency and recovery. | Fraud or lost state. |
## Quality Standards
- Use stimulus, condition, response, measure, tolerance and verification method.
## Anti-Patterns
- “Fun” as requirement. Fix: define research evidence.
- “Runs smoothly.” Fix: name hardware, build and metric.
- Client-authoritative economy. Fix: trusted validation.
- Save migration omitted. Fix: add corruption and interruption cases.
- Menu-only accessibility. Fix: cover gameplay verbs.
- Retention or ad revenue as a solitary acceptance measure. Fix: pair with agency, trust, wellbeing, privacy, fairness and stopping evidence.
## References
- [Game requirement catalogue](references/game-requirement-catalogue.md)
- [Game narrative requirement contract](references/game-narrative-requirement-contract.md)
<!-- dual-compat-end -->
