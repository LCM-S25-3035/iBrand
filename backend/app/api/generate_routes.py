import os
import json
from fastapi import APIRouter, HTTPException
from app.schemas.posts import PostCreate
from app.schemas.news import NewsItem
from openai import OpenAI

router = APIRouter()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
@router.post("/generate-post", response_model=PostCreate)
async def generate_post(news: NewsItem):
    """
    Generate a LinkedIn post and brand-consistent DALL·E image.
    """

    # Compose messages for GPT-4
    messages = [
        {
            "role": "system",
            "content": (
                "You are a social media copywriter for Tim Hortons. "
                "Generate a LinkedIn post in a friendly Canadian tone. "
                "Include up to 5 hashtags. "
                "Also generate a DALL·E image prompt describing a scene matching the Tim Hortons brand and the news topic. "
                "Do not include brand logos or text in the image prompt. "
                "Return ONLY JSON like:\n"
                "{\n"
                "  \"platform\": \"LinkedIn\",\n"
                "  \"content\": \"...\",\n"
                "  \"hashtags\": [\"#tag1\", \"#tag2\"],\n"
                "  \"image_prompt\": \"...\"\n"
                "}"
            )
        },
        {
            "role": "user",
            "content": f"News Title: {news.title}\n\nSummary: {news.summary}\n\nURL: {news.url}"
        }
    ]

    try:
        # 1. Generate post content & image prompt
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
        )

        post_json = json.loads(completion.choices[0].message.content.strip())

        # 2. Generate the image with DALL·E
        dalle_response = client.images.generate(
            model="dall-e-3",
            prompt=post_json["image_prompt"],
            size="1024x1024"
        )

        image_url = dalle_response.data[0].url

        return PostCreate(
            platform=post_json["platform"],
            content=post_json["content"],
            hashtags=post_json["hashtags"],
            image=image_url,
            news_id=getattr(news, "id", None)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
