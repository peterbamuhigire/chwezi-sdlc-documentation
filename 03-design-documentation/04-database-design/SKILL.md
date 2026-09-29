---
name: 04-database-design
description: Use when approved requirements and access patterns need an entity model, normalised schema, keys, constraints, indexes, tenancy, retention and migration plan; use HLD for ownership and accounting-engine-design for ledger invariants.
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---
# Database Design Skill
<!-- dual-compat-start -->
## Use When

- Persistent data structures must be specified before implementation or migration.

## Do Not Use When

- Do not use to design API payloads, bypass domain ownership, or optimise from guessed queries.

## Required Inputs

| Artefact | Source or provider | Required? | Missing behaviour |
|---|---|---|---|
| Approved entity rules and access patterns | SRS, HLD and API contracts | Required | Stop if ownership, lifecycle or identifiers are unresolved. |
| Workload, tenancy, retention and migration constraints | Operations, security and data owners | Required | Qualify absent volume evidence and avoid speculative indexes. |

## Workflow

1. Read the named inputs and confirm their approval, version and unresolved decisions.
2. Apply the decision rules below before drafting; stop on a missing authority, unsafe assumption or unresolved scope driver.
3. Produce the Database Design, entity model, data dictionary and migration plan through the existing domain procedure and load only the references needed for the chosen branch.
4. Trace each material statement in the Database Design, entity model, data dictionary and migration plan to an input, decision or explicitly qualified assumption.
5. Verify the observable acceptance conditions, record unassessed checks, and hand the artefacts to their named consumers.
6. If validation fails, recover by correcting the source decision or artefact and rerun the affected check; do not weaken the acceptance condition.

## Outputs

| Artefact | Consumer | Observable acceptance condition |
|---|---|---|
| Database Design, entity model, data dictionary and migration plan | Backend, data, test, security and operations teams | Constraints enforce invariants; indexes map to named access patterns; migration has rollback and verification; sensitive data has retention and access rules. |

## Evidence Produced

| Evidence | Consumer | Acceptance condition |
|---|---|---|
| Source and decision trace | Reviewer and downstream owner | Each material statement cites an approved input, named decision or qualified open issue. |
| Completed verification record | Release or phase gate owner | Every applicable check records pass/fail; unavailable checks remain `not assessed`. |

## Capability and permission boundaries

Read-only is the default for analysis, review, evaluation and planning. Read and search access to authorised project artefacts are required. Editing is limited to an explicitly requested project deliverable. Execution may run document, syntax or validation checks. Network access is used only for facts that require current verification. Do not publish, spend, change production, approve policy, or claim certification without explicit authority.

## Degraded mode

If any required capability is unavailable, return the narrowest useful qualified Database Design, entity model, data dictionary and migration plan draft plus a gap register showing the missing item, affected sections, risk and owner. Never convert an unassessed check into a pass.

## Decision Rules

| Choice | Action | Failure or risk avoided |
|---|---|---|
| Invariant must hold for every writer | Enforce with schema constraint where possible | Application bypass cannot corrupt data |
| Index has no named access pattern | Omit pending evidence | Write cost and storage are not wasted |

## Quality Standards

- Preserve repository terminology and trace every material choice to project context.
- Use deterministic acceptance conditions; replace vague quality claims with an observable check, threshold or named approval.
- Cover error, empty, edge, recovery and operational cases relevant to this skill.
- Verify standards, citations, APIs and package names before relying on them; qualify what cannot be checked.
- Stop release for a failed safety, security, legal, financial, accessibility or data-integrity gate.

## Anti-Patterns

- Using an ERD without constraints. Fix: specify keys, nullability, uniqueness and checks.
- Adding indexes by intuition. Fix: map each index to a measured query pattern.
- Using destructive migration without rollback. Fix: stage, backfill, verify and cut over.
- Ignoring tenant keys. Fix: define isolation and composite-key rules.
- Storing derived balances as source truth. Fix: define canonical records and rebuild rules.

## References

- [HLD neighbour](../01-high-level-design/SKILL.md)
- [API Specification neighbour](../03-api-specification/SKILL.md)
- [Accounting Engine Design neighbour](../16-accounting-engine-design/SKILL.md)
- [Diagram IR authoring](../01-high-level-design/references/diagram-ir-authoring.md): load before Step 4; the ERD is authored as IR against `diagram-ir.schema.json`, validated and generated.
- [As-built recovery](../01-high-level-design/references/as-built-recovery.md): load when recovering a schema design from DDL and migrations of a running system.
<!-- dual-compat-end -->




## Overview

Produces comprehensive database design documentation including a visual Entity-Relationship Diagram (authored as diagram IR, rendered through a generated Mermaid erDiagram), normalized table definitions, indexing strategy, constraint specifications, migration plan, and a complete data dictionary. This skill can run after HLD is complete and may execute in parallel with API Specification (03-api-specification). **MANDATORY:** When the target platform is MySQL, this skill SHALL integrate with `skills/mysql-best-practices/` and apply all rules defined therein.

## When to Use

- After `HLD.md` exists in `projects/<ProjectName>/<phase>/<document>/` and identifies data storage components.
- SRS Section 3.2 (Functional Requirements) provides entity candidates and business logic.
- `business_rules.md` in `projects/<ProjectName>/_context/` provides data relationships, validation rules, and constraints.
- `tech_stack.md` in `projects/<ProjectName>/_context/` specifies the database platform.

## Quick Reference

| Attribute   | Value |
|-------------|-------|
| **Inputs**  | `projects/<ProjectName>/<phase>/<document>/SRS_Draft.md`, `projects/<ProjectName>/<phase>/<document>/HLD.md`, `projects/<ProjectName>/_context/business_rules.md`, `projects/<ProjectName>/_context/tech_stack.md` |
| **Outputs** | `projects/<ProjectName>/<phase>/<document>/Database_Design.md`, `projects/<ProjectName>/<phase>/<document>/diagrams/erd.ir.json` (Mermaid generated into `_generated/`) |
| **Tone**    | Schema-precise, normalized, constraint-heavy |
| **Standard** | IEEE 1016-2009 Sec 6.7, ISO/IEC 25010 |

## Input Files

| File | Location | Required | Purpose |
|------|----------|----------|---------|
| SRS_Draft.md | `projects/<ProjectName>/<phase>/<document>/SRS_Draft.md` | Yes | Entity candidates from Section 3.2, data objects from Section 2.0 |
| HLD.md | `projects/<ProjectName>/<phase>/<document>/HLD.md` | Yes | Data storage components, architectural context, data flow paths |
| business_rules.md | `projects/<ProjectName>/_context/business_rules.md` | Yes | Data relationships, validation constraints, business logic rules |
| tech_stack.md | `projects/<ProjectName>/_context/tech_stack.md` | Yes | Database platform (MySQL 8.x, PostgreSQL, etc.), version constraints |

## Output Files

| File | Location | Description |
|------|----------|-------------|
| Database_Design.md | `projects/<ProjectName>/<phase>/<document>/Database_Design.md` | Complete database design document with all sections |
| erd.ir.json | `projects/<ProjectName>/<phase>/<document>/diagrams/erd.ir.json` | Diagram IR for the entity-relationship model; `diagrams generate` writes the Mermaid `erDiagram` to `_generated/FIG-nnn.mmd` |

## Core Instructions

Follow these eleven steps in order. Halt and notify the user if a required input file is missing.

### Step 1: Read Context Files

Read `SRS_Draft.md` and `HLD.md` from `projects/<ProjectName>/<phase>/<document>/`, and `business_rules.md` and `tech_stack.md` from `projects/<ProjectName>/_context/`. Log the absolute path of each file read. If any required file is missing, halt execution and report the gap.

### Step 2: Determine Database Platform

Parse `tech_stack.md` to identify the target database platform (MySQL 8.x, PostgreSQL, MariaDB, etc.). If the platform is MySQL or MariaDB, load and apply `skills/mysql-best-practices/` rules MANDATORILY for all subsequent steps. Document the platform version and any engine-specific constraints (e.g., InnoDB for MySQL).

### Step 3: Extract Entities

Extract entity candidates from SRS Section 3.2 (functional requirements) and Section 2.0 (data objects). Each entity becomes a table candidate. Cross-reference with `business_rules.md` to identify additional entities implied by relationships or constraints. List all identified entities with a one-sentence description.

### Step 4: Author the ERD as Diagram IR

Author an `erd` IR figure at `projects/<ProjectName>/<phase>/<document>/diagrams/erd.ir.json` (see `../01-high-level-design/references/diagram-ir-authoring.md`): one `entity` node per table with typed `attributes` (`key` `pk`, `fk` or `none`; `DECIMAL(19,4)` for money), one edge per relationship with `cardinality` (`1:1`, `1:N`, `N:M`, `0..1:N`), and a junction entity for every many-to-many relationship. Trace each entity to the FRs that create or read it. Run `python -m engine diagrams validate` and `python -m engine diagrams generate`; the generated `_generated/FIG-nnn.mmd` replaces the hand-written `erd.mmd`, and `<!-- diagram-ir: FIG-nnn -->` embeds the figure in `Database_Design.md`.

### Step 5: Verify Normalization

Analyze every table against normalization forms:
- **1NF:** Atomic values only, no repeating groups.
- **2NF:** No partial dependencies on composite keys.
- **3NF:** No transitive dependencies.

Document any intentional denormalization with a performance rationale citing specific query patterns or SRS requirements that justify the deviation.

### Step 6: Generate Table Definitions

For each table, specify: column name, data type, nullable flag, default value, and constraints (PK, FK, UNIQUE, CHECK, NOT NULL). Monetary values SHALL use `DECIMAL(19,4)` per the logic-modeling convention. Every table SHALL include `id` (PK), `created_at`, and `updated_at` audit columns. Include `deleted_at` for soft-delete tables where business rules require data retention.

### Step 7: Define Relationships and Foreign Keys

For every foreign key, explicitly state: parent table, child table, column mapping, `ON DELETE` action (CASCADE, SET NULL, RESTRICT), and `ON UPDATE` action. Referential integrity SHALL be enforced at the database level. Foreign key columns SHALL be indexed.

### Step 8: Define Indexing Strategy

Define indexes for each table with rationale:
- **Primary key indexes:** Every table (automatic).
- **Unique indexes:** Natural keys (email, username, slug).
- **Foreign key indexes:** Every FK column.
- **Composite indexes:** Common query patterns (include column order rationale).
- **Full-text indexes:** Search fields where applicable.

### Step 9: Generate Data Dictionary

Produce a comprehensive data dictionary covering every field across all tables:

| Table | Field | Type | Description | Constraints | Example Value |
|-------|-------|------|-------------|-------------|---------------|

Every column in every table SHALL appear in this dictionary.

### Step 10: Define Migration Strategy

Document the migration approach: versioned migrations (up/down scripts), seed data for reference tables, rollback procedures for each migration, and environment-specific considerations (dev, staging, production).

### Step 11: Multi-Tenancy and Final Output

If multi-tenancy is detected in SRS or HLD, define the tenant isolation strategy: shared database with `tenant_id` FK on every tenant-scoped table, or separate schemas. The `tenant_id` column SHALL have a foreign key constraint and be included in composite indexes for query performance. Write `Database_Design.md` and `diagrams/erd.ir.json` to `projects/<ProjectName>/<phase>/<document>/`, then validate and generate. Log total table count, column count, and relationship count.

## Output Format

The generated `Database_Design.md` shall use this section structure with a Document Header (Date, Version, Authors, Standard, Database Platform), followed by nine sections:

1. **Entity-Relationship Diagram** -- `<!-- diagram-ir: FIG-nnn -->` marker for the ERD IR (typed attributes and cardinality)
2. **Normalization Analysis** -- 1NF/2NF/3NF verification per table; denormalization rationale
3. **Table Definitions** -- One subsection per table with Column/Type/Nullable/Default/Constraints columns
4. **Relationships and Foreign Keys** -- FK definitions with ON DELETE/ON UPDATE cascade rules
5. **Indexing Strategy** -- Index definitions with rationale per table
6. **Data Dictionary** -- Table/Field/Type/Description/Constraints/Example Value for every column
7. **Migration Strategy** -- Versioned migrations (up/down), seed data, rollback procedures
8. **Multi-Tenancy** -- Tenant isolation strategy (if applicable)
9. **Traceability Matrix** -- Table/SRS Section/Requirement IDs/Business Rule mapping

Example ERD IR (generated into Mermaid `erDiagram` by `python -m engine diagrams generate`):

```json
{
  "schema_version": 1,
  "diagram_kind": "erd",
  "meta": {"figure_id": "FIG-001", "title": "Order data model", "caption": "Users, orders and order items",
           "alt_text": "Entity-relationship diagram: a user places many orders; each order contains one or more order items.",
           "srs_section": "3.3", "owner_document": "03-design-documentation/04-database-design/Database_Design.md"},
  "nodes": [
    {"id": "users", "label": "Users", "role": "entity", "trace": ["FR-001"],
     "attributes": [{"name": "id", "type": "INT", "key": "pk"}, {"name": "email", "type": "VARCHAR(255)", "key": "none"}]},
    {"id": "orders", "label": "Orders", "role": "entity", "trace": ["FR-002"],
     "attributes": [{"name": "id", "type": "INT", "key": "pk"}, {"name": "user_id", "type": "INT", "key": "fk"},
                    {"name": "total_amount", "type": "DECIMAL(19,4)", "key": "none"}]}
  ],
  "edges": [{"id": "places", "from": "users", "to": "orders", "label": "places", "cardinality": "1:N"}],
  "evidence": {"srs_section": "3.3", "source_documents": ["02-requirements-engineering/01-srs/srs.md"]}
}
```

## Common Pitfalls

| Pitfall | Remedy |
|---------|--------|
| Missing indexes on foreign keys | Every FK column SHALL have a corresponding index |
| No cascade rules defined | Every FK SHALL specify ON DELETE and ON UPDATE actions |
| Monetary values not using DECIMAL(19,4) | All currency/monetary columns SHALL use DECIMAL(19,4) |
| Missing soft delete columns | Tables with data retention rules SHALL include deleted_at |
| No audit columns | Every table SHALL have created_at and updated_at columns |
| Denormalization without rationale | Document the performance justification for every deviation from 3NF |

## Verification Checklist

- [ ] `Database_Design.md` and `diagrams/erd.ir.json` exist in `projects/<ProjectName>/<phase>/<document>/`.
- [ ] The ERD IR passes `python -m engine diagrams validate` with no HIGH finding, and the generated `erDiagram` renders through `scripts/build-doc.sh`.
- [ ] All tables have primary keys defined.
- [ ] Foreign keys have ON DELETE and ON UPDATE cascade rules defined.
- [ ] Monetary columns use `DECIMAL(19,4)`.
- [ ] Data dictionary covers every field in every table.
- [ ] `skills/mysql-best-practices/` rules applied if MySQL or MariaDB detected.

## Integration

| Direction | Skill | Relationship |
|-----------|-------|-------------|
| Upstream | 01-high-level-design | Consumes `HLD.md` for data storage components and data flow paths |
| Downstream | Phase 04 (Development) | Provides schema definitions for ORM models and migration scripts |
| Downstream | Phase 05 (Testing) | Provides table structure for data integrity and constraint test cases |
| Mandatory Ref | `skills/mysql-best-practices/` | Applied when MySQL or MariaDB is the target platform |

## Standards

- **IEEE 1016-2009 Sec 6.7** -- Data design viewpoint: entity definitions, relationships, constraints, and data dictionary
- **ISO/IEC 25010** -- Quality model for data integrity, performance efficiency, and reliability characteristics

## Resources

- `logic.prompt` -- Executable prompt containing the step-by-step database design generation logic.
- `README.md` -- Quick-start guide for this skill.
