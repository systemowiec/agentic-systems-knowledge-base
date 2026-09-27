# Background work, events, and persistent memory

> Use when: an agent wakes on a schedule, webhook, or queue; resumes a task; shares memory across runs; or writes instructions based on experience.
> Do not use when: a single task finishes in one call without persistent state or actions after the user receives a response.

Scope: agent systems with asynchronous work.

## Decision

Background execution **does not remove prompt injection risk**. An event, document, tool result, or memory entry can contain an attacker's instructions. Each trigger retains its own identity and trust level; do not turn it directly into the equivalent of an authorized user's message. Persistent instructions written by an agent require an approval process because they can carry an injection into future runs.

## Controls

- Authenticate or verify the origin of webhooks, queue messages, and requests from other agents. Accept typed events with an allowed schema and route them in code; treat descriptive text as data.
- Give each run an identifier, owner, delegated scope, expiry, and limits on cost and attempts. Before resumption, check that those permissions still apply.
- Design safe retries: event deduplication, idempotency keys for side effects, bounded attempts, a dead-letter queue, and a clear status. Do not automatically retry an operation with an unknown outcome until its state has been determined.
- Store memory and failure notes with provenance, date, and scope. Separate observations from instructions; promotion to a persistent rule requires validation appropriate to its risk.
- When an action needs a user's decision, pause the work in a pending state. Neither the model's judgment nor elapsed time substitutes for approval. Notify on actual outcomes, failures, or decisions needed.

## Sources

- [OWASP LLM01:2026 Prompt Injection](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM01_PromptInjection.md) — indirect and persistent injection through external sources and memory.
- [OWASP, Memory Is a Feature. It Is Also an Attack Surface](https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/) — persistent memory injection; 2026-05-13.
- [AWS Lambda, Best practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html) — duplicate events and idempotency.
- [OpenAI Agents SDK, Human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/) — safely resuming pending actions.
