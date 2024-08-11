from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from meetup_organizer.database.database import get_database_session
from meetup_organizer.database.models import UserDb
from meetup_organizer.schemas.token import Token
from meetup_organizer.shared.security import (
    create_access_token,
    verify_password,
)

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    dependencies=[],
)

FormData = Annotated[OAuth2PasswordRequestForm, Depends()]
Database = Annotated[Session, Depends(get_database_session)]


@router.post('/', response_model=Token)
async def login_for_access_token(
    form_data: FormData,
    database: Database,
):
    user_db = database.scalar(
        select(UserDb).where(UserDb.username == form_data.username)
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Username not found!',
        )

    if not verify_password(form_data.password, user_db.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect password',
        )

    access_token = create_access_token(data={'sub': user_db.username})

    return {'access_token': access_token, 'token_type': 'bearer'}
