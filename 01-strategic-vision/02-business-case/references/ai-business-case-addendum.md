# AI Business-Case Addendum

Parent skill: [Business case](../SKILL.md). Apply in addition to the generic
steps whenever the investment includes an AI capability (generation,
classification, extraction, retrieval, prediction, recommendation, or agent
action). The per-feature value hypothesis is produced by
[AI economic value brief](../../06-ai-economic-value-brief/SKILL.md); this
addendum turns one or more briefs into an investment decision a sponsor and a
finance reviewer can reproduce.

Finance and accounting treatment is not decided here. Route capitalisation,
scenario modelling and cost classification to the Chwezi Accounting Doctrine
engine (see Section 7).

## 1. Comparator set (replaces "current state vs proposal")

An AI business case compares at least three options, costed on the same basis
and horizon:

| Option | Definition | Why it is mandatory |
|---|---|---|
| A. Current state | The process as it runs today | Cost of inaction |
| B. Optimised non-AI | The best deterministic improvement: rules, templates, search, workflow redesign, staffing change | Many AI cases are really process cases; B often captures most of the value at lower risk |
| C. AI option(s) | One row per credible pattern (hosted model, self-hosted, classical ML, human-in-the-loop) | Forces the pattern choice to be justified economically |

Decision rule: option C is recommended only if its net benefit over option B,
not over option A, exceeds the required uplift agreed with the sponsor before
the numbers are run. Report both deltas.

## 2. Benefit logic

Each benefit line states mechanism, unit, volume, baseline, and evidence rung
(from the PRD's product-risk register):

```text
Annual benefit = affected volume x baseline cost or value per unit x expected change x adoption rate
```

- *Adoption rate* is a separate, evidenced variable. Accuracy without adoption
  earns nothing. Use pilot usage data where available; otherwise mark
  `[ADOPTION-ASSUMED]` and carry it into the downside case at no more than half
  the base value.
- Time saved counts as a benefit only when it converts into avoided hiring,
  redeployed capacity with a named use, or measurable throughput. Otherwise
  report it as a non-financial benefit.
- Quality benefits (fewer errors, fewer write-offs, faster collection) need a
  baseline error or loss rate from records, not estimates.

## 3. AI-specific cost lines

Omitting any line below is the most common way AI cases overstate return.

| Cost line | Driver | Note |
|---|---|---|
| Inference | Calls per task x tasks x price per unit, plus retries | Model on the downside case at a higher volume and a higher unit price |
| Retrieval and storage | Index size, refresh frequency, vector or search service | Grows with content, not users |
| Evaluation | Building and labelling the evaluation set; re-runs on each model or prompt change | Recurring, not one-off |
| Human review | Share of outputs reviewed x minutes per review x loaded staff cost | Often the largest line in regulated or financial workflows |
| Data preparation | Cleaning, labelling, consent and lawful-basis work | Front-loaded; frequently underestimated |
| Monitoring and drift | Dashboards, alerting, periodic re-evaluation | Operating cost for the life of the feature |
| Model change | Re-validation when a provider deprecates or changes a model | Plan at least one forced migration per year of horizon unless the provider commits otherwise in writing |
| Governance and compliance | DPIA, AI-specific documentation, audit support | Scale to the regulatory exposure recorded by the governance skills |
| Change management | Training, process redesign, communication, support uplift during rollout | See Section 5 |
| Exit | Cost to switch provider or revert to option B | Sets the real cost of lock-in |

Express the operating cost as **cost per successful task** so it can be
compared with the option-B unit cost.

## 4. Readiness scoring

Score each area 1 to 5 with named evidence. Any area at 1 or 2 becomes an
explicit approval condition with an owner and a date.

| Area | What a 4 or 5 requires |
|---|---|
| Data | Named owner; the required data exists, is accessible, and has a documented lawful basis; quality measured on a sample |
| Technology | Integration path proven by a spike; hosting and data-residency constraints resolved |
| Skills | Named people for evaluation, operation and review; gaps have a hiring or partner plan |
| Leadership | Sponsor has approved the uplift threshold and the kill criteria |
| Culture and process | Affected teams involved in the pilot; the changed workflow is documented |
| Governance | Accountability for AI decisions assigned; required assessments scheduled |

## 5. Change management as a costed plan

Budget and schedule four workstreams, each with an owner and a success
measure:

1. Process change: the redesigned workflow, including the manual fallback.
2. People: training, role changes, and reviewer staffing.
3. Function alignment: which business units' targets depend on the outcome.
4. Model operations: drift monitoring, re-evaluation cadence, and incident
   handling.

## 6. Go, no-go and kill criteria

Add to the generic Go/No-Go table:

| Criterion | Example threshold | Measurement |
|---|---|---|
| Uplift over option B | Net benefit per year at least 25% above option B in the base case | Pilot data and costed model |
| Evaluation pass | All acceptance slices at threshold on the frozen evaluation set | Evaluation report |
| Unit cost | Cost per successful task at or below the option-B unit cost within 2 quarters | Metering report |
| Adoption | At least 60% of eligible tasks routed through the AI path by pilot week 8 | Usage telemetry |
| Kill trigger | Two consecutive monthly reviews below the adoption or unit-cost threshold, or any serious incident | Steering review minutes |

Thresholds shown are illustrative; the sponsor sets them before the pilot.

## 7. Finance-engine consistency

Consult `chwezi-accounting-doctrine` (router `README.md`) and
record the gate run in the manifest:

- `09-budgeting-fpa-and-costing/scenario-and-sensitivity-modelling` for base,
  downside and upside cases and the sensitivity on adoption, unit price, and
  volume.
- `02-ifrs-core-standards/ifrs-intangible-assets-ias38` before presenting any
  development spend as capitalised. Discovery, prototyping and evaluation-set
  work usually sit in the research phase; the treatment is the finance
  engine's decision, not this document's. IFRS for SMEs reporters follow the
  finance engine's Section 18 guidance.
- `17-ai-automation-and-emerging/ai-in-finance-governance` when the AI touches
  finance processes.
- Use the NPV, ROI and payback formulas of the parent skill unchanged; the
  discount rate and currency basis (UGX, USD, or both with a stated rate
  source and date) come from the finance owner.

## 8. Worked example (original)

A Mbarara dairy cooperative wants AI to read handwritten milk-collection
slips (option C) instead of clerks keying them.

- Option A: 6 clerks, UGX 2.9 M per month loaded cost each, 2.1% keying error
  rate causing disputed farmer payments.
- Option B: tablets with a structured entry form at collection centres;
  estimated 2 clerks retained, error rate target 0.5%.
- Option C: slip photographs plus extraction, with human review of
  low-confidence fields; estimated 1 reviewer, error rate target 0.4%.
- Result: C beats A by a wide margin but beats B by less than the agreed
  uplift once review time, evaluation, and model-change costs are included.
  Recommendation: fund option B now; revisit C after 6 months of structured
  data exist, which would also serve as its evaluation set.

## Evidence and currentness

- `NO_TIME_SENSITIVE_CLAIMS` in the procedure; worked-example figures are
  illustrative only.
- Regulatory cost scaling depends on current AI Act and data-protection
  obligations; see the currentness note in
  `02-requirements-engineering/14-ai-feature-prd-spec/references/ai-eval-set-and-graduation-requirements.md`
  (checked 2026-09-24).
- Finance-engine skill paths verified to exist on 2026-09-24.

Sources: Marchiotto, A. (2025) *Adopting AI for Business Transformation*;
Cagan, M. (2008) *Inspired: How to Create Products Customers Love*; engine
synthesis with the parent skill and the Chwezi Accounting Doctrine router.
