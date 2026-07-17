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


if __name__ == "__main__":
    unittest.main()
