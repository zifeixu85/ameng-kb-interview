# 结构方案 JSON

在采访结束、创建目录前生成一个 JSON 文件。`init_vault.py` 只接受下面列出的模块和项目类型，避免任意路径写入。

```json
{
  "schema_version": 1,
  "vault_name": "示例知识库",
  "mode": "existing",
  "interview_depth": "standard",
  "primary_uses": ["personal", "projects", "learning", "content"],
  "first_input": "每周复盘录音",
  "first_output": "一篇内容母稿",
  "optional_modules": ["profile", "stories", "methods", "content", "talks"],
  "self_modules": ["identity", "values", "preferences", "stage_reviews", "ai_collaboration"],
  "project_types": ["product", "learning"],
  "custom_project_types": [],
  "task_system": "none",
  "calendar_system": "none",
  "existing_mappings": {
    "00-系统工作台": "Admin/System",
    "10-自我说明书": "Personal",
    "30-项目工作区": "Projects"
  },
  "privacy_notes": ["家庭与健康信息只保留在 10-自我说明书"],
  "evidence": {
    "content": "用户每周写公众号",
    "talks": "用户每季度做一次线下分享"
  },
  "context_review": {
    "reviewed_at": "2026-07-18",
    "read_scope": ["Personal", "Projects"],
    "excluded_paths": ["Personal/日记"],
    "source_index_note": "Admin/System/采访记录/2026-07-18-已有上下文审计.md",
    "source_count": 6,
    "known": ["当前角色", "已启用项目"],
    "missing": ["首个输出"],
    "conflicts": [],
    "stale_candidates": ["当前内容平台"]
  }
}
```

`context_review` 只用于 `mode: existing`，是向后兼容的可选字段；旧方案不需要补它。它只记录本次读取边界、来源索引笔记和差额类型，不写 private 正文摘要。

## 允许值

- `mode`: `new` 或 `existing`
- `interview_depth`: `quick`, `standard`, `deep`
- `self_modules`: `identity`, `values`, `personality`, `preferences`, `health_energy`, `family_intimacy`, `social_relations`, `stage_reviews`, `journal`, `ai_collaboration`
- `optional_modules`: `profile`, `products`, `customers`, `stories`, `methods`, `content`, `business_knowledge`, `opportunities`, `talks`, `career`
- `project_types`: `work`, `client`, `product`, `content`, `learning`, `community`, `hackathon`
- `task_system`: `none`, `todoist`, `other`
- `calendar_system`: `none`, `google-calendar`, `apple-calendar`, `outlook`, `other`

`custom_project_types` 只放用户确实有的稳定类型，使用简短中文名称，例如 `播客项目`。不得包含 `/`、`..` 或系统保留字符。

## 生成纪律

1. 每个动态模块必须在 `evidence` 写入触发依据。新 Vault 引用采访回答；已有 Vault 优先引用真正提供证据的现有笔记及必要的增量确认。
2. 用户只是“未来可能做”时，不启用模块。
3. 没有参加黑客松时，不把 `hackathon` 写入方案。
4. Todoist 和日历都可为 `none`；不要把工具选择当成知识库完整性的条件。
5. 已有 Vault 的 `existing_mappings` 由人和 AI 共同确认，初始化脚本不会自动移动旧目录。
6. 已有 Vault 的动态模块证据可来自已有笔记或本次增量确认；应在 `evidence` 中标明来源笔记，不得统一写成“来自采访”。
7. `context_review.source_index_note`、`read_scope` 和 `excluded_paths` 都使用 Vault 内相对路径；不存储绝对路径、密钥或 private 正文。
8. `known / missing / conflicts / stale_candidates` 只写非敏感主题名和差额状态。详细来源与用户修正保存在 `source_index_note` 指向的 private 审计 / 补访记录。
9. `self_modules` 只列本轮已经选择、存在可靠旧证据或已经产生真实内容的自我模块。高敏感模块不能因为选择了 `deep` 就自动全部启用。
10. `99-隐私边界与公开授权` 是固定模块，不写进 `self_modules`。
