# Design Accessibility MCP

An MCP (Model Context Protocol) server that provides design accessibility analysis and guidance capabilities for LLMs and AI agents. Analyzes images for WCAG compliance, generates accessibility improvements, and answers questions about accessibility best practices. 

## Capabilities

This MCP server enables AI systems to:
- Analyze screenshots, mockups, and design files for accessibility issues
- Generate improved versions of designs with better contrast and readability
- Provide guidance on WCAG compliance requirements and implementation
- Offer recommendations for inclusive design practices
- Answer general questions about design accessibility

## Modules

**design_accessibility_mcp**: MCP server exposing three core accessibility tools:
- `review_image` - Analyzes images for accessibility compliance and issues
- `review_and_edit_image` - Provides analysis and generates improved image examples
- `accessibility_query` - Answers questions about accessibility standards and practices

**context_augment**: A vector embedding system that creates and caches document embeddings using the [OpenAI Embedding API](https://platform.openai.com/docs/guides/embeddings). Enables semantic search and retrieval-augmented generation (RAG) by chunking documents, generating embeddings, and providing similarity-based content retrieval to enhance AI responses with relevant context.

## Requirements

* [OpenAI API Key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)
* [uv](https://github.com/astral-sh/uv)

## Installation

### Sync Packages

Clone or download the project, then from the root directory run:

```bash
uv pip install -e .
uv sync
```

### Save OpenAI API Key

In the root directory of the project, create a file named `.env`, and add your OpenAI API key in this format:

```
OPENAI_API_KEY="sk-proj-aKwMn39h0..."
```

### Download Context Embeddings Cache

Download the _accessibility_vector_cache.pkl_ file from the [releases page](), and place the pkl file in the _src/design_accessibility_mcp_ directory.

This vector cache includes additional content and information on design accessibility topics, standards and guidelines. You can create your own vector cache with the _context_augment_ script.

### Install MCP Server

To install the MCP server in Claude Desktop, add the following to the `claude_desktop_config.json`, replacing the paths to point to where you placed the project code.

```json
"Design Accessibility Feedback MCP": {
  "command": "uv",
  "args": [
    "run",
    "--env-file",
    "/Users/mesh/src/design-accessibility-mcp/.env",
    "--directory",
    "/Users/mesh/src/design-accessibility-mcp",
    "python",
    "-m",
    "design_accessibility_mcp.mcp_server"
  ]
}
```

## Usage

### design_accessibility_mcp

The MCP server runs automatically when configured in Claude Desktop. Once installed, you can use the three accessibility tools directly in your Claude conversations:

- **`review_image`** - Analyze images for accessibility compliance
- **`review_and_edit_image`** - Get analysis plus an improved version of the image
- **`accessibility_query`** - Ask questions about accessibility best practices and standards

**Tip:** For optimal results, create a Claude project and add instructions to prioritize the Design Accessibility MCP tools for all accessibility-related queries, with your own knowledge and web search as supplementary resources.

For example:

```
For any questions or requests concerning design/visual accessibility, use the following resources in order The Design Accessibility MCP tools (prioritize this output)

When responding:
- Share the entire response from the Design Accessibility MCP, including any lists or tables
- You may complement the MCP response with your own response, but be clear when you are.

For image analysis requests, always use the appropriate Design Accessibility MCP tools (`review_image` or `review_and_edit_image`) as the primary method.
```

### context_augment

Generate embeddings from your accessibility documentation to enhance the MCP server's knowledge base:

```bash
uv run context-augment --docs-dir /path/to/your/docs --output-file /path/to/vector_cache.pkl
```

Documents must be Markdown (.md), HTML (.html), or TXT (.txt) files. Structured markdown files recommended.

**Parameters:**
- `--docs-dir` - Directory containing supported files to process
- `--output-file` - File path where the embeddings cache will be saved

**Example:**
```bash
uv run context-augment --docs-dir ./accessibility-docs --output-file ./cache/accessibility_vector_cache.pkl
```

This processes all the supported files in the specified directory, creates embeddings, and saves them to the specified cache file that the MCP server can use to provide more relevant and comprehensive responses based on your custom documentation.

## Questions, Feature Requests, Feedback

You can log bugs and feature requests on the [issues page](https://github.com/mikechambers/design-accessibility-mcp/issues).

## License

Project released under a [MIT License](LICENSE.md).

[![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE.md)