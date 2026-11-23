# Coding Guidelines — Agent Addendum Template

## 1. Tool-Schema Discipline

Every tool wrapper validates inputs at the boundary.

```python
from agent_runtime.tools import tool, ToolResult, ReversibilityClass

@tool(
    name="email.send",
    reversibility=ReversibilityClass.IRREVERSIBLE,
    timeout_seconds=15,
    blast_radius_per_run=5,
)
def email_send(thread_id: str, body: str, recipient: str) -> ToolResult:
    # Schema is validated by the @tool decorator before this function is entered.
    return ToolResult(payload={"message_id": send(thread_id, body, recipient)})
```

Static check `ci/lint-tools.py` walks the AST and fails CI if any `@tool`-decorated function lacks `reversibility`, `timeout_seconds`, or `blast_radius_per_run`.

## 2. Irreversibility Annotations

- Code annotation: `ReversibilityClass.{IDEMPOTENT|COMPENSABLE|IRREVERSIBLE}`.
- Catalogue YAML: `reversibility_class: {idempotent|compensable|irreversible}`.
- Startup check: dispatcher cross-validates every code annotation against the YAML; mismatch fails startup and prevents the runtime from accepting requests.

## 3. Blast-Radius Caps

- Per-tool, per-run.
- Loaded from `Action_Catalogue_Spec.md` at run start.
- Enforced by the dispatcher; the planner is unaware.
- Cap exceeded → dispatcher returns `ToolResult.refused(reason="blast-radius-exceeded")`; the run continues with the refusal in the observation.

## 4. Deterministic State

State type:

```python
@dataclass(frozen=True)
class AgentRunState:
    plan: tuple[Step, ...]
    observations: tuple[Observation, ...]
    scratchpad: dict[str, Any]   # immutable view; copy-on-write
    cumulative_cost_usd: float
```

Mutation is replaced by transition application:

```python
def apply(state: AgentRunState, event: TransitionEvent) -> AgentRunState:
    # pure; no IO; no mutation
    ...
```

Tool wrappers return `ToolResult`; the orchestrator wraps the result in a `TransitionEvent` and calls `apply`. Replay = `reduce(apply, events, initial_state)`.

## 5. Idempotency Keys

```python
def idempotency_key(agent_run_id: str, step_index: int) -> str:
    return hashlib.sha256(f"{agent_run_id}:{step_index}".encode()).hexdigest()
```

- Passed to the underlying API call where supported.
- Retries reuse the same key.
- Lint check: any tool wrapper that calls an external SDK without passing the idempotency key (where the SDK supports it) fails CI.

## 6. Error & Timeout Policy

```python
class ToolError(Exception): ...
class RetryableToolError(ToolError): ...
class NonRetryableToolError(ToolError): ...
class SafetyToolError(ToolError): ...
```

- Timeouts: default from catalogue; raise `RetryableToolError` on timeout unless the call is documented non-idempotent.
- Backoff: `RetryableToolError` triggers retries at 1s, 4s, 16s with the same idempotency key.
- `NonRetryableToolError` fails the step; the orchestrator decides between re-plan and abstain.
- `SafetyToolError` (filter trip, kill-switch hit, schema fail at boundary) terminates the run; the audit log captures the cause.

## 7. Test Contract

Each tool wrapper requires these tests:

```python
def test_happy_path(): ...
def test_schema_fail_input_rejected(): ...
def test_timeout_raises_retryable(): ...
def test_non_retryable_error_propagates(): ...
def test_safety_error_terminates_run(): ...
```

Planner changes ship with `pytest -m agent_eval` run on the golden-task set for the affected feature.

Coverage gates: 90% on `agent_runtime/`; 100% on `agent_runtime/dispatcher.py`.

## 8. Static-Analysis & CI Hooks

| Check | Where | Failure mode |
|-------|-------|---------------|
| `lint-tools` | pre-commit, CI | missing decorator fields |
| `validate-catalogue` | CI, runtime startup | YAML/code mismatch |
| `idempotency-key-check` | CI | tool calls an SDK without passing the key |
| `state-mutation-check` | CI | tool wrappers mutate state directly |
| `agent-eval-gate` | CI on planner changes | golden-task regression > 2 pp |

## 9. Style Examples

### Good

```python
@tool(
    name="finance.ledger.entry.write",
    reversibility=ReversibilityClass.COMPENSABLE,
    compensating_tool="finance.ledger.entry.reverse",
    timeout_seconds=10,
    blast_radius_per_run=5000,
)
def ledger_entry_write(entry: LedgerEntry, idempotency_key: str) -> ToolResult:
    response = ledger_client.write(entry, idempotency_key=idempotency_key)
    return ToolResult(payload=response.to_dict())
```

### Bad

```python
def send_email(thread, body, to):                       # no decorator
    smtp.send(thread, body, to)                          # no idempotency, no timeout, no reversibility
    state.update({"last_sent": time.time()})             # mutates state in-place
```

## Filled work order · K3 idempotent ticket import

**SW-K3-01.** Fix duplicate status-history entries through the public ticket-import entry point. Accept event ID, ticket ID and requested status. Limit the implementation to import handling, transaction boundaries, compatibility with the existing ticket store and original test fixtures. Record impacted callers and the before and after revisions.

The implementation owner receives the public contract, existing callers, legacy record shape and retry rules. The independent software reviewer owns the acceptance cases and the expected results. The implementing assistant may add diagnostics but cannot weaken a held-back assertion.

| Input through the public importer | Expected observable result |
|---|---|
| E7, T1, review twice, identical payload | Same success outcome. One history entry |
| E8, T1, closed after E7 | A second distinct entry. Reject a fix that deduplicates by ticket ID alone |
| E7 repeated with a changed status | Conflict. No new entry |
| Failure after reserving E7 but before appending history, then retry | Exactly one complete event and history entry |
| Legacy ticket without saved event IDs, then E9 | Old history retained and one new entry |
| Two concurrent deliveries of E7 | One committed effect |

Reject a work order missing the retry or legacy invariant. Collect an original failure and a passing regression on separate tested revisions. D07 and E05 own implementation and revision-bound test evidence in their respective engines. C04 reconciles the producer receipts. At SRS stage these results are expected behavior, pending execution.
