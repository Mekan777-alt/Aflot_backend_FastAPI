from beanie import Document
from schemas.auth.auth import Optional, Worked, Position
from models.db import db
from pydantic import BaseModel, EmailStr, Field
from typing import List
from beanie import PydanticObjectId


class Vacancies(BaseModel):
    id: PydanticObjectId


class User(Document):
    __database__ = db
    __collection__ = "users"

    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    email: EmailStr
    password: str
    phone_number: str
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
    vacancies: Optional[List[Vacancies]] = None
    salt: Optional[str] = None
