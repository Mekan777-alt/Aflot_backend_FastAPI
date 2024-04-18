from .vacancies import router as create_router
from fastapi import APIRouter

vacancy_company_router = APIRouter(
    prefix="/api/v1",
    tags=["Вакансии компаний"]
)

vacancy_company_router.include_router(create_router)
