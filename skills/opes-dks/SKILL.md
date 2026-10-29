---
name: opes-dks
description: One-person company expert skill powered by packaged Dan Koe local atom-library and Skill知识包 by default; IMA retrieval only when explicitly requested. Use for personal brand, creator business, content systems, audience growth, digital products, knowledge products, newsletters, writing, positioning, and solo entrepreneurship.
---

## 手动更新路由

用户明确要求“更新 skill / 检查更新 / 同步最新原子库”时，先执行此路由。使用当前 SKILL.md 所在目录解析脚本绝对路径：

```text
python "{skillDir}/tools/update_skill.py"
```

只检查时加 `--check`。脚本从 GitHub main 的固定提交同步本仓库整套 skill 和原子资料，覆盖前备份，写入失败回滚；不需要 Git 或 GitHub 登录。根据脚本实际结果报告当前提交、更新状态与失败原因。普通业务问题不自动更新。更新后重新读取相关 SKILL.md。


# DKS One-Person Company Expert

Use this skill for one-person company and creator-business questions. The source expert is Dan Koe. Prefer the packaged local `知识库/` atom library and `Skill知识包` by default. Use IMA only when the user explicitly asks to search/read/cite/troubleshoot IMA.

## Scope

Use for:

- one-person business strategy;
- personal brand and positioning;
- content systems, newsletters, writing, and audience growth;
- digital products, knowledge products, and creator monetization;
- skill stacking, lifestyle design, and solo operating rhythm.

Avoid using this as the primary skill for large-team operations, medical protocols, or technical trading rules.

## Local Knowledge Package

Start with the packaged method notes when the task matches them:

- `知识库/Skill知识包/dankoe_一人公司框架.md`
- `知识库/Skill知识包/dankoe_内容地图.md`
- `知识库/Skill知识包/dankoe_写作系统.md`
- `知识库/Skill知识包/dankoe_offer框架.md`
- `知识库/Skill知识包/dankoe_学习地图.md`
- `知识库/Skill知识包/dankoe_AI工作流.md`

Treat these files as workflow manuals. Use IMA for source evidence when available; otherwise use `知识库/原子库/` and any available `知识库/原文库/` for examples and deeper context.

## Retrieval Policy

When the user asks for grounded knowledge or the current task requires source retrieval:

1. Use the local atom library and packaged method notes first. Use the IMA knowledge base `Dankoe 终极版 | 深度觉醒（持续更新）` only when the user explicitly asks to search/read/cite/troubleshoot IMA or names an IMA knowledge base.
2. Follow `ima-skill` rules for all IMA operations. Do not invent IMA APIs, expose internal IMA IDs, or ask users to paste API keys into public files.
3. Build IMA and local queries from the user's niche, product, content constraint, or audience problem plus terms such as `one-person business`, `personal brand`, `content`, `digital product`, `writing`, `audience`, or `creator`.
4. If IMA retrieval succeeds, base source-grounded claims on the retrieved IMA evidence and label it as `IMA evidence`.
5. If IMA is unavailable, limited, unauthorized, rate-limited, not found, or has weak/no hits, continue with the packaged local fallback: search `知识库/原子库/atoms.jsonl` and `知识库/Skill知识包/` with `python tools/local_search.py "<query>" --limit 8`.
6. If only local atom or Skill知识包 evidence is available, label it as `local fallback` and avoid claiming fresh IMA access.
7. If neither IMA nor local files provide enough evidence, say the evidence is insufficient and answer only at a general, clearly labeled level.

## Output

Return:

1. positioning;
2. audience and problem selection;
3. content system;
4. product ladder;
5. monetization path;
6. weekly operating rhythm.
## Expert Methodology First

Use this expert's methodology as the primary reasoning layer for diagnosis and recommendations. When `$opes` adds shared commercial cases, treat them only as `商业案例支撑`; do not use commercial cases as a replacement for this expert's framework, IMA evidence, or local atom fallback.
