
import asyncio

from dotenv import load_dotenv

from agents import Runner
from src.agents.openai_agent import hr_agent, mcp_server

load_dotenv()


async def main():
    async with mcp_server:
        # Check which tools the MCP server exposes
        tools = await mcp_server.list_tools()

        print("\nDiscovered MCP tools:")
        for tool in tools:
            print(f"- {tool.name}")

        # Send a query to the HR agent
        result = await Runner.run(
            hr_agent,
            "Check the leave balance for employee EMP001."
        )

        print("\nAgent response:")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
