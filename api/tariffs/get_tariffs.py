from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from models import swims_tariffs, description_tariffs, company_tariffs

router = APIRouter()


@router.get("/get_tariffs/company")
async def get_tariffs_company():
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
