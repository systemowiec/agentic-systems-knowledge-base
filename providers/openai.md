# OpenAI API: choosing an API surface and managing state

Scope: OpenAI Responses API, Agents SDK, and Agents API; feature availability depends on the model and API version.

> Use when: a project uses OpenAI to call a model or tools, or to run an agent.
> Do not use when: you need provider-neutral guidance; start with the [provider boundary](../decisions/provider-boundary.md).

## Decision

Choose the API surface according to how much of the agent loop and state you need managed. The Responses API provides direct model and tool calls. The Agents SDK adds an agent loop, handoffs, tools, guardrails, and resumption of an interrupted run. The Agents API provides a managed harness with sessions and an execution environment. Their fields and strategies are **specific to OpenAI**, not a universal LLM schema.

In the Responses API, reasoning effort is set with `reasoning.effort`; supported values vary by model. Long-running requests can use `background` mode, which has its own temporary retention rules. For a broad tool catalog, use `tool_search`/`defer_loading` where supported (`tool_search` in the Responses API: GPT-5.4 and later), and compare task success, token use, and latency against loading tools directly. For external MCP servers, review what data is sent to the server and set an approval policy for sensitive actions.

## Checks

- Choose one consistent continuation strategy: replay local history, use a session, or use a server-side response ID. Do not send both a full history and an ID that already restores it.
- In the Agents SDK, an interrupted approval returns `interruptions` and state for resumption; do not assume the run has produced a final answer.
- Keep secrets out of prompts and reused agent definitions. Code in a sandbox can read environment variables available to it; if it must not access them, use a trusted server or proxy.
- Model rate limits apply at the organization and project levels, so rotating keys does not increase the allocation. Handle rate-limit headers, `Retry-After`, and work queues.

## Sources

- [OpenAI: Agents and available API surfaces](https://developers.openai.com/api/docs/guides/agents)
- [OpenAI: Reasoning models](https://developers.openai.com/api/docs/guides/reasoning)
- [OpenAI: Tool search](https://developers.openai.com/api/docs/guides/tools-tool-search)
- [OpenAI: Background mode and retention](https://developers.openai.com/api/docs/guides/background)
- [OpenAI: Results and state](https://developers.openai.com/api/docs/guides/agents/results)
- [OpenAI: MCP connections](https://developers.openai.com/api/docs/guides/agents-api/tools/mcp)
- [OpenAI: Rate limits](https://developers.openai.com/api/docs/guides/rate-limits)
