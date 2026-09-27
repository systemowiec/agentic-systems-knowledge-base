# Topic map from version 2 to version 3

Use this map to check topic coverage, not to load every card for one task. Names on the left refer to the historical `docs/knowledge`; the right column shows the new locations.

| v2 file | v3 cards |
| --- | --- |
| `README.md` | `AGENT-ENTRY.md`, `catalog.json`, `sources/PROVENANCE.md` |
| `architecture/OVERVIEW.md` | `decisions/agent-or-workflow.md`, `decisions/single-or-multi-agent.md`, `decisions/provider-boundary.md` |
| `architecture/EVENTS.md` | `design/events-and-recovery.md`, `operations/background-work.md` |
| `architecture/PRIMITIVES.md` | `design/context-and-state.md`, `design/events-and-recovery.md`, `security/identity-tenancy-privacy.md` |
| `architecture/WALKING-SKELETON.md` | `methods/vertical-slice.md` |
| `principles/AGENT-DESIGN.md` | `decisions/agent-or-workflow.md`, `design/agent-contract.md`, `optional/cognitive-agents.md` |
| `principles/TOOL-DESIGN.md` | `design/tool-contract.md`, `design/observability-and-evals.md` |
| `principles/CONTEXT-ENGINEERING.md` | `design/context-and-state.md`, `design/retrieval-and-memory.md` |
| `principles/OBSERVABILITY.md` | `design/observability-and-evals.md`, `operations/production-readiness.md` |
| `principles/PRODUCTION.md` | `operations/production-readiness.md`, `security/trust-boundaries.md`, `design/context-and-state.md` |
| `principles/DEPLOYMENT.md` | `decisions/provider-boundary.md`, `operations/model-migration.md`, `providers/`, `security/sandboxing.md` |
| `principles/SECURITY.md` | `security/` |
| `principles/MCP-SERVER-BIBLE.md` | `protocols/mcp.md`, `design/tool-contract.md`, `security/sandboxing.md` |
| `patterns/COORDINATION.md` | `decisions/orchestration.md` |
| `patterns/AGENT-TEAMS.md` | `decisions/orchestration.md`, `optional/team-scheduler.md`, `design/events-and-recovery.md` |
| `patterns/COGNITIVE-ARCHITECTURE.md` | `optional/cognitive-agents.md` |
| `patterns/KNOWLEDGE.md` | `design/retrieval-and-memory.md`, `design/context-and-state.md` |
| `patterns/UI-FOR-AGENTS.md` | `ux/chat-streaming.md`, `ux/generative-ui.md`, `ux/voice.md` |
| `patterns/META-PROMPTING.md` | `methods/prompt-optimization.md` |
| `patterns/HUMAN-IN-THE-LOOP.md` | `security/approvals-and-side-effects.md`, `ux/chat-streaming.md` |
| `patterns/PROACTIVITY.md` | `operations/background-work.md`, `security/trust-boundaries.md` |
| `templates/agent.md` | `templates/agent.md` |
| `templates/mcp-server.md` | `templates/tool.md`, `protocols/mcp.md` |
| `templates/workflow.md` | `templates/workflow.md` |

The note on OpenAI agent orchestration was split between portable questions about response ownership and routing in `decisions/orchestration.md` and provider specific API details in `providers/openai.md`. SDK field names are not rules for every agent runtime.

Version 3 does not promote the AI_devs lesson map, reference product names, or fixed thresholds for tool counts and data sizes into normative guidance. Their provenance is noted in `sources/PROVENANCE.md`, and the reasons for claim corrections are in the claim ledger.
