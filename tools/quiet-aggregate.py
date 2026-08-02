#!/usr/bin/env python3
"""Record verified review findings and propose guardrails when they repeat."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any


FINDING_SCHEMA = "quiet-aggregate.finding/v1"
REPORT_SCHEMA = "quiet-aggregate.report/v1"
DEFAULT_LEDGER = Path(".pjario/quiet-aggregate.jsonl")
MAX_LEDGER_BYTES = 10_000_000
MAX_REPORT_BYTES = 2_000_000
MAX_RECORDS = 10_000
MAX_EVIDENCE_ITEMS = 20

PRIORITIES = ("P0", "P1", "P2", "P3")
CATEGORIES = ("bug", "security", "regression", "test_gap", "maintainability")
DISPOSITIONS = ("actionable", "follow-up", "rejected")
SOURCE_KINDS = ("autoreview", "human-review", "ci", "other")
DURABLE_FIXES = (
    "undecided",
    "rule",
    "template",
    "test",
    "lint",
    "runtime-guardrail",
    "tooling",
    "accepted-non-rule",
)
PROMOTION_DECISIONS = tuple(value for value in DURABLE_FIXES if value not in {"undecided", "accepted-non-rule"})
PRIORITY_ORDER = {priority: index for index, priority in enumerate(PRIORITIES)}

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
LOCAL_PATH_PATTERN = re.compile(r"(?:^|\s)(?:/Users/|/home/)[^\s]+")


def fail(message: str) -> None:
    raise SystemExit(f"quiet aggregate: {message}")


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def validate_text(value: Any, label: str, *, maximum: int, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        fail(f"{label} must be text")
    normalized = compact(value)
    if not normalized and not allow_empty:
        fail(f"{label} must not be empty")
    if len(normalized) > maximum:
        fail(f"{label} exceeds {maximum} characters")
    if any(pattern.search(normalized) for pattern in SECRET_PATTERNS):
        fail(f"{label} looks like it contains a credential; redact it before recording")
    if LOCAL_PATH_PATTERN.search(normalized):
        fail(f"{label} contains a local absolute path; use a repo-relative reference")
    return normalized


def validate_label(value: Any, label: str) -> str:
    normalized = validate_text(value, label, maximum=100)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", normalized):
        fail(f"{label} must use letters, numbers, dots, slashes, underscores, or hyphens")
    return normalized


def validate_observed_at(value: Any) -> str:
    text = validate_text(value, "observed_at", maximum=40)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        fail("observed_at must be an ISO-8601 timestamp")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        fail("observed_at must include a timezone")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def validate_repo_relative(value: Any, label: str) -> str:
    text = validate_text(value, label, maximum=500)
    normalized = text.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts or re.match(r"^[A-Za-z]:/", normalized):
        fail(f"{label} must be repo-relative")
    if not path.parts:
        fail(f"{label} must identify a file")
    return path.as_posix()


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
        fail(f"{label} must not write inside .git: {raw}")
    if must_exist and not resolved.is_file():
        fail(f"{label} does not exist: {raw}")
    return resolved


def atomic_write_text(path: Path, text: str) -> None:
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


def read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        size = path.stat().st_size
    except OSError as exc:
        fail(f"could not inspect {label} {path}: {exc}")
    if size > MAX_REPORT_BYTES:
        fail(f"{label} exceeds {MAX_REPORT_BYTES} bytes")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"could not read {label} {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{label} must contain one JSON object")
    return value


def validate_autoreview_finding(report: dict[str, Any], index: int) -> dict[str, Any]:
    findings = report.get("findings")
    if not isinstance(findings, list):
        fail("autoreview report must contain a findings array")
    if index < 0 or index >= len(findings):
        fail(f"finding index {index} is outside the report's {len(findings)} findings")
    finding = findings[index]
    if not isinstance(finding, dict):
        fail(f"autoreview finding {index} must be an object")
    required = {"title", "body", "priority", "confidence", "category", "code_location"}
    if set(finding) != required:
        fail(f"autoreview finding {index} has unexpected keys")
    if finding.get("priority") not in PRIORITIES:
        fail(f"autoreview finding {index} has an invalid priority")
    if finding.get("category") not in CATEGORIES:
        fail(f"autoreview finding {index} has an invalid category")
    confidence = finding.get("confidence")
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        fail(f"autoreview finding {index} has an invalid confidence")
    location = finding.get("code_location")
    if not isinstance(location, dict) or set(location) != {"file_path", "line"}:
        fail(f"autoreview finding {index} has an invalid code_location")
    line = location.get("line")
    if isinstance(line, bool) or not isinstance(line, int) or line < 1:
        fail(f"autoreview finding {index} has an invalid line")
    return {
        "title": validate_text(finding.get("title"), "finding title", maximum=140),
        "summary": validate_text(finding.get("body"), "finding body", maximum=2000),
        "priority": finding["priority"],
        "confidence": float(confidence),
        "category": finding["category"],
        "code_location": {
            "file_path": validate_repo_relative(location.get("file_path"), "finding file path"),
            "line": line,
        },
    }


def normalize_fingerprint_part(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def digest_id(prefix: str, value: dict[str, Any] | list[Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(payload).hexdigest()[:16]}"


def build_record(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    if args.from_autoreview:
        report_path = confined_path(root, args.from_autoreview, "autoreview report", must_exist=True)
        finding = validate_autoreview_finding(read_json(report_path, "autoreview report"), args.finding_index)
        source_kind = args.source_kind or "autoreview"
    else:
        missing = [
            option
            for option, value in (
                ("--title", args.title),
                ("--summary", args.summary),
                ("--priority", args.priority),
                ("--category", args.category),
                ("--file-path", args.file_path),
                ("--line", args.line),
            )
            if value is None
        ]
        if missing:
            fail("manual records require " + ", ".join(missing))
        if isinstance(args.line, bool) or args.line < 1:
            fail("line must be at least 1")
        finding = {
            "title": validate_text(args.title, "finding title", maximum=140),
            "summary": validate_text(args.summary, "finding summary", maximum=2000),
            "priority": args.priority,
            "confidence": args.confidence,
            "category": args.category,
            "code_location": {
                "file_path": validate_repo_relative(args.file_path, "finding file path"),
                "line": args.line,
            },
        }
        source_kind = args.source_kind or "human-review"

    if source_kind not in SOURCE_KINDS:
        fail(f"unsupported source kind: {source_kind}")
    source_ref = validate_text(args.source_ref, "source ref", maximum=240)
    reviewer = validate_text(args.reviewer or "unspecified", "reviewer", maximum=100)
    failure_class = validate_label(args.failure_class, "failure class")
    owner_boundary = validate_label(args.owner_boundary, "owner boundary")
    observed_at = validate_observed_at(
        args.observed_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    )
    evidence = [validate_text(item, "evidence", maximum=500) for item in args.evidence]
    if len(evidence) > MAX_EVIDENCE_ITEMS:
        fail(f"evidence is limited to {MAX_EVIDENCE_ITEMS} items")
    if not evidence:
        location = finding["code_location"]
        evidence = [f"{location['file_path']}:{location['line']}"]

    identity = {
        "source_kind": source_kind,
        "source_ref": source_ref,
        "title": finding["title"],
        "file_path": finding["code_location"]["file_path"],
        "line": finding["code_location"]["line"],
    }
    fingerprint_input = {
        "failure_class": normalize_fingerprint_part(failure_class),
        "owner_boundary": normalize_fingerprint_part(owner_boundary),
    }
    return {
        "schema_version": FINDING_SCHEMA,
        "id": digest_id("qaf", identity),
        "fingerprint": digest_id("qac", fingerprint_input),
        "observed_at": observed_at,
        "source": {"kind": source_kind, "ref": source_ref, "reviewer": reviewer},
        **finding,
        "classification": {
            "disposition": args.disposition,
            "failure_class": failure_class,
            "owner_boundary": owner_boundary,
            "durable_fix": args.durable_fix,
        },
        "evidence": evidence,
    }


def validate_record(value: Any, line_number: int | None = None) -> dict[str, Any]:
    where = f" on ledger line {line_number}" if line_number is not None else ""
    if not isinstance(value, dict):
        fail(f"finding record{where} must be an object")
    required = {
        "schema_version",
        "id",
        "fingerprint",
        "observed_at",
        "source",
        "title",
        "summary",
        "priority",
        "confidence",
        "category",
        "code_location",
        "classification",
        "evidence",
    }
    if set(value) != required:
        fail(f"finding record{where} has unexpected or missing keys")
    if value.get("schema_version") != FINDING_SCHEMA:
        fail(f"finding record{where} uses an unsupported schema")
    if not re.fullmatch(r"qaf-[0-9a-f]{16}", str(value.get("id", ""))):
        fail(f"finding record{where} has an invalid id")
    if not re.fullmatch(r"qac-[0-9a-f]{16}", str(value.get("fingerprint", ""))):
        fail(f"finding record{where} has an invalid fingerprint")
    validate_observed_at(value.get("observed_at"))
    validate_text(value.get("title"), "finding title", maximum=140)
    validate_text(value.get("summary"), "finding summary", maximum=2000)
    if value.get("priority") not in PRIORITIES:
        fail(f"finding record{where} has an invalid priority")
    confidence = value.get("confidence")
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        fail(f"finding record{where} has an invalid confidence")
    if value.get("category") not in CATEGORIES:
        fail(f"finding record{where} has an invalid category")

    source = value.get("source")
    if not isinstance(source, dict) or set(source) != {"kind", "ref", "reviewer"}:
        fail(f"finding record{where} has an invalid source")
    if source.get("kind") not in SOURCE_KINDS:
        fail(f"finding record{where} has an invalid source kind")
    validate_text(source.get("ref"), "source ref", maximum=240)
    validate_text(source.get("reviewer"), "reviewer", maximum=100)

    location = value.get("code_location")
    if not isinstance(location, dict) or set(location) != {"file_path", "line"}:
        fail(f"finding record{where} has an invalid code location")
    validate_repo_relative(location.get("file_path"), "finding file path")
    if isinstance(location.get("line"), bool) or not isinstance(location.get("line"), int) or location["line"] < 1:
        fail(f"finding record{where} has an invalid line")

    classification = value.get("classification")
    if not isinstance(classification, dict) or set(classification) != {
        "disposition",
        "failure_class",
        "owner_boundary",
        "durable_fix",
    }:
        fail(f"finding record{where} has an invalid classification")
    if classification.get("disposition") not in DISPOSITIONS:
        fail(f"finding record{where} has an invalid disposition")
    validate_label(classification.get("failure_class"), "failure class")
    validate_label(classification.get("owner_boundary"), "owner boundary")
    if classification.get("durable_fix") not in DURABLE_FIXES:
        fail(f"finding record{where} has an invalid durable fix")

    evidence = value.get("evidence")
    if not isinstance(evidence, list) or len(evidence) > MAX_EVIDENCE_ITEMS:
        fail(f"finding record{where} has invalid evidence")
    for item in evidence:
        validate_text(item, "evidence", maximum=500)

    expected_fingerprint = digest_id(
        "qac",
        {
            "failure_class": normalize_fingerprint_part(classification["failure_class"]),
            "owner_boundary": normalize_fingerprint_part(classification["owner_boundary"]),
        },
    )
    if value["fingerprint"] != expected_fingerprint:
        fail(f"finding record{where} fingerprint does not match its classification")
    expected_id = digest_id(
        "qaf",
        {
            "source_kind": source["kind"],
            "source_ref": source["ref"],
            "title": value["title"],
            "file_path": location["file_path"],
            "line": location["line"],
        },
    )
    if value["id"] != expected_id:
        fail(f"finding record{where} id does not match its observation identity")
    return value


def load_ledger(path: Path, *, missing_ok: bool = False) -> list[dict[str, Any]]:
    if not path.exists():
        if missing_ok:
            return []
        fail(f"ledger does not exist: {path}")
    if path.is_symlink():
        fail(f"ledger must not be a symlink: {path}")
    if path.stat().st_size > MAX_LEDGER_BYTES:
        fail(f"ledger exceeds {MAX_LEDGER_BYTES} bytes")
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        fail(f"could not read ledger {path}: {exc}")
    if len(lines) > MAX_RECORDS:
        fail(f"ledger exceeds {MAX_RECORDS} records")
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"ledger line {line_number} is invalid JSON: {exc}")
        record = validate_record(value, line_number)
        if record["id"] in seen:
            fail(f"ledger contains duplicate id {record['id']}")
        seen.add(record["id"])
        records.append(record)
    return records


def write_ledger(path: Path, records: list[dict[str, Any]]) -> None:
    if len(records) > MAX_RECORDS:
        fail(f"ledger exceeds {MAX_RECORDS} records")
    text = "".join(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n" for record in records)
    if len(text.encode("utf-8")) > MAX_LEDGER_BYTES:
        fail(f"ledger exceeds {MAX_LEDGER_BYTES} bytes")
    atomic_write_text(path, text)


def record_finding(path: Path, record: dict[str, Any], *, replace: bool = False) -> str:
    validate_record(record)
    records = load_ledger(path, missing_ok=True)
    for index, existing in enumerate(records):
        if existing["id"] != record["id"]:
            continue
        if existing == record:
            return "unchanged"
        if not replace:
            fail(f"finding {record['id']} already exists with different data; rerun with --replace")
        records[index] = record
        write_ledger(path, records)
        return "replaced"
    records.append(record)
    write_ledger(path, records)
    return "recorded"


def choose_recommendation(records: list[dict[str, Any]]) -> str:
    votes = Counter(
        record["classification"]["durable_fix"]
        for record in records
        if record["classification"]["durable_fix"] != "undecided"
    )
    if not votes:
        return "human-decision-required"
    if set(votes) == {"accepted-non-rule"}:
        return "revisit-accepted-non-rule"
    ranked = votes.most_common()
    if len(ranked) > 1 and ranked[0][1] == ranked[1][1]:
        return "human-decision-required"
    return ranked[0][0]


def build_report(records: list[dict[str, Any]], min_count: int) -> dict[str, Any]:
    if min_count < 2:
        fail("min-count must be at least 2")
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        if record["classification"]["disposition"] == "actionable":
            groups[record["fingerprint"]].append(record)

    candidates: list[dict[str, Any]] = []
    for fingerprint, grouped in groups.items():
        ordered = sorted(grouped, key=lambda item: (item["observed_at"], item["id"]))
        source_refs = sorted({item["source"]["ref"] for item in ordered})
        recommendation = choose_recommendation(ordered)
        ready = (
            len(ordered) >= min_count
            and len(source_refs) >= min_count
            and recommendation != "revisit-accepted-non-rule"
        )
        classification = ordered[0]["classification"]
        candidates.append(
            {
                "fingerprint": fingerprint,
                "failure_class": classification["failure_class"],
                "owner_boundary": classification["owner_boundary"],
                "occurrence_count": len(ordered),
                "source_count": len(source_refs),
                "first_seen": ordered[0]["observed_at"],
                "last_seen": ordered[-1]["observed_at"],
                "priorities": sorted(
                    {item["priority"] for item in ordered}, key=PRIORITY_ORDER.get
                ),
                "categories": sorted({item["category"] for item in ordered}),
                "source_refs": source_refs,
                "finding_ids": [item["id"] for item in ordered],
                "titles": sorted({item["title"] for item in ordered}),
                "recommended_fix": recommendation,
                "ready_for_promotion": ready,
            }
        )
    candidates.sort(
        key=lambda item: (
            not item["ready_for_promotion"],
            -item["source_count"],
            -item["occurrence_count"],
            item["fingerprint"],
        )
    )
    dispositions = Counter(record["classification"]["disposition"] for record in records)
    return {
        "schema_version": REPORT_SCHEMA,
        "finding_schema_version": FINDING_SCHEMA,
        "min_count": min_count,
        "totals": {
            "records": len(records),
            "actionable": dispositions["actionable"],
            "follow_up": dispositions["follow-up"],
            "rejected": dispositions["rejected"],
            "candidate_classes": len(candidates),
            "ready_for_promotion": sum(1 for item in candidates if item["ready_for_promotion"]),
        },
        "candidates": candidates,
    }


def markdown_code(value: str) -> str:
    return value.replace("`", "'")


def render_report_markdown(report: dict[str, Any]) -> str:
    totals = report["totals"]
    lines = [
        "# Quiet Aggregate Report",
        "",
        f"- Records: {totals['records']}",
        f"- Actionable: {totals['actionable']}",
        f"- Follow-up: {totals['follow_up']}",
        f"- Rejected: {totals['rejected']}",
        f"- Ready for promotion: {totals['ready_for_promotion']}",
        "",
    ]
    if not report["candidates"]:
        lines.extend(["No actionable finding classes recorded yet.", ""])
        return "\n".join(lines)
    for candidate in report["candidates"]:
        state = "READY" if candidate["ready_for_promotion"] else "WATCH"
        lines.extend(
            [
                f"## {state}: {candidate['failure_class']}",
                "",
                f"- Fingerprint: `{candidate['fingerprint']}`",
                f"- Owner boundary: `{markdown_code(candidate['owner_boundary'])}`",
                f"- Occurrences: {candidate['occurrence_count']} across {candidate['source_count']} sources",
                f"- Priorities: {', '.join(candidate['priorities'])}",
                f"- Recommended fix: `{candidate['recommended_fix']}`",
                f"- Sources: {', '.join(f'`{markdown_code(ref)}`' for ref in candidate['source_refs'])}",
                "",
            ]
        )
    return "\n".join(lines)


def build_proposal(candidate: dict[str, Any], decision: str, owner: str) -> str:
    source_evidence = "\n".join(
        f"- `{markdown_code(ref)}`" for ref in candidate["source_refs"]
    )
    return f"""# Quiet Aggregate Guardrail Proposal

Status: proposed, not applied

## Repeated Friction

- Failure class: {candidate['failure_class']}
- Owner boundary: `{markdown_code(candidate['owner_boundary'])}`
- Fingerprint: `{candidate['fingerprint']}`
- Occurrences: {candidate['occurrence_count']} across {candidate['source_count']} independent sources
- Priorities: {', '.join(candidate['priorities'])}

## Consolidated Decision

- Durable fix: {decision}
- Owner: `{markdown_code(owner)}`
- Quiet Aggregate does not edit rules, tests, templates, or runtime policy automatically. A human or implementation agent must review and apply this proposal.

## Source Evidence

{source_evidence}

## Acceptance Criteria

- The selected guardrail catches this failure class before staff review.
- Existing behavior still passes its relevant proof.
- The applied change references this fingerprint for auditability.
"""


def add_common_path_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root.")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER, help="Repo-relative JSONL ledger.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    record = subparsers.add_parser("record", help="Record one verified finding.")
    add_common_path_args(record)
    record.add_argument("--from-autoreview", type=Path, help="Validated autoreview JSON report.")
    record.add_argument("--finding-index", type=int, default=0)
    record.add_argument("--title")
    record.add_argument("--summary")
    record.add_argument("--priority", choices=PRIORITIES)
    record.add_argument("--confidence", type=float, default=1.0)
    record.add_argument("--category", choices=CATEGORIES)
    record.add_argument("--file-path")
    record.add_argument("--line", type=int)
    record.add_argument("--source-kind", choices=SOURCE_KINDS)
    record.add_argument("--source-ref", required=True)
    record.add_argument("--reviewer")
    record.add_argument("--observed-at")
    record.add_argument("--disposition", choices=DISPOSITIONS, default="actionable")
    record.add_argument("--failure-class", required=True)
    record.add_argument("--owner-boundary", required=True)
    record.add_argument("--durable-fix", choices=DURABLE_FIXES, default="undecided")
    record.add_argument("--evidence", action="append", default=[])
    record.add_argument("--replace", action="store_true")

    report = subparsers.add_parser("report", help="Aggregate recorded findings.")
    add_common_path_args(report)
    report.add_argument("--min-count", type=int, default=2)
    report.add_argument("--format", choices=("json", "markdown"), default="markdown")
    report.add_argument("--output", type=Path)

    propose = subparsers.add_parser("propose", help="Create a guardrail proposal for a ready class.")
    add_common_path_args(propose)
    propose.add_argument("--fingerprint", required=True)
    propose.add_argument("--min-count", type=int, default=2)
    propose.add_argument("--decision", choices=PROMOTION_DECISIONS, required=True)
    propose.add_argument("--owner", required=True)
    propose.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    ledger = confined_path(root, args.ledger, "ledger")

    if args.command == "record":
        if args.from_autoreview:
            report_path = confined_path(root, args.from_autoreview, "autoreview report", must_exist=True)
            if report_path == ledger:
                fail("autoreview report and ledger must use different paths")
        record = build_record(args, root)
        state = record_finding(ledger, record, replace=args.replace)
        print(f"quiet aggregate: {state} {record['id']} ({record['fingerprint']})")
        return 0

    records = load_ledger(ledger)
    report = build_report(records, args.min_count)
    if args.command == "report":
        rendered = (
            json.dumps(report, indent=2, sort_keys=True) + "\n"
            if args.format == "json"
            else render_report_markdown(report)
        )
        if args.output:
            output = confined_path(root, args.output, "report output")
            if output == ledger:
                fail("report output and ledger must use different paths")
            atomic_write_text(output, rendered)
            print(f"quiet aggregate: wrote {output.relative_to(root)}")
        else:
            print(rendered, end="")
        return 0

    candidate = next(
        (item for item in report["candidates"] if item["fingerprint"] == args.fingerprint),
        None,
    )
    if candidate is None:
        fail(f"unknown fingerprint: {args.fingerprint}")
    if not candidate["ready_for_promotion"]:
        fail(f"{args.fingerprint} has not repeated across {args.min_count} independent sources")
    proposal = build_proposal(
        candidate,
        args.decision,
        validate_text(args.owner, "owner", maximum=100),
    )
    if args.output:
        output = confined_path(root, args.output, "proposal output")
        if output == ledger:
            fail("proposal output and ledger must use different paths")
        atomic_write_text(output, proposal)
        print(f"quiet aggregate: wrote {output.relative_to(root)}")
    else:
        print(proposal, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
