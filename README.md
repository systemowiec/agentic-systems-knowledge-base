# Agentic Systems Knowledge Base

A project-independent knowledge base for designing, building, and evaluating LLM applications and agent systems. It assumes no particular product, provider, cloud, or need for multiple agents.

This is a living reference. Before implementing time-sensitive guidance, verify the target version or jurisdiction against current primary sources. A card is a starting point for that check, not a guarantee of current API behavior.

## Quick start

Agents should start with [AGENT-ENTRY.md](AGENT-ENTRY.md). Do not load the entire knowledge base into a prompt.

```sh
python3 scripts/kb.py search "an assistant analyzes private documents for several customers"
python3 scripts/kb.py pack "an assistant analyzes private documents for several customers" --risk multi_tenant --risk untrusted_content
python3 scripts/kb.py show security.identity-tenancy-privacy
python3 scripts/kb.py check
python3 scripts/kb.py evaluate
```

`search` returns a short candidate list. `pack` creates a bounded context pack and includes relevant security cards for declared risks. Its limit is measured in words, not model tokens; measure tokens with the target model's tokenizer when a strict budget matters. `show` opens a complete card. None of these commands requires a network service or vector database. Polish queries are also supported by search aliases; the returned guidance remains in English.

You can also ask an agent: “Use this knowledge base. Select only cards relevant to the task, verify version dependent sources, and cite the card IDs behind your decisions.” A ready to use project instruction is in [adapters/AGENTS-snippet.md](adapters/AGENTS-snippet.md).

## Structure

| Directory | Contents |
| --- | --- |
| `decisions/` | Agent versus workflow, one versus many agents, orchestration, and provider boundaries. |
| `design/` | Agent and tool contracts, context, state, retrieval, events, and evaluation. |
| `security/` | Trust boundaries, identity, data isolation, approvals, and sandboxing. |
| `operations/` | Background work, production readiness, and model migration. |
| `ux/` | Chat, generated UI, and voice. |
| `protocols/`, `providers/` | Version dependent protocol and API guidance. |
| `guides/` | Longer guides to open only after selecting a relevant card. |
| `methods/`, `optional/`, `templates/` | Working methods, optional patterns, and templates. |
| `sources/` | Evidence, migration mapping, and claim history. |

`catalog.json` is a compact search index, not a substitute for card content or sources. Each card starts with the decision; details and references follow. **Requirement**, **recommendation**, and **option** have different meanings: a requirement follows from a specific contract or threat, a recommendation is a starting point to test in a project, and an option is one possible design.

`.private/` is an optional local workspace for research prompts, drafts, and review notes. Git ignores the entire directory, so create it after cloning with `mkdir -p .private`. Its contents are working material, not verified guidance; move supported conclusions into the public cards through [CONTRIBUTING.md](CONTRIBUTING.md).

## How to use this knowledge base

- Start with the simplest architecture that meets requirements and evaluation results. Do not add agents, MCP, RAG, a gateway, or event sourcing merely because each has a card.
- Before implementing API or protocol guidance, check the version used by the project and the current primary documentation.
- Keep application decisions in the application repository and refer to relevant cards by ID. Do not put project specific decisions here.
- Follow [CONTRIBUTING.md](CONTRIBUTING.md) when changing this knowledge base. Sources and review history are part of the deliverable.

The selective reading structure is our design, informed by [skill discovery](https://developers.openai.com/api/docs/guides/tools-skills) and [deferred tool loading](https://developers.openai.com/api/docs/guides/tools-tool-search). It does not depend on either API. For human reference, [TERMINOLOGY.md](TERMINOLOGY.md) gives concise Polish equivalents of key English terms; agents do not need to load it by default.
