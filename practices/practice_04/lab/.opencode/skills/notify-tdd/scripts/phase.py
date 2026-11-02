"""Validate a feature's RED/GREEN phase against unittest results."""

import argparse
import io
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))


def run_suite(pattern: str) -> dict:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern=pattern)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    return {
        "tests": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
        "output": stream.getvalue(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("red", "green"))
    parser.add_argument("feature", choices=("a", "b"))
    args = parser.parse_args()
    baseline = run_suite("test_baseline.py")
    feature = run_suite({"a": "test_list.py", "b": "test_unsubscribe.py"}[args.feature])
    baseline_ok = baseline["successful"] and baseline["tests"] > 0 and baseline["skipped"] == 0
    feature_valid = feature["tests"] > 0 and feature["errors"] == 0 and feature["skipped"] == 0
    phase_ok = feature["failures"] > 0 if args.phase == "red" else feature["successful"]
    accepted = baseline_ok and feature_valid and phase_ok
    print(json.dumps({
        "phase": args.phase, "feature": args.feature,
        "accepted": accepted, "baseline": baseline, "feature_suite": feature,
    }, ensure_ascii=False, indent=2))
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
