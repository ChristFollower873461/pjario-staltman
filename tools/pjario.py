#!/usr/bin/env python3
"""Run Pjario's single Work Packet workflow."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA = "pjario.work/v1"
MAX_PACKET_BYTES = 256_000
REQUIRED_METADATA = (
    "Schema",
    "ID",
    "Title",
    "Status",
    "Complexity",
    "Profile",
    "Design Context",
)
REQUIRED_SECTIONS = (
    "Outcome",
    "Scope",
    "Non-Goals",
    "Risk Surfaces",
    "Plan",
    "Proof Requirements",
    "Evidence",
    "Review",
    "Known Gaps",
    "Next Action",
    "Learning",
)
RISK_SURFACES = (
    ("RISK-01", "data-writes"),
    ("RISK-02", "auth"),
    ("RISK-03", "multi-tenancy"),
    ("RISK-04", "external-calls"),
    ("RISK-05", "async-work"),
    ("RISK-06", "llm-ai"),
    ("RISK-07", "privacy"),
    ("RISK-08", "billing-cost"),
    ("RISK-09", "maintainability"),
    ("RISK-10", "rollout-rollback"),
)
STATUSES = {"draft", "active", "ready-for-review", "complete", "blocked"}
COMPLEXITIES = {"trivial", "non-trivial"}
PROFILES = {"core", "frontend"}
EVIDENCE_STATUSES = {"pending", "passed", "failed", "not-run", "accepted-gap"}
REVIEW_DECISIONS = {"pending", "PASS", "PASS WITH FOLLOW-UP", "BLOCK"}

SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    re.compile(
        r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*"
        r"(?:[\"'][A-Za-z0-9_./+=-]{12,}[\"']|[A-Za-z0-9_+=/-]{20,})"
    ),
)
LOCAL_PATH_PATTERN = re.compile(r"(?:^|\s)(?:/Users/|/home/|/private/|/tmp/)[^\s]+")
PLACEHOLDER_PATTERN = re.compile(r"\b(?:TODO|TBD|FILL\s+ME|REPLACE\s+ME)\b", re.IGNORECASE)


def fail(message: str) -> None:
    raise SystemExit(f"pjario: {message}")


def compact(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def safe_single_line(value: str, label: str, maximum: int = 240) -> str:
    normalized = compact(value)
    if not normalized:
        fail(f"{label} must not be empty")
    if len(normalized) > maximum:
        fail(f"{label} exceeds {maximum} characters")
    if any(pattern.search(normalized) for pattern in SECRET_PATTERNS):
        fail(f"{label} looks like it contains a credential")
    if LOCAL_PATH_PATTERN.search(normalized):
        fail(f"{label} contains a local absolute path")
    return normalized


def confined_path(root: Path, raw: Path, label: str, *, must_exist: bool = False) -> Path:
    root_resolved = root.resolve()
    if not root_resolved.is_dir():
        fail(f"root is not a directory: {root}")
    candidate = raw if raw.is_absolute() else root_resolved / raw
    if candidate.exists() and candidate.is_symlink():
        fail(f"{label} must not be a symlink: {raw}")
    resolved = candidate.resolve(strict=False)
    if resolved != root_resolved and root_resolved not in resolved.parents:
        fail(f"{label} must stay inside root: {raw}")
    relative = resolved.relative_to(root_resolved)
    if relative.parts and relative.parts[0] == ".git":
        fail(f"{label} must not be inside .git: {raw}")
    if must_exist and not resolved.is_file():
        fail(f"{label} does not exist: {raw}")
    return resolved


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.is_symlink():
        fail(f"refusing to replace symlinked output: {path}")
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    )
    temp_path = Path(handle.name)
    try:
        with handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)


def template_path() -> Path:
    package_root = Path(__file__).resolve().parents[1]
    candidates = (
        package_root / "build-system" / "templates" / "work-packet.md",
        package_root / "assets" / "work-packet.md",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    fail("work-packet template is missing from the package or exported skill")


def read_packet_text(path: Path) -> str:
    try:
        size = path.stat().st_size
    except OSError as exc:
        fail(f"could not inspect packet {path}: {exc}")
    if size > MAX_PACKET_BYTES:
        fail(f"packet exceeds {MAX_PACKET_BYTES} bytes")
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        fail(f"could not read packet {path}: {exc}")
    if any(pattern.search(text) for pattern in SECRET_PATTERNS):
        fail("packet looks like it contains a credential; redact it before continuing")
    if LOCAL_PATH_PATTERN.search(text):
        fail("packet contains a local absolute path; use repo-relative evidence")
    return text


def split_sections(text: str) -> tuple[dict[str, str], dict[str, str], list[str]]:
    errors: list[str] = []
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE))
    preamble = text[: matches[0].start()] if matches else text
    metadata: dict[str, str] = {}
    for line in preamble.splitlines():
        if line.startswith("#") or not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in metadata:
            errors.append(f"duplicate metadata field: {key}")
        metadata[key] = value.strip()

    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group(1).strip()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        if name in sections:
            errors.append(f"duplicate section: {name}")
        sections[name] = text[match.end() : end].strip()
    return metadata, sections, errors


def meaningful(value: str, *, allow_none: bool = False) -> bool:
    normalized = compact(re.sub(r"^[-*]\s*", "", value, flags=re.MULTILINE)).strip(" .")
    if not normalized or PLACEHOLDER_PATTERN.search(normalized):
        return False
    if not allow_none and normalized.lower() in {"none", "none identified", "none recorded", "n/a", "not applicable"}:
        return False
    return True


@dataclass(frozen=True)
class Risk:
    id: str
    state: str
    surface: str
    notes: str


@dataclass(frozen=True)
class Proof:
    id: str
    risk_ids: tuple[str, ...]
    requirement: str


@dataclass(frozen=True)
class Evidence:
    proof_id: str
    status: str
    detail: str


@dataclass(frozen=True)
class WorkPacket:
    path: Path
    metadata: dict[str, str]
    sections: dict[str, str]
    risks: tuple[Risk, ...]
    proofs: tuple[Proof, ...]
    evidence: tuple[Evidence, ...]
    review_decision: str


def content_lines(section: str) -> list[str]:
    return [line.strip() for line in section.splitlines() if line.strip()]


def parse_risks(section: str, errors: list[str]) -> tuple[Risk, ...]:
    risks: list[Risk] = []
    for line in content_lines(section):
        match = re.fullmatch(
            r"-\s*(RISK-\d{2,})\s*\|\s*(active|inactive)\s*\|\s*([a-z0-9-]+)\s*\|\s*(.+)",
            line,
        )
        if not match:
            errors.append(f"invalid risk line: {line}")
            continue
        risks.append(Risk(*match.groups()))
    expected = list(RISK_SURFACES)
    actual = [(risk.id, risk.surface) for risk in risks]
    if actual != expected:
        errors.append("Risk Surfaces must retain the canonical RISK-01 through RISK-10 IDs and order")
    for risk in risks:
        if risk.state == "active" and not meaningful(risk.notes):
            errors.append(f"{risk.id} is active but has no concrete notes")
    return tuple(risks)


def parse_proofs(section: str, errors: list[str]) -> tuple[Proof, ...]:
    proofs: list[Proof] = []
    seen: set[str] = set()
    for line in content_lines(section):
        match = re.fullmatch(
            r"-\s*(PROOF-\d{2,})\s*\|\s*risks=([^|]+?)\s*\|\s*(.+)",
            line,
        )
        if not match:
            errors.append(f"invalid proof line: {line}")
            continue
        proof_id, raw_risks, requirement = match.groups()
        if proof_id in seen:
            errors.append(f"duplicate proof ID: {proof_id}")
        seen.add(proof_id)
        risk_ids = tuple(item.strip() for item in raw_risks.split(",") if item.strip())
        if not risk_ids or ("none" in risk_ids and risk_ids != ("none",)):
            errors.append(f"{proof_id} must map either `none` or one or more RISK IDs")
        if not meaningful(requirement):
            errors.append(f"{proof_id} has a placeholder requirement")
        proofs.append(Proof(proof_id, risk_ids, requirement))
    if not proofs:
        errors.append("at least one proof requirement is required")
    return tuple(proofs)


def parse_evidence(section: str, errors: list[str]) -> tuple[Evidence, ...]:
    evidence: list[Evidence] = []
    seen: set[str] = set()
    for line in content_lines(section):
        match = re.fullmatch(
            r"-\s*(PROOF-\d{2,})\s*\|\s*([a-z-]+)\s*\|\s*(.+)",
            line,
        )
        if not match:
            errors.append(f"invalid evidence line: {line}")
            continue
        proof_id, status, detail = match.groups()
        if proof_id in seen:
            errors.append(f"duplicate evidence for {proof_id}")
        seen.add(proof_id)
        if status not in EVIDENCE_STATUSES:
            errors.append(f"{proof_id} has invalid evidence status: {status}")
        if status in {"passed", "failed", "accepted-gap"} and not meaningful(detail):
            errors.append(f"{proof_id} status {status} requires concrete evidence")
        evidence.append(Evidence(proof_id, status, detail))
    return tuple(evidence)


def parse_review(section: str, errors: list[str]) -> str:
    match = re.search(r"^Decision:\s*(.+?)\s*$", section, flags=re.MULTILINE)
    if not match:
        errors.append("Review must include `Decision:`")
        return "pending"
    decision = match.group(1).strip()
    if decision not in REVIEW_DECISIONS:
        errors.append("Review decision must be pending, PASS, PASS WITH FOLLOW-UP, or BLOCK")
    return decision


def parse_packet(path: Path) -> tuple[WorkPacket, list[str]]:
    text = read_packet_text(path)
    metadata, sections, errors = split_sections(text)
    missing_metadata = [key for key in REQUIRED_METADATA if key not in metadata]
    if missing_metadata:
        errors.append("missing metadata: " + ", ".join(missing_metadata))
    missing_sections = [name for name in REQUIRED_SECTIONS if name not in sections]
    if missing_sections:
        errors.append("missing sections: " + ", ".join(missing_sections))
    risks = parse_risks(sections.get("Risk Surfaces", ""), errors)
    proofs = parse_proofs(sections.get("Proof Requirements", ""), errors)
    evidence = parse_evidence(sections.get("Evidence", ""), errors)
    decision = parse_review(sections.get("Review", ""), errors)
    return WorkPacket(path, metadata, sections, risks, proofs, evidence, decision), errors


def validation_errors(packet: WorkPacket, *, phase: str = "check") -> list[str]:
    errors: list[str] = []
    metadata = packet.metadata
    if metadata.get("Schema") != SCHEMA:
        errors.append(f"Schema must be {SCHEMA}")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{1,63}", metadata.get("ID", "")):
        errors.append("ID must be 2-64 letters, numbers, dots, underscores, or hyphens")
    if not meaningful(metadata.get("Title", "")):
        errors.append("Title must be concrete")
    if metadata.get("Status") not in STATUSES:
        errors.append("Status must be draft, active, ready-for-review, complete, or blocked")
    if metadata.get("Complexity") not in COMPLEXITIES:
        errors.append("Complexity must be trivial or non-trivial")
    if metadata.get("Profile") not in PROFILES:
        errors.append("Profile must be core or frontend")
    if metadata.get("Profile") == "frontend" and not meaningful(metadata.get("Design Context", "")):
        errors.append("frontend work requires a concrete Design Context path")
    if not meaningful(packet.sections.get("Outcome", "")):
        errors.append("Outcome must be concrete")
    scope = packet.sections.get("Scope", "")
    if not any(meaningful(line) for line in content_lines(scope)):
        errors.append("Scope must contain at least one concrete item")
    if metadata.get("Complexity") == "non-trivial" and not meaningful(packet.sections.get("Plan", "")):
        errors.append("non-trivial work requires a concrete Plan")
    if not meaningful(packet.sections.get("Next Action", "")):
        errors.append("Next Action must be concrete")

    risk_ids = {risk.id for risk in packet.risks}
    proof_ids = {proof.id for proof in packet.proofs}
    evidence_ids = {item.proof_id for item in packet.evidence}
    for proof in packet.proofs:
        unknown = [risk_id for risk_id in proof.risk_ids if risk_id != "none" and risk_id not in risk_ids]
        if unknown:
            errors.append(f"{proof.id} maps unknown risks: {', '.join(unknown)}")
    for risk in packet.risks:
        if risk.state != "active":
            continue
        if not any(risk.id in proof.risk_ids for proof in packet.proofs):
            errors.append(f"{risk.id} is active but no proof requirement maps to it")
    if evidence_ids != proof_ids:
        missing = sorted(proof_ids - evidence_ids)
        extra = sorted(evidence_ids - proof_ids)
        if missing:
            errors.append("missing evidence rows for: " + ", ".join(missing))
        if extra:
            errors.append("evidence references unknown proofs: " + ", ".join(extra))

    if phase == "finish":
        for item in packet.evidence:
            if item.status in {"pending", "not-run", "failed"}:
                errors.append(f"{item.proof_id} is not satisfied: {item.status}")
        accepted_gaps = [item for item in packet.evidence if item.status == "accepted-gap"]
        if accepted_gaps and not meaningful(packet.sections.get("Known Gaps", "")):
            errors.append("accepted-gap evidence requires a concrete Known Gaps section")
        if metadata.get("Status") != "complete":
            errors.append("finish requires Status: complete")
        if packet.review_decision not in {"PASS", "PASS WITH FOLLOW-UP"}:
            errors.append("finish requires a passing review decision")
        if packet.review_decision == "PASS WITH FOLLOW-UP" and not meaningful(
            packet.sections.get("Known Gaps", "")
        ):
            errors.append("PASS WITH FOLLOW-UP requires a concrete Known Gaps section")
    return errors


def load_and_validate(root: Path, raw: Path, *, phase: str = "check") -> WorkPacket:
    path = confined_path(root, raw, "work packet", must_exist=True)
    packet, errors = parse_packet(path)
    errors.extend(validation_errors(packet, phase=phase))
    if errors:
        fail("work packet failed validation:\n- " + "\n- ".join(dict.fromkeys(errors)))
    return packet


def proof_defaults(complexity: str) -> tuple[str, str]:
    if complexity == "trivial":
        proofs = "- PROOF-01 | risks=none | Verify the scoped outcome and targeted diff."
        evidence = "- PROOF-01 | pending | -"
        return proofs, evidence
    proofs = "\n".join(
        (
            "- PROOF-01 | risks=none | Run the relevant automated checks.",
            "- PROOF-02 | risks=none | Verify one meaningful failure path or boundary.",
            "- PROOF-03 | risks=RISK-10 | Document rollout and rollback behavior.",
        )
    )
    evidence = "\n".join(
        (
            "- PROOF-01 | pending | -",
            "- PROOF-02 | pending | -",
            "- PROOF-03 | pending | -",
        )
    )
    return proofs, evidence


def start_packet(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    packet_id = safe_single_line(args.id, "id", maximum=64)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{1,63}", packet_id):
        fail("id must use letters, numbers, dots, underscores, or hyphens")
    title = safe_single_line(args.title, "title")
    outcome = safe_single_line(args.outcome, "outcome", maximum=500)
    design = safe_single_line(
        args.design or ("DESIGN.md" if args.profile == "frontend" else "Not applicable."),
        "design context",
        maximum=500,
    )
    plan = (
        "Not required for trivial work."
        if args.complexity == "trivial"
        else "TODO: Describe the approach, dependencies, failure boundaries, rollout, and rollback."
    )
    proofs, evidence = proof_defaults(args.complexity)
    replacements = {
        "{{ID}}": packet_id,
        "{{TITLE}}": title,
        "{{COMPLEXITY}}": args.complexity,
        "{{PROFILE}}": args.profile,
        "{{DESIGN_CONTEXT}}": design,
        "{{OUTCOME}}": outcome,
        "{{PLAN}}": plan,
        "{{PROOF_REQUIREMENTS}}": proofs,
        "{{EVIDENCE}}": evidence,
    }
    text = template_path().read_text(encoding="utf-8")
    for token, value in replacements.items():
        text = text.replace(token, value)
    unresolved = sorted(set(re.findall(r"{{[A-Z_]+}}", text)))
    if unresolved:
        fail("template contains unresolved tokens: " + ", ".join(unresolved))
    raw_output = args.output or Path(f".pjario/work/{packet_id}.md")
    output = confined_path(root, raw_output, "work packet output")
    if output.exists() and not args.force:
        fail(f"output exists: {output.relative_to(root)}; use --force to replace it")
    atomic_write(output, text)
    print(f"pjario: created {output.relative_to(root)}")
    print(f"pjario: next: fill Scope and remaining TODOs, then run `pjario check --packet {output.relative_to(root)}`")
    return 0


def check_packet(args: argparse.Namespace) -> int:
    packet = load_and_validate(args.root.resolve(), args.packet, phase="check")
    active = sum(1 for risk in packet.risks if risk.state == "active")
    print(
        f"PASS: {packet.metadata['ID']} is structurally ready "
        f"({packet.metadata['Complexity']}, {active} active risks, {len(packet.proofs)} proof requirements)."
    )
    return 0


def find_helper(root: Path, name: str) -> Path:
    source_dir = Path(__file__).resolve().parent
    candidates = (
        source_dir / f"{name}.py",
        source_dir / name,
        root / "tools" / f"{name}.py",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    fail(f"could not locate the bundled {name} helper")


def run_review(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    packet = load_and_validate(root, args.packet, phase="check")
    output = confined_path(root, args.output, "review packet output")
    helper = find_helper(root, "review-packet")
    command = [
        sys.executable,
        str(helper),
        "--context",
        packet.path.relative_to(root).as_posix(),
        "--output",
        output.relative_to(root).as_posix(),
    ]
    if args.base:
        command.extend(("--base", args.base))
    if args.cached:
        command.append("--cached")
    if args.include_untracked:
        command.append("--include-untracked")
    result = subprocess.run(command, cwd=root, text=True, check=False)
    if result.returncode != 0:
        fail(f"review packet generation failed with status {result.returncode}")
    return 0


def completion_payload(root: Path, packet: WorkPacket) -> dict[str, Any]:
    counts = {status: 0 for status in EVIDENCE_STATUSES}
    for item in packet.evidence:
        counts[item.status] += 1
    if packet.review_decision in {"PASS", "PASS WITH FOLLOW-UP"}:
        disposition = "complete" if packet.review_decision == "PASS" else "complete-with-follow-up"
    else:
        disposition = "ready-for-review"
    return {
        "schema_version": "pjario.completion/v1",
        "packet": packet.path.relative_to(root).as_posix(),
        "id": packet.metadata["ID"],
        "title": packet.metadata["Title"],
        "disposition": disposition,
        "review_decision": packet.review_decision,
        "proof": counts,
        "known_gaps": packet.sections["Known Gaps"],
        "next_action": packet.sections["Next Action"],
    }


def render_completion_markdown(payload: dict[str, Any]) -> str:
    proof = payload["proof"]
    return f"""# Pjario Completion Summary

- Packet: `{payload['packet']}`
- Work ID: `{payload['id']}`
- Title: {payload['title']}
- Disposition: `{payload['disposition']}`
- Review: `{payload['review_decision']}`
- Proof: {proof['passed']} passed, {proof['accepted-gap']} accepted gaps

## Known Gaps

{payload['known_gaps']}

## Next Action

{payload['next_action']}
"""


def finish_packet(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    packet = load_and_validate(root, args.packet, phase="finish")
    payload = completion_payload(root, packet)
    rendered = (
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if args.format == "json"
        else render_completion_markdown(payload)
    )
    if args.output:
        output = confined_path(root, args.output, "completion output")
        if output == packet.path:
            fail("completion output must not overwrite the Work Packet")
        atomic_write(output, rendered)
        print(f"pjario: wrote {output.relative_to(root)}")
    else:
        print(rendered, end="")
    return 0


def run_learning(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    quiet_args = list(args.quiet_args)
    if quiet_args and quiet_args[0] == "--":
        quiet_args.pop(0)
    if not quiet_args or quiet_args[0] not in {"record", "report", "propose"}:
        fail("learn requires a Quiet Aggregate command: record, report, or propose")
    if "--root" not in quiet_args:
        quiet_args[1:1] = ["--root", str(root)]
    helper = find_helper(root, "quiet-aggregate")
    result = subprocess.run([sys.executable, str(helper), *quiet_args], cwd=root, text=True, check=False)
    if result.returncode != 0:
        fail(f"Quiet Aggregate failed with status {result.returncode}")
    return 0


def adoption_items(target: Path, profile: str) -> list[dict[str, str]]:
    git_ok = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=target,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0
    def marker_action(path: str) -> str:
        return "KEEP" if (target / path).is_file() else "ADD"

    def optional_text(path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8") if path.is_file() else ""
        except (OSError, UnicodeDecodeError):
            return ""

    agents_text = optional_text(target / "AGENTS.md")
    agents_ready = "pjario.work/v1" in agents_text or "Pjario Work Packet" in agents_text

    items = [
        {"action": "KEEP" if git_ok else "REVIEW", "path": ".", "reason": "target is a Git worktree"},
        {
            "action": "KEEP" if agents_ready else ("REVIEW" if (target / "AGENTS.md").is_file() else "ADD"),
            "path": "AGENTS.md",
            "reason": "merge Pjario operating rules with repository-owned instructions",
        },
        {
            "action": marker_action("build-system/templates/work-packet.md"),
            "path": "build-system/",
            "reason": "versioned Work Packet, agent prompts, and engineering rules",
        },
        {
            "action": marker_action("tools/pjario.py"),
            "path": "tools/pjario.py",
            "reason": "single Work Packet command surface",
        },
        {
            "action": marker_action("tools/review-packet.py"),
            "path": "tools/review-packet.py",
            "reason": "bounded review context with mandatory work and diff inputs",
        },
        {
            "action": marker_action("tools/quiet-aggregate.py"),
            "path": "tools/quiet-aggregate.py",
            "reason": "private recurrence ledger and non-mutating proposals",
        },
        {
            "action": marker_action("tests/test_pjario.py"),
            "path": "tests/",
            "reason": "behavior, safety, export, and compatibility checks",
        },
        {
            "action": marker_action("evals/skill-behavior.json"),
            "path": "evals/skill-behavior.json",
            "reason": "deterministic skill routing and learning boundaries",
        },
    ]
    gitignore = optional_text(target / ".gitignore")
    ignore_ready = all(
        entry in gitignore for entry in (".pjario/*", "!.pjario/work/", "!.pjario/work/*.md")
    )
    items.append(
        {
            "action": "KEEP" if ignore_ready else "ADD",
            "path": ".gitignore",
            "reason": "ignore private runtime state while tracking Work Packets",
        }
    )
    makefile = target / "Makefile"
    make_text = optional_text(makefile)
    make_ready = "check-work:" in make_text and "finish-work:" in make_text
    items.extend(
        (
            {
                "action": "KEEP" if make_ready else ("REVIEW" if makefile.is_file() else "ADD"),
                "path": "Makefile",
                "reason": "merge Pjario targets without replacing host build commands",
            },
            {
                "action": "REVIEW",
                "path": ".github/workflows/",
                "reason": "add changed-packet and host-app checks only after local adoption passes",
            },
        )
    )
    if profile == "frontend":
        items.extend(
            (
                {
                    "action": marker_action("Pevie Hischer/build-system/templates/DESIGN.md"),
                    "path": "Pevie Hischer/",
                    "reason": "frontend implementation, review, and validation profile",
                },
                {
                    "action": "KEEP" if (target / "DESIGN.md").is_file() else "ADD",
                    "path": "DESIGN.md",
                    "reason": "Pevie frontend design contract",
                },
            )
        )
    return items


def adoption_dry_run(args: argparse.Namespace) -> int:
    if not args.dry_run:
        fail("adopt is dry-run-only; pass --dry-run and review the proposed file operations")
    target = args.target.resolve()
    if not target.is_dir():
        fail(f"adoption target is not a directory: {target}")
    items = adoption_items(target, args.profile)
    if args.format == "json":
        print(json.dumps({"profile": args.profile, "target": str(target), "items": items}, indent=2))
        return 0
    print("# Pjario Adoption Dry Run\n")
    print(f"- Target: `{target}`")
    print(f"- Profile: `{args.profile}`")
    print("- Mutation: `none`\n")
    for item in items:
        print(f"- {item['action']}: `{item['path']}` — {item['reason']}")
    return 0


def add_root(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", type=Path, default=Path("."), help="Target repository root.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start", help="Create one progressive Work Packet.")
    add_root(start)
    start.add_argument("--id", required=True)
    start.add_argument("--title", required=True)
    start.add_argument("--outcome", required=True)
    start.add_argument("--complexity", choices=sorted(COMPLEXITIES), required=True)
    start.add_argument("--profile", choices=sorted(PROFILES), default="core")
    start.add_argument("--design")
    start.add_argument("--output", type=Path)
    start.add_argument("--force", action="store_true")

    check = subparsers.add_parser("check", help="Validate planning and risk-to-proof readiness.")
    add_root(check)
    check.add_argument("--packet", type=Path, required=True)

    review = subparsers.add_parser("review", help="Build a review packet with Work Packet context.")
    add_root(review)
    review.add_argument("--packet", type=Path, required=True)
    review.add_argument("--output", type=Path, default=Path(".pjario/review-packet.md"))
    review.add_argument("--base")
    review.add_argument("--cached", action="store_true")
    review.add_argument("--include-untracked", action="store_true")

    finish = subparsers.add_parser("finish", help="Validate evidence and render a completion summary.")
    add_root(finish)
    finish.add_argument("--packet", type=Path, required=True)
    finish.add_argument("--format", choices=("markdown", "json"), default="markdown")
    finish.add_argument("--output", type=Path)

    learn = subparsers.add_parser("learn", help="Run Quiet Aggregate through the Pjario entry point.")
    add_root(learn)
    learn.add_argument("quiet_args", nargs=argparse.REMAINDER)

    adopt = subparsers.add_parser("adopt", help="Inspect a target repo without mutating it.")
    adopt.add_argument("--target", type=Path, default=Path("."))
    adopt.add_argument("--profile", choices=sorted(PROFILES), default="core")
    adopt.add_argument("--dry-run", action="store_true")
    adopt.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    handlers = {
        "start": start_packet,
        "check": check_packet,
        "review": run_review,
        "finish": finish_packet,
        "learn": run_learning,
        "adopt": adoption_dry_run,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
