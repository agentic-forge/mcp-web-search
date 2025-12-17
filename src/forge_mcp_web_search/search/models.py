"""Pydantic models for Brave Search API responses."""

from pydantic import BaseModel, Field


class WebSearchResult(BaseModel):
    """A single web search result."""

    title: str = Field(description="Page title")
    url: str = Field(description="Page URL")
    description: str = Field(description="Page description/snippet")
    age: str | None = Field(default=None, description="Result age (e.g., '2 hours ago')")
    language: str | None = Field(default=None, description="Page language")
    family_friendly: bool = Field(default=True, description="Whether result is family friendly")


class WebSearchResponse(BaseModel):
    """Response from web search."""

    query: str = Field(description="Original search query")
    total_results: int | None = Field(default=None, description="Estimated total results")
    results: list[WebSearchResult] = Field(description="Search results")


class NewsResult(BaseModel):
    """A single news search result."""

    title: str = Field(description="Article title")
    url: str = Field(description="Article URL")
    description: str = Field(description="Article description/snippet")
    source: str = Field(description="News source name")
    published: str = Field(description="Publication date/time")
    thumbnail: str | None = Field(default=None, description="Thumbnail image URL")


class NewsSearchResponse(BaseModel):
    """Response from news search."""

    query: str = Field(description="Original search query")
    results: list[NewsResult] = Field(description="News results")


class ImageResult(BaseModel):
    """A single image search result."""

    title: str = Field(description="Image title")
    url: str = Field(description="Full image URL")
    source_url: str = Field(description="Source page URL")
    thumbnail: str = Field(description="Thumbnail URL")
    width: int = Field(description="Image width in pixels")
    height: int = Field(description="Image height in pixels")
    source: str | None = Field(default=None, description="Source website name")


class ImageSearchResponse(BaseModel):
    """Response from image search."""

    query: str = Field(description="Original search query")
    results: list[ImageResult] = Field(description="Image results")


class VideoResult(BaseModel):
    """A single video search result."""

    title: str = Field(description="Video title")
    url: str = Field(description="Video page URL")
    description: str = Field(description="Video description")
    thumbnail: str = Field(description="Video thumbnail URL")
    duration: str | None = Field(default=None, description="Video duration (e.g., '5:30')")
    source: str = Field(description="Video platform/source")
    published: str | None = Field(default=None, description="Publication date")
    views: str | None = Field(default=None, description="View count")


class VideoSearchResponse(BaseModel):
    """Response from video search."""

    query: str = Field(description="Original search query")
    results: list[VideoResult] = Field(description="Video results")


class SuggestResponse(BaseModel):
    """Response from search suggestions."""

    query: str = Field(description="Original partial query")
    suggestions: list[str] = Field(description="Suggested search queries")
