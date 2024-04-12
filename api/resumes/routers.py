from fastapi import APIRouter
from .resumes import router

resumes_router = APIRouter(
    tags=["Resumes"],
)


resumes_router.include_router(router)

