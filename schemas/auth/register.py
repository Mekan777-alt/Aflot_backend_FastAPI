from pydantic import BaseModel
from typing import List


class Position(BaseModel):
    position_name: str


class Worked(BaseModel):
    worked: str


class RegisterUser(BaseModel):
    email: str
    phone_number: str
    first_name: str
    last_name: str
    patronymic: str
    country: str
    region: str
    city: str
    positions: List[Position]
    worked: List[Worked]
    password: str
    confirm_password: str
