from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "ameng-kb-interview"


class SelfManualContractTests(unittest.TestCase):
    def test_full_self_manual_map_is_documented(self):
        architecture = (SKILL / "references" / "vault-architecture.md").read_text(
            encoding="utf-8"
        )
        expected = (
            "01-身份与经历",
            "02-价值观与驱动力",
            "03-性格底色与心理测试",
            "04-偏好审美与表达习惯",
            "05-身体健康与能量状态",
            "06-家庭亲密关系与责任",
            "07-社会生活与重要关系",
            "08-状态变化与阶段复盘",
            "09-日记与自我观察",
            "10-AI协作偏好",
            "99-隐私边界与公开授权",
        )
        for directory in expected:
            self.assertIn(directory, architecture)

    def test_deep_mode_is_multi_session_and_sensitive_topics_are_opt_in(self):
        skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        playbook = (SKILL / "references" / "interview-playbook.md").read_text(
            encoding="utf-8"
        )
        self_manual = (SKILL / "references" / "self-manual-interview.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("通常 2–6 小时以上，分多次完成", skill_text)
        self.assertIn("不以一小时或问完固定题数作为完成标准", skill_text)
        self.assertIn("不得一次列出几十道题", playbook)
        self.assertIn("高敏感模块默认不选", self_manual)
        self.assertNotIn("完整版（约 45–60 分钟）", skill_text)

    def test_self_notes_track_confidence_and_valid_period(self):
        note_contract = (SKILL / "references" / "note-contract.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("confidence: 待确认 | 阶段性判断 | 已确认", note_contract)
        self.assertIn("valid_period: 长期 | 当前阶段 | 已过期", note_contract)


if __name__ == "__main__":
    unittest.main()
