from fastapi import Depends, HTTPException, APIRouter
from starlette.responses import JSONResponse
from starlette import status
from beanie import PydanticObjectId
from models import auth, company_model
from schemas.profile.profile_company import CompanyOldSettings

router = APIRouter(
    prefix="/api/v1",
    tags=["Company Profile"],
)


@router.get("/{company_id}/profile", status_code=status.HTTP_200_OK)
async def get_company_profile(company_id: PydanticObjectId):
    try:
        company_data = await company_model.get(company_id)

        if not company_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

        del company_data.vacancies

        return company_data

    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))


@router.get("/{company_id}/profile/old_settings", status_code=status.HTTP_200_OK, response_model=CompanyOldSettings)
async def get_company_old_settings(company_id: PydanticObjectId):
    try:

        company = await company_model.get(company_id)

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

        return company

    except HTTPException as e:

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.put("/{company_id}/profile/old_settings/save", status_code=status.HTTP_200_OK, response_model=CompanyOldSettings)
async def save_company_profile(company_id: PydanticObjectId, request: CompanyOldSettings):
    try:
        company = await company_model.get(company_id)
        auth_model = await auth.find_one({"email": company.email})

        if not company or not auth_model:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

        request = {k: v for k, v in request.dict().items() if v is not None}

        update_query = {"$set": {
            field: value for field, value in request.items()
        }}

        await company.update(update_query)
        await auth_model.update(update_query)

        return company
    except HTTPException as e:

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
