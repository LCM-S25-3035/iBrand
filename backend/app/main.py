from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.news_routes import router as news_router
from app.api.generate_routes import router as generate_router


app = FastAPI(title="MongoDB News API")

# frontend origin
origins = [
    "http://localhost:3000",     # Next.js dev server
    "http://127.0.0.1:3000",     # alternative localhost
    "http://0.0.0.0:3000",       # alternative dockerized dev
    "https://your-production-frontend.com"  #  production domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news_router)
app.include_router(generate_router)    
