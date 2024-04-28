from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from models.news import news_model
from models.db import db
from beanie import PydanticObjectId
from typing import Annotated, List
from api.auth.config import get_current_user
from schemas.news.get_news_schemas import NewsSchema, ImageData, ImageInfo, NewsResponse

import json


router = APIRouter()


@router.get('/news', status_code=status.HTTP_200_OK)
async def news_get(page: int = 1, page_size: int = 10):
    try:

        skip = (page - 1) * page_size
        limit = page_size

        total_news = await news_model.find().skip(skip).limit(limit).to_list()


        return total_news
    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/news/{news_id}')
async def get_news_id(news_id: PydanticObjectId, current_user: Annotated[dict, Depends(get_current_user)]):
    try:


        news_obj = await news_model.get(news_id)

        if not news_obj:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='News not found')

        return news_obj
    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)