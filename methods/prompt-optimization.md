# Prompt optimization

> Use when: a prompt or tool description fails to achieve the required result, or the model changes.
>
> Do not use when: the task, success criteria, and example data have not yet been defined.

## Decision

Establish a set of examples, metrics, and a baseline before changing the prompt. Change a small, clearly identified part of the instructions or tool set, then compare results on the same cases and on held-out validation data. Automated prompt generation is an option; generated text still needs review and testing.

Design implication: do not turn a single “lesson” from one failure into a universal rule. Fix a recurring problem where it originates: in the prompt, tool schema, input data, validation code, or UX.

## Checks

- Include typical cases, edge cases, and conflicting instructions.
- Keep a separate validation set to avoid fitting the prompt to development examples.
- Compare quality, cost, and latency; rerun the evaluation when changing models.
- Version the prompt and record why it changed and what the measurements showed.

## Sources

- [OpenAI, Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — objectives, datasets, metrics, and continuous evaluation.
- [OpenAI, Model optimization](https://developers.openai.com/api/docs/guides/model-optimization) — iterating on prompts based on measured results.
