---
document: system-orientation-guide
generated_from_commit: "<40-character SHA from git rev-parse HEAD>"
source_repository: <path to the repository, relative to the project root>
referenced_paths:
  - <repository-relative path of every file cited below>
---

# System Orientation Guide — <System Name>

> Method and quality rules: `references/system-orientation-guide.md` in the
> `03-dev-environment-setup` skill. Replace every angle-bracket placeholder.

## 1. Overview

<What the system does, for whom, and where its boundaries are. Cite the vision or SRS section.>

## 2. Architecture Layers

<The layers or major components and the direction of dependency between them. Link the HLD
figures where they exist.>

| Layer | Responsibility | Main paths | Depends on |
|---|---|---|---|
| <layer> | <responsibility> | `<path>` | <layer> |

## 3. Key Concepts

| Term | Meaning in this system | Glossary entry |
|---|---|---|
| <term> | <one-sentence meaning> | `_context/glossary.md#<term>` |

## 4. Guided Reading Path

<Five to fifteen steps, ordered from the entry point outwards. Each step is a short paragraph that
names one repository path in backticks, says what the reader will find there, and states how it
connects to the previous step.>

### Step 1 — <entry point>

<Paragraph citing `<path>`.>

### Step 2 — <what step 1 calls or builds>

<Paragraph citing `<path>` and its link to step 1.>

## 5. File Map

| Path | Responsibility |
|---|---|
| `<path>` | <one line> |

## 6. Complexity Hotspots

<Measured on <date> with `<command>`.>

| Path | Measure | Value | Why it matters to a new reader |
|---|---|---|---|
| `<path>` | <commits touching the file / line count / importers> | <n> | <consequence> |

## 7. Staleness Statement

This guide was written from commit `<SHA>` of `<repository>`. Run
`python -m engine validate <project>` to list referenced paths that have changed since then; revise
the affected steps and move the pin forward. If the repository is not reachable, the check reports
`NOT_ASSESSED`, not a pass.
