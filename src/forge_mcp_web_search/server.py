"""Web Search MCP Server using FastMCP and Brave Search API."""

from importlib.metadata import version
from typing import Annotated, Literal

from fastmcp import FastMCP
from pydantic import Field

from .search.client import BraveSearchClient
from .search.models import (
    ImageSearchResponse,
    NewsSearchResponse,
    SuggestResponse,
    VideoSearchResponse,
    WebSearchResponse,
)

# Get package version
__version__ = version("forge-mcp-web-search")

# Create FastMCP server
mcp = FastMCP(
    name="Web Search Server",
    version=__version__,
    instructions="""Web search server powered by Brave Search API.

Available tools:
- web_search: Search the web for information
- news_search: Search for recent news articles
- image_search: Search for images
- video_search: Search for videos
- suggest: Get search query suggestions/autocomplete

All searches support country and language filtering.
Time-based filtering available via 'freshness' parameter:
- pd = past day
- pw = past week
- pm = past month
- py = past year

Note: Requires BRAVE_API_KEY environment variable.
Free tier: 2,000 queries/month, 1 query/sec.
Get your API key at https://brave.com/search/api/
""",
)

# Shared client instance (initialized lazily on first use)
_client: BraveSearchClient | None = None


def get_client() -> BraveSearchClient:
    """Get or create the shared client instance."""
    global _client  # noqa: PLW0603
    if _client is None:
        _client = BraveSearchClient()
    return _client


@mcp.tool
async def web_search(
    query: Annotated[str, Field(description="Search query (max 400 chars, 50 words)")],
    count: Annotated[
        int,
        Field(ge=1, le=20, description="Number of results to return"),
    ] = 10,
    country: Annotated[
        str | None,
        Field(description="Country code (e.g., 'us', 'gb', 'de', 'fr')"),
    ] = None,
    search_lang: Annotated[
        str | None,
        Field(description="Language code (e.g., 'en', 'de', 'fr', 'es')"),
    ] = None,
    freshness: Annotated[
        Literal["pd", "pw", "pm", "py"] | None,
        Field(description="Time filter: pd=past day, pw=past week, pm=past month, py=past year"),
    ] = None,
    safe_search: Annotated[
        Literal["off", "moderate", "strict"],
        Field(description="Content filter level"),
    ] = "moderate",
) -> WebSearchResponse:
    """Search the web for information.

    Returns web pages matching the query, including title, URL, description,
    and optionally how recent the content is.

    Examples:
    - web_search(query="Python asyncio tutorial")
    - web_search(query="climate change news", freshness="pw")
    - web_search(query="restaurants berlin", country="de")
    """
    client = get_client()
    return await client.web_search(query, count, country, search_lang, freshness, safe_search)


@mcp.tool
async def news_search(
    query: Annotated[str, Field(description="News search query")],
    count: Annotated[
        int,
        Field(ge=1, le=20, description="Number of results to return"),
    ] = 10,
    country: Annotated[
        str | None,
        Field(description="Country code (e.g., 'us', 'gb', 'de')"),
    ] = None,
    search_lang: Annotated[
        str | None,
        Field(description="Language code (e.g., 'en', 'de', 'fr')"),
    ] = None,
    freshness: Annotated[
        Literal["pd", "pw", "pm", "py"] | None,
        Field(description="Time filter: pd=past day, pw=past week, pm=past month, py=past year"),
    ] = None,
    safe_search: Annotated[
        Literal["off", "moderate", "strict"],
        Field(description="Content filter level"),
    ] = "moderate",
) -> NewsSearchResponse:
    """Search for news articles.

    Returns recent news articles matching the query, including title, URL,
    description, source, publication time, and optional thumbnail.

    Examples:
    - news_search(query="AI regulations")
    - news_search(query="tech layoffs", freshness="pd")
    - news_search(query="bundesliga", country="de")
    """
    client = get_client()
    return await client.news_search(query, count, country, search_lang, freshness, safe_search)


@mcp.tool
async def image_search(
    query: Annotated[str, Field(description="Image search query")],
    count: Annotated[
        int,
        Field(ge=1, le=20, description="Number of results to return"),
    ] = 10,
    country: Annotated[
        str | None,
        Field(description="Country code (e.g., 'us', 'gb', 'de')"),
    ] = None,
    safe_search: Annotated[
        Literal["off", "moderate", "strict"],
        Field(description="Content filter level"),
    ] = "moderate",
) -> ImageSearchResponse:
    """Search for images.

    Returns images matching the query, including full image URL, thumbnail,
    source page URL, and dimensions (width/height).

    Examples:
    - image_search(query="sunset over mountains")
    - image_search(query="modern architecture")
    - image_search(query="cute puppies", safe_search="strict")
    """
    client = get_client()
    return await client.image_search(query, count, country, safe_search)


@mcp.tool
async def video_search(
    query: Annotated[str, Field(description="Video search query")],
    count: Annotated[
        int,
        Field(ge=1, le=20, description="Number of results to return"),
    ] = 10,
    country: Annotated[
        str | None,
        Field(description="Country code (e.g., 'us', 'gb', 'de')"),
    ] = None,
    search_lang: Annotated[
        str | None,
        Field(description="Language code (e.g., 'en', 'de', 'fr')"),
    ] = None,
    freshness: Annotated[
        Literal["pd", "pw", "pm", "py"] | None,
        Field(description="Time filter: pd=past day, pw=past week, pm=past month, py=past year"),
    ] = None,
    safe_search: Annotated[
        Literal["off", "moderate", "strict"],
        Field(description="Content filter level"),
    ] = "moderate",
) -> VideoSearchResponse:
    """Search for videos.

    Returns videos matching the query, including title, URL, description,
    thumbnail, duration, source platform, and view count.

    Examples:
    - video_search(query="Python tutorial for beginners")
    - video_search(query="cooking pasta", freshness="pm")
    - video_search(query="music video", safe_search="strict")
    """
    client = get_client()
    return await client.video_search(query, count, country, search_lang, freshness, safe_search)


@mcp.tool
async def suggest(
    query: Annotated[str, Field(description="Partial search query to get suggestions for")],
    count: Annotated[
        int,
        Field(ge=1, le=10, description="Number of suggestions to return"),
    ] = 5,
    country: Annotated[
        str | None,
        Field(description="Country code for localized suggestions"),
    ] = None,
) -> SuggestResponse:
    """Get search query suggestions/autocomplete.

    Returns suggested search queries based on a partial input.
    Useful for building search UIs with autocomplete functionality.

    Examples:
    - suggest(query="how to")
    - suggest(query="python", count=10)
    - suggest(query="wetter", country="de")
    """
    client = get_client()
    return await client.suggest(query, count, country)


def main():
    """Run the web search MCP server."""
    import argparse
    import logging

    import uvicorn
    from starlette.middleware import Middleware
    from starlette.middleware.cors import CORSMiddleware

    # Suppress benign ClosedResourceError on client disconnect
    logging.getLogger("mcp.server.streamable_http").setLevel(logging.CRITICAL)

    parser = argparse.ArgumentParser(description="Web Search MCP Server")
    parser.add_argument("--stdio", action="store_true", help="Use STDIO transport")
    parser.add_argument("--port", type=int, default=8001, help="Port for HTTP transport")
    parser.add_argument("--host", default="0.0.0.0", help="Host for HTTP transport")
    args = parser.parse_args()

    if args.stdio:
        mcp.run(transport="stdio")
    else:
        from starlette.responses import JSONResponse
        from starlette.routing import Route

        # Add CORS middleware for browser-based clients
        middleware = [
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
                allow_headers=["*"],
                expose_headers=["mcp-session-id"],
            )
        ]
        app = mcp.http_app(middleware=middleware)

        # Add health check endpoint for Docker healthchecks
        async def health_check(request):
            return JSONResponse({"status": "healthy", "service": "mcp-web-search"})

        app.routes.append(Route("/health", health_check))

        print(f"Starting Web Search MCP Server on http://{args.host}:{args.port}/mcp")
        print("Note: BRAVE_API_KEY environment variable must be set")
        uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
