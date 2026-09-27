# Identity, tenant isolation, and privacy

> Use when: an agent acts for a person or service, reads confidential data, or serves more than one tenant, user, or workspace.
> Do not use when: only public data is processed, with no identity or access to protected resources.

Scope: LLM applications, tools, and MCP servers.

## Decision

The model can propose an operation, but **the server establishes and enforces the initiator's identity and authority over the specific resource**. A `tenant_id` or object ID supplied in a prompt, tool argument, or header from an untrusted client is at most a selector; it does not prove access. A verified token or trusted gateway can convey tenant context, which the server checks against its own contract. Every read and write requires authorization even when the request comes from a trusted agent or background process.

## Controls

- Establish the verified initiator at entry and propagate its context through queues, handoffs, and tool calls. On resumption, check that delegation and membership still apply.
- Check authority for the **action and object** on every call; deny by default. Scope tool credentials to the required data and operations.
- For multiple tenants, derive tenant context from verified identity and current membership. Enforce isolation in databases, caches, files, indexes, queues, and logs; test cross-tenant reads and writes.
- For protected HTTP MCP, validate the token on every request, including its audience and required scope. Do not pass through an unverified token received by an MCP server. For STDIO, use an appropriate local-process trust model.
- Map data flows to the model, provider, tools, and observability systems. Apply data minimization, retention, and redaction. Local inference removes transfer to an external model provider only if the environment does not send that data through other channels.
- Log events needed for auditing, but do not log raw tokens, passwords, or sensitive user data.

## Sources

- [OWASP Multi Tenant Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html) — verified tenant context and isolation across layers.
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) — deny by default and check every request.
- [MCP Authorization, version 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) — HTTP scope, per-request tokens, and token audience.
- [MCP Security Best Practices, version 2026-07-28](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) — token passthrough and scope minimization.
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) — data to exclude from logs.
