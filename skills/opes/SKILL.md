---
name: opes
description: opeskill 超级个体工具箱总入口。用于商业化、offer、定价、获客、销售、一人公司、创作者商业、个人品牌、内容、领导力、运营、招聘、财富判断、杠杆、健康、睡眠、专注、拖延、行动改变、自信、交易系统和风险管理。默认优先使用授权 IMA 检索；IMA 不可用时使用本地原子库兜底。安装 SkillHub 轻量包后，可调用 $opes-download-atoms 下载、解压并安装全量 7 人原子库和商业案例库。
---

# opes 超级个体工具箱

这是 opeskill 的总入口，负责在 7 位专家 skill 和中文商业案例库之间做路由、编排和综合判断。

SkillHub 上传包是轻量包，不直接内置全量大原子库。对于需要资料依据的回答，优先使用授权 IMA 检索；如果 IMA 不可用、无权限、限额、找不到知识库或没有有效命中，再使用本地原子库兜底。

如果本地原子库缺失，先调用 `$opes-download-atoms`，或运行：

```powershell
python tools/download_full_atoms.py
```

它会从 GitHub Release 下载 `opes-local.zip`，并解压安装：

```text
知识库/原子库/{ahs,dks,hbs,lhs,mrs,nrs,rts}/atoms.jsonl
知识库/商业案例库/atoms.jsonl
```

不要把 IMA 作为唯一来源。能用 IMA 时优先 IMA；不能用时，使用已经安装的本地原子库和 `知识库/Skill知识包/` 方法说明。

## 默认 IMA 知识库

除非用户明确指定其他 IMA 知识库，否则默认使用这些名称：

| skill | default IMA knowledge base |
| --- | --- |
| `ahs` | `AlexHormozi 知识库 | 百万美元报价` |
| `dks` | `Dankoe 终极版 | 深度觉醒（持续更新）` |
| `hbs` | `Huberman知识库｜科学改善生活（持续更新）` |
| `lhs` | `LeilaHormozi 知识库 | 商业实战` |
| `mrs` | `MelRobbins 知识库 | 自我改变` |
| `nrs` | `纳瓦尔知识库 | 复利思维` |
| `rts` | `RaynerTeo交易知识库 | 顺势而为` |

如果默认 IMA 知识库没有找到，不要停止任务。说明 IMA 未命中，然后继续使用对应本地 `知识库/原子库/atoms.jsonl`。

## Core Workflow

1. Identify the user's outcome, constraint, and domain.
2. Select one primary child skill and up to two supporting child skills.
3. Read `references/experts.yaml` for the expert map.
4. Read `references/routing-rules.md` when routing is uncertain or the request spans domains.
5. Use the selected child skills when available.
6. Each selected child skill must use its own retrieval rule:
   - try its default IMA knowledge base first when IMA is available;
   - fall back to packaged `知识库/原子库/atoms.jsonl` if IMA fails or has no useful hits;
   - use `知识库/Skill知识包/` first when that child package provides method notes.
7. If a required child skill is not installed, say which local package is missing and continue only with installed modules if that still gives a useful answer.
8. Synthesize retrieved evidence using `references/synthesis-rules.md`.
9. Format the final answer using `references/output-formats.md`.

## Child Skill Map

- `opes-download-atoms`: download, extract, and install the full local atom libraries and commercial case library from GitHub Releases.
- `ahs`: commercialization expert powered by packaged Alex Hormozi local knowledge. Use for offers, pricing, monetization, acquisition, sales, conversion, lead generation, and business growth.
- `lhs`: organization execution expert powered by packaged Leila Hormozi local knowledge. Use for hiring, management, leadership, SOPs, operations, delegation, accountability, and team execution.
- `dks`: one-person company expert powered by packaged Dan Koe local knowledge. Use for personal brand, creator business, content systems, digital products, knowledge products, and solo entrepreneurship.
- `nrs`: wealth judgment expert powered by packaged Naval Ravikant local knowledge. Use for leverage, wealth, long-term games, direction choice, judgment, opportunity cost, and specific knowledge.
- `hbs`: mind-body performance expert powered by packaged Huberman Lab local knowledge. Use for sleep, focus, stress, energy, routines, habits, and neuroscience-informed performance.
- `mrs`: action change expert powered by packaged Mel Robbins local knowledge. Use for procrastination, confidence, fear, emotional reset, self-change, and immediate action.
- `rts`: trading system expert powered by packaged Rayner Teo local knowledge. Use for trading, price action, trends, market structure, risk management, backtesting, and trading psychology.

## Routing Modes

Default to the narrowest useful routing.

- Quick mode: select one child skill when the request is clearly inside one domain.
- Synthesis mode: select two or three child skills when the request has a primary domain plus an execution, strategy, health, or monetization dependency.
- Seven-expert mode: select all seven child skills only when the user explicitly asks for "all seven", "seven-expert mode", "所有知识库", "七人模式", "完整系统", or a full life/business roadmap.

## Retrieval Rule

When `$opes` is invoked:

1. Use each selected child skill's own IMA-first, local-fallback retrieval instructions.
2. Do not search all seven modules by default.
3. Use at least one relevant source from the primary module before presenting the answer as source-grounded. Prefer IMA evidence; if IMA is unavailable, use local atom fallback evidence.
4. For synthesis mode, retrieve at least one relevant source from each selected module when available.
5. Cite the expert module used in the answer, such as "商业化专家 ahs" or "一人公司专家 dks".
6. If a child package is missing, say the exact package name to install, such as `dks-local.zip`.
7. If IMA and local sources are both insufficient, label that part as inference rather than source-grounded.

## Commercial Case Support

When the user asks for business cases, Chinese-market examples, practical project examples, monetization cases, validation examples, or any commercialization topic where case evidence would improve the answer:

1. Use the selected expert modules for the method and diagnosis.
2. Use the bundled local commercial case atom library for case support:

```powershell
python tools/search_commercial_atoms.py "{query}" --atoms "知识库/商业案例库/atoms.jsonl" --limit 8
```

3. Build case queries from the user's platform, audience, offer, price point, acquisition channel, business model, and bottleneck. Examples: `小红书 高客单 成交`, `知识付费 私域 交付`, `AI 工具 变现`, `抖音 获客 转化`.
4. Do not treat commercial cases as the expert source. Label them as "商业案例支撑".
5. Separate `可复制动作` from `不可复制条件`, and treat revenue, GMV, ROI, and performance claims as self-reported unless independently verified.
6. If the bundled commercial case atom library is missing or has weak/no hits, continue without case support and say that this part is inference.

## Synthesis Requirements

Always produce one integrated recommendation, not disconnected expert summaries.

Include:

1. direct conclusion;
2. selected modules and why;
3. strongest retrieved or expert-grounded insights;
4. synthesized action plan;
5. risks, tradeoffs, or conflicts;
6. next actions.

When experts conflict, preserve the tradeoff. For example, `ahs` may optimize for revenue now, while `nrs` may warn about low-leverage work; `dks` may prefer solo leverage, while `lhs` may recommend team systems once operational complexity rises.

## Safety Boundaries

- For health topics, treat `hbs` output as educational and encourage professional medical help for diagnosis, treatment, medication, severe symptoms, or emergencies.
- For trading topics, treat `rts` output as educational and avoid personalized financial advice or guaranteed returns.
- For business topics, separate strategy from assumptions and identify what should be validated in the market.
