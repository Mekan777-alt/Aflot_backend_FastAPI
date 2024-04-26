from fastapi import APIRouter, HTTPException
from starlette import status

router = APIRouter()


@router.post("/")
async def photo_and_logo():
    try:

        pass

    except HTTPException as e:
        return HTTPException(detail=e.detail, status_code=status.HTTP_400_BAD_REQUEST)