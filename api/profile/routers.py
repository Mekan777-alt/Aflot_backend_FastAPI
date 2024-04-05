from .company_profile import router as profile_router
from fastapi import APIRouter

profile = APIRouter()

profile.include_router(profile_router)
