from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId
from starlette import status
from models import user_model


router = APIRouter()


@router.get("/{sailor_id}/resume", status_code=status.HTTP_200_OK, response_model=user_model)
async def get_resume(sailor_id: str):
    try:

        resume = await user_model.get(sailor_id)

        if not resume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No resume found")

        return resume

    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)
