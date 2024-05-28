from pydantic import BaseModel
from typing import Optional
from beanie import PydanticObjectId


class Resume(BaseModel):
    id: PydanticObjectId
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    photo_path: Optional[str] = None
