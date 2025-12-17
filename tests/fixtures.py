"""Mock API responses for testing."""

WEB_SEARCH_RESPONSE = {
    "query": {"original": "Python tutorial"},
    "web": {
        "total": 1000000,
        "results": [
            {
                "title": "Python Tutorial - W3Schools",
                "url": "https://www.w3schools.com/python/",
                "description": "Learn Python programming with our comprehensive tutorial.",
                "age": "2 days ago",
                "language": "en",
                "family_friendly": True,
            },
            {
                "title": "The Python Tutorial - Python.org",
                "url": "https://docs.python.org/3/tutorial/",
                "description": "Official Python tutorial from python.org.",
                "age": "1 week ago",
                "language": "en",
                "family_friendly": True,
            },
        ],
    },
}

NEWS_SEARCH_RESPONSE = {
    "query": {"original": "AI news"},
    "results": [
        {
            "title": "OpenAI Announces New Model",
            "url": "https://example.com/openai-news",
            "description": "OpenAI has announced a new language model.",
            "meta_url": {"hostname": "techcrunch.com"},
            "age": "2 hours ago",
            "thumbnail": {"src": "https://example.com/thumb1.jpg"},
        },
        {
            "title": "Google's AI Advances",
            "url": "https://example.com/google-ai",
            "description": "Google announces new AI capabilities.",
            "meta_url": {"hostname": "theverge.com"},
            "age": "5 hours ago",
            "thumbnail": None,
        },
    ],
}

IMAGE_SEARCH_RESPONSE = {
    "query": {"original": "sunset mountains"},
    "results": [
        {
            "title": "Beautiful Sunset Over Mountains",
            "url": "https://example.com/sunset-page",
            "properties": {
                "url": "https://example.com/images/sunset.jpg",
                "width": 1920,
                "height": 1080,
            },
            "thumbnail": {"src": "https://example.com/thumbs/sunset_thumb.jpg"},
            "source": "unsplash.com",
        },
        {
            "title": "Mountain Sunset Panorama",
            "url": "https://example.com/panorama-page",
            "properties": {
                "url": "https://example.com/images/panorama.jpg",
                "width": 4000,
                "height": 2000,
            },
            "thumbnail": {"src": "https://example.com/thumbs/panorama_thumb.jpg"},
            "source": "pexels.com",
        },
    ],
}

VIDEO_SEARCH_RESPONSE = {
    "query": {"original": "Python tutorial"},
    "results": [
        {
            "title": "Python Tutorial for Beginners",
            "url": "https://youtube.com/watch?v=abc123",
            "description": "Learn Python in this comprehensive beginner tutorial.",
            "thumbnail": {"src": "https://i.ytimg.com/vi/abc123/hqdefault.jpg"},
            "video": {"duration": "3:45:00", "views": "10M views"},
            "meta_url": {"hostname": "youtube.com"},
            "age": "1 year ago",
        },
        {
            "title": "Advanced Python Programming",
            "url": "https://youtube.com/watch?v=def456",
            "description": "Take your Python skills to the next level.",
            "thumbnail": {"src": "https://i.ytimg.com/vi/def456/hqdefault.jpg"},
            "video": {"duration": "2:30:00", "views": "500K views"},
            "meta_url": {"hostname": "youtube.com"},
            "age": "6 months ago",
        },
    ],
}

SUGGEST_RESPONSE = {
    "query": {"original": "how to"},
    "results": [
        {"query": "how to learn python"},
        {"query": "how to cook pasta"},
        {"query": "how to lose weight"},
        {"query": "how to make money online"},
        {"query": "how to tie a tie"},
    ],
}

# Alternative format some endpoints use
SUGGEST_RESPONSE_STRING_FORMAT = {
    "query": "how to",
    "results": [
        "how to learn python",
        "how to cook pasta",
        "how to lose weight",
    ],
}

ERROR_UNAUTHORIZED = {"error": "Invalid API key"}

ERROR_RATE_LIMIT = {"error": "Rate limit exceeded"}

EMPTY_WEB_SEARCH_RESPONSE = {
    "query": {"original": "xyznonexistentquery123"},
    "web": {"total": 0, "results": []},
}
