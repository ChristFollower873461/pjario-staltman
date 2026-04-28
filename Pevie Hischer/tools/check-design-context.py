#!/usr/bin/env python3
"""Validate a Stitch-compatible DESIGN.md file shape for Pevie adoption."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_TOKEN_GROUPS = [
    "name",
    "colors",
    "typography",
    "rounded",
    "spacing",
    "components",
]

REQUIRED_SECTIONS = [
    "Overview",
    "Colors",
    "Typography",
    "Layout",
    "Elevation & Depth",
    "Shapes",
    "Components",
    "Do's and Don'ts",
]

HEX_COLOR_RE = re.compile(r'"#[0-9A-Fa-f]{6}"')


def read_text(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")
    if not path.is_file():
        raise SystemExit(f"Expected file path, got: {path}")
    return path.read_text(encoding="utf-8")


def split_front_matter(text: str) -> tuple[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise SystemExit("DESIGN.md must start with YAML front matter delimited by `---`.")
    try:
        end_index = next(
            index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration as error:
        raise SystemExit("DESIGN.md front matter must close with `---`.") from error
    front_matter = "\n".join(lines[1:end_index])
    body = "\n".join(lines[end_index + 1 :])
    return front_matter, body


def validate_front_matter(front_matter: str) -> None:
    for group in REQUIRED_TOKEN_GROUPS:
        if not re.search(rf"^{re.escape(group)}:", front_matter, flags=re.MULTILINE):
            raise SystemExit(f"DESIGN.md front matter missing token group: {group}")
    if not HEX_COLOR_RE.search(front_matter):
        raise SystemExit("DESIGN.md front matter must include at least one hex color token.")


def validate_sections(body: str) -> None:
    headings = [
        match.group(1).strip()
        for match in re.finditer(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE)
    ]
    missing = [section for section in REQUIRED_SECTIONS if section not in headings]
    if missing:
        raise SystemExit(f"DESIGN.md missing required section: {missing[0]}")

    last_index = -1
    for section in REQUIRED_SECTIONS:
        current_index = headings.index(section)
        if current_index < last_index:
            raise SystemExit(
                "DESIGN.md sections are out of order. Expected Stitch-compatible order: "
                + ", ".join(REQUIRED_SECTIONS)
            )
        last_index = current_index


def validate_design_context(text: str) -> None:
    front_matter, body = split_front_matter(text)
    validate_front_matter(front_matter)
    validate_sections(body)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path, required=True, help="Path to DESIGN.md")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    validate_design_context(read_text(args.design))
    print("PASS: DESIGN.md has the required Pevie/Stitch-compatible shape.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
