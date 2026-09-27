# Key terms: English with Polish equivalents

The English terms below are used throughout the canonical cards. This short reference is for people preparing discussions with clients; agents do not need it in their default context. Polish equivalents are approximate and may vary by project.

| English term | Polish equivalent | Practical meaning |
| --- | --- | --- |
| Agent | agent | A model driven process that chooses its next step from intermediate results. |
| Workflow | przepływ pracy | Steps and transitions defined by application code. |
| Orchestration | orkiestracja | Routing and coordination of model driven tasks. |
| Handoff | przekazanie sterowania | A specialist takes over responsibility for the next response. |
| Agent as tool | agent jako narzędzie | A specialist returns a bounded result to a coordinating agent. |
| Tool calling | wywoływanie narzędzi | The model proposes a call; application code executes and authorizes it. |
| Tool contract | kontrakt narzędzia | Input, output, errors, permissions, and side effects of a tool. |
| Runtime | środowisko wykonania | Code and infrastructure that run the agent and hold trusted state. |
| Context window | okno kontekstowe | Token capacity available to a model call, with input and output accounting defined by the API. |
| Context engineering | projektowanie kontekstu | Selecting and structuring information supplied to a model for a task. |
| Conversation state | stan rozmowy | Information required to continue a conversation correctly. |
| Persistent memory | trwała pamięć | Selected information retained across tasks or sessions. |
| Retrieval | wyszukiwanie | Fetching relevant evidence when needed. |
| RAG | generowanie wspomagane wyszukiwaniem | Generating an answer using retrieved evidence. |
| Chunking | dzielenie na fragmenty | Preparing source material for retrieval. |
| Embedding | reprezentacja wektorowa | A numeric representation used in semantic search. |
| Evaluation / eval | ewaluacja | Testing behavior against defined task outcomes. |
| Trace | ślad wykonania | A linked record of steps, tool calls, and results. |
| Observability | obserwowalność | Signals that let operators understand system behavior. |
| Guardrail | zabezpieczenie / ograniczenie | A control that constrains or checks behavior; its strength depends on where it is enforced. |
| Human-in-the-loop | udział człowieka w decyzji | A person reviews or approves a defined operation. |
| Approval | zatwierdzenie | An authorized person's recorded decision on a specific proposed action. |
| Prompt injection | wstrzyknięcie instrukcji | Untrusted content attempts to redirect model behavior. |
| Trust boundary | granica zaufania | Point where data or authority crosses between differently trusted parties. |
| Sandbox | izolowane środowisko | Constrained environment for executing potentially unsafe code. |
| Least privilege | minimalne uprawnienia | Only the permissions needed for the task are granted. |
| Idempotency | idempotencja | A retry does not create an additional side effect. |
| Retry | ponowienie | Another attempt after failure or an unknown outcome. |
| Background job | zadanie w tle | Work that continues independently of one interactive request. |
| Durable execution | trwałe wykonanie | Work can resume after a process failure without losing required state. |
| Claim / lease | przejęcie zadania / dzierżawa | A worker holds a task for a limited time before it can be recovered. |
| Multi-tenancy | wieloklienckość | One system serves distinct customers with enforced data boundaries. |
| Streaming | strumieniowanie | Sending partial events or output before a run finishes. |
| Structured output | wynik o określonym schemacie | Model output that is validated against a data contract. |
| Provider adapter | adapter dostawcy | Code that maps application needs to one model provider's API. |
| Gateway | brama pośrednicząca | Shared service for provider access, policy, or accounting when justified. |
| Rate limit | limit żądań | Provider imposed request or token throughput constraint. |
