# A2A: communication between independent agents

Version scope: Agent2Agent `1.0.0`; `0.3` interfaces require separate handling.

> Use when: independent agent systems need to discover capabilities, delegate tasks, and exchange results across service or organizational boundaries.
> Do not use when: agents run in one runtime and a local invocation contract is sufficient.

## Decision

A2A describes **agent collaboration**, while MCP primarily exposes tools and context. An agent publishes an `AgentCard` with its capabilities, supported interfaces, and security requirements. The client selects a supported binding and version; the server handles messages, tasks, task states, and artifacts. Version `1.0` moved `protocolVersion` into the entries of `supportedInterfaces`. Do not copy `0.3` schemas into a `1.0` implementation.

A task may require additional authentication or a user decision (`TASK_STATE_AUTH_REQUIRED`). The task state **does not itself grant consent** to act. The implementation must define and verify the scope and validity of consent.

## Checks

- When an agent card declares authentication, verify it on every request and authorize the requested action under server policy. Public anonymous access is a separate decision about the scope of data and actions. Use encrypted transport in production.
- Limit what the public `AgentCard` reveals; expose sensitive details through an extended card after authentication.
- For webhooks and delivery retries, handle duplicates and verify the notification source.
- In `1.0`, the client sends `A2A-Version: 1.0` on every HTTP request (or the equivalent parameter); an absent version is interpreted as `0.3`. Test version compatibility, task states, streaming, errors, and cancellation. A2A does not replace application authorization policy.

## Sources

- [A2A 1.0.0 specification](https://a2a-protocol.org/v1.0.0/specification/)
- [What changed in A2A 1.0](https://a2a-protocol.org/latest/whats-new-v1/)
- [A2A 1.0 and its relationship to MCP](https://a2a-protocol.org/dev/blog/2026/03/12/a2a-protocol-ships-v10-production-ready-standard-for-agent-to-agent-communication/)
