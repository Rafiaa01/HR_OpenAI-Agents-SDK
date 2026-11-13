
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
     handoff_description=(
        "Handles employee leave balances, leave applications, "
        "and leave request reviews using HR MCP tools."
    ),
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
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are the first point of contact for user requests.

    Your job is to identify HR leave management requests
    and hand them off to the HR Leave Assistant.

    For questions about:
    - Leave balances
    - Applying for leave
    - Pending leave requests
    - Reviewing leave applications

    Always hand off to the HR Leave Assistant.

    Do not answer HR questions yourself.
    """,
    handoffs=[hr_agent],     
)