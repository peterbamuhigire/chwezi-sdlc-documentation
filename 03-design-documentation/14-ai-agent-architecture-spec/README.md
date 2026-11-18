## Objective

Produce the AI Agent Architecture Spec: runtime decomposition, loop and state machine, memory tiers, planner, dispatcher, supervisor (if multi-agent), durability and resumability, kill-switch wiring, and per-tenant isolation.

## Execution Steps

1. Verify `AI_Architecture_Spec.md`, `AI_Agent_Feature_PRD_Spec.md`, `Action_Catalogue_Spec.md`, `Multi_Tenancy_Architecture_Spec.md`, and tech-stack inputs exist.
2. Invoke `logic.prompt`.
3. In the [architecture template](references/ai-agent-architecture-spec-template.md), trace a source correction through memory and test a revoked reader in both a warm and a fresh session.
4. Review with the architect, AI lead, platform lead, and security lead. Promote ADR seeds via the agent ADR catalogue.

## Standards

- OWASP Top 10 for LLM Applications 2026 (published 2026-08-03; LLM01:2026-LLM10:2026 verified 2026-09-24 against the edition PDF at genai.owasp.org/resource/owasp-genai-llm-top-10-2026) and OWASP Top 10 for Agentic Applications 2026. Cite 2026 IDs; add the LLMxx:2025 ID only where an existing control set still uses it (2025-to-2026 map: `05-ai-red-team-test-plan/references/red-team-scenario-library.md`)
- NIST AI RMF
- ISO/IEC 42001
- AWS Well-Architected ML/AI Lens
