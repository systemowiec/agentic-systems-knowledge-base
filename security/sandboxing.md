# Isolating agent code and tools

> Use when: an agent runs code or shell commands, uses a browser with data access, or processes untrusted files in an execution environment.
> Do not use when: the agent has no execution environment or tools that can reach resources; still enforce access control on its other tools.

Scope: self-hosted and managed execution environments.

## Decision

Code selected or written by a model runs with the privileges of **the execution process**. A prompt, command-name filter, or absence of a `.env` file in the current directory does not restrict the process's access to secrets and the network. Treat untrusted code as requiring isolation proportional to the consequences of compromise; a sandbox provider's name does not establish its security properties.

## Controls

- Separate execution from services that hold credentials and broad privileges. Expose protected systems through narrow tools that check every request.
- Isolate workloads and data across users or tenants when they must not share resources. Restrict mounted paths and writes; use accounts without unnecessary privileges, and limit processes, memory, CPU, disk, and runtime.
- Apply egress controls appropriate to the task, including DNS and access to internal addresses. A domain allowlist is only one layer; account for redirects, proxies, and SSRF.
- Do not pass unnecessary secrets into a process in which the agent can run code. An environment variable accessible to that process **is not** a boundary between the agent and its tools. Use short-lived, narrowly scoped credentials and a secret broker or manager where the threat model requires one.
- Record execution metadata and outcomes needed for auditing, with redaction of secrets and sensitive data. Test interruption, resource limits, attempts to read another user's data, and traffic outside the allowed scope.

## Sources

- [OpenAI, Sandbox security](https://developers.openai.com/api/docs/guides/agents-api/environments/security) — isolation, networking, and credentials.
- [OpenAI, Local shell](https://developers.openai.com/api/docs/guides/tools-local-shell) — application-enforced isolation and limits.
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) — environment-variable risks and secret scope.
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) — an example of process privilege controls. This does not imply a requirement to use Kubernetes.
