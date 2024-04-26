from pydantic import BaseModel
from datetime import datetime


class CompanyFavoritesSchemas(BaseModel):
    company_name: str
    company_address: str
    date_joined: str
    active_vacancy: int
