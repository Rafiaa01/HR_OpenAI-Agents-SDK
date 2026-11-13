
import sys
from pathlib import Path

from agents.mcp import MCPServerStdio

from agents import Agent

PROJECT_ROOT = Path(__file__).resolve().parents[2]

mcp_server = MCPServerStdio(
    name="HR Leave Management MCP Server",
    params={
        "command": sys.executable,
        "args": ["-m", "src.mcp_server.server"],
        "cwd": str(PROJECT_ROOT),
    },
    cache_tools_list=True,
)

hr_agent = Agent(
    name="HR Leave Assistant",
    instructions="""
    You are an HR leave management assistant.

    Help employees with leave-related requests.
    Use the available MCP tools to check leave balances,
    submit leave applications, and retrieve or review
    leave requests.

    Never invent employee records or leave balances.
    Always use the MCP tools when accessing HR data.
    """,
    mcp_servers=[mcp_server],
)
