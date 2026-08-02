#!/usr/bin/env python3
"""Validate preferred Work Packet proof evidence or legacy ticket artifacts."""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path


NONEISH = {
    "",
    "none",
    "n/a",
    "na",
    "not applicable",
    "not-applicable",
    "not needed",
    "no",
}

RISK_KEYWORDS = {
    "Data writes or migrations": ["data", "migration", "schema", "backfill", "persistence"],
    "Authn/authz": ["auth", "permission", "access", "role", "authorization"],
    "Multi-tenancy": ["tenant", "workspace", "account boundary", "isolation"],
    "External calls": ["external", "timeout", "retry", "rate limit", "api"],
    "Async/background work": ["async", "background", "queue", "job", "worker"],
    "LLM/AI": ["llm", "ai", "model", "prompt", "review packet"],
    "PII/privacy": ["pii", "privacy", "sensitive", "redaction", "secret"],
    "Billing/cost": ["billing", "cost", "invoice", "quota", "meter"],
    "Technical debt/maintainability": [
        "debt",
        "maintainability",
        "duplication",
        "complexity",
        "architecture",
        "coupling",
        "cleanup",
        "todo",
    ],
    "Rollout/rollback": ["rollout", "rollback", "revert", "feature flag", "kill switch"],
}


def read_text(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"Expected file path: {path}")
    return path.read_text(encoding="utf-8")


def section_body(text: str, heading: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s+|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise SystemExit(f"Missing section: ## {heading}")
    return match.group(1).strip()


def is_meaningful(value: str) -> bool:
    normalized = re.sub(r"[\s.]+", " ", value.strip().lower()).strip(" -")
    return normalized not in NONEISH


def active_ticket_risks(ticket_text: str) -> dict[str, str]:
    body = section_body(ticket_text, "Risk Surfaces")
    risks: dict[str, str] = {}
    for line in body.splitlines():
        match = re.match(r"^-\s+(.+?):\s*(.*)$", line.strip())
        if not match:
            continue
        name = match.group(1).strip()
        detail = match.group(2).strip()
        if name in RISK_KEYWORDS and is_meaningful(detail):
            risks[name] = detail
    return risks


def required_proof(ticket_text: str) -> list[str]:
    body = section_body(ticket_text, "Required Proof")
    bullet_items = [
        line.strip("- ").strip()
        for line in body.splitlines()
        if line.strip().startswith("-") and is_meaningful(line.strip("- ").strip())
    ]
    if bullet_items:
        return bullet_items
    return [line.strip() for line in body.splitlines() if is_meaningful(line.strip())]


def proof_text(paths: list[Path]) -> str:
    return "\n".join(read_text(path) for path in paths).lower()


def normalize_evidence(text: str) -> str:
    text = text.replace("`", "")
    return re.sub(r"\s+", " ", text.lower()).strip()


def missing_risk_evidence(risks: dict[str, str], evidence_text: str) -> list[str]:
    missing: list[str] = []
    for risk_name, keywords in RISK_KEYWORDS.items():
        if risk_name not in risks:
            continue
        if not any(keyword in evidence_text for keyword in keywords):
            missing.append(risk_name)
    return missing


def validate(ticket: Path, qa_plan: Path, pr_note: Path, completion_report: Path | None) -> None:
    ticket_text = read_text(ticket)
    proof_items = required_proof(ticket_text)
    if not proof_items:
        raise SystemExit("Ticket Required Proof section is empty.")

    evidence_paths = [qa_plan, pr_note]
    if completion_report is not None:
        evidence_paths.append(completion_report)
    evidence = proof_text(evidence_paths)
    normalized_evidence = normalize_evidence(evidence)

    missing_items = [
        item
        for item in proof_items
        if normalize_evidence(item) not in normalized_evidence
    ]
    if missing_items:
        raise SystemExit(
            "QA/PR/completion evidence is missing ticket Required Proof items: "
            + "; ".join(missing_items)
        )

    risks = active_ticket_risks(ticket_text)
    missing = missing_risk_evidence(risks, evidence)
    if missing:
        raise SystemExit(
            "Evidence is missing proof for active ticket risk surfaces: " + ", ".join(missing)
        )


def validate_work_packet(packet: Path, root: Path | None = None) -> None:
    tool_path = Path(__file__).resolve().with_name("pjario.py")
    spec = importlib.util.spec_from_file_location("pjario_work_packet", tool_path)
    if spec is None or spec.loader is None:
        raise SystemExit("Could not load tools/pjario.py for Work Packet validation.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.load_and_validate((root or Path.cwd()).resolve(), packet, phase="finish")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, help="Preferred Pjario Work Packet path.")
    parser.add_argument("--ticket", type=Path)
    parser.add_argument("--qa-plan", type=Path)
    parser.add_argument("--pr-note", type=Path)
    parser.add_argument("--completion-report", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    legacy_values = (args.ticket, args.qa_plan, args.pr_note, args.completion_report)
    if args.packet:
        if any(value is not None for value in legacy_values):
            raise SystemExit("Use --packet by itself; do not mix Work Packet and legacy proof arguments.")
        validate_work_packet(args.packet)
        print("PASS: Work Packet proof IDs have terminal evidence and valid risk coverage.")
        return 0
    if not all(value is not None for value in (args.ticket, args.qa_plan, args.pr_note)):
        raise SystemExit("Provide --packet, or provide --ticket, --qa-plan, and --pr-note.")
    validate(args.ticket, args.qa_plan, args.pr_note, args.completion_report)
    print("PASS: QA/PR evidence covers ticket proof requirements and active risk surfaces.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
