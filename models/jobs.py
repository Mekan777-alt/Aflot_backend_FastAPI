from beanie import Document
from models.db import db
from typing import Optional
from datetime import datetime


class Ship(Document):
    __database__ = db
    __collection__ = "Jobs"

    position: str
    salary: str
    date_of_departure: Optional[datetime]
    contract_duration: str
    ship_name: str
    imo: Optional[str]
    ship_type: str
    year_built: int
    contact_person: str
    email: str
    dwt: int
    kw: int
    length: int
    width: int
    phone1: str
    phone2: Optional[str]
