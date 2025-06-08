from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["multimodal"]
collection = db["posts"]

app = FastAPI()

# Pydantic model for Post
class Post(BaseModel):
    title: str
    content: str
    author: Optional[str] = None
    published_date: Optional[str] = None
    url: Optional[str] = None

class PostInDB(Post):
    id: str

def serialize(post) -> dict:
    post["id"] = str(post["_id"])
    del post["_id"]
    return post

# === CRUD Endpoints ===

@app.post("/posts/", response_model=PostInDB)
def create_post(post: Post):
    result = collection.insert_one(post.dict())
    new_post = collection.find_one({"_id": result.inserted_id})
    return serialize(new_post)

@app.get("/posts/", response_model=List[PostInDB])
def get_all_posts():
    return [serialize(post) for post in collection.find()]

@app.get("/posts/{post_id}", response_model=PostInDB)
def get_post(post_id: str):
    post = collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return serialize(post)

@app.put("/posts/{post_id}", response_model=PostInDB)
def update_post(post_id: str, post: Post):
    result = collection.update_one({"_id": ObjectId(post_id)}, {"$set": post.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    updated_post = collection.find_one({"_id": ObjectId(post_id)})
    return serialize(updated_post)

@app.delete("/posts/{post_id}")
def delete_post(post_id: str):
    result = collection.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
