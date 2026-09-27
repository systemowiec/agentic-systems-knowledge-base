# Observability and evaluation

> Use when: model output affects users, tools, data, or a choice of architecture or model.
> Do not use when: writing only static documentation with no executing flow; this card becomes relevant before launch.

Provider evaluation tools change; the application should own its test cases.

## Decision

Evaluate the **task**, not just response style. Define ordinary, edge, and adverse cases; expected tool effects, sources, and stopping conditions. Calibrate automated grading against human judgment. Compare changes to prompts, models, retrieval, and architecture on the same cases. A newer model or an additional agent is not an improvement without better results or a justified cost benefit.

A trace should make it possible to reconstruct the input, instruction and model versions, source retrieval, tool choice, approval, result, and error. This does not mean storing full prompts and private data in every log. Telemetry schema, retention, and redaction should reflect debugging needs and privacy policy.

## Checks

- Measure task success, correct tool use, permission violations, source quality, latency, and cost separately.
- Include negative cases: missing source, prompt injection in a tool result, misrouting, interrupted response, and a repeated write action.
- Version test data, prompts, models, and graders. When model output varies, report the distribution rather than one score.
- Carry correlation identifiers and metadata in traces, and full content only when necessary and allowed.

## Sources

- [OpenAI, Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — task-based tests, human review, and change comparisons; does not require a particular Evals service.
- [OpenTelemetry, Trace semantic conventions](https://opentelemetry.io/docs/specs/semconv/general/trace/) — shared model of traces and correlation.
- [OpenTelemetry, GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/) — GenAI fields and their current status; check the version before implementation.
