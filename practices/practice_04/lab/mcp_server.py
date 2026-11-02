"""A stdio MCP exposing only fixed Notify Mini check profiles."""

from pathlib import Path
import subprocess
import sys

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from scripts.check import PROFILES

ROOT = Path(__file__).resolve().parent
mcp = FastMCP("notify-checks")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def project_check(profile: str = "all") -> dict[str, str | int]:
    """Run Notify Mini checks: baseline, a (listing), b (unsubscribe), or all.

    Returns status, exit_code and actual output. Unknown profiles are tool errors;
    failed tests return FAIL. No command or path input is accepted.
    """
    if profile not in PROFILES:
        raise ValueError(f"unknown profile {profile!r}; choose baseline, a, b or all")
    try:
        result = subprocess.run(
            [sys.executable, "scripts/check.py", profile],
            cwd=ROOT, capture_output=True, text=True, timeout=60, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("project checks exceeded 60 seconds") from exc
    return {
        "profile": profile,
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "exit_code": result.returncode,
        "output": (result.stdout + result.stderr)[-32000:],
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
