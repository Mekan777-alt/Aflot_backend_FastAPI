from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from api.auth.config import get_current_user
from typing import Annotated

router = APIRouter()


@router.get('/balance')
async def balance_sailor_company(current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        pass


    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)
