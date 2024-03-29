from fastapi import FastAPI
from api.auth.routers import auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(auth_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

