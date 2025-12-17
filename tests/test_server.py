"""Tests for MCP server tools via the underlying client."""

import respx
from httpx import Response

from forge_mcp_web_search.server import get_client, mcp

from .fixtures import (
    IMAGE_SEARCH_RESPONSE,
    NEWS_SEARCH_RESPONSE,
    SUGGEST_RESPONSE,
    VIDEO_SEARCH_RESPONSE,
    WEB_SEARCH_RESPONSE,
)


class TestServerModule:
    """Tests for the server module itself."""

    def test_mcp_server_exists(self):
        """Test that the MCP server is properly created."""
        assert mcp is not None
        assert mcp.name == "Web Search Server"

    def test_tools_are_registered(self):
        """Test that all tools are registered with the MCP server."""
        # Get registered tools
        tools = list(mcp._tool_manager._tools.keys())

        assert "web_search" in tools
        assert "news_search" in tools
        assert "image_search" in tools
        assert "video_search" in tools
        assert "suggest" in tools
        assert len(tools) == 5


class TestWebSearchTool:
    """Tests for the web_search tool functionality."""

    @respx.mock
    async def test_web_search_tool(self, _set_api_key):
        """Test web search via the server's client."""
        respx.get(
            "https://api.search.brave.com/res/v1/web/search",
        ).mock(return_value=Response(200, json=WEB_SEARCH_RESPONSE))

        client = get_client()
        result = await client.web_search("Python tutorial")

        assert len(result.results) == 2
        assert result.results[0].title == "Python Tutorial - W3Schools"


class TestNewsSearchTool:
    """Tests for the news_search tool functionality."""

    @respx.mock
    async def test_news_search_tool(self, _set_api_key):
        """Test news search via the server's client."""
        respx.get(
            "https://api.search.brave.com/res/v1/news/search",
        ).mock(return_value=Response(200, json=NEWS_SEARCH_RESPONSE))

        client = get_client()
        result = await client.news_search("AI news")

        assert len(result.results) == 2
        assert result.results[0].source == "techcrunch.com"


class TestImageSearchTool:
    """Tests for the image_search tool functionality."""

    @respx.mock
    async def test_image_search_tool(self, _set_api_key):
        """Test image search via the server's client."""
        respx.get(
            "https://api.search.brave.com/res/v1/images/search",
        ).mock(return_value=Response(200, json=IMAGE_SEARCH_RESPONSE))

        client = get_client()
        result = await client.image_search("sunset mountains")

        assert len(result.results) == 2
        assert result.results[0].width == 1920


class TestVideoSearchTool:
    """Tests for the video_search tool functionality."""

    @respx.mock
    async def test_video_search_tool(self, _set_api_key):
        """Test video search via the server's client."""
        respx.get(
            "https://api.search.brave.com/res/v1/videos/search",
        ).mock(return_value=Response(200, json=VIDEO_SEARCH_RESPONSE))

        client = get_client()
        result = await client.video_search("Python tutorial")

        assert len(result.results) == 2
        assert result.results[0].duration == "3:45:00"


class TestSuggestTool:
    """Tests for the suggest tool functionality."""

    @respx.mock
    async def test_suggest_tool(self, _set_api_key):
        """Test suggest via the server's client."""
        respx.get(
            "https://api.search.brave.com/res/v1/suggest/search",
        ).mock(return_value=Response(200, json=SUGGEST_RESPONSE))

        client = get_client()
        result = await client.suggest("how to")

        assert len(result.suggestions) == 5
