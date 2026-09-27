# Generated interfaces and artifacts

> Use when: a model creates a view, form, code, or interactive artifact for a user.
> Do not use when: the response is only text or its data fits a predesigned view.

Available formats and isolation depend on the host.

## Decision

Choose a degree of freedom appropriate to the risk: schema-constrained data rendered by the application, a limited component set, or a full HTML/JS artifact in an isolated environment. The more code a model creates, the more important sandboxing, network policy, validation of messages between artifact and host, and accessibility testing become. No CSS framework or version is universally required; pin the version used in the project and inspect the generated result.

Generated view content may come from untrusted data. Do not treat it as trusted application code or give it direct access to tokens, the host DOM, or sensitive tools. Actions initiated in the view must pass through the normal authorization and approval contract.

## Controls

- For schemas, validate types and allowed components; for code, isolate execution and constrain CSP and messages to the host.
- Show the user where data came from and what buttons do; do not hide write operations behind apparently passive elements.
- Test keyboard use, screen readers, small screens, empty states, and tool failures.
- With MCP Apps, check host support for the extension; do not equate it with core MCP.

## Sources

- [MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview) — extension for interactive interfaces in MCP hosts.
- [OWASP, Cross Site Scripting Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) — safe rendering of untrusted content.
- [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) — accessibility.
