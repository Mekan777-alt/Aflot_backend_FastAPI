import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from models.db import db
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
EXPIRATION_TIME = timedelta(minutes=30)


def create_jwt_token(data: dict):
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({"iat": datetime.utcnow(), "exp": expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_jwt_token(token: str):
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.PyJWTError:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    collection = db['User']
    user = await collection.find_one({"$or": [{"email": decoded_data["sub"]},
                                              {"phone_number": decoded_data["sub"]}, {"inn": decoded_data["sub"]}]})
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user
