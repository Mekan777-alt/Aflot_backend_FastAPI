import math
from fastapi import APIRouter, Depends, HTTPException
from models.register import company_model, Vacancies
from beanie import PydanticObjectId
from models.jobs import ship as ShipModel
from starlette import status
from api.auth.config import get_current_user
from schemas.vacancies_company.ship import Ship, ShipRead
from typing import Annotated

router = APIRouter()


@router.post("/{company_id}/create_vacancies", response_model=ShipRead, status_code=status.HTTP_201_CREATED)
async def create_vacancies_by_company(jobs_create: Ship, company_id: PydanticObjectId,
                                      current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        company_check = await company_model.get(company_id)

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


@router.get("/{company_id}/vacancies", status_code=status.HTTP_200_OK)
async def get_company_vacancies(company_id: PydanticObjectId, current_user: Annotated[dict, Depends(get_current_user)]):
    try:
        company_data = await company_model.get(company_id)
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

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get("/{company_id}/vacancies/{vacancy_id}", status_code=status.HTTP_200_OK)
async def get_vacancies_by_company(company_id: PydanticObjectId, vacancy_id: PydanticObjectId,
                                   current_user: Annotated[dict, Depends(get_current_user)]):

    try:

        company = await company_model.get(company_id)

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не найдена")

        vacancy = await ShipModel.get(vacancy_id)

        if not vacancy:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная вакансия не найдена")

        return vacancy

    except HTTPException as e:

        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.put("/{company_id}/vacancies/{vacancy_id}", response_model=ShipRead, status_code=status.HTTP_201_CREATED)
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

        company = await company_model.get(company_id)

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не найдена")

        await job.update(update_query)

        return job
    except HTTPException as e:

        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/vacancies")
async def get_all_vacancies(page: int = 1,
                            page_size: int = 4):
    try:

        skip = (page - 1) * page_size
        limit = page_size

        total_vacancies = await ShipModel.find().count()
        total_page = math.ceil(total_vacancies / page_size)


        vacancies = await ShipModel.find().skip(skip).limit(limit).to_list()

        return vacancies

    except HTTPException as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get("/vacancies/{vacancies_id}")
async def get_vacancies_id(vacancies_id: PydanticObjectId, current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        vacancies = await ShipModel.find({"_id": vacancies_id}).to_list()

        company = await company_model.find_one({'vacancies.id': vacancies_id})

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия по данной компании не доступна")

        data = {
            "company_name": company.company_name,
        }
        vacancies.append(data)

        return vacancies

    except HTTPException as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.post("/vacancies/{vacancies_id}")
async def send_msg_to_company(vacancies_id: PydanticObjectId):
    try:
        pass

    except HTTPException as e:

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
