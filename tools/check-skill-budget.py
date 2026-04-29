#!/usr/bin/env python3
"""Fail when an exported skill grows past its context budget."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def words(path: Path) -> int:
    return len(re.findall(r"\b\S+\b", path.read_text(encoding="utf-8")))


def markdown_files(skill_dir: Path) -> list[Path]:
    return sorted(path for path in skill_dir.rglob("*.md") if path.is_file())


def validate(skill_dir: Path, max_skill_words: int, max_total_words: int) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise SystemExit(f"Missing SKILL.md: {skill_md}")
    skill_words = words(skill_md)
    total_words = sum(words(path) for path in markdown_files(skill_dir))
    if skill_words > max_skill_words:
        raise SystemExit(f"SKILL.md budget exceeded: {skill_words} > {max_skill_words} words")
    if total_words > max_total_words:
        raise SystemExit(f"Skill markdown budget exceeded: {total_words} > {max_total_words} words")
    print(f"PASS: skill context budget ok ({skill_words} SKILL.md words, {total_words} total markdown words).")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--max-skill-words", type=int, default=300)
    parser.add_argument("--max-total-words", type=int, default=1000)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    validate(args.skill_dir, args.max_skill_words, args.max_total_words)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
