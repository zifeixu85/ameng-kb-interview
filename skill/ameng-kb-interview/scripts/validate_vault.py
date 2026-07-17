#!/usr/bin/env python3
"""Validate the public starter vault without modifying it."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath


REQUIRED_PATHS = [
    "AGENTS.md",
    "00-系统工作台/知识库说明.md",
    "00-系统工作台/建库配置.md",
    "10-自我说明书/99-隐私边界与公开授权/隐私边界与公开授权.md",
    "20-可复用资产库/README.md",
    "30-项目工作区/项目总览.md",
    "40-学习输入库/README.md",
    "99-附件库/_inbox",
]

FORBIDDEN_DEFAULTS = ["80-历史采矿场", "90-归档冷库", "原始"]
REQUIRED_ASSET_FIELDS = {"tags", "source", "source_type", "usage", "status", "sensitivity"}
ABSOLUTE_PATH = re.compile(r"(?:/Users/[^\s]+|[A-Za-z]:\\Users\\[^\s]+)")
SECRET_PATTERN = re.compile(r"(?i)(api[_-]?key|access[_-]?token|secret|password)\s*[:=]\s*[^\s<>{}]+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only checks for an ameng-kb-interview Vault")
    parser.add_argument("vault", help="Target Obsidian Vault path")
    return parser.parse_args()


def frontmatter_keys(text: str) -> set[str]:
    if not text.startswith("---\n"):
        return set()
    end = text.find("\n---", 4)
    if end < 0:
        return set()
    keys: set[str] = set()
    for line in text[4:end].splitlines():
        if line and not line.startswith((" ", "-", "#")) and ":" in line:
            keys.add(line.split(":", 1)[0].strip())
    return keys


def load_mappings(vault: Path) -> dict[str, str]:
    candidates = [vault / "00-系统工作台" / "知识库结构方案.json"]
    candidates.extend(sorted(vault.rglob("知识库结构方案.json")))
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen or not candidate.is_file() or candidate.is_symlink():
            continue
        seen.add(candidate)
        try:
            plan = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        mappings = plan.get("existing_mappings", {})
        if isinstance(mappings, dict):
            normalized = {str(key): str(value) for key, value in mappings.items()}
            expected = remap("00-系统工作台/知识库结构方案.json", normalized)
            if candidate.relative_to(vault).as_posix() == expected:
                return normalized
    return {}


def remap(relative: str, mappings: dict[str, str]) -> str:
    source = PurePosixPath(relative).as_posix()
    for prefix in sorted(mappings, key=len, reverse=True):
        normalized = prefix.strip("/")
        if source == normalized or source.startswith(normalized + "/"):
            suffix = source[len(normalized) :].lstrip("/")
            target = mappings[prefix].strip("/")
            return f"{target}/{suffix}" if suffix else target
    return source


def main() -> int:
    args = parse_args()
    vault = Path(args.vault).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not vault.is_dir():
        print(json.dumps({"errors": [f"Vault does not exist: {vault}"], "warnings": []}, ensure_ascii=False, indent=2))
        return 2

    mappings = load_mappings(vault)
    for relative in REQUIRED_PATHS:
        effective = remap(relative, mappings)
        if not (vault / effective).exists():
            errors.append(f"missing required path: {effective}")

    for relative in FORBIDDEN_DEFAULTS:
        if (vault / relative).exists():
            warnings.append(f"non-default legacy directory exists: {relative}")

    for note in vault.rglob("*.md"):
        relative = note.relative_to(vault).as_posix()
        if note.is_symlink():
            warnings.append(f"skipped symlinked Markdown: {relative}")
            continue
        try:
            text = note.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            warnings.append(f"cannot decode as UTF-8: {relative}")
            continue
        if ABSOLUTE_PATH.search(text):
            warnings.append(f"possible absolute private path: {relative}")
        if SECRET_PATTERN.search(text):
            errors.append(f"possible secret in Markdown: {relative}")
        asset_root = remap("20-可复用资产库", mappings).rstrip("/") + "/"
        if relative.startswith(asset_root) and note.name != "README.md":
            missing = REQUIRED_ASSET_FIELDS - frontmatter_keys(text)
            if missing:
                warnings.append(f"asset metadata missing {sorted(missing)}: {relative}")

    result = {"vault": str(vault), "errors": errors, "warnings": warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
