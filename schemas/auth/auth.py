from beanie import PydanticObjectId
from fastapi_users import schemas
from typing import Optional, List


class Position(schemas.BaseModel):
    position_name: str


class Worked(schemas.BaseModel):
    worked: str


class UserRead(schemas.BaseUser[PydanticObjectId]):
    pass


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    patronymic: str
    country: str
    region: str
    city: str
    telegram: Optional[str] = None
    positions: List[Position]
    worked: List[Worked]


class UserUpdate(schemas.BaseUserUpdate):
    pass


class CompanyRead(schemas.BaseUser[PydanticObjectId]):
    pass


class CompanyCreate(schemas.BaseUserCreate):
    company_name: str
    company_inn: str
    company_address: str
    phone_number: str
    last_name: str
    first_name: str
    patronymic: str
