from fastapi import APIRouter


router = APIRouter(
    prefix="/api/v1",
)


@router.get("/get_tariffs/company")
async def get_tariffs():
    pass


@router.get("/get_tariffs/swims")
async def get_tariffs():
    pass
