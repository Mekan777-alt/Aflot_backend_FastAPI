from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from config import db
from schemas.auth.register import RegisterUser
from starlette.responses import JSONResponse
from api.auth.config import create_jwt_token
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=RegisterUser)
async def register_user(register_data: RegisterUser):
    try:
        collection = db["auth"]
        if collection.find_one({"email": register_data.email}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        else:
            hashed_password = pwd_context.hash(register_data.password)
            register_data.password = hashed_password
            result = collection.insert_one(register_data.dict())
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={"_id": str(result.inserted_id)})
    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))


@router.post("/token")
def auth_user(username: str, password: str):
    is_password_valid = pwd_context.verify(password, password)

    jwt_token = create_jwt_token({"sub": username})

    return {"access_token": jwt_token, "token_type": "bearer"}

