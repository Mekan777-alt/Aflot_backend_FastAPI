from fastapi import APIRouter
from .register import router


auth_router = APIRouter(
    tags=["Authentication"]
)

auth_router.include_router(router)
