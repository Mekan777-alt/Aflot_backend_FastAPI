from typing import Optional, List
from pydantic import BaseModel, EmailStr
from beanie import PydanticObjectId
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm


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
    patronymic: Optional[str] = None
    role: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    telegram: Optional[str] = None
    positions: Optional[List[Position]] = None
    worked: Optional[List[Worked]] = None
    salt: Optional[str] = None


class UserRead(BaseModel):
    id: PydanticObjectId
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    role: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    telegram: Optional[str] = None
    positions: Optional[List[Position]] = None
    worked: Optional[List[Worked]] = None


class UserAuthenticate(OAuth2PasswordRequestForm):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str


class CompanyCreate(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    role: Optional[str] = None
    phone_number: str
    company_name: str
    company_inn: int
    company_address: str
    telegram: Optional[str] = None
    salt: Optional[str] = None


class CompanyRead(BaseModel):
    id: PydanticObjectId
    email: EmailStr
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    role: Optional[str] = None
    phone_number: str
    company_name: str
    company_inn: int
    company_address: str
    telegram: Optional[str] = None