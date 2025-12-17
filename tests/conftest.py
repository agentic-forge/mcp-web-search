"""Pytest configuration and fixtures."""

import pytest
import respx
from httpx import Response

from .fixtures import (
    EMPTY_WEB_SEARCH_RESPONSE,
    IMAGE_SEARCH_RESPONSE,
    NEWS_SEARCH_RESPONSE,
    SUGGEST_RESPONSE,
    VIDEO_SEARCH_RESPONSE,
    WEB_SEARCH_RESPONSE,
)


@pytest.fixture(autouse=True)
def _set_api_key(monkeypatch):
    """Ensure API key is set for all tests."""
    monkeypatch.setenv("BRAVE_API_KEY", "test-api-key")


@pytest.fixture
def _mock_web_search(respx_mock: respx.MockRouter):
    """Mock successful web search response."""
    respx_mock.get(
        "https://api.search.brave.com/res/v1/web/search",
    ).mock(return_value=Response(200, json=WEB_SEARCH_RESPONSE))
    return respx_mock


@pytest.fixture
def _mock_web_search_empty(respx_mock: respx.MockRouter):
    """Mock empty web search response."""
    respx_mock.get(
        "https://api.search.brave.com/res/v1/web/search",
    ).mock(return_value=Response(200, json=EMPTY_WEB_SEARCH_RESPONSE))
    return respx_mock


@pytest.fixture
def _mock_news_search(respx_mock: respx.MockRouter):
    """Mock successful news search response."""
    respx_mock.get(
        "https://api.search.brave.com/res/v1/news/search",
    ).mock(return_value=Response(200, json=NEWS_SEARCH_RESPONSE))
    return respx_mock


@pytest.fixture
def _mock_image_search(respx_mock: respx.MockRouter):
    """Mock successful image search response."""
    respx_mock.get(
        "https://api.search.brave.com/res/v1/images/search",
    ).mock(return_value=Response(200, json=IMAGE_SEARCH_RESPONSE))
    return respx_mock


@pytest.fixture
def _mock_video_search(respx_mock: respx.MockRouter):
    """Mock successful video search response."""
    respx_mock.get(
        "https://api.search.brave.com/res/v1/videos/search",
    ).mock(return_value=Response(200, json=VIDEO_SEARCH_RESPONSE))
    return respx_mock


@pytest.fixture
def _mock_suggest(respx_mock: respx.MockRouter):
    """Mock successful suggest response."""
    respx_mock.get(
        "https://api.search.brave.com/res/v1/suggest/search",
    ).mock(return_value=Response(200, json=SUGGEST_RESPONSE))
    return respx_mock


@pytest.fixture
def _mock_unauthorized(respx_mock: respx.MockRouter):
    """Mock unauthorized (401) response."""
    respx_mock.get(
        "https://api.search.brave.com/res/v1/web/search",
    ).mock(return_value=Response(401, json={"error": "Invalid API key"}))
    return respx_mock


@pytest.fixture
def _mock_rate_limit(respx_mock: respx.MockRouter):
    """Mock rate limit (429) response."""
    respx_mock.get(
        "https://api.search.brave.com/res/v1/web/search",
    ).mock(return_value=Response(429, json={"error": "Rate limit exceeded"}))
    return respx_mock


@pytest.fixture
def _mock_server_error(respx_mock: respx.MockRouter):
    """Mock server error (500) response."""
    respx_mock.get(
        "https://api.search.brave.com/res/v1/web/search",
    ).mock(return_value=Response(500, text="Internal Server Error"))
    return respx_mock
