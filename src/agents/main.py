
import asyncio

from dotenv import load_dotenv

from agents import InputGuardrailTripwireTriggered, Runner, set_trace_processors, trace
from src.agents.openai_agent import mcp_server, triage_agent
from src.agents.tracing import LocalTracingProcessor

load_dotenv()

set_trace_processors([LocalTracingProcessor()])
async def main():
    async with mcp_server:

        # Check which tools the MCP server exposes
        tools = await mcp_server.list_tools()

        print("\nDiscovered MCP tools:")
        for tool in tools:
            print(f"- {tool.name}")

        # Run the Triage Agent
        while True:
            user_query = input("\nYou: ").strip()

            if user_query.lower() == "exit":
                print("Exiting HR Assistant...")
                break

            if not user_query:
                continue

            try:
                with trace("HR Leave Management Workflow"):
                    result = await Runner.run(
                        triage_agent,
                        user_query
                    )

                    print("\nAssistant:", result.final_output)

            except InputGuardrailTripwireTriggered:
                print("\nRequest blocked: Only HR-related queries are allowed.")


if __name__ == "__main__":
    try:
      asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
            print("\nServer stopped.")