from fastapi import APIRouter

download_router = APIRouter(
    prefix="api/v1",
    tags=['Загрузка фото и логотипа']
)

