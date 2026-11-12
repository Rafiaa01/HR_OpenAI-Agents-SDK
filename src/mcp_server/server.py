import asyncio

from src.mcp_server import prompt, resources, tools  # noqa: F401
from src.mcp_server.app import mcp

if __name__ == "__main__":
    try:
        mcp.run(transport="stdio")
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("\nServer stopped.")