from fastapi import APIRouter
from schemas.auth.auth import UserCreate, UserRead, UserUpdate, CompanyRead, CompanyCreate
from api.auth.user_manager import auth_backend, fastapi_users
from api.auth.company_manager import fastapi_company

auth_router = APIRouter(
    prefix="/api/v1"
)

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt/user", tags=["auth"]
)
auth_router.include_router(
    fastapi_company.get_auth_router(auth_backend), prefix="/auth/jwt/company", tags=["auth"]
)
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/user",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_company.get_register_router(CompanyRead, CompanyCreate),
    prefix="/auth/company",
    tags=["auth"]
)
auth_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
