from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from starlette import status
from typing import Annotated
from models import user_model, company_model, auth
from api.auth.config import get_current_user
import shutil

router = APIRouter()


@router.post("/load-photo")
async def photo_and_logo(current_user: Annotated[dict, Depends(get_current_user)],
                         photo: UploadFile = File(...)):
    try:

        photo.filename = photo.filename.lower()
        path = f"static/{photo.filename}"

        with open(path, 'wb+') as buffer:
            shutil.copyfileobj(photo.file, buffer)

        user_id = current_user.get('id')

        if current_user['role'] == 'Моряк':

            user_info = await auth.get(user_id)

            resume = await user_model.get(user_info.resumeID)

            await resume.update({"$set": {"photo_path": path}})

            return resume

        elif current_user['role'] == 'Компания':

            company_info = await auth.get(user_id)

            resume = await company_model.get(company_info.resumeID)

            await resume.update({"$set": {"photo_path": path}})

            return resume

    except HTTPException as e:
        return HTTPException(detail=e.detail, status_code=status.HTTP_400_BAD_REQUEST)