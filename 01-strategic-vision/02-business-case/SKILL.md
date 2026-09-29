---
name: 02-business-case
description: "Use when decision-makers need a business case with ROI for a new system or ERP: costs, benefits, ROI, payback, NPV, risks, assumptions, sensitivity and a go/no-go call; use vision-statement for direction, lean-canvas for early hypotheses, and PRD generation after approval."
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---
# 02-Business-Case Skill
<!-- dual-compat-start -->
## Use When

- A sponsor must compare an investment option against the current state or credible alternatives.

## Do Not Use When

- Do not use as a product requirements document or to disguise missing cost evidence; unresolved commercial assumptions remain conditional.

## Required Inputs

| Artefact | Source or provider | Required? | Missing behaviour |
|---|---|---|---|
| Problem, options and sponsor decision | Approved context and sponsor | Required | Stop if the decision or comparator is unknown. |
| Cost, benefit and risk evidence | Finance owners, research and delivery estimates | Required | Qualify unavailable figures and show their effect on the recommendation. |

## Workflow

1. Read the named inputs and confirm their approval, version and unresolved decisions.
2. Apply the decision rules below before drafting; stop on a missing authority, unsafe assumption or unresolved scope driver.
3. Produce the Business Case and manifest through the existing domain procedure and load only the references needed for the chosen branch.
4. Trace each material statement in the Business Case and manifest to an input, decision or explicitly qualified assumption.
5. Verify the observable acceptance conditions, record unassessed checks, and hand the artefacts to their named consumers.
6. If validation fails, recover by correcting the source decision or artefact and rerun the affected check; do not weaken the acceptance condition.

## Outputs

| Artefact | Consumer | Observable acceptance condition |
|---|---|---|
| Business Case and manifest | Sponsor, finance reviewer and steering authority | The recommendation is reproducible from named assumptions, option comparison, sensitivity cases and explicit go/no-go criteria. |

## Evidence Produced

| Evidence | Consumer | Acceptance condition |
|---|---|---|
| Source and decision trace | Reviewer and downstream owner | Each material statement cites an approved input, named decision or qualified open issue. |
| Completed verification record | Release or phase gate owner | Every applicable check records pass/fail; unavailable checks remain `not assessed`. |

## Capability and permission boundaries

Read-only is the default for analysis, review, evaluation and planning. Read and search access to authorised project artefacts are required. Editing is limited to an explicitly requested project deliverable. Execution may run document, syntax or validation checks. Network access is used only for facts that require current verification. Do not publish, spend, change production, approve policy, or claim certification without explicit authority.

## Degraded mode

If any required capability is unavailable, return the narrowest useful qualified Business Case and manifest draft plus a gap register showing the missing item, affected sections, risk and owner. Never convert an unassessed check into a pass.

## Decision Rules

| Choice | Action | Failure or risk avoided |
|---|---|---|
| Benefits and costs have defensible ranges | Calculate scenarios and recommend | Recommendation rests on auditable evidence |
| A decision-critical input is unavailable | Issue a conditional case and block final approval | False precision drives investment |
| The investment includes an AI capability | Apply the AI business-case addendum: compare against an optimised non-AI option and cost evaluation, review, drift and model-change lines | AI return overstated against the wrong comparator |

## Quality Standards

- Preserve repository terminology and trace every material choice to project context.
- Use deterministic acceptance conditions; replace vague quality claims with an observable check, threshold or named approval.
- Cover error, empty, edge, recovery and operational cases relevant to this skill.
- Verify standards, citations, APIs and package names before relying on them; qualify what cannot be checked.
- Stop release for a failed safety, security, legal, financial, accessibility or data-integrity gate.

## Anti-Patterns

- Presenting one option as the only option. Fix: compare the current state and at least one credible alternative.
- Reporting a single ROI value from uncertain inputs. Fix: show base, downside and upside cases.
- Mixing sunk and future costs. Fix: label timing and decision relevance.
- Calling an unmeasured benefit strategic. Fix: define a proxy, owner and measurement date.
- Recommending go while a knockout risk is open. Fix: make the risk an explicit approval condition.

## References

- [SaaS business-case addendum](references/saas-business-case-addendum.md)
- [AI business-case addendum](references/ai-business-case-addendum.md): load when any option includes AI; adds the three-option comparator, AI cost lines, readiness scoring, kill criteria, and finance-engine routing.
- [Generation logic](logic.prompt)
<!-- dual-compat-end -->




> **SaaS mode:** if the project is a multi-tenant SaaS, apply `references/saas-business-case-addendum.md` in addition to the generic steps below.


## Overview

This is the third and final skill in Phase 01 (Strategic Vision). It consumes the Vision Statement and PRD produced by sibling skills to build a financial and strategic justification for the project. The Business Case provides decision-makers with quantitative data -- cost-benefit analysis, ROI projections, risk assessment, and measurable go/no-go criteria -- so they can make an informed investment decision before the project advances to Phase 02.

## When to Use

Run this skill after `01-prd-generation` has produced a PRD. It can also be executed standalone with only `vision.md` and `stakeholders.md` if the PRD is not yet available; in that mode the financial analysis will carry more "[COST-TBD]" flags, but the document structure remains valid.

## Quick Reference

| Attribute   | Value                                                                                 |
|-------------|---------------------------------------------------------------------------------------|
| **Inputs**  | `projects/<ProjectName>/_context/vision.md`, `projects/<ProjectName>/_context/stakeholders.md`, optionally `projects/<ProjectName>/<phase>/<document>/PRD.md`, `projects/<ProjectName>/<phase>/<document>/Vision_Statement.md` |
| **Output**  | `projects/<ProjectName>/<phase>/<document>/Business_Case.md`                                                          |
| **Tone**    | Executive, quantitative, decision-focused                                             |

## Input Files

| File                | Location                           | Required     | Purpose                                      |
|---------------------|------------------------------------|--------------|----------------------------------------------|
| `vision.md`         | `projects/<ProjectName>/_context/vision.md`     | **Required** | Primary source for problem domain and goals   |
| `stakeholders.md`   | `projects/<ProjectName>/_context/stakeholders.md` | **Required** | Identifies decision-makers and beneficiaries |
| `PRD.md`            | `projects/<ProjectName>/<phase>/<document>/PRD.md`                 | Recommended  | Enriches solution description and timeline    |
| `Vision_Statement.md` | `projects/<ProjectName>/<phase>/<document>/Vision_Statement.md`  | Optional     | Provides strategic alignment language         |

## Output Files

| File                | Location                       | Description                                    |
|---------------------|--------------------------------|------------------------------------------------|
| `Business_Case.md`  | `projects/<ProjectName>/<phase>/<document>/Business_Case.md`   | Complete business case with financial analysis |

## Core Instructions

1. **Read Context Files.** Read `vision.md` and `stakeholders.md`. Optionally read `PRD.md` and `Vision_Statement.md`. Log all file paths accessed. Halt execution if `vision.md` is missing.

2. **Generate Executive Summary.** Write one paragraph summarizing the business opportunity, the magnitude of investment required, and the expected return. Use active voice and executive tone.

3. **Generate Problem Statement.** Document the current state, pain points, and quantified impact of inaction. Extract data from `vision.md`. Where quantification data is unavailable, flag with `[IMPACT-TBD: Requires stakeholder input]`.

4. **Generate Proposed Solution.** Describe the high-level approach and list 3-5 key capabilities. Align each capability with a business goal from the vision. If `PRD.md` is available, summarize from it; otherwise derive from `vision.md`.

5. **Generate Cost-Benefit Analysis.** Produce three subsections -- Development Costs, Operational Costs, and Revenue/Savings Projections. Use LaTeX for Net Present Value:

   $$NPV = \sum_{t=0}^{n} \frac{CF_t}{(1+r)^t}$$

   Flag every unknown cost with `[COST-TBD]` and state assumptions explicitly.

6. **Generate ROI Projection.** Calculate return on investment:

   $$ROI = \frac{Net\ Benefits - Total\ Costs}{Total\ Costs} \times 100\%$$

   Include payback period:

   $$Payback = \frac{Total\ Investment}{Annual\ Net\ Benefit}$$

   State all assumptions.

7. **Generate Risk Assessment.** Construct a 3x3 probability-impact matrix (Low / Medium / High). List the top 5 risks, each with: Description, Probability, Impact, Mitigation Strategy, and Risk Owner. Do not fabricate probabilities; use qualitative assessment when data is unavailable.

8. **Generate Timeline and Milestones.** Align with the PRD release strategy if available. Include decision gates and review points.

9. **Generate Go/No-Go Criteria.** Define 3-5 measurable decision gates with specific thresholds (e.g., "Proceed if MVP demonstrates 80% feature completion within 110% of budget").

## Output Format

The generated `Business_Case.md` shall follow this template:

```markdown
# Business Case: [Project Name]

## 1. Executive Summary
[One paragraph: opportunity, investment, expected return]

## 2. Problem Statement
### 2.1 Current State
### 2.2 Pain Points
### 2.3 Cost of Inaction
<!-- Use [IMPACT-TBD] where data is unavailable -->

## 3. Proposed Solution
### 3.1 High-Level Approach
### 3.2 Key Capabilities
| # | Capability | Business Goal Alignment |
|---|------------|------------------------|

## 4. Cost-Benefit Analysis
### 4.1 Development Costs
### 4.2 Operational Costs
### 4.3 Revenue / Savings Projections
$$NPV = \sum_{t=0}^{n} \frac{CF_t}{(1+r)^t}$$
<!-- Flag unknowns with [COST-TBD] -->

## 5. ROI Projection
$$ROI = \frac{Net\ Benefits - Total\ Costs}{Total\ Costs} \times 100\%$$
$$Payback = \frac{Total\ Investment}{Annual\ Net\ Benefit}$$
### 5.1 Assumptions

## 6. Risk Assessment
### 6.1 Probability-Impact Matrix
|              | Low Impact | Medium Impact | High Impact |
|--------------|-----------|---------------|-------------|
| High Prob.   |           |               |             |
| Medium Prob. |           |               |             |
| Low Prob.    |           |               |             |

### 6.2 Top Risks
| # | Risk | Probability | Impact | Mitigation | Owner |
|---|------|-------------|--------|------------|-------|

## 7. Timeline and Milestones
| Milestone | Target Date | Decision Gate |
|-----------|-------------|---------------|

## 8. Go/No-Go Criteria
| # | Criterion | Threshold | Measurement Method |
|---|-----------|-----------|-------------------|

## 9. Approval
| Role | Name | Decision | Date |
|------|------|----------|------|
```

## Final Step: Write `manifest.md`

After generating all section files, create (or overwrite) `manifest.md` in this document's directory listing the section files in the correct assembly order:

```markdown
# Document Manifest — Business Case
# Generated by business-case. Edit to reorder or exclude sections before building.
01-executive-summary.md
02-problem-analysis.md
03-proposed-solution.md
04-cost-benefit.md
05-risks.md
```

This ensures `scripts/build-doc.sh` assembles sections in the intended order rather than alphabetical fallback.

## Common Pitfalls

- **Fabricating financial data.** Every figure must trace to a context file or carry a `[COST-TBD]` flag.
- **Missing risk mitigation.** Each identified risk must have a corresponding mitigation strategy and owner.
- **Vague go/no-go criteria.** Decision gates must include specific, measurable thresholds.
- **Ignoring cost of inaction.** Failing to quantify the consequences of not proceeding weakens the business justification.

### Royce Pilot Model Recommendation

Per Royce (1970) Step 3: "Do It Twice" — if this project is being developed for the first time, the Business Case should explicitly plan for a pilot/prototype phase. Royce's recommendation: for a 30-month project, schedule a 10-month pilot. The pilot is the entire development process done in miniature, to surface timing, storage, and interface unknowns before full development commits.

**Add to the Business Case document if applicable:**
- Section: Pilot/Proof of Concept Plan
  - Scope of pilot (which critical features/risks to model)
  - Pilot timeline (target: 25-33% of total project duration)
  - Pilot success criteria
  - How pilot learnings feed into full development planning
  - Cost of pilot vs. cost of discovery at testing phase

## Verification Checklist

- [ ] `Business_Case.md` exists in `projects/<ProjectName>/<phase>/<document>/`.
- [ ] All financial figures are flagged with a data source or `[COST-TBD]`.
- [ ] ROI and NPV formulas use LaTeX and are mathematically correct.
- [ ] Risk matrix covers at least 5 risks, each with a mitigation strategy.
- [ ] Go/no-go criteria are measurable with specific thresholds.
- [ ] Document traces to IEEE 1058-1998.

## Integration

| Direction   | Skill                         | Relationship                                    |
|-------------|-------------------------------|-------------------------------------------------|
| Upstream    | `01-prd-generation`           | Provides PRD with scope, features, and timeline |
| Upstream    | `03-vision-statement`         | Provides strategic alignment language            |
| Downstream  | Stakeholder review (external) | Business Case informs go/no-go decision          |

## Standards

- **IEEE 1058-1998** -- IEEE Standard for Software Project Management Plans
- **IEEE 29148-2018** -- Systems and software engineering -- Life cycle processes -- Requirements engineering

## Resources

- `logic.prompt` -- Executable prompt for this skill
- `README.md` -- Quick-start guide for this skill
