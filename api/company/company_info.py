from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from starlette import status
from api.auth.auth import get_current_user

router = APIRouter()


@router.get('/navy')
async def get_navy(page: int = 1, page_size: int = 4):
    try:

        pass

    except HTTPException as e:

        return HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
