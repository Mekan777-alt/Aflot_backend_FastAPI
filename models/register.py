import motor.motor_asyncio
from beanie import Document
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from schemas.auth.auth import Optional, List, Worked, Position

DATABASE_URL = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)

db = client['aflot_backend']


class User(BeanieBaseUser, Document):
    first_name: str
    last_name: str
    patronymic: str
    country: str
    region: str
    city: str
    telegram: Optional[str] = None
    positions: List[Position]
    worked: List[Worked]


class Company(BeanieBaseUser, Document):
    company_name: str
    company_inn: str
    company_address: str
    phone_number: str
    last_name: str
    first_name: str
    patronymic: str


async def get_user_db():
    yield BeanieUserDatabase(User)


async def get_company_db():
    yield BeanieUserDatabase(Company)
