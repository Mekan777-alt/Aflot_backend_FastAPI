from .vacancies import router as create_router
from fastapi import APIRouter

vacancy_company_router = APIRouter()

vacancy_company_router.include_router(create_router)
