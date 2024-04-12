from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from beanie import init_beanie
from models import db, user_model, company_model, auth, ship, news_model
from api.api_routers import api_router
from admin.app import admin, app as admin_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(
        database=db,
        document_models=[
            user_model,
            ship,
            company_model,
            auth,
            news_model,
        ],
    )
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(api_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
