# Database Guidance

No database is shipped with Chwezi SDLC Documentation. Each skill may reference database types (for example MySQL or PostgreSQL) defined in `projects/<ProjectName>/_context/tech_stack.md`, purely for document generation. Skill-local text may still write that path as the legacy alias `../project_context/tech_stack.md`. The scripts do not connect to those databases; they only use the context text to choose data type representations such as `DECIMAL(19,4)` for currency fields.
