from fastapi import Depends, HTTPException, APIRouter
from starlette.responses import JSONResponse
from starlette import status
from beanie import PydanticObjectId
from models.register import UserModel

router = APIRouter(
    prefix="/api/v1",
    tags=["Company Profile"],
)


@router.get("/{company_id}/profile", response_model=UserModel)
async def get_company_profile(company_id: PydanticObjectId):
    try:
        company_data = await UserModel.get(company_id)

        if not company_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

        del company_data.vacancies
        del company_data.hashed_password

        return company_data

    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))
