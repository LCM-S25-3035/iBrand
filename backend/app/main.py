from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi import Query


# === Constants for repeated strings ===
INVALID_OBJECT_ID_MSG = "Invalid ObjectId format"
NEWS_NOT_FOUND_MSG = "News article not found"

# Load .env from this file's directory
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["articles-db"]
collection = db["articles"]

app = FastAPI()

# === Utility Function to Validate ObjectId ===
def is_valid_object_id(id: str) -> bool:
    try:
        ObjectId(id)
        return True
    except InvalidId:
        return False

# === Pydantic Schemas ===
class Article(BaseModel):
    url: str
    source: str
    title: str
    author: Optional[str] = None
    published_at: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None

class ArticleInDB(Article):
    id: str

# === Serialization Helper ===
def serialize(news) -> dict:
    news["id"] = str(news["_id"])
    del news["_id"]
    return news

# === CRUD Endpoints ===

@app.get("/news/{news_id}", response_model=ArticleInDB)
def get_news_by_id(news_id: str):
    if not is_valid_object_id(news_id):
        raise HTTPException(status_code=400, detail=INVALID_OBJECT_ID_MSG)
    news = collection.find_one({"_id": ObjectId(news_id)})
    if not news:
        raise HTTPException(status_code=404, detail=NEWS_NOT_FOUND_MSG)
    return serialize(news)

@app.put("/news/{news_id}", response_model=ArticleInDB)
def update_news_by_id(news_id: str, article: Article):
    if not is_valid_object_id(news_id):
        raise HTTPException(status_code=400, detail=INVALID_OBJECT_ID_MSG)
    result = collection.update_one({"_id": ObjectId(news_id)}, {"$set": article.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=NEWS_NOT_FOUND_MSG)
    updated_news = collection.find_one({"_id": ObjectId(news_id)})
    return serialize(updated_news)

@app.delete("/news/{news_id}")
def delete_news_by_id(news_id: str):
    if not is_valid_object_id(news_id):
        raise HTTPException(status_code=400, detail=INVALID_OBJECT_ID_MSG)
    result = collection.delete_one({"_id": ObjectId(news_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=NEWS_NOT_FOUND_MSG)
    return {"message": "News article deleted successfully"}
