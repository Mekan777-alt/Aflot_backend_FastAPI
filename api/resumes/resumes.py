import math
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from typing import Annotated
from api.auth.config import get_current_user
from models.register import user_model
from starlette import status
from beanie import PydanticObjectId


router = APIRouter()


@router.get("/resumes", response_model=List[user_model])
async def get_all_vacancies_user(page: int = 1, page_size: int = 6):
    try:

        skip = (page - 1) * page_size
        limit = page_size

        total_count = await user_model.find().count()
        total_pages = math.ceil(total_count / page_size)

        vacancies = await user_model.find().skip(skip).limit(limit).to_list()

        return vacancies

    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/resumes/{sailor_id}", response_model=user_model)
async def get_user_vacancy(user_id: PydanticObjectId):
    try:

        user_vacancy = await user_model.get(user_id)

        if not user_vacancy:

            raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)

        return user_vacancy

    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/resumes/{sailor_id}/add_favorite", response_model=user_model, status_code=status.HTTP_201_CREATED)
async def add_user_to_favorite(user_id: PydanticObjectId, current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        user_favorite = await user_model.get(user_id)

        if not user_favorite:

            raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)



    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/resumes/search")
async def search_resume(current_user: Annotated[dict, Depends(get_current_user)],
                        title: str = Query(None), salary: int = Query(None)):

    try:

        query = {}

        if title:

            query["title"] = {"$regex": title, "$options": "i"}

        if salary:

            query["salary"] = {"$gte": salary}

        resume = user_model.find(query).to_list()

        return resume

    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)