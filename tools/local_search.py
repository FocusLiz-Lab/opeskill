#!/usr/bin/env python3
"""Small local search helper for packaged creator archive skills."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TEXT_EXTENSIONS = {".md", ".txt", ".jsonl"}


def tokenize(text: str) -> list[str]:
    raw = re.findall(r"[\w\u4e00-\u9fff]+", text.lower())
    tokens: list[str] = []
    for item in raw:
        tokens.append(item)
        if re.search(r"[\u4e00-\u9fff]", item) and len(item) > 2:
            tokens.extend(item[i : i + 2] for i in range(len(item) - 1))
    return tokens


def iter_files(root: Path):
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
            yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def jsonl_text(line: str) -> str:
    try:
        item = json.loads(line)
    except json.JSONDecodeError:
        return line
    values = []
    for key in ("knowledge", "original", "title", "summary", "use_when", "source_note"):
        value = item.get(key)
        if isinstance(value, str):
            values.append(value)
    for key in ("topics", "skills"):
        value = item.get(key)
        if isinstance(value, list):
            values.extend(str(v) for v in value)
    return "\n".join(values) or line


def make_snippet(text: str, terms: list[str], width: int) -> str:
    lower = text.lower()
    pos = -1
    for term in terms:
        if len(term) < 2:
            continue
        pos = lower.find(term.lower())
        if pos >= 0:
            break
    if pos < 0:
        pos = 0
    start = max(0, pos - width // 3)
    snippet = re.sub(r"\s+", " ", text[start : start + width]).strip()
    return snippet


def search(root: Path, query: str, limit: int, snippet_width: int):
    terms = tokenize(query)
    unique_terms = sorted(set(terms), key=len, reverse=True)
    results = []

    for path in iter_files(root):
        content = read_text(path)
        if not content:
            continue

        candidates: list[tuple[str, int]] = []
        if path.suffix.lower() == ".jsonl":
            for line_no, line in enumerate(content.splitlines(), 1):
                haystack = jsonl_text(line)
                score = score_text(haystack, path.name, unique_terms)
                if score:
                    candidates.append((haystack, score + max(0, 50 - line_no // 20)))
        else:
            score = score_text(content, path.name, unique_terms)
            if score:
                candidates.append((content, score))

        if not candidates:
            continue
        best_text, best_score = max(candidates, key=lambda item: item[1])
        results.append(
            {
                "score": best_score,
                "path": str(path.relative_to(root)),
                "snippet": make_snippet(best_text, unique_terms, snippet_width),
            }
        )

    return sorted(results, key=lambda item: item["score"], reverse=True)[:limit]


def score_text(text: str, title: str, terms: list[str]) -> int:
    haystack = text.lower()
    title_lower = title.lower()
    score = 0
    for term in terms:
        if len(term) < 2:
            continue
        count = haystack.count(term.lower())
        if count:
            score += min(count, 20) * (3 if len(term) > 3 else 1)
        if term.lower() in title_lower:
            score += 25
    return score


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the packaged local knowledge base.")
    parser.add_argument("query")
    parser.add_argument("--root", default="")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--snippet-width", type=int, default=420)
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    root = Path(args.root).resolve() if args.root else script_dir.parent / "知识库"
    if not root.exists():
        raise SystemExit(f"Knowledge root not found: {root}")

    results = search(root, args.query, args.limit, args.snippet_width)
    print(json.dumps({"query": args.query, "root": str(root), "results": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
