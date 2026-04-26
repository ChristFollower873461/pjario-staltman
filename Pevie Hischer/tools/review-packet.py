#!/usr/bin/env python3
"""Build a compact review packet for the Pevie Hischer frontend reviewer."""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path


DEFAULT_MAX_BYTES = 220_000


def run_git(root: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def run_git_optional(root: Path, args: list[str], default: str = "") -> str:
    try:
        return run_git(root, args)
    except RuntimeError:
        return default


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit("review-packet.py must run inside a git repository")
    return Path(result.stdout.strip())


def read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def collect_rules(root: Path) -> list[tuple[str, str]]:
    package = root / "Pevie Hischer"
    paths = [
        package / "AGENTS.md",
        package / "build-system" / "README.md",
    ]
    paths.extend(sorted((package / "build-system" / "agents").glob("*.md")))
    paths.extend(sorted((package / "build-system" / "rules").glob("*.md")))

    docs: list[tuple[str, str]] = []
    for path in paths:
        text = read_text(path).strip()
        if text:
            docs.append((path.relative_to(root).as_posix(), text))
    return docs


def collect_diff(root: Path, args: argparse.Namespace) -> str:
    target_path = "Pevie Hischer"
    if args.cached:
        return run_git(root, ["diff", "--cached", "--no-ext-diff", "--unified=80", "--", target_path])
    if args.base:
        try:
            return run_git(root, ["diff", "--no-ext-diff", "--unified=80", f"{args.base}...HEAD", "--", target_path])
        except RuntimeError:
            try:
                return run_git(root, ["diff", "--no-ext-diff", "--unified=80", args.base, "--", target_path])
            except RuntimeError as error:
                raise SystemExit(
                    f"Could not diff against base ref '{args.base}'. Ensure the ref exists locally "
                    "or fetch it from remote before running review-packet."
                ) from error
    staged = run_git(root, ["diff", "--cached", "--no-ext-diff", "--unified=80", "--", target_path])
    unstaged = run_git(root, ["diff", "--no-ext-diff", "--unified=80", "--", target_path])
    sections = []
    if staged.strip():
        sections.append("## Staged Diff\n\n```diff\n" + staged.rstrip() + "\n```")
    if unstaged.strip():
        sections.append("## Unstaged Diff\n\n```diff\n" + unstaged.rstrip() + "\n```")
    return "\n\n".join(sections)


def byte_len(text: str) -> int:
    return len(text.encode("utf-8"))


def build_packet(root: Path, args: argparse.Namespace) -> str:
    generated = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    head = run_git_optional(root, ["branch", "--show-current"], "(unborn)").strip() or "(unborn)"
    status = run_git(root, ["status", "--short", "--", "Pevie Hischer"]).rstrip() or "clean"
    docs = collect_rules(root)
    docs_text = "\n\n".join(f"## {name}\n\n{body}" for name, body in docs)
    diff = collect_diff(root, args).strip() or "No tracked diff found for `Pevie Hischer`."

    header = f"""# Pevie Hischer Review Packet

Generated: {generated}
Repo: {root}
Branch: {head}

## Review Request

Review these frontend-package changes with a staff frontend quality bar. Use P2+ as default blocking threshold.

## Git Status (Pevie Hischer only)

```text
{status}
```
"""

    docs_block = ""
    if docs_text:
        docs_block = f"""
# Package Rules

{docs_text}
"""

    diff_block = f"""
# Changes To Review

{diff}
"""

    minimum_required = byte_len(header) + byte_len(diff_block)
    if minimum_required > args.max_bytes:
        raise SystemExit(
            "Diff exceeds --max-bytes budget. Rerun with a larger --max-bytes value "
            "or a narrower --base range."
        )

    remaining = args.max_bytes - minimum_required
    optional_parts: list[str] = []
    if docs_block and remaining > 0:
        docs_notice = (
            "\n# Package Rules\n\n"
            "[omitted due to --max-bytes; rerun with a larger value for full frontend rules context]\n"
        )
        if byte_len(docs_block) <= remaining:
            optional_parts.append(docs_block)
        elif byte_len(docs_notice) <= remaining:
            optional_parts.append(docs_notice)

    return header + "".join(optional_parts) + diff_block


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="Base ref for PR-style diff")
    parser.add_argument("--cached", action="store_true", help="Review only staged changes")
    parser.add_argument("--output", type=Path, help="Write packet to file")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="Maximum packet size")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = repo_root()
    packet = build_packet(root, args)
    if args.output:
        output = args.output if args.output.is_absolute() else root / args.output
        output.write_text(packet, encoding="utf-8")
        print(f"Wrote {output}")
    else:
        print(packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
