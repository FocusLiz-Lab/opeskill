# opeskill 超级个体工具箱

opeskill 是一个面向超级个体的 Codex Claude Code等智能体 Skills 工具箱，用 7 位专家模型和共享中文商业案例库，帮助个人创作者、咨询顾问、自由职业者和小团队把能力转成可销售的产品、内容、获客系统和长期资产。

它适合用来处理这些问题：

- 设计 offer、定价、成交路径和商业化模型。
- 搭建一人公司、个人品牌、内容系统和数字产品。
- 用中文商业案例验证项目、平台打法、私域转化和交付模式。
- 处理招聘、管理、SOP、团队执行和增长运营。
- 做长期方向判断、杠杆选择、精力管理、行动启动和交易风控。

opeskill 采用“IMA 优先，本地原子库兜底”的方式：

1. 普通问题默认读取本地专家原子库和 Skill 知识包；只有用户主动要求 IMA 检索、引用或排错时，才读取对应 IMA 知识库。
2. 如果 IMA 未安装、无权限、限额、找不到知识库或没有有效命中，skill 会使用本地原子库兜底。
3. SkillHub 上传包是轻量包，内置下载工具；全量专家原子库可由 `$opes-download-atoms` 自动从 GitHub 下载、解压并安装。商业案例库由共享 `$commercial-case-library` 下载一次后复用。
<img width="2752" height="1536" alt="AI_专家决策系统架构" src="https://github.com/user-attachments/assets/a1f2a5e4-d8a6-4484-8040-71d5d2f1daa0" />

## 超级个体知识库合集

扫码获取知识库：

![知识库二维码](docs/knowledge-base-qrcode.png?v=20260705)

## 如何安装

通用安装方式（适用于 Codex / Claude Code / OpenClaw / Hermes等智能体）：

```bash
npx -y skills add FocusLiz-Lab/opeskill -g --all
```

也可以从 GitHub Releases 下载 `opes-local.zip`，解压后将其中的 skill 上传到支持 Skills 的客户端。

```text
https://github.com/FocusLiz-Lab/opeskill/releases
```

## 工具箱

| Skill | 做什么 |
|---|---|
| `$opes` | 主入口，按问题自动路由 7 位专家和商业案例库 |
| `$opes-download-atoms` | 下载、解压并安装全量 7 人专家原子库 |
| `$ahs` | Alex Hormozi：offer、定价、获客、销售、商业化 |
| `$lhs` | Leila Hormozi：招聘、管理、运营、SOP、团队执行 |
| `$dks` | Dan Koe：一人公司、个人品牌、内容系统、数字产品 |
| `$nrs` | Naval Ravikant：财富判断、杠杆、长期主义 |
| `$hbs` | Huberman Lab：睡眠、专注、压力、精力、习惯 |
| `$mrs` | Mel Robbins：行动力、拖延、自信、习惯启动 |
| `$rts` | Rayner Teo：交易系统、趋势、价格行为、风控 |

## 仓库结构

```text
opes/
├── SKILL.md
├── agents/
├── references/
├── tools/
│   ├── local_search.py
│   ├── search_commercial_atoms.py
│   └── download_full_atoms.py
├── docs/
│   └── knowledge-base-qrcode.png
└── 知识库/
    ├── 原子库/
    │   ├── ahs/
    │   ├── lhs/
    │   ├── dks/
    │   ├── nrs/
    │   ├── hbs/
    │   ├── mrs/
    │   └── rts/
    ├── Skill知识包/
    │   ├── ahs/
    │   ├── lhs/
    │   ├── dks/
    │   ├── nrs/
    │   ├── hbs/
    │   ├── mrs/
    │   └── rts/
```

## 原子库格式

所有 `atoms*.jsonl` 文件都是一行一条 JSON 记录，核心字段如下：

```json
{"id":"2024Q4_001","knowledge":"提炼后的知识点","original":"来源片段","url":"https://...","date":"2024-10-01","topics":["offer","pricing"],"skills":["opes"],"type":"case","confidence":"high"}
```

专家原子库按专家分目录存放，例如 `知识库/原子库/ahs/atoms_2024Q4.jsonl`。商业案例库使用同样格式，但放在共享 `$commercial-case-library` 的 `~/.agents/shared/commercial-case-library/知识库/商业案例库/` 中。

## 怎么用

### 作为 RAG 知识库

把 `知识库/原子库/{专家代码}/atoms.jsonl` 和共享商业案例库的 `atoms.jsonl` 导入向量数据库。按 `topics`、`skills`、`type` 过滤即可。

### 只读方法论

直接阅读 `知识库/Skill知识包/` 下对应专家目录。每个目录都可独立作为 system prompt 或工作流参考。

### 检索本地知识

```powershell
python tools/local_search.py "高客单 offer 成交"
python tools/search_commercial_atoms.py "小红书 高客单 成交" --limit 10
```

## 许可证

本项目知识库仅用于学习、研究和非商业用途。引用或二次发布时请注明来源；商业用途请联系作者授权。
