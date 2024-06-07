from pydantic import BaseModel
from typing import Optional
from datetime import date
from beanie import PydanticObjectId


class Vacancy(BaseModel):
    id: PydanticObjectId
    position: str
    date_of_departure: date
    ship_name: str
    salary: str
    contract_duration: str


class CompanyInfo(BaseModel):
    id: PydanticObjectId
    company_name: str
    photo_path: Optional[str] = None


class ResponseOffers(BaseModel):
    companyInfo: CompanyInfo
    vacancy: Vacancy


class News(BaseModel):
    id: PydanticObjectId
    title: str
    content: str
    created_at: Optional[str]
    photo_path: Optional[str] = None
    view_count: Optional[int] = None


class Resume(BaseModel):
    id: PydanticObjectId
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    photo_path: Optional[str] = None
