# Retrieval, RAG, and memory

> Use when: answers or actions must draw on a large, changing, or private knowledge collection.
> Do not use when: a small stable set of facts can safely be provided directly, or the task needs no external knowledge.

Retrieval implementations differ among providers.

Implementation details: [Retrieval, RAG, and memory design](../guides/retrieval-and-memory-design.md).

## Decision

Retrieval supplies evidence **on demand**; memory retains selected information across tasks. Do not conflate them. Start with a specific question: what data does the model lack, who may see it, and how will we know the right passages were found? Choose lexical, semantic, or hybrid search based on tests with your own queries, not merely because vectors are available.

For RAG, evaluate three things separately: whether the right material was retrieved, whether the answer follows from it, and whether the user sees the right source. Retrieved results are untrusted content. A citation or document excerpt cannot grant the agent new permissions. In multi-tenant systems, the access filter must apply **before** results reach the model; asking the model afterward to ignore another tenant's data does not protect isolation.

Store memory only with a defined purpose, scope, expiration, and way to correct or delete it. Do not automatically persist instructions found on web pages, in emails, or in tool results.

## Checks

- Collect representative queries with expected sources, including no answer, an outdated document, and a similar document from another tenant.
- Measure retrieval relevance separately from answer quality. Compare lexical, semantic, and hybrid search where the difference matters.
- Preserve document ID, version, provenance, and permissions. After deletion or permission changes, verify the index and cache too.
- Distinguish sources from model inferences in the answer; expose conflicts between sources.

## Sources

- [OpenAI, Retrieval](https://developers.openai.com/api/docs/guides/retrieval) — semantic and hybrid search, filtering, and ranking.
- [Lewis et al., Retrieval-Augmented Generation, 2020](https://arxiv.org/abs/2005.11401) — paper introducing the RAG pattern; does not by itself determine an infrastructure choice.
- [OWASP GenAI Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) — prompt injection and memory poisoning risks.
