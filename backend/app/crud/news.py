from bson import ObjectId
from app.db.mongodb import news_collection
from app.schemas.news import NewsCreate

async def get_news(skip: int = 0, limit: int = 10):
    cursor = news_collection.find().skip(skip).limit(limit)
    results = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # 👈 Cast ObjectId to string
        results.append(doc)
    return results

async def get_news_by_id(news_id: str):
    return await news_collection.find_one({"_id": ObjectId(news_id)})

async def create_news(news: NewsCreate):
    result = await news_collection.insert_one(news.dict())
    return await get_news_by_id(result.inserted_id)

async def update_news(news_id: str, news: dict):
    await news_collection.update_one({"_id": ObjectId(news_id)}, {"$set": news})
    return await get_news_by_id(news_id)

async def delete_news(news_id: str):
    return await news_collection.delete_one({"_id": ObjectId(news_id)})
