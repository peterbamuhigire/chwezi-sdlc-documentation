---
name: 02-elicitation-toolkit
description: "Use when selecting and conducting interviews, workshops, observation, surveys, document analysis, or prototypes to gather requirements; use stakeholder-analysis to identify participants first."
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---

# Elicitation Toolkit Skill

<!-- local-contract-start -->
<!-- dual-compat-start -->
## Use When

- selecting and conducting interviews, workshops, observation, surveys, document analysis, or prototypes to gather requirements; use stakeholder-analysis to identify participants first.
- Use this procedure when the required source artefacts are available and `Elicitation plan, raw evidence, and issue log` is the next lifecycle deliverable.

## Do Not Use When

- Use `stakeholder-analysis` when that neighbouring route owns the decision or deliverable.
- Do not invent missing project evidence, standards clauses, thresholds, or stakeholder decisions.

## Required Inputs

| Artefact | Source or provider | Required? | Behaviour when missing |
| --- | --- | --- | --- |
| Stakeholder register, elicitation objectives, domain context, constraints, and consent needs | Business analyst, sponsor, and project context | Yes | Stop the affected step, name the missing source, and return only a qualified gap record. |

## Workflow

1. Inspect the required inputs and log the exact sources, versions, unresolved assumptions, and decision owners.
   State and record the ceremony class (bounded, architectural or spike); draft and approve one numbered section at a time (`references/ceremony-and-section-approval.md`).
2. Build a dependency graph of open decisions. Resolve discoverable facts from project or verified external evidence instead of asking stakeholders to retrieve them.
3. Ask only the current decision frontier: unresolved choices whose prerequisites are satisfied. Batch independent questions; do not ask a dependent choice early.
4. Apply the selected elicitation technique and update the decision graph, glossary, confirmed facts, conflicts, and open issues after each round.
5. Stop when a required source, accountable decision owner, deterministic test oracle, or shared-understanding gate is absent.
6. Recover by preserving valid work, marking the blocked scope, and returning the narrowest qualified artefact plus the next evidence or decision needed.

## Outputs

| Artefact | Consumer | Acceptance condition |
| --- | --- | --- |
| Elicitation plan, raw evidence, and issue log | Requirements analysis and project decision owners | Required sections are populated, source links resolve, and every material requirement or decision has an observable review or test oracle. |

## Evidence Produced

| Evidence | Reviewer | Acceptance condition |
| --- | --- | --- |
| Source, decision, trace, and validation record for `Elicitation plan, raw evidence, and issue log` | Requirements quality reviewer | Inputs used, decisions made, checks run, failures, and unassessed items are explicit. |

## Capability and permission boundaries

Read and search are required. Editing is allowed only when the request authorises creation or repair of the named requirements artefact. Publishing, production mutation, destructive action, spending, and certification require explicit authority.

## Degraded mode

Fallback: if a required file, reviewer, standard source, network check, renderer, or execution capability is unavailable, return the narrowest useful qualified result and mark the affected check `not assessed`; never convert an unassessed check into a pass.

## Decision Rules

| Choice or condition | Action | Failure or risk avoided |
| --- | --- | --- |
| A claim is important but has only one conflicted or indirect source | Triangulate it or mark it disputed before requirements analysis. | False consensus and invented requirements. |
| Required inputs and test oracles are complete | Continue through the existing workflow and record evidence. | A deliverable whose acceptance cannot be reproduced. |
| A mandatory source or owner is missing | Stop the affected branch and issue a qualified gap record. | Fabricated context or unauthorised decisions. |

## Quality Standards

- Preserve stable identifiers and bidirectional traceability from project evidence to `Elicitation plan, raw evidence, and issue log` and its acceptance checks.
- Apply ISO/IEEE measures only with a named metric, method, threshold, evidence source, and responsible reviewer; run the anti-slop gate before release.

## Anti-Patterns

- Producing `Elicitation plan, raw evidence, and issue log` from assumed context. Fix: cite the project source or mark the scope blocked.
- Accepting a material requirement without a deterministic oracle. Fix: add a measurable result, boundary, and verification method.
- Crossing into `stakeholder-analysis` without routing the decision. Fix: hand off the named input and preserve trace links.
- Treating an unavailable check as passed. Fix: mark it `not assessed` and state the release consequence.
- Claiming standards, statutory, or stakeholder approval without evidence. Fix: cite the source and reviewer or qualify the claim.

## References

- [Skill authoring and release standard](../../../../docs/skill-authoring-standard.md)
- [Domain Checklists](references/domain-checklists.md)
- [Interview Guide](references/interview-guide.md)
- [Jad Workshop](references/jad-workshop.md)
- [Observation Ethnography](references/observation-ethnography.md)
- [Prototyping For Elicitation](references/prototyping-for-elicitation.md)
- [Questionnaires Surveys](references/questionnaires-surveys.md)
- [Decision-frontier elicitation](references/decision-frontier-elicitation.md)
- [Ceremony classification and section-scoped approval](references/ceremony-and-section-approval.md)
<!-- dual-compat-end -->
<!-- local-contract-end -->

## Overview

This skill provides a structured, multi-technique approach to requirements elicitation. It guides the AI through selecting the most appropriate elicitation technique based on stakeholder availability, domain complexity, and requirements maturity, then executes the chosen technique to produce a grounded elicitation log. The skill supports interviews, Joint Application Development (JAD) workshops, prototyping, observation, questionnaires, contextual inquiry, benchmarking, and artifact analysis, with domain-specific checklist hooks for specialized industries.

## When to Use This Skill

- After the stakeholder register has been produced by `01-stakeholder-analysis`
- When requirements need to be gathered from diverse stakeholder groups
- When the elicitation technique is unclear and a decision framework is needed
- When domain-specific requirements (healthcare, SaaS, POS, GIS) require specialized checklists
- When previous elicitation rounds produced incomplete or ambiguous requirements

## Quick Reference

| Attribute | Value |
|-----------|-------|
| **Inputs** | `projects/<ProjectName>/<phase>/<document>/stakeholder_register.md`, `projects/<ProjectName>/_context/vision.md`, `projects/<ProjectName>/_context/features.md` |
| **Output** | `projects/<ProjectName>/<phase>/<document>/elicitation_log.md` |
| **Tone** | Investigative, methodical, source-attributed |
| **Standards** | IEEE 29148-2018 Section 6.3, Laplante Ch.4, Wiegers Practices 4-6 |

## Input Files

| File | Location | Required | Purpose |
|------|----------|----------|---------|
| stakeholder_register.md | `projects/<ProjectName>/<phase>/<document>/stakeholder_register.md` | Yes | Stakeholder roles, communication preferences, engagement levels |
| vision.md | `projects/<ProjectName>/_context/vision.md` | Yes | Business goals, problem statement, domain context |
| features.md | `projects/<ProjectName>/_context/features.md` | Yes | Feature list for elicitation scoping |
| glossary.md | `projects/<ProjectName>/_context/glossary.md` | No | Domain terminology for consistent language |

## Output Files

| File | Location | Description |
|------|----------|-------------|
| elicitation_log.md | `projects/<ProjectName>/<phase>/<document>/elicitation_log.md` | Structured findings with source attribution, technique used, and confidence levels |

## Core Instructions

Follow these six steps in order. Halt and notify the user if a required input file is missing.

### Step 1: Read Context Files

Read `stakeholder_register.md` from `projects/<ProjectName>/<phase>/<document>/`, and `vision.md` and `features.md` from `projects/<ProjectName>/_context/`. Optionally read `glossary.md`. Log every file path read. If any required file is missing, halt execution and report the gap.

### Step 2: Assess Elicitation Context

Evaluate three dimensions to determine the appropriate elicitation technique:

**Dimension 1 -- Stakeholder Availability**

| Level | Description | Indicator |
|-------|-------------|-----------|
| High | Stakeholders are accessible for extended, interactive sessions | On-site team, dedicated availability windows |
| Medium | Stakeholders are available for scheduled sessions with limited duration | Remote team, shared across projects |
| Low | Stakeholders are difficult to reach or available only asynchronously | External clients, regulators, distributed globally |

**Dimension 2 -- Domain Complexity**

| Level | Description | Indicator |
|-------|-------------|-----------|
| High | Domain requires specialized knowledge, regulatory compliance, or complex workflows | Healthcare, finance, aerospace, legal |
| Medium | Domain has moderate complexity with some specialized terminology | E-commerce, SaaS, logistics |
| Low | Domain is well-understood with common patterns | CRUD applications, content management |

**Dimension 3 -- Requirements Maturity**

| Level | Description | Indicator |
|-------|-------------|-----------|
| Greenfield | No existing requirements; starting from scratch | New product, new market |
| Evolving | Partial requirements exist but need refinement | MVP iteration, feature expansion |
| Mature | Well-documented existing requirements needing validation | System migration, modernization |

### Step 3: Select Elicitation Technique

Use the following decision matrix to recommend one or more techniques:

| Context | Primary Technique | Secondary Technique |
|---------|-------------------|---------------------|
| High availability + High complexity + Greenfield | JAD Workshop | Interview |
| High availability + Low complexity + Greenfield | Interview | Prototyping |
| Medium availability + High complexity + Evolving | Interview | Contextual Inquiry |
| Medium availability + Medium complexity + Evolving | Prototyping | Questionnaire |
| Low availability + Any complexity + Any maturity | Questionnaire | Artifact Analysis |
| Any availability + High complexity + Mature | Contextual Inquiry | Interview |
| Any availability + Low complexity + Mature | Questionnaire | Artifact Analysis |
| New system replacing legacy / migration project | Artifact Analysis | Interview |
| NFR definition or competitive positioning needed | Benchmarking | Interview |
| Users cannot articulate needs verbally | Contextual Inquiry | Observation |

Present the recommendation to the user with rationale. The user may override the selection.

### Step 4: Execute Elicitation Technique

Execute the selected technique using the corresponding protocol. Each technique produces structured findings.

#### Technique A: Structured Interview

1. Select target stakeholders from the register (prioritize "Manage Closely" and "Keep Informed" quadrants)
2. Prepare interview questions using the three-tier approach:
   - **Context questions**: Establish the stakeholder's role and perspective
   - **Open-ended questions**: Explore needs, pain points, and workflows
   - **Closed questions**: Confirm specific requirements, constraints, and priorities
3. For each finding, record:
   - Source stakeholder (by ID from the register)
   - Verbatim statement or paraphrase
   - Requirement type: Functional, Non-Functional, Constraint, or Assumption
   - Confidence level: Confirmed, Likely, or Uncertain

Reference: `references/interview-guide.md`

#### Technique B: JAD Workshop

1. Define workshop scope and objectives from `features.md`
2. Identify participants from the stakeholder register (minimum: one sponsor, two users, one developer)
3. Structure the workshop agenda:
   - Opening: scope confirmation, ground rules
   - Discovery: facilitated discussion of features and workflows
   - Consensus: prioritization and conflict resolution
   - Closure: action items and next steps
4. Record consensus decisions, dissenting views, and open items

Reference: `references/jad-workshop.md`

#### Technique C: Prototyping

1. Identify features from `features.md` that benefit from visual exploration
2. Describe low-fidelity prototype elements (screens, workflows, data layouts)
3. Define feedback questions for each prototype element
4. Record stakeholder reactions, suggested changes, and confirmed requirements

Reference: `references/prototyping-for-elicitation.md`

#### Technique D: Observation

1. Identify processes or workflows relevant to the project scope
2. Define observation targets: tasks, sequences, decision points, pain points
3. Document observed workflows with:
   - Step-by-step task descriptions
   - Time estimates per task
   - Error-prone steps
   - Workarounds currently in use
4. Derive requirements from observed gaps and inefficiencies

Reference: `references/observation-ethnography.md`

#### Technique E: Questionnaire

1. Design the questionnaire with question types matched to information needs:
   - Multiple choice for categorical data
   - Likert scale (1-5) for satisfaction and priority ratings
   - Open-ended for qualitative insights
2. Target distribution to stakeholder groups from the register
3. Define minimum response thresholds for statistical validity
4. Summarize responses with aggregated metrics and notable outliers

Reference: `references/questionnaires-surveys.md`

#### Technique F: Contextual Inquiry

1. Arrange to observe target stakeholders in their actual working environment while they perform real tasks (not a staged demo)
2. Adopt the "apprentice" posture — the analyst is a learner; the stakeholder is the expert performing their normal work
3. Ask questions in real time while observing; do not defer all questions to a separate debrief session
4. Document observed workflows with:
   - Step-by-step task descriptions including physical environment interactions
   - Tacit knowledge and undocumented workarounds currently in use
   - Physical or environmental constraints that affect system requirements
   - Discrepancies between what stakeholders say they do and what they actually do
5. Derive requirements from observations; tag requirements sourced solely from verbal statements vs. observed behaviour
6. Record field notes immediately; produce process maps from the notes before the next working session

- **Best for:** Discovering undocumented workflows, tacit knowledge, physical environment constraints; domains where users cannot fully articulate their needs in a formal interview setting
- **Output:** Field notes, process maps, discovered requirements that users could not articulate verbally

Reference: `references/observation-ethnography.md`

#### Technique G: Benchmarking

1. Identify the comparison targets: industry standards, regulatory benchmarks, or direct competitor products relevant to the project domain
2. Define the comparison dimensions aligned to the project scope (features, performance thresholds, NFR values, UX patterns)
3. For each dimension, record:
   - The client's current state (from context files or stakeholder interviews)
   - The benchmark value or feature presence in the comparison target
   - The gap classification: Functional Gap (missing feature), Performance Gap (below threshold), or Parity (meets benchmark)
4. Derive NFR targets from benchmark performance data; express as measurable thresholds (e.g., "The system shall process a transaction in ≤ 2 seconds, per industry median of 1.8 seconds")
5. Use the gap list to set stakeholder expectations before detailed requirements are written; attach the benchmark table to the elicitation log

- **Best for:** Establishing NFR baselines, identifying table-stakes features, setting stakeholder expectations for new system capabilities
- **Output:** Benchmark comparison table, functional and performance gap list, NFR targets derived from industry standards

Reference: `references/benchmarking-template.md`

#### Technique H: Data Gathering / Artifact Analysis

1. Collect all available existing artefacts from the client: documents, reports, spreadsheets, database schemas, input forms, screen captures, and logs from the current system
2. For each artefact, record:
   - Artefact ID and type (form, report, schema, screenshot, policy document)
   - Source system or process
   - Business rules embedded in the artefact (calculated fields, validation rules, conditional logic)
   - Data entities, attributes, and observed relationships
3. Annotate each artefact with derived requirements and business rules; use `[ARTEFACT-SOURCE: <ID>]` tags to preserve traceability
4. Identify discrepancies between artefact-derived requirements and verbally stated requirements; flag each discrepancy with `[CONFLICT: Artefact vs. Stated Requirement]`
5. Build a data dictionary entry for every data entity discovered; feed entries into the project glossary
6. For legacy system migration projects, map every existing field and rule to a proposed new-system equivalent; mark gaps with `[MIGRATION-GAP]`

- **Best for:** Understanding as-is processes, identifying hidden business rules, legacy system migration, and cross-checking verbally stated requirements against physical evidence
- **Output:** Annotated artefacts, business rule inventory, data dictionary entries, migration gap list (if applicable)

Reference: `references/artifact-analysis-checklist.md`

### Step 5: Apply Domain-Specific Checklists

If the project domain matches one of the following, apply the corresponding checklist to ensure domain-critical requirements are not missed:

| Domain | Checklist Focus | Key Concerns |
|--------|----------------|--------------|
| **Healthcare** | HIPAA compliance, HL7/FHIR integration, patient data handling | Privacy, audit trails, interoperability |
| **SaaS** | Multi-tenancy, subscription billing, API rate limiting | Tenant isolation, usage metering, SLA |
| **POS** | Payment processing, inventory sync, offline mode | PCI-DSS, real-time updates, hardware integration |
| **GIS** | Spatial data handling, coordinate systems, map rendering | Projection accuracy, data volume, tile caching |

For each checklist item, record whether the item was addressed (Yes/No/Partial) and the source of the finding.

Reference: `references/domain-checklists.md`

### Step 6: Write Elicitation Log

Assemble all findings and write to `projects/<ProjectName>/<phase>/<document>/elicitation_log.md`. Log the total finding count, technique(s) used, and the number of unresolved items.

## Output Format Specification

The generated `elicitation_log.md` shall follow this structure:

```
# Elicitation Log: [Project Name]

## Document Header
- Project: [Name]
- Version: 1.0
- Date: [Current Date]
- Technique(s) Used: [Interview / JAD / Prototyping / Observation / Questionnaire / Contextual Inquiry / Benchmarking / Artifact Analysis]
- Status: Draft

## 1. Elicitation Context
### 1.1 Stakeholder Availability Assessment
### 1.2 Domain Complexity Assessment
### 1.3 Requirements Maturity Assessment
### 1.4 Technique Selection Rationale

## 2. Elicitation Findings
### 2.1 Functional Requirements
### 2.2 Non-Functional Requirements
### 2.3 Constraints
### 2.4 Assumptions

## 3. Source Attribution Matrix

## 4. Domain Checklist Results (if applicable)

## 5. Open Items and Unresolved Questions

## 6. Confidence Summary

## 7. Standards Traceability

## Appendix A: Raw Interview/Workshop Notes
## Appendix B: Revision History
```

Each finding in Section 2 shall use this format:

```
#### EL-XXX: [Finding Title]

- **Type**: Functional | Non-Functional | Constraint | Assumption
- **Source**: [Stakeholder ID] -- [Role]
- **Technique**: [Interview | JAD | Prototyping | Observation | Questionnaire]
- **Statement**: "[Verbatim or paraphrased stakeholder statement]"
- **Derived Requirement**: The system shall [requirement statement].
- **Confidence**: Confirmed | Likely | Uncertain
- **Priority**: Critical | High | Medium | Low
- **Notes**: [Additional context or dependencies]
```

## Common Pitfalls

- Selecting a single technique without considering stakeholder availability, leading to low participation and incomplete findings
- Recording findings without source attribution, making downstream validation impossible
- Skipping domain-specific checklists, resulting in missed regulatory or integration requirements
- Treating elicitation as a one-pass activity rather than iterating when confidence levels are low
- Using leading questions that bias stakeholder responses toward a predetermined solution
- Failing to distinguish between requirements, constraints, and assumptions in the log

## Verification Checklist

- [ ] All required input files were read and logged
- [ ] Elicitation context was assessed across all three dimensions
- [ ] Technique selection rationale is documented and grounded in context assessment
- [ ] Every finding has a source stakeholder ID, technique, and confidence level
- [ ] Findings are classified by type (Functional, Non-Functional, Constraint, Assumption)
- [ ] Domain-specific checklists were applied if the domain matches a supported category
- [ ] Open items and unresolved questions are explicitly listed
- [ ] No requirement statement uses subjective language without a defined metric
- [ ] Standards Traceability section maps to IEEE 29148 Section 6.3

## Integration

| Direction | Skill | Relationship |
|-----------|-------|-------------|
| Upstream | `01-stakeholder-analysis` | Consumes stakeholder register |
| Downstream | `03-brd-generation` | Feeds elicitation findings for BRD generation |
| Downstream | `02-requirements-engineering/waterfall/05-feature-decomposition` | Feeds functional requirements |
| Downstream | `02-requirements-engineering/agile/01-user-story-generation` | Feeds user-facing requirements |

## Standards Compliance

| Standard | Governs |
|----------|---------|
| IEEE 29148-2018 Section 6.3 | Requirements elicitation process and techniques |
| Laplante Ch.4 | Elicitation technique selection and execution |
| Wiegers Practice 4 | Interview and workshop facilitation |
| Wiegers Practice 5 | Observation and contextual inquiry (Techniques D and F) |
| Wiegers Practice 6 | Survey and questionnaire design |
| Adzic (2012) — Impact Mapping | Contextual Inquiry apprentice model; discovering tacit requirements |
| IEEE Std 610.12-1990 | Terminology definitions |

## Resources

- `references/interview-guide.md` -- Structured interview protocol
- `references/jad-workshop.md` -- JAD workshop facilitation guide
- `references/prototyping-for-elicitation.md` -- Low-fi prototyping workflow
- `references/observation-ethnography.md` -- Contextual inquiry and observation checklist (Techniques D and F)
- `references/questionnaires-surveys.md` -- Survey design templates
- `references/domain-checklists.md` -- Domain-specific elicitation checklists
- `references/benchmarking-template.md` -- Benchmark comparison table and gap classification guide (Technique G)
- `references/artifact-analysis-checklist.md` -- Artifact inventory, business rule extraction, and migration gap checklist (Technique H)
- [Java enterprise requirements overlay](../../../references/java-enterprise-requirements-overlay.md) -- elicit version, transaction, failure, migration, production, and support evidence for Java/JVM estates
