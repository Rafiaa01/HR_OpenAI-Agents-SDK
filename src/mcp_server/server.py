import asyncio

from src.mcp_server import prompt, resources, tools  # noqa: F401
from src.mcp_server.app import mcp

if __name__ == "__main__":
    try:
        mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8001,
    )
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("\nServer stopped.")