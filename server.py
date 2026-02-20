import httpx
import json
import sys

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Clixon MCP Server")

_config_cache: dict = {}
_config_url: str = ""


@mcp.tool()
def fetch_config(
    url: str,
    username: str = "",
    password: str = "",
    verify_ssl: bool = False,
) -> str:
    """
    Fetch network device configuration via RESTCONF.

    Args:
        url: RESTCONF URL, e.g. https://device:8443/restconf/data
        username: HTTP basic auth username (optional).
        password: HTTP basic auth password (optional).
        verify_ssl: Whether to verify SSL certificates (default: False).
    """

    global _config_cache, _config_url

    headers = {"Accept": "application/yang-data+json"}

    try:
        auth = (username, password) if username else None
        response = httpx.get(
            url,
            headers=headers,
            auth=auth,
            verify=verify_ssl,
            timeout=30,
        )
        response.raise_for_status()
        _config_cache = response.json()
        _config_url = url
        return json.dumps(_config_cache, indent=2)
    except Exception as e:
        return f"Error fetching config: {e}"


@mcp.tool()
def get_config() -> str:
    """
    Return the currently cached RESTCONF configuration.

    Call fetch_config first to load configuration from a device.
    """

    if not _config_cache:
        return "No configuration cached. Use fetch_config to load from a device."

    return json.dumps(_config_cache, indent=2)


@mcp.tool()
def get_config_path(path: str) -> str:
    """
    Extract a specific section from the cached configuration by dot-separated path.

    Args:
        path: Dot-separated path into the config, e.g.
              "ietf-interfaces:interfaces" or
              "ietf-interfaces:interfaces.interface"
    """

    if not _config_cache:
        return "No configuration cached. Use fetch_config to load from a device."

    current = _config_cache

    for key in path.split("."):
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return f"Path '{path}' not found in configuration."

    return json.dumps(current, indent=2) if not isinstance(current, str) else current


@mcp.resource("config://server-info")
def server_info() -> str:
    """
    Return server metadata as JSON.
    """

    return json.dumps(
        {
            "name": "Clixon MCP Server",
            "version": "0.1.0",
            "python_version": f"{__import__('sys').version}",
            "tools": ["fetch_config", "get_config", "get_config_path"],
        },
        indent=2,
    )


@mcp.prompt()
def analyze_config(url: str) -> str:
    """
    Create a prompt to fetch and analyze device configuration.
    """

    return (
        f"Please fetch the RESTCONF configuration from '{url}', "
        f"then provide an overview of the device configuration including:\n"
        f"1. Configured interfaces and their status\n"
        f"2. Routing configuration\n"
        f"3. Any other notable settings"
    )


if __name__ == "__main__":
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    mcp.run(transport=transport)
