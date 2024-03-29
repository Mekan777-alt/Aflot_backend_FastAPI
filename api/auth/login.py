from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from config import db
from typing import Annotated
from schemas.auth.login import Login
from starlette.responses import JSONResponse
from api.auth.register import pwd_context
from api.auth.config import create_jwt_token, get_current_user

router = APIRouter()


@router.post("/token")
def auth_user(login_data: Login):
    try:
        collection = db['auth']
        user = collection.find_one({"email": login_data.email})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Неверный адрес электронной почты или "
                                                                              "пароль")

        is_password_correct = pwd_context.verify(login_data.password, user.get("password"))
        if not is_password_correct:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный адрес электронной почты или "
                                                                                "пароль")

        jwt_token = create_jwt_token({"sub": user.get("email")})
        return JSONResponse(status_code=status.HTTP_200_OK, content={"token": jwt_token})
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/user/me")
def auth_user_me(user: Annotated[dict, Depends(get_current_user)]):
    return user
