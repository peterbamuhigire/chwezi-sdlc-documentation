# 04 - Database Design

## Objective

Generate a comprehensive database design document with ERD, normalized table definitions, indexing strategy, and a complete data dictionary per IEEE 1016-2009 Sec 6.7. When MySQL or MariaDB is selected, consult the engineering catalog's `mysql-engineering` skill and its `mysql-best-practices` reference for applicable implementation patterns.

## Execution Steps

1. **Read Inputs** -- Load `SRS_Draft.md`, `HLD.md`, `business_rules.md`, and `tech_stack.md`. Halt if any required file is missing.
2. **Design Schema** -- Extract entities, generate ERD (Mermaid erDiagram), verify normalization (1NF/2NF/3NF), and define table structures with typed columns and constraints.
3. **Define Relationships** -- Specify foreign keys with explicit cascade rules, indexing strategy, and referential integrity enforcement.
4. **Produce Outputs** -- Write `Database_Design.md` and `erd.mmd` to `projects/<ProjectName>/<phase>/<document>/`. Generate the data dictionary and migration strategy.

## Quality Reminders

- All tables SHALL be verified against 3NF; document any intentional denormalization with performance rationale.
- Monetary columns SHALL use `DECIMAL(19,4)` without exception.
- Every table SHALL include `id` (PK), `created_at`, and `updated_at` audit columns.
- Every foreign key SHALL have explicit ON DELETE and ON UPDATE cascade rules.
- Every FK column SHALL be indexed.

## Resources

- `SKILL.md` -- Full skill specification with core instructions and verification checklist.
- `logic.prompt` -- Executable prompt for the database design generation workflow.
