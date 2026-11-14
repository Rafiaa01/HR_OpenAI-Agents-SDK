# HR Leave Management Agent — OpenAI Agents SDK + MCP

## Project Overview

An AI-powered HR Leave Management Assistant built using the **OpenAI Agents SDK** and an existing **FastMCP server**.

The system uses multiple agents to handle employee leave-related queries, execute MCP tools, validate requests through guardrails, and record execution traces.

## Technologies Used

- Python
- OpenAI Agents SDK
- MCP Python SDK
- FastMCP
- Pydantic
- python-dotenv
- JSON-based storage

## Architecture

The project uses a two-agent architecture:

1. **Triage Agent:** Receives user queries, checks the HR-domain guardrail, and routes HR-related requests to the specialist agent.
2. **HR Leave Assistant:** Connects to the existing HR MCP server and executes the appropriate tools.

The MCP server exposes the following tools:

- `check_leave_balance`
- `submit_leave_application`
- `get_pending_leave_requests`
- `review_leave_application`

The server also provides an employee handbook resource and a leave application prompt.

## Implemented Features

### 1. MCP Server Integration

- Connected the existing FastMCP server using `MCPServerStdio`.
- Configured the server to run as a subprocess.
- Discovered and exposed MCP tools to the HR Leave Assistant.
- Used `Runner.run()` to execute agent workflows.

### 2. Multi-Agent Architecture and Handoffs

- Created a Triage Agent and an HR Leave Assistant.
- Configured handoffs using `handoffs=[hr_agent]`.
- Enabled the Triage Agent to delegate HR-related tasks to the specialist agent.

### 3. Input Guardrails

- Implemented an HR-domain input guardrail.
- Allowed HR-related queries.
- Blocked unrelated requests using a guardrail tripwire.
- Handled `InputGuardrailTripwireTriggered` exceptions.

### 4. Local Tracing

- Implemented a custom `LocalTracingProcessor`.
- Recorded execution events in `src/agents/traces.jsonl`.
- Captured agent execution, guardrail results, handoffs, MCP tool calls, and token usage.
- Used `set_trace_processors()` to configure local tracing.

### 5. End-to-End Testing

Successfully tested the following scenarios:

| Test | Expected behavior | Result |
|---|---|---|
| Single tool call | Check employee leave balance | Passed |
| Multiple tool calls | Check balance and pending requests | Passed |
| Guardrail validation | Block unrelated requests | Passed |

**