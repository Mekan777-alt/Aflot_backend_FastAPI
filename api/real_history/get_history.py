from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from models import real_history
from typing import List
from api.auth.config import get_current_user
from typing import Annotated

router = APIRouter(
    prefix="/api/v1",
    tags=["Real History"],
)


@router.get("/real-history", status_code=status.HTTP_200_OK, response_model=List[real_history])
async def get_history(current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        history = await real_history.find().to_list()

        if not history:

            raise HTTPException(detail="No history found", status_code=status.HTTP_404_NOT_FOUND)

        return history
    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)
