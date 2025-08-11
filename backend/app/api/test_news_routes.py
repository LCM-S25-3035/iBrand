import pytest
from httpx import AsyncClient
from mongomock_motor import AsyncMongoMockClient
from fastapi import FastAPI
from app.api import news as news_router  # Import your router file
from app.db import mongodb
from app.schemas.news import NewsCreate

# --- Fixtures ---
@pytest.fixture(autouse=True)
async def setup_db(monkeypatch):
    """Patch MongoDB with an in-memory mock before each test."""
    mock_client = AsyncMongoMockClient()
    mock_collection = mock_client.db.test_news
    monkeypatch.setattr("app.crud.news.news_collection", mock_collection)
    yield

@pytest.fixture
def test_app():
    """Create a FastAPI app with the news router mounted."""
    app = FastAPI()
    app.include_router(news_router.router)
    return app

# --- Tests ---
@pytest.mark.asyncio
async def test_create_and_get_news(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        # Create
        payload = {"title": "Breaking News", "content": "Some content", "author": "Reporter X"}
        create_resp = await ac.post("/news/", json=payload)
        assert create_resp.status_code == 200
        data = create_resp.json()
        assert data["title"] == payload["title"]
        assert "_id" in data

        # Get list
        list_resp = await ac.get("/news/")
        assert list_resp.status_code == 200
        news_list = list_resp.json()
        assert len(news_list) == 1
        assert news_list[0]["title"] == "Breaking News"

        # Get single by ID
        news_id = data["_id"]
        get_resp = await ac.get(f"/news/{news_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["title"] == "Breaking News"

@pytest.mark.asyncio
async def test_get_news_not_found(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        resp = await ac.get("/news/66c2f97e5ac9e5b5cbf3f3f3")  # random ObjectId
        assert resp.status_code == 404
        assert resp.json()["detail"] == "News not found"

@pytest.mark.asyncio
async def test_update_news(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        # Create one
        payload = {"title": "Old", "content": "Something", "author": "A"}
        created = await ac.post("/news/", json=payload)
        news_id = created.json()["_id"]

        # Update
        update_payload = {"title": "Updated", "content": "Something", "author": "A"}
        upd_resp = await ac.put(f"/news/{news_id}", json=update_payload)
        assert upd_resp.status_code == 200
        assert upd_resp.json()["title"] == "Updated"
