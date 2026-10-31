---
name: 05-architecture-decision-records
description: Use when recording a consequential architecture choice, context, options, rationale, consequences, owner, and supersession path. Use ai-adr-catalogue for AI-system decisions and formal-review-gates for approval checkpoints.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Architecture Decision Records Skill

<!-- dual-compat-start -->

## Use When

- Use when recording a consequential architecture choice, context, options, rationale, consequences, owner, and supersession path. Use ai-adr-catalogue for AI-system decisions and formal-review-gates for approval checkpoints.

## Do Not Use When

- Do not use for trivial implementation choices that do not affect system structure, cost, or future flexibility.
- Do not use this skill to fabricate missing project facts, legal conclusions, test results, approvals, or certification claims.

## Required Inputs

| Artefact | Source or provider | Required? | Missing-input behaviour |
|---|---|---:|---|
| Decision problem; architectural context; constraints; viable options; evaluation evidence; affected interfaces; decision owner | Architecture owner and affected engineering or operations teams | Yes | Stop dependent work; name the missing item, owner, and decision impact. A review check remains `not assessed`. |
| Scope, audience, baseline/version, and accountable decision owner | Requester or project context | Yes | Ask for or record the gap; do not infer authority or scope. |

## Capability and permission boundaries

Default to read-only. Read and search access to the supplied artefacts are required. Editing is limited to an explicitly authorised requested draft or project files. Execute validation only when authorised; publishing, signature, certification, production mutation, destructive action, spending, and risk acceptance require explicit authority.

## Degraded Mode

When files, tools, network, rendering, fonts, execution, or evidence are unavailable, return the narrowest useful qualified draft or finding set. Name every unavailable check and its consequence; an unassessed check is never a pass. Preserve evidence already gathered and provide the exact next verification step.

## Decision Rules

| Condition | Action | Failure or risk avoided |
|---|---|---|
| A required source, owner, obligation, or acceptance condition is missing | Stop the affected claim and record the gap | Unsupported governance artefact |
| Evidence satisfies the declared acceptance condition | Record the decision and hand off to the named consumer | Ambiguous approval or release |

## Workflow

1. Confirm the requested artefact, audience, scope, decision owner, and applicable baseline or version. Work read-only by default; source mutation, publication, signature, certification, production change, or risk acceptance requires explicit authority.
2. Inspect every required input and record missing, stale, conflicting, or inaccessible evidence. Stop claims that depend on an unresolved required input.
3. Apply the Decision Rules, then execute the existing Core Instructions below in order; preserve project terminology and trace each material statement to its source.
4. Test the draft against the output acceptance conditions and domain quality standards. If a check cannot run, mark it `not assessed` and never convert it into a pass.
5. On failure, recover by preserving completed evidence, identifying the narrowest corrective action and owner, and rerunning only the affected checks before handoff.
6. Produce the named artefact and evidence record; publish, sign, certify, mutate production, or accept risk only under explicit authority.

## Outputs

| Artefact | Consumer | Observable acceptance condition |
|---|---|---|
| Architecture Decision Records | Accountable reviewer, control owner, auditor, or release authority | Each ADR records options, rationale, consequences, status, owner, date, and supersession links without rewriting history. |
| Gap and decision record | Accountable owner and downstream reviewer | Every gap has status, impact, owner, next action, and no unsupported pass or approval. |

## Evidence Produced

| Evidence | Contents | Acceptance condition |
|---|---|---|
| Architecture Decision Records evidence record | Source identifiers, scope/version, decisions, checks, exceptions, and approval state | A reviewer can reproduce each material conclusion from named sources. |
| Validation record | Check, result (`pass`, `fail`, or `not assessed`), evidence location, date, and actor | No required check is omitted or silently treated as passed. |

## Quality Standards

- Every ADR has status, decided_on, deciders; every `superseded_by` points to a real ADR; every catalog entry has a matching file.
- Use deterministic acceptance conditions and preserve traceability from source to decision and output.
- Separate facts, inferences, assumptions, and approvals; never present one as another.
- Apply `28-anti-ai-slop` during authoring and `29-ai-slop-audit` at major checkpoints and release.

## Anti-Patterns

- **Producing Architecture Decision Records from assumptions instead of named project sources.** Fix: Cite the source or mark the item unverified.
- **Treating a missing or inaccessible check as passed.** Fix: Mark it `not assessed`, state impact, and block dependent claims.
- **Using vague gates such as `adequate`, `secure`, or `user-friendly`.** Fix: Replace each with an observable criterion, threshold, and evidence source.
- **Copying a generic template without product, control, role, version, or jurisdiction detail.** Fix: Ground every section in the supplied context and remove unused boilerplate.
- **Publishing, signing, certifying, changing production, or accepting risk without authority.** Fix: Prepare a draft and route the decision to the accountable owner.
- **Listing evidence without provenance or an acceptance result.** Fix: Record source, period, integrity check, mapping, and pass/fail/not-assessed status.

## Worked Example

Example: if a required source, owner, obligation, or acceptance condition is missing, stop the affected claim and record the gap. Record the evidence and result in the validation record; this avoids unsupported governance artefact.

## References

- [Repository operating rules](../../AGENTS.md): apply the engine's routing, evidence, and release gates.
- [Domain language and decision context](../../02-requirements-engineering/fundamentals/during/05-conceptual-data-modeling/references/domain-language-and-decisions.md)

<!-- dual-compat-end -->

> **SaaS mode:** if the project is a multi-tenant SaaS, see `references/saas-adr-catalogue.md` for the expected ADR families.

## Overview

This skill produces one Architecture Decision Record (ADR) per significant architectural choice and registers it in the project ADR catalog. The catalog is the auditor-facing index the Phase 09 gate reconciles against the filesystem.

## When to Use This Skill

- When the team commits to a major technology choice (database, queue, language runtime).
- When deviating from a baselined constraint, standard, or reference architecture.
- When deprecating or superseding an earlier architectural decision.
- When a decision affects multiple modules, teams, or the cost model.

### Decision-moment detection (trigger phrases)

> Adapted from ECC's `architecture-decision-records` skill
> (upstream repository github.com/affaan-m/ECC),
> whose contribution over a plain template is that it is a *capture
> mechanism*, not just a format to fill in by hand.

Do not wait for the user to say "record an ADR." Treat the following as
signals that a decision moment just occurred, and suggest capturing it —
never auto-create the file without explicit confirmation:

**Explicit signals**
- "Let's go with X."
- "We should use X instead of Y."
- "The trade-off is worth it because..."

**The specific rejection-capture trigger**
- "We decided to..."
- "The reason we're doing X instead of Y is..."

Either phrasing means a rejected alternative exists somewhere in the
conversation that just happened. Do not let it evaporate — extract it into
the Alternatives Considered block (below) in the same turn, while the
reasoning is still available, rather than reconstructing it later from
memory.

## Inputs

- Decision title and one-paragraph context.
- Options considered (at least two) and the selected option.
- **For every rejected option: an explicit "Why not" line** (see Alternatives
  Considered below) — not just pros/cons, a stated reason it lost.
- Rationale: forces, trade-offs, and consequences.
- Deciders (role names) and decision date.

## Alternatives Considered — mandatory "Why not" line

Every rejected alternative recorded in an ADR MUST carry an explicit reason
it was rejected, not only a pros/cons list. Pros and cons describe the
option; "why not" is the actual rejection rationale, and it is the part of
an ADR that survives and the part AI-drafted ADRs most often omit. Use this
shape for each alternative, matching the ADR body template already in this
skill's `Output Contract`:

```markdown
### Alternative: [Name]
- **Pros:** [benefits]
- **Cons:** [drawbacks]
- **Why not:** [the specific reason this alternative was rejected — not
  "it was worse", but the concrete constraint, cost, or risk that decided it]
```

An alternative entry without a "Why not" line fails this skill's quality
check the same way a missing decider or a dangling `superseded_by` does —
"we just picked it" is not a valid rationale (see `Anti-Patterns` above).

## Stimulus / Process / Response

1. **Stimulus:** a decision point surfaces during design, review, or an incident post-mortem.
2. **Process:**
   1. Select the next sequential ID `ADR-NNNN`.
   2. Write the ADR file under `projects/<ProjectName>/09-governance-compliance/05-adr/NNNN-slug.md`.
   3. Append the entry to `projects/<ProjectName>/_registry/adr-catalog.yaml`.
   4. If the decision supersedes a prior ADR, set the prior entry's `status: superseded` and its `superseded_by` field.
3. **Response:** one new ADR file plus one catalog entry, reconciled by `AdrCatalogCheck`.

## Output Contract

- File: `projects/<ProjectName>/09-governance-compliance/05-adr/NNNN-<slug>.md` — content follows the ADR template.
- Registry: `projects/<ProjectName>/_registry/adr-catalog.yaml` — validated against `engine/registry/schemas/adr-catalog.schema.json`.

## Status Lifecycle

- `proposed` — drafted but not yet ratified by deciders.
- `accepted` — ratified; in force.
- `deprecated` — no longer recommended but not replaced.
- `superseded` — replaced by another ADR; `superseded_by` field MUST point to an existing catalog ID.

## Catalog Format

```yaml
adrs:
  - id: ADR-0001
    title: "Use PostgreSQL 15 as the primary RDBMS"
    status: accepted
    decided_on: 2026-04-16
    deciders: ["Chief Architect", "Tech Lead"]
    affects: ["03-design-documentation"]
```

## Worked example

See [`examples/representative/`](examples/representative/).
