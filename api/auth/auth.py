from abc import ABC, abstractmethod
from typing import Optional
from fastapi import HTTPException, Depends
from models.db import db
from pydantic import BaseModel
from api.auth.config import oauth2_scheme, verify_jwt_token, pwd_context
from datetime import datetime


class AuthSchemas(BaseModel):
    email: str
    role: str


class AuthService(ABC):
    @abstractmethod
    async def authenticate(self, email: str, password: str) -> Optional[AuthSchemas]:
        pass


class UserAuthService(AuthService):

    def __init__(self):
        self.auth_collection = db['Auth']

    async def authenticate(self, email: str, password: str) -> Optional[AuthSchemas]:
        user = await self.auth_collection.find_one({"$or": [{"email": email},
                                                            {"phone_number": email}, {"inn": email}]})
        if not user:
            return None

        is_correct_password = pwd_context.verify(password, user['hashed_password'])

        if not is_correct_password:
            raise HTTPException(detail="Incorrect password", status_code=401)

        await self.auth_collection.update_one({"_id": user['_id']}, {"$set": {"last_login": datetime.now()}})

        return AuthSchemas(email=user['email'], role=user['role'])

    async def find_user(self, email: str) -> Optional[AuthSchemas]:
        user = await self.auth_collection.find_one({"$or": [{"email": email},
                                                            {"phone_number": email}, {"inn": email}]})
        if not user:
            return None
        return AuthSchemas(email=user['email'], role=user['role'])


class CompanyAuthService(AuthService):

    def __init__(self):
        self.auth_collection = db['Auth']

    async def authenticate(self, email: str, password: str) -> Optional[AuthSchemas]:
        company = await self.auth_collection.find_one({"$or": [{"email": email},
                                                               {"phone_number": email}, {"inn": email}]})

        if not company:
            return None

        is_correct_password = pwd_context.verify(password, company['hashed_password'])

        if not is_correct_password:
            raise HTTPException(detail="Invalid password", status_code=401)

        await self.auth_collection.update_one({"_id": company['_id']}, {"$set": {"last_login": datetime.now()}})

        return AuthSchemas(email=company['email'], role=company['role'])

    async def find_company(self, email: str) -> Optional[AuthSchemas]:
        company = await self.auth_collection.find_one({"$or": [{"email": email},
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
