from fastapi import APIRouter
from schemas.auth.auth import UserCreate, UserRead
from api.auth.user_manager import user_auth_backend, fastapi_users

auth_router = APIRouter(
    prefix="/api/v1"
)

auth_router.include_router(
    fastapi_users.get_auth_router(user_auth_backend)
)
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/user",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)


