from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skill" / "ameng-kb-interview"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class ExistingVaultContractTests(unittest.TestCase):
    def test_existing_vault_uses_private_context_without_restarting_interview(self):
        skill = read("skill/ameng-kb-interview/SKILL.md")
        playbook = read("skill/ameng-kb-interview/references/interview-playbook.md")
        existing_doc = read("docs/已有Vault接入.md")

        self.assertIn("`private` 笔记可用于理解用户本人", skill)
        self.assertIn("已有笔记足以回答的问题不再询问", skill)
        self.assertIn("只对缺失信息使用开放式新问题", playbook)
        self.assertIn("已有笔记就是采访证据", existing_doc)
        self.assertNotIn("不扫描私人正文", skill)
        self.assertNotIn("不读取私人正文", existing_doc)
        self.assertNotIn("仍先保留 1–2 个认识用户的问题", playbook)

    def test_supporting_contracts_cover_provenance_privacy_and_staleness(self):
        architecture = read("skill/ameng-kb-interview/references/vault-architecture.md")
        schema = read("skill/ameng-kb-interview/references/structure-plan-schema.md")
        security = read("SECURITY.md")
        agent_metadata = read("skill/ameng-kb-interview/agents/openai.yaml")

        self.assertIn("已知且当前 / 缺失 / 冲突 / 疑似过期", architecture)
        self.assertIn('"context_review"', schema)
        self.assertIn("不写 private 正文摘要", schema)
        self.assertIn("不跟随越出 Vault 的软链接", security)
        self.assertIn("过期", agent_metadata)

    def test_existing_sources_are_reused_without_duplicate_interview_notes(self):
        skill = read("skill/ameng-kb-interview/SKILL.md")
        note_contract = read("skill/ameng-kb-interview/references/note-contract.md")
        privacy = read("skill/ameng-kb-interview/references/routing-and-privacy.md")

        self.assertIn("不为达到数量而复制已有笔记", skill)
        self.assertIn("不为形式强建采访文件", skill)
        self.assertIn("旧笔记可以直接作为来源", note_contract)
        self.assertIn("继承所有来源中最严格的级别", note_contract)
        self.assertIn("读取不等于公开", privacy)


if __name__ == "__main__":
    unittest.main()
