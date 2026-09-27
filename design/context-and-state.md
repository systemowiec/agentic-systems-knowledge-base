# Model context, application state, and references

> Use when: a task involves multiple turns, long inputs, tools, history, or persistent memory.
> Do not use when: a one-off call needs no retained state; a simple input and output contract is enough.

The details of storing conversation history depend on the provider API.

## Decision

Separate three things: **model context** (what the model needs to know on this turn), **execution state** (identifiers, permissions, database client, operation progress), and **persistent knowledge** (facts, documents, and memory to retrieve later). Put only the data needed to resolve the task in the prompt. Secrets and runtime objects stay in code.

Choose a conversation continuation method explicitly: store and replay the history yourself, use SDK-managed state, or use a provider continuation identifier. Each method has different implications for privacy, durability, cost, and error reproduction. Do not mix full history replay with a server-side state identifier without checking API semantics; you may duplicate context by accident.

For large results, provide a short description and a reference to an artifact the agent can open on demand. There is no universal “5 KB” threshold: usefulness, token size, permissions, and ability to retrieve the data again should determine the choice.

## Checks

- Decide which history elements are needed for correct decisions and which may be retained. Test whether compaction or summarization loses constraints, decisions, or identifiers.
- On resumption, preserve the case identifier, approval state, contract version, and idempotency key for actions with side effects.
- Authorize artifact references when they are read, and give them their own lifecycle. Do not treat an opaque ID as a permission grant.
- Measure costs on real requests. A continuation identifier does not necessarily remove the cost of earlier context.

## Sources

- [OpenAI, Conversation state](https://developers.openai.com/api/docs/guides/conversation-state) — continuation methods and `previous_response_id` semantics.
- [OpenAI, Results and state](https://developers.openai.com/api/docs/guides/agents/results) — run state and resumption in the Agents SDK; provider-specific details.
- [OWASP GenAI Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) — memory and untrusted content as risk surfaces.
