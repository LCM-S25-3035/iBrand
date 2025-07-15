from bson import ObjectId
from app.db.mongodb import news_collection
from app.schemas.news import NewsCreate

async def get_all_news(skip: int = 0, limit: int = 10):
    cursor = news_collection.find().skip(skip).limit(limit)
    results = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        results.append(doc)
    return results

async def get_news_by_id(news_id: str):
    try:
        return await news_collection.find_one({"_id": ObjectId(news_id)})
    except Exception as e:
        print(f"[ERROR] Invalid ObjectId: {e}")
        return None

async def create_news(news: NewsCreate):
    payload = news.dict()
    result = await news_collection.insert_one(payload)
    return await get_news_by_id(result.inserted_id)

async def update_news(news_id: str, updated_data: dict):
    await news_collection.update_one(
        {"_id": ObjectId(news_id)},
        {"$set": updated_data}
    )
    return await get_news_by_id(news_id)

async def delete_news(news_id: str):
    return await news_collection.delete_one({"_id": ObjectId(news_id)})
