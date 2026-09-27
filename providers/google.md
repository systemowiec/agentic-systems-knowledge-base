# Gemini API: Interactions and tool history

Scope: Gemini Interactions API and GenerateContent for compatibility with older integrations; configuration depends on the model.

> Use when: a project uses Gemini or migrates a GenerateContent integration to the Interactions API.
> Do not use when: you need only rules that are independent of Google.

## Decision

Google recommends the Interactions API for new projects; GenerateContent remains supported. The Interactions API can keep conversation history on the server through `previous_interaction_id` and stores interactions by default (`store=true`). `store=false` disables storage for continuation; in that mode, neither `previous_interaction_id` nor `background=true` can be used. A previous interaction ID carries history, but **does not** automatically carry `tools`, `system_instruction`, or `generation_config`; provide these again on the next turn. Interactions does not yet have feature parity: custom `safety_settings`, Batch API, and explicit caching remain in GenerateContent, among other features. The documentation does not yet support remote MCP for Gemini 3.

In GenerateContent, use `thinkingLevel` for Gemini 3 and `thinkingBudget` for Gemini 2.5; do not treat `budget_tokens` as a universal Gemini field. When manually replaying history, preserve the received `thoughtSignature`, especially for Gemini 3 function calling, where a missing signature can cause a validation error. The official SDK handles this automatically when you pass the full response object.

## Checks

- For function calls, preserve call IDs, part order, and exact matching between each call and its response.
- Do not drop fields needed for continuation when normalizing responses in a multi-provider layer. Choose `store` and the retention period according to data requirements; `store=false` does not automatically mean the provider performs no other processing or logging.
- Test model, tool, and API compatibility on representative cases; do not assume Gemini 2.5 and 3 behave identically.

## Sources

- [Google: Interactions API](https://ai.google.dev/gemini-api/docs/interactions-overview)
- [Google: Migrating to Interactions](https://ai.google.dev/gemini-api/docs/migrate-to-interactions)
- [Google: Gemini thinking](https://ai.google.dev/gemini-api/docs/generate-content/thinking)
- [Google: Thought signatures](https://ai.google.dev/gemini-api/docs/generate-content/thought-signatures)
