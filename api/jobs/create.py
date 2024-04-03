from fastapi import APIRouter, Depends
from models.register import User
from schemas.jobs.ship import Ship
from api.auth.user_manager import current_active_user

router = APIRouter(
    prefix="/api/v1"
)


@router.get("/create_jobs")
async def create_job(company: User = Depends(current_active_user)):
    return f"Hello {company}"
