from fastapi import APIRouter
from fastapi import Depends, HTTPException
from models.register import User as UserModel
from models.register import db
from .config import pwd_context, create_jwt_token
from schemas.auth.auth import UserCreate, UserRead, UserAuthenticate
from starlette import status
from fastapi import Form

router = APIRouter(
    prefix="/api/v1"
)


@router.post("/register", response_model=UserRead)
async def register_user(user_data: UserCreate):
    try:
        collection = db['User']
        if await collection.find_one({"email": user_data.email}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

        if user_data.password != user_data.confirm_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The passwords don't match")

        hashed_password = pwd_context.hash(user_data.password)

        user_data.password = hashed_password

        user = UserModel(**user_data.dict())
        await user.create()

        return user
    except HTTPException as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/token")
async def authenticate_user(data: str = Form(...), password: str = Form(...)):
    try:
        collection = db['User']
        user = await collection.find_one({"$or": [{"email": data}, {"phone_number": data}, {"inn": data}]})
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        is_password_correct = pwd_context.verify(password, user['password'])

        if not is_password_correct:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        jwt_token = create_jwt_token({"sub": data})
        return {"access_token": jwt_token, "token_type": "bearer"}
    except HTTPException as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
