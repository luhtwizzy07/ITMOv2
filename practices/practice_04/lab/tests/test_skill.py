import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / ".opencode/skills/notify-tdd/scripts/phase.py"
PASSING = "import unittest\nclass Case(unittest.TestCase):\n    def test_case(self):\n        self.assertTrue(True)\n"
FAILING = PASSING.replace("True)", "False)")


class SkillGateTest(unittest.TestCase):
    def gate(self, feature_source, phase="red", baseline_source=PASSING):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / ".opencode/skills/notify-tdd/scripts/phase.py"
            script.parent.mkdir(parents=True)
            shutil.copyfile(GATE, script)
            (root / "tests").mkdir()
            (root / "tests/test_baseline.py").write_text(baseline_source)
            (root / "tests/test_list.py").write_text(feature_source)
            completed = subprocess.run(
                [sys.executable, str(script), phase, "a"],
                capture_output=True, text=True, check=False,
            )
            return completed.returncode, json.loads(completed.stdout)

    def test_red_accepts_a_real_assertion_failure(self):
        code, result = self.gate(FAILING)
        self.assertEqual(code, 0)
        self.assertTrue(result["accepted"])

    def test_red_rejects_import_errors(self):
        code, result = self.gate("import missing_notify_dependency\n")
        self.assertEqual(code, 1)
        self.assertGreater(result["feature_suite"]["errors"], 0)

    def test_red_rejects_zero_tests(self):
        self.assertEqual(self.gate("")[0], 1)

    def test_red_rejects_skipped_tests(self):
        skipped = FAILING.replace("    def test_case", "    @unittest.skip('not implemented')\n    def test_case")
        self.assertEqual(self.gate(skipped)[0], 1)

    def test_red_rejects_broken_baseline(self):
        self.assertEqual(self.gate(FAILING, baseline_source=FAILING)[0], 1)

    def test_green_requires_passing_feature_tests(self):
        self.assertEqual(self.gate(FAILING, phase="green")[0], 1)
        self.assertEqual(self.gate(PASSING, phase="green")[0], 0)
