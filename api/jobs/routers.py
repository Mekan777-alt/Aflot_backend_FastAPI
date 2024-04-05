from .vacancies import router as create_router
from fastapi import APIRouter

jobs_router = APIRouter()

jobs_router.include_router(create_router)
