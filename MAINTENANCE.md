# Maintaining the knowledge base

Use this runbook when reviewing this repository for changes in LLM engineering. It defines the research process; the cards remain the guidance for application work. Start with `catalog.json` and inspect only cards affected by a finding. Do not put the entire repository into one model context.

## Review cadence

- **Monthly:** Scan primary release notes, specifications, and security advisories for changes that could invalidate version dependent cards or reveal a material omission. Start with `protocols/`, `providers/`, `security/`, and `operations/`; expand to other cards when the evidence points there.
- **Quarterly:** Review the full catalog for important gaps, conflicting claims, stale links, changes in enterprise practice, and topics that deserve a new card. Recheck whether optional patterns are still labeled as choices rather than universal requirements.
- **Immediately when relevant:** Review affected cards after a breaking API or protocol change, a deprecation, a security incident, or a material change in law or standards. Do not wait for the next scheduled review.

The cadence is a reminder to investigate, not a statement that a card stays valid until its next review. Before applying version dependent guidance to an application, verify its target version and jurisdiction against current primary sources.

## Research scope

Check only topics that affect the repository, then map each finding to specific card IDs. Include:

1. Provider APIs and model capabilities: OpenAI, Anthropic, Google, xAI, and other providers when a card covers them; deprecations, compatibility, tool use, structured output, reasoning controls, context, streaming, realtime, data handling, and migration.
2. Interoperability and commerce: MCP, A2A, and any relevant agent communication or commerce specifications. Verify the official name, steward, revision, maturity, and security model of each candidate before adding it. Treat ACP, UCP, and x402 as research topics, not assumed universal standards.
3. Agent design and operations: orchestration, durable execution, state, retrieval, memory, evaluations, observability, reliability, cost controls, and deployment tradeoffs.
4. Enterprise risk: prompt injection, tool and content trust, identity, authorization, tenant isolation, secrets, approvals, sandboxing, privacy, retention, auditability, incident response, and applicable security or regulatory frameworks.

## Evidence and decisions

Prefer official specifications, vendor documentation and release notes, standards bodies, security advisories, and reproducible tests. Record the publication or revision date, the date checked, the exact version and scope, the source URL, and any uncertainty. A blog post, benchmark, or AI generated report can identify a lead; it cannot alone establish a requirement. Distinguish a released feature from a proposal, preview, or third party implementation.

For each candidate change, record: affected card ID and exact claim; evidence; impact on security, compatibility, reliability, cost, or usability; confidence; and one of **correct now**, **investigate or test**, **watch**, or **no change**. Separate verified requirements from recommended starting points and design options. State when evidence conflicts or when an enterprise practice applies only to a particular environment or jurisdiction.

Keep detailed working notes in the ignored `.private/` directory. For verified material corrections, follow [CONTRIBUTING.md](CONTRIBUTING.md): update the smallest relevant card, `catalog.json` when needed, and `sources/CLAIM-LEDGER.md`. Run `python3 scripts/kb.py check` and `python3 scripts/kb.py evaluate`. Report what was checked, what changed, what remains uncertain, and the next triggers to watch. Never call the entire knowledge base “up to date” based only on a partial scan.

## Prompt for the next review

> Review this knowledge base using `MAINTENANCE.md`. First inspect `catalog.json` and the relevant cards, then research current primary sources for the monthly changes or quarterly full review I request. Focus on claims whose versions, security assumptions, or enterprise recommendations may have changed. Produce a source linked finding list with exact card IDs, claim changes, impact, confidence, and proposed wording. Distinguish released standards from drafts and options from requirements. If I ask you to update the repository, apply only verified changes through `CONTRIBUTING.md` and run the repository checks. Keep raw research in `.private/` and keep application specific decisions out of this knowledge base.
