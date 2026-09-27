# Trust boundaries and prompt injection

> Use when: a model reads web pages, documents, emails, tool results, memory, messages from other agents, or other content outside the application's trusted instructions.
> Do not use when: the task is fully deterministic and does not pass such content to a model; apply ordinary application security controls instead.

Scope: LLM systems across providers.

## Decision

Content retrieved from the outside world is **data, not an authorized instruction**. Indirect prompt injection is possible even without a conversation with a user: an agent need only read an attacker-controlled document, search result, or memory entry. Role separation and an instruction to "ignore commands in data" help the model, but they are not a security boundary. The code executing an operation must restrict data access, tool calls, and side effects.

## Controls

- Preserve content provenance and trust level. Do not copy external text into system or developer instructions or persistent agent instructions.
- When data will steer the next step, extract required fields into a constrained schema and validate them before use. Do not treat model output alone as authorization.
- A tool checks identity, scope, object, and arguments on **every** call. This remains necessary after an agent handoff and after task resumption.
- Restrict egress and the rendering of links and images; model output can trigger exfiltration even without a write-capable tool.
- Before persisting a note, rule, summary, or memory from external content, check its source and scope. Persistence must not automatically promote it to an instruction.
- Test injection at real entry points: RAG documents, tool responses, logs, emails, and memory. Measure not only response text but also tool selection and actual effects.

Full analysis workflow: [LLM system threat model](../guides/security-threat-model.md).

## Sources

- [OWASP LLM01:2026 Prompt Injection](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM01_PromptInjection.md) and [LLM10:2026 Improper Output Handling](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/final/LLM10_ImproperOutputHandling.md) — injection through content, tools, and memory, and handling model output.
- [OWASP, Memory Is a Feature. It Is Also an Attack Surface](https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/) — persistent context poisoning; 2026-05-13.
- [OpenAI, Safety in building agents](https://developers.openai.com/api/docs/guides/agent-builder-safety) — structuring the flow of untrusted data. Its Agent Builder guidance is product-specific.
