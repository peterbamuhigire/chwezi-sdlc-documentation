---
name: 17-game-system-architecture-specification
description: "Use when designing game client, authoritative state, engine integration, content, saves, multiplayer backend, platform adapters, telemetry, security, build, and live-operations architecture from an approved game SRS."
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Game System Architecture Specification
<!-- dual-compat-start -->
## Use When
- An approved game SRS needs architecture and ADRs.
## Do Not Use When
- Detailed classes are the task; use the game technical implementation specification.
- Do not hide authority or save ownership inside engine components.
## Required Inputs
| Artefact | Source or provider | Required? | Behaviour when missing |
|---|---|---|---|
| `GREQ-*`, engine/platform decision, topology, budgets and risks | Requirements, architecture and production | Yes | Stop and return unresolved decisions. |
| Plugins, platform services, data and threat constraints | Specialist owners | Conditional | Mark integration provisional. |
## Workflow
1. Draw contexts for client, services, platform, content/build, telemetry and operators.
2. Define state, command/event flow, determinism, saves/migrations and time/randomness ownership.
3. Establish engine-neutral domain boundaries and Unity, Godot, Unreal or Apple adapters.
4. Specify content streaming, asset import, graphics/audio/UI/camera budgets, accessibility/localisation settings and fallbacks, consuming approved visual contracts from `chwezi-design-engine`.
5. Design online topology, replication budget, sessions, persistence and compatibility where applicable.
6. Design trust, data/economy/ad integrity, separate SDK privacy boundaries, child-safe disabled defaults, build provenance, observability and rollback/kill switches.
7. Define shared-platform seams as optional capabilities with per-game adoption, identity, performance and simplicity criteria; do not force every package into every game.
8. Stop on a missing owner, budget, privacy/rights boundary or failure path; recover with ADR options.
## Outputs
| Artefact | Consumer | Acceptance condition |
|---|---|---|
| Game architecture and ADRs | Implementers, QA, security and operations | State, interfaces, failures, budgets and traces are reviewable. |
## Evidence Produced
| Evidence | Reviewer | Acceptance condition |
|---|---|---|
| `GARCH-*` trace and failure model | Architecture board | Each element maps to requirement, ADR, test and signal. |
## Capability and permission boundaries
Read and search are allowed. Provisioning, purchasing or production change requires explicit authority.
## Degraded mode
Produce the narrowest qualified context, mark unavailable checks `not assessed`, and name the experiment needed.
## Decision Rules
| Choice or condition | Action | Failure or risk avoided |
|---|---|---|
| Logic can avoid engine objects | Isolate testable domain code. | Engine coupling. |
| Action originates on client | Validate authoritative state. | Cheating. |
| Schema changes | Version, migrate and test rollback. | Lost state. |
## Quality Standards
- Express state and failure behaviour; verify version-sensitive facts officially.
## Anti-Patterns
- Giant scene. Fix: bounded lifetimes.
- Component as architecture. Fix: domain/adapters.
- Reliable messages everywhere. Fix: semantic budgets.
- Config without kill switch. Fix: validation and expiry.
- Service as hard dependency. Fix: degraded behaviour.
- Ads/analytics treated as one consent boundary. Fix: model each SDK, purpose, data flow, deletion and disable path separately.
## References
- [Game architecture viewpoints](references/game-architecture-viewpoints.md)
- [Game AI and narrative architecture contract](references/game-ai-narrative-architecture-contract.md)
<!-- dual-compat-end -->
