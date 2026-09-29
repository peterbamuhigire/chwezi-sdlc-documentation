# Opportunity Assessment and Product-Risk Evidence Gate

Parent skill: [PRD generation](../SKILL.md). Load this reference before Step 5
(Product Objectives) whenever a PRD is being written for a new product, a new
module, or a material change to an existing one. It decides whether the PRD may
be written at all and adds two mandatory PRD sections: the Opportunity Record
and the Product-Risk Evidence Register.

Upstream discovery practice (interviews, prototypes, assumption maps) lives in
the engineering catalog skill `product-business/product-discovery`. This
reference does not repeat it. It governs the handoff: what discovery must have
proven, in what form, before requirements are allowed to harden.

## 1. Why this gate exists

A PRD is a commitment of engineering money. Its most expensive failure is not
an ambiguous requirement; it is an unambiguous requirement for a product nobody
needed, nobody could operate, or the business could not sustain. A polished
document can hide that failure. This gate forces the evidence into view.

## 2. Opportunity Record (PRD section 2.0, before Market Context)

The Opportunity Record describes the problem, never the solution. If any row
names a screen, feature, model or technology, rewrite it or reject it.

| # | Field | What a complete answer contains | Blocking defect |
|---|---|---|---|
| O1 | Problem | One sentence naming the actor, the situation, and the measurable consequence today | A feature list presented as a problem |
| O2 | Who has it | Named segment with an observable qualifying attribute (role, volume, region, channel) | "SMEs", "users", "everyone" |
| O3 | Size | Bottom-up count: qualifying units x frequency x value per event, with source and date | A top-down market figure with no denominator |
| O4 | Success measure | Primary outcome metric, baseline, target, window, and the revenue or cost mechanism it moves | Output metrics (features shipped, screens built) |
| O5 | Current alternatives | What the segment does today, including manual work, spreadsheets, and doing nothing, with the cost of each | "No competitors" |
| O6 | Right to win | The specific asset (data, distribution, licence, integration, expertise) the client holds that a rival lacks | Generic quality or price claims |
| O7 | Timing | The change that makes this viable now (regulation, platform, cost curve, behaviour) with evidence | "The market is ready" |
| O8 | Route to buyer | How the product is sold, installed and paid for, and the requirements that route imposes | Omitted; it silently drives integration, onboarding and pricing requirements |
| O9 | Critical constraints | Non-negotiable conditions from channel, law, partner, or operating environment | Design choices disguised as constraints |
| O10 | Recommendation | Go, no-go, or discover-further, with the named decision owner and date | A recommendation with no owner |

Decision rules:

- O1 to O4 unanswered: do not write the PRD. Return a discovery brief listing
  the missing answers.
- O5 shows a free, adequate alternative the segment already uses: the value
  hypothesis must state the switching trigger and its evidence, or the
  recommendation is no-go.
- O8 routes through a partner, integrator, reseller or telco: add the partner's
  operating requirements (extensibility, white-labelling, settlement,
  support tiers) to the PRD constraint register.
- A sponsor mandates the product regardless of the assessment: write the PRD,
  but record the mandate, the assessment result, and the sponsor as risk owner.
  A mandate is a decision, not evidence.

## 3. Product-Risk Evidence Register (PRD section 5.1, before the Feature Priority Matrix)

Every material feature group carries four risks. Each needs evidence of stated
strength before the requirement it motivates can be baselined.

| Risk | Question the evidence must answer | Minimum admissible evidence | Typical owner |
|---|---|---|---|
| Value | Will the named segment choose and keep using this over its current alternative? | Behaviour, not opinion: prototype task choice, pre-commitment (letter of intent, deposit, pilot contract), repeat use in a pilot | Product lead |
| Usability | Can the named persona complete the core task unaided in its real environment? | Moderated test with at least five target users per primary persona on a realistic prototype; task completion and critical errors recorded | UX lead |
| Feasibility | Can this team build and operate it within the time, budget and technology available? | Spike or proof-of-concept against the riskiest integration, data volume, or model behaviour, with measured results | Engineering lead |
| Viability | Does it work for the whole business: unit economics, sales, support, legal, finance, partners? | Named sign-off from each affected function, and a unit-economics line that stays positive in the downside case | Sponsor |

The five-user figure is a planning convention for finding the most frequent
usability problems in one persona, not a statistical threshold. Increase it when
personas differ materially or when the task is safety- or money-critical.

### Evidence-strength ladder

Record the strongest rung reached for each risk. Rungs are ordered; a higher
rung supersedes lower ones only when it tests the same assumption.

| Rung | Evidence type | Admissible for |
|---|---|---|
| E0 | Stakeholder belief, AI-generated idea, analogy to another market | Nothing; marks the risk `UNTESTED` |
| E1 | Desk research, analyst data, competitor observation | Sizing (O3) and alternatives (O5) only |
| E2 | Interviews about past behaviour (not future intent) | Problem existence (O1, O2) |
| E3 | Prototype test with target users, spike with measured result | Usability and feasibility baseline |
| E4 | Commitment: signed pilot, deposit, paid pre-order, integration partner agreement | Value and viability baseline |
| E5 | Live behaviour in a limited release: retention, repeat use, unit cost observed | Promotion to general release |

### Register row format

```markdown
| Risk ID | Feature group | Risk | Assumption tested | Evidence (rung, source, date, n) | Result vs threshold | Status | If wrong, what breaks | Owner |
```

Status values: `RETIRED` (evidence meets threshold), `ACCEPTED` (owner accepts
the residual risk in writing), `OPEN` (evidence pending; requirement stays
`[DRAFT]`), `FAILED` (evidence contradicts; feature leaves scope or returns to
discovery).

### Gate rules

| Condition | Action | Failure avoided |
|---|---|---|
| Any Must-have feature has a risk at E0 | Mark the PRD `SPECULATIVE` and block baseline | Engineering builds a guess |
| Value risk `OPEN` for a Must-have | Requirement stays `[DRAFT]`; schedule a value test before sprint planning | Shipping a usable product nobody wants |
| Feasibility risk rests on an unproven integration (mobile money API, tax authority e-invoicing, bank feed) | Require a spike against the sandbox or a partner confirmation before committing a date | Date commitments on unknown third-party behaviour |
| Viability sign-off missing from finance, legal or support | Record `NOT_ASSESSED`; business-case go criteria cannot pass | A product the organisation cannot sell or support |
| Evidence is AI-generated synthesis with no primary observation | Treat as E0 | Fabricated research entering a baseline |

## 4. Assumption-break register

For every `ACCEPTED` or `OPEN` risk, state how the product fails if the
assumption is wrong, and choose a mitigation level proportionate to likelihood
times impact. Mitigation is graded, not binary: a written fallback procedure, a
manual override, a feature flag, a degraded mode, an automated recovery. The
choice of level is itself a requirement.

| Assumption | Likelihood (L/M/H) | Impact (L/M/H) | Observable failure | Mitigation level chosen | Requirement ID |
|---|---|---|---|---|---|

Apply the same proportionality to non-functional requirements. A scalability,
availability or throughput target must trace to observed or contracted demand.
A target with no demand evidence is over-specification: it raises build and
operating cost without a verifiable benefit. Mark it `[NFR-UNSUPPORTED]` and ask
for the demand source.

## 5. Decision frame and ranked product principles

Before prioritising, record the frame every trade-off is judged against:

1. The problem (O1) and the primary persona.
2. The goals, in strict rank order. Ties are not allowed. "Security first, then
   speed of task completion, then breadth of function" is a usable ranking;
   "all critical" is not.
3. Three to seven product principles: beliefs specific to this product that
   settle recurring disputes (for example, "a cashier's shift reconciliation
   must never depend on connectivity"). A principle that any product could
   claim ("must be reliable") or that is a design heuristic rather than a
   product belief is rejected.

Each Feature Priority Matrix rationale cites the goal rank or principle it
serves.

## 6. Single-customer demand screen

When a feature is requested by one prospect or funder as a condition of a deal:

- Restate the request as the underlying problem and test whether it recurs
  across the segment (O2). Evidence from one account is E2 at most.
- If it does not recur, route it to a configuration, extension point, or
  partner-delivered customisation rather than the core product.
- If it is accepted into the core, record the account, the commercial value,
  the maintenance cost over the support horizon, and what it displaces.

## 7. Minimal product rule

The PRD's committed release is the smallest scope that passed the value and
usability tests together. Once validated, removing a feature re-opens those
risks; a later scope cut requires re-test or a written acceptance from the
sponsor. When estimates overrun on validated scope, the default is a date
change, not a silent cut.

## 8. Worked example (original)

A Kampala savings and credit cooperative (SACCO) wants members to apply for
emergency loans by USSD and a mobile app.

- O1: Members wait a median of 4 working days for loans under UGX 500,000
  because applications need a branch visit; 31% of applications in the last two
  quarters were abandoned (branch register, Q1 to Q2 2026).
- Value risk: 42 of 60 members shown a clickable USSD prototype completed an
  application and 35 asked when it would go live (E3). The cooperative board
  signed a paid 3-branch pilot (E4). Status `RETIRED` for the pilot scope.
- Usability risk: 5 of 6 members over 55 failed the PIN-confirmation step on
  first attempt (E3). Status `OPEN`; requirement FR-LN-007 stays `[DRAFT]`
  until a revised flow reaches at least 5 of 6 unaided completions.
- Feasibility risk: disbursement depends on a mobile-money collections and
  disbursement API. The sandbox spike confirmed callbacks but not reversal
  behaviour. Status `OPEN`; if reversal fails silently, ledger and wallet
  diverge. Mitigation level: daily automated reconciliation plus a manual
  exception queue (FR-LN-021, FR-LN-022).
- Viability risk: finance sign-off obtained; the cooperative's compliance
  officer has not reviewed data-protection obligations. Recorded
  `NOT_ASSESSED`; route to `dpia-generator`.

## 9. Premium versus generic output

| Generic output | Premium output |
|---|---|
| "Users want faster loans" | Actor, baseline, abandonment rate, source and period |
| "Validated with stakeholders" | Rung, sample size, result against a pre-set threshold |
| Every risk marked low | Open risks named, with the requirement they hold in draft |
| Uniform 99.99% availability | Availability traced to branch operating hours and a contracted pilot volume |
| Feature list sorted by who asked loudest | Rationale cites a ranked goal or product principle |

## Evidence and currentness

- `NO_TIME_SENSITIVE_CLAIMS` for the procedure. The five-user usability figure
  is a planning convention and is labelled as such.
- Worked-example figures are illustrative and must be replaced with project
  evidence.
- Access date for this synthesis: 2026-09-24.

Sources: Cagan, M. (2008) *Inspired: How to Create Products Customers Love*;
Ximenes, F. (2024) *Strategic Software Engineering: Software Engineering Beyond
the Code*; engine synthesis with `product-business/product-discovery` and
`02-requirements-engineering/references/problem-goal-fixture.md`.
