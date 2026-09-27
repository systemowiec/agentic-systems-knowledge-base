# Multi-agent runtime

Open this guide only when the [decision to split agents](../decisions/single-or-multi-agent.md) confirms a need for collaboration, or when work must survive a process failure. A simple task may need only one agent loop or a [workflow](../decisions/agent-or-workflow.md). The patterns below are portable design choices, not requirements of a particular framework.

## 1. Define boundaries and response ownership

Every agent should have a specific reason to exist: a distinct tool surface, permission scope, approval policy, result format, model, or responsibility for the conversation. Record that reason in its contract and test whether the split improves quality or control compared with one agent. A separate domain name, a long prompt, or organizational convenience alone is insufficient.

Choose one owner of the user response for each branch. If a specialist takes over the conversation, use a **handoff**: control and responsibility for the next response transfer together. If the specialist performs a bounded analysis and returns to the coordinator, use a **helper** with a tool-like contract. The coordinator then synthesizes the response. Avoid cases where both independently answer the user or neither does.

Describe routing with short, discriminating conditions. It should be clear which inputs select a specialist and when the case returns to the coordinator. Provide an “unable to handle” result and an escalation path. Runtime controls, not only a prompt instruction, must limit misrouting and cyclic handoffs.

## 2. Set an inter-agent contract

A delegation should carry the minimum the recipient needs: case ID, goal, permitted actions, deadline or budget, references to data, contract version, and expected result. If code consumes the result, use a schema and validation. Distinguish task results, requests for more data, permission denials, transient errors, and permanent errors. A bare “done” without an effect identifier or validated result is not enough to close a task.

Do not copy the entire conversation history to every specialist. Pass a summary of important decisions and authorized artifact references, then fetch details on demand. A reference is not a permission grant: authorize the recipient when it reads the artifact. Initiator identity, credentials, database clients, and execution state stay in code. If the recipient needs part of that information, the application supplies only its necessary, safe representation.

Messages and results from another agent are also data with provenance. Do not automatically promote them to system instructions. Check permissions for every tool at execution time, including after a handoff or resumption.

## 3. Add durability only when needed

A short delegation can run in one loop. When a task waits for a person, runs for a long time, or must survive a failure, persist its ID, state, dependencies, assigned worker, result, and error reason. A pending approval state preserves the exact intended action and the policy or required approver role; after a decision, record the verified identity of the person who made it. Then resume the same operation if the runtime allows it; do not present it as a new user instruction.

Model task dependencies explicitly when they exist. A DAG helps identify ready work and blocked work; reject cycles. A DAG is not required for every conversation among agents. With multiple workers, use a **claim/lease** mechanism or an equivalent queue. A task may return to the pool after its lease expires, so account for duplicate execution. An external write needs an idempotency key or a check of its result before retrying. Do not assume that a missing response means no effect occurred.

Retries need a limit and delay, and must distinguish transient from permanent errors. Provide states for orphaned, cancelled, and human-pending tasks. When workers update a shared document or state, assign resource ownership or check its version before writing. Resolve conflicts explicitly; “last write wins” may discard another worker's changes. A shared results board can help some systems but is not a mandatory component.

## 4. Evaluate the whole execution

Compare the system with a simpler baseline on the same tasks. Measure final task success, routing correctness, helper result quality, cost, latency, and unnecessary handoffs. A trace should show who requested an action, who performed it, which policy applied, and what effect occurred, subject to privacy rules. Test specialist refusal, invalid result schema, handoff cycles, failure after an external side effect, lease expiry, retries, and cancellation of a task subtree. For multi-tenant systems, test tenant boundary crossing after each handoff.

## 5. OpenAI Agents SDK fields are provider-specific

In the OpenAI Agents SDK, `handoff` transfers control and `agent.asTool()` returns a result to the lead agent. `outputType` defines structured output. A run result may include `lastAgent`, history, `interruptions`, and state for resumption after approval; whether to use `session` or a continuation identifier depends on how history is managed. These names and behaviors describe the **OpenAI SDK**, not a universal protocol. When transferring the pattern to another runtime, preserve the intent of the contract and test that runtime's actual state semantics. [A2A](../protocols/a2a.md) supports collaboration between independent systems across a service boundary when a local contract is insufficient; internal delegation does not require it.

## Sources

- [OpenAI, Orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration) — response ownership, handoffs, and agents as tools.
- [OpenAI, Agent definitions](https://developers.openai.com/api/docs/guides/agents/define-agents) — specialist contracts and structured output.
- [OpenAI, Results and state](https://developers.openai.com/api/docs/guides/agents/results) — history, `lastAgent`, and run resumption.
- [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) — selecting patterns and measuring the benefits of complexity.
- [Temporal, Durable AI](https://docs.temporal.io/ai) — an example of durable execution and failure recovery, without prescribing that implementation.
