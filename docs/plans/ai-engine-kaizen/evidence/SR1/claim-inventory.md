# SR1 claim inventory and front-door baseline

As of: 2026-11-23  
Accountable owner: Peter  
Execution role: SDLC specification author  
Observed README baseline: `0fe8d74bbad170cfa9d0efca510af9ef5c7f6924` (2026-11-19)  
Integrated checkout inspected: `65d3f6fd587f96e411e6e18b10889c3661f6f1b3`  
Source revision for the four implementation packets: see the revision column below.  
Environment: Windows checkout; content and fixture walkthrough evidence only. No production AI service, hosted model, public importer, or customer corpus was exercised.

## Proposed AI capability claims

“Fixture-tested” means the documented behavior was checked against the frozen synthetic cases and an independent task walkthrough is recorded. It does not mean an implementation or production service was tested. No AI capability below is classified as live-tested.

| Capability claim for the README journey | Owner and entry point | Revision and result | Environment and limit | Classification |
|---|---|---|---|---|
| Turn an AI feature request into a measurable decision with named inputs, deadline, label owner and fallback. | Accountable artifact owner: Peter. Entry: [AI-feature PRD addendum](../../../../../02-requirements-engineering/14-ai-feature-prd-spec/references/ai-feature-prd-addendum.md). Product decision owner remains project-specific. | Packet revision `22421ba7c10d9f9f19ae33b567d99c6f14a7e6a5`; [AC-S01 walkthrough](../S01/independent-review.md) recomputed K1 and confirmed deadline/label-owner omissions stay open. | Frozen K1 arithmetic and document walkthrough. No model predictions, live triage, stakeholder approval or rollout target. | Fixture-tested |
| Specify dataset/corpus ownership, eligibility, grouping, time cutoffs, leakage controls and withdrawal behavior. | Accountable artifact owner: Peter. Entry: [AI data and knowledge-base template](../../../../../02-requirements-engineering/15-ai-data-and-knowledge-base-spec/references/ai-data-and-knowledge-base-spec-template.md). Corpus and rights owners remain project-specific. | Packet revision `47187e3edb31b71d89739b0486f1e5e97972c458`; [AC-S02 walkthrough](../S02/independent-review.md) reproduced partition membership and K2 withdrawn-document handling. | Seven synthetic rows and synthetic Atlas corpus only. No real corpus was indexed or permission checked. | Fixture-tested |
| Join a policy-specific evaluation to a model card and a release decision. | Accountable artifact owner: Peter. Entries: [AI evaluation release evidence](../../../../../05-testing-documentation/04-ai-eval-harness-spec/references/ai-evaluation-release-evidence.md) and [AI model card template](../../../../../03-design-documentation/12-ai-model-card/references/ai-model-card-template.md). Evaluation and release approvers remain project-specific. | Evaluation/handoff revision `e1d764be0332b95670728ad3d8e28b029634660b`; model-card revision `2b855d4f2e0874dc4f9d670d3c9bdf4e1b57230a`; [AC-S03 walkthrough](../S03/independent-review.md) recomputed K1 metrics and checked K2 retrieval versus answer support. | Frozen cases and exact arithmetic. No model was trained, hosted, or graded live; no release was approved. | Fixture-tested |
| Give an AI-assisted software change an independent oracle and give an AI release a compatible rollback and operator path. | Accountable artifact owner: Peter. Entries: [coding-guidelines addendum](../../../../../04-development-artifacts/05-ai-agent-coding-guidelines-addendum/references/ai-agent-coding-guidelines-addendum-template.md) and [AI rollout runbook](../../../../../06-deployment-operations/11-ai-feature-rollout-runbook/references/ai-rollout-runbook-template.md). Implementer and operating owners remain project-specific. | Packet revision `d56eefac9899ceba9623b826211ebcaf99451886`; [AC-S04 walkthrough](../S04/independent-review.md) checked the K3 public entry point, retry, conflict, legacy-row and interrupted-write cases and the K4 compatible bundle rollback. | Synthetic work order and bundle walkthrough only. No public importer implementation, deployment, production rollback or operator acceptance. | Fixture-tested |
| Hand off the four synthetic cases through linked requirement, data, evaluation and operating-decision records. | Accountable artifact owner: Peter. Entry: [S05 handoff manifest](../S05/handoff.json) and [acceptance walkthrough](../S05/independent-review.md). | Handoff `e1d764be0332b95670728ad3d8e28b029634660b`; four assertions passed. The recorded focused pytest invocation also hit the repository-wide coverage threshold because it exercised no engine module. | Read-only fresh-reader walkthrough and focused fixture test; no production behavior or user acceptance. | Fixture-tested |

No AI capability is marked generally available or live-tested. A live model service, trained-model quality, hosted behavior, customer-data permission, production rollout and stakeholder acceptance are deferred from README capability claims until they have an owner, entry point and environment-specific evidence. The packet does not establish that those capabilities exist.

## Existing README front door to preserve

The baseline README title is `Chwezi SDLC Documentation`. Its existing first-screen claims describe a 160-skill software lifecycle documentation library, a Python validation kernel, document generation, and intended audiences and use. These are existing claims, not newly verified by this SR1 inventory.

### Navigation and anchors

- The contents list names 13 destinations: Capabilities; Find the right skill; How it works; What is inside; Standards it follows; Requirements; Installation; Project workspaces, gates and document builds; Validation; Quality and improvement; What the October 2026 kaizen improved; References; Contributing and licence.
- Named compatibility-sensitive headings include `Capabilities`, `Find the right skill`, `How it works`, `Standards it follows`, `Requirements`, `Installation`, `Validation`, `Quality and improvement`, `What the October 2026 kaizen improved`, and `Contributing and licence`.
- Existing README-inbound references and the README-preservation result must be rechecked against the baseline before a rewrite. The prior October record reports one inbound README anchor at that cycle; it is historical evidence, not a current count.
- The current README links to the skill catalogue, reference index, installation guidance, standards and sources, validation materials, project workflow, hybrid and regulated models, and the unattended runner. Local destinations must resolve at the release check.

### Commands and install paths

The front door currently documents: `git clone`, `cd`, `python3 -m pip install -c requirements-ci.txt -e ".[dev,docs]"`, `python3 -X utf8 scripts/validate_engine.py`, `python3 -m engine new-project Acme --methodology waterfall --domain healthcare`, and `python3 -m engine validate projects/Acme`. The README qualifies that a fresh workspace has 22 blocking findings. Other installation and manual-route commands appear later in the page. SR3 owns disposable-checkout command replay; SR1 does not claim those commands were executed in this environment.

Install routes to preserve include the Python package/kernel setup, skill-only loading for Claude Code or Codex, `install.sh`, `install.ps1`, project/user scope and the unattended runner route under `auto-agents/`. Platform-specific limitations from the old README remain dated and must not be promoted to current results without rerunning.

### Historic non-AI capability map

Keep resolvable destinations for these broader lifecycle uses while adding the AI journey:

- Strategy and requirements: PRDs, business cases, stakeholder analysis, requirements analysis, Waterfall SRS, Agile stories and traceability. Start points include `01-strategic-vision/`, `02-requirements-engineering/` and [the skill catalogue](../../../../skill-catalogue.md).
- Design and implementation documentation: architecture, API, database, development artifacts and coding guidance under `03-design-documentation/` and `04-development-artifacts/`.
- Testing and release: test strategy/report, deployment and operations under `05-testing-documentation/` and `06-deployment-operations/`.
- Agile, end-user, governance and compliance: `07-agile-artifacts/`, `08-end-user-documentation/` and `09-governance-compliance/`.
- Sector-specific work: the 11 domain packs under `domains/`, with the corresponding index or catalogue destination.
- Workspace creation, phase gates, hybrid projects, regulated evidence, document builds, validation, installation and the Jidoka unattended runner.
- Games and other specialist routes currently called out in the README and skill catalogue; the README warns about a known routing-proxy near miss for the unqualified phrase “software requirements specification.”

The exact workflow-to-skill catalogue is [docs/skill-catalogue.md](../../../../skill-catalogue.md); SR2 must select working non-AI examples from it and keep these lifecycle destinations available.

### Licence and history

`LICENSE` declares MIT and copyright `2026 Peter Bamuhigire`. Keep the contributing/licence route and link to the actual license. The README includes dated validation results, routing-proxy results, kaizen score history, known limitations, and a long October 2026 improvement history. New text must not make historical results look current. Preserve the existing detailed improvement destination or provide an intentional resolvable replacement.

## Currentness and model check

Official OpenAI pages checked on 2026-11-23:

- [Model release notes](https://help.openai.com/en/articles/9624314-model-release-notes) list GPT-6.2 Astra and GPT-6.2 Sol for the API on 2026-11-17.
- [ChatGPT Work and Codex availability](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex) says the model selector can expose GPT-6.2 Astra/Sol depending on plan, seat and workspace settings; CLI support is stated as requiring Codex 0.166.0 or later.
- [OpenAI API model catalogue](https://developers.openai.com/api/docs/models) describes GPT-6.2 Astra and Sol and provides API-level model IDs and prices. Those API prices do not establish subscription cost or cost for this run.

Currentness record: R13 in `sources.json` supports the dated API release claim (publication 2026-11-17; accessed and verified 2026-11-23; context-bound; review 2026-11-30; verified within the release-note scope; it does not establish account access). R14 supports provider-described task fit and API pricing (publication 2026-11-17; accessed and verified 2026-11-23; context-bound; review 2026-11-30; provider claims only). The Work/Codex page was accessed 2026-11-23 and reported an update three hours before access; exact publication time was not exposed. Its plan/seat/workspace scope is verified for platform eligibility, with account-specific availability still unknown. Recheck after any model release, account or workspace setting change and before a README claim names model availability or policy. Review owner: execution lead; policy decision owner: Peter.

Disposition: the release check found GPT-6.2 Astra/Sol after the repository's 17 November Codex policy note. The user-level model policy says to prefer Sol 6.2/medium when exposed, with Terra 6.1/medium as fallback; no change is proposed. The actual active account/runtime catalogue and selected-model identifier are not exposed to this evidence process, so availability on this exact session is `NOT_ASSESSED`. No task-specific cost, latency or quality comparison was run. A full model-policy decision remains open for a separately authorized currentness review; this README slice does not claim model policy currentness passed.

## Acceptance and remaining review boundary

The five capability rows above have accountable artifact ownership, real tracked entry points, packet revisions, a result, environment and explicit limits. Evidence class is fixture-tested in every case. Their project-level product, corpus, evaluation, implementation, operations and release owners are not named by the synthetic packet and must not be inferred from Peter's artifact accountability.

The README itself remains unchanged at the inspected revision. This record is an inventory for SR1, not stakeholder/user acceptance of the proposed README. SR2 must draft from this matrix and preserve the named non-AI destinations. SR3 must perform the preservation, link/anchor, command and independent-reader checks against the old README revision before any release claim.
