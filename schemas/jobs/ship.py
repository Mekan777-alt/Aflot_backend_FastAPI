from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from beanie import PydanticObjectId


class ShipRead(BaseModel):
    id: PydanticObjectId
    position: str
    ship_name: str


class Ship(BaseModel):
    position: str
    salary: str
    date_of_departure: Optional[datetime] = None
    contract_duration: str
    ship_name: str
    imo: Optional[str] = None
    ship_type: str
    year_built: int
    contact_person: str
    email: Optional[EmailStr] = None
    dwt: int
    kw: int
    length: int
    width: int
    phone1: str
    phone2: Optional[str] = None
