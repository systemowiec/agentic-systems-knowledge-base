# Project instruction snippet for agents

Copy the text below into your application's agent instructions and replace `<knowledge-base-path>` with the local path. The application's requirements, permissions, and user instructions still apply.

```text
When a task involves an LLM or agent system, use the knowledge base at <knowledge-base-path> selectively. First read AGENT-ENTRY.md. If terminal access and Python 3 are available, use `python3 <knowledge-base-path>/scripts/kb.py search "task description"` to find candidate cards, or `pack` with relevant `--risk` flags for short excerpts. If the script is unavailable or its results are incomplete, inspect `catalog.json` and topic directories. Open only cards that may affect the decision. For writes, private data, multiple tenants, untrusted sources, or code execution, include the applicable security cards. Verify time-sensitive API, model, protocol, security standard, and regulatory claims against current primary sources. If verification is unavailable, state that limit. In your result, cite relevant card IDs and important deviations. Do not load the whole knowledge base into context.
```
