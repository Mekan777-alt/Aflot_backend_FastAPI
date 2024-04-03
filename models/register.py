from beanie import Document
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from schemas.auth.auth import Optional, List, Worked, Position
from models.db import db


class User(BeanieBaseUser, Document):
    __database__ = db
    __collection__ = "users"

    first_name: str
    last_name: str
    patronymic: str
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    telegram: Optional[str] = None
    positions: Optional[List[Position]] = None
    worked: Optional[List[Worked]] = None
    company_name: Optional[str] = None
    company_inn: Optional[str] = None
    company_address: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        exclude_none = True


async def get_user_db():
    yield BeanieUserDatabase(User)

