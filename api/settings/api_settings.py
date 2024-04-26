from fastapi import APIRouter, HTTPException
from models import position, vessel
from starlette import status
from typing import List

router = APIRouter()


@router.get("/settings", status_code=status.HTTP_200_OK)
async def get_settings():
    try:

        data_list = []

        position_models = await position.find().to_list()

        if position_models:

            data_list.append(position_models)
        else:

            pass
        vessel_models = await vessel.find().to_list()

        if vessel_models:

            data_list.append(vessel_models)
        else:

            pass

        return data_list
    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)