from fastapi import APIRouter, Depends, HTTPException
from models import company_model, auth, user_model
from beanie import PydanticObjectId
from models.jobs import ship as ShipModel
from starlette import status
from api.auth.config import get_current_user
from schemas.vacancies_company.ship import Ship, ShipRead
from schemas.vacancies_company.vacancies_list import VacanciesResponse, ResponseCount, Vacancies
from typing import Annotated, Optional
from schemas.vacancies_company.user_resume import Resume
from typing import List

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

        if not company.vacancies:
            company.vacancies = []

        company.vacancies.append(new_vacancy.id)
        await company.save()

        return new_vacancy
    except HTTPException as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/vacancies", status_code=status.HTTP_200_OK, response_model=List[VacanciesResponse])
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
            vacancies_data = await ShipModel.get(vacancy)
            if vacancies_data.status == 'активная вакансия':
                response = VacanciesResponse(
                    vacancies=Vacancies(**dict(vacancies_data)),
                    responseCount=ResponseCount(responseCount=len(vacancies_data.responses)),
                )
                vacancies_info.append(response)
            else:
                pass

        return vacancies_info
    except HTTPException as e:

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get('/vacancies/{vacancy_id}/response', status_code=status.HTTP_200_OK, response_model=List[Resume])
async def response_vacancy_id(vacancy_id: PydanticObjectId,
                              current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        company_id = current_user.get("id")
        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не зарегистрирована")

        vacancy = await ShipModel.get(vacancy_id)

        if not vacancy:
            raise HTTPException(detail='Vacancy not found', status_code=status.HTTP_404_NOT_FOUND)

        responses = vacancy.responses

        resume_list = []
        for response in responses:
            resume = await user_model.get(response)

            resume_list.append(resume)

        return resume_list
    except HTTPException as e:

        return e


@router.get('/vacancies/{vacancy_id}/job-offers', status_code=status.HTTP_200_OK)
async def job_offers_vacancy_id(vacancy_id: PydanticObjectId,
                                current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        company_id = current_user.get("id")
        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не зарегистрирована")

        company = await company_model.get(company_info.resumeID)

        job_offers = company.job_offers

        job_offers_info = []

        for job_offer in job_offers:
            job_offers_data = await user_model.get(job_offer)
            job_offers_data.append(job_offer)

        return job_offers_info
    except HTTPException as e:

        return HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/vacancies/{vacancy_id}/ready-to-work', status_code=status.HTTP_200_OK)
async def response_vacancy_id(vacancy_id: PydanticObjectId,
                              current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        company_id = current_user.get("id")
        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не зарегистрирована")

        company = await company_model.get(company_info.resumeID)

    except HTTPException as e:

        return HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/drafts', status_code=status.HTTP_200_OK)
async def get_drafts_vacancy(current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        pass


    except HTTPException as e:

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get('/irrelevant-vacancies', status_code=status.HTTP_200_OK)
async def get_irrelevant_vacancy(current_user: Annotated[dict, Depends(get_current_user)]):
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

            if vacancies_data.status == 'Неактуальная вакансия':
                vacancies_info.append(vacancies_data)

        return vacancies_info
    except HTTPException as e:

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.put('/irrelevant-vacancies/{vacancy_id}/active', status_code=status.HTTP_201_CREATED)
async def active_irrelevant_vacancy(current_user: Annotated[dict, Depends(get_current_user)],
                                    vacancy_id: PydanticObjectId):
    try:

        company_id = current_user.get("id")
        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не зарегистрирована")

        vacancy = await ShipModel.get(vacancy_id)

        await vacancy.update({"$set": {"status": "активная вакансия"}})

        return vacancy
    except HTTPException as e:

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.delete('/irrelevant-vacancies/{vacancy_id}/delete', status_code=status.HTTP_200_OK)
async def delete_irrelevant_vacancy(current_user: Annotated[dict, Depends(get_current_user)],
                                    vacancy_id: PydanticObjectId):
    try:
        company_id = current_user.get("id")
        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не зарегистрирована")

        company = await company_model.get(company_info.resumeID)

        await company_model.update(company, {"$pull": {"vacancies": {"id": vacancy_id}}})

        vacancy = await ShipModel.get(vacancy_id)
        await vacancy.delete()

        return vacancy

    except HTTPException as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.put('/vacancies/{vacancy_id}/close', status_code=status.HTTP_201_CREATED)
async def close_vacancy(current_user: Annotated[dict, Depends(get_current_user)], vacancy_id: PydanticObjectId):
    try:
        company_id = current_user.get("id")
        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная компания не зарегистрирована")

        vacancy = await ShipModel.get(vacancy_id)

        await vacancy.update({"$set": {"status": "Неактуальная вакансия"}})

        return vacancy

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
