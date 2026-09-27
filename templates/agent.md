# Template: agent contract

Fill this in for a specific application. If a code-defined workflow can complete the task, justify using an agent with `decisions.agent-or-workflow`.

```text
Name and owner:
Goal and user:
Input and trigger:
Decisions delegated to the agent:
Termination condition and output format:
Tools available to this role:
Permissions enforced outside the model:
Model context / runtime state / persistent memory:
When approval is required:
Time, cost, turn, and retry limits:
Failure, escalation, and recovery policy:
Owner of the user-facing response:
Evaluation tasks and quality metrics:
```

Agent instructions must match the tools actually available at runtime. Outputs consumed by code should have a validated contract. Related cards: `design.agent-contract`, `security.approvals-and-side-effects`, `design.observability-and-evals`.
