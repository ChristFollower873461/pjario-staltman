import argparse
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


def load_module():
    root = Path(__file__).resolve().parents[2]
    script = root / "Pevie Hischer" / "tools" / "review-packet.py"
    spec = importlib.util.spec_from_file_location("pevie_review_packet", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load Pevie Hischer review-packet.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


review_packet = load_module()


class PevieReviewPacketTests(unittest.TestCase):
    def init_repo(self, root: Path) -> None:
        subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        package = root / "Pevie Hischer"
        (package / "build-system" / "agents").mkdir(parents=True)
        (package / "build-system" / "rules").mkdir(parents=True)
        (package / "build-system").mkdir(exist_ok=True)
        (package / "AGENTS.md").write_text("# Agent rules\n", encoding="utf-8")
        (package / "build-system" / "README.md").write_text("# Build system\n", encoding="utf-8")
        (package / "build-system" / "agents" / "frontend-implementation-agent.md").write_text(
            "# Impl agent\n", encoding="utf-8"
        )
        (package / "build-system" / "rules" / "frontend-production-readiness.md").write_text(
            "# Rules\n", encoding="utf-8"
        )

    def args(self, **kwargs):
        base = {
            "base": None,
            "cached": False,
            "output": None,
            "max_bytes": 50_000,
        }
        base.update(kwargs)
        return argparse.Namespace(**base)

    def test_collect_rules_reads_package_docs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            docs = review_packet.collect_rules(root)
            names = [name for name, _ in docs]
            self.assertIn("Pevie Hischer/AGENTS.md", names)
            self.assertIn("Pevie Hischer/build-system/README.md", names)

    def test_build_packet_includes_changes_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            packet = review_packet.build_packet(root, self.args())
            self.assertIn("# Changes To Review", packet)
            self.assertIn("No tracked diff found", packet)

    def test_build_packet_keeps_changes_section_when_budget_is_tight(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            with mock.patch.object(review_packet, "collect_rules", return_value=[("rule.md", "x" * 4000)]):
                packet = review_packet.build_packet(root, self.args(max_bytes=900))

            self.assertIn("# Changes To Review", packet)
            self.assertIn("No tracked diff found", packet)
            self.assertTrue(
                "# Package Rules" not in packet
                or "[omitted due to --max-bytes;" in packet
            )
            self.assertLessEqual(review_packet.byte_len(packet), 900)

    def test_build_packet_fails_when_diff_cannot_fit_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            with mock.patch.object(review_packet, "collect_diff", return_value="D" * 5000):
                with self.assertRaises(SystemExit) as exc:
                    review_packet.build_packet(root, self.args(max_bytes=200))
            self.assertIn("Diff exceeds --max-bytes budget", str(exc.exception))

    def test_collect_diff_returns_staged_diff_for_new_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            target = root / "Pevie Hischer" / "AGENTS.md"
            target.write_text("# Agent rules\n\nupdated\n", encoding="utf-8")
            subprocess.run(["git", "add", "Pevie Hischer/AGENTS.md"], cwd=root, check=True)
            diff = review_packet.collect_diff(root, self.args())
            self.assertIn("## Staged Diff", diff)
            self.assertIn("updated", diff)

    def test_collect_diff_with_missing_base_has_clear_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.init_repo(root)
            with self.assertRaises(SystemExit) as exc:
                review_packet.collect_diff(root, self.args(base="definitely-missing-ref"))
            self.assertIn("Could not diff against base ref", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
