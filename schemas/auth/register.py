from pydantic import BaseModel, EmailStr
from typing import List
from schemas.auth.validate import check_password_complexity
from fastapi import HTTPException
from starlette import status


class Position(BaseModel):
    position_name: str


class Worked(BaseModel):
    worked: str


class RegisterUser(BaseModel):
    email: EmailStr
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

    def verify_password(self):
        if not check_password_complexity(self.password):
            raise HTTPException(detail='Пароль должен содержать минимум 8 символов, включая хотя бы одну заглавную '
                                       'букву, одну строчную букву, одну цифру и один спецсимвол из!@#$%^&*(),.?":{}|<>',
                                status_code=status.HTTP_400_BAD_REQUEST)


class RegisterCompany(BaseModel):
    company_name: str
    company_inn: str
    company_address: str
    email: EmailStr
    phone_number: str
    last_name: str
    first_name: str
    patronymic: str
    password: str
    confirm_password: str

    def verify_password(self):
        if not check_password_complexity(self.password):
            raise HTTPException(detail='Пароль должен содержать минимум 8 символов, включая хотя бы одну заглавную '
                                       'букву, одну строчную букву, одну цифру и один спецсимвол из!@#$%^&*(),.?":{}|<>',
                                status_code=status.HTTP_400_BAD_REQUEST)
