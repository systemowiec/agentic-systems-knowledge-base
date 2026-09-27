# Template: tool or MCP server contract

This template does not decide whether the tool should be a local function, HTTP API, or MCP server. Justify the choice using interoperability, trust boundaries, and the execution environment.

```text
Operation name and purpose:
Who may call it, and how the server verifies identity:
Input: schema, validation, size limits:
Output: schema, data source, error types:
Side effects, affected resource, and recipient:
Idempotency key and retry semantics:
Timeout, limits, and cost:
Tenant scope and authorization at call time:
Approval or other risk control:
Contract version and client compatibility:
Tests: valid input, denied access, bad argument, retry:
```

If using MCP, check `protocols.mcp` and the version supported by the host. Model supplied values such as `tenant_id` are not proof of permission. Related cards: `design.tool-contract`, `security.identity-tenancy-privacy`.
