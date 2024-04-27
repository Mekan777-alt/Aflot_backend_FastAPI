from beanie import Document, PydanticObjectId
from pydantic import Field
from models.db import db
from typing import Optional, List
from datetime import date
from pydantic import EmailStr


class ship(Document):
    __database__ = db


    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    position: str
    salary: str
    date_of_departure: Optional[date] = None
    contract_duration: str
    ship_name: str
    imo: Optional[str] = None
    ship_type: str
    year_built: int
    contact_person: str
    status: str
    email: Optional[EmailStr] = None
    dwt: int
    kw: int
    length: int
    width: int
    phone1: str
    phone2: Optional[str] = None
    responses: Optional[List[PydanticObjectId]] = None
    job_offers: Optional[List[PydanticObjectId]] = None
