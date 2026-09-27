# Agent contract

> Use when: an agent will be called by an application, user, or another agent.
>
> Do not use when: implementing a deterministic function with no independent model decisions.

## Decision

Define an agent by its task, allowed actions, input, output, and responsibility boundaries. Use a schema and validation for results consumed by code. Keep instructions, tools, policies, and contract versions somewhere reviewable and testable; Markdown is an option, not a runtime requirement.

Separate facts the model needs from data needed only by code. Caller identity, database clients, and secrets should stay in execution context; the model receives only data needed for the task. Context interfaces depend on the SDK.

## Checks

- Specify the response owner, termination condition, budgets, and behavior on error.
- Name the tools and explain when the agent may use them; instructions must not promise tools unavailable at runtime. Enforce authorization outside the prompt.
- Validate input and output, and version contract changes visible to consumers.
- Before finishing, check results against task criteria; also test missing data, invalid results, and unavailable tools.

## Sources

- [OpenAI, Agent definitions](https://developers.openai.com/api/docs/guides/agents/define-agents) — components of an agent definition, structured output, and separation of model history from runtime context.
- [OpenAI, Results and state](https://developers.openai.com/api/docs/guides/agents/results) — result, history, and continuation state as distinct contract surfaces.
