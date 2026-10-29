---
name: opes-update
description: 手动检查并更新 超级个体 的 opeskill 整套 skill 和原子资料。用户调用 $opes-update、/opes-update 或明确要求升级该工具箱时使用。
---

# 超级个体 更新

调用 `$opes-update` 时直接执行更新，无需补充参数。将 `{skillDir}` 解析为当前 SKILL.md 所在目录，运行：

```text
python "{skillDir}/tools/update_skill.py"
```

用户只要求检查更新时追加 `--check`，不下载或写入文件。自定义安装位置时，可用 `--skills-dir` 指向各 skill 文件夹的共同父目录。

脚本检查 `FocusLiz-Lab/opeskill` 的 GitHub main 提交，同步对应整套 skill、当前更新入口自身及原子资料。覆盖前备份，写入失败回滚；无需安装 Git 或登录 GitHub。商业案例库统一使用共享目录；专家工具箱不会重复安装共享案例数据。

根据脚本返回的 `status`、`commit`、`changed` 和 `backup` 报告结果。执行失败时说明实际原因，不宣称更新成功。更新成功后重新读取本次需要使用的 SKILL.md；若宿主尚未发现新 skill，提示刷新技能列表或重新打开会话。普通业务请求继续使用 `$opes`。
