from fastapi import APIRouter
from .get_tariffs import router


tariffs_router = APIRouter(
    tags=['Tariffs'],
)

tariffs_router.include_router(router)
