# mcp-web-search

[![CI](https://github.com/agentic-forge/mcp-web-search/actions/workflows/ci.yml/badge.svg)](https://github.com/agentic-forge/mcp-web-search/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Web Search MCP server using [Brave Search API](https://brave.com/search/api/) built with [FastMCP](https://gofastmcp.com/).

## Features

- **5 search tools** - Web, News, Images, Videos, and Suggestions
- **Rich filtering** - Country, language, freshness, safe search
- **Streaming HTTP transport** - Deploy as a remote MCP server
- **Free tier available** - 2,000 queries/month

## Tools

### `web_search`

Search the web for information.

```python
web_search(query="Python asyncio tutorial")
web_search(query="climate change", freshness="pw", country="us")
```

### `news_search`

Search for recent news articles.

```python
news_search(query="AI regulations")
news_search(query="tech layoffs", freshness="pd")
```

### `image_search`

Search for images.

```python
image_search(query="sunset over mountains")
image_search(query="modern architecture", safe_search="strict")
```

### `video_search`

Search for videos.

```python
video_search(query="Python tutorial for beginners")
video_search(query="cooking pasta", freshness="pm")
```

### `suggest`

Get search query suggestions/autocomplete.

```python
suggest(query="how to")
suggest(query="python", count=10)
```

## Parameters

### Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | str | Search query (required) |
| `count` | int | Number of results (1-20, default: 10) |
| `country` | str | Country code (e.g., 'us', 'gb', 'de') |
| `search_lang` | str | Language code (e.g., 'en', 'de', 'fr') |
| `safe_search` | str | Content filter: 'off', 'moderate', 'strict' |

### Freshness Filter

Filter results by time:

| Value | Meaning |
|-------|---------|
| `pd` | Past day |
| `pw` | Past week |
| `pm` | Past month |
| `py` | Past year |

## Installation

```bash
# Clone the repository
git clone https://github.com/agentic-forge/mcp-web-search.git
cd mcp-web-search

# Install dependencies
uv sync
```

## Configuration

Get your API key from [Brave Search API](https://brave.com/search/api/).

Set the environment variable:

```bash
export BRAVE_API_KEY="your-api-key-here"
```

Or create a `.envrc.local` file:

```bash
export BRAVE_API_KEY="your-api-key-here"
```

## Running the Server

### HTTP Transport (recommended for remote access)

```bash
# Default: HTTP on port 8001
uv run python -m forge_mcp_web_search

# Custom port
uv run python -m forge_mcp_web_search --port 3000
```

Server will be available at `http://localhost:8001/mcp`

### STDIO Transport (for local MCP clients)

```bash
uv run python -m forge_mcp_web_search --stdio
```

## MCP Client Configuration

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "web-search": {
      "command": "uv",
      "args": ["run", "python", "-m", "forge_mcp_web_search", "--stdio"],
      "cwd": "/path/to/mcp-web-search",
      "env": {
        "BRAVE_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Remote HTTP Server

```json
{
  "mcpServers": {
    "web-search": {
      "url": "http://localhost:8001/mcp"
    }
  }
}
```

## Testing with Anvil

Use [forge-anvil](https://github.com/agentic-forge/forge-anvil) to test the server:

```bash
# Start the server
export BRAVE_API_KEY="your-api-key"
uv run python -m forge_mcp_web_search

# In another terminal
cd /path/to/forge-anvil
export ANVIL_SERVER=http://localhost:8001/mcp

# List tools
anvil list-tools

# Search the web
anvil call web_search --json-args '{"query": "Python tutorial"}'

# Search for news
anvil call news_search --json-args '{"query": "AI news", "freshness": "pd"}'

# Get suggestions
anvil call suggest --arg query="how to"
```

## Development

```bash
# Install dev dependencies
uv sync --group dev

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov

# Type checking
uv run basedpyright

# Linting
uv run ruff check .

# Install pre-commit hooks
uv run pre-commit install
```

## API Rate Limits

| Tier | Rate | Monthly Limit | Cost |
|------|------|---------------|------|
| Free AI | 1 req/sec | 2,000 queries | $0 |
| Base AI | 20 req/sec | 20M queries | $5/1k |
| Pro AI | 50 req/sec | Unlimited | $9/1k |

## License

MIT
