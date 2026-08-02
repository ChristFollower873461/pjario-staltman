import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


def load_module():
    root = Path(__file__).resolve().parents[1]
    script = root / "tools" / "quiet-aggregate.py"
    spec = importlib.util.spec_from_file_location("quiet_aggregate", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load tools/quiet-aggregate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


quiet = load_module()


def autoreview_report(title="Missing rollback proof", file_path="build-system/templates/pr.md"):
    return {
        "findings": [
            {
                "title": title,
                "body": "The change has no verified rollback path.",
                "priority": "P2",
                "confidence": 0.96,
                "category": "maintainability",
                "code_location": {"file_path": file_path, "line": 12},
            }
        ],
        "overall_correctness": "patch is incorrect",
        "overall_explanation": "One actionable finding.",
        "overall_confidence": 0.96,
    }


def record_args(root, report, source_ref, observed_at, **overrides):
    values = {
        "from_autoreview": report,
        "finding_index": 0,
        "title": None,
        "summary": None,
        "priority": None,
        "confidence": 1.0,
        "category": None,
        "file_path": None,
        "line": None,
        "source_kind": None,
        "source_ref": source_ref,
        "reviewer": "codex",
        "observed_at": observed_at,
        "disposition": "actionable",
        "failure_class": "missing-rollback-proof",
        "owner_boundary": "release-proof",
        "durable_fix": "template",
        "evidence": [],
        "replace": False,
    }
    values.update(overrides)
    return quiet.argparse.Namespace(**values)


class QuietAggregateTests(unittest.TestCase):
    def test_repeated_verified_findings_become_ready_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report_path = root / "review.json"
            report_path.write_text(json.dumps(autoreview_report()), encoding="utf-8")
            first = quiet.build_record(
                record_args(root, report_path, "pr-10/cycle-1", "2026-07-01T12:00:00Z"),
                root,
            )
            second = quiet.build_record(
                record_args(root, report_path, "pr-12/cycle-1", "2026-07-03T12:00:00Z"),
                root,
            )

            report = quiet.build_report([first, second], min_count=2)

            self.assertEqual(report["totals"]["ready_for_promotion"], 1)
            candidate = report["candidates"][0]
            self.assertTrue(candidate["ready_for_promotion"])
            self.assertEqual(candidate["occurrence_count"], 2)
            self.assertEqual(candidate["source_count"], 2)
            self.assertEqual(candidate["recommended_fix"], "template")
            self.assertEqual(first["fingerprint"], second["fingerprint"])

    def test_two_findings_from_one_review_do_not_trigger_promotion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report_path = root / "review.json"
            report_path.write_text(json.dumps(autoreview_report()), encoding="utf-8")
            first = quiet.build_record(
                record_args(root, report_path, "pr-10/cycle-1", "2026-07-01T12:00:00Z"),
                root,
            )
            second = quiet.build_record(
                record_args(
                    root,
                    report_path,
                    "pr-10/cycle-1",
                    "2026-07-01T12:01:00Z",
                    title="Another expression of the same failure",
                ),
                root,
            )
            second["id"] = "qaf-0000000000000000"

            candidate = quiet.build_report([first, second], min_count=2)["candidates"][0]

            self.assertEqual(candidate["occurrence_count"], 2)
            self.assertEqual(candidate["source_count"], 1)
            self.assertFalse(candidate["ready_for_promotion"])

    def test_record_is_idempotent_and_requires_replace_for_reclassification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger = root / ".pjario" / "quiet-aggregate.jsonl"
            report_path = root / "review.json"
            report_path.write_text(json.dumps(autoreview_report()), encoding="utf-8")
            record = quiet.build_record(
                record_args(root, report_path, "pr-10/cycle-1", "2026-07-01T12:00:00Z"),
                root,
            )

            self.assertEqual(quiet.record_finding(ledger, record), "recorded")
            self.assertEqual(quiet.record_finding(ledger, record), "unchanged")
            changed = json.loads(json.dumps(record))
            changed["classification"]["disposition"] = "rejected"
            with self.assertRaisesRegex(SystemExit, "--replace"):
                quiet.record_finding(ledger, changed)
            self.assertEqual(quiet.record_finding(ledger, changed, replace=True), "replaced")
            self.assertEqual(quiet.load_ledger(ledger)[0]["classification"]["disposition"], "rejected")

    def test_rejected_and_follow_up_findings_are_audited_but_not_aggregated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report_path = root / "review.json"
            report_path.write_text(json.dumps(autoreview_report()), encoding="utf-8")
            rejected = quiet.build_record(
                record_args(
                    root,
                    report_path,
                    "pr-10/cycle-1",
                    "2026-07-01T12:00:00Z",
                    disposition="rejected",
                ),
                root,
            )
            follow_up = quiet.build_record(
                record_args(
                    root,
                    report_path,
                    "pr-11/cycle-1",
                    "2026-07-02T12:00:00Z",
                    disposition="follow-up",
                ),
                root,
            )

            report = quiet.build_report([rejected, follow_up], min_count=2)

            self.assertEqual(report["candidates"], [])
            self.assertEqual(report["totals"]["rejected"], 1)
            self.assertEqual(report["totals"]["follow_up"], 1)

    def test_proposal_is_explicitly_non_mutating(self):
        candidate = {
            "fingerprint": "qac-0123456789abcdef",
            "failure_class": "missing-rollback-proof",
            "owner_boundary": "release-proof",
            "occurrence_count": 2,
            "source_count": 2,
            "priorities": ["P2"],
            "source_refs": ["pr-10/cycle-1", "pr-12/cycle-1"],
        }

        proposal = quiet.build_proposal(candidate, "template", "release coordinator")

        self.assertIn("Status: proposed, not applied", proposal)
        self.assertIn("does not edit rules", proposal)
        self.assertIn("pr-10/cycle-1", proposal)

    def test_secret_like_finding_is_rejected_before_ledger_write(self):
        report = autoreview_report()
        fake_token = "gh" + "p_abcdefghijklmnopqrstuvwxyz123456"
        report["findings"][0]["body"] = f"token={fake_token}"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report_path = root / "review.json"
            report_path.write_text(json.dumps(report), encoding="utf-8")

            with self.assertRaisesRegex(SystemExit, "credential"):
                quiet.build_record(
                    record_args(root, report_path, "pr-10/cycle-1", "2026-07-01T12:00:00Z"),
                    root,
                )

    def test_absolute_code_location_and_output_escape_are_rejected(self):
        private_path = "/" + "Users/example/private.py"
        report = autoreview_report(file_path=private_path)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report_path = root / "review.json"
            report_path.write_text(json.dumps(report), encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "repo-relative"):
                quiet.build_record(
                    record_args(root, report_path, "pr-10/cycle-1", "2026-07-01T12:00:00Z"),
                    root,
                )
            with self.assertRaisesRegex(SystemExit, "stay inside root"):
                quiet.confined_path(root, Path("../outside.json"), "output")

    def test_corrupt_and_duplicate_ledgers_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger = root / "ledger.jsonl"
            ledger.write_text("not json\n", encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "invalid JSON"):
                quiet.load_ledger(ledger)

            report_path = root / "review.json"
            report_path.write_text(json.dumps(autoreview_report()), encoding="utf-8")
            record = quiet.build_record(
                record_args(root, report_path, "pr-10/cycle-1", "2026-07-01T12:00:00Z"),
                root,
            )
            encoded = json.dumps(record)
            ledger.write_text(f"{encoded}\n{encoded}\n", encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "duplicate id"):
                quiet.load_ledger(ledger)

    def test_tampered_identity_and_symlinked_ledger_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report_path = root / "review.json"
            report_path.write_text(json.dumps(autoreview_report()), encoding="utf-8")
            record = quiet.build_record(
                record_args(root, report_path, "pr-10/cycle-1", "2026-07-01T12:00:00Z"),
                root,
            )
            record["source"]["ref"] = "pr-99/tampered"
            ledger = root / "ledger.jsonl"
            ledger.write_text(json.dumps(record) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "observation identity"):
                quiet.load_ledger(ledger)

            real_ledger = root / "real-ledger.jsonl"
            real_ledger.write_text("", encoding="utf-8")
            linked_ledger = root / "linked-ledger.jsonl"
            linked_ledger.symlink_to(real_ledger)
            with self.assertRaisesRegex(SystemExit, "must not be a symlink"):
                quiet.load_ledger(linked_ledger)

    def test_large_report_git_internal_path_and_ledger_overwrite_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            oversized = root / "oversized.json"
            oversized.write_text("x" * (quiet.MAX_REPORT_BYTES + 1), encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "exceeds"):
                quiet.read_json(oversized, "autoreview report")

            (root / ".git").mkdir()
            with self.assertRaisesRegex(SystemExit, "inside .git"):
                quiet.confined_path(root, Path(".git/config"), "ledger")

            ledger = root / ".pjario" / "quiet-aggregate.jsonl"
            ledger.parent.mkdir()
            ledger.write_text("", encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "different paths"):
                quiet.main(
                    [
                        "report",
                        "--root",
                        str(root),
                        "--output",
                        ".pjario/quiet-aggregate.jsonl",
                    ]
                )

    def test_cli_records_reports_and_proposes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report_path = root / "review.json"
            report_path.write_text(json.dumps(autoreview_report()), encoding="utf-8")
            common = [
                "record",
                "--root",
                str(root),
                "--from-autoreview",
                "review.json",
                "--failure-class",
                "missing-rollback-proof",
                "--owner-boundary",
                "release-proof",
                "--durable-fix",
                "template",
                "--observed-at",
                "2026-07-01T12:00:00Z",
            ]
            self.assertEqual(quiet.main([*common, "--source-ref", "pr-10/cycle-1"]), 0)
            self.assertEqual(quiet.main([*common, "--source-ref", "pr-12/cycle-1"]), 0)
            ledger = root / ".pjario" / "quiet-aggregate.jsonl"
            aggregate = quiet.build_report(quiet.load_ledger(ledger), min_count=2)
            fingerprint = aggregate["candidates"][0]["fingerprint"]
            output = root / "proposal.md"

            self.assertEqual(
                quiet.main(
                    [
                        "propose",
                        "--root",
                        str(root),
                        "--fingerprint",
                        fingerprint,
                        "--decision",
                        "template",
                        "--owner",
                        "release-coordinator",
                        "--output",
                        "proposal.md",
                    ]
                ),
                0,
            )
            self.assertIn("proposed, not applied", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
