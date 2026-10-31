# Experiment Validity and Platform Requirements

Parent skill: [05-saas-growth-experiment-doc](../SKILL.md). Load this reference when an experiment
doc must be defensible to a sceptical data scientist, when several teams share one experimentation
platform, or when the SRS must state requirements for the experimentation platform itself.

The parent skill states the hypothesis, metrics, sample, stop rule and decision rule. This file adds
what makes those statements trustworthy: intent classification, validity checks, concurrency rules,
long-term measurement, and verifiable platform requirements. It states WHAT the experiment and
platform must guarantee; the engineering build (assignment service, pipelines, statistics engine)
belongs to `ai/ai-feature-rollout-and-experimentation` in the engineering catalog engine (the successor of the retired `experiment-engineering` skill).

## 1. Classify the experiment intent first

Intent drives metric choice, sample size, duration and how much weight the result carries later.
Record exactly one intent in the doc header.

| Intent | Question it answers | Primary metric type | Typical duration | Result may justify |
|---|---|---|---|---|
| De-risk | Does this change break anything for a slice of users? | System and guardrail metrics (errors, latency, crash rate) | Days | Continuing the rollout; never a product-impact claim |
| Learn | Is this idea worth further investment? | Sensitive feature-level metric | 1-2 weeks, smaller allocation | A follow-up measure test; never a launch on its own |
| Measure (launch) | What is the effect on the metric we promised? | Pre-registered primary metric with power analysis | Full powered duration, whole weekly cycles | Ship / iterate / reject |
| Long-term | Does the effect persist, decay or reverse? | Retention, churn, revenue per user | Weeks to months (holdback) | Confirming or revising a shipped decision |

Decision rule: a Learn-intent result cited as launch evidence is a `[V&V-FAIL: intent mismatch]`.
Re-run as a Measure test with its own power analysis.

## 2. Metric set contract

Every Measure test declares:

- **One primary metric** that sits causally close to the change (feature-level), with its written
  link to a company-level metric. A company-level metric as primary is allowed only when the power
  analysis shows it can move within the planned duration.
- **Guardrails** in two tiers: product-wide guardrails the platform applies to every test (crash
  rate, payment failure rate, page or screen latency at P75/P95, unsubscribe or complaint rate) and
  test-specific guardrails. Each guardrail has a numeric degradation threshold and an action
  (alert, pause, abort).
- **Diagnostic metrics** that explain the mechanism; they never decide the outcome.
- **Product-experience invariants**: surfaces that must remain present and working in every
  variant (cart access, account access, payment entry, help). A variant that removes an invariant is
  invalid, not a losing arm.

Metric sensitivity checks before launch:

| Check | Pass condition | If it fails |
|---|---|---|
| Minimum detectable effect (MDE) | MDE at 80% power and the chosen alpha is at or below the smallest effect worth acting on | Choose a more sensitive metric, reduce variants, or extend duration before launch |
| Variance | High-variance metrics (revenue, time spent) have a pre-declared capping (winsorisation) threshold or covariate adjustment | Capping chosen after seeing results is `[V&V-FAIL: post-hoc analysis]` |
| Variant count | Sample per arm supports the MDE for every arm | Filter arms offline first (for ranking models) or cut arms |

Variance reduction (capping, stratification, pre-experiment covariate adjustment such as CUPED)
is legitimate only when declared in the analysis plan before launch and when the covariate data
predates exposure.

## 3. Validity checks the doc must schedule

| Check | When | Pass condition | Failure action |
|---|---|---|---|
| Variant QA (per variant, per platform) | Before launch | Each variant renders the intended change for named test accounts on every targeted device class; control shows no treatment | Block launch |
| Canary ramp | First hours of exposure, small allocation | System metrics, logging completeness and guardrails within threshold | Pause, fix, restart the clock |
| Sample ratio mismatch (SRM) | Daily and at analysis | Chi-square test of observed vs configured allocation not significant at the platform threshold (common practice: p < 0.0005 flags severe SRM) | Results are untrustworthy; diagnose assignment, redirects, bot filtering or logging loss; do not analyse effects |
| A/A health | After platform, logging, identity or metric-pipeline changes, and periodically | False-positive rate across A/A runs consistent with alpha | Freeze decisions on affected metrics |
| Interference / spillover | Design time | Randomisation unit matches the interaction unit (user, household, tenant, merchant, cluster of connected users) | Cluster-randomise or change the unit |
| Novelty and primacy | At analysis | Effect examined by exposure day or cohort; whole weekly cycles covered | Extend (pre-registered) or run a holdback |

## 4. Peeking and stopping rules

- Fixed-horizon tests are analysed once, at the pre-registered sample. Dashboards may show
  guardrail health during the run, but primary-metric significance is hidden or masked (variant
  labels anonymised) until the analysis date.
- Early stopping for success is allowed only with a pre-declared sequential method (group
  sequential boundaries or always-valid inference) named in the doc.
- Early stopping for harm is always allowed when a guardrail threshold is breached.
- Extending a test because it is "almost significant" inflates false positives unless the extension
  rule was pre-registered. Correct book-era advice that "running longer reduces false-positive
  risk" to: extension is valid only as a pre-declared rule or under a sequential method; otherwise
  replicate with a fresh, powered test.
- Borderline results (p close to alpha) or effects far above historical norms for similar changes
  trigger replication before launch when the change is costly to reverse.

## 5. Concurrent experiments

State for each test whether it runs isolated or overlapping.

| Condition | Choose | Wrong-choice failure |
|---|---|---|
| Change touches the same surface, layout region or ranking parameter as another live test | Same layer (mutually exclusive) | Variants collide visually or functionally; effects cannot be attributed |
| Revenue attribution or high-stakes launch needs precise effect | Isolated | Estimate contaminated by other tests |
| Independent surfaces, speed matters | Overlapping (different layers) | Needless queueing; teams peek and stop early to free traffic |

The doc names the layer or surface it occupies and lists live tests on the same journey.

## 6. Long-term impact

| Strategy | Use when | Cost to state in the doc |
|---|---|---|
| Single-feature holdback | One feature's lasting effect on retention or churn is disputed | Maintaining the old path; holdback users excluded from related tests |
| Cumulative holdback | A quarter's roadmap is evaluated as a whole | Frozen product for a small group; spillover ("feature envy") risk |
| Post-period analysis | Holdback is too expensive | Weaker causal claim; seasonality confounds |
| Proxy metric validated against history | Fast signal needed | Proxy must have documented correlation with the long-term metric |

Holdback requirements: exposure parity for all unrelated features, an owner, an end date, and a
rule for excluding holdback users from overlapping tests on the same journey.

## 7. Experimentation platform requirements (verifiable)

Use when the SRS covers a platform that product teams will run tests on. Adapt identifiers.

| ID | Requirement | Fit criterion / test oracle |
|---|---|---|
| EXP-FR-001 | The platform shall assign units to variants deterministically from a unit ID and experiment salt. | Re-requesting assignment for 10,000 fixed IDs returns identical variants in 100% of calls. |
| EXP-FR-002 | The platform shall reject launch of a Measure-intent experiment lacking hypothesis, primary metric, guardrails, power analysis, duration and decision rule. | Launch API returns a validation error naming each missing field. |
| EXP-FR-003 | The platform shall compute an SRM test daily for every running experiment and alert the owner when the p-value falls below the configured threshold. | Injected 52/48 split on a 50/50 test with 200,000 units raises an alert within one computation cycle. |
| EXP-FR-004 | The platform shall let an authorised tester preview any variant as a specified unit ID without assigning or affecting that unit. | Preview leaves the unit's assignment log unchanged. |
| EXP-FR-005 | The platform shall support a canary phase with configurable allocation and automatic pause on guardrail breach. | Simulated error-rate breach pauses exposure and notifies the owning team's on-call. |
| EXP-FR-006 | The platform shall enforce mutual exclusion between experiments tagged with the same layer. | No unit appears in two experiments of the same layer in assignment logs. |
| EXP-FR-007 | The platform shall mask variant labels on interim dashboards for fixed-horizon tests until the analysis date. | Dashboard shows "Arm 1 / Arm 2" before the date and real names after. |
| EXP-FR-008 | The platform shall display available traffic capacity per surface for the next 8 weeks. | Capacity view matches configured allocations within 1 percentage point. |
| EXP-NFR-001 | Assignment latency shall not exceed the agreed budget (for example P95 ≤ 20 ms server-side). | Load test report at peak traffic. |

Platform quality metrics (not vanity counts such as "tests launched"): share of tests meeting the
design standard, share aborted for misconfiguration, share inconclusive, restart rate, and median
setup time.

## 8. Worked example (original)

A Kampala marketplace tests showing the mobile-money fee before the confirm step on MTN MoMo and
Airtel Money checkout.

- Intent: Measure. Hypothesis: showing the fee earlier raises completed checkouts by at least 1.5
  percentage points because surprise at confirmation causes abandonment.
- Primary: checkout completion per checkout start (baseline 61%). Guardrails: payment-failure rate
  (abort if +0.5 pp), support tickets tagged "fee" (alert if +20%), checkout screen P95 load on
  low-end Android (abort if +300 ms). Invariant: cash-on-delivery option remains visible.
- Unit: buyer account, because one household often shares a phone but not an account; SRM checked
  daily at p < 0.0005.
- Power: 80%, alpha 0.05 two-sided, MDE 1.5 pp needs about 16,400 starts per arm; at 3,000 starts a
  day split across two arms that is 11 days, rounded up to 14 to cover two weekly cycles and month-end salary spikes.
- Layer: "checkout-UI"; the concurrent delivery-slot test runs in a different layer.
- Decision: ship if primary is significant and positive and no guardrail breaches; otherwise iterate
  on fee wording in a Learn test.

## Evidence/currentness

Access date 2026-09-24. Verified: SRM detection by chi-square with a strict threshold (commonly
p < 0.0005) — Microsoft Research, "Diagnosing Sample Ratio Mismatch in A/B Testing"; Fabijan et al.
(2019). Sequential-testing and CUPED method names are stable concepts (Deng et al. 2013).
NOT_ASSESSED: the organisation's actual platform thresholds, latency budgets and traffic volumes —
take them from project context.

Sources: Nassery (2025) *Next-Level A/B Testing*; Kohavi, Tang & Xu (2020) *Trustworthy Online
Controlled Experiments*; Fabijan et al. (2019) SRM taxonomy (KDD).
