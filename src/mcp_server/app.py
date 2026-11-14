import os

from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier

load_dotenv()

api_key = os.getenv("MCP_API_KEY")

if not api_key:
    raise ValueError("MCP_API_KEY is not configured")

auth = StaticTokenVerifier(
    tokens={
        api_key: {
            "client_id": "hr-client",
            "scopes": [],
        }
    }
)

mcp = FastMCP(
    "HR Leave Management Assistant",
    auth=auth,
)
