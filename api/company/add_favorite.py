from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from beanie import PydanticObjectId
from starlette.responses import JSONResponse
from models import company_model

router = APIRouter()


@router.get('{company_id}/favorite_sailor')
async def get_favorite_sailor(company_id: PydanticObjectId):
    try:

        pass

    except HTTPException as e:

        return HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)