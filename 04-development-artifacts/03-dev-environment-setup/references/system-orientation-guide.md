# System Orientation Guide — Method and Quality Rules

A system orientation guide gives a developer who is new to a codebase a dependable route into it. It
sits beside the development environment setup guide: the setup guide gets the code running; the
orientation guide explains what the code is and in which order to read it. Use it when a team
inherits a system, when a new developer joins, or when an as-built design has been recovered
(`03-design-documentation/01-high-level-design/references/as-built-recovery.md`) and needs a
reading companion.

Start from `../templates/system-orientation-guide.md`. A worked example over this engine's own
`engine/` package is in `../examples/system-orientation-guide-srs-engine.md`.

## Fixed outline

The guide has seven sections, in this order:

1. **Overview.** What the system does, for whom, and where its boundaries are, in one or two
   paragraphs. Cite the vision or SRS where one exists.
2. **Architecture layers.** The layers or major components and the direction of dependency
   between them. Where an HLD exists, link its context and container figures rather than redrawing
   them.
3. **Key concepts.** The domain and technical terms a reader must know before the code makes sense.
   Each term links to the project glossary (`_context/glossary.md`); add missing terms to the
   glossary instead of defining them only here.
4. **Guided reading path.** Five to fifteen steps, ordered by dependency from the entry point
   outwards (see the ordering rule below).
5. **File map.** A table of the directories and files a reader will meet, with one line on the
   responsibility of each.
6. **Complexity hotspots.** The files that change most or are hardest to change safely, with the
   evidence for each claim.
7. **Staleness statement.** The commit the guide was written from and how to check whether it is
   still current.

## Reading-path ordering rule

- Begin at the entry point a user or operator actually triggers: the command-line entry, the
  front controller, the route file or the scheduled job.
- Each later step reads a file that the previous step calls, loads or hands data to. The reader
  should never meet a name that has not yet been explained.
- Treat a cluster of similar files (all the checks, all the reporters, all the migrations) as one
  step: read one member closely and state what the others share.
- Put edge cases (error handling, waivers, retries) after the main flow, and end with the step
  that produces the system's output.
- Stay within five to fifteen steps. Fewer than five means the steps are too coarse; more than
  fifteen means clusters have not been grouped.

## Writing each step

Each step is a short paragraph of formal prose, not a bullet fragment. It names one real repository
path in backticks, says what the reader will find there, and states how it connects to the previous
step ("`engine/artifact_graph.py` is what the command in step 1 builds before any gate runs").
Dashboard-style two-line captions are not sufficient for a deliverable; the reader must be able to
follow the path without the code open beside them.

## Evidence for hotspots

Base every hotspot on evidence, not impression:

- change frequency: `git log --format= --name-only -- <scope> | sort | uniq -c | sort -rn | head`;
- size: line counts of the largest files in scope;
- coupling: the number of modules that import the file (from a text search or the project's index).

State the command and the date it was run. Do not call a file "complex" without one of these
measures.

## Staleness and pinning

The guide's frontmatter carries `generated_from_commit` (the full 40-character SHA, quoted),
`source_repository` (a path relative to the project root, or absolute) and `referenced_paths`.
`python -m engine validate <project>` then reports each referenced path, and each backticked
repository path in the body, that has changed since the pinned commit
(`staleness/changed-since-generation`). When the source repository is not reachable the kernel
records `NOT_ASSESSED` rather than a pass.

## Quality checklist

- [ ] All seven sections are present in the fixed order.
- [ ] The reading path has 5–15 steps, each citing a real repository path and its link to the previous step.
- [ ] Every path in the reading path and the file map resolves in the pinned commit.
- [ ] Every key concept links to the glossary.
- [ ] Every hotspot cites a measure and the command that produced it.
- [ ] Frontmatter pins the guide with `generated_from_commit`, `source_repository` and `referenced_paths`.

## Related guidance

The engineering engine's code-tour guidance
(`chwezi-dev-engine/skills/sdlc-meta/doc-architect/references/code-tour.md`) applies the same
topology-first ordering to interactive tours; this reference is the documentation form of the same
principle.

## Attribution

Orientation outline, reading-path ordering and commit-pinned staleness adapted from Understand
Anything (MIT, https://github.com/Egonex-AI/Understand-Anything, commit
b05cc3b20990afca537b4fc0a49b4d7fbdc65bb0). Paraphrased.
