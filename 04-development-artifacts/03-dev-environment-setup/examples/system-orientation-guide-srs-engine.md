---
document: system-orientation-guide
generated_from_commit: "9b8a27fc2a536766023353e221109252793cd1ea"
source_repository: .
referenced_paths:
  - engine/cli.py
  - engine/workspace.py
  - engine/artifact_graph.py
  - engine/parsers/frontmatter.py
  - engine/parsers/markers.py
  - engine/gates/base.py
  - engine/gates/phase02.py
  - engine/checks/traceability.py
  - engine/checks/markers.py
  - engine/findings.py
  - engine/waivers.py
  - engine/reporters/markdown.py
---

# System Orientation Guide — SRS Engine Validation Kernel (worked example)

> Worked example for `references/system-orientation-guide.md`. It orients a new maintainer in this
> repository's own `engine/` package, so every path below can be checked in continuous integration
> (`engine/tests/test_system_orientation_example.py`). In this example the "project root" is the
> repository root, hence `source_repository: .`.

## 1. Overview

The validation kernel is a Python package, invoked as `python -m engine`, that reads a client
project workspace under `projects/<ProjectName>/` and decides whether its documentation meets the
engine's contracts. It does not write requirements. It parses the Markdown artefacts, runs a fixed
set of gates, applies any approved waivers and reports the remaining findings as Markdown, JUnit or
SARIF. A finding of HIGH severity fails the run. The kernel's boundary is the workspace directory:
it reads project files and registries and writes only the reports and registry files that a
command explicitly names.

## 2. Architecture Layers

Dependencies point downwards in the table: each layer uses only the layers beneath it.

| Layer | Responsibility | Main paths | Depends on |
|---|---|---|---|
| Command line | Parse commands and options; compose the run | `engine/cli.py` | All layers below |
| Reporting | Render findings for people and CI tools | `engine/reporters/` | Findings |
| Gates | Group checks by life-cycle phase and attach standards clauses | `engine/gates/` | Checks, graph, findings |
| Checks | One rule each over the artefact graph | `engine/checks/` | Graph, findings |
| Artefact graph | Immutable in-memory model of the workspace | `engine/artifact_graph.py`, `engine/parsers/` | Workspace |
| Workspace | Locate and enumerate the project's files | `engine/workspace.py` | None |

## 3. Key Concepts

| Term | Meaning in this system | Glossary entry |
|---|---|---|
| Workspace | A project directory that contains `_context/` | `_context/glossary.md#workspace` |
| Artefact | One Markdown file with its frontmatter, identifiers and markers | `_context/glossary.md#artefact` |
| Marker | A bracketed tag such as `[CONTEXT-GAP: reason]` that flags an open issue | `_context/glossary.md#marker` |
| Gate | A named group of checks for one phase, with a severity and a standards clause | `_context/glossary.md#gate` |
| Finding | One reported result with severity, location and optional diagnostic fields | `_context/glossary.md#finding` |
| Waiver | A time-limited, approved exception to one gate for one scope | `_context/glossary.md#waiver` |

## 4. Guided Reading Path

### Step 1 — The command-line entry

Begin with `engine/cli.py`. The `validate` command is the path a consultant and the CI pipeline
both take: it loads the workspace, builds the artefact graph, runs every gate registered in
`_default_registry()`, applies waivers and chooses the exit code. Read this function first, because
every later step is something it calls; the other commands (`sync`, `baseline`, `diagrams`,
`signoff`) reuse the same building blocks.

### Step 2 — Locating the workspace

The first object `validate` creates comes from `engine/workspace.py`. It is deliberately small: it
refuses any directory without `_context/` and enumerates every Markdown file beneath the root in
sorted order. That sorted enumeration is why findings appear in a stable order from run to run.

### Step 3 — Building the artefact graph

Step 1 then passes the workspace to `engine/artifact_graph.py`. For each file it records the path,
title, phase, identifiers written in bold and the markers, and freezes the result. Every check reads
this graph rather than the file system, so a check can be tested with a graph built from a temporary
directory.

### Step 4 — Parsing frontmatter and markers

The graph delegates two parsing tasks. `engine/parsers/frontmatter.py` reads the YAML block at the
top of each file, and `engine/parsers/markers.py` finds bracketed markers while ignoring those
quoted in inline code or fenced blocks. The ignore rule is what lets skill documents describe the
marker vocabulary without tripping the kernel.

### Step 5 — The gate contract

With the graph built, step 1 runs the gates. `engine/gates/base.py` defines the contract every gate
honours (an identifier, a title, a severity and an `evaluate` method) and the registry that refuses
duplicate identifiers. Read it before any concrete gate, because it explains why the order of
registration in step 1 is also the order of the report.

### Step 6 — A concrete phase gate

`engine/gates/phase02.py` is a representative gate. It composes several checks (SMART
non-functional requirements, the stimulus-response form, requirement semantics, the identifier and
glossary registries) and attaches the governing IEEE clause to each finding. The other phase gates
in `engine/gates/` follow the same pattern for their phases, so one close reading is enough.

### Step 7 — The checks as a cluster

The gates in step 6 call checks in `engine/checks/`. Read `engine/checks/traceability.py` as the
representative member: it takes the graph, applies one rule (every functional requirement links up
to a business goal and down to a test case) and adds findings. The other checks share that shape;
they differ only in the rule.

### Step 8 — The blocking-marker gate

`engine/checks/markers.py` is the one check registered directly as a gate. It turns any unresolved
blocking marker found in step 4 into a HIGH finding. It is the reason a draft that still says
`[CONTEXT-GAP: …]` cannot pass, and it is the gate that most often fails a consultant's first run.

### Step 9 — Findings

Every check and gate writes to the collection defined in `engine/findings.py`. The severity scale
decides blocking (HIGH and above), and the optional diagnostic fields (code, subject, evidence,
supported fixes) carry machine-readable detail for repairing agents without changing older checks.

### Step 10 — Waivers, the edge case

Before reporting, step 1 applies `engine/waivers.py`. A waiver names a gate, a scope, an approver
and an expiry of at most ninety days; a malformed register stops the run, and an expired waiver
no longer removes its finding. Read this after the main flow, because it only removes findings that the earlier
steps produced.

### Step 11 — Reporting the result

The run ends in `engine/reporters/markdown.py` (and its JUnit and SARIF siblings in
`engine/reporters/`). The Markdown reporter lists the remaining and the waived findings for the
consultant; the other two feed CI annotations. Step 1 then exits non-zero if any remaining finding
is blocking.

## 5. File Map

| Path | Responsibility |
|---|---|
| `engine/cli.py` | Command-line commands and the default gate registry |
| `engine/workspace.py` | Workspace location and file enumeration |
| `engine/artifact_graph.py` | Immutable artefact graph |
| `engine/parsers/` | Frontmatter and marker parsing |
| `engine/gates/` | Phase gates and the gate contract |
| `engine/checks/` | Individual rules over the graph |
| `engine/findings.py` | Finding, severity and collection types |
| `engine/waivers.py` | Waiver register and application |
| `engine/reporters/` | Markdown, JUnit and SARIF output |
| `engine/registry/schemas/` | JSON schemas for registries and diagram IR |
| `engine/tests/` | Unit tests and fixtures, including `engine/tests/fixtures/healthcare_admissions/` |

## 6. Complexity Hotspots

Measured on 29 September 2026 with
`git log --format= --name-only -- engine | sort | uniq -c | sort -rn | head` (change frequency) and
`wc -l` (size).

| Path | Measure | Value | Why it matters to a new reader |
|---|---|---|---|
| `engine/cli.py` | Commits touching the file | 14 | Every new command lands here; read the whole file before adding one |
| `engine/gates/phase09.py` | Commits touching the file | 12 | Governance rules change with regulation; expect frequent revisions |
| `engine/gates/phase03.py` | Commits touching the file | 9 | Design gates grew with the diagram IR work |
| `engine/diagram_ir.py` | Line count | 451 | The largest single module; read `engine/registry/schemas/diagram-ir.schema.json` first |

## 7. Staleness Statement

This guide was written from commit `9b8a27fc2a536766023353e221109252793cd1ea` of this repository.
Place it in a workspace and run `python -m engine validate <project>` to list referenced paths that
have changed since then; revise the affected steps and move the pin forward. If the repository is
not reachable, the check reports `NOT_ASSESSED`, not a pass.
