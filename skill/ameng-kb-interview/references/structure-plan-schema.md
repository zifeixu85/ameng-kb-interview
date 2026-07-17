# 结构方案 JSON

在采访结束、创建目录前生成一个 JSON 文件。`init_vault.py` 只接受下面列出的模块和项目类型，避免任意路径写入。

```json
{
  "schema_version": 1,
  "vault_name": "示例知识库",
  "mode": "new",
  "primary_uses": ["personal", "projects", "learning", "content"],
  "first_input": "每周复盘录音",
  "first_output": "一篇内容母稿",
  "optional_modules": ["profile", "stories", "methods", "content", "talks"],
  "project_types": ["product", "learning"],
  "custom_project_types": [],
  "task_system": "none",
  "calendar_system": "none",
  "existing_mappings": {},
  "privacy_notes": ["家庭与健康信息只保留在 10-自我说明书"],
  "evidence": {
    "content": "用户每周写公众号",
    "talks": "用户每季度做一次线下分享"
  }
}
```

## 允许值

- `mode`: `new` 或 `existing`
- `optional_modules`: `profile`, `products`, `customers`, `stories`, `methods`, `content`, `business_knowledge`, `opportunities`, `talks`, `career`
- `project_types`: `work`, `client`, `product`, `content`, `learning`, `community`, `hackathon`
- `task_system`: `none`, `todoist`, `other`
- `calendar_system`: `none`, `google-calendar`, `apple-calendar`, `outlook`, `other`

`custom_project_types` 只放用户确实有的稳定类型，使用简短中文名称，例如 `播客项目`。不得包含 `/`、`..` 或系统保留字符。

## 生成纪律

1. 每个动态模块必须在 `evidence` 写入来自采访的触发依据。
2. 用户只是“未来可能做”时，不启用模块。
3. 没有参加黑客松时，不把 `hackathon` 写入方案。
4. Todoist 和日历都可为 `none`；不要把工具选择当成知识库完整性的条件。
5. 已有 Vault 的 `existing_mappings` 由人和 AI 共同确认，初始化脚本不会自动移动旧目录。
