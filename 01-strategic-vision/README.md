# Phase 01: Strategic Vision

## Purpose

This phase generates the strategic foundation documents that define project direction before detailed requirements engineering begins. It produces the business justification, product vision, and requirements overview.

## Sub-Skills

| Order | Skill | Output | Standard |
|-------|-------|--------|----------|
| 1 | 03-vision-statement | Vision_Statement.md | IEEE 29148 Sec 6.2 |
| 2 | 01-prd-generation | PRD.md | IEEE 29148, IEEE 1233 |
| 3 | 02-business-case | Business_Case.md | IEEE 1058 |

## Execution Order

Every product needs one digital marketing, social media and website strategy. The new-project command seeds its authoring brief. For existing products, extend an adequate website specification, commercial strategy or product strategy chapter. Register the authoritative Markdown document or multi-chapter manifest with YAML fields `document: product-market-strategy` and `strategy_status: draft`, and set `product_market_strategy: required` in the frontmatter of `_context/methodology.md`. Set the status to `reviewed` after inspecting the buyer proposition, channel decisions, website journey, measurement plan and evidence. Include it in the index and DOCX/PDF build map. The Phase 01 gate checks registration and review status; assess content and rendered outputs separately. Private platforms can specify internal adoption or partner distribution.

Run vision-statement first because it establishes the formal product and stakeholder direction. Run PRD next to convert that direction into scoped capabilities and quality expectations. Run business-case last so investment logic uses the current vision and PRD assumptions.

## Dependencies

- Upstream: Phase 00 (Meta-Initialization) establishes methodology and workspace targeting.
- Downstream: Phase 02 (Requirements Engineering) consumes the strategic outputs to derive formal requirements or Agile stories.

## Workspace Model

The canonical runtime workspace for this phase is `projects/<ProjectName>/`.

- Context source of truth: `projects/<ProjectName>/_context/`
- Generated artifacts: `projects/<ProjectName>/01-strategic-vision/...`

<!-- alias-block start -->
Existing skill-local references to `../project_context/` and `../output/` are compatibility aliases into the active project workspace, not a second architecture.
<!-- alias-block end -->
