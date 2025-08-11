from fastapi import APIRouter, HTTPException
from app.schemas.news import NewsCreate, NewsOut
from app.crud import news

router = APIRouter(prefix="/news", tags=["News"])

@router.get("/", response_model=list[NewsOut])
async def read_news(skip: int = 0, limit: int = 10):
    return await news.get_news(skip, limit)

@router.get("/{news_id}", response_model=NewsOut)
async def read_news_item(news_id: str):
    result = await news.get_news_by_id(news_id)
    if not result:
        raise HTTPException(status_code=404, detail="News not found")
    return result

@router.post("/", response_model=NewsOut)
async def create_news_item(item: NewsCreate):
    return await news.create_news(item)

@router.put("/{news_id}", response_model=NewsOut)
async def update_news_item(news_id: str, item: NewsCreate):
    return await news.update_news(news_id, item.dict(exclude_unset=True))

@router.delete("/{news_id}")
async def delete_news_item(news_id: str):
    result = await news.delete_news(news_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="News not found")
    return {"msg": "Deleted"}
