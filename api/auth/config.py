import os
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

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
