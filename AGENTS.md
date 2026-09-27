# Instructions for agents

Start with [AGENT-ENTRY.md](AGENT-ENTRY.md) when using this knowledge base. Select only relevant cards and avoid loading the entire repository into context. Verify time-sensitive claims about models, APIs, protocols, security standards, and regulations against current primary sources before implementation. If verification is unavailable, state that limit.

If you have terminal access and Python 3, you may use the local, read-only `scripts/kb.py` to select cards: run `python3 scripts/kb.py search "task description"` for candidates, or `python3 scripts/kb.py pack "task description" --risk multi_tenant --risk untrusted_content` for short excerpts with applicable security cards. Use only risk flags that match the task; run `python3 scripts/kb.py --help` to see the commands and flags. Open full cards before relying on their rationale or sources. The script is a heuristic index, so inspect `catalog.json` or the relevant directories if results are missing or surprising. Without a terminal or Python 3, use `catalog.json` and the cards directly.

Do not load the local `.private/` directory by default. Its drafts and research notes are unverified inputs, not canonical guidance; consult them only when the user asks for that work.

When changing this repository, follow [CONTRIBUTING.md](CONTRIBUTING.md), provide evidence for changed claims, and run `python3 scripts/kb.py check` and `python3 scripts/kb.py evaluate`. Keep application specific decisions and data in the application repository.
