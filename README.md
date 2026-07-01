# Creator Brain Skills 本地知识库包

这是一个面向 Codex/ChatGPT Skills 的 7 人专家知识库包。它采用“IMA 优先，本地原子库兜底”的方式：

1. 如果用户已安装并配置 `ima-skill`，且你已授权 TA 访问对应 IMA 知识库，skill 会优先读取 IMA。
2. 如果 IMA 未安装、无权限、限额、找不到知识库或没有有效命中，skill 会自动使用 zip 包内的本地原子库。
3. `creator-brain-local.zip` 已内置中文商业案例原子库，涉及商业化、变现、offer、定价、获客、成交、验证时，会自动作为“商业案例支撑”使用。

## 包清单

所有 zip 包在 GitHub Releases 中下载：

```text
https://github.com/FocusLiz-Lab/creator-brain-skills/releases
```

| 文件 | 用途 |
| --- | --- |
| `creator-brain-local.zip` | 7 人总路由 skill，内置商业案例原子库 |
| `ahs-local.zip` | Alex Hormozi 商业化、offer、定价、获客、销售 |
| `dks-local.zip` | Dan Koe 一人公司、个人品牌、内容系统、数字产品 |
| `hbs-local.zip` | Huberman Lab 睡眠、专注、压力、健康表现 |
| `lhs-local.zip` | Leila Hormozi 组织执行、招聘、管理、SOP |
| `mrs-local.zip` | Mel Robbins 行动力、自信、拖延、自我改变 |
| `nrs-local.zip` | Naval Ravikant 财富、杠杆、判断力、长期主义 |
| `rts-local.zip` | Rayner Teo 交易系统、趋势、价格行为、风控 |

## 安装方式

到 Releases 下载需要的 zip，解压到你的 Codex skills 目录。

Windows 示例：

```text
C:\Users\你的用户名\.codex\skills\creator-brain
C:\Users\你的用户名\.codex\skills\ahs
C:\Users\你的用户名\.codex\skills\dks
```

建议至少安装：

```text
creator-brain-local.zip
ahs-local.zip
dks-local.zip
```

如果想使用完整 7 人模式，则安装全部 8 个 zip。

## 默认 IMA 知识库名

| skill | 默认 IMA 知识库 |
| --- | --- |
| `ahs` | `AlexHormozi 知识库 \| 百万美元报价` |
| `dks` | `Dankoe 终极版 | 深度觉醒（持续更新）` |
| `hbs` | `Huberman知识库｜科学改善生活（持续更新）` |
| `lhs` | `LeilaHormozi 知识库 \| 商业实战` |
| `mrs` | `MelRobbins 知识库 \| 自我改变` |
| `nrs` | `纳瓦尔知识库 \| 复利思维` |
| `rts` | `RaynerTeo交易知识库 \| 顺势而为` |

如果用户在提问中明确指定了其他 IMA 知识库名，则优先使用用户指定的名称。

## 使用示例

```text
用 creator-brain 帮我设计一个小红书高客单知识付费项目
```

```text
用 ahs 分析我的 offer 和定价
```

```text
用 dks 帮我搭建一人公司内容系统
```

```text
用 creator-brain 七人模式，帮我做一个个人 IP 商业化路线图
```

## 商业案例支撑

`creator-brain-local.zip` 内置：

```text
知识库/商业案例库/commercial_atoms.jsonl
tools/search_commercial_atoms.py
```

当问题涉及商业化、变现、offer、定价、获客、成交、验证、中文市场案例时，会检索本地商业案例原子库。

示例检索命令：

```powershell
python tools/search_commercial_atoms.py "小红书 高客单 成交" --atoms "知识库/商业案例库/commercial_atoms.jsonl" --limit 8
```

商业案例只作为“商业案例支撑”，不等同于专家方法论。收入、GMV、ROI 等数据默认视为案例自述，不能当作收益保证。

## 公开包边界

本仓库上传的是 lite 包：

- 包含本地原子库
- 包含必要搜索工具
- 包含 skill 说明
- 不包含原始 IMA 凭证
- 不包含完整原文库
- 不包含年份文章目录

这意味着别人可以直接本地使用；如果 TA 有 IMA 授权，就优先读取 IMA；如果没有，也能用本地原子库继续工作。

## 更新包

本仓库 Releases 中的 zip 是生成后的发布包。如果你维护源数据，需要在本地重新构建原子库和 zip 后再上传。

核心原则：

```text
使用时：IMA 优先，本地原子库兜底
发布时：只发 lite 包，不发原文库和凭证
```
