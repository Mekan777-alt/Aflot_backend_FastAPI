from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId
from starlette import status
from models import user_model, auth
from typing import Annotated
from api.auth.config import get_current_user


router = APIRouter()


@router.get("/resume", status_code=status.HTTP_200_OK)
async def get_resume(current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        if current_user['role'] == 'Компания':

            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        user_id = current_user.get('id')

        resume_id = await auth.get(user_id)

        resume = await user_model.get(resume_id.resumeID)

        if not resume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No resume found")

        return resume

    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


