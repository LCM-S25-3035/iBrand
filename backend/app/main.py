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

# === Constants for MongoDB operators ===
MONGO_REGEX = "$regex"
MONGO_OPTIONS = "$options"


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


# === Constants for Pagination  ===
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100


# === Pagination Response Model ===
class PaginatedArticles(BaseModel):
    current_page: int
    max_page: int
    total_items: int
    items: List[ArticleInDB]


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


# ✅ NEW: Filter + Pagination endpoint
@app.get("/news", response_model=PaginatedArticles)  # <-- Update response_model here
def get_all_news(
    author: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
):
    query = {}

    if author:
        query["author"] = {MONGO_REGEX: author, MONGO_OPTIONS: "i"}
    if source:
        query["source"] = {MONGO_REGEX: source, MONGO_OPTIONS: "i"}
    if title:
        query["title"] = {MONGO_REGEX: title, MONGO_OPTIONS: "i"}


    total_items = collection.count_documents(query)
    cursor = collection.find(query).skip(skip).limit(limit)
    news_list = [serialize(news) for news in cursor]

    current_page = (skip // limit) + 1 if limit else 1
    max_page = (total_items + limit - 1) // limit  # ceiling division

    return {
        "current_page": current_page,
        "max_page": max_page,
        "total_items": total_items,
        "items": news_list,
    }