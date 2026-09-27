# Template: workflow with a model

Use this to describe a repeatable process. It may contain zero, one, or several model calls.

```text
Goal and trigger:
Input and expected outcome:
Deterministic steps:
Model-dependent steps and why they are needed:
Data and trust level at each step:
Tools, permissions, and side-effect boundaries:
Persistent state, checkpoints, and recovery:
Idempotent retry and compensation:
Human approval point and behavior after denial:
Timeout, cost, and retry limits:
Observability signals and evaluation set:
```

Test the full path in a small working vertical slice before expanding it. Related cards: `methods.vertical-slice`, `design.events-and-recovery`, `design.observability-and-evals`.
