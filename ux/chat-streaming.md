# Chat, streaming, and interaction states

> Use when: a user watches an agent's response in real time or needs to approve its action.
> Do not use when: the application is only a batch API without an interactive interface.

Stream event semantics depend on the chosen API.

## Decision

Show the user **the task state**, not the model's raw internal loop: started, waiting for a tool, partial result, input or approval needed, completed, and failed. Text arriving in a stream may still change or end in an error. Mark the final answer and confirmed effect in the UI only after checking the operation's outcome against the runtime contract. Create an attempt record and idempotency key before an external action; a broken stream does not undo an effect that has already occurred.

Present approval as a specific proposed action with its object, effect, and scope. The interface must be able to resume an interrupted task without fabricating a new approval. For long operations, show progress based on real stages, not an invented percentage.

## Controls

- Handle cancellation, connection loss, resumption, and event redelivery without executing the action twice.
- Distinguish "agent planning" from "action completed" in the UI; a chat confirmation may be insufficient authorization.
- Support screen readers, focus management, and error states; do not convey meaning only through color or animation.
- Test with a slow tool, an interrupted stream, denied approval, and a partial response.

## Sources

- [OpenAI, Streaming API responses](https://developers.openai.com/api/docs/guides/streaming-responses) — example stream event semantics; other providers may define them differently.
- [OpenAI, Results and state](https://developers.openai.com/api/docs/guides/agents/results) — outcomes and resumption after interruption in the Agents SDK.
- [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) — interface accessibility requirements.
