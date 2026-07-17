# ameng-kb-interview

用一次对话采访，把空白或已有的 Obsidian Vault，变成一套 AI 能继续读取、更新和使用的个人知识库。

- AI 一次只问一个问题，你可以直接口语回答。
- 采访后先给出目录预案，确认后再写入。
- 固定的是治理骨架，内容、产品、客户、FAQ、项目类型等由你的真实情况决定。
- 第一版不仅建目录，还会生成首批笔记并跑通一次真实输出。

> **这不是 Obsidian 社区插件。** 它是一个 Codex / Agent Skill：Obsidian 负责查看和编辑本地 Markdown，AI Agent 负责采访、整理、生成目录和写入笔记。

## 最终会得到什么

首次采访通常会交付：

- 一份保留原话的采访记录；
- 一份经你确认的知识库结构方案；
- 一份隐私与公开边界；
- 6–12 篇有真实内容的基础笔记；
- 必要的项目母舰和动态模块；
- 一次基于知识库完成的真实输出，例如活动报名、自我介绍、文章初稿、项目下一步或 FAQ 草稿。

不会默认生成 A梦个人 Vault 里的历史采矿场、归档冷库、黑客松、客户或商机目录。

## 5 分钟快速开始

### 1. 安装 Skill

```bash
git clone https://github.com/zifeixu85/ameng-kb-interview.git
cd ameng-kb-interview
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skill/ameng-kb-interview "${CODEX_HOME:-$HOME/.codex}/skills/"
```

然后重启 Codex，或新建一个 Codex 任务。

也可以下载 [`dist/ameng-kb-interview.skill`](dist/ameng-kb-interview.skill)，用支持 Agent Skills 的客户端安装。

### 2. 准备 Obsidian Vault

第一次使用 Obsidian：

1. 新建一个长期保存的空文件夹。
2. 在 Obsidian 里选择“打开本地仓库”，选中这个文件夹。
3. 在 Codex 中打开**完全相同的文件夹**。
4. 暂时不需要安装任何 Obsidian 第三方插件。

如果你希望先看到最小骨架，可以下载 [`dist/ameng-kb-interview-starter-vault.zip`](dist/ameng-kb-interview-starter-vault.zip)：

1. 解压后得到 `starter-vault/`；
2. 在 Obsidian 和 Codex 中打开同一个 `starter-vault/`；
3. 安装并调用 `$ameng-kb-interview`，让采访结果补全结构和首批笔记。

Starter ZIP 只适用于新建/空 Vault。已有 Vault 不要直接合并这份模板，请使用下面的只读映射流程。

### 3. 开始采访

在 Codex 中输入：

```text
请使用 $ameng-kb-interview。这是一个新的 Obsidian Vault。
先带我完成快速版知识库采访，采访后先给目录预案，等我确认后再写入正式文件。
```

采访完成后，先检查目录预案，再回复“确认写入”。回到 Obsidian，打开 `00-开始这里.md`。

## 已有 Obsidian Vault

请使用更保守的提示词：

```text
请使用 $ameng-kb-interview。这是一个已有内容的 Vault。
请先只读检查顶层目录和必要的入口文件，不要移动、改名、覆盖或删除任何现有内容。
先给我兼容映射方案，等我确认后再开始采访和写入。
```

已有 Vault 的默认流程是：只读检查 → 职责映射 → 用户确认 → 开始采访 → 增量写入。在映射确认之前不创建采访记录或任何其他文件。初始化脚本会跳过已有的用户文件；对它自己创建且带明确标记的配置区块，只更新标记内容，保留标记外的用户文字。

## 固定骨架与动态模块

所有人只共享六个稳定职责：

```text
00-系统工作台  规则、配置、模板和采访来源
10-自我说明书  真实经历、判断、能力与隐私边界
20-可复用资产库  从经历与输入中提取的资产
30-项目工作区  需要持续推进和恢复上下文的项目
40-学习输入库  尚待消化的外部输入
99-附件库  图片、音频、PDF 等附件
```

采访会按需启用：对外角色、产品与服务、客户与用户、素材与案例、方法与判断、内容生产、FAQ/SOP、合作机会、主题分享、职业资产，以及真实存在的项目类型。

[查看完整目录决策说明](docs/目录设计说明.md)

## 快速版与完整版

- **快速版（约 15–20 分钟）**：核心采访 + 一个最高频场景，适合现场体验和第一次建库。
- **完整版（约 45–60 分钟）**：增加项目、学习、内容、产品、客户等条件分支，适合认真建立第一版系统。

全程支持“跳过”“暂停”“继续采访”。恢复时会从采访记录里的下一题继续。

## 初始化脚本（可选）

Skill 会优先调用自带脚本，以保证不覆盖已有文件。你也可以在仓库根目录手动运行：

```bash
python3 skill/ameng-kb-interview/scripts/init_vault.py \
  "/path/to/your-vault" \
  --plan examples/structure-plan.creator.json \
  --dry-run
```

确认预览后去掉 `--dry-run`。验证结构：

```bash
python3 skill/ameng-kb-interview/scripts/validate_vault.py "/path/to/your-vault"
```

脚本不是前置条件；没有 Python 时，Agent 也可以按照同一规则创建文件。

## 第一次使用 Obsidian 的两个设置

1. 在“文件与链接”里把新附件默认位置设为 `99-附件库/_inbox`。
2. 确保 Obsidian 和 Codex 打开的根目录是同一个文件夹。

不需要先安装 Dataview、Tasks、Todoist 或日历插件。任务软件和日历都是可选执行层，不影响第一版知识库成立。

## 仓库结构

```text
ameng-kb-interview/
├── README.md
├── NOTICE.md
├── PRIVACY.md
├── skill/ameng-kb-interview/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/
│   ├── scripts/
│   └── assets/starter-vault/
├── docs/
├── examples/
├── scripts/build_dist.py
├── tests/
└── dist/
    ├── ameng-kb-interview.skill
    └── ameng-kb-interview-starter-vault.zip
```

## 隐私与安全

- Markdown 默认保存在你的本地 Vault。
- AI 处理内容时，所选资料可能会发送给你配置的模型服务商；这不等于“完全本地”。
- `private / internal / public` 是 AI 协作策略标签，不是加密、访问控制或文件系统隔离。
- Codex、本机其他用户或应用仍可能读取其有权限的明文笔记；iCloud、Obsidian Sync、Dropbox 等同步工具也可能上传 Vault。
- 需要硬隔离时，请使用独立、不同步或经加密保护的 Vault，不要提供密码、Token 或其他秘密。
- `10-自我说明书` 默认 private，不能被公开内容自动调用。
- 新提取的资产默认 `status: 待确认`。
- 本项目没有遥测，也不会自动上传、发布、发消息或创建外部承诺。
- 在已有 Vault 使用前请先备份。

详见 [PRIVACY.md](PRIVACY.md) 与 [SECURITY.md](SECURITY.md)。

## 常见问题

### 为什么没有替所有人创建产品库、客户库和黑客松目录？

因为目录应该服务真实工作。采访没有发现持续使用场景时，就不制造空壳。

### 一定要用 Todoist 或日历吗？

不用。知识库管理上下文、判断、复盘和资产；任务与日历可以沿用你现在的工具，也可以完全不用。

### 可以直接用在已有 Vault 吗？

可以，但必须先做只读映射。Skill 和脚本都不会默认迁移、删除或覆盖用户文字；只会在本工具建立的明确受管标记内更新配置。

### 采访生成的内容可以直接公开吗？

不建议。AI 新提取内容默认“待确认”，你确认事实、表达和隐私边界后再公开使用。

## 来源与许可

使用 AI 采访帮助用户启动知识库这一思路，受到叁斤老师课堂材料《知识库采访机器人》的启发；该材料同时注明其 IP 采访框架参考楚川老师。本项目基于这一启发重新撰写和重构，没有收录原材料的逐字提问、示范答案、启动语或汇报文案；公开版的目录模型、隐私路由、脚本和模板根据 A梦当前 Obsidian 实践重新设计。

脚本与测试使用 MIT License；文档、Skill 文本和模板使用 CC BY-NC-SA 4.0。详见 [NOTICE.md](NOTICE.md) 和 [LICENSE](LICENSE)。
