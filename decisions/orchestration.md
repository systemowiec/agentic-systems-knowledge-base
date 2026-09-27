# Choosing an orchestration pattern

> Use when: at least two model-driven processes work together on one task.
>
> Do not use when: one function or one agent handles the entire task.

## Decision

First decide **who owns the response to the user**. If a specialist takes over the conversation, use a handoff. If the specialist performs a bounded task and the coordinator composes the response, treat the specialist as a tool-like helper. In the OpenAI Agents SDK, these patterns are called `handoff` and `agent-as-tool`; names and mechanics may differ in other runtimes.

Sequential execution fits known dependencies, parallel execution fits independent tasks, and a coordinator fits tasks whose breakdown depends on the input. This is a **design inference**, not a mandatory structure for every multi-agent system.

[Multi-agent runtime](../guides/multi-agent-runtime.md) covers contracts, context transfer, and recovery in detail; open it when implementing the system.

## Checks

- Define routing conditions, the response owner, and the result format for each branch.
- Pass only the context the recipient needs; avoid copying the entire history by default.
- Use a validated data contract for results consumed by code.
- Test misrouting, missing responses, conflicting results, and cyclic handoffs.
- Enforce permissions and approvals at the action boundary, regardless of routing.

## Sources

- [OpenAI, Orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration) — handoffs and agents as tools.
- [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) — routing, parallelization, and orchestrator-worker patterns.
