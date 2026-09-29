# Database Guidance

No database is shipped with Chwezi SDLC Documentation. Each skill may reference database types defined in `../project_context/tech_stack.md` (e.g., MySQL or PostgreSQL) purely for document generation. The scripts do not connect to those databases; they only use the context text to choose data type representations such as `DECIMAL(19,4)` for currency fields.
