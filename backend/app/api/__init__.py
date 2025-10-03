from fastapi import APIRouter
from app.api.v1 import news, sources, categories

api_router = APIRouter()

api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])