# Clixon MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) server for fetching and querying network device configuration via RESTCONF. Connects to Clixon-based (or any RESTCONF-capable) devices and makes the configuration available to AI coding agents like OpenCode.

## Setup

```bash
uv sync
```

## Run

```bash
uv run server.py
```

## Tools

| Tool | Description |
|------|-------------|
| `fetch_config` | Fetch device configuration via RESTCONF (supports basic auth and TLS) |
| `get_config` | Return the currently cached configuration |
| `get_config_path` | Extract a specific section by dot-separated path (e.g. `ietf-interfaces:interfaces.interface`) |

## Resources

- `config://server-info` — Server metadata (name, version, available tools)

## Prompts

- `analyze_config` — Fetch and analyze device configuration (interfaces, routing, etc.)

## Connect to OpenCode

Add to your `opencode.json` (project root or `~/.config/opencode/opencode.json`):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "clixon": {
      "type": "local",
      "command": ["uv", "run", "server.py"],
      "enabled": true
    }
  }
}
```

Adjust the command path if the server isn't in OpenCode's working directory:

```json
"command": ["uv", "run", "/absolute/path/to/mcp/server.py"]
```

## Example Usage in OpenCode

Once connected, ask questions like:

- `Fetch the config from https://mydevice:8443/restconf/data with user admin and password admin`
- `What interfaces are configured?`
- `Show me the routing configuration`
- `Are there any interfaces that are down?`

The AI agent will call `fetch_config` to pull the RESTCONF data, cache it in memory, and then use `get_config` / `get_config_path` to answer follow-up questions about the device configuration.