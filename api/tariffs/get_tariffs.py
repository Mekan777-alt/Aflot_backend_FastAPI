from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from api.auth.config import get_current_user
from starlette import status
from typing import List
from models import swims_tariffs, description_tariffs, company_tariffs

router = APIRouter()


@router.get("/get_tariffs/company", status_code=status.HTTP_200_OK, response_model=List[company_tariffs])
async def get_tariffs_company(current_user: Optional[dict] = Depends(get_current_user)):
    try:

        tariffs = await company_tariffs.find().to_list()

        if not tariffs:
            raise HTTPException(detail="No tariffs found", status_code=status.HTTP_404_NOT_FOUND)

        return tariffs

    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/get_tariffs/sailor", status_code=status.HTTP_200_OK)
async def get_tariffs_swims():
    try:

        data = []

        tariffs = await swims_tariffs.find().to_list()

        if not tariffs:
            raise HTTPException(detail="No tariffs found", status_code=status.HTTP_404_NOT_FOUND)

        data.append(tariffs)
        descriptions = await description_tariffs.find().to_list()

        if not descriptions:
            raise HTTPException(detail="No descriptions found", status_code=status.HTTP_404_NOT_FOUND)

        data.append(descriptions)
        return data
    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)
