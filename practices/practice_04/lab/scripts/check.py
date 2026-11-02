"""One fixed test runner shared by the shell, skill, hook and MCP."""

import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROFILES = {
    "baseline": "test_baseline.py",
    "a": "test_list.py",
    "b": "test_unsubscribe.py",
    "all": "test_*.py",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", nargs="?", default="all", choices=PROFILES)
    args = parser.parse_args()
    pattern = PROFILES[args.profile]
    if not list((ROOT / "tests").glob(pattern)):
        print(f"FAIL: no tests for profile {args.profile}", file=sys.stderr)
        return 2
    command = [
        sys.executable, "-m", "unittest", "discover",
        "-s", "tests", "-p", pattern, "-v",
    ]
    completed = subprocess.run(command, cwd=ROOT, check=False)
    print(f"CHECK {args.profile}: {'PASS' if completed.returncode == 0 else 'FAIL'}", flush=True)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
