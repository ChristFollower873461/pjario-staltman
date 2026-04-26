import argparse
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


def load_review_packet_module():
    root = Path(__file__).resolve().parents[1]
    script = root / "tools" / "review-packet.py"
    spec = importlib.util.spec_from_file_location("review_packet", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load tools/review-packet.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


review_packet = load_review_packet_module()


class ReviewPacketTests(unittest.TestCase):
    def init_repo(self, repo: Path) -> None:
        subprocess.run(["git", "init"], cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (repo / "AGENTS.md").write_text("# Agent rules\n", encoding="utf-8")
        (repo / "build-system").mkdir()
        (repo / "build-system" / "README.md").write_text("# Build system\n", encoding="utf-8")
        (repo / "build-system" / "agents").mkdir()
        (repo / "build-system" / "rules").mkdir()

    def test_sensitive_filename_detection_is_case_insensitive(self):
        self.assertTrue(review_packet.is_sensitive_untracked(".env"))
        self.assertTrue(review_packet.is_sensitive_untracked("Nested/API_KEYS.txt"))
        self.assertTrue(review_packet.is_sensitive_untracked("creds/PRIVATE_key.pem"))
        self.assertFalse(review_packet.is_sensitive_untracked("docs/readme.md"))

    def test_collect_untracked_skips_sensitive_files_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.init_repo(repo)
            (repo / ".env").write_text("TOKEN=topsecret\n", encoding="utf-8")
            (repo / "notes.txt").write_text("safe\n", encoding="utf-8")

            result = review_packet.collect_untracked(repo, max_bytes=4096, include_sensitive=False)

            self.assertIn("## Untracked Files", result)
            self.assertIn("Skipped likely sensitive files by default: .env", result)
            self.assertIn("### notes.txt", result)
            self.assertNotIn("TOKEN=topsecret", result)

    def test_collect_untracked_can_include_sensitive_when_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.init_repo(repo)
            (repo / ".env").write_text("TOKEN=topsecret\n", encoding="utf-8")

            result = review_packet.collect_untracked(repo, max_bytes=4096, include_sensitive=True)

            self.assertIn("### .env", result)
            self.assertIn("TOKEN=topsecret", result)
            self.assertNotIn("Skipped likely sensitive files by default", result)

    def test_build_packet_keeps_changes_section_when_budget_is_tight(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.init_repo(repo)
            args = argparse.Namespace(
                base=None,
                cached=False,
                include_untracked=False,
                include_sensitive_untracked=False,
                output=None,
                max_bytes=900,
            )
            with mock.patch.object(review_packet, "collect_rules", return_value=[("rule.md", "x" * 4000)]):
                packet = review_packet.build_packet(repo, args)

            self.assertIn("# Changes To Review", packet)
            self.assertIn("No tracked diff found.", packet)
            self.assertTrue(
                "# Repo Instructions And Rules" not in packet
                or "[omitted due to --max-bytes;" in packet
            )
            self.assertLessEqual(review_packet.byte_len(packet), args.max_bytes)

    def test_build_packet_fails_when_diff_cannot_fit_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.init_repo(repo)
            args = argparse.Namespace(
                base=None,
                cached=False,
                include_untracked=False,
                include_sensitive_untracked=False,
                output=None,
                max_bytes=200,
            )
            with mock.patch.object(review_packet, "collect_diff", return_value="D" * 5000):
                with self.assertRaises(SystemExit) as exc:
                    review_packet.build_packet(repo, args)
            self.assertIn("Diff exceeds --max-bytes budget", str(exc.exception))

    def test_collect_diff_with_missing_base_has_clear_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.init_repo(repo)
            args = argparse.Namespace(base="definitely-missing-ref", cached=False)
            with self.assertRaises(SystemExit) as exc:
                review_packet.collect_diff(repo, args)
            self.assertIn("Could not diff against base ref", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
