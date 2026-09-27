# Agent system production readiness

> Use when: an LLM or agent system will serve real users, handle real data, or act in a production environment.
> Do not use when: testing a single hypothesis in an isolated prototype without real data or external effects.

Scope: provider-independent decisions; check API details for the version in use.

## Decision

Assess readiness against **specific tasks, data, risks, and intended effects**, rather than a universal list of products. A shared gateway, a single provider, multiple models, content moderation, and comprehensive audit logging are use-case-dependent choices. Enforceable authorization boundaries, failure handling, and evidence of acceptable behavior in relevant scenarios are required.

## Controls

- Define successful and unwanted scenarios. Test representative tasks, indirect prompt injection, malformed data, unauthorized actions, work after timeouts, and model changes. Preserve a baseline before migration.
- Check authorization for every tool and data isolation; restrict network access and code execution. For high-impact actions, test the approval gate and rejection path.
- Set usage, cost, and concurrency limits. When a provider rate limit is reached, honor `Retry-After` or use bounded backoff with jitter; do not rely on rotating keys to bypass an organization- or project-level limit.
- Ensure idempotent side effects, handling for unknown outcomes, the ability to stop work, and data recovery within the retention policy.
- Observe quality, latency, cost, denied access, and task status. Logs must support auditing without storing secrets or excessive personal data; define their retention period.
- Check provider terms, data processing locations, and legal obligations in deployment jurisdictions. For example, Article 50 of the EU AI Act has a defined scope and exceptions; do not treat it as a global mandate for every system.

## Sources

- [NIST AI RMF Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) — use-case-specific risk management.
- [OWASP Top 10 for LLM Applications 2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/README.md) — 2026 edition's LLM risk map, including authority and agency; 2026 edition.
- [OpenAI, Rate limits](https://developers.openai.com/api/docs/guides/rate-limits) — limits and safe retries for this API.
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) — auditing, redaction, and retention.
- [EUR-Lex, Regulation (EU) 2024/1689, Article 50](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A02024R1689-20260727) — EU transparency obligations.
