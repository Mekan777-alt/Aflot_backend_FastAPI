from pydantic import BaseModel


class AdminAuth(BaseModel):
    username: str
    password: str
