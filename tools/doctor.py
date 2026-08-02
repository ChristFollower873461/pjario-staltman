#!/usr/bin/env python3
"""Validate Pjario Staltman package or target-repo adoption readiness."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import subprocess
from pathlib import Path


CORE_REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "build-system/README.md",
    "build-system/agents/build-coordinator.md",
    "build-system/agents/implementation-agent.md",
    "build-system/agents/software-engineer-reviewer.md",
    "build-system/rules/review-standards.md",
    "build-system/rules/scale-readiness.md",
    "build-system/rules/proof-matrix.md",
    "build-system/rules/oh-shucksenburg-technical-debt.md",
    "build-system/templates/ticket.md",
    "build-system/templates/planning-brief.md",
    "build-system/templates/build-request.md",
    "build-system/templates/completion-report.md",
    "build-system/templates/pr.md",
    "build-system/templates/qa-plan.md",
    "build-system/templates/garbage-collection.md",
    "tools/check-planning-brief.py",
    "tools/check-proof.py",
    "tools/kickoff.py",
    "tools/review-packet.py",
    "tools/triage-review-finding.py",
    "Makefile",
]

PACKAGE_REQUIRED_FILES = [
    "ADOPTION-CHECKLIST.md",
    "CHANGELOG.md",
    "COMPLETENESS.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "docs/license-posture.md",
    "docs/prerequisites.md",
    "docs/remove-from-target-repo.md",
    "docs/supply-chain.md",
    "docs/trust-contract.md",
    "PUBLICATION-CHECKLIST.md",
    "RESEARCH-NOTES.md",
    "SECURITY.md",
    ".github/workflows/quality.yml",
]

PEVIE_REQUIRED_FILES = [
    "Pevie Hischer/AGENTS.md",
    "Pevie Hischer/README.md",
    "Pevie Hischer/build-system/README.md",
    "Pevie Hischer/build-system/agents/frontend-implementation-agent.md",
    "Pevie Hischer/build-system/agents/frontend-staff-reviewer.md",
    "Pevie Hischer/build-system/rules/frontend-production-readiness.md",
    "Pevie Hischer/build-system/rules/frontend-proof-matrix.md",
    "Pevie Hischer/build-system/rules/oh-shucksenburg-frontend-debt.md",
    "Pevie Hischer/build-system/rules/frontend-taste-and-review-standards.md",
    "Pevie Hischer/build-system/templates/DESIGN.md",
    "Pevie Hischer/build-system/templates/ticket.md",
    "Pevie Hischer/build-system/templates/planning-brief.md",
    "Pevie Hischer/build-system/templates/pr.md",
    "Pevie Hischer/build-system/templates/qa-plan.md",
    "Pevie Hischer/tools/check-design-context.py",
    "Pevie Hischer/tools/check-planning-brief.py",
    "Pevie Hischer/tools/review-packet.py",
    "Pevie Hischer/Makefile",
]

PEVIE_DESIGN_PATHS = [
    "DESIGN.md",
    "docs/product/DESIGN.md",
]

PRIVACY_PATTERNS = [
    (re.compile(r"/Users/[A-Za-z0-9_.-]+"), "local absolute user path"),
    (re.compile(r"\bstandley\b", re.IGNORECASE), "private username"),
    (re.compile(r"\b" + "A" + "IC" + r"\b"), "private organization marker"),
    (re.compile(r"\b" + "A" + "rk" + r"\b"), "private agent name"),
    (re.compile(r"AuthKey_[A-Za-z0-9_]+"), "Apple auth key token pattern"),
    (re.compile(r"SubscriptionKey_[A-Za-z0-9_]+"), "subscription key pattern"),
    (re.compile(r"sk-[A-Za-z0-9_-]{12,}"), "API key pattern"),
    (re.compile(r"gho_[A-Za-z0-9_]+"), "GitHub token pattern"),
    (re.compile(r"AIza[0-9A-Za-z_-]+"), "Google API key pattern"),
    (re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"), "private key block"),
    (
        re.compile(
            r"\b("
            + "|".join(["OPENAI" + "_API_KEY", "GEMINI" + "_API_KEY", "CLOUDFLARE" + "_API_TOKEN"])
            + r")\b"
        ),
        "secret env var",
    ),
]

SCAN_EXCLUDES = {
    ".DS_Store",
    ".review-packet.md",
    "Pevie Hischer/.review-packet.md",
}

STACK_HINTS = {
    "web": [
        "expected host proof: lint, typecheck, unit tests, e2e or browser smoke, accessibility, and performance budget where relevant",
    ],
    "ios": [
        "expected host proof: simulator build/test, manual smoke path, screenshots/logs, signing or bundle identity when release-related",
    ],
    "macos": [
        "expected host proof: build/test, launch smoke, logs, signing/notarization checks when distribution-related",
    ],
    "backend": [
        "expected host proof: unit/integration tests, contract/schema checks, migration/rollback proof, and observability for risky paths",
    ],
}

MIN_PYTHON_VERSION = (3, 11)
REQUIRED_COMMANDS = ["git", "make"]
PEVIE_NETWORK_COMMANDS = ["npx"]


class Report:
    def __init__(self, passes: list[str] | None = None, warnings: list[str] | None = None, failures: list[str] | None = None) -> None:
        self.passes = passes or []
        self.warnings = warnings or []
        self.failures = failures or []

    def pass_(self, message: str) -> None:
        self.passes.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def fail(self, message: str) -> None:
        self.failures.append(message)


def git_files(root: Path, extra_args: list[str] | None = None) -> list[Path] | None:
    args = ["git", "ls-files"]
    if extra_args:
        args.extend(extra_args)
    result = subprocess.run(
        args,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        return None
    return [root / line for line in result.stdout.splitlines() if line.strip()]


def text_files(root: Path) -> list[Path]:
    tracked = git_files(root)
    if tracked is not None:
        untracked = git_files(root, ["--others", "--exclude-standard"]) or []
        candidates = tracked + untracked
    else:
        candidates = [path for path in root.rglob("*") if path.is_file()]
    files: list[Path] = []
    for path in candidates:
        rel = path.relative_to(root).as_posix()
        if rel.startswith(".git/") or rel in SCAN_EXCLUDES or "__pycache__" in path.parts:
            continue
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if b"\0" in data:
            continue
        files.append(path)
    return files


def require_files(root: Path, rels: list[str], report: Report, label: str) -> None:
    missing = [rel for rel in rels if not (root / rel).is_file()]
    if missing:
        report.fail(f"{label} missing files: {', '.join(missing)}")
    else:
        report.pass_(f"{label} required files are present.")


def check_runtime_tools(report: Report, public_ready: bool, profile: str) -> None:
    missing = [command for command in REQUIRED_COMMANDS if shutil.which(command) is None]
    if missing:
        report.fail("Required local commands are missing: " + ", ".join(missing))
    else:
        report.pass_("Required local commands are available.")

    if sys.version_info < MIN_PYTHON_VERSION:
        required = ".".join(str(part) for part in MIN_PYTHON_VERSION)
        current = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        report.fail(f"Python {required}+ is required; current runtime is {current}.")
    else:
        report.pass_("Python runtime is supported.")

    if profile in {"pevie", "both"}:
        missing_network = [command for command in PEVIE_NETWORK_COMMANDS if shutil.which(command) is None]
        if missing_network:
            report.warn(
                "Pevie design linting and make public-ready need npm/npx; missing: "
                + ", ".join(missing_network)
            )
        elif public_ready:
            report.pass_("Pevie npm/npx lint command is available.")


def require_gitignore(root: Path, report: Report) -> None:
    path = root / ".gitignore"
    if not path.is_file():
        report.warn(".gitignore is missing; generated review/export artifacts may be committed by accident.")
        return
    text = path.read_text(encoding="utf-8")
    required = [".review-packet.md", ".dist/", "__pycache__/", "*.pyc"]
    missing = [entry for entry in required if entry not in text]
    if missing:
        report.fail(f".gitignore missing generated-artifact entries: {', '.join(missing)}")
    else:
        report.pass_(".gitignore excludes generated artifacts.")


def require_workflow_root(root: Path, report: Report) -> None:
    workflow_dir = root / ".github" / "workflows"
    workflows = sorted(workflow_dir.glob("*.yml")) + sorted(workflow_dir.glob("*.yaml"))
    if not workflows:
        report.fail("No root .github/workflows/*.yml file found; GitHub will not discover nested workflows.")
        return
    report.pass_("Root GitHub workflow files are present.")

    nested = sorted((root / "Pevie Hischer" / ".github" / "workflows").glob("*.yml"))
    handoff = root / "MAIN-AGENT-HANDOFF.md"
    handoff_text = handoff.read_text(encoding="utf-8").lower() if handoff.is_file() else ""
    if nested and "repo root" not in handoff_text:
        report.warn("Nested Pevie workflow exists, but root-copy guidance was not found in MAIN-AGENT-HANDOFF.md.")


def check_supply_chain_pins(root: Path, report: Report) -> None:
    pevie_makefile = root / "Pevie Hischer" / "Makefile"
    workflow = root / ".github" / "workflows" / "quality.yml"
    pevie_workflow = root / "Pevie Hischer" / ".github" / "workflows" / "pevie-quality.yml"
    supply_chain = root / "docs" / "supply-chain.md"
    missing = [path.relative_to(root).as_posix() for path in [pevie_makefile, workflow, supply_chain] if not path.is_file()]
    if missing:
        report.fail("Supply-chain pin check missing files: " + ", ".join(missing))
        return

    pevie_text = pevie_makefile.read_text(encoding="utf-8")
    workflow_text = workflow.read_text(encoding="utf-8")
    if pevie_workflow.is_file():
        workflow_text += "\n" + pevie_workflow.read_text(encoding="utf-8")
    supply_text = supply_chain.read_text(encoding="utf-8")
    failures: list[str] = []
    design_version_match = re.search(
        r"^DESIGN_MD_VERSION\s*\?=\s*(\d+\.\d+\.\d+)\s*$",
        pevie_text,
        re.MULTILINE,
    )
    if not design_version_match:
        failures.append("Pevie DESIGN_MD_VERSION must be pinned to an exact semantic version.")
    if "@google/design.md@$(DESIGN_MD_VERSION)" not in pevie_text:
        failures.append("Pevie design lint must use the pinned DESIGN_MD_VERSION.")
    if 'python-version: "3.11"' not in workflow_text:
        failures.append("GitHub Actions Python runtime must stay pinned to 3.11.")
    if 'node-version: "24"' not in workflow_text:
        failures.append("GitHub Actions Node runtime must stay pinned to 24.")
    action_uses = re.findall(
        r"uses:\s+actions/(checkout|setup-python|setup-node)@([^\s#]+)",
        workflow_text,
    )
    pinned_actions = {
        action for action, ref in action_uses if re.fullmatch(r"[0-9a-f]{40}", ref)
    }
    required_actions = {"checkout", "setup-python", "setup-node"}
    if pinned_actions != required_actions or any(
        not re.fullmatch(r"[0-9a-f]{40}", ref) for _, ref in action_uses
    ):
        failures.append("GitHub Actions dependencies must use immutable 40-character commit pins.")
    if design_version_match:
        documented_version = f"@google/design.md@{design_version_match.group(1)}"
        if documented_version not in supply_text:
            failures.append(
                "docs/supply-chain.md must document the exact DESIGN_MD_VERSION from the Pevie Makefile."
            )
    if failures:
        for failure in failures:
            report.fail(failure)
    else:
        report.pass_("Supply-chain external tool pins are documented and enforced.")


def require_pevie_design(root: Path, report: Report, mode: str) -> None:
    if mode == "package":
        example_designs = [
            "Pevie Hischer/build-system/templates/DESIGN.md",
            "Pevie Hischer/examples/DESIGN.md",
            "Pevie Hischer/examples/golden-workflow/DESIGN.md",
        ]
        require_files(root, example_designs, report, "Pevie DESIGN.md examples")
        return

    if any((root / rel).is_file() for rel in PEVIE_DESIGN_PATHS):
        report.pass_("Adopted Pevie repo has a DESIGN.md source of truth.")
    else:
        report.fail("Adopted Pevie repo needs DESIGN.md or docs/product/DESIGN.md before UI work.")


def scan_privacy(root: Path, report: Report) -> None:
    findings: list[str] = []
    for path in text_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for pattern, label in PRIVACY_PATTERNS:
                if pattern.search(line):
                    findings.append(f"{rel}:{line_number} ({label})")
                    break
            if len(findings) >= 20:
                break
        if len(findings) >= 20:
            break
    if findings:
        report.fail("Potential private/publication-sensitive strings found: " + "; ".join(findings))
    else:
        report.pass_("Repository text files passed the privacy string scan.")


def check_generated_artifacts_not_tracked(root: Path, report: Report) -> None:
    tracked = git_files(root) or []
    bad = [
        path.relative_to(root).as_posix()
        for path in tracked
        if path.name == ".review-packet.md" or ".dist" in path.parts
    ]
    if bad:
        report.fail("Generated artifacts are tracked: " + ", ".join(bad))
    else:
        report.pass_("Generated review/export artifacts are not tracked.")


def check_publication_docs(root: Path, report: Report) -> None:
    docs = [
        "LICENSE",
        "PUBLICATION-CHECKLIST.md",
        "SECURITY.md",
        "CONTRIBUTING.md",
        "docs/license-posture.md",
        "docs/prerequisites.md",
        "docs/remove-from-target-repo.md",
        "docs/supply-chain.md",
        "docs/trust-contract.md",
    ]
    missing = [rel for rel in docs if not (root / rel).is_file()]
    if missing:
        report.fail("Publication-ready docs are incomplete: " + ", ".join(missing))
    else:
        report.pass_("Publication, security, contribution, and trust docs are present.")

    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").is_file() else ""
    trust = (root / "docs" / "trust-contract.md").read_text(encoding="utf-8") if (root / "docs" / "trust-contract.md").is_file() else ""
    if "make public-ready" not in readme or "make public-ready" not in trust:
        report.fail("README.md and docs/trust-contract.md must document the public-ready gate.")
    license_text = (root / "LICENSE").read_text(encoding="utf-8") if (root / "LICENSE").is_file() else ""
    if "MIT License" not in license_text:
        report.fail("Public reuse requires the approved MIT LICENSE file.")


def add_stack_hints(stack: str, report: Report) -> None:
    for hint in STACK_HINTS.get(stack, []):
        report.warn(hint)


def run_checks(root: Path, mode: str, profile: str, public_ready: bool, stack: str = "generic") -> Report:
    report = Report(passes=[], warnings=[], failures=[])
    check_runtime_tools(report, public_ready, profile)
    require_files(root, CORE_REQUIRED_FILES, report, "Core workflow")
    if mode == "package":
        require_files(root, PACKAGE_REQUIRED_FILES, report, "Package polish")
    if profile in {"pevie", "both"}:
        require_files(root, PEVIE_REQUIRED_FILES, report, "Pevie workflow")
        require_pevie_design(root, report, mode)
    require_workflow_root(root, report)
    if mode == "package":
        check_supply_chain_pins(root, report)
    require_gitignore(root, report)
    check_generated_artifacts_not_tracked(root, report)
    scan_privacy(root, report)
    if public_ready and mode == "package":
        check_publication_docs(root, report)
    add_stack_hints(stack, report)
    return report


def print_report(report: Report) -> None:
    for message in report.passes:
        print(f"PASS: {message}")
    for message in report.warnings:
        print(f"WARN: {message}")
    for message in report.failures:
        print(f"FAIL: {message}")
    print(
        "SUMMARY: "
        f"{len(report.passes)} passed, {len(report.warnings)} warnings, {len(report.failures)} failures."
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Package or target repo root.")
    parser.add_argument("--mode", choices=["package", "adopted"], default="package")
    parser.add_argument("--profile", choices=["core", "pevie", "both"], default="both")
    parser.add_argument("--stack", choices=["generic", "web", "ios", "macos", "backend"], default="generic")
    parser.add_argument("--public-ready", action="store_true", help="Run publication-readiness checks too.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Root does not exist or is not a directory: {root}")
    report = run_checks(root, args.mode, args.profile, args.public_ready, stack=args.stack)
    print_report(report)
    return 1 if report.failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
