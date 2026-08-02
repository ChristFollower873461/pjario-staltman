import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


def load_module():
    root = Path(__file__).resolve().parents[1]
    script = root / "tools" / "pjario.py"
    spec = importlib.util.spec_from_file_location("pjario_cli", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load tools/pjario.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


pjario = load_module()
SOURCE_ROOT = Path(__file__).resolve().parents[1]


class PjarioTests(unittest.TestCase):
    def test_start_creates_one_progressive_trivial_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(
                pjario.main(
                    [
                        "start",
                        "--root",
                        str(root),
                        "--id",
                        "DOC-002",
                        "--title",
                        "Clarify setup copy",
                        "--outcome",
                        "Readers understand the setup boundary.",
                        "--complexity",
                        "trivial",
                    ]
                ),
                0,
            )
            path = root / ".pjario" / "work" / "DOC-002.md"
            text = path.read_text(encoding="utf-8")
            self.assertIn("Schema: pjario.work/v1", text)
            self.assertIn("Not required for trivial work.", text)
            self.assertEqual(text.count("## Evidence"), 1)
            packet, parse_errors = pjario.parse_packet(path)
            self.assertFalse(parse_errors)
            errors = pjario.validation_errors(packet)
            self.assertTrue(any("Scope" in error for error in errors))

    def test_golden_packets_finish_with_stable_proof_ids(self):
        for relative in (
            "examples/work-packets/trivial-copy.md",
            "examples/work-packets/non-trivial-integration.md",
        ):
            packet = pjario.load_and_validate(SOURCE_ROOT, Path(relative), phase="finish")
            self.assertTrue(packet.proofs)
            self.assertEqual({proof.id for proof in packet.proofs}, {item.proof_id for item in packet.evidence})

    def test_completion_summary_uses_repo_relative_packet_path(self):
        packet = pjario.load_and_validate(
            SOURCE_ROOT,
            Path("examples/work-packets/trivial-copy.md"),
            phase="finish",
        )
        payload = pjario.completion_payload(SOURCE_ROOT, packet)
        self.assertEqual(payload["packet"], "examples/work-packets/trivial-copy.md")
        self.assertNotIn(str(SOURCE_ROOT), json.dumps(payload))

    def test_active_risk_requires_explicit_proof_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            text = (SOURCE_ROOT / "examples/work-packets/non-trivial-integration.md").read_text(
                encoding="utf-8"
            )
            text = text.replace(
                "- RISK-05 | inactive | async-work | none",
                "- RISK-05 | active | async-work | Background refresh must be idempotent.",
            )
            path = root / "packet.md"
            path.write_text(text, encoding="utf-8")
            packet, parse_errors = pjario.parse_packet(path)
            self.assertFalse(parse_errors)
            self.assertIn(
                "RISK-05 is active but no proof requirement maps to it",
                pjario.validation_errors(packet),
            )

    def test_frontend_profile_requires_design_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            text = (SOURCE_ROOT / "examples/work-packets/trivial-copy.md").read_text(encoding="utf-8")
            text = text.replace("Profile: core", "Profile: frontend")
            path = root / "packet.md"
            path.write_text(text, encoding="utf-8")
            packet, parse_errors = pjario.parse_packet(path)
            self.assertFalse(parse_errors)
            self.assertTrue(any("Design Context" in error for error in pjario.validation_errors(packet)))

    def test_accepted_gap_requires_named_gap_before_finish(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            text = (SOURCE_ROOT / "examples/work-packets/trivial-copy.md").read_text(encoding="utf-8")
            text = text.replace(
                "- PROOF-01 | passed | Production render test passed and the targeted diff contains only the description and assertion.",
                "- PROOF-01 | accepted-gap | Safari was not available in the local environment.",
            )
            path = root / "packet.md"
            path.write_text(text, encoding="utf-8")
            packet, parse_errors = pjario.parse_packet(path)
            self.assertFalse(parse_errors)
            self.assertTrue(any("Known Gaps" in error for error in pjario.validation_errors(packet, phase="finish")))

            text = text.replace("- None recorded.\n\n## Next Action", "- Safari remains untested.\n\n## Next Action", 1)
            path.write_text(text, encoding="utf-8")
            pjario.load_and_validate(root, Path("packet.md"), phase="finish")

    def test_finish_requires_complete_status_and_passing_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            text = (SOURCE_ROOT / "examples/work-packets/trivial-copy.md").read_text(encoding="utf-8")
            text = text.replace("Status: complete", "Status: ready-for-review")
            text = text.replace("Decision: PASS", "Decision: pending")
            path = root / "packet.md"
            path.write_text(text, encoding="utf-8")
            packet, parse_errors = pjario.parse_packet(path)
            self.assertFalse(parse_errors)
            errors = pjario.validation_errors(packet, phase="finish")
            self.assertIn("finish requires Status: complete", errors)
            self.assertIn("finish requires a passing review decision", errors)

    def test_review_includes_explicit_work_packet_and_diff(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "qa@example.invalid"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Pjario QA"], cwd=root, check=True)
            (root / "app.txt").write_text("before\n", encoding="utf-8")
            subprocess.run(["git", "add", "app.txt"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "base"], cwd=root, check=True)
            packet_dir = root / ".pjario" / "work"
            packet_dir.mkdir(parents=True)
            packet_path = packet_dir / "DOC-001.md"
            packet_path.write_text(
                (SOURCE_ROOT / "examples/work-packets/trivial-copy.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (root / "app.txt").write_text("after\n", encoding="utf-8")

            self.assertEqual(
                pjario.main(
                    [
                        "review",
                        "--root",
                        str(root),
                        "--packet",
                        ".pjario/work/DOC-001.md",
                    ]
                ),
                0,
            )
            review = (root / ".pjario" / "review-packet.md").read_text(encoding="utf-8")
            self.assertIn("# Explicit Work Context", review)
            self.assertIn("Schema: pjario.work/v1", review)
            self.assertIn("-before", review)
            self.assertIn("+after", review)

    def test_bundled_helper_wins_over_target_repo_lookalike(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake = root / "tools" / "review-packet.py"
            fake.parent.mkdir()
            fake.write_text("raise SystemExit('target helper ran')\n", encoding="utf-8")
            helper = pjario.find_helper(root, "review-packet")
            self.assertEqual(helper, SOURCE_ROOT / "tools" / "review-packet.py")
            self.assertNotEqual(helper, fake)

    def test_learn_routes_to_quiet_aggregate_without_hidden_model_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(
                pjario.main(
                    [
                        "learn",
                        "--root",
                        str(root),
                        "record",
                        "--title",
                        "Missing timeout",
                        "--summary",
                        "The external client has no bounded timeout.",
                        "--priority",
                        "P2",
                        "--category",
                        "bug",
                        "--file-path",
                        "src/client.py",
                        "--line",
                        "12",
                        "--source-kind",
                        "human-review",
                        "--source-ref",
                        "pr-10/staff-review",
                        "--failure-class",
                        "missing-timeout",
                        "--owner-boundary",
                        "external-client",
                    ]
                ),
                0,
            )
            ledger = root / ".pjario" / "quiet-aggregate.jsonl"
            self.assertTrue(ledger.is_file())
            self.assertEqual(len(ledger.read_text(encoding="utf-8").splitlines()), 1)

    def test_adoption_dry_run_does_not_mutate_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            before = list(root.iterdir())
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(
                    pjario.main(
                        ["adopt", "--target", str(root), "--profile", "frontend", "--dry-run"]
                    ),
                    0,
                )
            self.assertEqual(list(root.iterdir()), before)
            self.assertIn("Mutation: `none`", output.getvalue())
            self.assertIn("DESIGN.md", output.getvalue())
            self.assertIn("tools/review-packet.py", output.getvalue())
            self.assertIn("evals/skill-behavior.json", output.getvalue())
            self.assertIn(".github/workflows/", output.getvalue())

    def test_adoption_inventory_recognizes_exact_core_markers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = (
                "build-system/templates/work-packet.md",
                "tools/pjario.py",
                "tools/review-packet.py",
                "tools/quiet-aggregate.py",
                "tests/test_pjario.py",
                "evals/skill-behavior.json",
            )
            for relative in paths:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("marker\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("Use pjario.work/v1.\n", encoding="utf-8")
            (root / ".gitignore").write_text(
                ".pjario/*\n!.pjario/work/\n!.pjario/work/*.md\n",
                encoding="utf-8",
            )
            (root / "Makefile").write_text("check-work:\nfinish-work:\n", encoding="utf-8")
            actions = {item["path"]: item["action"] for item in pjario.adoption_items(root, "core")}
            expected = (
                "build-system/",
                "tools/pjario.py",
                "tools/review-packet.py",
                "tools/quiet-aggregate.py",
                "tests/",
                "evals/skill-behavior.json",
                "AGENTS.md",
                ".gitignore",
                "Makefile",
            )
            for relative in expected:
                self.assertEqual(actions[relative], "KEEP", relative)

    def test_packet_rejects_secret_shapes_and_output_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_token = "gh" + "p_abcdefghijklmnopqrstuvwxyz123456"
            with self.assertRaisesRegex(SystemExit, "credential"):
                pjario.main(
                    [
                        "start",
                        "--root",
                        str(root),
                        "--id",
                        "SEC-001",
                        "--title",
                        "Security check",
                        "--outcome",
                        f"Never store {fake_token}",
                        "--complexity",
                        "trivial",
                    ]
                )
            with self.assertRaisesRegex(SystemExit, "stay inside root"):
                pjario.confined_path(root, Path("../packet.md"), "packet")

            packet = root / "packet.md"
            packet.write_text(
                (SOURCE_ROOT / "examples/work-packets/trivial-copy.md")
                .read_text(encoding="utf-8")
                .replace("Production render test", "/private/var/folders/local-result Production render test"),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(SystemExit, "local absolute path"):
                pjario.parse_packet(packet)


if __name__ == "__main__":
    unittest.main()
