import math
from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.auth import UserRead
from typing import List
from typing import Annotated
from api.auth.auth import get_current_user
from models.register import user_model
from starlette import status
from beanie import PydanticObjectId


router = APIRouter(
    prefix="/api/v1"
)


@router.get("/resumes", response_model=List[user_model])
async def get_all_vacancies_user(current_user: Annotated[dict, Depends(get_current_user)], page: int = 1,
                                 page_size: int = 6):
    try:

        skip = (page - 1) * page_size
        limit = page_size

        total_count = await user_model.find().count()
        total_pages = math.ceil(total_count / page_size)

        vacancies = await user_model.find().skip(skip).limit(limit).to_list()

        return vacancies

    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/resumes/{user_id}", response_model=UserRead)
async def get_user_vacancy(user_id: PydanticObjectId, current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        user_vacancy = await user_model.get(user_id)

        if not user_vacancy:

            raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)

        return user_vacancy

    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/resumes/search")
async def search_resume(title: str = Query(None), salary: int = Query(None)):

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