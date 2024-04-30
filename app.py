from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from beanie import init_beanie
from starlette.staticfiles import StaticFiles

from models import (db, user_model, company_model, auth, ship, news_model, contact, feedback, vessel, position,
                    real_history, swims_tariffs, description_tariffs, company_tariffs)
from api.api_routers import api_router


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
            contact,
            feedback,
            position,
            vessel,
            real_history,
            swims_tariffs,
            description_tariffs,
            company_tariffs
        ],
    )
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(api_router)

app.mount('/static', StaticFiles(directory='static'), name='static')
