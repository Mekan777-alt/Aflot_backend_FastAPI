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


class Favorites(BaseModel):
    id: PydanticObjectId


class user_model(Document):
    __database__ = db
    __collection__ = "User"

    id: PydanticObjectId = Field(None, alias="_id")
    email: Indexed(EmailStr, unique=True)
    phone_number: Indexed(str, unique=True)
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
    status: Optional[str]
    date_joined: datetime.datetime


class company_model(Document):
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
    favorites: Optional[List[Favorites]] = None
    black_list: Optional[List[BlackList]] = None
    vacancies: Optional[List[Vacancies]] = None
    date_joined: datetime.datetime
    notification_settings: NotificationSettings = NotificationSettings()
