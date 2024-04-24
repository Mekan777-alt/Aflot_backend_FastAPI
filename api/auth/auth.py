from abc import ABC, abstractmethod
from fastapi import HTTPException, Depends
from models.db import db
from pydantic import BaseModel
from datetime import datetime
from beanie import PydanticObjectId
from passlib.context import CryptContext



pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "plaintext"],
    deprecated="auto",
)


class AuthSchemas(BaseModel):
    id: PydanticObjectId
    email: str
    phone_number: str
    role: str
    sub: str

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role,
            "sub": self.sub,
        }


class AuthServiceABC(ABC):
    @abstractmethod
    async def authenticate(self, email: str, password: str):
        pass


class AuthServices(AuthServiceABC):

    def __init__(self):
        self.auth_collection = db['auth']

    async def authenticate(self, username: str, password: str):
        user = await self.auth_collection.find_one({"$or": [{"email": username},
                                                            {"phone_number": username}, {"inn": username}]})
        if not user:

            return None

        is_correct_password = pwd_context.verify(password, user['hashed_password'])

        if not is_correct_password:
            raise HTTPException(detail="Incorrect password", status_code=401)

        await self.auth_collection.update_one({"_id": user['_id']}, {"$set": {"last_login": datetime.now()}})

        return (AuthSchemas(id=user['_id'], email=user['email'], role=user['role'], phone_number=user['phone_number'],
                            sub=username).to_dict())

    async def find_user(self, username: str):
        user = await self.auth_collection.find_one({"$or": [{"email": username},
                                                            {"phone_number": username}, {"inn": username}]})
        if not user:
            return None
        return (AuthSchemas(id=user['_id'], email=user['email'], role=user['role'], phone_number=user['phone_number'],
                            sub=username).to_dict())

    async def check_user(self, username: str):
        user = await self.auth_collection.find_one({"$or": [{"email": username},
                                                            {"phone_number": username}, {"inn": username}]})
        if not user:

            return False

        return True
