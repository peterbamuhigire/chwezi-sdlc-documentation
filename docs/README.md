# Documentation index

This page indexes `docs/` for Chwezi SDLC Documentation. The root [`README.md`](../README.md) is the entry point and [`AGENTS.md`](../AGENTS.md) is the router for agents. Dated records keep the names and paths they were written with, including the former repository name `srs-skills`; do not rewrite them.

## Contracts and gates

| Document | What it defines |
|---|---|
| [`pathing-model.md`](pathing-model.md) | The canonical `projects/<ProjectName>/` workspace and the legacy `../project_context/` and `../output/` aliases. |
| [`deterministic-governance.md`](deterministic-governance.md) | How the phase gates are governed, with one gate file per phase: [`phase01`](deterministic-gate-phase01.md), [`phase02`](deterministic-gate-phase02.md), [`phase03`](deterministic-gate-phase03.md), [`phase04`](deterministic-gate-phase04.md), [`phase05`](deterministic-gate-phase05.md), [`phase06`](deterministic-gate-phase06.md), [`phase07`](deterministic-gate-phase07.md), [`phase08`](deterministic-gate-phase08.md), [`phase09`](deterministic-gate-phase09.md) and [`hybrid`](deterministic-gate-hybrid.md). |
| [`standards-clause-registry.md`](standards-clause-registry.md) | Every check ID mapped to a standard and clause. Several labels still cite superseded editions; see "Quality and improvement" in the root README. |
| [`hybrid-operating-model.md`](hybrid-operating-model.md) | The Water-Scrum-Fall contract. |
| [`regulated-evidence-model.md`](regulated-evidence-model.md) | The minimum evidence chain for regulated delivery. |
| [`sdd-phase-boundary-contract.md`](sdd-phase-boundary-contract.md) | The SDD phase-boundary contract checked by `scripts/validate_sdd_phase_boundaries.py`. |
| [`skill-authoring-standard.md`](skill-authoring-standard.md) | How to write and release a skill. |
| [`agent-runtime-safety.md`](agent-runtime-safety.md), [`approval-enforcement.md`](approval-enforcement.md), [`approval-adapter.json`](approval-adapter.json), [`control-plane-adoption.md`](control-plane-adoption.md) | The agent safety, approval and control-plane contracts. |
| [`ai-prompting/domain-prompt-compilation-contract.md`](ai-prompting/domain-prompt-compilation-contract.md) | The contract for prompt handoffs. |
| [`API.md`](API.md), [`DATABASE.md`](DATABASE.md) | Statements that the engine ships no runtime API and no database. |
| [`CHANGELOG.md`](CHANGELOG.md) | Dated changes, newest first. |

## Quality and improvement records

| Location | Contents |
|---|---|
| [`kaizen/2026-10-engine-kaizen/`](kaizen/2026-10-engine-kaizen/) | The 29 October 2026 cycle: scope, baseline scorecard, backlog, experiment log, validation record, final report, next-cycle notes and a dated source register. |
| [`kaizen/2026-10-engine-kaizen-pass-2/`](kaizen/2026-10-engine-kaizen-pass-2/) | The 31 October 2026 cycle (pass 2), with the same eight files plus [`07-docs-followups.md`](kaizen/2026-10-engine-kaizen-pass-2/07-docs-followups.md) from the documentation wave. Start with `05-final-report.md` and `06-next-cycle.md`. |
| [`audits/`](audits/) | The September 2026 audits, including the [29 September re-audit](audits/2026-09-29-m10-reaudit/README.md) (published 54.6 out of 100). |
| [`continuous-improvement/`](continuous-improvement/) | Earlier kaizen waves and records, including the [book-extraction retirement](continuous-improvement/book-extraction-retirement-2026-09-24.md). |
| [`updates/`](updates/) | Three dated engine updates. |
| [`engine-upgrade-july-2026/`](engine-upgrade-july-2026/), [`evaluation/2026-04-12/`](evaluation/2026-04-12/), [`implementation/review-05-Apr-2026/`](implementation/review-05-Apr-2026/) | Earlier evaluations and the July 2026 upgrade plan; the two reading lists are in `evaluation/2026-04-12/suggested-reading.md` and `engine-upgrade-july-2026/05-reading-list.md`. |
| [`migration/`](migration/) | The April 2026 skill-path migration table. |
| [`plans/`](plans/), [`superpowers/`](superpowers/) | Historical design plans and specifications. |

`docs/alignment-2026-06/` is local-only and gitignored; it is not part of the public repository.
