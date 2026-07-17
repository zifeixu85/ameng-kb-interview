#!/usr/bin/env python3
"""Build UTF-8-safe standalone distribution archives with license notices."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "ameng-kb-interview"
STARTER = SKILL / "assets" / "starter-vault"
SKILL_LEGAL = ["LICENSE", "LICENSE-CODE", "LICENSE-CONTENT", "NOTICE.md", "PRIVACY.md", "SECURITY.md"]
STARTER_LEGAL = [
    ("docs/STARTER-VAULT.md", "README.md"),
    ("LICENSE-CONTENT", "LICENSE-CONTENT"),
    ("NOTICE.md", "NOTICE.md"),
    ("PRIVACY.md", "PRIVACY.md"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build .skill and starter Vault ZIP archives")
    parser.add_argument("--output-dir", default=str(ROOT / "dist"), help="Output directory")
    return parser.parse_args()


def source_files(root: Path):
    for path in sorted(root.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts and path.name != ".DS_Store":
            yield path


def build_skill(output: Path) -> None:
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in source_files(SKILL):
            archive.write(path, (Path(SKILL.name) / path.relative_to(SKILL)).as_posix())
        for name in SKILL_LEGAL:
            archive.write(ROOT / name, (Path(SKILL.name) / name).as_posix())


def build_starter(output: Path) -> None:
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in source_files(STARTER):
            archive.write(path, (Path("starter-vault") / path.relative_to(STARTER)).as_posix())
        for source, target in STARTER_LEGAL:
            archive.write(ROOT / source, target)


def main() -> int:
    args = parse_args()
    output = Path(args.output_dir).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    build_skill(output / "ameng-kb-interview.skill")
    build_starter(output / "ameng-kb-interview-starter-vault.zip")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
