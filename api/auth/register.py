from fastapi import APIRouter
from fastapi import Depends, HTTPException
from models.register import UserModel, CompanyModel
from models.register import db
from .config import pwd_context, create_jwt_token, generate_salt, hash_password
from schemas.auth.auth import UserCreate, UserRead, CompanyRead, CompanyCreate
from starlette import status
from api.auth.auth import UserAuthService, CompanyAuthService
from schemas.auth.auth import Token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/api/v1"
)


@router.post("/register/user", response_model=UserRead)
async def register_user(user_data: UserCreate):
    try:

        collection = db['User']

        if await collection.find_one({"email": user_data.email}):

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")


        if user_data.password != user_data.confirm_password:

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The passwords don't match")

        salt = generate_salt()
        hashed_password = hash_password(user_data.password, salt)

        user_data.password = hashed_password
        user_data.salt = salt

        user_data.role = 'sailor'

        user = UserModel(**user_data.dict())

        await user.create()

        return user
    except HTTPException as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/register/company", response_model=CompanyRead)
async def register_company(company_data: CompanyCreate):
    try:

        collection = db['Company']

        if await collection.find_one({"email": company_data.email}):

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")


        if company_data.password != company_data.confirm_password:

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The passwords don't match")

        salt = generate_salt()
        hashed_password = hash_password(company_data.password, salt)

        company_data.password = hashed_password
        company_data.salt = salt

        company_data.role = 'company'

        company = CompanyModel(**company_data.dict())

        await company.create()

        return company

    except HTTPException as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/token", response_model=Token)
async def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user_service = UserAuthService()
        company_service = CompanyAuthService()

        user = await user_service.authenticate(form_data.username, form_data.password)
        company = await company_service.authenticate(form_data.username, form_data.password)
        if not user and not company:
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        if user:
            jwt_token = create_jwt_token({"sub": form_data.username, 'role': user.role})
            return {"access_token": jwt_token, "token_type": "bearer"}

        if company:
            jwt_token = create_jwt_token({"sub": form_data.username, 'role': company.role})
            return {"access_token": jwt_token, "token_type": "bearer"}

    except HTTPException as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
