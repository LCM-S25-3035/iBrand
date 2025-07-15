from fastapi import APIRouter, HTTPException
from app.schemas.news import NewsCreate, NewsOut
from app.crud import news as news_crud

router = APIRouter(prefix="/news", tags=["News"])

@router.get("/", response_model=list[NewsOut])
async def fetch_all_news(skip: int = 0, limit: int = 10):
    print(f"[DEBUG] Fetching news with skip={skip} & limit={limit}")
    return await news_crud.get_all_news(skip, limit)

@router.get("/{news_id}", response_model=NewsOut)
async def fetch_news_by_id(news_id: str):
    print(f"[DEBUG] Fetching news item with ID: {news_id}")
    result = await news_crud.get_news_by_id(news_id)
    if not result:
        raise HTTPException(status_code=404, detail="News not found")
    return result

@router.post("/", response_model=NewsOut)
async def add_news_item(payload: NewsCreate):
    print(f"[DEBUG] Creating news item: {payload.title}")
    return await news_crud.create_news(payload)

@router.put("/{news_id}", response_model=NewsOut)
async def modify_news_item(news_id: str, payload: NewsCreate):
    print(f"[DEBUG] Updating news item with ID: {news_id}")
    return await news_crud.update_news(news_id, payload.dict(exclude_unset=True))

@router.delete("/{news_id}")
async def remove_news_item(news_id: str):
    print(f"[DEBUG] Deleting news item with ID: {news_id}")
    result = await news_crud.delete_news(news_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="News not found")
    return {"message": f"News item {news_id} has been deleted"}
