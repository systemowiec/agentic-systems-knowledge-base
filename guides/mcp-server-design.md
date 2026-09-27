# Designing an MCP server

Scope: MCP `2026-07-28`, with compatibility checks for revisions `2025-03-26`–`2025-11-25` and `2024-11-05`.

> Use when: implementing an MCP server, publishing its tools, or connecting it to multiple hosts.
> Do not use when: deciding only whether MCP is needed; start with the [short card](../protocols/mcp.md).

In this guide, a **specification requirement** is a `MUST` rule for the stated revision and feature. A **project decision** is an architectural choice that must be justified by requirements, rather than presented as a protocol obligation.

## 1. Identify the hosts and protocol revision

List the target hosts, their SDKs, supported MCP revisions, transports, and authorization methods. Revision `2026-07-28` has neither `initialize` nor protocol sessions: every request carries the version, client information, and capabilities in `_meta`; the server **must** implement `server/discover`. Do not assume that a new SDK release selects the new protocol revision by default. For example, the TypeScript SDK v2 client defaults to the older `initialize` flow; `auto` mode and pinning to `2026-07-28` require explicit configuration. Test the exact combinations you plan to use. [MCP versioning](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning), [TypeScript SDK](https://ts.sdk.modelcontextprotocol.io/v2/protocol-versions).

## 2. Build the smallest vertical slice

Implement `server/discover`, then one safe read through `tools/list` and `tools/call`. Give the tool a short name, a specific purpose, and a valid JSON Schema `inputSchema`; for a call without parameters, use, for example, `{"type":"object","additionalProperties":false}`. Declare the `tools` capability and answer `tools/list` even when the list is empty. The server **must** validate input, enforce access, rate-limit calls, and sanitize results. Framework, language, tool count, and layer boundaries are project decisions. [Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools).

## 3. Keep the three contracts distinct

| Surface | Protocol contract | Practical choice |
| --- | --- | --- |
| Tools | `tools/list`, `tools/call`, `inputSchema`; `outputSchema` is optional. | An action invoked at the model's request, with a clear effect and authorization scope. |
| Resources | `resources/list`, `resources/read`, URIs; `resources/templates/list` can be added. | Contextual data the host can select without performing an action. |
| Prompts | `prompts/list`, `prompts/get`, optional arguments and messages. | A task template presented for the user's deliberate selection. |

Declare the corresponding capability for every surface you support. Lists may change over time and depend on authorization for **the current request**, but not on hidden connection state or a side effect of an earlier RPC. Tool names should be stable and unique within a server; an aggregator of multiple servers resolves collisions. Validate resource URIs and prevent path traversal for file paths. [Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools), [Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources), [Prompts](https://modelcontextprotocol.io/specification/2026-07-28/server/prompts).

## 4. Choose a transport and secure the network boundary

`stdio` suits a process launched by the host: one JSON-RPC message per line on `stdin`/`stdout`. Send logs to `stderr` because `stdout` **must** contain MCP messages only. Such a process can also run on the service side. For remote HTTP, revision `2026-07-28` requires a single POST endpoint and a separate POST for each message. The client sends `Accept: application/json, text/event-stream`; the server may return one JSON response or an SSE stream tied to that request. HTTP requires an `MCP-Protocol-Version` header matching `_meta`, `Mcp-Method` for requests, and `Mcp-Name` for `tools/call`, `resources/read`, and `prompts/get`. The server **must** check `Origin`; for local use, it should bind to localhost. The old GET endpoint and `Mcp-Session-Id` are not part of the new revision. [stdio](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio), [Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http).

## 5. Bind authorization to every request

MCP authorization itself is optional. When protecting HTTP under the MCP authorization profile, the server publishes OAuth Protected Resource Metadata and validates the token and its audience on **every** request. The HTTP OAuth specification does not apply to `stdio`; credentials come from the process environment. In a multi-tenant system, derive identity from a trusted token or host, not from a model-supplied `tenant_id` argument. Recheck authorization for `tools/call` and `resources/read` even after list discovery. Database isolation, one process per tenant, a gateway, and the caching model are project decisions; cache keys must account for access scope. [Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization), [Caching](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/caching).

## 6. Handle changing lists and errors

Return lists in deterministic order and support pagination. If you declare `listChanged`, send notifications to clients that subscribe through `subscriptions/listen`; do not promise notifications without implementing them. Complete `server/discover`, list, and `resources/read` results **must** include `ttlMs ≥ 0` and `cacheScope`. These are cache hints, not substitutes for access checks; use `private` for an identity-dependent result. Return malformed RPCs or unknown tools as JSON-RPC errors; return tool execution failures as results with `isError: true` so the model can correct its call. `structuredContent` may be any JSON value; if you declare an `outputSchema`, the result **must** conform to it. For older clients, including a textual JSON representation can help. A nonexistent resource returns `-32602`, not an empty `contents` array. [Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools), [Resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources), [Caching](https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/caching).

## 7. Test interoperability

| Client/server | Handshake and state | HTTP transport | Decisive test |
| --- | --- | --- | --- |
| `2026-07-28` / `2026-07-28` | `_meta` on every request, `server/discover`; no `initialize`. | Sessionless POST and no GET; SSE only for responses or `subscriptions/listen`. | Correct headers; reject the wrong version and invalid `Origin`. |
| `2025-03-26`–`2025-11-25` | `initialize` and older session semantics. | Streamable HTTP with a different session and stream lifecycle. | Explicitly test with a host and SDK for that revision. |
| `2024-11-05` | `initialize`. | Older HTTP+SSE; a separate adapter if needed. | Connect to an actual older host. |

A new client and an old server do not become compatible by changing only the version number. Decide whether to support both protocol eras in one server or publish two adapters; test `server/discover`, fallback, and error behavior against the [version matrix](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning). Tests should cover cross-tenant access denial, invalid schemas, a tool removed after `tools/list`, large results, stream interruption, and resumption through an explicit application identifier. Use the [MCP Inspector](https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector/protocol-eras), and run a scenario through every target host before production.
