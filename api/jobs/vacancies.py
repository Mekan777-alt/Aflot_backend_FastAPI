from fastapi import APIRouter, Depends, HTTPException
from models.register import CompanyModel, Vacancies, UserModel
from beanie import PydanticObjectId
from models.jobs import Ship as ShipModel
from starlette import status
from models.db import db
from api.auth.auth import get_current_user
from starlette.responses import JSONResponse
from schemas.jobs.ship import Ship, ShipRead
from typing import Annotated

router = APIRouter(
    prefix="/api/v1",
    tags=["Vacancies"]
)


@router.post("/{company_id}/create_vacancies", response_model=ShipRead)
async def create_vacancies_by_company(jobs_create: Ship, company_id: PydanticObjectId,
                                      current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        company_check = await CompanyModel.get(company_id)

        if not company_check:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не зарегистрирована")

        jobs_create.status = 'активная вакансия'
        new_vacancy = ShipModel(**jobs_create.dict())

        await new_vacancy.create()

        vacancy = Vacancies(id=new_vacancy.id)

        if not company_check.vacancies:
            company_check.vacancies = []

        company_check.vacancies.append(vacancy)
        await company_check.save()

        return new_vacancy
    except HTTPException as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/{company_id}/vacancies")
async def get_company_vacancies(company_id: PydanticObjectId, current_user: Annotated[dict, Depends(get_current_user)]):
    try:
        company_data = await CompanyModel.get(company_id)
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
                                   current_user: Annotated[dict, Depends(get_current_user)]):

    try:

        company = await CompanyModel.get(company_id)

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не найдена")

        vacancy = await ShipModel.get(vacancy_id)

        if not vacancy:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная вакансия не найдена")

        return vacancy

    except HTTPException as e:

        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.put("/{company_id}/vacancies/{vacancy_id}", response_model=ShipRead)
async def update_vacancies_by_company(request: Ship, company_id: PydanticObjectId, vacancy_id: PydanticObjectId,
                                      current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        request = {k: v for k, v in request.dict().items() if v is not None}

        update_query = {"$set": {
            field: value for field, value in request.items()
        }}

        job = await ShipModel.get(vacancy_id)

        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная вакансия не найдена")

        company = await CompanyModel.get(company_id)

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не найдена")

        await job.update(update_query)

        return job
    except HTTPException as e:

        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/vacancies")
async def get_all_vacancies(current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        vacancies = await ShipModel.find().to_list()
        return vacancies

    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))


@router.get("/vacancies/{vacancies_id}")
async def get_vacancies_id(vacancies_id: PydanticObjectId, current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        vacancies = await ShipModel.find({"_id": vacancies_id}).to_list()

        company = await CompanyModel.find_one({'vacancies.id': vacancies_id})

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия по данной компании не доступна")

        data = {
            "company_name": company.company_name,
        }
        vacancies.append(data)

        return vacancies

    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))


