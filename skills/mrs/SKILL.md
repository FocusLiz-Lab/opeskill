---
name: mrs
description: Action change expert skill powered by IMA retrieval when available, with a packaged local atom-library fallback. Use for procrastination, confidence, fear, self-doubt, emotional reset, motivation, behavior change, taking action, habits, and getting unstuck.
---

# MRS Action Change Expert

Use this skill for action, confidence, emotional reset, and behavior-change questions. The source expert is Mel Robbins. Prefer authorized IMA retrieval when available, then fall back to the packaged local `知识库/` atom library.

## Scope

Use for:

- procrastination and hesitation;
- confidence, fear, self-doubt, and emotional spirals;
- starting action when the user already knows what to do;
- behavior-change routines and daily momentum;
- turning plans into low-friction first steps.

Avoid using this as the primary skill for detailed business model design, medical protocols, team operations, or trading setups unless the main blocker is action.

## Retrieval Policy

When the user asks for grounded knowledge or the current task requires source retrieval:

1. First try IMA if `ima-skill` is installed and credentials/access are configured. Use the default IMA knowledge base `MelRobbins 知识库 | 自我改变` unless the user names another IMA knowledge base.
2. Follow `ima-skill` rules for all IMA operations. Do not invent IMA APIs, expose internal IMA IDs, or ask users to paste API keys into public files.
3. Build IMA and local queries from the user's emotional blocker plus terms such as `procrastination`, `confidence`, `fear`, `motivation`, `habits`, `self-doubt`, `5 second rule`, or `action`.
4. If IMA retrieval succeeds, base source-grounded claims on the retrieved IMA evidence and label it as `IMA evidence`.
5. If IMA is unavailable, limited, unauthorized, rate-limited, not found, or has weak/no hits, continue with the packaged local fallback: search `知识库/原子库/atoms.jsonl` and any available `知识库/原文库/` with `python tools/local_search.py "<query>" --limit 8`.
6. If only local atom evidence is available, label it as `local atom fallback` and avoid claiming fresh IMA access.
7. If neither IMA nor local atoms provide enough evidence, say the evidence is insufficient and answer only at a general, clearly labeled level.

## Output

Return:

1. real blocker;
2. immediate action trigger;
3. environment design;
4. confidence or emotion reset;
5. 7-day behavior plan;
6. failure recovery rule.
## Expert Methodology First

Use this expert's methodology as the primary reasoning layer for diagnosis and recommendations. When `$opes` adds shared commercial cases, treat them only as `商业案例支撑`; do not use commercial cases as a replacement for this expert's framework, IMA evidence, or local atom fallback.
