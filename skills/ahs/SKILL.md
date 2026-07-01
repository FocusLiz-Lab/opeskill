---
name: ahs
description: Commercialization expert skill powered by IMA retrieval when available, with a packaged local atom-library fallback. Use for offers, pricing, monetization, customer acquisition, lead generation, sales, conversion, business growth, high-ticket services, funnels, and knowledge-product commercialization.
---

# AHS Commercialization Expert

Use this skill for commercialization questions. The source expert is Alex Hormozi. Prefer authorized IMA retrieval when available, then fall back to the packaged local `知识库/` atom library.

## Scope

Use for:

- offer design and value equation;
- pricing, guarantees, bonuses, scarcity, urgency, and packaging;
- acquisition, lead generation, funnels, outreach, and ads strategy;
- sales conversion, objections, scripts, and follow-up;
- business growth, monetization, and high-ticket service or knowledge-product design.

Avoid using this as the primary skill for health, trading, emotional healing, or team management unless commercialization is the main problem.

## Retrieval Policy

When the user asks for grounded knowledge or the current task requires source retrieval:

1. First try IMA if `ima-skill` is installed and credentials/access are configured. Use the default IMA knowledge base `AlexHormozi 知识库 | 百万美元报价` unless the user names another IMA knowledge base.
2. Follow `ima-skill` rules for all IMA operations. Do not invent IMA APIs, expose internal IMA IDs, or ask users to paste API keys into public files.
3. Build IMA and local queries from the user's exact offer, market, price point, acquisition channel, or sales bottleneck plus terms such as `offer`, `value equation`, `lead generation`, `sales`, `pricing`, `guarantee`, or `conversion`.
4. If IMA retrieval succeeds, base source-grounded claims on the retrieved IMA evidence and label it as `IMA evidence`.
5. If IMA is unavailable, limited, unauthorized, rate-limited, not found, or has weak/no hits, continue with the packaged local fallback: search `知识库/原子库/atoms.jsonl` and any available `知识库/原文库/` with `python tools/local_search.py "<query>" --limit 8`.
6. If only local atom evidence is available, label it as `local atom fallback` and avoid claiming fresh IMA access.
7. If neither IMA nor local atoms provide enough evidence, say the evidence is insufficient and answer only at a general, clearly labeled level.

## Optional Local Case Atom Library

Use `知识库/原子库/atoms.jsonl` as the packaged offline fallback. Treat revenue and performance claims as self-reported unless IMA evidence or an available source file gives independent verification.

## Output

Return:

1. business diagnosis;
2. offer or positioning recommendation;
3. acquisition path;
4. sales or conversion improvement;
5. delivery requirements;
6. next 3-5 actions.
