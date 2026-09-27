# MCP: tools and context

Version scope: MCP `2026-07-28`; older clients may use an earlier revision.

> Use when: a host and server need to exchange tools, resources, or prompts through a standard protocol.
> Do not use when: a simple local function call meets the requirements without an interoperability layer.

## Decision

MCP defines how a host connects to a capability provider. It **does not mandate** hexagonal architecture, Python, PostgreSQL, a particular number of tools, or the absence of domain logic on the server. Tool names should be unique within one server; each tool has a description and an `inputSchema`. When combining servers, the client or proxy resolves name collisions, for example with prefixes. The tool list may change; `tools/list` supports pagination and caching. Results may contain text, structured data, images, audio, or resource links. For implementation details, use the [server design guide](../guides/mcp-server-design.md).

Revision `2026-07-28` has a stateless protocol core: no `initialize` or `Mcp-Session-Id`. **Application** state can still be maintained through explicit identifiers. Streamable HTTP is the standard remote transport. It requires `Mcp-Method` for requests and `Mcp-Name` for tool calls, resource reads, and prompt retrieval. The older HTTP+SSE transport is being phased out. Before implementation, check the revisions supported by each target host and SDK. `stdio` also works in an isolated service environment; it is not limited to desktop applications.

## Checks

- For a protected HTTP server, follow MCP authorization requirements: metadata discovery, a token for the correct resource, and server-side token validation. For `stdio`, secure the process environment; code running there can read its environment variables.
- Limit available tools according to the caller's identity and verify authorization at invocation time. Do not let a model-supplied `tenant_id` stand in for trusted identity.
- Treat descriptions, annotations, and results from another server as untrusted. Provide review or approval for sensitive actions according to risk.
- Sampling, roots, and logging in the core are deprecated in this revision. Tasks and MCP Apps are optional extensions that require support on both sides.

## Sources

- [MCP 2026-07-28 specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP 2026-07-28: Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [MCP 2026-07-28: Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)
- [MCP 2026-07-28 changes](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [OpenAI: MCP connections in a service environment](https://developers.openai.com/api/docs/guides/agents-api/tools/mcp)
