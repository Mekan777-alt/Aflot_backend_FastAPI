from fastapi import APIRouter
from .auth.routers import auth_router
from .news.routers import news_router
from .resumes.routers import resumes_router
from .company.routers import company_router
from .vacancy.routers import vacancy_company_router
from .company_profile.routers import profile_router
from .tariffs.routers import tariffs_router
from .favorites.routers import favorite_router
from .contacts.routers import contacts_router
from .sailor_profile.routers import sailor_profile_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(news_router)
api_router.include_router(resumes_router)
api_router.include_router(company_router)
api_router.include_router(vacancy_company_router)
api_router.include_router(profile_router)
api_router.include_router(tariffs_router)
api_router.include_router(favorite_router)
api_router.include_router(contacts_router)
api_router.include_router(sailor_profile_router)
