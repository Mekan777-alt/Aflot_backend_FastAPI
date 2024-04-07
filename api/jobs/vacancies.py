from fastapi import APIRouter, Depends, HTTPException
from models.register import UserModel, Vacancies
from beanie import PydanticObjectId
from models.jobs import Ship as ShipModel
from starlette import status
from api.auth.config import get_current_user
from starlette.responses import JSONResponse
from schemas.jobs.ship import Ship, ShipRead

router = APIRouter(
    prefix="/api/v1",
    tags=["Vacancies"]
)


@router.post("/{company_id}/create_vacancies", response_model=ShipRead)
async def create_vacancies_by_company(jobs_create: ShipModel, company_id: PydanticObjectId,
                                      current_user: UserModel = Depends(get_current_user)):
    try:

        company_check = await UserModel.get(company_id)

        if not company_check:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не зарегистрирована")

        await jobs_create.create()

        vacancy = Vacancies(id=jobs_create.id)

        if not company_check.vacancies:
            company_check.vacancies = []

        company_check.vacancies.append(vacancy)
        await company_check.save()

        return jobs_create
    except HTTPException as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/{company_id}/vacancies")
async def get_company_vacancies(company_id: PydanticObjectId, current_user: UserModel = Depends(get_current_user)):
    try:
        company_data = await UserModel.get(company_id)
        if not company_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не зарегистрирована")

        vacancies = company_data.vacancies

        vacancies_info = []

        for vacancy in vacancies:
            vacancies_data = await ShipModel.get(vacancy.id)
            if vacancies_data:
                vacancies_info.append(vacancies_data)
            else:
                pass

        return vacancies_info
    except HTTPException as e:

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))


@router.get("/{company_id}/vacancies/{vacancy_id}")
async def get_vacancies_by_company(company_id: PydanticObjectId, vacancy_id: PydanticObjectId,
                                   current_user: UserModel = Depends(get_current_user)):

    try:

        pass

    except HTTPException as e:

        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.put("/{company_id}/vacancies/{vacancy_id}")
async def update_vacancies_by_company(jobs_update: ShipModel, company_id: PydanticObjectId,
                                      user: UserModel = Depends(get_current_user)):
    try:

        pass

    except HTTPException as e:

        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/vacancies")
async def get_all_vacancies(user: UserModel = Depends(get_current_user)):
    try:

        vacancies = await ShipModel.find().to_list()
        return vacancies

    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))


@router.get("/vacancies/{vacancies_id}", response_model=ShipModel)
async def get_vacancies_id(vacancies_id: PydanticObjectId, user: UserModel = Depends(get_current_user)):
    try:

        vacancies = await ShipModel.get(vacancies_id)

        return vacancies

    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))


