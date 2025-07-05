#accessibility-mcp

accessibility-mcp provides an MCP server that expands existing LLMs / Agents to provide information, suggestions and feedback on design accessibility topics, as well as accessibility feedback for images and design.

It provides two modules:

**accessibility_mcp** : MCP server that exposes accessibility feedback, review and edit functionality

**context_augement** : Script that enables the creation of serialized vector embeddings, using the [OpenAI Vector Embedding API](https://platform.openai.com/docs/guides/embeddings), to allow customizing and enhancing AI response with specific content. 

## Requirements

OpenAI API Key.

##Installation


### Sync Packages
Download / sync the project to you computer, and then from within the root directory run:

```
uv pip install -e .
uv sync
```

### Download Context Embeddings Cache



### Install MCP Server

To install the MCP server in Claude Desktop, add the following to the *claude_desktop_config.json", replacing the paths to point to where you place the project code.

```javascript
"Design Accessibility Feedback MCP": {
  "command": "uv",
  "args": [
    "run",
    "--env-file",
    "/Users/ACCOUNT_NAME/src/accessibility-mcp/.env",
    "--directory",
    "/Users/ACCOUNT_NAME/src/accessibility-mcp",
    "python",
    "-m",
    "accessibility_mcp.mcp_server"
  ]
}
```

## Usage

### accessibility_mcp

### context_augment