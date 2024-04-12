from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from models.news import news_model
from typing import Annotated
from beanie import PydanticObjectId


router = APIRouter(
    prefix="/api/v1",
)


@router.get('/news')
async def news(page: int = 1, page_size: int = 10):
    try:

        skip = (page - 1) * page_size
        limit = page_size

        total_news = await news_model.find().skip(skip).limit(limit).to_list()

        if not total_news:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No news')

        return total_news

    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/news/{news_id}')
async def get_news_id(news_id: PydanticObjectId):
    try:


        news_obj = await news_model.get(news_id)

        if not news_obj:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='News not found')

        return news_obj
    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)