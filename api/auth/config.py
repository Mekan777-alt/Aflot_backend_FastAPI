import os
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from starlette import status
from api.auth.register import oauth2_scheme
from config import db
from bson import ObjectId

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
EXPIRE_MINUTES = timedelta(minutes=30)


def create_jwt_token(data: dict):
    expire = datetime.utcnow() + EXPIRE_MINUTES
    data.update({'exp': expire})

    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_jwt_token(token: str):
    try:

        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded

    except jwt.PyJWTError:

        return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    decoded = verify_jwt_token(token)
    if not decoded:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

    collection = db['auth']
    user = collection.find_one({"email": decoded['sub']})

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user['_id'] = str(user['_id'])
    return user
