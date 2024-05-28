from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from beanie import PydanticObjectId


class VacanciesCompany(BaseModel):
    id: PydanticObjectId
    position: str
    salary: str
    ship_name: str
    date_of_departure: Optional[date] = None
    contract_duration: str


class VacanciesResponse(BaseModel):
    current_page: int
    total_pages: int
    vacancies: List[VacanciesCompany]
