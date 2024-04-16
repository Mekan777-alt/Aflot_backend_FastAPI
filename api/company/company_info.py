from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from api.auth.config import get_current_user
from typing import Annotated

router = APIRouter()


@router.get('/navy')
async def get_navy(current_user: Annotated[dict, Depends(get_current_user)], page: int = 1, page_size: int = 4):
    try:

        pass

    except HTTPException as e:

        return HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
