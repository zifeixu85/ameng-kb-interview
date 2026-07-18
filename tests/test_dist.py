from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "scripts" / "build_dist.py"


class DistributionTests(unittest.TestCase):
    def test_archives_include_licenses_and_utf8_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run(
                [sys.executable, str(BUILD), "--output-dir", temp],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            with zipfile.ZipFile(Path(temp) / "ameng-kb-interview.skill") as archive:
                names = set(archive.namelist())
                self.assertIn("ameng-kb-interview/SKILL.md", names)
                self.assertIn("ameng-kb-interview/LICENSE-CODE", names)
                self.assertIn("ameng-kb-interview/LICENSE-CONTENT", names)
                self.assertIn("ameng-kb-interview/NOTICE.md", names)
                chinese = [item for item in archive.infolist() if any(ord(char) > 127 for char in item.filename)]
                self.assertTrue(chinese)
                self.assertTrue(all(item.flag_bits & 0x800 for item in chinese))

            with zipfile.ZipFile(Path(temp) / "ameng-kb-interview-starter-vault.zip") as archive:
                names = set(archive.namelist())
                self.assertIn("starter-vault/00-开始这里.md", names)
                self.assertIn("README.md", names)
                self.assertIn("LICENSE-CONTENT", names)
                self.assertIn("NOTICE.md", names)
                chinese = [item for item in archive.infolist() if any(ord(char) > 127 for char in item.filename)]
                self.assertTrue(chinese)
                self.assertTrue(all(item.flag_bits & 0x800 for item in chinese))

    def test_checked_in_archives_match_release_sources(self):
        skill_archive = ROOT / "dist" / "ameng-kb-interview.skill"
        with zipfile.ZipFile(skill_archive) as archive:
            for relative in (
                "SKILL.md",
                "agents/openai.yaml",
                "references/first-run-and-resume.md",
                "references/interview-playbook.md",
                "references/note-contract.md",
                "references/routing-and-privacy.md",
                "references/self-manual-interview.md",
                "references/structure-plan-schema.md",
                "references/vault-architecture.md",
            ):
                source = ROOT / "skill" / "ameng-kb-interview" / relative
                self.assertEqual(
                    archive.read(f"ameng-kb-interview/{relative}"),
                    source.read_bytes(),
                    f"stale dist entry: {relative}",
                )
            for relative in ("PRIVACY.md", "SECURITY.md"):
                self.assertEqual(
                    archive.read(f"ameng-kb-interview/{relative}"),
                    (ROOT / relative).read_bytes(),
                    f"stale dist entry: {relative}",
                )

        starter_archive = ROOT / "dist" / "ameng-kb-interview-starter-vault.zip"
        with zipfile.ZipFile(starter_archive) as archive:
            self.assertEqual(archive.read("PRIVACY.md"), (ROOT / "PRIVACY.md").read_bytes())
            self.assertEqual(
                archive.read("starter-vault/AGENTS.md"),
                (ROOT / "skill" / "ameng-kb-interview" / "assets" / "starter-vault" / "AGENTS.md").read_bytes(),
            )
            self_paths = [
                name
                for name in archive.namelist()
                if name.startswith("starter-vault/10-自我说明书/")
            ]
            self.assertEqual(
                sorted(self_paths),
                [
                    "starter-vault/10-自我说明书/99-隐私边界与公开授权/隐私边界与公开授权.md",
                    "starter-vault/10-自我说明书/README.md",
                ],
            )


if __name__ == "__main__":
    unittest.main()
