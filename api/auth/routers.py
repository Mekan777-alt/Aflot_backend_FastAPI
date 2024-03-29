from fastapi import APIRouter
from api.auth.register import router as register_router

auth_router = APIRouter(
    prefix="/api/v1/auth"
)

auth_router.include_router(register_router)
