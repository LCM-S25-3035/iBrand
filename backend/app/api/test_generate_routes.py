import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock
from app.api import posts  # Import your file containing the route
from app.schemas.news import NewsItem

@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(posts.router)
    return app

@pytest.fixture(autouse=True)
def mock_openai(monkeypatch):
    """
    Patch the OpenAI client methods used in generate_post
    to return predictable mock responses.
    """
    # Mock the completions.create method
    mock_completion = MagicMock()
    mock_completion.choices = [
        MagicMock(message=MagicMock(content="""
        {
            "platform": "LinkedIn",
            "content": "Exciting news about coffee!",
            "hashtags": ["#TimHortons", "#Coffee", "#Canada"],
            "image_prompt": "A cozy Tim Hortons coffee shop in winter"
        }
        """.strip()))
    ]

    mock_chat = MagicMock()
    mock_chat.completions.create.return_value = mock_completion

    # Mock the images.generate method
    mock_dalle = MagicMock()
    mock_dalle.data = [MagicMock(url="http://fake-image-url.com/image.png")]

    mock_client = MagicMock()
    mock_client.chat = mock_chat
    mock_client.images.generate.return_value = mock_dalle

    # Patch the 'client' in your posts module
    monkeypatch.setattr("app.api.posts.client", mock_client)
    return mock_client


@pytest.mark.asyncio
async def test_generate_post_success(test_app, mock_openai):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        news_payload = {
            "title": "Tim Hortons launches new latte",
            "summary": "A special winter latte is now available nationwide.",
            "url": "https://example.com/news/latte"
        }

        response = await ac.post("/generate-post", json=news_payload)
        assert response.status_code == 200

        data = response.json()
        assert data["platform"] == "LinkedIn"
        assert "Exciting news" in data["content"]
        assert "hashtags" in data
        assert data["image"] == "http://fake-image-url.com/image.png"

        # Ensure OpenAI methods were called
        mock_openai.chat.completions.create.assert_called_once()
        mock_openai.images.generate.assert_called_once()


@pytest.mark.asyncio
async def test_generate_post_openai_failure(test_app, monkeypatch):
    """Simulate an OpenAI API failure."""
    # Patch client.chat.completions.create to raise an error
    def raise_error(*args, **kwargs):
        raise RuntimeError("OpenAI service unavailable")

    monkeypatch.setattr("app.api.posts.client.chat.completions.create", raise_error)

    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        news_payload = {
            "title": "Tim Hortons outage",
            "summary": "App is temporarily down.",
            "url": "https://example.com/news/outage"
        }

        response = await ac.post("/generate-post", json=news_payload)
        assert response.status_code == 500
        assert "OpenAI service unavailable" in response.json()["detail"]
