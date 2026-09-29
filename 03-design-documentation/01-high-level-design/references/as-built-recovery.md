# As-Built Design Recovery

Load this reference when a system already runs in production but has no current high-level design,
low-level design or database design, and the task is to document what exists. Typical cases are
PHP/MySQL business systems that have grown for years without design records. The output describes
the system as built. It is not a requirements document and it does not approve anything.

## The governing rule

The requirements-analysis skill states the guard this procedure depends on: "the repository tells
you how the system behaves today, not what the business requires it to do"
(`02-requirements-engineering/fundamentals/during/04-requirements-analysis/SKILL.md`, the Fixed policy
row of the provenance table). An as-built document may show that the code rounds a tax amount down;
it may not turn that observation into a requirement. Requirements still need a stakeholder source.

## Procedure

### Step 1 — Obtain structure without guesswork

Read structure from the code and the schema, not from memory or naming conventions:

- **Entry points.** Routes, controllers, command-line jobs, scheduled tasks, queue consumers and
  webhooks, taken from the router files and the scheduler configuration.
- **Services and modules.** The classes and functions those entry points call, followed as far as
  the design level needs (component level for HLD, class and method level for LLD).
- **Schema.** Tables, columns, keys, indexes, triggers and views from DDL and migrations only. A live
  database dump is acceptable when the migrations are incomplete, but record which source was used.
- **Integrations.** Outbound HTTP clients, message brokers, payment and SMS gateways, and file drops,
  with the configuration keys that select them.

For tooling, follow the engineering engine's graph-first comprehension reference
(`chwezi-dev-engine/skills/sdlc-meta/ai-assisted-development/references/graph-first-codebase-comprehension.md`):
query whatever index the project already has, then read the files it names. This reference adds no
tool dependency. Never accept "no callers" for a PHP member call (`$this->service->post()`) from any
index without a text search across the codebase; dynamic dispatch and container wiring hide callers
from static indexes.

### Step 2 — Map modules to design components

Group what Step 1 found into the components the HLD uses (context, containers, components, data
stores, external systems). Express each recovered figure as diagram IR, following
`diagram-ir-authoring.md` in this folder, and validate it with
`python -m engine diagrams validate <project>`. Recovered figures are then checked in the same way
as designed ones: every node and edge traces to an identifier or is flagged.

### Step 3 — Tag every statement with its provenance

Every descriptive statement carries one of two markers:

| Marker | Use for | Evidence required |
| --- | --- | --- |
| `[AS-BUILT]` | A fact read directly from code, configuration or schema | The file path and line, or the table and column, in the same sentence or an adjacent citation |
| `[VERIFY: reason]` | An inference (a behaviour deduced from several files) or an ambiguity (two readings of the same code, dead code of unknown status, a configuration value that differs by environment) | The reason names what a human must confirm and who can confirm it |

Write the marker at the end of the statement it qualifies, for example:
"Invoice numbers are allocated from the `invoice_sequences` table inside the posting transaction
(`app/Services/InvoiceService.php`, lines 88–120). [AS-BUILT]" and "Credit notes appear to be
unused since 2023; the last row in `credit_notes` is dated March 2023.
[VERIFY: confirm with the finance lead whether credit notes are raised outside the system]".

Both markers are non-blocking in the validation kernel: `python -m engine validate` reports them in
the artifact graph but does not fail the build on them. Whether unresolved `[VERIFY]` markers should
block client delivery is a doctrine decision reserved to the engine owner; until it is taken, list
every open `[VERIFY]` marker in the document's open-issues section before release.

### Step 4 — Pin the document to a commit

Add frontmatter that pins the document to the code it describes:

```yaml
generated_from_commit: "3f9c2e1d4b5a69788c7d6e5f4a3b2c1d0e9f8a7b"   # full 40-character SHA, quoted
source_repository: ../garage-erp                                   # path relative to the project root
referenced_paths:
  - app/Services/InvoiceService.php
  - database/migrations/2024_01_10_create_invoices_table.php
```

`python -m engine validate` then reports every referenced path that has changed since that commit
(`staleness/changed-since-generation`), so a reader knows which sections to re-check. Regenerate or
revise the affected sections and move the pin forward; never edit the pin without re-reading the
changed files.

### Step 5 — Keep description and requirement apart

Place the as-built documents under `03-design-documentation/` with "As-Built" in the title. Where the
recovered behaviour looks like a business rule, record it as a candidate for requirements
elicitation (an open question in `02-elicitation-toolkit`), not as an `FR-` or `BR-` identifier.
When a later SRS is written for the same system, each requirement cites a stakeholder or policy
source; an `[AS-BUILT]` statement may be cited as context but never as the authority.

## Quality checklist

- [ ] Every descriptive statement ends with `[AS-BUILT]` or `[VERIFY: reason]`.
- [ ] Every `[AS-BUILT]` statement cites a file and line, or a table and column.
- [ ] The schema description comes from DDL or migrations, and the source is named.
- [ ] Recovered figures are diagram IR and pass `python -m engine diagrams validate`.
- [ ] Frontmatter carries `generated_from_commit` (40 hexadecimal characters), `source_repository`
      and `referenced_paths`.
- [ ] No recovered behaviour has been given a requirement identifier.
- [ ] "No callers" claims for PHP member calls were cross-checked by text search.

## Attribution

Provenance tags (EXTRACTED / INFERRED / AMBIGUOUS) adapted from Graphify (Apache-2.0,
https://github.com/Graphify-Labs/graphify, commit d6eaa8aae8df155874ebb1044302c055c286342a).
Paraphrased; no Graphify text or code copied; Graphify is not a dependency. Here EXTRACTED maps to
`[AS-BUILT]`, and INFERRED and AMBIGUOUS both map to `[VERIFY: reason]`.
