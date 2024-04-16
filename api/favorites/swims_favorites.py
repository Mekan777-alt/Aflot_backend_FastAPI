from fastapi import APIRouter, Depends, HTTPException
from models.db import db
from starlette import status
from beanie import PydanticObjectId


router = APIRouter()


@router.get('/{swims_id}/favorite/vacancies')
async def get_favorite_vacancies(swims_id: PydanticObjectId):
    try:

        pass

    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/{swims_id}/favorite/company')
async def get_favorite_company(swims_id: PydanticObjectId):
    try:

        pass

    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)
