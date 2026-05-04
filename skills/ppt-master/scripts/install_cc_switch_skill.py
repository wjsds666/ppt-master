#!/usr/bin/env python3
"""
Install or refresh the local ppt-master skill inside cc-switch.

Default behavior uses a symlink so the registered skill always follows the
current repository checkout.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sqlite3
import time
import uuid
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
SKILL_MD = SKILL_DIR / "SKILL.md"


def parse_frontmatter(skill_md: Path) -> tuple[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{skill_md} is missing YAML frontmatter")

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise ValueError(f"{skill_md} has invalid YAML frontmatter")

    frontmatter = parts[1]
    name = ""
    description_lines: list[str] = []
    capture_description = False

    for raw_line in frontmatter.splitlines():
        line = raw_line.rstrip()
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip('"').strip("'")
            capture_description = False
            continue
        if line.startswith("description:"):
            value = line.split(":", 1)[1].strip()
            capture_description = True
            if value and value != ">":
                description_lines.append(value.strip('"').strip("'"))
            continue
        if capture_description:
            if not line or (line and not raw_line.startswith(" ")):
                capture_description = False
                continue
            description_lines.append(line.strip())

    if not name:
        raise ValueError("Missing `name` in SKILL.md frontmatter")
    description = " ".join(part for part in description_lines if part).strip()
    return name, description


def iter_skill_files(skill_dir: Path):
    for path in sorted(skill_dir.rglob("*")):
        if path.is_dir():
            continue
        rel = path.relative_to(skill_dir)
        if any(part in {"__pycache__", ".DS_Store"} for part in rel.parts):
            continue
        yield path


def compute_content_hash(skill_dir: Path) -> str:
    digest = hashlib.sha256()
    for path in iter_skill_files(skill_dir):
        rel = path.relative_to(skill_dir).as_posix().encode("utf-8")
        digest.update(rel)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def ensure_registered(
    db_path: Path,
    *,
    skill_id: str,
    name: str,
    description: str,
    directory: str,
    content_hash: str,
) -> None:
    now = int(time.time())
    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute(
            "SELECT id FROM skills WHERE directory = ? OR name = ? LIMIT 1",
            (directory, name),
        ).fetchone()
        if row:
            skill_id = row[0]
            conn.execute(
                """
                UPDATE skills
                SET name = ?,
                    description = ?,
                    directory = ?,
                    enabled_claude = 1,
                    enabled_codex = 1,
                    enabled_gemini = 1,
                    enabled_opencode = 1,
                    enabled_hermes = 1,
                    content_hash = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (name, description, directory, content_hash, now, skill_id),
            )
        else:
            conn.execute(
                """
                INSERT INTO skills (
                    id, name, description, directory,
                    enabled_claude, enabled_codex, enabled_gemini,
                    enabled_opencode, enabled_hermes,
                    installed_at, content_hash, updated_at
                ) VALUES (?, ?, ?, ?, 1, 1, 1, 1, 1, ?, ?, ?)
                """,
                (skill_id, name, description, directory, now, content_hash, now),
            )
        conn.commit()
    finally:
        conn.close()


def stage_skill(source_dir: Path, target_dir: Path, *, copy_mode: bool) -> None:
    if target_dir.exists() or target_dir.is_symlink():
        if target_dir.is_symlink() or target_dir.is_file():
            target_dir.unlink()
        else:
            shutil.rmtree(target_dir)

    target_dir.parent.mkdir(parents=True, exist_ok=True)

    if copy_mode:
        shutil.copytree(source_dir, target_dir, symlinks=True)
    else:
        os.symlink(source_dir, target_dir, target_is_directory=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cc-switch-home",
        default="~/.cc-switch",
        help="cc-switch data directory (default: ~/.cc-switch)",
    )
    parser.add_argument(
        "--skill-folder-name",
        default="ppt-master",
        help="Folder name under ~/.cc-switch/skills (default: ppt-master)",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy the skill instead of symlinking it",
    )
    args = parser.parse_args()

    cc_switch_home = Path(args.cc_switch_home).expanduser().resolve()
    db_path = cc_switch_home / "cc-switch.db"
    skills_dir = cc_switch_home / "skills"
    target_dir = skills_dir / args.skill_folder_name

    if not db_path.exists():
        raise FileNotFoundError(f"cc-switch database not found: {db_path}")

    name, description = parse_frontmatter(SKILL_MD)
    content_hash = compute_content_hash(SKILL_DIR)
    stage_skill(SKILL_DIR, target_dir, copy_mode=args.copy)
    ensure_registered(
        db_path,
        skill_id=str(uuid.uuid4()),
        name=name,
        description=description,
        directory=str(target_dir),
        content_hash=content_hash,
    )

    mode = "copied" if args.copy else "symlinked"
    print(f"Skill {name!r} {mode} to: {target_dir}")
    print(f"Registered in cc-switch: {db_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
