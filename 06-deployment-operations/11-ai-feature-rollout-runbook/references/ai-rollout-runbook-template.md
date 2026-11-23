# AI Feature Rollout Runbook Template

## 1. Rollout Stages

| Stage | Audience | Default size | Bake duration | Exit gate |
|-------|----------|---------------|----------------|-----------|
| 1. Internal | staff workspaces | full company | 7 d | dogfood findings logged; 0 CRITICAL/HIGH |
| 2. Design partners | named cohort, opt-in | 3-8 workspaces | 14 d | qualitative sign-off; eval golden green |
| 3. Opt-in beta | workspace-admin opt-in, all tiers eligible | open opt-in | 14 d | SLO met; red-team smoke green |
| 4. Percentage cohort | 5% -> 25% -> 50% -> 100% | 5% start | 3 d per step | SLO met at each step |
| 5. GA | all eligible workspaces | -- | -- | trust-center + model card published |

## 2. Promotion Gates

Each transition requires ALL of:

- [ ] Eval harness golden green for the bake duration (no > 2 pp regression).
- [ ] Red-team smoke green; 0 CRITICAL and 0 HIGH open.
- [ ] Hallucination SLO met for the bake duration.
- [ ] Cost / call within ceiling at this cohort.
- [ ] Customer success qualitative sign-off (any partner can block).
- [ ] DPO sign-off if the stage exposes the feature in EEA or new regulated region.
- [ ] Rollback rehearsal: at least one successful rollback drill in the last 90 days.

## 3. Auto-Rollback Triggers

Wire these into the gateway / feature-flag system before stage 2:

| Trigger | Window | Action |
|---------|--------|--------|
| Citation accuracy drop > 5 pp | 24 h | revert prompt tag to last green |
| Factuality drop > 5 pp | 24 h | revert prompt tag; SEV2 |
| Safety violation event | any | pause feature; SEV1 |
| Unauthorised agent action emitted | any | pause feature; SEV1 |
| Cost > 200% of per-tenant ceiling for 1 h | 1 h | throttle then pause for that tenant; alert FinOps |
| Eval CI regression on candidate PR | per merge | block merge |
| Provider primary outage > 5 min | 5 min | route to fallback |

## 4. Comms Plan

| Stage | Channel | Artefact | Owner |
|-------|---------|----------|-------|
| Internal | #ai-launch + email | LRR doc, run-of-show | AI lead |
| Design partners | personal email | pre-rollout note, daily check-in | CSM |
| Opt-in beta | in-product modal + help article | privacy notice, opt-in modal | Product Marketing |
| Percentage cohort | status page, release notes | rolling status entry | RelMgr |
| GA | blog + customer email + sales enablement + trust-center | model card link, RAI declaration | Marketing + Trust |

## 5. Opt-in / Opt-out

| Region | Default | Override | Disclosure |
|--------|---------|----------|------------|
| US | on | workspace-admin off | first-use modal |
| Rest of world | on | workspace-admin off | first-use modal |
| EEA | off for high-risk; on for limited-risk | workspace-admin on | EU AI Act Art. 13 notice |
| Kenya / Nigeria / South Africa | on with consent | workspace-admin off | local DPA notice |

Consent capture: stored in tenant settings with timestamp and admin id. Re-prompt if EU AI Act tier or regulatory classification changes.

## 6. Post-Launch Monitoring Window

- 14 days heightened monitoring.
- Daily 15-min AI-quality stand-up: AI lead, SRE on-call, CSM rep, security on-call.
- Every flagged output reviewed within 24 h.
- Per-tenant cost dashboard reviewed daily for the first 14 d, then weekly.
- Hallucination SLO dashboard reviewed daily for the first 30 d.

## 7. Roles and Sign-off Ledger

| Sign-off | Role | Stage |
|----------|------|-------|
| Launch readiness | AI Lead | before stage 1 |
| Design-partner cohort | CSM | before stage 2 |
| Opt-in beta GA-readiness | Product, Eng, Security | before stage 3 |
| Percentage cohort step | SRE on-call | before each step |
| GA | CPO + CTO + DPO + CISO | before stage 5 |
| Post-launch close-out | AI Lead | after 30 d |

## Filled operator drill · K4 compatible bundle rollback

**OPS-K4-01.** The on-duty release operator owns restoration. The support lead owns user correction and replays a frozen eligible query after recovery. Record the release decision, timestamp, operation ID, component IDs and before/after response.

| Bundle | Code, feature schema and vocabulary | Base, tokenizer and adapter | Prompt and index |
|---|---|---|---|
| G1 accepted | code-1, schema-1, vocab-1 | base-1, tok-1, adapter-1 | prompt-1, index-1 |
| G2 candidate | code-2, schema-1, vocab-2 | base-2, tok-2, adapter-2 | prompt-2, index-2 |

Before serving, validate the entire candidate tuple. Reject adapter-2 on base-1 even if the schema name matches. If index promotion stops mid-update, leave G1 serving or restore the complete G1 tuple. Replay the same promotion ID only after reading its recorded state. The expected outcome is one logical transition, no partial bundle and the same eligible G1 response on replay. Record its identity and observed caller result before declaring recovery.

A change in input length with delayed labels calls for investigation. Keep task-quality impact unknown until outcome labels arrive. A difference between online and training transforms on the same frozen record establishes skew. Send a correction to the release operator, retain the failed tuple and decision receipt, and require a compatible re-promotion check. Engineering executes this drill and records observed results.
