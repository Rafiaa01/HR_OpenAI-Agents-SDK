import asyncio
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

async def main():
    api_key = os.getenv("MCP_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {
                "name": "auth-test",
                "version": "1.0.0",
            },
        },
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8001/mcp",
            headers=headers,
            json=payload,
        )

        print("Status:", response.status_code)
        print("Response:", response.text[:1000])

asyncio.run(main())