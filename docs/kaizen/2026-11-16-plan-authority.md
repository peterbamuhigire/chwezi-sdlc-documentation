# Resumable plan authority — 16 November 2026

The resumable-execution contract now distinguishes an owner's scope and acceptance
baseline from an executor's progress updates. A failed criterion cannot be weakened
to obtain completion. Changes require an impact decision and affected evidence
becomes stale. User/buyer/operator needs and actual feedback remain inputs to the
requirements owner. Independent scenario review found the route discoverable and
the existing domain/authority gates intact.

Codex defaults are `gpt-6.1-terra` with medium reasoning, replacing Luna at Peter's
request. An explicitly selected `gpt-6-astra`/high root is preserved. Equivalent
role TOML line endings pass; changed model/settings do not. The helper matches the
tested development-engine helper, and a disposable semantic-drift exercise passed.
Root documentation tests passed 33 cases with the engine-code coverage plugin
disabled for this root-only suite. The earlier default invocation ran the same
cases but failed its unrelated zero engine-coverage threshold; that attempt is
not counted as a successful default-coverage run. Engine-code coverage itself was
not remeasured by this documentation change.

Currentness review, 16 November: current official model pages and the active
runtime/account catalogue were checked before accepting the owner-selected pins.
Sources: [OpenAI release](https://openai.com/index/introducing-gpt-6-1-terra/),
[model specification](https://developers.openai.com/api/docs/models/gpt-6.1-terra),
[Anthropic release](https://www.anthropic.com/claude-fable-and-mythos-5-2).
Reading/review tasks supplied bounded task-fit evidence. Comparative local cost,
latency and quality gains and Claude account catalogue availability remain
NOT_ASSESSED. Claude model configuration, permissions and publishing controls
were retained. Existing sessions do not change model merely because files changed.

The managed runtime adds approved-sidecar drift checks, with separate regression
and propagation evidence recorded below. No new workflow manager was introduced;
real factory operation and customer acceptance remain NOT_ASSESSED.

Runtime 2.1.0 was applied using the community canonical managed updater. Its
canonical full suite passed 68 tests; all 21 managed files verify and a repeated
preview reports no pending changes. Project configuration and the setup plan are
preserved. The skill-engine validator passes with zero errors and five existing
report-only size warnings. The final diff passes whitespace checks. These are
local changes; no live factory, scheduler, application rollout or publication ran.
