# Agent or workflow?

> Use when: choosing how to handle a task involving a model and tools.
>
> Do not use when: an ordinary function can solve the task without a model; start with code in that case.

## Decision

Choose a **code-defined workflow** when the steps and transition conditions are known. A model may perform an individual step, such as extraction or classification. Choose an **agent** when the required steps depend on intermediate results and cannot reasonably be specified in advance. This is an architectural choice, not a product label.

Design implication: start with the smallest solution that meets a measurable goal. Add autonomy only when tests on real cases show benefits that outweigh its additional cost, latency, and error risk.

## Checks

- Record which decisions are made by code and which by the model.
- Set a work budget, termination condition, and way to handle uncertainty.
- Test valid, incomplete, and conflicting inputs.
- Compare results with a simpler baseline on the same examples and metrics.

## Sources

- [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) — distinguishes code-directed workflows from agents that direct their own steps.
- [OpenAI, Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — evaluation scope for individual calls, workflows, and agents.
