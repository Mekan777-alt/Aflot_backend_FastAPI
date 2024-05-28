from pydantic import BaseModel
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
    photo_path: str
