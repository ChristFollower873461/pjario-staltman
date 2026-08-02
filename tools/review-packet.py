#!/usr/bin/env python3
"""Build a compact review packet for an LLM or agentic code reviewer."""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import subprocess
import sys
from pathlib import Path


DEFAULT_MAX_BYTES = 240_000
SENSITIVE_UNTRACKED_PATTERNS = [
    "*.env",
    "*.env.*",
    "*.key",
    "*.pem",
    "*.p12",
    "*.pfx",
    "*credentials*",
    "*secret*",
    "*token*",
    "*apikey*",
    "*api_key*",
    "*private*key*",
]


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
        raise SystemExit("review-packet.py must be run inside a git repo")
    return Path(result.stdout.strip())


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def byte_len(text: str) -> int:
    return len(text.encode("utf-8"))


def is_sensitive_untracked(rel: str) -> bool:
    lower = rel.lower()
    for pattern in SENSITIVE_UNTRACKED_PATTERNS:
        if fnmatch.fnmatch(lower, pattern):
            return True
    return False


def collect_rules(root: Path) -> list[tuple[str, str]]:
    paths = [
        root / "AGENTS.md",
        root / "build-system" / "README.md",
    ]
    paths.extend(sorted((root / "build-system" / "agents").glob("*.md")))
    paths.extend(sorted((root / "build-system" / "rules").glob("*.md")))

    docs: list[tuple[str, str]] = []
    for path in paths:
        text = read_text(path).strip()
        if text:
            docs.append((path.relative_to(root).as_posix(), text))
    return docs


def collect_explicit_context(root: Path, paths: list[Path]) -> list[tuple[str, str]]:
    docs: list[tuple[str, str]] = []
    root_resolved = root.resolve()
    for raw in paths:
        candidate = raw if raw.is_absolute() else root_resolved / raw
        if candidate.exists() and candidate.is_symlink():
            raise SystemExit(f"Context file must not be a symlink: {raw}")
        resolved = candidate.resolve(strict=False)
        if resolved != root_resolved and root_resolved not in resolved.parents:
            raise SystemExit(f"Context file must stay inside the repository: {raw}")
        if not resolved.is_file():
            raise SystemExit(f"Context file does not exist: {raw}")
        text = read_text(resolved).strip()
        if text:
            docs.append((resolved.relative_to(root_resolved).as_posix(), text))
    return docs


def collect_diff(root: Path, args: argparse.Namespace) -> str:
    if args.cached:
        return run_git(root, ["diff", "--cached", "--no-ext-diff", "--unified=80"])

    if args.base:
        try:
            return run_git(root, ["diff", "--no-ext-diff", "--unified=80", f"{args.base}...HEAD"])
        except RuntimeError:
            try:
                return run_git(root, ["diff", "--no-ext-diff", "--unified=80", args.base])
            except RuntimeError as error:
                raise SystemExit(
                    f"Could not diff against base ref '{args.base}'. Ensure the ref exists locally "
                    "or fetch it from remote before running review-packet."
                ) from error

    staged = run_git(root, ["diff", "--cached", "--no-ext-diff", "--unified=80"])
    unstaged = run_git(root, ["diff", "--no-ext-diff", "--unified=80"])
    sections = []
    if staged.strip():
        sections.append("## Staged Diff\n\n```diff\n" + staged.rstrip() + "\n```")
    if unstaged.strip():
        sections.append("## Unstaged Diff\n\n```diff\n" + unstaged.rstrip() + "\n```")
    return "\n\n".join(sections)


def collect_untracked(root: Path, max_bytes: int, include_sensitive: bool) -> str:
    files = run_git(root, ["ls-files", "--others", "--exclude-standard"]).splitlines()
    chunks: list[str] = []
    used = 0
    skipped_sensitive: list[str] = []
    for rel in files:
        if not include_sensitive and is_sensitive_untracked(rel):
            skipped_sensitive.append(rel)
            continue
        path = root / rel
        if not path.is_file():
            continue
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if b"\0" in data:
            continue
        remaining = max_bytes - used
        if remaining <= 0:
            chunks.append("\n[untracked files truncated]\n")
            break
        included = data[:remaining]
        text = included.decode("utf-8", errors="replace")
        used += len(included)
        chunks.append(f"### {rel}\n\n```text\n{text.rstrip()}\n```")
    if skipped_sensitive:
        preview = ", ".join(skipped_sensitive[:8])
        note = f"Skipped likely sensitive files by default: {preview}"
        if len(skipped_sensitive) > 8:
            note += f", and {len(skipped_sensitive) - 8} more"
        chunks.insert(0, note)
    if not chunks:
        return ""
    return "## Untracked Files\n\n" + "\n\n".join(chunks)


def build_packet(root: Path, args: argparse.Namespace) -> str:
    generated = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    head = run_git_optional(root, ["branch", "--show-current"], "(unborn)").strip()
    if not head:
        head = "(unborn)"
    status = run_git(root, ["status", "--short"]).rstrip() or "clean"

    docs = collect_rules(root)
    docs_text = "\n\n".join(
        f"## {name}\n\n{body}" for name, body in docs
    )

    diff = collect_diff(root, args).strip()
    if not diff:
        diff = "No tracked diff found."

    header = f"""# Review Packet

Generated: {generated}
Repo: {root}
Branch: {head}

## Review Request

Review the supplied changes as the staff software engineer review agent. Use P2+ as the default blocking threshold. Return `PASS`, `PASS WITH FOLLOW-UP`, or `BLOCK`.

## Git Status

```text
{status}
```
"""

    explicit_context = collect_explicit_context(root, getattr(args, "context", []))
    context_block = ""
    if explicit_context:
        context_text = "\n\n".join(
            f"## {name}\n\n{body}" for name, body in explicit_context
        )
        context_block = f"""
# Explicit Work Context

{context_text}
"""

    docs_block = ""
    if docs_text:
        docs_block = f"""
# Repo Instructions And Rules

{docs_text}
"""

    diff_block = f"""
# Changes To Review

{diff}
"""

    # Explicit work context and the diff are mandatory. If either cannot fit, fail loudly.
    minimum_required = byte_len(header) + byte_len(context_block) + byte_len(diff_block)
    if minimum_required > args.max_bytes:
        raise SystemExit(
            "Required work context and diff exceed --max-bytes budget. "
            "Rerun with a larger --max-bytes value "
            "or a narrower --base range."
        )

    remaining = args.max_bytes - minimum_required
    optional_parts: list[str] = []
    if docs_block and remaining > 0:
        docs_notice = (
            "\n# Repo Instructions And Rules\n\n"
            "[omitted due to --max-bytes; rerun with a larger value for full rules context]\n"
        )
        if byte_len(docs_block) <= remaining:
            optional_parts.append(docs_block)
            remaining -= byte_len(docs_block)
        elif byte_len(docs_notice) <= remaining:
            optional_parts.append(docs_notice)
            remaining -= byte_len(docs_notice)

    if args.include_untracked and remaining > 0:
        # Reserve from remaining so untracked context cannot displace tracked diff.
        untracked_budget = max(0, remaining)
        untracked_block = collect_untracked(
            root,
            untracked_budget,
            include_sensitive=args.include_sensitive_untracked,
        )
        if untracked_block:
            untracked_chunk = "\n" + untracked_block + "\n"
            if byte_len(untracked_chunk) <= remaining:
                optional_parts.append(untracked_chunk)
                remaining -= byte_len(untracked_chunk)

    return header + context_block + "".join(optional_parts) + diff_block


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="Base ref for PR-style review, for example main or origin/main")
    parser.add_argument(
        "--context",
        action="append",
        type=Path,
        default=[],
        help="Repo-confined context file to include before rules and diff; repeatable.",
    )
    parser.add_argument("--cached", action="store_true", help="Review only staged changes")
    parser.add_argument("--include-untracked", action="store_true", help="Include untracked text files")
    parser.add_argument(
        "--include-sensitive-untracked",
        action="store_true",
        help="Include untracked files that match sensitive-name patterns",
    )
    parser.add_argument("--output", type=Path, help="Write the packet to this file instead of stdout")
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
