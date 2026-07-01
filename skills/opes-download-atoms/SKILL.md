---
name: opes-download-atoms
description: 下载、解压并安装 opeskill 全量本地原子库。用于安装 SkillHub 轻量包后，从 GitHub Release 自动拉取 `opes-local.zip`，并安装 7 位专家原子库和中文商业案例库。
---

# opes-download-atoms 全量原子库安装

当用户要求下载、补全、更新、修复或安装 opeskill 全量原子库时，运行：

```powershell
python tools/download_full_atoms.py
```

这个工具会自动完成：

1. 从 GitHub Release 下载 `opes-local.zip`。
2. 解压 `知识库/原子库/` 下 7 位专家原子库。
3. 解压 `知识库/商业案例库/` 下中文商业案例库。
4. 安装到当前 opeskill 目录。

安装完成后，应存在：

```text
知识库/原子库/ahs/atoms.jsonl
知识库/原子库/dks/atoms.jsonl
知识库/原子库/hbs/atoms.jsonl
知识库/原子库/lhs/atoms.jsonl
知识库/原子库/mrs/atoms.jsonl
知识库/原子库/nrs/atoms.jsonl
知识库/原子库/rts/atoms.jsonl
知识库/商业案例库/atoms.jsonl
```
