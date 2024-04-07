import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import secrets
from models.db import db
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from passlib.hash import pbkdf2_sha256

load_dotenv()

SECRET_KEY = secrets.token_hex(64)
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "plaintext"],
    deprecated="auto",
)
EXPIRATION_TIME = timedelta(minutes=30)


def generate_salt():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    ).public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def hash_password(password: str, salt: bytes):
    hashed_password = pbkdf2_sha256.hash(password, salt=salt, rounds=100000)
    return hashed_password


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
