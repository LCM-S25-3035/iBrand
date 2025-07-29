from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import asyncio
from emojigen_client import EmojiGenClient

app = FastAPI()

# Instantiate the EmojiGen client (update URL & key as needed)
emoji_client = EmojiGenClient(base_url="http://localhost:8001")

class SocialPost(BaseModel):
    text: str
    mood: Optional[str] = None

class EnrichedPost(BaseModel):
    original_text: str
    emojis: list[str]
    stickers: Optional[list[str]] = None

@app.post("/enrich", response_model=EnrichedPost)
async def enrich_post(post: SocialPost):
    try:
        result = await emoji_client.enrich(post.text, mood=post.mood)
        return EnrichedPost(
            original_text=post.text,
            emojis=result.get("emoji", []),
            stickers=result.get("stickers", [])
        )
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"EmojiGen API error: {e}")
