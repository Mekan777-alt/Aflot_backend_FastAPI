from fastapi import APIRouter, HTTPException
from starlette import status


router = APIRouter()


@router.get("/main", status_code=status.HTTP_200_OK)
async def main_page():
    try:

        pass


    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)