# Retrieval, RAG, and memory design

This guide expands the [Retrieval, RAG, and memory](../design/retrieval-and-memory.md) card. Open it when a project involves private or changing documents, multi-step retrieval, or persistent memory. The short card is enough for an initial decision.

The guidance is provider-independent; API examples are sources, not requirements to use those APIs.

## 1. Start with questions, not an index

Record the tasks the system must answer and examples of correct sources. Include factual questions, synthesis across documents, exact-identifier lookup, questions requiring the current version, and questions the knowledge collection cannot answer. The last group matters just as much: without it, an agent may express false certainty.

Check whether retrieval is needed. A small, stable set of rules may fit in short context or code. A large, changing collection usually calls for finding relevant passages on demand. Separate “memory” is needed only when information should persist across tasks; it is not a synonym for a document index.

## 2. Define source ownership and lifecycle

Each document should have an identifier, owner, version, update time, access level, and withdrawal process. For documents belonging to multiple tenants, apply permission filters before passing results to the model. Checking after answer generation is too late: the model may already have seen another tenant's passage. Also verify caches, summary copies, and the index after a membership change or document deletion.

Ingestion may deduplicate, identify formats, and split text into chunks. Choose chunk boundaries based on document structure and question types; no single size works everywhere. Preserve the link between each chunk and its full source so citations can be verified. If extracting a PDF, image, or table loses meaning, fix extraction before tuning retrieval.

## 3. Choose and evaluate retrieval

Keyword search can work well for names, numbers, and exact phrases. Semantic search helps with paraphrases; hybrid search combines both signals. That does not mean hybrid always wins. Compare methods on questions representative of the product and grade against expected sources. Measure **recall** of needed passages and the share of irrelevant results, then assess final answer quality separately. Use metadata filters for version, language, date, and permissions where those fields matter.

For multi-step tasks, an agent may search again after seeing initial results, but limit steps and cost. Return source IDs, short excerpts, and a way to open the full document. Do not paste an entire collection “just in case.”

## 4. Separate evidence from instructions

Retrieved results are data, even if they say “ignore previous instructions.” Do not promote document text into system instructions. The application enforces permissions, approvals, and allowed actions outside the model. The model can explain which passage supports an answer; it cannot grant itself new access because a source asks it to.

An answer should show the source version or date when relevant. If sources disagree, expose the conflict or apply an explicit precedence rule set by the data owner. If there is no strong source, the task may end with “I don't know,” a clarification request, or escalation.

## 5. Memory needs its own policy

Memory of profiles, preferences, or earlier work requires decisions about who may write it, who may read it, how long it lasts, how a user can correct it, and how it is deleted. A model-generated summary is a hypothesis about earlier events, not automatically a source of truth. Preserve its provenance and verify important facts before acting on them later.

Do not let an agent turn instructions found on the web, in email, or in logs into persistent rules on its own. That creates a long-lived prompt injection channel. You may store an observation marked as coming from an untrusted source, then promote it to a rule only through a controlled process.

## 6. Minimum test set

Prepare cases with a correct source, two conflicting sources, an outdated document, no answer, a similar document from another tenant, a withdrawn document, prompt injection in a retrieved passage, and an extraction error. Check document selection, citations, answer content, tool actions, and absence of cross-tenant leakage separately. Rerun the same set after changing the model, chunking, or ranking.

## Sources

- [Lewis et al., Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — the original RAG paper.
- [OpenAI, Retrieval](https://developers.openai.com/api/docs/guides/retrieval) — an example of search, filtering, and ranking; a provider implementation.
- [OWASP GenAI Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) — prompt injection and memory poisoning.
- [OWASP Multi Tenant Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html) — data isolation between tenants.
