from fastapi import APIRouter
from .resumes import router

vacancy_user_router = APIRouter()


vacancy_user_router.include_router(router)

