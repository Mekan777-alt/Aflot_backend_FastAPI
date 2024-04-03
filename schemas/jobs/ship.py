from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Ship(BaseModel):
    position: str
    salary: str
    date_of_departure: Optional[datetime]
    contract_duration: str
    ship_name: str
    imo: Optional[str]
    ship_type: str
    year_built: int
    contact_person: str
    email: Optional[EmailStr]
    dwt: int
    kw: int
    length: int
    width: int
    phone1: str
    phone2: Optional[str]
