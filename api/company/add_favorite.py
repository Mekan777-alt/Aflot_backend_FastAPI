from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import JSONResponse
from models import company_model

router = APIRouter()


@router.get('/favorite_sailor')
async def get_favorite_sailor():
    pass