# Reference: Authoring Design Figures as Diagram IR

Load this reference whenever a High-Level Design, Low-Level Design or Database Design needs a figure. It replaces free-hand Mermaid for the figure kinds listed below. The figure, its Mermaid preview and the traceability table are all derived from one validated source, so a figure cannot drift from the requirements it claims to realise.

The IR contract is `engine/registry/schemas/diagram-ir.schema.json` (JSON Schema draft 2020-12, `schema_version` 1). The pattern is adapted from Archify (MIT, https://github.com/tt-a1i/archify, commit 0e4949f910a8e390bd3b4933883a4dcabad571be); the text here is paraphrased and no schema, code or test text was copied.

## 1. When a figure is required

The figure obligations are unchanged from the skills:

| Skill | Figure | IR kind |
|---|---|---|
| HLD Step 3 | System context | `context` |
| HLD Step 4 | Component architecture | `component` |
| HLD Step 5 | Deployment topology | `deployment` |
| HLD Step 7 | Each major data flow | `dataflow` |
| LLD Step 4 | Each critical workflow from SRS §3.2 | `sequence` |
| LLD Step 5 | Each entity with a lifecycle | `state` |
| Database Design Step 4 | Entity-relationship model | `erd` |

Class diagrams (LLD Step 3) have no IR kind in `schema_version` 1. Author them as fenced Mermaid `classDiagram` blocks with the `%% alt:` and `%% caption:` comments described in section 7.

## 2. Where the files live

Work inside the document directory that `scripts/build-doc.sh` stitches (for example `projects/<ProjectName>/03-design-documentation/01-high-level-design/`):

```text
<doc-dir>/diagrams/<name>.ir.json        one figure per file (you author these)
<doc-dir>/_generated/<FIG-nnn>.mmd       generated Mermaid preview (never edit)
<doc-dir>/_generated/trace-table.md      generated traceability table (never edit)
<doc-dir>/_generated/.validated.json     hashes accepted by the last validate
<doc-dir>/_generated/.generated.json     hashes written by the last generate
```

Embed a figure in a section file with a marker on its own line, and the traceability table the same way:

```markdown
<!-- diagram-ir: FIG-001 -->
<!-- diagram-ir: trace-table -->
```

`scripts/render_diagrams.py` expands each marker at build time into a captioned figure with alt text. It refuses to build when an IR changed after the last validate or when the generated files are stale.

## 3. The IR document

Every object is closed: an unknown property is an error (`schema/additionalProperties`).

| Field | Rule |
|---|---|
| `schema_version` | `1` |
| `diagram_kind` | one of `context`, `component`, `deployment`, `sequence`, `state`, `dataflow`, `erd` |
| `meta.figure_id` | `FIG-001` … `FIG-999`, unique within the document |
| `meta.title`, `meta.caption` | sentence case; the caption is printed below the figure |
| `meta.alt_text` | at least 20 characters; says what the figure shows, not "diagram of…" alone |
| `meta.srs_section` | the SRS section the figure realises, e.g. `3.2` |
| `meta.owner_document` | POSIX-relative path of the section file; no `..`, drive letter or backslash |
| `nodes[]` | `id`, `label`, `role`; optional `trace`, `description`, `boundary`, `lane`; `attributes` on `erd` entities only |
| `edges[]` | `id`, `from`, `to`; optional `label`, `trace`; `kind` and `order` required on `sequence`; `cardinality` required on `erd` |
| `boundaries[]` | optional grouping (`id`, `label`, `trace`), drawn as a subgraph |
| `semantic_checks` | optional; see section 5 |
| `evidence` | `srs_section`, optional `baseline_label`, `source_documents[]` (relative paths of the SRS files used) |

Roles per kind: `context` {system, person, external_system}; `component` {component, datastore, queue, external}; `deployment` {node, zone, datastore, external}; `sequence` {participant}; `state` {start, state, terminal}; `dataflow` {process, store, external_entity}; `erd` {entity}. ERD attributes are `{name, type, key}` with `key` one of `pk`, `fk`, `none`; use `DECIMAL(19,4)` for money. Sequence message `kind` is `sync`, `async` or `return`.

## 4. Naming identifiers and filling `trace`

- Element ids are lower case, start with a letter, and use `a-z`, `0-9`, `-` or `_` (at most 48 characters): `api-gateway`, `pending-review`. Ids are unique across the nodes, edges and boundaries of one figure and stay stable across revisions, because the baseline delta tracks them.
- `trace` lists requirement identifiers exactly as they appear in `_registry/identifiers.yaml`. Run `python -m engine sync projects/<ProjectName>` first, then copy the ids. Never invent an id; an unknown id fails with `diagram/unknown-trace-id`.
- Trace each element to the requirements it realises: components and flows to FRs and NFRs, the stimulus message of a sequence to its stimulus-response FR, lifecycle states and transitions to the FRs that govern them.
- Every in-scope FR should appear on at least one element across the project's figures. An FR drawn nowhere is reported as `diagram/uncovered-requirement` (report-only in this release).

## 5. Stating `semantic_checks`

Semantic checks turn the requirements into closed-world rules the kernel proves on the figure. They never change the generated Mermaid.

- `required_paths`: for each SRS §3.2 stimulus-response pair the figure realises, add `{from: <stimulus source>, to: <responding element>}`.
- `required_edges`: an interaction the SRS names explicitly (for example "the system shall notify the billing service").
- `allowed_terminals`: the end states the data model allows (for example `closed`, `cancelled`). In a `state` figure every non-terminal state needs an outgoing transition, or the check reports `diagram/dead-end-state`.
- `allowed_roots`: legitimate entry points. `state` figures default to their `start` nodes; `dataflow` figures default to external entities and stores.

If a check fails, repair the figure (add the missing edge, transition or trace) or correct the SRS through change control. Never repair by deleting the requirement from `trace` or the semantic check that failed.

## 6. Command sequence

```text
python -m engine sync projects/<ProjectName>
python -m engine diagrams validate projects/<ProjectName> --doc <doc-dir>
python -m engine diagrams generate projects/<ProjectName> --doc <doc-dir>
bash scripts/build-doc.sh <doc-dir> <OutputName>
python -m engine diagrams verify-manifest <doc-dir>
```

`validate` prints each finding with its code, JSON-pointer subject and supported fixes, and records the accepted IR hashes. `generate` refuses an IR whose hash differs from the validated one (`diagram/candidate-not-validated`). `build-doc.sh` writes `<OutputName>.figures.json` beside the `.docx` with the IR, Mermaid, PNG and SVG hashes, the renderer version, the font family and the font-substitution result. `verify-manifest` names any figure whose source or output changed after the build.

What the checks prove: that every trace id exists, that the declared structure holds, and that each FR is drawn somewhere. They do not prove that the design is right; that remains a reviewer judgement.

## 7. Mermaid that is not IR

Existing Mermaid stays valid and is rendered by `scripts/render_diagrams.py`. Convert a figure to IR when its document is next revised. For any fenced Mermaid block you keep, put two comment lines inside the block so the figure has real alt text and a caption instead of the nearest heading:

````markdown
```mermaid
%% alt: Class diagram of the billing module: Invoice aggregates InvoiceLine and uses TaxPolicy.
%% caption: Billing module classes
classDiagram
  ...
```
````

## 8. Degraded mode

If the kernel cannot run (no Python, no project workspace), still author the IR files. Mark each figure in the document `[V&V-FAIL: diagram IR not validated]`, leave the trace-table marker in place, and report the validate, generate and render checks as `NOT_ASSESSED`. Do not paste hand-written Mermaid or a hand-typed traceability table as a substitute.
