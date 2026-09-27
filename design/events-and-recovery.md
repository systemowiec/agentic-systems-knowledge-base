# State, events, and recovery

> Use when: a task outlasts one request, may wait for a person, or performs external actions.
>
> Do not use when: a single call is short, has no side effects, and can safely be repeated.

## Decision

Persist the state needed to continue: work identifier, stage, results of completed steps, pending decision, and links to external calls. After a pause, resume the same operation if the runtime supports it. An event log helps reconstruct what happened, but **full event sourcing is not a prerequisite** for every agent system.

Design implication: before retrying a step with side effects, check whether its effect has already occurred. Use an idempotency key or another mechanism appropriate to the service. Treat diagnostic traces, domain history, and execution state as distinct data with distinct retention policies.

## Checks

- Test interruption after an external write, before a local write, and while awaiting approval.
- Distinguish `completed`, `failed`, `cancelled`, and `waiting` states.
- If you publish events, define their identifier, schema, version, and ordering requirements.
- Plan retries, timeouts, cancellation, compensation, or manual resolution of ambiguous effects.
- Set retention and data protection rules for the event log.

## Sources

- [OpenAI, Results and state](https://developers.openai.com/api/docs/guides/agents/results) — resuming an interrupted run with its state.
- [Temporal, Durable AI](https://docs.temporal.io/ai) — an implementation example of durable execution, approvals, and failure recovery; not the only architecture.
