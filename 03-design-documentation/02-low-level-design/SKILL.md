---
name: 02-low-level-design
description: Use when an approved HLD needs implementation-ready module, class, sequence, state, algorithm and error contracts; use high-level-design for system boundaries, api-specification for external APIs, and database-design for persistence structures.
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---
# Low-Level Design Skill
<!-- dual-compat-start -->
## Use When

- A component boundary and its requirements are approved and developers need deterministic implementation detail.

## Do Not Use When

- Do not use to revisit system architecture silently or to generate code without approved behavioural contracts.

## Required Inputs

| Artefact | Source or provider | Required? | Missing behaviour |
|---|---|---|---|
| Approved HLD, requirements and ADRs | Phase 02/03 artefacts | Required | Stop if component ownership or interface is unresolved. |
| Language, platform and coding constraints | Technology decisions and engineering standards | Required | Return technology-neutral contracts when the stack is undecided. |

## Workflow

1. Read the named inputs and confirm their approval, version and unresolved decisions.
2. Apply the decision rules below before drafting; stop on a missing authority, unsafe assumption or unresolved scope driver.
3. Produce the Low-Level Design and traceability notes through the existing domain procedure and load only the references needed for the chosen branch.
4. Trace each material statement in the Low-Level Design and traceability notes to an input, decision or explicitly qualified assumption.
5. Verify the observable acceptance conditions, record unassessed checks, and hand the artefacts to their named consumers.
6. If validation fails, recover by correcting the source decision or artefact and rerun the affected check; do not weaken the acceptance condition.

## Outputs

| Artefact | Consumer | Observable acceptance condition |
|---|---|---|
| Low-Level Design and traceability notes | Implementers, reviewers and test engineers | Each unit has responsibilities, interfaces, state transitions, errors, concurrency rules and requirement-linked test oracles. |

## Evidence Produced

| Evidence | Consumer | Acceptance condition |
|---|---|---|
| Source and decision trace | Reviewer and downstream owner | Each material statement cites an approved input, named decision or qualified open issue. |
| Completed verification record | Release or phase gate owner | Every applicable check records pass/fail; unavailable checks remain `not assessed`. |

## Capability and permission boundaries

Read-only is the default for analysis, review, evaluation and planning. Read and search access to authorised project artefacts are required. Editing is limited to an explicitly requested project deliverable. Execution may run document, syntax or validation checks. Network access is used only for facts that require current verification. Do not publish, spend, change production, approve policy, or claim certification without explicit authority.

## Degraded mode

If any required capability is unavailable, return the narrowest useful qualified Low-Level Design and traceability notes draft plus a gap register showing the missing item, affected sections, risk and owner. Never convert an unassessed check into a pass.

## Decision Rules

| Choice | Action | Failure or risk avoided |
|---|---|---|
| Behaviour crosses a system boundary | Escalate to HLD/API ADR | Local design does not contradict architecture |
| Behaviour is module-internal | Specify in LLD | Implementation ambiguity is removed |

## Quality Standards

- Preserve repository terminology and trace every material choice to project context.
- Use deterministic acceptance conditions; replace vague quality claims with an observable check, threshold or named approval.
- Cover error, empty, edge, recovery and operational cases relevant to this skill.
- Verify standards, citations, APIs and package names before relying on them; qualify what cannot be checked.
- Stop release for a failed safety, security, legal, financial, accessibility or data-integrity gate.

## Anti-Patterns

- Repeating HLD component boxes. Fix: specify units, state and call sequence.
- Writing pseudocode with undefined failure paths. Fix: define errors and recovery.
- Inventing framework APIs. Fix: verify the selected stack or stay technology-neutral.
- Ignoring concurrency and idempotency. Fix: state the invariant and race handling.
- Producing classes with no requirement trace. Fix: map each responsibility to an approved requirement.

## References

- [High-Level Design neighbour](../01-high-level-design/SKILL.md)
- [API Specification neighbour](../03-api-specification/SKILL.md)
- [Database Design neighbour](../04-database-design/SKILL.md)
- [Diagram IR authoring](../01-high-level-design/references/diagram-ir-authoring.md): load before Steps 4 and 5; sequence and state figures are authored as IR against `diagram-ir.schema.json`, validated and generated.
- [As-built recovery](../01-high-level-design/references/as-built-recovery.md): load when the LLD describes existing code rather than a new design.
<!-- dual-compat-end -->




## Overview

This is the second skill in Phase 03 (Design Documentation). It decomposes the high-level components defined in HLD.md into implementable modules with class structures, interaction sequences, state transitions, and algorithmic detail. The resulting LLD.md serves as the definitive blueprint for developers, mapping every module back to its originating HLD component and SRS requirement.

## When to Use

- After the `01-high-level-design` skill has produced `HLD.md` in `projects/<ProjectName>/<phase>/<document>/`.
- Requires `business_rules.md` in `projects/<ProjectName>/_context/` for algorithm formalization and calculation logic.

## Quick Reference

| Attribute     | Value                                                                 |
|---------------|-----------------------------------------------------------------------|
| **Inputs**    | `projects/<ProjectName>/<phase>/<document>/HLD.md`, `projects/<ProjectName>/<phase>/<document>/SRS_Draft.md`, `projects/<ProjectName>/_context/business_rules.md` |
| **Output**    | `projects/<ProjectName>/<phase>/<document>/LLD.md`                                                    |
| **Tone**      | Implementation-precise, diagram-heavy, algorithm-focused              |
| **Standards** | IEEE 1016-2009 Sec 6, ISO/IEC 25010, ISO/IEC 25062                   |

## Input Files

| File               | Location                                  | Required | Purpose                                          |
|--------------------|-------------------------------------------|----------|--------------------------------------------------|
| HLD.md             | `projects/<ProjectName>/<phase>/<document>/HLD.md`                        | Yes      | Component architecture to decompose into modules |
| SRS_Draft.md       | `projects/<ProjectName>/<phase>/<document>/SRS_Draft.md`                  | Yes      | Stimulus-response pairs for sequence diagrams    |
| business_rules.md  | `projects/<ProjectName>/_context/business_rules.md`    | Yes      | Business logic and calculations to formalize     |

## Output Files

| File    | Location             | Description                                              |
|---------|----------------------|----------------------------------------------------------|
| LLD.md  | `projects/<ProjectName>/<phase>/<document>/LLD.md`   | Complete Low-Level Design with diagrams and algorithms   |
| diagrams/*.ir.json | `projects/<ProjectName>/<phase>/<document>/diagrams/` | Sequence and state figures as diagram IR |

## Core Instructions

Follow these nine steps in order. Halt and notify the user if a required input file is missing.

### Step 1: Read and Validate Inputs

Read `HLD.md` and `SRS_Draft.md` from `projects/<ProjectName>/<phase>/<document>/`, and `business_rules.md` from `projects/<ProjectName>/_context/`. Log every file path read. If any required file is missing, halt execution and report the gap.

### Step 2: Decompose Components into Modules

For each component identified in HLD.md, decompose it into modules and classes. Define each module's single responsibility, public interface, and internal dependencies. Group related classes into packages or namespaces that mirror the HLD layered architecture.

### Step 3: Generate Class Diagrams

Class diagrams have no diagram-IR kind yet, so produce Mermaid `classDiagram` blocks for each module, and put `%% alt: <what the figure shows>` and `%% caption: <caption>` comment lines inside every block so the rendered figure carries real alt text and a caption. Classes shall include:
- Typed attributes (`String`, `Integer`, `DECIMAL(19,4)` for monetary values, `DateTime`)
- Parameterized methods with return types
- Relationships: inheritance (`<|--`), composition (`*--`), dependency (`..>`), association (`-->`)

```mermaid
%% alt: Class diagram of the order module: Order contains OrderItem lines and calculates its total.
%% caption: Order module classes
classDiagram
    class Order {
        -orderId : UUID
        -totalAmount : DECIMAL(19,4)
        +calculateTotal() : DECIMAL(19,4)
        +applyDiscount(rate : DECIMAL(5,4)) : void
    }
    class OrderItem {
        -quantity : Integer
        -unitPrice : DECIMAL(19,4)
    }
    Order *-- OrderItem : contains
```

### Step 4: Author Sequence Figures as IR

Author one `sequence` IR figure (`<doc-dir>/diagrams/<name>.ir.json`, see `../01-high-level-design/references/diagram-ir-authoring.md`) for each of 5-8 critical workflows derived from SRS Section 3.2 stimulus-response pairs. Participants are nodes (role `participant`); messages are edges with `order` and `kind` (`sync`, `async`, `return`). Each figure shall show:
- Actor-to-component message flows, with the stimulus message traced to its FR (otherwise `diagram/unmapped-sequence`)
- Both the happy path and at least one error/alternate path (a separate figure when the paths diverge)
- Return values and asynchronous callbacks where applicable
- The stimulus-response pair as a `semantic_checks.required_paths` entry

### Step 5: Author State Machine Figures as IR

Author one `state` IR figure for every entity that has lifecycle states: roles `start`, `state` and `terminal`, transition guards as edge labels (for example `payment_verified`), and the terminal states the data model allows in `semantic_checks.allowed_terminals`. A non-terminal state without an outgoing transition fails with `diagram/dead-end-state`. Run `python -m engine diagrams validate projects/<ProjectName> --doc <doc-dir>` and `python -m engine diagrams generate projects/<ProjectName> --doc <doc-dir>`, fix every finding without deleting a trace or a semantic check, and embed each figure with `<!-- diagram-ir: FIG-nnn -->`. If the kernel cannot run, follow the reference's degraded mode and report the check as `NOT_ASSESSED`.

### Step 6: Formalize Business Rules as Algorithms

For each complex business rule in `business_rules.md`, produce structured pseudocode. Use LaTeX notation for all calculations:

- $LateFee = Balance \times Rate \times DaysOverdue$
- $Discount = SubTotal \times DiscountRate$ where $SubTotal > MinThreshold$

Include preconditions, postconditions, and edge-case guards for every algorithm. Document time complexity where relevant.

### Step 7: Design Error Handling

Define a comprehensive error handling strategy:
- **Error Code Taxonomy**: Enumerate domain-specific error codes mapped to HTTP status codes (e.g., `ORD-4001: Invalid order state transition` -> `409 Conflict`).
- **Exception Hierarchy**: Design the exception class tree (e.g., `ApplicationException` -> `ValidationException`, `BusinessRuleException`, `IntegrationException`).
- **Recovery Behavior**: Specify retry policy, fallback, or escalation per error type.

### Step 8: Define Data Validation Rules

For each input accepted by a module, define validation constraints per ISO/IEC 25062:
- Data type and format (e.g., email regex, ISO 8601 dates)
- Range checks (min/max values, string length bounds)
- Required vs. optional fields
- Cross-field validation rules (e.g., `endDate > startDate`)

### Step 9: Generate Traceability Matrix and Write Output

Produce a traceability table mapping every LLD module to its HLD component and originating SRS requirement ID:

| LLD Module           | HLD Component      | SRS Requirement IDs |
|----------------------|--------------------|---------------------|
| OrderService         | Order Management   | FR-3.2.1, FR-3.2.3 |
| PaymentGatewayAdapter| Payment Processing | FR-3.2.5, FR-3.2.6 |

Below the module matrix, embed the generated figure trace table with `<!-- diagram-ir: trace-table -->`; never type the figure-to-requirement rows by hand. Write the completed document to `projects/<ProjectName>/<phase>/<document>/LLD.md`. Log the total module count, diagram count, and algorithm count.

## Output Format

The generated `LLD.md` shall follow this structure:

```
# Low-Level Design: [Project Name]
## Document Header
## 1. Introduction and Scope
## 2. Module Decomposition
### 2.x [Module Name] -- Responsibility, Class Diagram, Dependencies
## 3. Interaction Sequences
### 3.x [Workflow Name] Sequence Diagram
## 4. State Machine Models
### 4.x [Entity Name] State Diagram
## 5. Algorithm Specifications
### 5.x [Rule Name] Pseudocode
## 6. Error Handling Design (Taxonomy, Hierarchy, Recovery)
## 7. Data Validation Rules
## 8. Traceability Matrix
## Appendix A: Glossary
```

## Common Pitfalls

1. **Missing state transitions**: Every state must have at least one outbound transition or be explicitly terminal. Orphan states indicate incomplete analysis.
2. **Incomplete sequence flows**: Omitting error paths produces optimistic designs. Every sequence diagram shall include at least one failure branch.
3. **Algorithms without edge cases**: Division by zero, null inputs, empty collections, and boundary values shall be guarded in every algorithm.
4. **Generic error handling**: "Catch all exceptions" is not a design. Each error type shall have a specific code, message, and recovery strategy.

## Verification Checklist

- [ ] Every HLD component decomposes into at least one LLD module with a class diagram.
- [ ] Class diagrams use typed attributes (including `DECIMAL(19,4)` for monetary values) and parameterized methods.
- [ ] At least 5 sequence diagrams cover critical workflows with both happy and error paths.
- [ ] State machine diagrams include all terminal states and transition guard conditions.
- [ ] Sequence and state figures are IR files that pass `python -m engine diagrams validate` with no HIGH finding; every class diagram block carries `%% alt:` and `%% caption:`.
- [ ] Every business rule algorithm includes preconditions, postconditions, and edge-case handling.
- [ ] Traceability matrix links every LLD module back to HLD components and SRS requirement IDs.

## Integration

| Direction  | Skill                                        | Relationship                                  |
|------------|----------------------------------------------|-----------------------------------------------|
| Upstream   | `03-design-documentation/01-high-level-design` | Consumes HLD.md component architecture      |
| Downstream | `03-design-documentation/03-api-specification`  | Feeds module interfaces for API contracts   |
| Downstream | `03-design-documentation/04-database-design`    | Feeds entity models for schema design       |
| Downstream | Phase 05 Testing                                | Feeds algorithms and state models for test case generation |

## Standards

- **IEEE 1016-2009 Sec 6**: Software Design Descriptions. Governs the structure of design viewpoints including decomposition, dependency, interface, and detail views.
- **ISO/IEC 25010**: Systems and software quality models. Provides the quality attribute framework referenced in module responsibilities.
- **ISO/IEC 25062**: Common Industry Format for usability test reports. Governs data validation rule documentation format.

## Resources

- `logic.prompt` -- executable prompt for automated LLD generation.
- `README.md` -- quick-start guide for this skill.
