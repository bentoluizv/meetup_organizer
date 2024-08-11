from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from meetup_organizer.database.database import get_database_session
from meetup_organizer.database.models import UserDb
from meetup_organizer.schemas.user import CreationalUserSchema, User
from meetup_organizer.shared.security import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(get_current_user)],
)

Database = Annotated[Session, Depends(get_database_session)]


@router.post('/', status_code=HTTPStatus.CREATED)
def create_user(
    user_data: CreationalUserSchema,
    database: Database,
):
    new_user = User.create(user_data)
    user_db = UserDb(**new_user.model_dump())

    stmt = select(UserDb).where(UserDb.username == user_db.username)

    exists = database.scalar(stmt)

    if exists:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Username already exists',
        )

    database.add(user_db)
    database.commit()
