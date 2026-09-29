# Book-driven Kaizen Wave 3: SRS application

Use this reference when improving requirements, architecture, API, testing, deployment,
governance, or agent-system capabilities. It is an independent synthesis of the 18-source
study recorded in the central ledger at `chwezi-dev-engine/docs/continuous-improvement/`.

Owning skill: [Kaizen owner](../SKILL.md).

## Transfer controls

- Treat requirements and API contracts as observable state machines: inputs, outputs,
  status/error semantics, invariants, idempotence, retries, timeouts, and ownership.
- Trace every material requirement to design, implementation, test evidence, operational
  signal, and rollback. Include failed paths, abuse cases, accessibility, and data quality.
- For agents, record source, success measure, safety boundary, steering/decision rights,
  switch or circuit breaker, and sharpening/review signals. Human approval remains explicit
  for consequential actions.
- Use small reversible experiments; retain baseline, hypothesis, guardrail, stop rule,
  acceptance evidence, residual risk, and re-audit date.

## Boundaries

Book examples do not establish current framework APIs, protocol standards, security controls,
or regulatory requirements. Do not copy exploit recipes, unsafe shell snippets, old HTTP
assumptions, or model/tool claims. Route current claims through Digital Research and label
missing evidence `NOT_ASSESSED`.

## Measures and routing

Measure trace-link coverage, failed-path test coverage, defect escape rate, requirement
rework, decision latency, rollback success, and unresolved evidence count. Apply to the
requirements-quality, API, test-strategy, deployment/monitoring, AI-evaluation, and governance
routes before standardising a change.

## Currentness gate

At task time verify volatile claims against current primary documentation (for example,
RFC 9110/9114, current framework documentation, OWASP guidance, and applicable standards),
record access date/freshness/support/uncertainty, and schedule review on change triggers.
