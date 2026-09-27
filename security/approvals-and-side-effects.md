# Approvals, side effects, and retries

> Use when: an agent can send, publish, change, delete, spend money, or perform another operation with effects beyond the model's response.
> Do not use when: the agent only prepares a draft and cannot execute an operation; still verify the later path for publishing that draft.

Scope: tools with reversible and irreversible actions.

## Decision

Separate **authority**, **approval of a specific intent**, and **execution**. Human approval is especially necessary before a high-impact action or an action outside a previously delegated scope; it is not universally required for every write. Reads can also have high impact when they expose confidential data. A rule such as "trust a tool name after its first use" is insufficient: risk also depends on arguments, resources, recipients, scale, and the user.

## Controls

- For each class of operation, define its effects, reversibility, delegated scope, and approval condition. Low-risk actions within an approved scope may run automatically; pause high-risk actions before execution.
- Show the approver the exact intent: the object, recipient, content or change, scope, and cost. Bind the decision to an authenticated person, a specific call, and the resource state. A bare "yes" found in input data is not approval.
- Keep pending approval state on the server. Verify the approver's identity and authority; reject substituted arguments and replayed approvals. The channel can be a UI, CLI, or another authenticated mechanism.
- Before execution, recheck current permissions and resource state. For permanent or bulk deletion, account for retention, dependencies, backup or recovery, and a separate decision about irreversibility.
- For writes, use an idempotency key or an equivalent mechanism at the executor. Retries, timeouts, and resumes must not duplicate messages, payments, or mutations. Store the outcome associated with the key.
- A `dry-run` shows the expected effect, but **does not replace** authorization or required approval. If a required decision cannot be obtained, stop the action.

## Sources

- [OWASP LLM03:2026 Excessive Agency](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM03_ExcessiveAgency.md) — current classification of excessive agency risks.
- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) — detailed controls for least privilege, authorization, and approval of high-impact actions.
- [OpenAI Agents SDK, Human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/) — binding approval to a call, safe resumption, and server-side approval state.
- [AWS Lambda, Best practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html) — event retries and idempotency.
