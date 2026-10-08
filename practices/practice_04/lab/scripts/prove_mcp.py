"""Exercise the real stdio MCP with the official client; emit a transcript."""

import asyncio
import json
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]


async def main() -> None:
    parameters = StdioServerParameters(
        command=sys.executable, args=[str(ROOT / "mcp_server.py")], cwd=str(ROOT),
    )
    async with stdio_client(parameters) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            initialized = await session.initialize()
            listed = await session.list_tools()
            assert [tool.name for tool in listed.tools] == ["project_check"]
            success = await session.call_tool("project_check", {"profile": "baseline"})
            invalid = await session.call_tool("project_check", {"profile": "not-a-profile"})
            wrong_type = await session.call_tool("project_check", {"profile": 42})
            assert not success.isError
            assert success.structuredContent["status"] == "PASS"
            assert success.structuredContent["exit_code"] == 0
            assert invalid.isError and wrong_type.isError
            print(json.dumps({
                "server": initialized.serverInfo.model_dump(mode="json"),
                "protocol": initialized.protocolVersion,
                "tools": [tool.model_dump(mode="json") for tool in listed.tools],
                "calls": [
                    {"arguments": arguments, "result": result.model_dump(mode="json")}
                    for arguments, result in [
                        ({"profile": "baseline"}, success),
                        ({"profile": "not-a-profile"}, invalid),
                        ({"profile": 42}, wrong_type),
                    ]
                ],
            }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
