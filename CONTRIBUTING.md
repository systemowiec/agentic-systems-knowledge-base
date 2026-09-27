# Updating the knowledge base

## Language policy

Write canonical cards, guides, catalog descriptions, templates, and agent-facing output in English. Preserve official API names, protocol fields, and source titles. Polish belongs only in the optional human [terminology reference](TERMINOLOGY.md) and in search aliases or test queries that verify Polish lookup. Do not maintain parallel translations of the cards.

## Types of content

- **Durable principle:** follows from a trust boundary, data ownership, a contract, or an observable risk. It may still have exceptions.
- **Design choice:** compares options and conditions instead of declaring one technology mandatory.
- **Version dependent fact:** describes a protocol, SDK, model, API, standard, or regulation. Name its applicable version, model, or jurisdiction, link to a direct primary source, and write guidance that prompts verification before use.
- **Example:** illustrates a choice; it is not a rule for other applications.

## Change procedure

1. Identify the exact claim to add or correct and the situations in which it matters.
2. Check the official specification or documentation, primary research, or a reproducible test. Record the URL, review date, and limits of the evidence in the correction ledger when the change is material; Git history retains editorial changes. A single AI generated report is not sufficient evidence.
3. Record significant corrections to security, protocols, APIs, or previous claims under “Corrections after the v3 release” in `sources/CLAIM-LEDGER.md`. Include the old and new wording, version scope, and evidence. Keep the historical v2 to v3 table intact.
4. Change one canonical card. Link to it from other locations instead of copying its rule.
5. Update `catalog.json`, including its summary, triggers, risk tags, and `version_scope`.
6. Run `python3 scripts/kb.py check` and `python3 scripts/kb.py evaluate`. For provider or model dependent changes, also test a representative task in the target environment.

Do not label every pattern a “best practice.” Distinguish verified requirements, reasonable starting points, and choices that need measurement. Do not add fixed thresholds for agent or tool counts, bytes, or tokens without evidence and a defined scope.

## Freshness review

A specification change, API deprecation, or security incident triggers review of affected cards. Check version dependent cards periodically against current primary sources. The claim ledger retains material corrections, and Git retains earlier versions.
