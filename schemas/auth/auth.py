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
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    telegram: Optional[str] = None
    positions: Optional[List[Position]] = None
    worked: Optional[List[Worked]] = None
    company_name: Optional[str] = None
    company_inn: Optional[str] = None
    company_address: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        exclude_unset = True


class UserUpdate(schemas.BaseUserUpdate):
    pass



