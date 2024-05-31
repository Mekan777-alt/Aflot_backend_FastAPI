from fastapi import Depends, HTTPException, APIRouter
from starlette.responses import JSONResponse
from starlette import status
from beanie import PydanticObjectId
from models import auth, company_model
from schemas.profile.profile_company import CompanyOldSettings
from typing import Annotated
from api.auth.config import get_current_user
from schemas.profile.profile_company import CompanySchema

router = APIRouter()


@router.get("/profile", status_code=status.HTTP_200_OK, response_model=CompanySchema,
            summary="Возвращает профиль компании")
async def get_company_profile(current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        company_id = current_user.get('id')

        company_info = await auth.get(company_id)

        if not company_info:

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Company not found")

        resume = await company_model.get(company_info.resumeID)

        return resume

    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))


@router.get("/profile/old_settings", status_code=status.HTTP_200_OK, response_model=CompanyOldSettings,
            summary="Возвращает ДОП настройки профиля компании")
async def get_company_old_settings(current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        company_id = current_user.get('id')

        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Company not found")

        resume = await company_model.get(company_info.resumeID)

        return resume

    except HTTPException as e:

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.put("/profile/old_settings/save", status_code=status.HTTP_200_OK, response_model=CompanyOldSettings,
            summary="Изменение ДОП настроек профиля компании")
async def save_company_profile(request: CompanyOldSettings, current_user: Annotated[dict, Depends(get_current_user)]):
    try:
        company_id = current_user.get('id')

        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Company not found")

        resume = await company_model.get(company_info.resumeID)

        request = {k: v for k, v in request.dict().items() if v is not None}

        update_query = {"$set": {
            field: value for field, value in request.items()
        }}

        await resume.update(update_query)
        await company_info.update(update_query)

        return company_info
    except HTTPException as e:

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
