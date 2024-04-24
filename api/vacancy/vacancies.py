import math
from fastapi import APIRouter, Depends, HTTPException
from models.register import Vacancies
from models import company_model, auth
from beanie import PydanticObjectId
from models.jobs import ship as ShipModel
from starlette import status
from api.auth.config import get_current_user
from schemas.vacancies_company.ship import Ship, ShipRead
from typing import Annotated, Optional

router = APIRouter()


@router.post("/create_vacancies", response_model=ShipRead, status_code=status.HTTP_201_CREATED)
async def create_vacancies_by_company(jobs_create: Ship,
                                      current_user: Annotated[dict, Depends(get_current_user)]):
    try:
        company_id = current_user.get("id")
        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не зарегистрирована")

        company = await company_model.get(company_info.resumeID)
        jobs_create.status = 'активная вакансия'
        new_vacancy = ShipModel(**jobs_create.dict())

        await new_vacancy.create()

        vacancy = Vacancies(id=new_vacancy.id)

        if not company.vacancies:
            company.vacancies = []

        company.vacancies.append(vacancy)
        await company.save()

        return new_vacancy
    except HTTPException as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/vacancies", status_code=status.HTTP_200_OK)
async def get_company_vacancies(current_user: Annotated[dict, Depends(get_current_user)]):
    try:
        company_id = current_user.get("id")
        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не зарегистрирована")

        company = await company_model.get(company_info.resumeID)
        vacancies = company.vacancies

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


@router.get("/vacancies/{vacancy_id}", status_code=status.HTTP_200_OK)
async def get_vacancies_by_company(current_user: Annotated[dict, Depends(get_current_user)],
                                   vacancy_id: PydanticObjectId):

    try:

        company_id = current_user.get("id")
        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не зарегистрирована")

        vacancy = await ShipModel.get(vacancy_id)

        if not vacancy:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная вакансия не найдена")

        return vacancy

    except HTTPException as e:

        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.put("/vacancies/{vacancy_id}", response_model=ShipRead, status_code=status.HTTP_201_CREATED)
async def update_vacancies_by_company(request: Ship, vacancy_id: PydanticObjectId,
                                      current_user: Optional[dict] = Depends(get_current_user)):
    try:

        company_id = current_user.get("id")
        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не зарегистрирована")

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


@router.get("/all-vacancies")
async def get_all_vacancies(page: int = 1, page_size: int = 4):
    try:

        skip = (page - 1) * page_size
        limit = page_size

        total_vacancies = await ShipModel.find().count()
        total_page = math.ceil(total_vacancies / page_size)


        vacancies = await ShipModel.find().skip(skip).limit(limit).to_list()

        return vacancies

    except HTTPException as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get("/all-vacancies/{vacancies_id}")
async def get_vacancies_id(vacancies_id: PydanticObjectId):
    try:

        data = []

        vacancies = await ShipModel.find_one({"_id": vacancies_id})

        if not vacancies:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная вакансия не найдена")

        data.append(vacancies)
        company = await company_model.find_one({'vacancies.id': vacancies_id})

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия по данной компании не доступна")

        company_info = {
            "id": str(PydanticObjectId(company.id)),
            "company_name": company.company_name,

        }
        data.append(company_info)

        return data

    except HTTPException as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.post("/all-vacancies/{vacancies_id}/add_favorite")
async def add_vacancy_to_favorite(vacancies_id: PydanticObjectId):
    try:
        pass

    except HTTPException as e:

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.post("/all-vacancies/{vacancies_id}/add_favorite/company/{company_id}")
async def add_company_to_favorite(vacancies_id: PydanticObjectId, company_id: PydanticObjectId):
    try:
        pass

    except HTTPException as e:

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.post("/all-vacancies/{vacancies_id}/add_blacklist", status_code=status.HTTP_201_CREATED)
async def add_blacklist(vacancies_id: PydanticObjectId):
    try:
        pass

    except HTTPException as e:

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)

