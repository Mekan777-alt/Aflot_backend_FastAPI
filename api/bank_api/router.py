from fastapi import APIRouter
from .pay import router

bank_router = APIRouter(
    tags=['Bank API'],
    prefix='/api/v1',
)


bank_router.include_router(router)
