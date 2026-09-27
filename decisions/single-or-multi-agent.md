# One agent or several?

> Use when: considering specialist agents or splitting a task among agents.
>
> Do not use when: the issue is the order of fixed steps; consider an ordinary workflow first.

## Decision

Start with one agent with a clearly defined task. Add another when the contract changes: response ownership, tools, permissions, approval policy, model, result format, or evaluation method. Dividing a domain into team names alone does not justify additional agents.

Design implication: use multiple agents when specialization measurably improves quality or control. Every split adds routing, context transfer, and failure modes.

## Checks

- For each agent, document why it exists and identify one response owner for each path.
- Define the specialist's minimum input, result, and permissions.
- Evaluate misrouting, cyclic handoffs, cost, and latency on representative tasks.
- Simplify the architecture if the split does not improve results.

## Sources

- [OpenAI, Agent definitions](https://developers.openai.com/api/docs/guides/agents/define-agents) — a focused agent as a starting point and reasons to split one.
- [OpenAI, Orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration) — response ownership and the cost of splitting too early.
- [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) — add complexity after measuring its benefits.
