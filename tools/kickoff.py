#!/usr/bin/env python3
"""Generate a compact implementation-agent kickoff prompt."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def read_text(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"Expected a file path: {path}")
    return path.read_text(encoding="utf-8")


def detect_complexity(ticket_text: str) -> str:
    match = re.search(
        r"^Level:\s*(trivial|non-trivial)\s*$",
        ticket_text,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    if not match:
        raise SystemExit("Ticket must include `Level: trivial` or `Level: non-trivial`.")
    return match.group(1).lower()


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def existing(root: Path, paths: list[str]) -> list[str]:
    return [path for path in paths if (root / path).is_file()]


def command_list(profile: str, ticket: str, plan: str | None, design: str | None) -> list[str]:
    if profile == "pevie":
        commands = [
            f'make -f "Pevie Hischer/Makefile" check-planning-brief TICKET="{ticket}"'
            + (f' PLAN="{plan}"' if plan else ""),
        ]
        if design:
            commands.append(f'make -f "Pevie Hischer/Makefile" design-lint DESIGN="{design}"')
        commands.extend(
            [
                'make -f "Pevie Hischer/Makefile" test',
                'make -f "Pevie Hischer/Makefile" review-packet',
            ]
        )
        return commands

    return [
        f'make check-planning-brief TICKET="{ticket}"' + (f' PLAN="{plan}"' if plan else ""),
        "make check-proof TICKET=<ticket> QA=<qa-plan> PR=<pr-note>",
        "make test",
        "make review-packet",
    ]


def build_request_commands() -> list[str]:
    return [
        "make doctor",
        "run every Required Proof command named in the build request",
        "make review-packet",
    ]


def build_request_prompt(repo: Path, build_request: Path, profile: str, base: str) -> str:
    read_text(build_request)
    request_rel = rel(build_request, repo)
    read_first = existing(
        repo,
        [
            "AGENTS.md",
            "build-system/agents/build-coordinator.md",
            "build-system/agents/implementation-agent.md",
            "build-system/rules/proof-matrix.md",
        ],
    )
    if profile == "pevie":
        read_first.extend(
            existing(
                repo,
                [
                    "Pevie Hischer/AGENTS.md",
                    "Pevie Hischer/build-system/agents/frontend-implementation-agent.md",
                    "Pevie Hischer/build-system/rules/frontend-proof-matrix.md",
                    "Pevie Hischer/build-system/rules/frontend-production-readiness.md",
                    "Pevie Hischer/build-system/rules/frontend-taste-and-review-standards.md",
                ],
            )
        )

    lines = [
        "# Build Request Kickoff",
        "",
        f"Start in: `{repo.resolve()}`",
        f"Base branch/ref: `{base}`",
        f"Profile: `{profile}`",
        "Frontend profile: `Pevie Hischer`" if profile == "pevie" else "Frontend profile: `not selected`",
        "",
        "## Read First",
        *[f"- `{path}`" for path in read_first],
        "",
        "## Task Source",
        f"- Build request: `{request_rel}`",
        "",
        "## Working Contract",
        "- Treat the build request as the coordinator contract.",
        "- Inspect the repo and current state before editing.",
        "- Keep implementation scoped to the request's in-scope items.",
        "- Run the request's Required Proof before reporting done.",
        "- Capture artifacts, gaps, and the next coordinator action in the completion report.",
        "",
        "## Required Proof Commands",
        *[f"- `{command}`" for command in build_request_commands()],
        "",
        "## Completion Report",
        "Return changed files, commands run, proof status, artifacts, known gaps, and the next coordinator action.",
    ]
    return "\n".join(lines) + "\n"


def build_prompt(
    repo: Path,
    ticket: Path,
    planning_brief: Path | None,
    design: Path | None,
    profile: str,
    base: str,
) -> str:
    ticket_text = read_text(ticket)
    complexity = detect_complexity(ticket_text)
    if complexity == "non-trivial" and planning_brief is None:
        raise SystemExit("Non-trivial tickets require --planning-brief for kickoff generation.")
    if planning_brief is not None:
        read_text(planning_brief)
    if design is not None:
        read_text(design)

    ticket_rel = rel(ticket, repo)
    plan_rel = rel(planning_brief, repo) if planning_brief else None
    design_rel = rel(design, repo) if design else None

    read_first = existing(
        repo,
        [
            "AGENTS.md",
            "build-system/agents/implementation-agent.md",
            "build-system/rules/proof-matrix.md",
        ],
    )
    if profile == "pevie":
        read_first.extend(
            existing(
                repo,
                [
                    "Pevie Hischer/AGENTS.md",
                    "Pevie Hischer/build-system/agents/frontend-implementation-agent.md",
                    "Pevie Hischer/build-system/rules/frontend-proof-matrix.md",
                    "Pevie Hischer/build-system/rules/frontend-production-readiness.md",
                    "Pevie Hischer/build-system/rules/frontend-taste-and-review-standards.md",
                ],
            )
        )

    task_sources = [f"- Ticket: `{ticket_rel}`"]
    if plan_rel:
        task_sources.append(f"- Planning brief: `{plan_rel}`")
    if design_rel:
        task_sources.append(f"- DESIGN.md: `{design_rel}`")

    commands = command_list(profile, ticket_rel, plan_rel, design_rel)

    lines = [
        "# Implementation Agent Kickoff",
        "",
        f"Start in: `{repo.resolve()}`",
        f"Base branch/ref: `{base}`",
        f"Profile: `{profile}`",
        "Frontend profile: `Pevie Hischer`" if profile == "pevie" else "Frontend profile: `not selected`",
        f"Ticket complexity: `{complexity}`",
        "",
        "## Read First",
        *[f"- `{path}`" for path in read_first],
        "",
        "## Task Sources",
        *task_sources,
        "",
        "## Working Contract",
        "- Inspect the repo before editing.",
        "- Keep the patch scoped to the ticket and planning brief.",
        "- Do not rewrite unrelated files or revert user work.",
        "- Map every meaningful risk to proof before reporting done.",
        "- Promote repeated review friction into a durable rule, template, test, or lint.",
        "",
        "## Required Proof Commands",
        *[f"- `{command}`" for command in commands],
        "",
        "## Completion Report",
        "Return changed files, commands run, pass/fail results, known gaps, and the next coordinator action.",
    ]
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."), help="Target repo path.")
    parser.add_argument("--ticket", type=Path, help="Ticket markdown path.")
    parser.add_argument("--build-request", type=Path, help="Build request markdown path.")
    parser.add_argument("--planning-brief", type=Path, help="Planning brief markdown path.")
    parser.add_argument("--design", type=Path, help="DESIGN.md path for Pevie work.")
    parser.add_argument("--profile", choices=["core", "pevie"], default="core")
    parser.add_argument("--base", default="main", help="Base branch/ref for review.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if bool(args.ticket) == bool(args.build_request):
        raise SystemExit("Provide exactly one of --ticket or --build-request.")
    if args.build_request:
        print(
            build_request_prompt(
                repo=args.repo,
                build_request=args.build_request,
                profile=args.profile,
                base=args.base,
            ),
            end="",
        )
        return 0
    print(
        build_prompt(
            repo=args.repo,
            ticket=args.ticket,
            planning_brief=args.planning_brief,
            design=args.design,
            profile=args.profile,
            base=args.base,
        ),
        end="",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
