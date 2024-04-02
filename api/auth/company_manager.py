from typing import Optional
from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin
from models.register import Company, get_company_db
from api.auth.user_manager import SECRET, get_jwt_strategy, bearer_transport


class CompanyManager(ObjectIDIDMixin, BaseUserManager[Company, PydanticObjectId]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, company: Company, request: Optional[Request] = None):
        print(f"Company {company.id} has registered.")

    async def on_after_forgot_password(
        self, company: Company, token: str, request: Optional[Request] = None
    ):
        print(f"Company {company.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, company: Company, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for company {company.id}. Verification token: {token}")


async def get_company_manager(company_db: BeanieUserDatabase = Depends(get_company_db)):
    yield CompanyManager(company_db)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_company = FastAPIUsers[Company, PydanticObjectId](get_company_manager, [auth_backend])

# current_active_user = fastapi_company.current_user(active=True)
