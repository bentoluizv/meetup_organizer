from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from meetup_organizer.database.database import get_database_session
from meetup_organizer.database.models import UserDb
from meetup_organizer.schemas.token import TokenData
from meetup_organizer.shared.settings import Settings

ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = PasswordHash.recommended()


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    encoded_jwt = encode(
        payload=to_encode,
        key=Settings().SECRET_KEY,  # type: ignore
        algorithm=Settings().ALGORITHM,  # type: ignore
    )
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(
    session: Annotated[Session, Depends(get_database_session)],
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='auth'))],
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            jwt=token,
            key=Settings().SECRET_KEY,  # type: ignore
            algorithms=[Settings().ALGORITHM],  # type: ignore
        )
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except DecodeError:
        raise credentials_exception

    user = session.scalar(
        select(UserDb).where(UserDb.username == token_data.username)
    )

    if not user:
        raise credentials_exception

    return user
