# 虚构结构方案示例

本目录的所有示例人物、职业、项目和描述均为虚构，不来自 A梦或真实客户。

- `structure-plan.student.json`：学生，只启用学习项目，不出现产品、客户和内容库。
- `structure-plan.creator.json`：创作者，启用对外表达、素材、方法与内容生产。
- `structure-plan.consultant.json`：顾问，启用产品、客户、业务知识和客户交付项目。
- `structure-plan.existing.json`：已有 Vault，展示目录映射与向后兼容的 `context_review`；只记范围、索引和差额类型，不放 private 正文。

示例中的 `self_modules` 只启用当前用户确实需要的自我说明书模块。`99-隐私边界与公开授权` 是固定基础设施，不写进 `self_modules`。

`interview_depth` 可以是 `quick`、`standard` 或 `deep`；旧方案缺省该字段时按 `quick` 处理。

可以把任一 JSON 传给 `init_vault.py --plan`，观察不同采访结果如何长出不同目录。
