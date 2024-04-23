from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from models.news import news_model
from beanie import PydanticObjectId
from typing import Annotated
from api.auth.config import get_current_user

router = APIRouter()


@router.get('/news')
async def news(current_user: dict = Depends(get_current_user), page: int = 1, page_size: int = 10):
    try:
        skip = (page - 1) * page_size
        limit = page_size

        projection = {
            "photo_path": 1
        }

        total_news = await news_model.find({}, projection).skip(skip).limit(limit).to_list()

        for news_item in total_news:
            if "photo_path" in news_item:
                news_item["photo_path"] = str(news_item["photo_path"])

        if not total_news:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No news')

        return total_news

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('/news/{news_id}')
async def get_news_id(news_id: PydanticObjectId, current_user: Annotated[dict, Depends(get_current_user)]):
    try:


        news_obj = await news_model.get(news_id)

        if not news_obj:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='News not found')

        return news_obj
    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)