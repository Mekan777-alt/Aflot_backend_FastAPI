from datetime import datetime
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from models.register import user_model, company_model
from models.auth import auth as auth_model
from .config import (generate_jwt_token, generate_salt, hash_password, oauth2_scheme,
                     verify_jwt_token, convert_objectid_to_str)
from schemas.auth.auth import UserCreate, UserRead, CompanyRead, CompanyCreate
from starlette import status
from api.auth.auth import AuthServices, AuthSchemas
from schemas.auth.auth import Token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/register/user", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    try:

        if await user_model.find_one({"email": user_data.email}):

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

        if await user_model.find_one({"phone_number": user_data.phone_number}):

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already exists")

        if user_data.password != user_data.confirm_password:

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The passwords don't match")

        salt = generate_salt()
        hashed_password = hash_password(user_data.password, salt)

        user_data_dict = user_data.dict()
        user_data_dict["date_joined"] = datetime.now()

        user = user_model(**user_data_dict)

        service = AuthServices()

        for k, v in user_data_dict.items():

            if k == 'email':

                auth_user = await service.check_user(v)

                if auth_user:

                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

            elif k == 'phone_number':

                auth_user = await service.check_user(v)

                if auth_user:

                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already exists")
            else:

                pass

        auth = auth_model(
            email=user_data.email,
            hashed_password=hashed_password,
            salt=salt,
            phone_number=user_data.phone_number,
            role=user_data.role,
            is_active=True,
            is_superuser=False,
            is_verified=False,
            last_login=datetime.now(),
        )

        await auth.create()
        await user.create()

        return user
    except HTTPException as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/register/company", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def register_company(company_data: CompanyCreate):
    try:

        if await company_model.find_one({"email": company_data.email}):

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

        if await company_model.find_one({"phone_number": company_data.phone_number}):

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already exists")

        if await company_model.find_one({"company_inn": company_data.company_inn}):

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INN already exists")

        if company_data.password != company_data.confirm_password:

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The passwords don't match")

        salt = generate_salt()
        hashed_password = hash_password(company_data.password, salt)

        company_data_dict = company_data.dict()
        company_data_dict["date_joined"] = datetime.now()

        company = company_model(**company_data_dict)

        service = AuthServices()

        for k, v in company_data_dict.items():

            if k == 'email':

                auth_user = await service.check_user(v)

                if auth_user:

                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

            elif k == 'phone_number':

                auth_user = await service.check_user(v)

                if auth_user:

                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already exists")

            elif k == 'company_inn':

                auth_user = await service.check_user(v)

                if auth_user:

                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INN already exists")

            else:

                pass

        auth = auth_model(
            email=company_data.email,
            hashed_password=hashed_password,
            salt=salt,
            inn=company_data.company_inn,
            phone_number=company_data.phone_number,
            role=company_data.role,
            is_active=True,
            is_superuser=False,
            is_verified=False,
            last_login=datetime.now(),
        )

        await company.create()
        await auth.create()

        return company

    except HTTPException as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/token", response_model=Token)
async def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        service = AuthServices()

        user = await service.authenticate(form_data.username, form_data.password)

        if not user:

            raise HTTPException(detail="Invalid username or password", status_code=status.HTTP_401_UNAUTHORIZED)

        data_token = convert_objectid_to_str(user, AuthSchemas)
        jwt_token = generate_jwt_token(data_token)

        return jwt_token

    except HTTPException as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/refresh_token", response_model=Token)
async def refresh_token_get(refresh_token: str = Depends(oauth2_scheme)):
    try:
        decoded_data = verify_jwt_token(refresh_token)

        service = AuthServices()

        if not decoded_data:
            raise HTTPException(status_code=400, detail="Invalid token")

        user = await service.find_user(decoded_data['sub'])

        if not user:

            raise HTTPException(status_code=401, detail="Invalid user or company")

        token = generate_jwt_token(decoded_data)

        return token

    except HTTPException as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
