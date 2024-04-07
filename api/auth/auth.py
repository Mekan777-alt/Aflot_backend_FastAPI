from abc import ABC, abstractmethod
from typing import Optional
from fastapi import HTTPException, Depends
from models.db import db
from pydantic import BaseModel
from api.auth.config import hash_password, oauth2_scheme, verify_jwt_token, pwd_context
from motor.motor_asyncio import AsyncIOMotorClient


class AuthSchemas(BaseModel):
    email: str
    role: str


class AuthService(ABC):
    @abstractmethod
    async def authenticate(self, email: str, password: str) -> Optional[AuthSchemas]:
        pass


class UserAuthService(AuthService):

    def __init__(self):
        self.user_collection = db['UserModel']

    async def authenticate(self, email: str, password: str) -> Optional[AuthSchemas]:
        user = await self.user_collection.find_one({"$or": [{"email": email},
                                                            {"phone_number": email}, {"inn": email}]})
        if not user:

            return None

        is_correct_password = pwd_context.verify(password, user['password'])

        if not is_correct_password:

            raise HTTPException(detail="Incorrect password", status_code=401)

        return AuthSchemas(email=user['email'], role=user['role'])

    async def find_user(self, email: str) -> Optional[AuthSchemas]:
        user = await self.user_collection.find_one({"$or": [{"email": email},
                                                            {"phone_number": email}, {"inn": email}]})
        if not user:
            return None
        return AuthSchemas(email=user['email'], role=user['role'])


class CompanyAuthService(AuthService):

    def __init__(self):
        self.company_collection = db['CompanyModel']

    async def authenticate(self, email: str, password: str) -> Optional[AuthSchemas]:
        company = await self.company_collection.find_one({"$or": [{"email": email},
                                                                  {"phone_number": email}, {"inn": email}]})

        if not company:

            return None

        is_correct_password = pwd_context.verify(password, company['password'])

        if not is_correct_password:

            raise HTTPException(detail="Invalid password", status_code=401)

        return AuthSchemas(email=company['email'], role=company['role'])

    async def find_company(self, email: str) -> Optional[AuthSchemas]:
        company = await self.company_collection.find_one({"$or": [{"email": email},
                                                                  {"phone_number": email}, {"inn": email}]})
        if not company:
            return None

        return AuthSchemas(email=company['email'], role=company['role'])


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_service = UserAuthService()
    company_service = CompanyAuthService()

    decoded_data = verify_jwt_token(token)

    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = await user_service.find_user(decoded_data['sub'])
    company = await company_service.find_company(decoded_data['sub'])

    if user:
        return user

    if company:
        return company
