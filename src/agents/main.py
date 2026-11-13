
import asyncio

from dotenv import load_dotenv

from agents import InputGuardrailTripwireTriggered, Runner
from src.agents.openai_agent import mcp_server, triage_agent

load_dotenv()


async def main():
    async with mcp_server:

        # Check which tools the MCP server exposes
        tools = await mcp_server.list_tools()

        print("\nDiscovered MCP tools:")
        for tool in tools:
            print(f"- {tool.name}")

        # Run the Triage Agent
        try:
            result = await Runner.run(
                triage_agent,
                "Check the leave balance for employee EMP001."
            )

            print("\nAgent response:")
            print(result.final_output)

        except InputGuardrailTripwireTriggered:
            print("\nRequest blocked: Only HR-related queries are allowed.")


if __name__ == "__main__":
    asyncio.run(main())
