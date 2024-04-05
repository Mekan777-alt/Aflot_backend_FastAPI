from beanie import Document, PydanticObjectId
from pydantic import Field
from models.db import db
from typing import Optional
from datetime import datetime
from pydantic import EmailStr


class Ship(Document):
    __database__ = db
    __collection__ = "Jobs"

    id: Optional[PydanticObjectId] = Field(None, alias="_id")
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
