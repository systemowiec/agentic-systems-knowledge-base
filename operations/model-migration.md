# Model migration without breaking the contract

Scope: changing the model, model family, API, or provider in a running application.

> Use when: you plan to replace a model or move to a new API variant.
> Do not use when: you are choosing the first model and have no existing behavior to preserve.

## Decision

Treat migration as a change in system behavior, not merely a change in model identifier. Record a baseline on real scenarios: answer correctness, tool selection, action outcomes, security, cost, latency, and failure behavior. Version the model, prompt, tool contracts, and conversation-state strategy together. Compare candidates on the same case set, including long context and interrupted runs.

When changing providers, check fields that do not map one-to-one. OpenAI has model-specific `reasoning.effort` values; Claude changes thinking modes across versions; Gemini distinguishes `thinkingLevel` from `thinkingBudget` and requires thought signatures to be preserved in certain flows. Moving from GenerateContent to the Interactions API also changes the state and retention strategy.

## Controls

- Before deployment, run evaluations representative of production, including negative security cases, correct tool calls, and model-specific constraints (for example, rejection of a final `assistant` prefill in Claude 4.6+ and restrictions on forced `tool_choice` or non-default sampling parameters in certain newer models).
- Roll out in stages; monitor differences and keep a straightforward rollback to the previous configuration and state data, provided the formats remain compatible.
- Check official migration notes, model availability, limits, and deprecations immediately before making the change. Dates and parameters in this knowledge base are a starting point, not a guarantee of future compatibility.

## Sources

- [OpenAI: Model optimization and evals](https://developers.openai.com/api/docs/guides/model-optimization)
- [OpenAI: Reasoning models](https://developers.openai.com/api/docs/guides/reasoning)
- [Anthropic: Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
- [Anthropic: Claude API errors and model-specific exceptions](https://platform.claude.com/docs/en/api/errors)
- [Anthropic: Using the Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
- [Google: Migrating to Interactions](https://ai.google.dev/gemini-api/docs/migrate-to-interactions)
- [Google: Thought signatures](https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures)
