# Model Card: <feature> v<version>

- Date: YYYY-MM-DD
- Owner: <role / name>
- Status: { draft | published | superseded }
- Supersedes: <prior version, if any>

## 1. Purpose

- AI feature: <feature name>
- AI FR: <AI-FR-XXX>
- What it does: <one paragraph>
- Users: <personas>
- Decisions informed: <decision>
- Buyer outcome: <outcome>

## 2. Operational Pins

| Component | Pin |
|-----------|-----|
| Base model | <provider/model@version> |
| Prompt registry tag | <prompts/<feature>@vX.Y.Z> |
| Retrieval index version | <index@YYYY-MM-DD> |
| Gateway config tag | <gateway@vX.Y> |
| Content-filter version | <cf@vX.Y> |
| Eval suite tag | <eval/<feature>@vX.Y> |
| Post-processor version | <pp@vX.Y> |

## 3. Training and Grounding Data

### Base model (hosted)

- Provider disclosure: <link to provider's model card / data sheet>
- Provider knowledge cutoff: YYYY-MM
- Training-data exclusion verified: <evidence: contract clause, gateway endpoint, audit date>

### Retrieval data (if RAG)

- Sources: <Data-Source IDs from AI Data Spec>
- Volume: <documents / tokens>
- Languages: <list>
- Freshness: <interval>
- Exclusions: <PII redaction, banned doc patterns>

### Fine-tune data (if fine-tuned)

- Training set: <size, source, labelling provenance>
- Holdout set: <size>
- Class balance: <table>

## 4. Evaluation Metrics

| Metric | Value | Eval set | Date |
|--------|-------|----------|------|
| Golden pass rate | XX% | EVAL-XXX | YYYY-MM-DD |
| Factuality | 0.XX | EVAL-XXX | YYYY-MM-DD |
| Abstention precision | XX% | EVAL-XXX | YYYY-MM-DD |
| Citation rate (RAG) | XX% | EVAL-XXX | YYYY-MM-DD |
| Hallucination rate | X.X% | EVAL-XXX | YYYY-MM-DD |
| Judge-LLM score | 0.XX | EVAL-XXX | YYYY-MM-DD |
| Latency P95 | XXX ms | prod telemetry | YYYY-MM-DD |
| Cost / call | $0.0X | prod telemetry | YYYY-MM-DD |

## 5. Red-team Summary

| Category | Status | Open findings | Severity | Remediation date |
|----------|--------|-----------------|----------|--------------------|
| Prompt injection | pass / fail | n | low / med / high | YYYY-MM-DD |
| Jailbreak | | | | |
| Data exfiltration | | | | |
| Cross-tenant leak | | | | |
| PII surfacing | | | | |
| Hallucination probe | | | | |
| Bias surfacing | | | | |

## 6. Limitations

- Knowledge cutoff: <date>; queries about events after that fall back to <behaviour>.
- Languages evaluated: <list>. Unevaluated languages may degrade.
- Domain edges under-represented: <list>.
- Latency degrades when <condition>.

## 7. Bias Notes and Mitigations

| Dimension | Risk | Mitigation |
|-----------|------|------------|
| Gender | <risk> | <mitigation> |
| Race / ethnicity | | |
| Age | | |
| Disability | | |
| Geography | | |
| Language | | |

## 8. Intended Use

- <Business contexts where the feature is supported>.
- Pricing tiers exposed: <Starter / Pro / Business / Enterprise>.

## 9. Out-of-scope Use

- Medical advice: prohibited.
- Legal advice: prohibited.
- Investment advice: prohibited.
- Hiring / promotion / firing decisions: prohibited.
- Credit / lending / insurance underwriting: prohibited.
- Housing decisions: prohibited.
- Generation of content for protected-class judgements: prohibited.

## 10. Human Oversight

- Per-step approval required for: <list>.
- Contestability: <reroute / regenerate / escalate>.
- Audit log retention: <duration>.

## 11. EU AI Act Annex IV Cross-walk

| Annex IV item | Section |
|----------------|---------|
| General description | 1 |
| Elements and development process | 2, 3 |
| Data sets used | 3 |
| Validation and testing | 4, 5 |
| Risk management | 6, 7 |
| Human oversight | 10 |
| Changes through lifecycle | 13 |

## 12. Change Log

| Version | Date | Author | Summary | Linked ADR / eval delta |
|---------|------|--------|---------|--------------------------|
| v0.9 | YYYY-MM-DD | | initial | |
| v1.0 | YYYY-MM-DD | | GA | |

## 13. References

- AI Feature PRD Spec: <link>
- AI Architecture Spec: <link>
- AI Data Spec: <link>
- Eval report: <link>
- Red-team report: <link>
- Provider model card: <link>

## Example model card decision · FR-K1-01

Card MC-K1 refers to evaluation EVAL-01, labels tickets-v1, comparator rules-v1 and candidate-v1. These frozen predictions illustrate dispatch policy. The shift lead retains dispatch authority.

Under CAP-2 the candidate proposes five reviews for two slots. Reject this configuration. Under CAP-ALL its fixture penalty is 2 versus 11 for the rule. Defer rollout pending confirmed ownership, timing and representative outcome evidence. Record live uncertainty, subgroup size and label coverage before any broader claim.

For a retrieved answer under atlas-v2, record the retriever result and claim support separately. P2 revision 2 retrieved first can coexist with a failed answer. An uncalibrated judge cannot approve an unsupported answer or a failed permission check. See the [worked evaluation record](../../../05-testing-documentation/04-ai-eval-harness-spec/references/ai-evaluation-release-evidence.md).
