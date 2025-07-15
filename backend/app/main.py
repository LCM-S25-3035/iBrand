from fastapi import FastAPI
from app.api.news_routes import router as news_router

app = FastAPI(title="MongoDB News API - Version 2")
app.include_router(news_router)
