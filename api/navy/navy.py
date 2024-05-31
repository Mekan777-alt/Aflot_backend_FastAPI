from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from api.auth.config import get_current_user
from typing import Annotated

router = APIRouter()


@router.get('/navy', summary="Морской флот")
async def get_navy(page: int = 1, page_size: int = 10):
    try:

        pass

    except HTTPException as e:

        return HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
