# Agent with memory and an open-ended decision loop

> Use when: a task requires exploration, extended collaboration, or choosing the next step from changing context.
>
> Do not use when: the outcome and steps are known, and predictability, cost, and ease of audit matter more.

## Decision

CoALA describes memory, available actions, and the process of selecting actions. It can inform the design of an agent that uses observations and memory. It does not require tools named `think` and `recall`, a claim of “self-awareness,” or inferences about the user's emotions.

Design implication: treat these mechanisms as an **optional research pattern**. Memory needs provenance, access control, correction, and a deletion policy. A model's hypotheses about a user do not become facts without confirmation.

## Checks

- Distinguish observations, inferences, and durable records.
- Restrict external actions with permissions and side-effect controls.
- Compare quality with a simple agent that has no additional memory or reflection tools.
- Test false memories, stale data, and cases where the user has not consented to storage.

## Sources

- [Sumers et al., Cognitive Architectures for Language Agents (CoALA)](https://arxiv.org/abs/2309.02427) — a descriptive framework for memory, action spaces, and decision loops; it does not prescribe a tool set or personality traits.
