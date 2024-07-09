from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from beanie import PydanticObjectId


class SalarySchema(BaseModel):
    salaryFrom: str
    salaryTo: str


class VacanciesCompany(BaseModel):
    id: PydanticObjectId
    position: str
    salary: Optional[SalarySchema]
    ship_name: str
    date_of_departure: Optional[date] = None
    contract_duration: str


class VacanciesResponse(BaseModel):
    current_page: int
    total_pages: int
    vacancies: List[VacanciesCompany]
