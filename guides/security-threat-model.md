# Threat modeling an LLM and agent system

> Use when: designing data flow to a model or adding tools, memory, code execution, background actions, or access to multiple users' data.
> Skip when: you need a quick decision about one risk; start with the relevant short card in `security/`.

This guide is an analysis method, not a particular provider's specification. **Requirement** means an obligation imposed by the chosen protocol, contract, or adopted policy; **recommendation** is a starting point derived from the threats; **choice** requires a decision for the particular deployment.

## 1. Map flows and assets

List every input: a human user, API, webhook, queue, RAG document, web page, email, tool result, another agent, and memory. Trace each path from input through context assembly, the model, tool dispatcher, and executor to a database, file, message recipient, or external service. Add the return path: tool results, logs, and memory may enter future context.

For each edge, record **who initiated it**, how their identity was established, whose data flows through it, who controls the content, what credentials the process has, where data is stored, and what irreversible effect could occur. Identify assets: secrets, personal data, tenant data, funds, production configuration, and the integrity of persistent instructions. Do not assume that a model provider, runtime, or sandbox automatically supplies the isolation your system needs.

## 2. Check each trust boundary

1. **External data → model.** Recommendation: treat text, images, and tool results as data even when they look like system commands. Preserve their provenance in context, extract fields into a constrained schema, and test indirect prompt injection. This reduces risk but does not eliminate it. Do not automatically promote a RAG document or agent note to persistent instructions.
2. **Model → tool.** Critical recommendation: authorize each tool call against the verified initiator, scope, object, and arguments. Checking the model's response text does not replace this control. If you use protected HTTP MCP, its specification requires a token in every request and validation of the token audience; a `tenant_id` field in arguments alone is not authorization.
3. **Code execution → files, network, and secrets.** Recommendation: assume agent-run code can read anything available to its process. An environment variable in the same environment does not separate a secret from the shell. Isolate tasks and tenants; restrict mounts, egress, runtime, and resources. Perform privileged actions through a narrow tool or credential broker that enforces its own policy. Choice: VM, container, managed sandbox, and secret-delivery method depend on the threat model; test the actual configuration.
4. **Tenant A → tenant B.** Critical recommendation: bind tenant context to verified identity and current membership on the server. An ID in a request is a selector. Authorize the object on reads and writes; test databases, caches, search indexes, storage, queues, and logs. RLS or separate schemas are implementation choices, not by themselves proof of isolation.
5. **Intent → external effect.** Recommendation: assess risk by recipient, content, scale, cost, reversibility, and prior delegation. Pause a high-impact action for approval by an authorized person or an independent mechanism required by policy. Bind approval to the exact operation and resource state; protect server-side approval state against substitution and replay. Do not infer approval from "yes" in a document or model response. Choice: UI, CLI, or another authenticated channel.
6. **Retry → duplicate effect.** Recommendation: expect timeouts, duplicate messages, and resumption after failure. Before sending, paying, deleting, or changing data, use an idempotency key or equivalent deduplication at the executor. If the outcome is unknown, determine the first operation's state before trying again. A `dry-run` aids review but does not replace required approval.
7. **Trace → data leak.** Recommendation: record the initiator, policy decision, tool, operation ID, and outcome. Redact tokens, passwords, and sensitive data; limit access and retention. Full replay of input content is a choice with an additional privacy cost, not a universal requirement.

## 3. Tests before production

Test at least the following scenarios through real call paths, observing effects and logs:

- A document or tool response instructs the agent to send secret data out. Expected: no unauthorized read or egress.
- A user or model substitutes `tenant_id` and a resource ID. Expected: both read and write are denied.
- Agent-run code attempts to read process secrets, another task's files, and an internal network address. Expected: environment boundaries block access.
- Someone alters arguments after approval was displayed or replays the same approval. Expected: the altered or repeated operation does not execute.
- A task times out after a successful write and the queue redelivers its event. Expected: one effect and a determinable status.
- A malicious note enters memory. Expected: it does not become an instruction in later sessions.

Record the owner of each control, test evidence, and residual risk. If a control depends on an SDK, cloud service, or MCP version, record the version and check its documentation before deployment. If a test reveals a path to unauthorized effects, close that path instead of adding a warning to the prompt.

## Sources

- [OWASP Top 10 for LLM Applications 2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/README.md) — canonical sources for LLM01, LLM03, and LLM10; 2026 edition.
- [OWASP Multi Tenant Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html) and [Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) — isolation and per-request authorization.
- [MCP Authorization 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) — requirements for protected HTTP MCP.
- [OpenAI Sandbox security](https://developers.openai.com/api/docs/guides/agents-api/environments/security) and [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) — execution and secret isolation.
- [OpenAI Agents SDK: Human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/) and [AWS Lambda Best practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html) — approval and idempotency.
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) — log exclusions and retention.
