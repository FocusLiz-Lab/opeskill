#!/usr/bin/env python
"""Search the generated commercial atom library."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def default_atoms() -> Path:
    env_path = os.environ.get("SCYS_COMMERCIAL_ATOMS")
    if env_path:
        return Path(env_path).expanduser().resolve()
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "知识库" / "商业案例库" / "atoms.jsonl"
        if candidate.exists():
            return candidate
        candidate = parent / "_atoms" / "commercial_atoms.jsonl"
        if candidate.exists():
            return candidate
        candidate = parent / "知识库" / "商业案例库" / "commercial_atoms.jsonl"
        if candidate.exists():
            return candidate
    return Path.cwd() / "_atoms" / "commercial_atoms.jsonl"


def terms(query: str) -> list[str]:
    return [t for t in re.split(r"[\s,，、|/]+", query.strip()) if t]


def load_atoms(path: Path):
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def atom_text(atom: dict) -> str:
    parts = [
        atom.get("title", ""),
        atom.get("heading", ""),
        atom.get("knowledge", ""),
        atom.get("original", ""),
        atom.get("summary", ""),
        atom.get("evidence", ""),
        " ".join(atom.get("commercial_stages") or []),
        " ".join(atom.get("platforms") or []),
        " ".join(atom.get("project_types") or []),
    ]
    return " ".join(parts).lower()


def match_filter(values: list[str], wanted: str | None) -> bool:
    if not wanted:
        return True
    wanted_items = [x.strip() for x in wanted.split(",") if x.strip()]
    return any(w in values for w in wanted_items)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="keyword query")
    parser.add_argument("--atoms", default=str(default_atoms()), help="commercial_atoms.jsonl path")
    parser.add_argument("--stage", default=None, help="comma-separated stage filter, e.g. offer,acquisition")
    parser.add_argument("--platform", default=None, help="comma-separated platform filter, e.g. 小红书,抖音")
    parser.add_argument("--project", default=None, help="comma-separated project type filter")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    atoms_path = Path(args.atoms).resolve()
    query_terms = terms(args.query)
    results = []
    for atom in load_atoms(atoms_path):
        if not match_filter(atom.get("commercial_stages") or [], args.stage):
            continue
        if not match_filter(atom.get("platforms") or [], args.platform):
            continue
        if not match_filter(atom.get("project_types") or [], args.project):
            continue
        haystack = atom_text(atom)
        hits = [t for t in query_terms if t.lower() in haystack]
        if not hits:
            continue
        score = int(atom.get("score") or 0) + len(hits) * 5
        row = dict(atom)
        row["_search_score"] = score
        results.append(row)

    results.sort(key=lambda x: x.get("_search_score", 0), reverse=True)
    results = results[: args.limit]

    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    for i, atom in enumerate(results, 1):
        src = atom.get("source") or {}
        print(f"{i}. [{atom.get('_search_score')}] {atom.get('title')}")
        print(f"   id: {atom.get('id') or atom.get('atom_id')}")
        print(f"   stages: {', '.join(atom.get('commercial_stages') or [])}")
        print(f"   platforms: {', '.join(atom.get('platforms') or [])}")
        print(f"   projects: {', '.join(atom.get('project_types') or [])}")
        metrics = atom.get("metrics") or []
        if metrics:
            print(f"   metrics: {', '.join(metrics)}")
        print(f"   file: {src.get('file')}")
        print(f"   evidence: {atom.get('original') or atom.get('evidence')}")
        print()


if __name__ == "__main__":
    main()
