from fastapi import APIRouter, Depends, HTTPException
from models.db import db
from starlette import status
from beanie import PydanticObjectId
from typing import Annotated
from api.auth.config import get_current_user

router = APIRouter()


@router.get('/{sailor_id}/favorite/vacancies')
async def get_favorite_vacancies(swims_id: PydanticObjectId, current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        pass

    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/{sailor_id}/favorite/company')
async def get_favorite_company(swims_id: PydanticObjectId, current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        pass

    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)
