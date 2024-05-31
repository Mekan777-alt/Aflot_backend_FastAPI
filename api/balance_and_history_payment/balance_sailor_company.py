from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from api.auth.config import get_current_user
from typing import Annotated, List
from models import auth, user_model
from schemas.balance.payment_details import PaymentDetails, PaymentHistory

router = APIRouter()


@router.get('/balance', response_model=PaymentDetails, status_code=status.HTTP_200_OK,
            summary="Возвращает баланс пользователя и компании")
async def balance_sailor_company(current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        user_id = current_user.get('id')

        user_info = await auth.get(user_id)

        if not user_info:

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        resume = await user_model.get(user_info.resumeID)

        count_history = sum(resume.payment_history) if resume.payment_history is not None else 0


        data = PaymentDetails(
            balance=resume.balance,
            autofill=resume.autofill,
            count_history=count_history,
        )

        return data
    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/balance/history', response_model=List[PaymentHistory], status_code=status.HTTP_200_OK,
            summary="Возваращает историю пополнение пользователя и компании")
async def history_payment(current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        user_id = current_user.get('id')

        user_info = await auth.get(user_id)

        if not user_info:

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        resume = await user_model.get(user_info.resumeID)

        history = resume.payment_history if resume.payment_history is not None else []

        return history

    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)
