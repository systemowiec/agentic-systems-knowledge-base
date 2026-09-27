# First end-to-end slice

> Use when: building a new system or testing a risky architectural change.
>
> Do not use when: a small change can already be tested quickly through an existing production path.

## Decision

Build one working path from input to result first. Include the boundaries that carry risk in the project: model, tool, authorization, persistence, approval, or interface. Do not build every layer and every agent against mocks alone before testing a real integration.

Design implication: the aim is to detect a broken contract or flawed assumption quickly. Mock a dependency when it speeds learning, but run at least one test with a real integration before considering the architecture validated.

## Checks

- Define one successful case and one common failure.
- Check the user-visible result and the trace of calls and decisions.
- Measure quality, latency, and cost on a small set of representative inputs.
- Expand the system only after fixing the contract problems found.

## Sources

- [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) — start simply and measure before adding complexity.
- [OpenAI, Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — test behavior on data representative of the task.
