# 笔记契约

## 正式派生笔记最低属性

```yaml
---
tags:
  - type/素材
  - topic/示例主题
date: YYYY-MM-DD
source: 首次建库采访 YYYY-MM-DD
source_type: 采访
source_note: "[[00-系统工作台/采访记录/YYYY-MM-DD-首次建库采访|首次建库采访]]"
usage:
  - 未来可用于什么场景
status: 待确认
sensitivity: internal
last_reviewed: YYYY-MM-DD
---
```

规则：

- `tags` 至少包含一个 `type/...` 和一个 `topic/...`。
- `source`、`source_type`、`usage`、`status`、`sensitivity` 必填。
- Vault 内 Markdown 来源使用 `source_note` wikilink；网页用 `source_url`；Vault 外文件用 `external_path`。
- 不保留空字段。没有值时删掉该字段。
- AI 新提取的资产默认 `status: 待确认`。

## 原始采访记录

```yaml
---
tags:
  - type/采访原文
  - topic/首次建库
date: YYYY-MM-DD
source: 用户口述
source_type: 采访
usage:
  - 作为首批知识资产的来源证据
status: 已记录
sensitivity: private
last_reviewed: YYYY-MM-DD
interview_mode: quick | full
interview_stage: 0
---
```

正文至少包含：采访目标、逐题原话、阶段进度、结构决定、派生笔记、待确认项。

## 双链最低要求

每篇正式派生笔记至少链接回采访原文或项目母舰。采访原文的“派生笔记”列表必须链接回每篇生成笔记。

有效关系包括：来源于、属于、验证、补充、被用于、替代。不要为了数量随机链接同标签笔记。

## 原子化规则

- 一个故事一篇笔记。
- 一个方法或判断一篇笔记。
- 一个产品 / 服务一篇笔记。
- 一个项目一个项目包，至少有 `项目总览.md`。
- 课程或文章按主题消化，不按来源名称在资产库里建大目录。

## 项目母舰最低结构

```yaml
---
status: active
sensitivity: internal
project_type: 产品实验
source_type: 自己项目
start_date: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
---
```

正文包含：目标、当前状态、关键日期、下一步候选、关键决策、进展与证据、外部资料入口、复盘与资产沉淀。

项目状态只使用 `active / waiting / paused / completed / archived`。不要用移动文件夹表达状态。

## 内容版本

启用内容模块时，区分：

- `选题/`：只有方向与读者问题；
- `母稿/`：跨平台核心表达；
- `发布版本/`：读者实际看到的版本；
- `发布复盘/`：数据、反馈与下一步判断。

发布版本是事实快照；后续改写新建版本，不覆盖旧版本。
