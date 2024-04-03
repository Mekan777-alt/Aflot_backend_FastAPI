from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from beanie import init_beanie
from models.register import User
from models.db import db
from api.auth.routers import auth_router
from fastapi_admin.app import app as admin_app
from api.jobs.routers import jobs_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(
        database=db,
        document_models=[
            User,
        ],
    )
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/admin", admin_app)

app.include_router(auth_router)
app.include_router(jobs_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


@app.middleware("http")
async def check_request_type(request: Request, call_next):
    auth_router_mapping = {
        "/auth/jwt/login": "/auth",
        "/auth/user": "/user",
        "/auth/company": "/company",
    }

    for path, prefix in auth_router_mapping.items():
        if request.url.path.startswith(path):
            request.state.auth_router_prefix = prefix
            break

    response = await call_next(request)
    return response
