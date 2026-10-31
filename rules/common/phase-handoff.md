# Phase Handoff — Each Arrow Is a File on Disk

> Grounded in ECC's `docs/PLAN-PRD-PATTERN.md`
> (upstream repository github.com/affaan-m/ECC): *"Each arrow
> is a file on disk, not a conversation in memory."* Confirmed against this
> engine's own actual handoff points before being written as a rule — see
> `01-strategic-vision/README.md`'s Dependencies section and
> `02-requirements-engineering/waterfall/01-initialize-srs/SKILL.md`, both of
> which already work this way; this rule makes the pattern explicit and
> engine-wide instead of leaving it implicit per phase.

## The rule

Every SDLC phase transition in this engine
(`01-strategic-vision` → `02-requirements-engineering` → `03-design-documentation`
→ `04-development-artifacts` → `05-testing-documentation` →
`06-deployment-operations` → `07-agile-artifacts` → `08-end-user-documentation`
→ `09-governance-compliance`) must produce a committable staging file under
`projects/<ProjectName>/<phase>/<document>/` that the next phase's skill
**explicitly reads and cites**, not a conversational summary carried forward
in the agent's context window.

This engine already does this in practice — `02-requirements-engineering`'s
`01-initialize-srs` seeds `projects/<ProjectName>/_context/` (vision,
features, tech stack, business rules, quality standards, glossary) precisely
so every downstream IEEE/ISO skill has a "writeable folder" and a named
source file to read rather than relying on what was said earlier in the
session. `01-strategic-vision/README.md` states the same contract in its
Dependencies section: "Downstream: Phase 02 ... consumes the strategic
outputs" — the outputs, meaning the files, not the conversation that produced
them.

## Why this matters here specifically

- **Transferable.** A reviewer or a fresh agent session can pick up
  `projects/<ProjectName>/02-requirements-engineering/01-srs/` on its own and
  be caught up — no replaying the elicitation conversation.
- **Auditable.** `09-governance-compliance`'s traceability matrix, baseline
  delta, and sign-off ledger all depend on being able to point at a specific
  file and version, not "what the agent said it did."
- **Machine-checkable.** `08-waiver-management`, `07-baseline-delta`, and the
  routing smoke tests can diff a staging file against its prior version. They
  cannot diff a conversation.
- **Resumable.** A project can sit idle between phases for weeks; the next
  phase's skill must not depend on session continuity.

## What to check

- A phase's skill that claims to consume "the vision" or "the requirements"
  without naming the file path it read is violating this rule — require the
  explicit path (e.g., `projects/<ProjectName>/_context/vision.md`,
  `projects/<ProjectName>/02-requirements-engineering/01-srs/`) in its own
  Input Files table, the way `04-requirements-analysis` and
  `02-acceptance-criteria` already do.
- If a phase is skipped for small-scope work (e.g., no `01-prd-generation`
  needed for a two-page brief — see the depth-selector guidance in
  `02-requirements-engineering`), that is a legitimate shortcut, exactly as
  ECC's pattern allows skipping `/plan-prd` for scoped bug fixes. The rule is
  about how phases connect when they run, not a mandate that every phase must
  always run.
