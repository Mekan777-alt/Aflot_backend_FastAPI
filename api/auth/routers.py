from fastapi import APIRouter
from .auth import router


auth_router = APIRouter(
    tags=["Authentication"]
)

auth_router.include_router(router)
