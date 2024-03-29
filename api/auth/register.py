from fastapi import APIRouter, HTTPException
from starlette import status
from config import db
from schemas.auth.register import RegisterUser
from starlette.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=RegisterUser)
def register_user(register_data: RegisterUser):
    try:
        collection = db["auth"]
        if collection.find_one({"email": register_data.email}):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Данный пользователь уже есть в системе")
        if register_data.password != register_data.confirm_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пароли не совпадают")
        hashed_password = pwd_context.hash(register_data.password)
        register_data.password = hashed_password

        del register_data.confirm_password
        result = collection.insert_one(register_data.dict())
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"_id": str(result.inserted_id)})
    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))
