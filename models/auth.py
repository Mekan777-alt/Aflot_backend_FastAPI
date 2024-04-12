from datetime import datetime
from beanie import Document
from beanie import Indexed
from beanie import PydanticObjectId
from pydantic import EmailStr, Field
from typing import Optional


class auth(Document):

    __collection__ = 'auth'

    id: PydanticObjectId = Field(None, alias="_id")
    email: Indexed(EmailStr, unique=True)
    inn: Optional[int] = None
    phone_number: Indexed(str, unique=True)
    hashed_password: str
    role: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    last_login: datetime
    salt: str
