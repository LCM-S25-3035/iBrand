from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
import os
from dotenv import load_dotenv
from fastapi import Query


# === Constants for repeated strings ===
INVALID_OBJECT_ID_MSG = "Invalid ObjectId format"
POST_NOT_FOUND_MSG = "Post not found"

# Load env vars
load_dotenv()
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
def serialize(post) -> dict:
    post["id"] = str(post["_id"])
    del post["_id"]
    return post

# === CRUD Endpoints ===


@app.get("/posts/{post_id}", response_model=ArticleInDB)
def get_post(post_id: str):
    if not is_valid_object_id(post_id):
        raise HTTPException(status_code=400, detail=INVALID_OBJECT_ID_MSG)
    post = collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail=POST_NOT_FOUND_MSG)
    return serialize(post)

@app.put("/posts/{post_id}", response_model=ArticleInDB)
def update_post(post_id: str, post: Article):
    if not is_valid_object_id(post_id):
        raise HTTPException(status_code=400, detail=INVALID_OBJECT_ID_MSG)
    result = collection.update_one({"_id": ObjectId(post_id)}, {"$set": post.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=POST_NOT_FOUND_MSG)
    updated_post = collection.find_one({"_id": ObjectId(post_id)})
    return serialize(updated_post)

@app.delete("/posts/{post_id}")
def delete_post(post_id: str):
    if not is_valid_object_id(post_id):
        raise HTTPException(status_code=400, detail=INVALID_OBJECT_ID_MSG)
    result = collection.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=POST_NOT_FOUND_MSG)
    return {"message": "Post deleted successfully"}
