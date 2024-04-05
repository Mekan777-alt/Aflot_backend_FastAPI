from typing import Optional, List
from pydantic import BaseModel, EmailStr
from beanie import PydanticObjectId
from fastapi import Form

class Position(BaseModel):
    position_name: str


class Worked(BaseModel):
    worked: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
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


class UserRead(BaseModel):
    id: PydanticObjectId
    email: EmailStr


class UserAuthenticate(BaseModel):
    data: str = Form(...)
    password: str = Form(...)
