from fastapi import APIRouter, HTTPException, Depends
import math
from starlette import status
from beanie import PydanticObjectId
from models import company_model, auth, user_model
from models.register import FavoritesVacancies
from models import ship as ShipModel
from typing import Annotated
from api.auth.config import get_current_user

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


@router.post('/all-vacancies/{vacancies_id}/respond', status_code=status.HTTP_201_CREATED)
async def respond_vacancy(vacancies_id: PydanticObjectId, current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        pass

    except HTTPException as e:

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


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
