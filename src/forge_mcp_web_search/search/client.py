"""Brave Search API client."""

import os
from typing import Literal

import httpx

from .models import (
    ImageResult,
    ImageSearchResponse,
    NewsResult,
    NewsSearchResponse,
    SuggestResponse,
    VideoResult,
    VideoSearchResponse,
    WebSearchResponse,
    WebSearchResult,
)


class SearchError(Exception):
    """Base exception for search errors."""

    pass


class APIKeyMissingError(SearchError):
    """API key is not configured."""

    pass


class RateLimitError(SearchError):
    """Rate limit exceeded."""

    pass


class APIError(SearchError):
    """Error from Brave Search API."""

    pass


class BraveSearchClient:
    """Async client for Brave Search API."""

    BASE_URL = "https://api.search.brave.com/res/v1"

    def __init__(self, api_key: str | None = None, timeout: float = 30.0):
        """Initialize the client.

        Args:
            api_key: Brave Search API key. If not provided, reads from BRAVE_API_KEY env var.
            timeout: Request timeout in seconds.
        """
        self.api_key = api_key or os.environ.get("BRAVE_API_KEY")
        if not self.api_key:
            raise APIKeyMissingError(
                "BRAVE_API_KEY environment variable is required. "
                "Get your API key at https://brave.com/search/api/"
            )
        self.timeout = timeout

    async def _request(self, endpoint: str, params: dict) -> dict:
        """Make an authenticated request to Brave Search API.

        Args:
            endpoint: API endpoint (e.g., 'web/search')
            params: Query parameters

        Returns:
            JSON response as dict

        Raises:
            RateLimitError: If rate limit exceeded (429)
            APIError: For other API errors
        """
        headers = {
            "X-Subscription-Token": self.api_key,
            "Accept": "application/json",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.BASE_URL}/{endpoint}",
                params=params,
                headers=headers,
            )

            if response.status_code == 401:
                raise APIError("Invalid API key")
            if response.status_code == 429:
                raise RateLimitError(
                    "Rate limit exceeded. Free tier: 1 req/sec, 2000/month. "
                    "Consider upgrading at https://brave.com/search/api/"
                )
            if response.status_code != 200:
                raise APIError(f"API request failed: {response.status_code} {response.text}")

            return response.json()

    async def web_search(
        self,
        query: str,
        count: int = 10,
        country: str | None = None,
        search_lang: str | None = None,
        freshness: Literal["pd", "pw", "pm", "py"] | None = None,
        safe_search: Literal["off", "moderate", "strict"] = "moderate",
    ) -> WebSearchResponse:
        """Search the web.

        Args:
            query: Search query (max 400 characters, 50 words)
            count: Number of results (1-20)
            country: Country code (e.g., 'us', 'gb', 'de')
            search_lang: Language code (e.g., 'en', 'de', 'fr')
            freshness: Time filter - pd (past day), pw (past week),
                      pm (past month), py (past year)
            safe_search: Content filter level

        Returns:
            WebSearchResponse with results
        """
        params: dict = {
            "q": query,
            "count": min(max(count, 1), 20),
            "safesearch": safe_search,
        }

        if country:
            params["country"] = country
        if search_lang:
            params["search_lang"] = search_lang
        if freshness:
            params["freshness"] = freshness

        data = await self._request("web/search", params)

        # Parse web results
        results = []
        web_data = data.get("web", {})
        for item in web_data.get("results", []):
            results.append(
                WebSearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    description=item.get("description", ""),
                    age=item.get("age"),
                    language=item.get("language"),
                    family_friendly=item.get("family_friendly", True),
                )
            )

        return WebSearchResponse(
            query=data.get("query", {}).get("original", query),
            total_results=web_data.get("total"),
            results=results,
        )

    async def news_search(
        self,
        query: str,
        count: int = 10,
        country: str | None = None,
        search_lang: str | None = None,
        freshness: Literal["pd", "pw", "pm", "py"] | None = None,
        safe_search: Literal["off", "moderate", "strict"] = "moderate",
    ) -> NewsSearchResponse:
        """Search for news articles.

        Args:
            query: Search query
            count: Number of results (1-20)
            country: Country code
            search_lang: Language code
            freshness: Time filter
            safe_search: Content filter level

        Returns:
            NewsSearchResponse with news articles
        """
        params: dict = {
            "q": query,
            "count": min(max(count, 1), 20),
            "safesearch": safe_search,
        }

        if country:
            params["country"] = country
        if search_lang:
            params["search_lang"] = search_lang
        if freshness:
            params["freshness"] = freshness

        data = await self._request("news/search", params)

        results = []
        for item in data.get("results", []):
            thumbnail = None
            if item.get("thumbnail"):
                thumbnail = item["thumbnail"].get("src")

            results.append(
                NewsResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    description=item.get("description", ""),
                    source=item.get("meta_url", {}).get("hostname", "Unknown"),
                    published=item.get("age", ""),
                    thumbnail=thumbnail,
                )
            )

        return NewsSearchResponse(
            query=data.get("query", {}).get("original", query),
            results=results,
        )

    async def image_search(
        self,
        query: str,
        count: int = 10,
        country: str | None = None,
        safe_search: Literal["off", "moderate", "strict"] = "moderate",
    ) -> ImageSearchResponse:
        """Search for images.

        Args:
            query: Search query
            count: Number of results (1-20)
            country: Country code
            safe_search: Content filter level

        Returns:
            ImageSearchResponse with image results
        """
        params: dict = {
            "q": query,
            "count": min(max(count, 1), 20),
            "safesearch": safe_search,
        }

        if country:
            params["country"] = country

        data = await self._request("images/search", params)

        results = []
        for item in data.get("results", []):
            properties = item.get("properties", {})
            thumbnail = item.get("thumbnail", {})

            results.append(
                ImageResult(
                    title=item.get("title", ""),
                    url=properties.get("url", item.get("url", "")),
                    source_url=item.get("url", ""),
                    thumbnail=thumbnail.get("src", ""),
                    width=properties.get("width", 0),
                    height=properties.get("height", 0),
                    source=item.get("source", ""),
                )
            )

        return ImageSearchResponse(
            query=data.get("query", {}).get("original", query),
            results=results,
        )

    async def video_search(
        self,
        query: str,
        count: int = 10,
        country: str | None = None,
        search_lang: str | None = None,
        freshness: Literal["pd", "pw", "pm", "py"] | None = None,
        safe_search: Literal["off", "moderate", "strict"] = "moderate",
    ) -> VideoSearchResponse:
        """Search for videos.

        Args:
            query: Search query
            count: Number of results (1-20)
            country: Country code
            search_lang: Language code
            freshness: Time filter
            safe_search: Content filter level

        Returns:
            VideoSearchResponse with video results
        """
        params: dict = {
            "q": query,
            "count": min(max(count, 1), 20),
            "safesearch": safe_search,
        }

        if country:
            params["country"] = country
        if search_lang:
            params["search_lang"] = search_lang
        if freshness:
            params["freshness"] = freshness

        data = await self._request("videos/search", params)

        results = []
        for item in data.get("results", []):
            thumbnail = item.get("thumbnail", {})

            results.append(
                VideoResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    description=item.get("description", ""),
                    thumbnail=thumbnail.get("src", ""),
                    duration=item.get("video", {}).get("duration"),
                    source=item.get("meta_url", {}).get("hostname", "Unknown"),
                    published=item.get("age"),
                    views=item.get("video", {}).get("views"),
                )
            )

        return VideoSearchResponse(
            query=data.get("query", {}).get("original", query),
            results=results,
        )

    async def suggest(
        self,
        query: str,
        count: int = 5,
        country: str | None = None,
    ) -> SuggestResponse:
        """Get search suggestions/autocomplete.

        Args:
            query: Partial search query
            count: Number of suggestions (1-10)
            country: Country code

        Returns:
            SuggestResponse with suggested queries
        """
        params: dict = {
            "q": query,
            "count": min(max(count, 1), 10),
        }

        if country:
            params["country"] = country

        data = await self._request("suggest/search", params)

        # Extract suggestions from response
        suggestions = []
        for item in data.get("results", []):
            if isinstance(item, dict):
                suggestions.append(item.get("query", ""))
            elif isinstance(item, str):
                suggestions.append(item)

        # Extract original query from response
        query_data = data.get("query", {})
        if isinstance(query_data, dict):
            original_query = query_data.get("original", query)
        else:
            original_query = query

        return SuggestResponse(
            query=original_query,
            suggestions=suggestions,
        )
