from fastapi import APIRouter, Depends, HTTPException
from models.register import User, Vacancies
from beanie import PydanticObjectId
from models.jobs import Ship as ShipModel
from starlette import status
from starlette.responses import JSONResponse
from schemas.jobs.ship import Ship, ShipRead

router = APIRouter(
    prefix="/api/v1"
)


@router.post("/{company_id}/create_vacancies", response_model=ShipRead)
async def create_job(jobs_create: ShipModel, company_id: PydanticObjectId):
    try:

        company_check = await User.get(company_id)

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
async def get_company_vacancies(company_id: PydanticObjectId):
    try:
        company_data = await User.get(company_id)
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
