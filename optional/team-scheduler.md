# Durable task scheduler for an agent team

> Use when: multiple workers handle dependent tasks and work must survive process failure or a long wait.
>
> Do not use when: a short synchronous delegation can safely finish in one call.

## Decision

Persist tasks, their states, execution owners, and results. Record dependencies explicitly when they affect ordering. If you model them as a DAG, reject cycles and start a task only when its required predecessors have completed. A blackboard or shared artifact store is one way to pass results, not a mandatory architecture component.

Design implication: a worker should **claim** a task for a limited time or use an equivalent queue mechanism. Lease expiry makes recovery possible but may cause re-execution. External side effects therefore need duplicate protection, while retries need limits, delays, and an escalation path.

## Checks

- Define unambiguous `ready`, `claimed`, `waiting`, `completed`, `failed`, and `cancelled` states, and audit transitions.
- Before writing to a shared resource, check ownership or version; resolve conflicts explicitly.
- Test failure before a claim, after a claim, after an external side effect, and before recording the result.
- Measure orphaned tasks, retries, backlog, and wait time.

## Sources

- [Temporal, Durable AI](https://docs.temporal.io/ai) — an example of durable execution and work recovery; it does not prescribe a particular scheduler.
- [Temporal, Worker performance](https://docs.temporal.io/develop/worker-performance) — queues and task polling by workers.
- [PostgreSQL, SELECT](https://www.postgresql.org/docs/current/sql-select.html) — `SKIP LOCKED` as a possible mechanism for a table-backed queue, not a default storage choice.
