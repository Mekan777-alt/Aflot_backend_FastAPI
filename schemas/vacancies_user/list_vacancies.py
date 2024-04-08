from pydantic import BaseModel
from typing import List
from schemas.auth.auth import UserRead


class ListVacancies(BaseModel):
    vacancies: List[UserRead]
