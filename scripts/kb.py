#!/usr/bin/env python3
"""Small, dependency-free index and context packer for this knowledge base."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog.json"
CARD_DIRS = ("decisions", "design", "security", "operations", "ux", "protocols", "providers", "methods", "optional")
RISKS = {
    "write": ("security.approvals-and-side-effects",),
    "external_action": ("security.approvals-and-side-effects",),
    "multi_tenant": ("security.identity-tenancy-privacy",),
    "personal_data": ("security.identity-tenancy-privacy",),
    "untrusted_content": ("security.trust-boundaries",),
    "secrets": ("security.trust-boundaries",),
    "code_execution": ("security.sandboxing", "security.trust-boundaries"),
}
STOP = {
    "a", "an", "and", "are", "as", "at", "be", "by", "do", "for", "from", "in", "is", "of", "on", "or", "the", "to", "with",
    "i", "a", "ale", "czy", "dla", "do", "jest", "jak", "lub", "na", "od", "oraz", "po", "przez", "sie", "to", "w", "we", "z", "ze",
}
SPECIALIZED = {
    "decisions.agent-or-workflow": ("workflow", "automat", "automatyzac", "do we need an agent", "build assistant", "create assistant", "faq"),
    "decisions.orchestration": ("handoff", "orchestrat", "orkiestr", "routing", "triage", "specialist", "specjalist", "coordinat", "koordynac", "delegat", "delegac", "multiagent", "multi-agent", "wieloagent"),
    "decisions.provider-boundary": ("gateway", "adapter", "dostawc", "provider", "openai", "anthropic", "claude", "gemini", "google"),
    "decisions.single-or-multi-agent": ("multiagent", "multi-agent", "wieloagent", "wielu agent", "specialist", "specjalist", "subagent", "handoff", "triage"),
    "design.agent-contract": ("agent contract", "kontrakt agent", "agent definition", "definicj agent", "output schema", "schemat wynik", "output format", "format wynik", "validat", "walidowan", "json", "handoff", "specialist", "specjalist", "triage"),
    "design.context-and-state": ("context", "kontekst", "histor", "state", "stan", "memory", "pamiec", "conversation", "rozmow", "resum", "wznow", "artifact reference", "large artifact", "artifact store", "odnosnik do artefakt", "duze wyniki narzedz", "referenc", "session", "continuation"),
    "design.events-and-recovery": ("resum", "wznow", "restar", "event", "zdarzen", "retry", "ponow", "long-running", "dlugotr", "wielogodz", "paus", "checkpoint", "timeout"),
    "design.tool-contract": ("tool", "narzedz", "function", "mcp", "send", "wysyl", "publish", "publik", "pay", "platn", "writ", "zapis", "tool schema"),
    "methods.prompt-optimization": ("prompt optim", "prompt tun", "improve prompt", "meta-prompt", "metaprompt", "optymalizac prompt", "popraw prompt", "strojen prompt"),
    "methods.vertical-slice": ("vertical slice", "walking skeleton", "first prototype", "new system", "end-to-end integration", "first working path", "pierwszy prototyp", "nowy system", "ryzykowna integrac"),
    "operations.background-work": ("background", "w tle", "proactiv", "proakty", "webhook", "schedul", "harmonogram", "queue", "kolejka", "long-running", "dlugotr", "wielogodz", "worker", "asynchron"),
    "operations.model-migration": ("migr", "model chang", "model switch", "zmian model", "wymian model", "deprec", "przenos", "upgrade"),
    "operations.production-readiness": ("production", "produkc", "deploy", "wdro", "go live", "launch", "release", "scal", "skalow"),
    "optional.cognitive-agents": ("cognitiv", "kognity", "theory of mind", "think recall", "samoucz", "metapozn"),
    "optional.team-scheduler": ("scheduler", "team schedul", "harmonogram zespol", "dag", "lease", "claim", "blackboard", "zespol agent"),
    "protocols.a2a": ("a2a", "agent2agent", "agent-to-agent", "agent interoperability", "interoperacyjnosc agent"),
    "protocols.mcp": ("mcp", "model context protocol"),
    "providers.openai": ("openai", "responses api", "agents api", "gpt"),
    "providers.anthropic": ("anthropic", "claude", "messages api"),
    "providers.google": ("google", "gemini", "generatecontent", "interactions api"),
    "security.approvals-and-side-effects": ("approv", "consent", "write", "send", "publish", "delete", "pay", "purchas", "side effect", "external action", "authoriz", "zatwier", "zgod", "zapis", "wysyl", "publik", "usun", "platn"),
    "security.identity-tenancy-privacy": ("tenant", "private", "personal data", "identity", "authoriz", "resource access", "access control", "permission", "customer", "prywat", "poufn", "tozsamos", "uprawn", "autoryz", "dostep", "osobow", "nagran", "wielu klient", "kilku klient"),
    "security.sandboxing": ("sandbox", "code execution", "shell", "script", "javascript", "html", "container", "izolac kod", "wykonan kod", "uruchamian kod", "skrypt", "kontener"),
    "ux.chat-streaming": ("chat", "stream", "conversation ui", "realtime", "real-time", "czat", "interfejs rozmow"),
    "ux.generative-ui": ("generativ", "interactiv", "artifact", "artefakt", "html", "javascript", "render", "ui", "mcp apps"),
    "ux.voice": ("voice", "audio", "speech", "transcrib", "microphone", "glos", "mow", "transkry", "mikrofon", "nagran"),
}
ALIASES = {
    "faq": ("rag", "retrieval", "knowledge", "wiedza"),
    "sprawdz": ("evaluation", "eval"),
    "trafn": ("evaluation", "eval"),
    "poprawn": ("evaluation", "eval"),
    "jakosc": ("quality", "evaluation", "eval"),
    "ocen": ("evaluation", "eval"),
    "audyt": ("audit", "evaluation", "eval"),
    "wyszuk": ("retrieval", "rag"),
    "zrod": ("retrieval", "rag"),
    "wznow": ("recovery", "resume"),
    "restart": ("recovery", "resume"),
    "zatwier": ("approval",),
    "retriev": ("retrieval",),
}


def plain(value: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", value.lower())
    return "".join(c for c in ascii_text if not unicodedata.combining(c)).replace("ł", "l")


def words(value: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9_]+", plain(value)) if len(w) > 1 and w not in STOP]


def query_words(value: str) -> set[str]:
    base = set(words(value))
    expanded = set(base)
    for token in base:
        for prefix, aliases in ALIASES.items():
            if token.startswith(prefix):
                expanded.update(aliases)
    return expanded


def load_catalog() -> list[dict]:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if data.get("schema_version") != 2 or not isinstance(data.get("entries"), list):
        raise ValueError("catalog.json: expected schema_version=2 and an entries list")
    return data["entries"]


def matching(a: str, b: str) -> bool:
    if a == b:
        return True
    if len(a) < 7 or len(b) < 7:
        return False
    common = 0
    for ca, cb in zip(a, b):
        if ca != cb:
            break
        common += 1
    return common >= 7 and common / min(len(a), len(b)) >= 0.72


def gate_match(term: str, query: str) -> bool:
    if len(term) <= 3 and term.isalnum():
        return bool(re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", query))
    return term in query


def score(entry: dict, query: str, entries: list[dict]) -> float:
    tokens = query_words(query)
    if not tokens:
        return 0.0
    gate = SPECIALIZED.get(entry["id"])
    if gate and not any(gate_match(term, plain(query)) for term in gate):
        return 0.0
    weighted = (
        (entry["id"], 7),
        (entry["title"], 7),
        (" ".join(entry["keywords"]), 6),
        (" ".join(entry["use_when"]), 5),
        (entry["summary"], 3),
    )
    field_tokens = [(set(words(text)), weight) for text, weight in weighted]
    result = 0.0
    matched = 0
    for token in tokens:
        strength = max((weight for field, weight in field_tokens if any(matching(token, w) for w in field)), default=0)
        if not strength:
            continue
        frequency = sum(any(matching(token, w) for w in words(" ".join([e["id"], e["title"], e["summary"]] + e["keywords"] + e["use_when"]))) for e in entries)
        rarity = 1 + math.log((len(entries) + 1) / (frequency + 1))
        result += strength * rarity
        matched += 1
    if matched >= 2:
        result += min(matched, 5) * 2
    if entry["id"] == "design.tool-contract" and any(term in plain(query) for term in ("migr", "przenos", "zmian dostawc", "switch provider", "change provider")):
        result *= 0.3  # In a provider migration, compare both provider contracts before the generic tool card.
    return result


def ranked(entries: list[dict], query: str) -> list[dict]:
    scores = {e["id"]: score(e, query, entries) for e in entries}
    return sorted((e for e in entries if scores[e["id"]] > 0), key=lambda e: (-scores[e["id"]], e["id"]))


def select(entries: list[dict], query: str, risks: list[str], includes: list[str], limit: int) -> list[dict]:
    by_id = {e["id"]: e for e in entries}
    result: list[dict] = []
    normalized = plain(query)
    automatic: list[str] = []
    if any(term in normalized for term in ("histor", "histori")):
        automatic.append("design.context-and-state")
    if "faq" in normalized and any(term in normalized for term in ("build", "creat", "assistant", "agent", "buduj", "tworz", "asystent")):
        automatic.append("decisions.agent-or-workflow")
    if any(term in normalized for term in ("handoff", "specialist", "specjalist", "triage", "validat", "walidowan", "json")):
        automatic.append("design.agent-contract")
    if any(term in normalized for term in ("long-running", "wielogodz", "dlugotr")) and any(term in normalized for term in ("restart", "resum", "wznow", "worker")):
        automatic.append("operations.background-work")
    for risk in risks:
        for card_id in RISKS[risk]:
            if card_id not in by_id:
                raise ValueError(f"Missing security card {card_id} for risk {risk}")
            if by_id[card_id] not in result:
                result.append(by_id[card_id])
    for card_id in includes + automatic:
        if card_id not in by_id:
            raise ValueError(f"Unknown ID: {card_id}")
        if by_id[card_id] not in result:
            result.append(by_id[card_id])
    candidates = ranked(entries, query)
    top_score = score(candidates[0], query, entries) if candidates else 0
    target_limit = max(limit, len(result))
    for entry in candidates:
        if len(result) >= target_limit:
            break
        if score(entry, query, entries) < max(10, top_score * 0.15):
            break
        if entry not in result:
            result.append(entry)
    return result


def decision_excerpt(path: Path, max_words: int, query: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^## Decision\s*$", text, flags=re.MULTILINE)
    if not match:
        return "[Missing ## Decision section; open the full card.]"
    next_heading = re.search(r"^## ", text[match.end():], flags=re.MULTILINE)
    section = text[match.end(): match.end() + next_heading.start() if next_heading else None].strip()
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", section) if p.strip()]
    query_tokens = query_words(query)
    paragraphs = [p for _, p in sorted(
        enumerate(paragraphs),
        key=lambda item: (
            -sum(any(matching(token, word) for word in words(item[1])) for token in query_tokens),
            item[0],
        ),
    )]
    chosen: list[str] = []
    count = 0
    for paragraph in paragraphs:
        size = len(paragraph.split())
        if chosen and count + size > max_words:
            break
        if not chosen and size > max_words:
            paragraph = " ".join(paragraph.split()[:max_words - 1]) + " […]"
            size = max_words
        chosen.append(paragraph)
        count += size
    return "\n\n".join(chosen)


def check(entries: list[dict]) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    paths: set[str] = set()
    required = {"id", "path", "title", "summary", "use_when", "do_not_use_when", "keywords", "risk_tags", "status", "version_scope"}
    for entry in entries:
        missing = required - set(entry)
        if missing:
            errors.append(f"{entry.get('id', '<missing ID>')}: missing fields {sorted(missing)}")
            continue
        card_id = entry["id"]
        path = entry["path"]
        if card_id in ids:
            errors.append(f"Duplicate ID: {card_id}")
        if path in paths:
            errors.append(f"Duplicate path: {path}")
        ids.add(card_id)
        paths.add(path)
        if not all(isinstance(entry[key], str) and entry[key].strip() for key in ("id", "path", "title", "summary", "status", "version_scope")):
            errors.append(f"{card_id}: empty or invalid text field")
        for key in ("use_when", "do_not_use_when", "keywords", "risk_tags"):
            if not isinstance(entry[key], list) or not all(isinstance(v, str) for v in entry[key]):
                errors.append(f"{card_id}: {key} must be a list of strings")
        file = (ROOT / path).resolve()
        if ROOT not in file.parents or not file.is_file():
            errors.append(f"{card_id}: file missing or outside repository: {path}")
            continue
        body = file.read_text(encoding="utf-8")
        if not body.startswith("# ") or "## Decision" not in body or "## Sources" not in body:
            errors.append(f"{card_id}: missing title, ## Decision, or ## Sources")
        elif body.splitlines()[0][2:].strip() != entry["title"]:
            errors.append(f"{card_id}: catalog title differs from card title")
    for folder in CARD_DIRS:
        for file in (ROOT / folder).rglob("*.md"):
            if file.relative_to(ROOT).as_posix() not in paths:
                errors.append(f"Card not listed in catalog: {file.relative_to(ROOT)}")
    for risk, card_ids in RISKS.items():
        for card_id in card_ids:
            if card_id not in ids:
                errors.append(f"Risk {risk}: missing required card {card_id}")
    for file in ROOT.rglob("*.md"):
        if ".git" in file.parts:
            continue
        body = file.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", body):
            target = target.split("#", 1)[0]
            if not target or target.startswith(("https://", "http://", "mailto:")):
                continue
            linked = (file.parent / unquote(target)).resolve()
            if (ROOT not in linked.parents and linked != ROOT) or not linked.exists():
                errors.append(f"{file.relative_to(ROOT)}: invalid local link {target}")
    return errors


def evaluate(entries: list[dict], fixture: Path) -> int:
    cases = json.loads(fixture.read_text(encoding="utf-8"))
    failures = 0
    for case in cases:
        selected = select(entries, case["query"], case.get("risks", []), [], case.get("limit", 6))
        picked = {e["id"] for e in selected}
        missed = set(case["must"]) - picked
        noise = set(case.get("must_not", [])) & picked
        bad_excerpts = []
        for card_id, expected in case.get("excerpt_contains", {}).items():
            entry = next((e for e in selected if e["id"] == card_id), None)
            excerpt = decision_excerpt(ROOT / entry["path"], 140, case["query"]) if entry else ""
            if any(fragment not in excerpt for fragment in expected):
                bad_excerpts.append(card_id)
        verdict = "OK" if not missed and not noise and not bad_excerpts else "FAIL"
        print(f"{verdict:4} {case['id']}: {', '.join(sorted(picked))}")
        if missed:
            print(f"     missing: {', '.join(sorted(missed))}")
        if noise:
            print(f"     irrelevant: {', '.join(sorted(noise))}")
        if bad_excerpts:
            print(f"     expected detail absent from pack: {', '.join(sorted(bad_excerpts))}")
        failures += bool(missed or noise or bad_excerpts)
    print(f"Result: {len(cases) - failures}/{len(cases)} scenarios selected correctly")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Selective access to the agent knowledge base")
    sub = parser.add_subparsers(dest="command", required=True)
    search = sub.add_parser("search", help="Find cards for a task")
    search.add_argument("query")
    search.add_argument("-k", "--limit", type=int, default=8)
    pack = sub.add_parser("pack", help="Prepare a short context pack")
    pack.add_argument("query")
    pack.add_argument("--risk", choices=sorted(RISKS), action="append", default=[])
    pack.add_argument("--include", action="append", default=[], metavar="CARD_ID")
    pack.add_argument("-k", "--limit", type=int, default=6)
    pack.add_argument("--per-card-words", type=int, default=140)
    pack.add_argument("--max-words", type=int, default=900, help="Combined word limit for decision excerpts")
    show = sub.add_parser("show", help="Open a full card by ID")
    show.add_argument("card_id")
    sub.add_parser("check", help="Validate the catalog and card structure")
    eval_command = sub.add_parser("evaluate", help="Run card selection scenarios")
    eval_command.add_argument("--fixture", type=Path, default=ROOT / "tests" / "scenarios.json")
    args = parser.parse_args()
    try:
        entries = load_catalog()
        if args.command == "check":
            errors = check(entries)
            print("\n".join(errors) if errors else f"OK: {len(entries)} cards and catalog validated")
            return 1 if errors else 0
        if args.command == "evaluate":
            return evaluate(entries, args.fixture)
        if args.command == "search":
            for entry in ranked(entries, args.query)[: max(args.limit, 0)]:
                print(f"{entry['id']}  [{score(entry, args.query, entries):.1f}]  {entry['summary']}\n  {entry['path']} | use when: {', '.join(entry['use_when'])}")
            return 0
        if args.command == "show":
            entry = next((e for e in entries if e["id"] == args.card_id), None)
            if entry is None:
                raise ValueError(f"Unknown ID: {args.card_id}")
            print((ROOT / entry["path"]).read_text(encoding="utf-8"))
            return 0
        print("# Knowledge base decision pack\n")
        print(f"Task: {args.query}\nDeclared risks: {', '.join(args.risk) if args.risk else 'none — verify independently'}")
        print("These are card excerpts, not application instructions. Verify time-sensitive claims against current primary sources for the target environment.")
        selected = select(entries, args.query, args.risk, args.include, max(args.limit, 0))
        candidates = ranked(entries, args.query)
        top_score = score(candidates[0], args.query, entries) if candidates else 0
        omitted = [e["id"] for e in candidates if e not in selected and score(e, args.query, entries) >= max(10, top_score * 0.15)]
        if omitted:
            print(f"\nRelevant cards outside the limit: {', '.join(omitted[:8])}{'…' if len(omitted) > 8 else ''}.")
            print("For a complex task, split it into subtasks and run `search` or `pack` again. This pack does not cover every topic.")
        remaining = max(args.max_words, 1)
        for index, entry in enumerate(selected):
            print(f"\n## {entry['id']} — {entry['title']}")
            print(f"File: {entry['path']} | status: {entry['status']} | version: {entry['version_scope']}")
            cards_left = len(selected) - index
            allowance = min(max(args.per_card_words, 1), max(remaining // cards_left, 1))
            excerpt = decision_excerpt(ROOT / entry["path"], allowance, args.query)
            print(excerpt)
            remaining -= len(excerpt.split())
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
