from fastapi import APIRouter
from .company_info import router as company_info_router
from .add_favorite import router as favorite_router

company_router = APIRouter(
    prefix="/ap1/v1",
    tags=["Navy"],
)

company_router.include_router(company_info_router)
company_router.include_router(favorite_router)
