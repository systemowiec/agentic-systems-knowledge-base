# Claude API: messages, tools, and thinking

Scope: Claude Messages API; thinking behavior depends on the selected model and API version.

> Use when: integrating the Claude API or moving conversation history and tool calls to it.
> Do not use when: the project does not use Anthropic or needs only a provider-neutral tool contract.

## Decision

The Messages API uses `user` and `assistant` messages; an instruction that applies from the start goes in the separate `system` field. Some newer models also accept `system` messages mid-conversation after a user turn. A final `assistant` message used as a **prefill** works on some older models, but Claude 4.6 and later, and Claude Mythos Preview, return `400 invalid_request_error`. For those models, end the request with a user message; use instructions or supported structured output to control the format.

Check thinking mode for the specific model. On Claude 4.6, manual `budget_tokens` is deprecated. Claude 4.7 and later reject `thinking: {type: "enabled"}` and use adaptive thinking, while 4.5 and earlier reject adaptive thinking. Mythos Preview is a separate exception that supports extended thinking. Thinking blocks and signatures carried through conversation history must retain their original form when the API requires it. On some new models, the signature is also tied to the preceding `system`, `tools`, and conversation history, so do not change that prefix when replaying a conversation. Do not normalize these blocks or Gemini thought signatures into plain text.

## Checks

- Keep tool calls and their results paired in the correct order; check the latest documentation before manually editing history.
- Do not assume `tool_choice: any` or forcing a specific tool works on every model: Claude Opus 5.5 and Fable 5.1, among others, reject these modes with a 400 error.
- For Claude 4.7 and later, and Mythos Preview, custom `temperature`, `top_p`, or `top_k` values also cause a 400 error. Remove those settings during migration when the model does not support them.
- Keep trusted runtime data, secrets, and permissions separate from model-visible content. The application remains responsible for tool authorization.
- When changing models, test prefill, thinking mode, limits, content format, and tool behavior on real scenarios.

## Sources

- [Anthropic: Create a Message](https://platform.claude.com/docs/en/api/messages/create)
- [Anthropic: Using the Messages API — prefill and system-message exceptions](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)
- [Anthropic: Claude API errors — model-specific errors](https://platform.claude.com/docs/en/api/errors)
- [Anthropic: Extended thinking and migration to adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
- [Anthropic: Thinking blocks and context](https://platform.claude.com/docs/en/build-with-claude/context-windows)
