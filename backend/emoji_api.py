from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Dummy emoji generation function (replace with real logic)
def generate_emoji_from_text(text: str, mood: Optional[str] = None) -> str:
    # TODO: Use `text` for actual emoji generation logic in future
    _ = text  # Prevents unused variable warning for now
    return "😊" if mood == "happy" else "😐"


app = FastAPI(title="EmojiGen API", description="API to generate custom emojis and stickers")

class TextInput(BaseModel):
    text: str
    mood: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Welcome to EmojiGen API!"}

@app.post("/generate")
def generate_emoji(data: TextInput):
    try:
        emoji = generate_emoji_from_text(data.text, mood=data.mood)
        return {"emoji": emoji}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("emoji_api:app", host="127.0.0.1", port=8001, reload=True)
