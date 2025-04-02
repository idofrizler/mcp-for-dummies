# MCP Server Configuration File Locations

This document details where to place your MCP Server configuration JSON file based on your AI agent system.

The JSON file has this format:
```json
{
  "mcpServers": {
    "my-first-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/full/path/to/my-first-mcp/folder/",
        "run",
        "/relative/path/to/server.py"
      ]
    }
    //, "another-mcp": { ... }
  }
}
```
If it already exists, add another JSON sub-entry next to the existing ones, under the top-level `mcpServers` key.

## Cursor
1. On the Cursor menu, go to `File -> Preferences -> Cursor Settings`
2. Go to `MCP` on the opened menu
3. Click `Add new global MCP server`
4. Save the MCP JSON format (the one with "mcpServers") into the opened file.

## Cline
1. On the Cline top menu, click the `MCP Server` icon (the one looking like three stacked servers)
2. Click `Installed`, and then `Configure MCP Servers`
3. Save the MCP JSON format (the one with "mcpServers") into the opened file.
