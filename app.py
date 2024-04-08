from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from beanie import init_beanie
from models import db, UserModel, CompanyModel, Auth, Ship
from api.auth.routers import auth_router
from api.vacancy_company.routers import vacancy_company_router
from api.profile.routers import profile
from api.resumes.routers import vacancy_user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(
        database=db,
        document_models=[
            UserModel,
            Ship,
            CompanyModel,
            Auth
        ],
    )
    yield
app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(vacancy_company_router)
app.include_router(profile)
app.include_router(vacancy_user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

