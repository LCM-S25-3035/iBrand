import pytest
from bson import ObjectId
from mongomock_motor import AsyncMongoMockClient
from app.schemas.news import NewsCreate
from app.db import mongodb
from app.services.news import get_news, get_news_by_id, create_news, update_news, delete_news

@pytest.fixture(autouse=True)
async def setup_db():
    # Create a mock MongoDB client and override the real one
    mock_client = AsyncMongoMockClient()
    mongodb.news_collection = mock_client.db.test_news  # Patch with test collection
    yield

@pytest.mark.asyncio
async def test_create_and_get_news():
    news_data = NewsCreate(title="Test Title", content="Test content", author="Author A")
    new_doc = await create_news(news_data)
    
    assert new_doc["title"] == "Test Title"
    assert new_doc["content"] == "Test content"
    assert new_doc["author"] == "Author A"
    assert "_id" in new_doc

@pytest.mark.asyncio
async def test_get_news():
    # Insert multiple news
    for i in range(3):
        await create_news(NewsCreate(title=f"Title {i}", content="Body", author="Author"))

    news_list = await get_news()
    assert len(news_list) == 3
    assert all("title" in item for item in news_list)

@pytest.mark.asyncio
async def test_get_news_by_id():
    news_data = NewsCreate(title="Single", content="Only this", author="X")
    inserted = await create_news(news_data)
    
    fetched = await get_news_by_id(inserted["_id"])
    assert fetched["title"] == "Single"
    assert fetched["author"] == "X"

@pytest.mark.asyncio
async def test_update_news():
    news_data = NewsCreate(title="Before", content="Content", author="Y")
    inserted = await create_news(news_data)

    await update_news(inserted["_id"], {"title": "After"})
    updated = await get_news_by_id(inserted["_id"])
    assert updated["title"] == "After"

@pytest.mark.asyncio
async def test_delete_news():
    news_data = NewsCreate(title="ToDelete", content="Bye", author="Z")
    inserted = await create_news(news_data)
    response = await delete_news(inserted["_id"])
    assert response.deleted_count == 1

    should_be_none = await get_news_by_id(inserted["_id"])
    assert should_be_none is None
