---
name: opes-download-atoms
description: 下载、解压并安装 opeskill 全量本地专家原子库。用于安装 SkillHub 轻量包后，从 GitHub main 自动拉取 最新仓库数据，并安装 7 位专家原子库。商业案例库已抽离为共享依赖 `$commercial-case-library`，不要在本 skill 内重复下载。
---

# 下载或更新 Skill 与完整原子库

用户要求下载、补全、更新或修复原子库时，运行当前 skill 目录中的脚本：

```text
python "{skillDir}/tools/update_skill.py"
```

加 `--check` 仅检查。它检查 GitHub main 当前提交，并同步本仓库整套 skill 及专家原子库；覆盖前备份，写入失败回滚。普通业务问题不自动更新。以实际执行结果报告更新状态，更新后重新读取相关 SKILL.md。旧 `tools/download_full_atoms.py` 入口兼容同一流程。

商业案例仍使用共享 `$commercial-case-library`，不重复安装到专家工具箱内。
