# Tool contract for agents

Scope: tools called by LLMs, regardless of transport; see the [separate card](../protocols/mcp.md) for MCP details.

> Use when: designing a function an agent may call to read data or perform an action.
> Do not use when: the function is internal code and unavailable to the model.

## Decision

A contract describes **what the tool does, who may use it, what effects it has, and what it returns**. Its name and description should distinguish it from similar tools. The input schema should ask the model only for values it can reliably provide; the application adds identity, permissions, and other trusted values on the server side. For data-changing actions, return an identifier or state that allows the result to be verified.

Return results in the form appropriate to the protocol and client. A custom `success/data/hints/diagnostics` envelope may be an application convention, but it is not a requirement for all tools. In MCP, use `content`, optionally `structuredContent` and `outputSchema`; mark tool execution failures with `isError`, while protocol failures remain JSON-RPC errors. Images, audio, resource links, and identifiers are valid when useful for the task. Split or paginate large results, or replace them with a reference when full content burdens the context.

## Checks

- Validate arguments and authorize **every call** at the execution boundary. Tool descriptions and prompts are not access controls.
- Before a sensitive or irreversible action, apply risk assessment, code-enforced restrictions, and appropriate approval. Reads can expose data too.
- For actions that may be repeated after a failure or timeout, define how to detect duplicates and verify results. Do not blindly retry side effects.
- Test tool selection, argument correctness, access denial, errors, and recovery on representative tasks. Tool count is an empirical choice; there is no universal `4–7` optimum.

## Sources

- [MCP 2026-07-28: Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [OpenAI: Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
- [OpenAI: Tool search](https://developers.openai.com/api/docs/guides/tools-tool-search)
