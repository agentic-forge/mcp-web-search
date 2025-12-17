"""Brave Search API client and models."""

from .client import BraveSearchClient, SearchError
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

__all__ = [
    "BraveSearchClient",
    "SearchError",
    "WebSearchResult",
    "WebSearchResponse",
    "NewsResult",
    "NewsSearchResponse",
    "ImageResult",
    "ImageSearchResponse",
    "VideoResult",
    "VideoSearchResponse",
    "SuggestResponse",
]
