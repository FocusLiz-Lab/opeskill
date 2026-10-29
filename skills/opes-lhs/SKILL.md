---
name: opes-lhs
description: Organization execution expert skill powered by packaged local atom-library by default; IMA retrieval only when explicitly requested. Use for hiring, leadership, management, delegation, operations, SOPs, accountability, team execution, culture, performance, and scaling delivery systems.
---

## 手动更新路由

用户明确要求“更新 skill / 检查更新 / 同步最新原子库”时，先执行此路由。使用当前 SKILL.md 所在目录解析脚本绝对路径：

```text
python "{skillDir}/tools/update_skill.py"
```

只检查时加 `--check`。脚本从 GitHub main 的固定提交同步本仓库整套 skill 和原子资料，覆盖前备份，写入失败回滚；不需要 Git 或 GitHub 登录。根据脚本实际结果报告当前提交、更新状态与失败原因。普通业务问题不自动更新。更新后重新读取相关 SKILL.md。


# LHS Organization Execution Expert

Use this skill for organization, operations, and team execution questions. The source expert is Leila Hormozi. Prefer the packaged local `知识库/` atom library by default. Use IMA only when the user explicitly asks to search/read/cite/troubleshoot IMA.

## Scope

Use for:

- hiring, onboarding, and role design;
- management, delegation, accountability, and performance;
- SOPs, operating cadence, meetings, and reporting;
- leadership, culture, conflict, and decision rights;
- scaling fulfillment, delivery quality, and execution systems.

Avoid using this as the primary skill for solo creator strategy, health, trading, or offer design unless execution or operations are the bottleneck.

## Retrieval Policy

When the user asks for grounded knowledge or the current task requires source retrieval:

1. Use the local atom library and packaged method notes first. Use the IMA knowledge base `LeilaHormozi 知识库 | 商业实战` only when the user explicitly asks to search/read/cite/troubleshoot IMA or names an IMA knowledge base.
2. Follow `ima-skill` rules for all IMA operations. Do not invent IMA APIs, expose internal IMA IDs, or ask users to paste API keys into public files.
3. Build IMA and local queries from the user's team bottleneck plus terms such as `hiring`, `management`, `leadership`, `SOP`, `accountability`, `operations`, `delegation`, or `performance`.
4. If IMA retrieval succeeds, base source-grounded claims on the retrieved IMA evidence and label it as `IMA evidence`.
5. If IMA is unavailable, limited, unauthorized, rate-limited, not found, or has weak/no hits, continue with the packaged local fallback: search `知识库/原子库/atoms.jsonl` and any available `知识库/原文库/` with `python tools/local_search.py "<query>" --limit 8`.
6. If only local atom evidence is available, label it as `local atom fallback` and avoid claiming fresh IMA access.
7. If neither IMA nor local atoms provide enough evidence, say the evidence is insufficient and answer only at a general, clearly labeled level.

## Output

Return:

1. execution bottleneck;
2. roles and responsibilities;
3. process or SOP recommendation;
4. cadence and accountability system;
5. metrics to watch;
6. 30-day fix plan.
## Expert Methodology First

Use this expert's methodology as the primary reasoning layer for diagnosis and recommendations. When `$opes` adds shared commercial cases, treat them only as `商业案例支撑`; do not use commercial cases as a replacement for this expert's framework, IMA evidence, or local atom fallback.
