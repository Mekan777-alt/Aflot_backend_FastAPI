from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from models import contacts, feedback
from schemas.contact.contact_schemas import ContactSchema
from api.auth.auth import get_current_user
from typing import Annotated

router = APIRouter()


@router.get('/contacts', status_code=status.HTTP_200_OK, response_model=contacts)
async def get_contact_service(current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        contacts_service = await contacts.find_one()

        if not contacts_service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')

        return contacts_service

    except HTTPException as e:
        return HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/feedback', status_code=status.HTTP_201_CREATED, response_model=feedback)
async def send_feedback(request: ContactSchema, current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        new_feedback = feedback(**request.dict())

        await new_feedback.create()

        return new_feedback

    except HTTPException as e:

        return HTTPException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
