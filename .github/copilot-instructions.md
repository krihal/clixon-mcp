# Copilot Instructions

## Build & Run

- **Install dependencies:** `uv sync`
- **Run the server:** `uv run server.py`
- The server uses stdio transport by default and is designed to be launched by an MCP client (e.g., OpenCode)

## Architecture

This is a single-file MCP server (`server.py`) built with the `FastMCP` class from the `mcp` Python SDK. It exposes:

- **Tools** — callable functions (calculate, shell commands, file I/O)
- **Resources** — read-only data endpoints (server info)
- **Prompts** — reusable prompt templates (summarize, explain code)

All tools, resources, and prompts are registered via decorators (`@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()`) on the single `mcp` instance.

## Conventions

- Tools that interact with the filesystem or shell include error handling that returns error strings rather than raising exceptions — this ensures the MCP client always gets a response.
- The `calculate` tool uses a restricted `eval` with an explicit allowlist of safe math functions — new math functions must be added to the `allowed_names` dict.
- Shell commands have a 30-second timeout enforced by `subprocess.run`.

## Adding New Tools

Add a new function in `server.py` decorated with `@mcp.tool()`. Include a docstring — it becomes the tool's description shown to the AI agent.

```python
@mcp.tool()
def my_tool(arg: str) -> str:
    """Description shown to the AI agent."""
    return result
```
