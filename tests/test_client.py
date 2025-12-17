"""Tests for BraveSearchClient."""

import pytest
import respx
from httpx import Response

from forge_mcp_web_search.search.client import (
    APIError,
    APIKeyMissingError,
    BraveSearchClient,
    RateLimitError,
)

from .fixtures import (
    IMAGE_SEARCH_RESPONSE,
    NEWS_SEARCH_RESPONSE,
    SUGGEST_RESPONSE,
    VIDEO_SEARCH_RESPONSE,
    WEB_SEARCH_RESPONSE,
)


class TestClientInitialization:
    """Tests for client initialization."""

    def test_client_with_api_key(self):
        """Test client accepts API key directly."""
        client = BraveSearchClient(api_key="test-key")
        assert client.api_key == "test-key"

    def test_client_from_env_var(self, monkeypatch):
        """Test client reads API key from environment."""
        monkeypatch.setenv("BRAVE_API_KEY", "env-key")
        client = BraveSearchClient()
        assert client.api_key == "env-key"

    def test_client_missing_api_key(self, monkeypatch):
        """Test client raises error when API key is missing."""
        monkeypatch.delenv("BRAVE_API_KEY", raising=False)
        with pytest.raises(APIKeyMissingError):
            BraveSearchClient()


class TestWebSearch:
    """Tests for web search."""

    @respx.mock
    async def test_web_search_basic(self):
        """Test basic web search."""
        respx.get(
            "https://api.search.brave.com/res/v1/web/search",
        ).mock(return_value=Response(200, json=WEB_SEARCH_RESPONSE))

        client = BraveSearchClient(api_key="test-key")
        result = await client.web_search("Python tutorial")

        assert result.query == "Python tutorial"
        assert len(result.results) == 2
        assert result.results[0].title == "Python Tutorial - W3Schools"
        assert result.total_results == 1000000

    @respx.mock
    async def test_web_search_with_params(self):
        """Test web search with all parameters."""
        respx.get(
            "https://api.search.brave.com/res/v1/web/search",
        ).mock(return_value=Response(200, json=WEB_SEARCH_RESPONSE))

        client = BraveSearchClient(api_key="test-key")
        result = await client.web_search(
            query="Python tutorial",
            count=5,
            country="us",
            search_lang="en",
            freshness="pw",
            safe_search="strict",
        )

        assert result.query == "Python tutorial"


class TestNewsSearch:
    """Tests for news search."""

    @respx.mock
    async def test_news_search_basic(self):
        """Test basic news search."""
        respx.get(
            "https://api.search.brave.com/res/v1/news/search",
        ).mock(return_value=Response(200, json=NEWS_SEARCH_RESPONSE))

        client = BraveSearchClient(api_key="test-key")
        result = await client.news_search("AI news")

        assert result.query == "AI news"
        assert len(result.results) == 2
        assert result.results[0].title == "OpenAI Announces New Model"
        assert result.results[0].source == "techcrunch.com"
        assert result.results[0].thumbnail == "https://example.com/thumb1.jpg"
        assert result.results[1].thumbnail is None


class TestImageSearch:
    """Tests for image search."""

    @respx.mock
    async def test_image_search_basic(self):
        """Test basic image search."""
        respx.get(
            "https://api.search.brave.com/res/v1/images/search",
        ).mock(return_value=Response(200, json=IMAGE_SEARCH_RESPONSE))

        client = BraveSearchClient(api_key="test-key")
        result = await client.image_search("sunset mountains")

        assert result.query == "sunset mountains"
        assert len(result.results) == 2
        assert result.results[0].title == "Beautiful Sunset Over Mountains"
        assert result.results[0].width == 1920
        assert result.results[0].height == 1080


class TestVideoSearch:
    """Tests for video search."""

    @respx.mock
    async def test_video_search_basic(self):
        """Test basic video search."""
        respx.get(
            "https://api.search.brave.com/res/v1/videos/search",
        ).mock(return_value=Response(200, json=VIDEO_SEARCH_RESPONSE))

        client = BraveSearchClient(api_key="test-key")
        result = await client.video_search("Python tutorial")

        assert result.query == "Python tutorial"
        assert len(result.results) == 2
        assert result.results[0].title == "Python Tutorial for Beginners"
        assert result.results[0].duration == "3:45:00"
        assert result.results[0].views == "10M views"


class TestSuggest:
    """Tests for search suggestions."""

    @respx.mock
    async def test_suggest_basic(self):
        """Test basic suggest."""
        respx.get(
            "https://api.search.brave.com/res/v1/suggest/search",
        ).mock(return_value=Response(200, json=SUGGEST_RESPONSE))

        client = BraveSearchClient(api_key="test-key")
        result = await client.suggest("how to")

        assert result.query == "how to"
        assert len(result.suggestions) == 5
        assert "how to learn python" in result.suggestions


class TestErrorHandling:
    """Tests for error handling."""

    @respx.mock
    async def test_unauthorized_error(self):
        """Test handling of 401 unauthorized."""
        respx.get(
            "https://api.search.brave.com/res/v1/web/search",
        ).mock(return_value=Response(401, json={"error": "Invalid API key"}))

        client = BraveSearchClient(api_key="invalid-key")
        with pytest.raises(APIError, match="Invalid API key"):
            await client.web_search("test")

    @respx.mock
    async def test_rate_limit_error(self):
        """Test handling of 429 rate limit."""
        respx.get(
            "https://api.search.brave.com/res/v1/web/search",
        ).mock(return_value=Response(429, json={"error": "Rate limit exceeded"}))

        client = BraveSearchClient(api_key="test-key")
        with pytest.raises(RateLimitError):
            await client.web_search("test")

    @respx.mock
    async def test_server_error(self):
        """Test handling of 500 server error."""
        respx.get(
            "https://api.search.brave.com/res/v1/web/search",
        ).mock(return_value=Response(500, text="Internal Server Error"))

        client = BraveSearchClient(api_key="test-key")
        with pytest.raises(APIError, match="500"):
            await client.web_search("test")
