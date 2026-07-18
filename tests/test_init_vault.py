from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INIT = ROOT / "skill" / "ameng-kb-interview" / "scripts" / "init_vault.py"
VALIDATE = ROOT / "skill" / "ameng-kb-interview" / "scripts" / "validate_vault.py"


class InitVaultTests(unittest.TestCase):
    def run_init(self, vault: Path, plan: dict | None = None, dry_run: bool = False) -> subprocess.CompletedProcess:
        command = [sys.executable, str(INIT), str(vault)]
        if plan is not None:
            plan_path = vault.parent / "plan.json"
            plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            command.extend(["--plan", str(plan_path)])
        if dry_run:
            command.append("--dry-run")
        return subprocess.run(command, check=False, capture_output=True, text=True)

    def test_core_only_does_not_create_business_or_hackathon_folders(self):
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            result = self.run_init(vault)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((vault / "00-系统工作台" / "知识库说明.md").exists())
            self.assertTrue((vault / "20-可复用资产库" / "README.md").exists())
            self.assertTrue((vault / "10-自我说明书" / "99-隐私边界与公开授权" / "隐私边界与公开授权.md").exists())
            self.assertFalse((vault / "10-自我说明书" / "01-身份与经历").exists())
            self.assertFalse((vault / "10-自我说明书" / "02-价值观与驱动力").exists())
            self.assertFalse((vault / "20-可复用资产库" / "2-产品与服务").exists())
            self.assertFalse((vault / "30-项目工作区" / "黑客松项目").exists())
            config = (vault / "00-系统工作台" / "建库配置.md").read_text(encoding="utf-8")
            self.assertIn("- 采访深度：quick", config)
            start = (vault / "00-开始这里.md").read_text(encoding="utf-8")
            self.assertIn("选择快速、标准或深度版", start)

    def test_plan_creates_only_selected_modules_and_project_types(self):
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            plan = {
                "schema_version": 1,
                "vault_name": "虚构创作者",
                "mode": "new",
                "interview_depth": "deep",
                "primary_uses": ["content", "projects"],
                "first_input": "访谈录音",
                "first_output": "内容母稿",
                "self_modules": ["identity", "preferences", "ai_collaboration"],
                "optional_modules": ["profile", "stories", "content"],
                "project_types": ["content"],
                "custom_project_types": ["播客项目"],
                "task_system": "none",
                "calendar_system": "none",
                "existing_mappings": {},
                "privacy_notes": ["家庭信息不进入公开内容"],
                "evidence": {"content": "每周写作", "stories": "有访谈案例"},
            }
            result = self.run_init(vault, plan)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((vault / "20-可复用资产库" / "6-内容生产" / "母稿").exists())
            self.assertTrue((vault / "10-自我说明书" / "01-身份与经历" / "README.md").exists())
            self.assertTrue((vault / "10-自我说明书" / "04-偏好审美与表达习惯" / "README.md").exists())
            self.assertTrue((vault / "10-自我说明书" / "10-AI协作偏好" / "README.md").exists())
            self.assertFalse((vault / "10-自我说明书" / "05-身体健康与能量状态").exists())
            self.assertTrue((vault / "30-项目工作区" / "内容项目").exists())
            self.assertTrue((vault / "30-项目工作区" / "播客项目").exists())
            self.assertFalse((vault / "20-可复用资产库" / "2-产品与服务").exists())
            self.assertFalse((vault / "30-项目工作区" / "黑客松项目").exists())
            config = (vault / "00-系统工作台" / "建库配置.md").read_text(encoding="utf-8")
            self.assertIn("## 已启用自我说明书模块", config)
            self.assertIn("- 采访深度：deep", config)
            self.assertIn("`preferences`：10-自我说明书/04-偏好审美与表达习惯", config)
            validate = subprocess.run(
                [sys.executable, str(VALIDATE), str(vault)], check=False, capture_output=True, text=True
            )
            self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)

    def test_all_self_modules_follow_the_self_manual_methodology(self):
        expected = {
            "identity": "01-身份与经历",
            "values": "02-价值观与驱动力",
            "personality": "03-性格底色与心理测试",
            "preferences": "04-偏好审美与表达习惯",
            "health_energy": "05-身体健康与能量状态",
            "family_intimacy": "06-家庭亲密关系与责任",
            "social_relations": "07-社会生活与重要关系",
            "stage_reviews": "08-状态变化与阶段复盘",
            "journal": "09-日记与自我观察",
            "ai_collaboration": "10-AI协作偏好",
        }
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            plan = {
                "schema_version": 1,
                "vault_name": "完整自我说明书",
                "mode": "new",
                "self_modules": list(expected),
                "optional_modules": [],
                "project_types": [],
                "custom_project_types": [],
                "existing_mappings": {},
            }
            result = self.run_init(vault, plan)
            self.assertEqual(result.returncode, 0, result.stderr)
            for module_id, directory in expected.items():
                readme = vault / "10-自我说明书" / directory / "README.md"
                self.assertTrue(readme.exists(), module_id)
                self.assertIn("`private`", readme.read_text(encoding="utf-8"))

            children = {path.name for path in (vault / "10-自我说明书").iterdir() if path.is_dir()}
            self.assertEqual(children, set(expected.values()) | {"99-隐私边界与公开授权"})

    def test_existing_file_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            target = vault / "00-系统工作台" / "知识库说明.md"
            target.parent.mkdir(parents=True)
            target.write_text("用户自己的内容\n", encoding="utf-8")
            result = self.run_init(vault)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), "用户自己的内容\n")

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            result = self.run_init(vault, dry_run=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(vault.exists())
            report = json.loads(result.stdout)
            self.assertEqual(len(report["created"]), len(set(report["created"])))

    def test_existing_mapping_reuses_user_directories(self):
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            projects_readme = vault / "Projects" / "README.md"
            projects_readme.parent.mkdir(parents=True)
            projects_readme.write_text("用户自己的项目说明\n", encoding="utf-8")
            resources_readme = vault / "Resources" / "README.md"
            resources_readme.parent.mkdir(parents=True)
            resources_readme.write_text("用户自己的学习说明\n", encoding="utf-8")
            plan = {
                "schema_version": 1,
                "vault_name": "Existing Vault",
                "mode": "existing",
                "primary_uses": ["projects"],
                "self_modules": ["values", "stage_reviews"],
                "optional_modules": [],
                "project_types": ["work"],
                "custom_project_types": [],
                "existing_mappings": {
                    "00-系统工作台": "Admin/System",
                    "10-自我说明书": "Personal",
                    "30-项目工作区": "Projects",
                    "40-学习输入库": "Resources",
                },
                "privacy_notes": [],
                "evidence": {},
            }
            result = self.run_init(vault, plan)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(projects_readme.read_text(encoding="utf-8"), "用户自己的项目说明\n")
            self.assertEqual(resources_readme.read_text(encoding="utf-8"), "用户自己的学习说明\n")
            self.assertTrue((vault / "Projects" / "项目总览.md").exists())
            self.assertTrue((vault / "Projects" / "工作项目").exists())
            self.assertTrue((vault / "Personal" / "02-价值观与驱动力" / "README.md").exists())
            self.assertTrue((vault / "Personal" / "08-状态变化与阶段复盘" / "README.md").exists())
            self.assertFalse((vault / "Personal" / "03-性格底色与心理测试").exists())
            self.assertFalse((vault / "30-项目工作区").exists())
            self.assertFalse((vault / "00-系统工作台").exists())
            self.assertFalse((vault / "10-自我说明书").exists())
            config = (vault / "Admin" / "System" / "建库配置.md").read_text(encoding="utf-8")
            self.assertIn("`30-项目工作区` → `Projects`", config)
            start = (vault / "00-开始这里.md").read_text(encoding="utf-8")
            self.assertIn("[[Projects/项目总览|项目总览]]", start)
            self.assertIn("[[Resources/README|学习输入库]]", start)
            self.assertNotIn("[[30-项目工作区/项目总览", start)
            agents = (vault / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("`Admin/System/建库配置.md`", agents)
            self.assertIn("`Personal` 默认 private", agents)
            self.assertNotIn("`10-自我说明书` 默认 private", agents)
            validate = subprocess.run(
                [sys.executable, str(VALIDATE), str(vault)], check=False, capture_output=True, text=True
            )
            self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)

    def test_existing_context_review_is_optional_and_rendered_without_private_body(self):
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            plan = {
                "schema_version": 1,
                "vault_name": "Existing Vault",
                "mode": "existing",
                "primary_uses": ["projects"],
                "optional_modules": [],
                "project_types": [],
                "custom_project_types": [],
                "existing_mappings": {
                    "00-系统工作台": "Admin/System",
                    "10-自我说明书": "Personal",
                },
                "privacy_notes": [],
                "evidence": {},
                "context_review": {
                    "reviewed_at": "2026-07-18",
                    "read_scope": ["Personal"],
                    "excluded_paths": ["Personal/日记"],
                    "source_index_note": "Admin/System/采访记录/2026-07-18-已有上下文审计.md",
                    "source_count": 3,
                    "known": ["当前角色"],
                    "missing": ["首个输出"],
                    "conflicts": [],
                    "stale_candidates": ["当前项目"],
                },
            }
            result = self.run_init(vault, plan)
            self.assertEqual(result.returncode, 0, result.stderr)

            config = (vault / "Admin" / "System" / "建库配置.md").read_text(encoding="utf-8")
            self.assertIn("## 已有上下文审计", config)
            self.assertIn("- 来源数量：3", config)
            self.assertIn("- 缺失：首个输出", config)
            self.assertIn("- 疑似过期：当前项目", config)
            self.assertIn("不写 private 正文摘要", config)
            saved_plan = json.loads(
                (vault / "Admin" / "System" / "知识库结构方案.json").read_text(encoding="utf-8")
            )
            self.assertEqual(saved_plan["context_review"], plan["context_review"])

    def test_context_review_rejects_paths_outside_the_vault(self):
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            plan = {
                "schema_version": 1,
                "vault_name": "Unsafe context review",
                "mode": "existing",
                "optional_modules": [],
                "project_types": [],
                "custom_project_types": [],
                "existing_mappings": {},
                "context_review": {
                    "read_scope": ["../outside"],
                    "known": [],
                    "missing": [],
                    "conflicts": [],
                    "stale_candidates": [],
                },
            }
            result = self.run_init(vault, plan)
            self.assertEqual(result.returncode, 2)
            self.assertIn("unsafe context_review read_scope path", result.stderr)

    def test_path_traversal_in_custom_project_type_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            plan = {
                "schema_version": 1,
                "vault_name": "Unsafe",
                "mode": "new",
                "optional_modules": [],
                "project_types": [],
                "custom_project_types": ["../escape"],
                "existing_mappings": {},
            }
            result = self.run_init(vault, plan)
            self.assertEqual(result.returncode, 2)
            self.assertIn("unsafe custom project type", result.stderr)
            self.assertFalse((Path(temp) / "escape").exists())

    def test_unknown_or_unsafe_self_module_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            plan = {
                "schema_version": 1,
                "vault_name": "Unsafe self module",
                "mode": "new",
                "self_modules": ["../private"],
                "optional_modules": [],
                "project_types": [],
                "custom_project_types": [],
                "existing_mappings": {},
            }
            result = self.run_init(vault, plan)
            self.assertEqual(result.returncode, 2)
            self.assertIn("unknown self_modules", result.stderr)
            self.assertFalse(vault.exists())

    def test_unknown_interview_depth_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            plan = {
                "schema_version": 1,
                "vault_name": "Invalid depth",
                "mode": "new",
                "interview_depth": "forever",
                "self_modules": [],
                "optional_modules": [],
                "project_types": [],
                "custom_project_types": [],
                "existing_mappings": {},
            }
            result = self.run_init(vault, plan)
            self.assertEqual(result.returncode, 2)
            self.assertIn("interview_depth must be 'quick', 'standard', or 'deep'", result.stderr)
            self.assertFalse(vault.exists())

    def test_self_modules_must_be_an_array_without_duplicates(self):
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            base = {
                "schema_version": 1,
                "vault_name": "Invalid self modules",
                "mode": "new",
                "optional_modules": [],
                "project_types": [],
                "custom_project_types": [],
                "existing_mappings": {},
            }
            for value, message in [
                ("identity", "self_modules must be an array"),
                (["identity", "identity"], "self_modules must not contain duplicates"),
            ]:
                plan = dict(base, self_modules=value)
                result = self.run_init(vault, plan)
                self.assertEqual(result.returncode, 2)
                self.assertIn(message, result.stderr)

    def test_windows_style_mapping_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            plan = {
                "schema_version": 1,
                "vault_name": "Unsafe mapping",
                "mode": "existing",
                "optional_modules": [],
                "project_types": [],
                "custom_project_types": [],
                "existing_mappings": {"30-项目工作区": "..\\escape"},
            }
            result = self.run_init(vault, plan)
            self.assertEqual(result.returncode, 2)
            self.assertIn("unsafe existing mapping target", result.stderr)

    def test_symlinked_directory_cannot_escape_vault(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            vault = root / "vault"
            outside = root / "outside"
            vault.mkdir()
            outside.mkdir()
            (vault / "00-系统工作台").symlink_to(outside, target_is_directory=True)
            result = self.run_init(vault)
            self.assertEqual(result.returncode, 2)
            self.assertIn("write path escapes Vault", result.stderr)
            self.assertEqual(list(outside.iterdir()), [])

    def test_managed_block_preserves_user_text_outside_markers(self):
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp) / "vault"
            target = vault / "00-开始这里.md"
            target.parent.mkdir(parents=True)
            target.write_text(
                "# 我的首页\n\n用户前置内容\n"
                "<!-- AMENG_KB_START_START -->\n旧受管内容\n<!-- AMENG_KB_START_END -->\n"
                "用户后置内容\n",
                encoding="utf-8",
            )
            result = self.run_init(vault)
            self.assertEqual(result.returncode, 0, result.stderr)
            updated = target.read_text(encoding="utf-8")
            self.assertIn("用户前置内容", updated)
            self.assertIn("用户后置内容", updated)
            self.assertNotIn("旧受管内容", updated)
            self.assertIn("第一次使用", updated)


if __name__ == "__main__":
    unittest.main()
