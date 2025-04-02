# MCP 101 - AI Agent Sees Colors

This example demonstrates how to create an MCP tool that analyzes images and determines their dominant color. The tool can identify basic colors (red, blue, green, yellow) or return a hex color code for other colors.

## Setup Steps

### 1. Prerequisites
First, make sure you have UV installed on your system. [What is UV?](../docs/uv.md)

### 2. Set up the project environment
```bash
# Navigate to the project root directory
cd /path/to/mcp-for-dummies

# Create a new virtual environment
uv venv

# Install the package in editable mode with dev dependencies
uv pip install -e .
```

### 3. Test the server
Run the server locally to ensure it works:
```bash
# Run from the project root directory
uv --directory . run mcp-101-detect-colors/server.py
```
The server should start without any errors. Press Ctrl+C to stop it once you've verified it works.

### 4. Configure MCP Server
Copy this MCP configuration to your AI Agent's configuration file. [How to update the MCP Server JSON?](../docs/mcp-file-location.md)

```json
{
  "mcpServers": {
    "detect-colors-101": {
      "command": "uv",
      "args": [
        "--directory",
        "/full/path/to/mcp-for-dummies",
        "run",
        "mcp-101-detect-colors/server.py"
      ]
    }
  }
}
```

Note: Replace `/full/path/to/mcp-for-dummies` with the actual full path to your project directory.

### 5. Verify server status
After configuring:
1. Check your AI Agent's MCP Server status
2. If you don't see the server running, try reloading the Agent
3. The server should appear as "detect-colors-101" in your MCP servers list

### 6. Test the color detection
1. Open your AI Agent chat
2. Find an image on the internet (must be accessible via URL)
3. Paste the image URL into the chat
4. The Agent will use the MCP server to analyze the image and tell you its dominant color

Example chat interaction:
```
You: Can you tell me the dominant color in this image? https://example.com/red-flower.jpg
Agent: Let me analyze that image for you... The dominant color is red.
```

## Output

The tool will return one of the following:
- Basic color names: "red", "blue", "green", "yellow"
- Hex color code (e.g., "#ff0000") for colors that don't match the basic categories
- Error message if the image cannot be fetched or processed

