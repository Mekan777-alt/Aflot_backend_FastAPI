import datetime
from beanie import Document
from schemas.auth.auth import Optional, Worked, Position
from models.db import db
from pydantic import BaseModel, EmailStr, Field
from typing import List
from beanie import PydanticObjectId, Indexed


class NotificationSettings(BaseModel):
    send_email: bool = False
    send_sms: bool = False
    send_telegram: bool = False
    mailing_notification: bool = False


class Vacancies(BaseModel):
    id: PydanticObjectId


class BlackList(BaseModel):
    id: PydanticObjectId


class FavoritesSailor(BaseModel):
    id: PydanticObjectId


class FavoritesCompany(BaseModel):
    id: PydanticObjectId


class FavoritesVacancies(BaseModel):
    id: PydanticObjectId


class user_model(Document):
    __database__ = db

    id: PydanticObjectId = Field(None, alias="_id")
    email: Indexed(EmailStr, unique=True)
    phone_number: Indexed(str, unique=True)
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    telegram: Optional[str] = None
    positions: Optional[List[Position]] = None
    worked: Optional[List[Worked]] = None
    status: Optional[str] = None
    favorites_company: Optional[List[FavoritesCompany]] = None
    favorites_vacancies: Optional[List[FavoritesVacancies]] = None
    notification_settings: NotificationSettings


class company_model(Document):
    __database__ = db

    id: PydanticObjectId = Field(None, alias="_id")
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    telegram: Optional[str] = None
    company_name: str
    company_inn: Indexed(int, unique=True)
    company_address: str
    favorites_resume: Optional[List[FavoritesSailor]] = None
    black_list_resume: Optional[List[BlackList]] = None
    vacancies: Optional[List[Vacancies]] = None
    notification_settings: NotificationSettings
