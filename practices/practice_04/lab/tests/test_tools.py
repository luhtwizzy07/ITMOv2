import asyncio
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from mcp_server import project_check

ROOT = Path(__file__).resolve().parents[1]


class CheckToolTest(unittest.TestCase):
    def test_unknown_profile_does_not_launch_a_command(self):
        with patch("mcp_server.subprocess.run") as run:
            with self.assertRaisesRegex(ValueError, "unknown profile"):
                project_check("../../another-project")
            run.assert_not_called()

    def test_test_failure_is_not_reported_as_pass(self):
        with patch("mcp_server.subprocess.run", return_value=subprocess.CompletedProcess(
            args=[], returncode=1, stdout="CHECK a: FAIL\n", stderr="assertion failed\n",
        )):
            result = project_check("a")
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["exit_code"], 1)
        self.assertIn("assertion failed", result["output"])

    def test_timeout_is_an_explicit_error(self):
        with patch("mcp_server.subprocess.run", side_effect=subprocess.TimeoutExpired([], 60)):
            with self.assertRaisesRegex(RuntimeError, "exceeded 60 seconds"):
                project_check("baseline")

    def test_real_stdio_success_and_invalid_input(self):
        asyncio.run(self.check_stdio())

    async def check_stdio(self):
        parameters = StdioServerParameters(
            command=sys.executable, args=[str(ROOT / "mcp_server.py")], cwd=str(ROOT),
        )
        async with stdio_client(parameters) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                await session.initialize()
                tools = await session.list_tools()
                self.assertEqual([tool.name for tool in tools.tools], ["project_check"])
                result = await session.call_tool("project_check", {"profile": "baseline"})
                self.assertFalse(result.isError)
                self.assertEqual(result.structuredContent["status"], "PASS")
                bad = await session.call_tool("project_check", {"profile": "unknown"})
                self.assertTrue(bad.isError)
                self.assertIn("unknown profile", bad.content[0].text)
                wrong_type = await session.call_tool("project_check", {"profile": 42})
                self.assertTrue(wrong_type.isError)
