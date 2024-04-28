from fastapi import APIRouter, HTTPException, Depends
import math
from starlette import status
from beanie import PydanticObjectId
from models import company_model, auth, user_model
from models.register import FavoritesVacancies, FavoritesCompany
from models import ship as ShipModel
from typing import Annotated
from api.auth.config import get_current_user
from starlette.responses import JSONResponse

router = APIRouter()


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


@router.get("/all-vacancies/{vacancies_id}", status_code=status.HTTP_200_OK)
async def get_vacancies_id(vacancies_id: PydanticObjectId):
    try:

        data = []

        vacancies = await ShipModel.find_one({"_id": vacancies_id})

        if not vacancies:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данная вакансия не найдена")

        data.append(vacancies)
        company = await company_model.find_one({'vacancies': vacancies_id})

        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия по данной компании не доступна")

        company_info = {
            "id": str(PydanticObjectId(company.id)),
            "company_name": company.company_name,

        }
        data.append(company_info)

        return data

    except HTTPException as e:
        return e


@router.post('/all-vacancies/{vacancies_id}/respond')
async def respond_vacancy(vacancies_id: PydanticObjectId, current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        user_id = current_user.get("id")

        user_info = await auth.get(user_id)

        if not user_info:

            raise HTTPException(detail="User not found", status_code=status.HTTP_401_UNAUTHORIZED)

        resume_id = user_info.resumeID

        vacancy_info = await ShipModel.get(vacancies_id)

        if not vacancy_info:

            raise HTTPException(detail="Vacancy not found", status_code=status.HTTP_404_NOT_FOUND)

        if not vacancy_info.responses:
            vacancy_info.responses = []

        vacancy_info.responses.append(resume_id)

        await vacancy_info.save()

        return JSONResponse(content="Отклик на вакансию отправлен", status_code=status.HTTP_200_OK)

    except HTTPException as e:

        return e


@router.post("/all-vacancies/{vacancies_id}/add_favorite")
async def add_vacancy_to_favorite(vacancies_id: PydanticObjectId,
                                  current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        user_id = current_user.get('id')

        if not user_id:

            raise HTTPException(detail='User not found', status_code=status.HTTP_404_NOT_FOUND)

        resume_id = await auth.get(user_id)

        if not resume_id:
            raise HTTPException(detail='Resume not found', status_code=status.HTTP_404_NOT_FOUND)

        resume = await user_model.get(resume_id.resumeID)

        new_favorite = FavoritesVacancies(id=vacancies_id)

        if not resume.favorites_vacancies:
            resume.favorites_vacancies = []

        resume.favorites_vacancies.append(new_favorite)

        await resume.save()

        return {"message": f"{vacancies_id} - added to favorites"}

    except HTTPException as e:

        return e


@router.post("/all-vacancies/{vacancies_id}/add_favorite/company/{company_id}")
async def add_company_to_favorite(vacancies_id: PydanticObjectId, company_id: PydanticObjectId,
                                  current_user: Annotated[dict, Depends(get_current_user)]):
    try:
        user_id = current_user.get('id')

        if not user_id:

            raise HTTPException(detail='User not found', status_code=status.HTTP_404_NOT_FOUND)

        user = await auth.get(user_id)

        resume = await user_model.get(user.resumeID)

        new_favorite_company = FavoritesCompany(id=company_id)

        if not resume.favorites_company:
            resume.favorites_company = []

        for i in resume.favorites_company:

            if i.id == company_id:

                return HTTPException(detail="Данная компания уже у вас в избранных", status_code=status.HTTP_200_OK)

        resume.favorites_company.append(new_favorite_company)

        await resume.save()


        return {"message": f"{company_id} - added to favorites"}

    except HTTPException as e:

        return e


@router.get("/all-vacancies/{vacancies_id}/all-vacancies-company/{company_id}", status_code=status.HTTP_200_OK)
async def get_all_vacancies_company(vacancies_id: PydanticObjectId, company_id: PydanticObjectId):
    try:

        company = await company_model.get(company_id)

        if not company:

            raise HTTPException(detail='Company not found', status_code=status.HTTP_404_NOT_FOUND)

        company_all_vacancy = company.vacancies if company.vacancies else []

        if not company_all_vacancy:

            return company_all_vacancy

        data = []
        for vacancy in company_all_vacancy:

            job = await ShipModel.get(vacancy)

            data.append(job)

        return data

    except HTTPException as e:
        return e

