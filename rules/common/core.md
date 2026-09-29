# Core Rules — SRS Engine

> Distilled from this engine's own `CLAUDE.md` / `AGENTS.md`.

## Establish shared understanding before starting a new project

When the user says "start a new project" or equivalent, first apply the
decision-frontier method in
`02-requirements-engineering/fundamentals/before/02-elicitation-toolkit/references/decision-frontier-elicitation.md`:
ask only the questions whose prerequisites are settled, write the stated
intent back, and stop until the owner confirms it. Then ask the five setup
questions (name, description, methodology, owner, team size) one at a time —
never as a list. `superpowers:brainstorming` may be used as an optional aid
where it is installed; it is not required.

## Run the hybrid-detection heuristic on the methodology answer

If the user answers "Agile" or "Scrum" but also describes formal documentation
gates, detailed up-front requirements, or end-of-cycle testing, flag this as a
potential Water-Scrum-Fall pattern and note it in `_context/vision.md`. Ask
explicitly: *"Does your team have a formal requirements sign-off before
development begins?"* — a "yes" confirms the hybrid.

## Client project documentation is never silently removed

Content under `projects/<ProjectName>/` is reviewed and either kept, edited, or
deleted **by the consultant** before building — never silently removed by the
agent. This directory is untracked and gitignored; it is not part of what this
engine publishes.

## Evidence Rule — self-assessment below full marks must cite the gap

> Grounded in ECC's `agent-self-evaluation` skill
> (`C:\Users\Peter\Downloads\ECC-main\skills\agent-self-evaluation\SKILL.md`).

Before calling any SRS, plan, or proposal deliverable produced by this engine
complete, any self-assessment that scores below full marks on a given
criterion — completeness, standards compliance, traceability, whatever axis
is being judged — **must cite specific evidence for the gap, not just name
it**. "Could be more complete" is not an assessment; "US-014 has no
error-path acceptance criterion" is. The mantra, verbatim from the ECC
source: *"Show the gap, don't just name it."*

This is a final gate, not a scoring ceremony: if a gap can be closed in the
same turn (an unfilled traceability row, a missing "Must not" line), close it
before reporting completion rather than merely noting it. If it cannot be
closed without stakeholder input, state exactly what evidence is missing and
who must supply it — do not silently round the assessment up to pass.

## Cross-engine routing for methodology and finance content

Engineering/methodology skills route to the `chwezi-dev-engine` engine; finance,
IFRS, IAS, tax, and bookkeeping route to `chwezi-accounting-doctrine`. Consult
both in addition to the active SRS work when the content calls for them — never
duplicate their doctrine locally.
