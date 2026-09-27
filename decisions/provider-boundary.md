# Boundary between an application and model providers

Scope: systems using one or more LLM providers.

> Use when: deciding whether and how to place a provider API behind an adapter or gateway.
> Do not use when: changing only a local prompt with no integration impact.

## Decision

Not every project needs a centralized gateway. Start with a simple boundary in code: the application contract covers what must actually be portable (task, result, errors, observability), while the provider adapter preserves provider-specific fields and state semantics. A separate gateway service is justified when shared limits, billing, policies, or multiple applications offset its operational cost.

Do not treat the Responses API as a common standard for OpenAI, Anthropic, and Gemini. OpenAI uses fields such as `reasoning.effort` in Responses; Claude has its own `thinking` and signed blocks; Gemini uses `thinkingLevel`/`thinkingBudget` and `thoughtSignature` in GenerateContent. Overly flat normalization loses features and can break continuation. Expose native features deliberately through the adapter instead of promising full model interchangeability.

## Checks

- Weigh adapter cost against portability benefits. Maintain compatibility tests for features you use, rather than assuming all models behave alike.
- Keep trusted identity and secrets out of model context. Authorize every tool at execution time.
- Define history format, retry behavior, limits, retention, tool handling, and errors for each provider. Do not work around organization limits by rotating keys.
- If you normalize the event stream, preserve the raw identifier, stage, metadata, and state needed for resumption and debugging.

## Sources

- [OpenAI: Reasoning models](https://developers.openai.com/api/docs/guides/reasoning)
- [OpenAI: Rate limits](https://developers.openai.com/api/docs/guides/rate-limits)
- [Anthropic: Create a Message](https://platform.claude.com/docs/en/api/messages/create)
- [Anthropic: Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
- [Google: Interactions API](https://ai.google.dev/gemini-api/docs/interactions-overview)
- [Google: Thought signatures](https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures)
