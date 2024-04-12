from fastapi import APIRouter
from .get_news import router

news_router = APIRouter(
    tags=["News"],
)


news_router.include_router(router)
