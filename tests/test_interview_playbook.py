from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK = ROOT / "skill" / "ameng-kb-interview" / "references" / "interview-playbook.md"


class InterviewPlaybookTests(unittest.TestCase):
    def test_quick_mode_starts_with_the_person_and_scaffolds_use_cases(self):
        text = PLAYBOOK.read_text(encoding="utf-8")

        self.assertIn("先不谈知识库。你现在主要在做什么？", text)
        self.assertNotIn("未来 30 天，你最希望这套知识库", text)
        self.assertIn("再提出最多 3 个闭环候选", text)
        self.assertIn("都不是，我自己说", text)
        self.assertIn("还不确定，请你推荐", text)
        self.assertIn("不重复询问", text)
        self.assertIn("只给 1 个建议闭环", text)


if __name__ == "__main__":
    unittest.main()
