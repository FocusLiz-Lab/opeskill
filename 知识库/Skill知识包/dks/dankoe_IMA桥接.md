# Dankoe 默认 IMA 检索方法

## 定位

IMA 是资料库和检索层。Dankoe skills 是方法论和工作流层。整套 Dankoe skills 默认使用同一个 IMA 知识库作为资料来源；`dankoe-ima` 只是显式检索、排错或桥接说明入口。

组合方式：

```text
IMA search/read -> evidence summary -> Dankoe workflow -> final output
```

不要让 Dankoe skills 假装拥有完整资料。需要 Dankoe 原始资料时，默认先用 IMA 检索；IMA 不可用时才退回本仓库抽象知识包。

## 默认知识库

默认知识库名：

```text
Dankoe 终极版 | 深度觉醒（持续更新）
```

用户可以替换为自己的知识库名称。

用户调用任意 Dankoe workflow skill 时，不需要每次都说“先从 Dankoe 终极版 | 深度觉醒（持续更新）里找资料”。只要没有明确指定其他知识库，就默认自动使用这个知识库。

默认知识库可用时直接使用。用户如果只给了模糊名称，搜索到多个同名或相似知识库时，不要自动选择内容最多或排名最靠前的库。必须列出可见名称，让用户确认使用哪一个。

## IMA 安装与凭证

如果用户没有安装 IMA skill，提示：

```text
请安装 ima 技能
下载地址：https://app-dl.ima.qq.com/skills/ima-skills-1.1.7.zip
API Key 获取：https://ima.qq.com/agent-interface
```

凭证必须通过 IMA 官方 skill / 官方配置流程保存。不要把 API Key 写进仓库、README、公开截图或聊天记录。

## 路由规则

- 从哪里开始学、先看哪些、学习答疑 -> `dankoe-learning-map`
- 写公众号、朋友圈、小红书、Newsletter、脚本 -> `dankoe-writing`
- 设计产品、报价、服务、课程、咨询 -> `dankoe-offer`
- 内容定位、内容支柱、选题系统 -> `dankoe-content`
- 一人公司整体路线 -> `dankoe-roadmap`
- AI 工作流、知识库工作台、自动化交付 -> `dankoe-ai-system`

## 检索摘要

每次 IMA 检索后，先给摘要：

```markdown
## IMA 检索摘要
- 知识库：
- 检索词：
- 命中的材料：
- 可用证据：
- 不确定/缺失：
```

然后再运行具体 Dankoe 工作流。

## 常见查询设计

自媒体学习：

- 个人品牌
- 内容地图
- 2 Hour Writer
- 从0涨粉
- 真实内容

AI 一人公司：

- AI一人公司
- 2026 一人公司
- AI工作流
- AI系统化生活
- 个人品牌自动化

数字产品：

- Mental Monetization
- Make It Profitable
- 推出产品
- landing page
- digital product

写作：

- 2 Hour Writer
- Newsletter
- 深刻观点
- 内容生态系统
- 随笔

## 边界

- 不包含 IMA 凭证。
- 不写死知识库 ID。
- 多个知识库匹配时不自动选择。
- 不暴露 media_id、folder_id、knowledge_base_id。
- 不长篇复制源文。
- IMA 不可用时，只能用本仓库抽象知识包。
