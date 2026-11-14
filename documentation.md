# Technical Documentation
# HR Leave Management Agent — OpenAI Agents SDK + MCP

## 1. Introduction

The HR Leave Management Agent is a multi-agent application developed using the OpenAI Agents SDK and Model Context Protocol (MCP).

The application connects an existing HR Leave Management MCP server to an AI-powered agent system. Employees and users can interact with the system using natural language to retrieve leave balances, view pending applications, and perform leave-related operations.

The project demonstrates MCP integration, multi-agent orchestration, handoffs, input guardrails, and execution tracing.

## 2. System Architecture

The application consists of three main components:

1. **Triage Agent**
2. **HR Leave Assistant**
3. **HR Leave Management MCP Server**

### Architecture Flow

```text
              User Query
                  |
                  v
             Triage Agent
                  |
                  v
           Input Guardrail
                  |
          +-------+-------+
          |               |
       Allowed         Blocked
          |               |
          v               v
      Handoff          Stop Request
          |
          v
   HR Leave Assistant
          |
          v
    MCP Server (STDIO)
          |
          v
     MCP Tools
          |
          v
    Leave Management
       Services
          |
          v
      JSON Storage
          |
          v
     Tool Response
          |
          v
    HR Leave Assistant
          |
          v
       User Response
```

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| OpenAI Agents SDK | Agent creation and orchestration |
| MCP Python SDK | MCP client-server communication |
| FastMCP | MCP server implementation |
| Pydantic | Data validation |
| JSON | Data persistence |
| python-dotenv | Environment variable management |

## 4. Project Structure

```text
project/
│
├── src/
│   │
│   ├── agents/
│   │   ├── main.py
│   │   ├── openai_agent.py
│   │   ├── guardrails.py
│   │   ├── tracing.py
│   │   └── traces.jsonl
│   │
│   ├── mcp_server/
│   │   └── server.py
│   │
│   ├── services/
│   │   └── leave_service.py
│   │
│   └── storage/
│       └── storage_json.py
│
├── .env
├── .gitignore
├── README.md
└── DOCUMENTATION.md
```

The `traces.jsonl` file is generated at runtime and should be excluded from Git.

## 5. MCP Server Integration

### 5.1 MCPServerStdio

The OpenAI Agents SDK connects to the existing HR MCP server through `MCPServerStdio`.

The server is launched as a subprocess using the Python executable from the active virtual environment.

Example configuration:

```python
mcp_server = MCPServerStdio(
    name="HR Leave Management MCP Server",
    params={
        "command": sys.executable,
        "args": ["-m", "src.mcp_server.server"],
        "cwd": str(PROJECT_ROOT),
    },
    cache_tools_list=True,
)
```

**Important configuration details:**

- `name`: Identifies the MCP server.
- `command`: Specifies the Python executable.
- `args`: Specifies the MCP server module to execute.
- `cwd`: Sets the project root as the working directory.
- `cache_tools_list`: Enables caching of the discovered tools list.

The SDK manages the server subprocess and communicates with it through STDIO transport.

### 5.2 MCP Tool Discovery

The MCP server exposes four tools:

| Tool | Responsibility |
|---|---|
| `check_leave_balance` | Retrieves an employee's available leave balance |
| `submit_leave_application` | Submits a new leave application |
| `get_pending_leave_requests` | Retrieves pending leave applications |
| `review_leave_application` | Reviews a leave application |

The HR agent discovers these tools through the MCP server connection.

### 5.3 Connecting MCP Tools to the Agent

The MCP server is attached to the HR agent:

```python
hr_agent = Agent(
    name="HR Leave Assistant",
    instructions="Handle HR leave-related requests using MCP tools.",
    mcp_servers=[mcp_server],
)
```

The `mcp_servers` parameter makes the server's discovered tools available to the agent.

The language model interprets the user's request and decides which tool to call.

## 6. Multi-Agent Architecture

### 6.1 HR Leave Assistant

The HR Leave Assistant is the specialist agent responsible for leave-related operations.

Its responsibilities include:

- Checking employee leave balances.
- Submitting leave applications.
- Retrieving pending applications.
- Reviewing leave requests.

It uses the connected MCP server to execute these operations.

### 6.2 Triage Agent

The Triage Agent acts as the entry point for user requests.

Its responsibilities include:

- Receiving user queries.
- Applying the configured input guardrail.
- Identifying HR-related requests.
- Delegating appropriate requests to the HR Leave Assistant.

### 6.3 Agent Handoffs

Handoffs allow one agent to transfer control to another specialized agent.

The Triage Agent is configured with:

```python
triage_agent = Agent(
    name="Triage Agent",
    instructions="Route HR-related requests to the HR Leave Assistant.",
    handoffs=[hr_agent],
    input_guardrails=[hr_domain_guardrail],
)
```

The `handoffs` parameter registers the HR specialist as a destination agent.

When an HR-related request is received, the Triage Agent can transfer control to the HR Leave Assistant.

## 7. Input Guardrails

### 7.1 Purpose

Guardrails provide a validation mechanism for controlling which requests an agent should process.

This project implements an HR-domain input guardrail.

It checks whether the user's query contains relevant HR keywords.

Examples of accepted keywords include:

- leave
- employee
- balance
- application
- pending
- approve
- reject
- absence

### 7.2 Guardrail Implementation

The guardrail uses the `input_guardrail` decorator and returns a `GuardrailFunctionOutput`.

```python
return GuardrailFunctionOutput(
    output_info="HR domain validation",
    tripwire_triggered=not is_hr_related,
)
```

If the request is unrelated to HR, the tripwire is triggered.

### 7.3 Exception Handling

The main application handles the guardrail exception:

```python
except InputGuardrailTripwireTriggered:
    print(
        "Request blocked: Only HR-related queries are allowed."
    )
```

This prevents unrelated requests from proceeding through the normal agent workflow.

**Note:** The current implementation uses keyword matching as a simple demonstration. It is not a comprehensive semantic classifier and may need improvement for production use.

## 8. Local Tracing and Execution Monitoring

### 8.1 Purpose

Tracing provides visibility into the execution of an agent workflow.

It helps developers understand:

- Which agent processed a request.
- Whether a guardrail was triggered.
- Whether a handoff occurred.
- Which MCP tools were called.
- What inputs and outputs were exchanged.
- Token usage and execution events.

### 8.2 Custom Tracing Processor

A custom `LocalTracingProcessor` is implemented in `tracing.py`.

It extends the SDK's `TracingProcessor` interface.

The processor captures events through methods such as:

- `on_trace_start()`
- `on_trace_end()`
- `on_span_start()`
- `on_span_end()`

Completed spans and trace events are written to:

```text
src/agents/traces.jsonl
```

The file uses JSON Lines format, meaning each line represents an individual JSON event.

### 8.3 Configuring Local Tracing

The custom processor is registered using:

```python
set_trace_processors([
    LocalTracingProcessor()
])
```

This configures the application to use the local processor instead of the default trace processor list.

### 8.4 Trace Events

The trace file can contain different types of events:

| Event / Span | Description |
|---|---|
| `trace_started` | Indicates that a workflow has started |
| `trace_completed` | Indicates that a workflow has finished |
| `guardrail` | Records guardrail validation |
| `handoff` | Records transfer between agents |
| `mcp_tools` | Records discovered MCP tools |
| `function` | Records an executed tool call |
| `agent` | Records agent execution |
| `response` | Records model response and usage information |

Local tracing is useful for debugging and inspecting the workflow without relying on access to another person's OpenAI dashboard.

**Security consideration:** Trace files may contain employee identifiers, tool inputs, outputs, and other execution details. They should not be committed to a public repository.

## 9. Main Application Workflow

The `main.py` file is the application's entry point.

Its responsibilities include:

1. Loading environment variables.
2. Registering the local tracing processor.
3. Starting the MCP server connection.
4. Discovering available MCP tools.
5. Accepting user queries through an interactive loop.
6. Running the Triage Agent.
7. Handling guardrail exceptions.
8. Displaying the final response.

### 9.1 Running the Agent

The application uses:

```python
result = await Runner.run(
    triage_agent,
    user_query
)

print(result.final_output)
```

`Runner.run()` executes the agent workflow and returns the final result.

The application continues accepting requests until the user enters `exit`.

## 10. End-to-End Testing

The following scenarios were tested successfully.

### Test Case 1: Single MCP Tool Call

**Input:**

```text
Check the leave balance for employee EMP001.
```

**Expected behavior:**

- Guardrail allows the request.
- Triage Agent hands off to HR Leave Assistant.
- HR agent calls `check_leave_balance`.
- Employee balance is returned.

**Observed result:**

```json
{
    "employee_id": "EMP001",
    "employee_name": "Ali Khan",
    "annual_leave_balance": 17
}
```

**Status:** Passed.

### Test Case 2: Multiple MCP Tool Calls

**Input:**

```text
Check the leave balance of employee EMP001
and show all pending leave requests.
```

**Expected behavior:**

The HR Leave Assistant executes:

1. `check_leave_balance`
2. `get_pending_leave_requests`

Both function spans were observed in the same workflow trace.

**Status:** Passed.

### Test Case 3: Guardrail Validation

**Input:**

```text
Write me a Python game.
```

**Expected behavior:**

- The guardrail identifies the request as unrelated to HR.
- The tripwire is triggered.
- The request is blocked.
- No handoff or MCP business tool execution occurs.

**Observed trace:**

```json
{
    "type": "guardrail",
    "name": "hr_domain_guardrail",
    "triggered": true
}
```

**Status:** Passed.

## 11. Installation and Execution

### Prerequisites

- Python installed.
- Existing HR Leave Management MCP project.
- OpenAI API key.
- Required project dependencies.

### Install Agents SDK

```bash
pip install openai-agents python-dotenv
```

Install the remaining dependencies required by the existing MCP project.

### Environment Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key
```

Do not commit this file to Git.

### Run the Application

From the project root:

```bash
python -m src.agents.main
```

The MCP server is started automatically by the Agents SDK through `MCPServerStdio`.

Type `exit` to stop the interactive application.

## 12. Key Concepts Demonstrated

| Concept | How it is used |
|---|---|
| MCP | Standardized communication between the agent and external tools |
| FastMCP | Creates the HR MCP server |
| MCPServerStdio | Connects the Agents SDK to the MCP server |
| Agent | Defines a specialized AI assistant |
| Runner | Executes the agent workflow |
| Handoff | Transfers control between specialized agents |
| Guardrail | Validates incoming user requests |
| Tracing | Records workflow execution and tool activity |

## 13. Conclusion

This project demonstrates the integration of the OpenAI Agents SDK with an existing MCP server to build a multi-agent HR application.

The implementation covers MCP tool discovery and execution, agent handoffs, input guardrails, local tracing, and end-to-end testing.

It provides practical experience in building AI agent workflows that interact with external services through the Model Context Protocol.