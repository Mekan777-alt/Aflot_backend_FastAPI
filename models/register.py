from beanie import Document
from schemas.auth.auth import Optional, Worked, Position
from models.db import db
from pydantic import BaseModel, EmailStr, Field
from typing import List
from beanie import PydanticObjectId, Indexed


class Vacancies(BaseModel):
    id: PydanticObjectId


class UserModel(Document):
    __database__ = db
    __collection__ = "User"

    id: PydanticObjectId = Field(None, alias="_id")
    email: Indexed(EmailStr, unique=True)
    phone_number: str
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    role: str
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    telegram: Optional[str] = None
    positions: Optional[List[Position]] = None
    worked: Optional[List[Worked]] = None


class CompanyModel(Document):
    __database__ = db
    __collection__ = "Company"

    id: PydanticObjectId = Field(None, alias="_id")
    email: Indexed(EmailStr, unique=True)
    phone_number: Indexed(str, unique=True)
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    role: str
    telegram: Optional[str] = None
    company_name: str
    company_inn: Indexed(int, unique=True)
    company_address: str
    vacancies: Optional[List[Vacancies]] = None