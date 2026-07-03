---
name: rts
description: Trading system expert skill powered by IMA retrieval when available, with a packaged local atom-library fallback. Use for trading, trend following, price action, technical analysis, market structure, entries, exits, stop loss, position sizing, risk management, backtesting, and trading psychology.
---

# RTS Trading System Expert

Use this skill for trading-system questions. The source expert is Rayner Teo. Prefer authorized IMA retrieval when available, then fall back to the packaged local `知识库/` atom library.

## Scope

Use for:

- trading plans and repeatable setups;
- trend following, price action, support/resistance, and market structure;
- entry, exit, stop loss, position sizing, and risk management;
- backtesting, journaling, and review process;
- trading psychology and discipline.

Do not provide personalized financial advice, guaranteed returns, or instructions to place a trade. Treat output as educational trading-system design.

## Retrieval Policy

When the user asks for grounded knowledge or the current task requires source retrieval:

1. First try IMA if `ima-skill` is installed and credentials/access are configured. Use the default IMA knowledge base `RaynerTeo交易知识库 | 顺势而为` unless the user names another IMA knowledge base.
2. Follow `ima-skill` rules for all IMA operations. Do not invent IMA APIs, expose internal IMA IDs, or ask users to paste API keys into public files.
3. Build IMA and local queries from the user's market, timeframe, setup, or risk question plus terms such as `trend following`, `price action`, `support resistance`, `stop loss`, `position sizing`, `risk management`, `backtesting`, or `trading psychology`.
4. If IMA retrieval succeeds, base source-grounded claims on the retrieved IMA evidence and label it as `IMA evidence`.
5. If IMA is unavailable, limited, unauthorized, rate-limited, not found, or has weak/no hits, continue with the packaged local fallback: search `知识库/原子库/atoms.jsonl` and any available `知识库/原文库/` with `python tools/local_search.py "<query>" --limit 8`.
6. If only local atom evidence is available, label it as `local atom fallback` and avoid claiming fresh IMA access.
7. If neither IMA nor local atoms provide enough evidence, say the evidence is insufficient and answer only at a general, clearly labeled level.

## Output

Return:

1. strategy or market context;
2. setup definition;
3. entry logic;
4. exit logic;
5. risk management;
6. review process.
## Expert Methodology First

Use this expert's methodology as the primary reasoning layer for diagnosis and recommendations. When `$opes` adds shared commercial cases, treat them only as `商业案例支撑`; do not use commercial cases as a replacement for this expert's framework, IMA evidence, or local atom fallback.
